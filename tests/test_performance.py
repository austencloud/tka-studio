"""
Performance & Load Tests - Phase 3

Comprehensive performance validation of microservices infrastructure
under various load conditions and stress scenarios.
"""

import pytest
import time
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from unittest.mock import Mock, patch
import psutil
import gc
from typing import List, Dict, Any

from desktop.modern.core.events.event_bus import TypeSafeEventBus, EventPriority
from desktop.modern.core.events.domain_events import (
    SequenceUpdatedEvent,
    UIStateChangedEvent,
    BeatAddedEvent,
    BeatUpdatedEvent
)
from desktop.modern.presentation.tabs.construct.infrastructure.event_integration import (
    ConstructTabEventIntegration
)
from desktop.modern.presentation.tabs.construct.infrastructure.resilient_panel_factory import (
    CircuitBreaker,
    CircuitBreakerConfig,
    ResilientPanelFactory
)
from desktop.modern.presentation.tabs.construct.infrastructure.service_mesh import (
    ComponentServiceMesh
)


class TestEventBusPerformance:
    """Test event bus performance under various load conditions."""
    
    @pytest.fixture
    def event_bus(self):
        """Create event bus for performance testing."""
        return TypeSafeEventBus()
    
    @pytest.fixture
    def performance_components(self):
        """Create components for performance testing."""
        components = {}
        for i in range(20):  # Many components
            component = Mock()
            component.process_event = Mock(return_value=f"processed_{i}")
            components[f"component_{i}"] = component
        return components
    
    def test_high_volume_synchronous_events(self, event_bus):
        """Test event bus performance under high synchronous load."""
        events_received = []
        processing_times = []
        
        def performance_handler(event):
            start_time = time.time()
            events_received.append(event)
            # Simulate processing work
            time.sleep(0.001)  # 1ms processing time
            processing_times.append(time.time() - start_time)
        
        event_bus.subscribe("sequence.updated", performance_handler)
        
        # Publish large number of events
        start_time = time.time()
        num_events = 1000
        
        for i in range(num_events):
            event = SequenceUpdatedEvent(
                sequence_id=f"perf_seq_{i}",
                change_type="performance_test"
            )
            event_bus.publish(event)
        
        end_time = time.time()
        
        # Verify all events were processed
        assert len(events_received) == num_events
        
        # Calculate performance metrics
        total_time = end_time - start_time
        throughput = num_events / total_time
        avg_processing_time = sum(processing_times) / len(processing_times)
        
        print(f"Synchronous throughput: {throughput:.2f} events/second")
        print(f"Average processing time: {avg_processing_time*1000:.2f}ms")
        
        # Performance assertions
        assert throughput > 500  # Should handle at least 500 events/second
        assert avg_processing_time < 0.01  # Average processing < 10ms
    
    @pytest.mark.asyncio
    async def test_high_volume_asynchronous_events(self, event_bus):
        """Test event bus performance under high asynchronous load."""
        events_received = []
        processing_times = []
        
        async def async_performance_handler(event):
            start_time = time.time()
            events_received.append(event)
            # Simulate async processing work
            await asyncio.sleep(0.001)  # 1ms async processing
            processing_times.append(time.time() - start_time)
        
        event_bus.subscribe("sequence.updated", async_performance_handler)
        
        # Publish large number of events asynchronously
        start_time = time.time()
        num_events = 1000
        
        tasks = []
        for i in range(num_events):
            event = SequenceUpdatedEvent(
                sequence_id=f"async_perf_{i}",
                change_type="async_performance_test"
            )
            task = event_bus.publish_async(event)
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Verify all events were processed
        assert len(events_received) == num_events
        
        # Calculate performance metrics
        total_time = end_time - start_time
        throughput = num_events / total_time
        avg_processing_time = sum(processing_times) / len(processing_times)
        
        print(f"Asynchronous throughput: {throughput:.2f} events/second")
        print(f"Average async processing time: {avg_processing_time*1000:.2f}ms")
        
        # Async should be significantly faster
        assert throughput > 1000  # Should handle at least 1000 events/second
        assert avg_processing_time < 0.005  # Average processing < 5ms
    
    def test_memory_usage_with_many_subscriptions(self, event_bus):
        """Test memory efficiency with large number of subscriptions."""
        import gc
        
        # Measure initial memory
        gc.collect()
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        handlers = []
        subscription_ids = []
        
        # Create many subscriptions
        for i in range(2000):
            def handler(event, i=i):
                return f"handler_{i}_processed"
            
            handlers.append(handler)
            sub_id = event_bus.subscribe("sequence.updated", handler)
            subscription_ids.append(sub_id)
        
        # Measure memory after subscriptions
        gc.collect()
        after_subscription_memory = process.memory_info().rss
        subscription_memory_delta = (after_subscription_memory - initial_memory) / 1024 / 1024  # MB
        
        # Publish events to trigger handlers
        for i in range(200):
            event = SequenceUpdatedEvent(
                sequence_id=f"memory_test_{i}",
                change_type="memory_test"
            )
            event_bus.publish(event)
        
        # Measure memory after event processing
        gc.collect()
        after_processing_memory = process.memory_info().rss
        processing_memory_delta = (after_processing_memory - after_subscription_memory) / 1024 / 1024  # MB
        
        # Clean up subscriptions
        for sub_id in subscription_ids:
            event_bus.unsubscribe(sub_id)
        
        # Measure memory after cleanup
        gc.collect()
        final_memory = process.memory_info().rss
        cleanup_memory_delta = (final_memory - initial_memory) / 1024 / 1024  # MB
        
        print(f"Memory usage - Subscriptions: {subscription_memory_delta:.2f}MB")
        print(f"Memory usage - Processing: {processing_memory_delta:.2f}MB")
        print(f"Memory usage - After cleanup: {cleanup_memory_delta:.2f}MB")
        
        # Memory assertions
        assert subscription_memory_delta < 100  # Subscriptions should use < 100MB
        assert processing_memory_delta < 50   # Processing should use < 50MB
        assert cleanup_memory_delta < 10     # Cleanup should restore memory < 10MB overhead
        
        # Verify cleanup
        assert event_bus.get_subscription_count() == 0
    
    def test_concurrent_publish_subscribe_operations(self, event_bus):
        """Test concurrent publish/subscribe operations for thread safety."""
        events_received = []
        subscription_ids = []
        lock = threading.Lock()
        
        def threadsafe_handler(event):
            with lock:
                events_received.append(event.sequence_id)
        
        def subscriber_thread():
            """Thread that continuously subscribes/unsubscribes."""
            for i in range(50):
                sub_id = event_bus.subscribe("sequence.updated", threadsafe_handler)
                subscription_ids.append(sub_id)
                time.sleep(0.001)
        
        def publisher_thread():
            """Thread that continuously publishes events."""
            for i in range(100):
                event = SequenceUpdatedEvent(
                    sequence_id=f"concurrent_{threading.current_thread().ident}_{i}",
                    change_type="concurrent_test"
                )
                event_bus.publish(event)
                time.sleep(0.001)
        
        # Start concurrent threads
        threads = []
        
        # Start subscriber threads
        for i in range(3):
            thread = threading.Thread(target=subscriber_thread)
            threads.append(thread)
            thread.start()
        
        # Start publisher threads
        for i in range(5):
            thread = threading.Thread(target=publisher_thread)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify thread safety
        assert len(events_received) > 0  # Some events should be processed
        assert len(subscription_ids) > 0  # Some subscriptions should be created
        
        # No exceptions should occur during concurrent operations
        print(f"Concurrent test - Events processed: {len(events_received)}")
        print(f"Concurrent test - Subscriptions created: {len(subscription_ids)}")
    
    def test_event_priority_performance(self, event_bus):
        """Test event priority handling performance."""
        high_priority_events = []
        low_priority_events = []
        processing_order = []
        
        def priority_handler(event):
            processing_order.append((event.priority.value, event.sequence_id))
            if event.priority == EventPriority.HIGH:
                high_priority_events.append(event)
            elif event.priority == EventPriority.LOW:
                low_priority_events.append(event)
        
        event_bus.subscribe("sequence.created", priority_handler)
        
        # Create events with mixed priorities
        events_to_publish = []
        
        for i in range(100):
            # Mix of high and low priority events
            if i % 2 == 0:
                event = SequenceUpdatedEvent(
                    sequence_id=f"high_priority_{i}",
                    change_type="high_priority_test",
                    priority=EventPriority.HIGH
                )
            else:
                event = SequenceUpdatedEvent(
                    sequence_id=f"low_priority_{i}",
                    change_type="low_priority_test",
                    priority=EventPriority.LOW
                )
            events_to_publish.append(event)
        
        # Publish all events
        start_time = time.time()
        
        for event in events_to_publish:
            event_bus.publish(event)
        
        end_time = time.time()
        
        # Verify priority ordering
        assert len(processing_order) == 100
        
        # Check that high priority events tend to be processed first
        high_priority_positions = []
        low_priority_positions = []
        
        for i, (priority, seq_id) in enumerate(processing_order):
            if priority == EventPriority.HIGH.value:
                high_priority_positions.append(i)
            elif priority == EventPriority.LOW.value:
                low_priority_positions.append(i)
        
        # Calculate average positions
        avg_high_position = sum(high_priority_positions) / len(high_priority_positions)
        avg_low_position = sum(low_priority_positions) / len(low_priority_positions)
        
        print(f"Average high priority position: {avg_high_position:.2f}")
        print(f"Average low priority position: {avg_low_position:.2f}")
        
        # High priority should generally be processed before low priority
        assert avg_high_position < avg_low_position
        
        # Performance should not be significantly impacted
        total_time = end_time - start_time
        throughput = 100 / total_time
        assert throughput > 500  # Should still handle 500+ events/second with priorities


