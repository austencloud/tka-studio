"""
Full System Integration Test - Phase 4

Comprehensive validation of complete microservices infrastructure
integration including saga pattern, event flows, and system resilience.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import asyncio
import time
import threading
from typing import Dict, Any, List

from desktop.modern.core.events.event_bus import TypeSafeEventBus
from desktop.modern.core.events.domain_events import (
    SequenceUpdatedEvent,
    UIStateChangedEvent,
    BeatAddedEvent,
    BeatUpdatedEvent,
    SequenceCreatedEvent
)
from desktop.modern.presentation.tabs.construct.infrastructure.event_integration import (
    ConstructTabEventIntegration,
    create_event_integration
)
from desktop.modern.presentation.tabs.construct.infrastructure.service_mesh import (
    ComponentServiceMesh
)
from desktop.modern.presentation.tabs.construct.infrastructure.resilient_panel_factory import (
    ResilientPanelFactory,
    CircuitBreakerState
)
from desktop.modern.presentation.tabs.construct.infrastructure.initialization_saga import (
    ConstructTabInitializationSaga,
    create_construct_tab_initialization_saga,
    SagaStatus
)
from desktop.modern.core.dependency_injection.di_container import DIContainer


class TestFullSystemIntegration:
    """Test complete system integration with all microservices components."""
    
    @pytest.fixture
    def full_system_setup(self):
        """Setup complete integrated microservices system."""
        # Core infrastructure
        event_bus = TypeSafeEventBus()
        event_integration = ConstructTabEventIntegration(event_bus)
        service_mesh = ComponentServiceMesh()
        container = Mock(spec=DIContainer)
        resilient_factory = ResilientPanelFactory(container)
        
        # Mock component ecosystem
        mock_components = {
            "workbench": Mock(),
            "start_position_picker": Mock(),
            "option_picker": Mock(),
            "layout_manager": Mock(),
            "sequence_builder": Mock(),
            "motion_validator": Mock(),
        }
        
        # Configure mock components with realistic behavior
        self._configure_mock_components(mock_components)
        
        # Setup integrations
        event_integration.setup_event_handlers(mock_components)
        proxied_components = service_mesh.setup_mesh_for_construct_tab(mock_components)
        
        return {
            "event_bus": event_bus,
            "event_integration": event_integration,
            "service_mesh": service_mesh,
            "resilient_factory": resilient_factory,
            "container": container,
            "components": mock_components,
            "proxied_components": proxied_components,
        }
    
    def _configure_mock_components(self, components: Dict[str, Mock]):
        """Configure mock components with realistic behavior."""
        # Workbench
        workbench = components["workbench"]
        workbench.get_current_sequence.return_value = Mock(id="test_sequence", length=3)
        workbench.refresh_display = Mock()
        workbench.update_beat = Mock()
        workbench.clear_selection = Mock()
        
        # Start Position Picker
        sp_picker = components["start_position_picker"]
        sp_picker.set_position = Mock()
        sp_picker.get_selected_position.return_value = "N"
        sp_picker.update_state = Mock()
        
        # Option Picker
        option_picker = components["option_picker"]
        option_picker.refresh_options = Mock()
        option_picker.clear_options = Mock()
        option_picker.select_option = Mock()
        
        # Layout Manager
        layout_manager = components["layout_manager"]
        layout_manager.update_layout = Mock()
        layout_manager.transition_to_mode = Mock()
        layout_manager.get_current_mode.return_value = "workbench"
        
        # Sequence Builder
        seq_builder = components["sequence_builder"]
        seq_builder.add_beat = Mock()
        seq_builder.update_beat = Mock()
        seq_builder.remove_beat = Mock()
        seq_builder.validate_sequence = Mock(return_value=True)
        
        # Motion Validator
        motion_validator = components["motion_validator"]
        motion_validator.validate_motion = Mock(return_value={"valid": True})
        motion_validator.check_conflicts = Mock(return_value=[])
    
    @pytest.mark.asyncio
    async def test_saga_with_full_event_integration(self, full_system_setup):
        """Test saga pattern working with complete event integration."""
        system = full_system_setup
        
        # Mock successful panel creation
        resilient_factory = system["resilient_factory"]
        with patch.object(resilient_factory.panel_factory, 'create_workbench_panel') as mock_workbench:
            mock_workbench.return_value = (Mock(), system["components"]["workbench"])
        
        with patch.object(resilient_factory.panel_factory, 'create_start_position_panel') as mock_sp:
            mock_sp.return_value = (Mock(), system["components"]["start_position_picker"])
        
        with patch.object(resilient_factory.panel_factory, 'create_option_picker_panel') as mock_op:
            mock_op.return_value = (Mock(), system["components"]["option_picker"])
        
        # Create and execute saga
        saga = create_construct_tab_initialization_saga(
            resilient_factory,
            system["service_mesh"],
            system["event_integration"],
            system["container"]
        )
        
        result = await saga.execute()
        
        # Verify saga completion
        assert result is True
        assert saga.status == SagaStatus.COMPLETED
        
        # Verify event integration received saga events
        assert len(system["event_integration"].subscription_ids) > 0
        
        # Verify components were created and integrated
        assert mock_workbench.called
        assert mock_sp.called
        assert mock_op.called
    
    def test_circuit_breaker_with_service_mesh_integration(self, full_system_setup):
        """Test circuit breaker integration with service mesh under load."""
        system = full_system_setup
        service_mesh = system["service_mesh"]
        proxied_components = system["proxied_components"]
        
        # Configure workbench to fail
        workbench = system["components"]["workbench"]
        workbench.problematic_operation = Mock(side_effect=Exception("Component failure"))
        
        workbench_proxy = proxied_components["workbench"]
        
        # Trigger multiple failures to open circuit breaker
        failure_count = 0
        for i in range(10):
            try:
                workbench_proxy.problematic_operation()
            except Exception:
                failure_count += 1
        
        # Verify circuit breaker protection
        cb_status = service_mesh.get_circuit_breaker_status("workbench")
        assert cb_status["state"] == CircuitBreakerState.OPEN.value
        assert failure_count >= 5  # Should have recorded failures
        
        # Other components should remain operational
        option_picker_proxy = proxied_components["option_picker"]
        result = option_picker_proxy.refresh_options()
        
        # Option picker should still work
        assert system["components"]["option_picker"].refresh_options.called
    
    def test_event_flow_through_complete_system(self, full_system_setup):
        """Test events flowing correctly through the complete integrated system."""
        system = full_system_setup
        event_bus = system["event_bus"]
        components = system["components"]
        
        # Track event flow through system
        event_flow = []
        
        def flow_tracker(event):
            event_flow.append(f"{event.event_type}:{event.sequence_id}")
        
        # Subscribe to multiple event types
        event_bus.subscribe("sequence.updated", flow_tracker)
        event_bus.subscribe("sequence.beat_added", flow_tracker)
        event_bus.subscribe("ui.start_position_picker.state_changed", flow_tracker)
        
        # Simulate complex workflow
        
        # 1. Start position selection
        system["event_integration"]._publish_start_position_selected("S")
        
        # 2. Sequence creation
        sequence_event = SequenceCreatedEvent(
            sequence_id="integration_test_seq",
            sequence_name="Integration Test Sequence"
        )
        event_bus.publish(sequence_event)
        
        # 3. Beat addition
        beat_event = BeatAddedEvent(
            sequence_id="integration_test_seq",
            beat_data={"letter": "A", "blue_motion": "pro", "red_motion": "anti"},
            beat_position=1,
            total_beats=1
        )
        event_bus.publish(beat_event)
        
        # 4. Sequence update
        update_event = SequenceUpdatedEvent(
            sequence_id="integration_test_seq",
            change_type="beat_added"
        )
        event_bus.publish(update_event)
        
        # Allow event processing
        time.sleep(0.1)
        
        # Verify event flow
        assert len(event_flow) >= 4
        
        # Verify expected events were processed
        expected_patterns = [
            "ui.start_position_picker.state_changed",
            "sequence.created:integration_test_seq",
            "sequence.beat_added:integration_test_seq",
            "sequence.beat_added:integration_test_seq"  # Update event
        ]
        
        # Check that events followed expected patterns
        for pattern in expected_patterns:
            matching_events = [e for e in event_flow if pattern in e]
            assert len(matching_events) >= 1, f"Expected pattern {pattern} not found in {event_flow}"
    
    def test_system_resilience_under_partial_failures(self, full_system_setup):
        """Test system resilience when some components fail but others continue working."""
        system = full_system_setup
        event_bus = system["event_bus"]
        service_mesh = system["service_mesh"]
        components = system["components"]
        
        # Configure partial failure scenario
        components["workbench"].refresh_display.side_effect = Exception("Workbench failed")
        components["sequence_builder"].add_beat.side_effect = Exception("Sequence builder failed")
        
        # Keep other components working
        components["option_picker"].refresh_options.return_value = "success"
        components["layout_manager"].update_layout.return_value = "updated"
        
        # Track successful operations
        successful_operations = []
        
        def success_tracker():
            successful_operations.append(time.time())
        
        components["option_picker"].refresh_options.side_effect = success_tracker
        components["layout_manager"].update_layout.side_effect = success_tracker
        
        # Trigger system-wide event
        comprehensive_event = SequenceUpdatedEvent(
            sequence_id="resilience_test",
            change_type="comprehensive_update"
        )
        
        event_bus.publish(comprehensive_event)
        
        # Allow processing
        time.sleep(0.2)
        
        # Verify partial success (graceful degradation)
        assert len(successful_operations) >= 1  # At least some operations succeeded
        
        # Verify failed components are protected by circuit breakers
        workbench_status = service_mesh.get_circuit_breaker_status("workbench")
        seq_builder_status = service_mesh.get_circuit_breaker_status("sequence_builder")
        
        # Circuit breakers should be monitoring/protecting failed components
        assert "state" in workbench_status
        assert "state" in seq_builder_status
    
    def test_performance_under_integrated_load(self, full_system_setup):
        """Test system performance under integrated load scenarios."""
        system = full_system_setup
        event_bus = system["event_bus"]
        
        # Track system performance
        processed_events = []
        processing_times = []
        
        def performance_tracker(event):
            start_time = time.time()
            processed_events.append(event.sequence_id)
            # Simulate processing time
            time.sleep(0.0001)  # 0.1ms
            processing_times.append(time.time() - start_time)
        
        event_bus.subscribe("sequence.updated", performance_tracker)
        
        # Generate integrated load
        num_events = 500
        start_time = time.time()
        
        for i in range(num_events):
            event = SequenceUpdatedEvent(
                sequence_id=f"integrated_load_{i}",
                change_type="load_test"
            )
            event_bus.publish(event)
        
        end_time = time.time()
        
        # Calculate performance metrics
        total_time = end_time - start_time
        throughput = num_events / total_time
        avg_processing_time = sum(processing_times) / len(processing_times)
        
        print(f"Integrated system performance:")
        print(f"  Throughput: {throughput:.2f} events/second")
        print(f"  Average processing time: {avg_processing_time*1000:.2f}ms")
        print(f"  Events processed: {len(processed_events)}")
        
        # Performance assertions for integrated system
        assert len(processed_events) == num_events
        assert throughput > 200  # Should handle at least 200 events/second
        assert avg_processing_time < 0.01  # Average processing < 10ms
    
    @pytest.mark.asyncio
    async def test_async_system_integration(self, full_system_setup):
        """Test async integration across all system components."""
        system = full_system_setup
        event_bus = system["event_bus"]
        
        # Track async processing
        async_events = []
        
        async def async_integration_tracker(event):
            await asyncio.sleep(0.001)  # Simulate async work
            async_events.append(event.sequence_id)
        
        event_bus.subscribe("sequence.updated", async_integration_tracker)
        
        # Generate async load
        num_events = 200
        
        tasks = []
        for i in range(num_events):
            event = SequenceUpdatedEvent(
                sequence_id=f"async_integration_{i}",
                change_type="async_test"
            )
            task = event_bus.publish_async(event)
            tasks.append(task)
        
        start_time = time.time()
        await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Calculate async performance
        total_time = end_time - start_time
        throughput = num_events / total_time
        
        print(f"Async system integration:")
        print(f"  Async throughput: {throughput:.2f} events/second")
        print(f"  Events processed: {len(async_events)}")
        
        # Async should perform well
        assert len(async_events) == num_events
        assert throughput > 400  # Should handle at least 400 events/second async
    
    def test_system_recovery_after_mass_failure(self, full_system_setup):
        """Test system recovery after mass component failure."""
        system = full_system_setup
        event_bus = system["event_bus"]
        service_mesh = system["service_mesh"]
        components = system["components"]
        
        # Phase 1: Simulate mass failure
        failing_components = ["workbench", "sequence_builder", "motion_validator"]
        
        for comp_name in failing_components:
            if comp_name in components:
                # Configure all methods to fail
                for attr_name in dir(components[comp_name]):
                    if not attr_name.startswith("_") and callable(getattr(components[comp_name], attr_name)):
                        setattr(components[comp_name], attr_name, Mock(side_effect=Exception("Mass failure")))
        
        # Trigger events during failure period
        failure_events = []
        for i in range(50):
            event = SequenceUpdatedEvent(
                sequence_id=f"failure_period_{i}",
                change_type="failure_test"
            )
            event_bus.publish(event)
            failure_events.append(event.sequence_id)
        
        # Allow circuit breakers to activate
        time.sleep(0.1)
        
        # Verify circuit breakers opened
        opened_breakers = []
        for comp_name in failing_components:
            if comp_name in service_mesh.circuit_breakers:
                status = service_mesh.get_circuit_breaker_status(comp_name)
                if status["state"] == CircuitBreakerState.OPEN.value:
                    opened_breakers.append(comp_name)
        
        assert len(opened_breakers) >= 2  # At least some circuit breakers should open
        
        # Phase 2: Simulate recovery
        for comp_name in failing_components:
            if comp_name in components:
                # Restore normal operation
                components[comp_name].reset_mock()
                components[comp_name].process_event = Mock(return_value="recovered")
                components[comp_name].refresh_display = Mock(return_value="refreshed")
        
        # Reset circuit breakers to simulate recovery
        for comp_name in failing_components:
            if comp_name in service_mesh.circuit_breakers:
                service_mesh.reset_circuit_breaker(comp_name)
        
        # Trigger events during recovery period
        recovery_events = []
        for i in range(50):
            event = SequenceUpdatedEvent(
                sequence_id=f"recovery_period_{i}",
                change_type="recovery_test"
            )
            event_bus.publish(event)
            recovery_events.append(event.sequence_id)
        
        # Verify recovery
        recovered_breakers = []
        for comp_name in failing_components:
            if comp_name in service_mesh.circuit_breakers:
                status = service_mesh.get_circuit_breaker_status(comp_name)
                if status["state"] == CircuitBreakerState.CLOSED.value:
                    recovered_breakers.append(comp_name)
        
        print(f"Recovery test results:")
        print(f"  Opened breakers during failure: {opened_breakers}")
        print(f"  Recovered breakers: {recovered_breakers}")
        print(f"  Failure period events: {len(failure_events)}")
        print(f"  Recovery period events: {len(recovery_events)}")
        
        # System should recover
        assert len(recovered_breakers) >= 2  # Components should recover
    
    def test_end_to_end_workflow_simulation(self, full_system_setup):
        """Test complete end-to-end workflow through integrated system."""
        system = full_system_setup
        event_bus = system["event_bus"]
        event_integration = system["event_integration"]
        
        # Track workflow progression
        workflow_steps = []
        
        def workflow_tracker(event):
            workflow_steps.append(f"{event.event_type}:{getattr(event, 'sequence_id', 'N/A')}")
        
        # Subscribe to workflow events
        event_types = [
            "ui.start_position_picker.state_changed",
            "sequence.created",
            "sequence.beat_added",
            "sequence.updated",
            "layout.recalculated"
        ]
        
        for event_type in event_types:
            event_bus.subscribe(event_type, workflow_tracker)
        
        # Simulate complete workflow
        
        # Step 1: User selects start position
        event_integration._publish_start_position_selected("N")
        
        # Step 2: System creates new sequence
        sequence_event = SequenceCreatedEvent(
            sequence_id="workflow_sequence",
            sequence_name="Workflow Test Sequence"
        )
        event_bus.publish(sequence_event)
        
        # Step 3: User adds beats
        for i in range(3):
            beat_event = BeatAddedEvent(
                sequence_id="workflow_sequence",
                beat_data={
                    "letter": chr(65 + i),  # A, B, C
                    "blue_motion": "pro" if i % 2 == 0 else "anti",
                    "red_motion": "anti" if i % 2 == 0 else "pro"
                },
                beat_position=i + 1,
                total_beats=i + 1
            )
            event_bus.publish(beat_event)
        
        # Step 4: System updates layout
        event_integration._publish_layout_recalculated("sequence_complete")
        
        # Step 5: Final sequence update
        final_update = SequenceUpdatedEvent(
            sequence_id="workflow_sequence",
            change_type="sequence_completed"
        )
        event_bus.publish(final_update)
        
        # Allow workflow processing
        time.sleep(0.2)
        
        # Verify workflow progression
        print(f"Workflow steps completed: {len(workflow_steps)}")
        for i, step in enumerate(workflow_steps):
            print(f"  {i+1}. {step}")
        
        # Should have processed all workflow steps
        assert len(workflow_steps) >= 6  # At least the major workflow events
        
        # Verify sequence creation and beat additions
        sequence_events = [s for s in workflow_steps if "workflow_sequence" in s]
        assert len(sequence_events) >= 5  # Created + 3 beats + final update
        
        # Verify UI state changes
        ui_events = [s for s in workflow_steps if "ui." in s]
        assert len(ui_events) >= 1  # At least start position selection


class TestSystemHealthAndMonitoring:
    """Test system health monitoring and observability features."""
    
    @pytest.fixture
    def monitored_system(self):
        """Setup system with comprehensive monitoring."""
        event_bus = TypeSafeEventBus()
        event_integration = ConstructTabEventIntegration(event_bus)
        service_mesh = ComponentServiceMesh()
        
        components = {
            "workbench": Mock(),
            "start_position_picker": Mock(),
            "option_picker": Mock(),
        }
        
        event_integration.setup_event_handlers(components)
        service_mesh.setup_mesh_for_construct_tab(components)
        
        return {
            "event_bus": event_bus,
            "event_integration": event_integration,
            "service_mesh": service_mesh,
            "components": components,
        }
    
    def test_system_health_reporting(self, monitored_system):
        """Test comprehensive system health reporting."""
        system = monitored_system
        
        # Generate some system activity
        event_bus = system["event_bus"]
        
        for i in range(20):
            event = SequenceUpdatedEvent(
                sequence_id=f"health_test_{i}",
                change_type="health_monitoring"
            )
            event_bus.publish(event)
        
        # Check event bus health
        event_stats = event_bus.get_event_stats()
        subscription_count = event_bus.get_subscription_count()
        
        # Check service mesh health
        service_mesh = system["service_mesh"]
        mesh_metrics = service_mesh.get_metrics()
        
        # Check individual component health
        component_health = {}
        for comp_name in ["workbench", "start_position_picker", "option_picker"]:
            if comp_name in service_mesh.circuit_breakers:
                status = service_mesh.get_circuit_breaker_status(comp_name)
                component_health[comp_name] = status
        
        print("System Health Report:")
        print(f"  Event Bus - Stats: {event_stats}")
        print(f"  Event Bus - Subscriptions: {subscription_count}")
        print(f"  Service Mesh - Metrics: {mesh_metrics}")
        print(f"  Component Health: {component_health}")
        
        # Health assertions
        assert subscription_count > 0  # Should have active subscriptions
        assert "total_requests" in mesh_metrics  # Should have metrics
        assert len(component_health) == 3  # Should monitor all components
    
    def test_performance_metrics_collection(self, monitored_system):
        """Test collection of performance metrics across system."""
        system = monitored_system
        event_bus = system["event_bus"]
        service_mesh = system["service_mesh"]
        
        # Generate measured load
        start_time = time.time()
        
        for i in range(100):
            event = SequenceUpdatedEvent(
                sequence_id=f"metrics_test_{i}",
                change_type="metrics_collection"
            )
            event_bus.publish(event)
        
        end_time = time.time()
        
        # Collect performance metrics
        processing_time = end_time - start_time
        throughput = 100 / processing_time
        
        mesh_metrics = service_mesh.get_metrics()
        
        print("Performance Metrics:")
        print(f"  Event Processing Throughput: {throughput:.2f} events/second")
        print(f"  Total Processing Time: {processing_time:.3f} seconds")
        print(f"  Service Mesh Metrics: {mesh_metrics}")
        
        # Performance should meet benchmarks
        assert throughput > 500  # Should handle 500+ events/second
        assert processing_time < 1.0  # Should complete in under 1 second
    
    def test_error_rate_monitoring(self, monitored_system):
        """Test monitoring of error rates across system."""
        system = monitored_system
        service_mesh = system["service_mesh"]
        components = system["components"]
        
        # Configure some components to fail intermittently
        components["workbench"].intermittent_op = Mock()
        call_count = 0
        
        def intermittent_failure():
            nonlocal call_count
            call_count += 1
            if call_count % 3 == 0:  # Fail every 3rd call
                raise Exception("Intermittent failure")
            return "success"
        
        components["workbench"].intermittent_op.side_effect = intermittent_failure
        
        # Generate mixed success/failure operations
        proxied_components = service_mesh.setup_mesh_for_construct_tab(components)
        workbench_proxy = proxied_components["workbench"]
        
        for i in range(30):
            try:
                workbench_proxy.intermittent_op()
            except Exception:
                pass  # Expected failures
        
        # Check error rates
        workbench_status = service_mesh.get_circuit_breaker_status("workbench")
        
        total_requests = workbench_status["total_requests"]
        failed_requests = workbench_status["failed_requests"]
        error_rate = (failed_requests / total_requests) * 100 if total_requests > 0 else 0
        
        print(f"Error Rate Monitoring:")
        print(f"  Total Requests: {total_requests}")
        print(f"  Failed Requests: {failed_requests}")
        print(f"  Error Rate: {error_rate:.2f}%")
        
        # Should track error rates accurately
        assert total_requests == 30
        assert failed_requests == 10  # Every 3rd call fails
        assert abs(error_rate - 33.33) < 1.0  # Should be approximately 33%
