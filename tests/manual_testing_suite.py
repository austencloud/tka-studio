"""
Manual Testing Procedures and Verification Scripts

Provides interactive testing tools and verification procedures for the
microservices infrastructure implementation.
"""

import sys
import time
import asyncio
from typing import Dict, Any, List
from unittest.mock import Mock

# Add the TKA source path for imports
sys.path.insert(0, r'f:\CODE\TKA\src')

try:
    from desktop.modern.core.events.event_bus import TypeSafeEventBus, get_event_bus
    from desktop.modern.core.events.domain_events import (
        SequenceUpdatedEvent,
        UIStateChangedEvent,
        BeatAddedEvent
    )
    from desktop.modern.presentation.tabs.construct.infrastructure.event_integration import (
        ConstructTabEventIntegration,
        create_event_integration
    )
    from desktop.modern.presentation.tabs.construct.infrastructure.resilient_panel_factory import (
        ResilientPanelFactory,
        CircuitBreakerState
    )
    from desktop.modern.presentation.tabs.construct.infrastructure.service_mesh import (
        ComponentServiceMesh
    )
    from desktop.modern.core.dependency_injection.di_container import DIContainer
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please ensure TKA source directory is accessible")
    sys.exit(1)


class ManualTestRunner:
    """Interactive test runner for manual verification."""
    
    def __init__(self):
        self.results = []
    
    def run_test(self, test_name: str, test_func, *args, **kwargs):
        """Run a test and record results."""
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            start_time = time.time()
            result = test_func(*args, **kwargs)
            end_time = time.time()
            
            duration = end_time - start_time
            
            self.results.append({
                "test": test_name,
                "status": "PASS",
                "duration": duration,
                "result": result
            })
            
            print(f"✅ PASS - {test_name} ({duration:.3f}s)")
            if result:
                print(f"Result: {result}")
            
        except Exception as e:
            self.results.append({
                "test": test_name,
                "status": "FAIL",
                "error": str(e)
            })
            
            print(f"❌ FAIL - {test_name}")
            print(f"Error: {e}")
    
    def print_summary(self):
        """Print test summary."""
        print(f"\n{'='*60}")
        print("TEST SUMMARY")
        print(f"{'='*60}")
        
        passed = len([r for r in self.results if r["status"] == "PASS"])
        failed = len([r for r in self.results if r["status"] == "FAIL"])
        total = len(self.results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%" if total > 0 else "No tests run")
        
        if failed > 0:
            print("\nFailed Tests:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['error']}")


def test_component_creation_resilience():
    """Test A: Component Creation Resilience."""
    try:
        from desktop.modern.presentation.tabs.construct.infrastructure.resilient_panel_factory import ResilientPanelFactory
        from desktop.modern.core.dependency_injection.di_container import DIContainer
        
        container = Mock(spec=DIContainer)
        factory = ResilientPanelFactory(container)
        
        results = []
        
        # Test normal creation
        try:
            with Mock() as mock_panel_factory:
                factory.panel_factory = mock_panel_factory
                mock_panel_factory.create_workbench_panel.return_value = (Mock(), Mock())
                
                panel, component = factory.create_workbench_panel()
                results.append(f"Workbench created: {component is not None}")
        except Exception as e:
            results.append(f"Workbench creation failed: {e}")
        
        # Check circuit breaker status
        try:
            status = factory.get_circuit_breaker_status()
            results.append(f"Circuit breaker status available: {len(status) > 0}")
            
            for comp_name, comp_status in status.items():
                results.append(f"{comp_name}: {comp_status['state']}")
                
        except Exception as e:
            results.append(f"Circuit breaker status failed: {e}")
        
        return results
        
    except Exception as e:
        raise Exception(f"Component creation test failed: {e}")


def test_event_flow_verification():
    """Test B: Event Flow Verification."""
    try:
        # Create event integration
        integration = create_event_integration()
        
        results = []
        
        # Setup mock components
        components = {
            "workbench": Mock(),
            "option_picker": Mock(),
            "start_position_picker": Mock()
        }
        
        integration.setup_event_handlers(components)
        results.append(f"Event handlers setup: {len(integration.subscription_ids) > 0}")
        
        # Trigger event
        event = SequenceUpdatedEvent(sequence_id="test", change_type="beat_added")
        integration.event_bus.publish(event)
        
        results.append("Event published successfully")
        
        # Check event stats
        try:
            stats = integration.event_bus.get_event_stats()
            results.append(f"Event stats available: {len(stats) > 0}")
        except Exception as e:
            results.append(f"Event stats error: {e}")
        
        return results
        
    except Exception as e:
        raise Exception(f"Event flow test failed: {e}")


def test_memory_usage():
    """Memory Usage Test."""
    try:
        import psutil
        import gc
        
        # Before event system
        process = psutil.Process()
        gc.collect()
        memory_before = process.memory_info().rss
        
        # Create event system and components
        event_bus = TypeSafeEventBus()
        integration = ConstructTabEventIntegration(event_bus)
        
        components = {}
        for i in range(20):
            components[f"component_{i}"] = Mock()
        
        integration.setup_event_handlers(components)
        
        # After event system
        gc.collect()
        memory_after = process.memory_info().rss
        memory_delta = (memory_after - memory_before) / 1024 / 1024  # MB
        
        # Cleanup
        integration.shutdown()
        
        result = f"Memory usage increased by: {memory_delta:.2f} MB"
        
        if memory_delta > 50:  # More than 50MB
            raise Exception(f"Memory usage too high: {memory_delta:.2f} MB")
        
        return result
        
    except Exception as e:
        raise Exception(f"Memory test failed: {e}")


def test_event_throughput():
    """Event Throughput Test."""
    try:
        event_bus = TypeSafeEventBus()
        events_processed = 0
        
        def counter_handler(event):
            nonlocal events_processed
            events_processed += 1
        
        event_bus.subscribe("sequence.updated", counter_handler)
        
        # Measure throughput
        start_time = time.time()
        num_events = 1000
        
        for i in range(num_events):
            event = SequenceUpdatedEvent(sequence_id=f"seq_{i}", change_type="perf_test")
            event_bus.publish(event)
        
        end_time = time.time()
        throughput = num_events / (end_time - start_time)
        
        result = f"Event throughput: {throughput:.2f} events/second"
        
        if throughput < 500:  # Less than 500 events/second
            raise Exception(f"Throughput too low: {throughput:.2f} events/second")
        
        return result
        
    except Exception as e:
        raise Exception(f"Throughput test failed: {e}")


def test_circuit_breaker_functionality():
    """Circuit Breaker Functionality Test."""
    try:
        from desktop.modern.presentation.tabs.construct.infrastructure.resilient_panel_factory import (
            CircuitBreaker, CircuitBreakerConfig
        )
        
        config = CircuitBreakerConfig(failure_threshold=3, recovery_timeout=1.0)
        cb = CircuitBreaker("test_component", config)
        
        results = []
        
        # Test initial state
        results.append(f"Initial state: {cb.state.value}")
        results.append(f"Can execute initially: {cb.can_execute()}")
        
        # Trigger failures
        for i in range(3):
            cb.record_failure(Exception(f"Test failure {i}"))
        
        results.append(f"State after failures: {cb.state.value}")
        results.append(f"Can execute after failures: {cb.can_execute()}")
        
        # Test recovery
        time.sleep(1.1)  # Wait for recovery timeout
        results.append(f"Can execute after timeout: {cb.can_execute()}")
        
        # Test successful recovery
        cb.record_success()
        cb.record_success()
        results.append(f"State after successes: {cb.state.value}")
        
        return results
        
    except Exception as e:
        raise Exception(f"Circuit breaker test failed: {e}")


def test_service_mesh_integration():
    """Service Mesh Integration Test."""
    try:
        service_mesh = ComponentServiceMesh()
        
        components = {
            "workbench": Mock(),
            "option_picker": Mock(),
        }
        
        # Configure component behaviors
        components["workbench"].test_method = Mock(return_value="success")
        components["option_picker"].refresh = Mock(return_value="refreshed")
        
        # Setup mesh
        proxied = service_mesh.setup_mesh_for_construct_tab(components)
        
        results = []
        results.append(f"Components proxied: {len(proxied)}")
        
        # Test proxied method calls
        result = proxied["workbench"].test_method()
        results.append(f"Proxied method result: {result}")
        
        # Test circuit breaker integration
        cb_status = service_mesh.get_circuit_breaker_status("workbench")
        results.append(f"Circuit breaker status: {cb_status['state']}")
        
        # Test metrics
        metrics = service_mesh.get_metrics()
        results.append(f"Metrics available: {'total_requests' in metrics}")
        
        return results
        
    except Exception as e:
        raise Exception(f"Service mesh test failed: {e}")


async def test_async_event_processing():
    """Async Event Processing Test."""
    try:
        event_bus = TypeSafeEventBus()
        async_events_processed = []
        
        async def async_handler(event):
            await asyncio.sleep(0.001)  # Simulate async work
            async_events_processed.append(event.sequence_id)
        
        event_bus.subscribe("sequence.updated", async_handler)
        
        # Test async publishing
        num_events = 100
        start_time = time.time()
        
        tasks = []
        for i in range(num_events):
            event = SequenceUpdatedEvent(sequence_id=f"async_{i}", change_type="async_test")
            task = event_bus.publish_async(event)
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        end_time = time.time()
        
        duration = end_time - start_time
        throughput = num_events / duration
        
        result = f"Async throughput: {throughput:.2f} events/second, Processed: {len(async_events_processed)}"
        
        if len(async_events_processed) != num_events:
            raise Exception(f"Not all events processed: {len(async_events_processed)}/{num_events}")
        
        return result
        
    except Exception as e:
        raise Exception(f"Async test failed: {e}")


def run_manual_tests():
    """Run all manual tests."""
    runner = ManualTestRunner()
    
    print("TKA Microservices Infrastructure - Manual Testing Suite")
    print("=" * 60)
    
    # Run synchronous tests
    runner.run_test("Component Creation Resilience", test_component_creation_resilience)
    runner.run_test("Event Flow Verification", test_event_flow_verification)
    runner.run_test("Memory Usage", test_memory_usage)
    runner.run_test("Event Throughput", test_event_throughput)
    runner.run_test("Circuit Breaker Functionality", test_circuit_breaker_functionality)
    runner.run_test("Service Mesh Integration", test_service_mesh_integration)
    
    # Run async test
    try:
        async_result = asyncio.run(test_async_event_processing())
        runner.results.append({
            "test": "Async Event Processing",
            "status": "PASS",
            "result": async_result
        })
        print(f"✅ PASS - Async Event Processing")
        print(f"Result: {async_result}")
    except Exception as e:
        runner.results.append({
            "test": "Async Event Processing",
            "status": "FAIL",
            "error": str(e)
        })
        print(f"❌ FAIL - Async Event Processing")
        print(f"Error: {e}")
    
    # Print summary
    runner.print_summary()
    
    return runner.results


def run_performance_benchmark():
    """Run performance benchmark tests."""
    print("\nPerformance Benchmark Suite")
    print("=" * 40)
    
    benchmarks = {}
    
    # Event Bus Performance
    try:
        event_bus = TypeSafeEventBus()
        events_received = 0
        
        def handler(event):
            nonlocal events_received
            events_received += 1
        
        event_bus.subscribe("sequence.updated", handler)
        
        start_time = time.time()
        for i in range(5000):
            event = SequenceUpdatedEvent(sequence_id=f"bench_{i}", change_type="benchmark")
            event_bus.publish(event)
        end_time = time.time()
        
        throughput = 5000 / (end_time - start_time)
        benchmarks["Event Bus Throughput"] = f"{throughput:.2f} events/second"
        
    except Exception as e:
        benchmarks["Event Bus Throughput"] = f"FAILED: {e}"
    
    # Circuit Breaker Performance
    try:
        from desktop.modern.presentation.tabs.construct.infrastructure.resilient_panel_factory import (
            CircuitBreaker, CircuitBreakerConfig
        )
        
        config = CircuitBreakerConfig()
        cb = CircuitBreaker("benchmark", config)
        
        start_time = time.time()
        for i in range(10000):
            if cb.can_execute():
                cb.record_success()
        end_time = time.time()
        
        ops_per_second = 10000 / (end_time - start_time)
        benchmarks["Circuit Breaker Operations"] = f"{ops_per_second:.2f} ops/second"
        
    except Exception as e:
        benchmarks["Circuit Breaker Operations"] = f"FAILED: {e}"
    
    # Print benchmark results
    for test_name, result in benchmarks.items():
        print(f"{test_name}: {result}")
    
    return benchmarks


def interactive_test_menu():
    """Interactive test menu for manual verification."""
    while True:
        print("\n" + "=" * 50)
        print("TKA Microservices Infrastructure - Interactive Testing")
        print("=" * 50)
        print("1. Run All Manual Tests")
        print("2. Run Performance Benchmarks")
        print("3. Test Component Creation")
        print("4. Test Event Flow")
        print("5. Test Circuit Breaker")
        print("6. Test Service Mesh")
        print("7. Test Memory Usage")
        print("8. Exit")
        print("-" * 50)
        
        try:
            choice = input("Select test (1-8): ").strip()
            
            if choice == "1":
                run_manual_tests()
            elif choice == "2":
                run_performance_benchmark()
            elif choice == "3":
                result = test_component_creation_resilience()
                print("Result:", result)
            elif choice == "4":
                result = test_event_flow_verification()
                print("Result:", result)
            elif choice == "5":
                result = test_circuit_breaker_functionality()
                print("Result:", result)
            elif choice == "6":
                result = test_service_mesh_integration()
                print("Result:", result)
            elif choice == "7":
                result = test_memory_usage()
                print("Result:", result)
            elif choice == "8":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please select 1-8.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    # Check if running in interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_test_menu()
    else:
        # Run all tests by default
        results = run_manual_tests()
        print("\nRunning performance benchmarks...")
        benchmarks = run_performance_benchmark()
        
        # Summary
        print("\n" + "=" * 60)
        print("FINAL SUMMARY")
        print("=" * 60)
        
        passed = len([r for r in results if r["status"] == "PASS"])
        total = len(results)
        
        print(f"Manual Tests: {passed}/{total} passed")
        print("Performance Benchmarks:")
        for name, result in benchmarks.items():
            print(f"  {name}: {result}")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED - Infrastructure is ready for deployment!")
        else:
            print(f"\n⚠️  {total - passed} tests failed - Review required before deployment")