class TestCircuitBreakerLoadTests:
    """Test circuit breaker performance under load conditions."""
    
    @pytest.fixture
    def load_test_circuit_breaker(self):
        """Create circuit breaker for load testing."""
        config = CircuitBreakerConfig(
            failure_threshold=50,
            recovery_timeout=5.0,
            success_threshold=10
        )
        return CircuitBreaker("load_test_component", config)
    
    def test_concurrent_requests(self, load_test_circuit_breaker):
        """Test circuit breaker under concurrent load."""
        results = []
        results_lock = threading.Lock()
        
        def simulate_request():
            if load_test_circuit_breaker.can_execute():
                # Simulate 70% success rate
                import random
                if random.random() < 0.7:
                    load_test_circuit_breaker.record_success()
                    with results_lock:
                        results.append("success")
                else:
                    load_test_circuit_breaker.record_failure(Exception("Simulated failure"))
                    with results_lock:
                        results.append("failure")
            else:
                with results_lock:
                    results.append("blocked")
        
        # Execute concurrent requests
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(simulate_request) for _ in range(2000)]
            for future in as_completed(futures):
                future.result()  # Wait for completion
        
        end_time = time.time()
        
        # Analyze results
        success_count = results.count("success")
        failure_count = results.count("failure")
        blocked_count = results.count("blocked")
        
        total_requests = len(results)
        execution_time = end_time - start_time
        throughput = total_requests / execution_time
        
        print(f"Load test results:")
        print(f"  Success: {success_count}")
        print(f"  Failure: {failure_count}")
        print(f"  Blocked: {blocked_count}")
        print(f"  Throughput: {throughput:.2f} requests/second")
        
        # Assertions
        assert total_requests == 2000
        assert success_count > 0  # Some requests should succeed
        assert throughput > 1000  # Should handle at least 1000 requests/second
        
        # Circuit breaker should provide protection
        if failure_count > 50:  # If enough failures occurred
            assert blocked_count > 0  # Some requests should be blocked
    
    def test_circuit_breaker_recovery_timing(self):
        """Test circuit breaker recovery timing accuracy under load."""
        config = CircuitBreakerConfig(
            failure_threshold=10,
            recovery_timeout=2.0  # 2 seconds
        )
        circuit_breaker = CircuitBreaker("timing_test", config)
        
        # Trigger circuit breaker opening
        for i in range(10):
            circuit_breaker.record_failure(Exception(f"Failure {i}"))
        
        assert circuit_breaker.state.value == "open"
        assert not circuit_breaker.can_execute()
        
        # Test timing accuracy
        open_time = time.time()
        
        # Should not execute immediately
        time.sleep(1.0)
        assert not circuit_breaker.can_execute()
        
        # Should not execute at 1.5 seconds
        time.sleep(0.5)
        assert not circuit_breaker.can_execute()
        
        # Should allow execution after timeout
        time.sleep(0.6)  # Total 2.1 seconds
        half_open_time = time.time()
        
        assert circuit_breaker.can_execute()
        assert circuit_breaker.state.value == "half_open"
        
        # Verify timing accuracy
        actual_timeout = half_open_time - open_time
        expected_timeout = 2.0
        timing_accuracy = abs(actual_timeout - expected_timeout)
        
        print(f"Expected timeout: {expected_timeout}s")
        print(f"Actual timeout: {actual_timeout:.3f}s")
        print(f"Timing accuracy: {timing_accuracy:.3f}s")
        
        # Should be accurate within 200ms
        assert timing_accuracy < 0.2
    
    def test_circuit_breaker_statistics_accuracy(self):
        """Test circuit breaker statistics accuracy under load."""
        config = CircuitBreakerConfig(failure_threshold=100)  # High threshold
        circuit_breaker = CircuitBreaker("stats_test", config)
        
        # Generate known pattern of requests
        expected_successes = 0
        expected_failures = 0
        
        # Pattern: 3 successes, 1 failure, repeat
        for cycle in range(250):  # 1000 total requests
            for i in range(3):
                circuit_breaker.record_success()
                expected_successes += 1
            
            circuit_breaker.record_failure(Exception("Pattern failure"))
            expected_failures += 1
        
        # Verify statistics
        stats = circuit_breaker.get_stats()
        
        assert stats["total_requests"] == 1000
        assert stats["successful_requests"] == expected_successes
        assert stats["failed_requests"] == expected_failures
        assert stats["success_rate"] == 75.0  # 3/4 = 75%
        assert stats["failure_rate"] == 25.0  # 1/4 = 25%
        
        print(f"Statistics accuracy test:")
        print(f"  Total requests: {stats['total_requests']}")
        print(f"  Success rate: {stats['success_rate']}%")
        print(f"  Failure rate: {stats['failure_rate']}%")
    
    def test_multiple_circuit_breakers_isolation(self):
        """Test isolation between multiple circuit breakers under load."""
        # Create multiple circuit breakers
        circuit_breakers = {}
        for i in range(5):
            config = CircuitBreakerConfig(failure_threshold=20)
            circuit_breakers[f"cb_{i}"] = CircuitBreaker(f"component_{i}", config)
        
        # Simulate different failure patterns for each
        def simulate_component_load(cb_name, failure_rate):
            cb = circuit_breakers[cb_name]
            results = {"success": 0, "failure": 0, "blocked": 0}
            
            for i in range(100):
                if cb.can_execute():
                    import random
                    if random.random() < failure_rate:
                        cb.record_failure(Exception("Load test failure"))
                        results["failure"] += 1
                    else:
                        cb.record_success()
                        results["success"] += 1
                else:
                    results["blocked"] += 1
            
            return results
        
        # Execute with different failure rates
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(simulate_component_load, "cb_0", 0.1): "cb_0",  # 10% failure
                executor.submit(simulate_component_load, "cb_1", 0.3): "cb_1",  # 30% failure
                executor.submit(simulate_component_load, "cb_2", 0.5): "cb_2",  # 50% failure
                executor.submit(simulate_component_load, "cb_3", 0.7): "cb_3",  # 70% failure
                executor.submit(simulate_component_load, "cb_4", 0.9): "cb_4",  # 90% failure
            }
            
            results = {}
            for future in as_completed(futures):
                cb_name = futures[future]
                results[cb_name] = future.result()
        
        # Verify isolation
        print("Circuit breaker isolation test results:")
        for cb_name, result in results.items():
            cb = circuit_breakers[cb_name]
            state = cb.state.value
            print(f"  {cb_name}: {result}, state: {state}")
        
        # Low failure rate components should remain closed
        assert circuit_breakers["cb_0"].state.value == "closed"
        assert circuit_breakers["cb_1"].state.value == "closed"
        
        # High failure rate components should open
        assert circuit_breakers["cb_3"].state.value == "open"
        assert circuit_breakers["cb_4"].state.value == "open"


class TestIntegratedSystemPerformance:
    """Test performance of integrated microservices system."""
    
    @pytest.fixture
    def integrated_performance_system(self):
        """Setup integrated system for performance testing."""
        event_bus = TypeSafeEventBus()
        event_integration = ConstructTabEventIntegration(event_bus)
        service_mesh = ComponentServiceMesh()
        
        # Create many mock components
        components = {}
        for i in range(15):
            component = Mock()
            component.process_event = Mock(return_value=f"processed_{i}")
            component.handle_sequence_update = Mock(return_value=f"updated_{i}")
            components[f"component_{i}"] = component
        
        # Setup integrations
        event_integration.setup_event_handlers(components)
        proxied_components = service_mesh.setup_mesh_for_construct_tab(components)
        
        return {
            "event_bus": event_bus,
            "event_integration": event_integration,
            "service_mesh": service_mesh,
            "components": components,
            "proxied_components": proxied_components,
        }
    
    def test_end_to_end_throughput(self, integrated_performance_system):
        """Test end-to-end throughput of integrated system."""
        system = integrated_performance_system
        event_bus = system["event_bus"]
        
        # Track processing
        events_processed = []
        
        def throughput_tracker(event):
            events_processed.append(time.time())
        
        event_bus.subscribe("sequence.updated", throughput_tracker)
        
        # Generate high-volume event stream
        num_events = 1000
        start_time = time.time()
        
        for i in range(num_events):
            event = SequenceUpdatedEvent(
                sequence_id=f"throughput_test_{i}",
                change_type="throughput_test"
            )
            event_bus.publish(event)
        
        end_time = time.time()
        
        # Calculate throughput
        total_time = end_time - start_time
        throughput = num_events / total_time
        
        print(f"End-to-end throughput: {throughput:.2f} events/second")
        
        # Should maintain good throughput despite complexity
        assert len(events_processed) == num_events
        assert throughput > 400  # Should handle at least 400 events/second
    
    @pytest.mark.asyncio
    async def test_async_system_performance(self, integrated_performance_system):
        """Test async performance of integrated system."""
        system = integrated_performance_system
        event_bus = system["event_bus"]
        
        # Track async processing
        async_events_processed = []
        
        async def async_throughput_tracker(event):
            await asyncio.sleep(0.001)  # Simulate async work
            async_events_processed.append(time.time())
        
        event_bus.subscribe("sequence.updated", async_throughput_tracker)
        
        # Generate async event stream
        num_events = 500
        start_time = time.time()
        
        tasks = []
        for i in range(num_events):
            event = SequenceUpdatedEvent(
                sequence_id=f"async_throughput_{i}",
                change_type="async_test"
            )
            task = event_bus.publish_async(event)
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Calculate async throughput
        total_time = end_time - start_time
        throughput = num_events / total_time
        
        print(f"Async system throughput: {throughput:.2f} events/second")
        
        # Async should be faster
        assert len(async_events_processed) == num_events
        assert throughput > 800  # Should handle at least 800 events/second async
    
    def test_system_memory_efficiency(self, integrated_performance_system):
        """Test memory efficiency of integrated system."""
        system = integrated_performance_system
        event_bus = system["event_bus"]
        
        # Measure baseline memory
        gc.collect()
        process = psutil.Process()
        baseline_memory = process.memory_info().rss
        
        # Generate sustained load
        for cycle in range(100):
            # Create event batch
            events = [
                SequenceUpdatedEvent(
                    sequence_id=f"memory_test_{cycle}_{i}",
                    change_type="memory_test"
                )
                for i in range(50)
            ]
            
            # Process event batch
            for event in events:
                event_bus.publish(event)
            
            # Periodic memory check
            if cycle % 25 == 0:
                gc.collect()
                current_memory = process.memory_info().rss
                memory_delta = (current_memory - baseline_memory) / 1024 / 1024  # MB
                print(f"Cycle {cycle}: Memory delta: {memory_delta:.2f}MB")
        
        # Final memory check
        gc.collect()
        final_memory = process.memory_info().rss
        total_memory_delta = (final_memory - baseline_memory) / 1024 / 1024  # MB
        
        print(f"Total memory delta after 5000 events: {total_memory_delta:.2f}MB")
        
        # Memory should remain reasonable
        assert total_memory_delta < 200  # Should use less than 200MB additional
    
    def test_system_resilience_under_load(self, integrated_performance_system):
        """Test system resilience under combined load and failures."""
        system = integrated_performance_system
        event_bus = system["event_bus"]
        service_mesh = system["service_mesh"]
        
        # Configure some components to fail under load
        components = system["components"]
        failing_components = ["component_5", "component_10", "component_14"]
        
        for comp_name in failing_components:
            if comp_name in components:
                components[comp_name].process_event.side_effect = Exception("Load failure")
        
        # Track successful processing
        successful_events = []
        
        def resilience_tracker(event):
            successful_events.append(event.sequence_id)
        
        event_bus.subscribe("sequence.updated", resilience_tracker)
        
        # Generate load with failures
        num_events = 1000
        start_time = time.time()
        
        for i in range(num_events):
            event = SequenceUpdatedEvent(
                sequence_id=f"resilience_test_{i}",
                change_type="resilience_test"
            )
            event_bus.publish(event)
        
        end_time = time.time()
        
        # System should continue functioning despite failures
        assert len(successful_events) == num_events  # Events still tracked
        
        # Check circuit breaker states
        cb_statuses = {}
        for comp_name in failing_components:
            if comp_name in service_mesh.circuit_breakers:
                status = service_mesh.get_circuit_breaker_status(comp_name)
                cb_statuses[comp_name] = status["state"]
        
        print(f"Resilience test - Events processed: {len(successful_events)}")
        print(f"Circuit breaker states: {cb_statuses}")
        
        # System should maintain performance
        total_time = end_time - start_time
        throughput = num_events / total_time
        assert throughput > 300  # Should maintain at least 300 events/second


class TestScalabilityCharacteristics:
    """Test scalability characteristics of the microservices infrastructure."""
    
    def test_scaling_with_component_count(self):
        """Test system performance scaling with number of components."""
        throughput_results = {}
        
        # Test with different numbers of components
        component_counts = [5, 10, 20, 50]
        
        for count in component_counts:
            event_bus = TypeSafeEventBus()
            event_integration = ConstructTabEventIntegration(event_bus)
            
            # Create specified number of components
            components = {}
            for i in range(count):
                component = Mock()
                component.process_event = Mock(return_value=f"processed_{i}")
                components[f"component_{i}"] = component
            
            event_integration.setup_event_handlers(components)
            
            # Measure throughput
            events_processed = []
            
            def scaling_tracker(event):
                events_processed.append(event.sequence_id)
            
            event_bus.subscribe("sequence.updated", scaling_tracker)
            
            # Generate test load
            num_events = 500
            start_time = time.time()
            
            for i in range(num_events):
                event = SequenceUpdatedEvent(
                    sequence_id=f"scale_test_{count}_{i}",
                    change_type="scaling_test"
                )
                event_bus.publish(event)
            
            end_time = time.time()
            
            # Calculate throughput
            total_time = end_time - start_time
            throughput = num_events / total_time
            throughput_results[count] = throughput
            
            print(f"Components: {count}, Throughput: {throughput:.2f} events/second")
        
        # Analyze scaling characteristics
        print("\nScaling analysis:")
        for count in component_counts:
            print(f"  {count} components: {throughput_results[count]:.2f} events/sec")
        
        # Should scale reasonably (not necessarily linearly)
        # Throughput shouldn't drop dramatically with more components
        min_throughput = min(throughput_results.values())
        max_throughput = max(throughput_results.values())
        
        # Throughput should remain within reasonable bounds
        assert min_throughput > 100  # Minimum acceptable throughput
        assert max_throughput / min_throughput < 10  # No more than 10x difference
    
    def test_memory_scaling_characteristics(self):
        """Test memory usage scaling with system complexity."""
        memory_results = {}
        component_counts = [10, 25, 50]
        
        for count in component_counts:
            # Measure baseline memory
            gc.collect()
            process = psutil.Process()
            baseline_memory = process.memory_info().rss
            
            # Create system with specified complexity
            event_bus = TypeSafeEventBus()
            event_integration = ConstructTabEventIntegration(event_bus)
            service_mesh = ComponentServiceMesh()
            
            components = {}
            for i in range(count):
                component = Mock()
                components[f"component_{i}"] = component
            
            event_integration.setup_event_handlers(components)
            service_mesh.setup_mesh_for_construct_tab(components)
            
            # Measure memory after setup
            gc.collect()
            setup_memory = process.memory_info().rss
            memory_delta = (setup_memory - baseline_memory) / 1024 / 1024  # MB
            memory_results[count] = memory_delta
            
            print(f"Components: {count}, Memory usage: {memory_delta:.2f}MB")
            
            # Cleanup for next iteration
            event_integration.shutdown()
        
        # Analyze memory scaling
        print("\nMemory scaling analysis:")
        for count in component_counts:
            print(f"  {count} components: {memory_results[count]:.2f}MB")
        
        # Memory usage should scale reasonably
        max_memory = max(memory_results.values())
        assert max_memory < 500  # Should use less than 500MB even with 50 components
        
        # Should show roughly linear scaling (within bounds)
        memory_per_component_50 = memory_results[50] / 50
        memory_per_component_10 = memory_results[10] / 10
        
        # Memory per component shouldn't increase dramatically
        assert memory_per_component_50 / memory_per_component_10 < 3
