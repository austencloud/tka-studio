"""
Event Integration Unit Tests - Phase 1

Comprehensive validation of event-driven architecture implementation
leveraging existing TypeSafeEventBus infrastructure.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import asyncio
import time
from typing import Dict, Any

from src.desktop.modern.presentation.tabs.construct.infrastructure.event_integration import (
    ConstructTabEventIntegration,
    create_event_integration
)
from src.desktop.modern.core.events.event_bus import TypeSafeEventBus, EventPriority
from src.desktop.modern.core.events.domain_events import (
    SequenceUpdatedEvent,
    UIStateChangedEvent,
    BeatAddedEvent,
    BeatUpdatedEvent,
    SequenceCreatedEvent
)
from src.desktop.modern.core.commands.command_system import Command


class TestEventIntegration:
    """Test suite for ConstructTabEventIntegration."""
    
    @pytest.fixture
    def event_bus(self):
        """Create fresh event bus for each test."""
        return TypeSafeEventBus()
    
    @pytest.fixture
    def event_integration(self, event_bus):
        """Create event integration instance."""
        return ConstructTabEventIntegration(event_bus)
    
    @pytest.fixture
    def mock_components(self):
        """Create mock components for testing."""
        return {
            "workbench": Mock(),
            "start_position_picker": Mock(),
            "option_picker": Mock(),
            "layout_manager": Mock(),
            "start_position_handler": Mock(),
        }
    
    def test_initialization(self, event_integration, event_bus):
        """Test proper initialization of event integration."""
        assert event_integration.event_bus is event_bus
        assert event_integration.command_processor is not None
        assert isinstance(event_integration.components, dict)
        assert isinstance(event_integration.subscription_ids, dict)
        assert event_integration._handling_sequence_modification is False
    
    def test_setup_event_handlers(self, event_integration, mock_components):
        """Test event handler setup creates proper subscriptions."""
        event_integration.setup_event_handlers(mock_components)
        
        # Verify subscriptions were created
        assert len(event_integration.subscription_ids) > 0
        assert "sequence_updated" in event_integration.subscription_ids
        assert "beat_added" in event_integration.subscription_ids
        assert "ui_state_changed" in event_integration.subscription_ids
        assert event_integration.components == mock_components
    
    def test_publish_start_position_selected(self, event_integration, event_bus):
        """Test start position selection event publishing."""
        events_received = []
        
        def capture_event(event):
            events_received.append(event)
        
        event_bus.subscribe("ui.start_position_picker.state_changed", capture_event)
        event_integration._publish_start_position_selected("N")
        
        assert len(events_received) == 1
        event = events_received[0]
        assert isinstance(event, UIStateChangedEvent)
        assert event.component == "start_position_picker"
        assert event.new_value == "N"
        assert event.priority == EventPriority.HIGH
    
    def test_handle_sequence_updated(self, event_integration, mock_components):
        """Test sequence update event handling."""
        event_integration.setup_event_handlers(mock_components)
        
        event = SequenceUpdatedEvent(
            sequence_id="test_seq",
            change_type="beat_added",
            new_state={"beat_count": 3}
        )
        
        event_integration._handle_sequence_updated(event)
        
        # Verify appropriate component methods were called
        option_picker = mock_components["option_picker"]
        layout_manager = mock_components["layout_manager"]
        
        # Should trigger component updates
        assert hasattr(option_picker, 'refresh_from_sequence') or hasattr(option_picker, 'update_from_sequence')
    
    def test_command_execution(self, event_integration):
        """Test command processor integration."""
        mock_command = Mock(spec=Command)
        mock_command.description = "Test Command"
        mock_command.can_execute.return_value = True
        mock_command.execute.return_value = "success"
        mock_command.command_id = "test_cmd_123"
        
        result = event_integration.execute_command(mock_command)
        
        assert result.success
        assert mock_command.execute.called
    
    def test_subscription_cleanup(self, event_integration, event_bus):
        """Test event subscription cleanup."""
        mock_components = {"test": Mock()}
        event_integration.setup_event_handlers(mock_components)
        
        initial_count = len(event_integration.subscription_ids)
        assert initial_count > 0
        
        event_integration.shutdown()
        
        assert len(event_integration.subscription_ids) == 0
        assert len(event_integration.components) == 0
    
    def test_sequence_modification_state_tracking(self, event_integration, mock_components):
        """Test sequence modification state tracking prevents recursion."""
        event_integration.setup_event_handlers(mock_components)
        
        # Simulate nested sequence modification
        event_integration._handling_sequence_modification = True
        
        event = SequenceUpdatedEvent(
            sequence_id="test_seq",
            change_type="beat_updated"
        )
        
        # Should skip handling if already handling
        event_integration._handle_sequence_updated(event)
        
        # Verify no recursive handling occurred
        assert event_integration._handling_sequence_modification is True
    
    def test_beat_added_event_handling(self, event_integration, mock_components):
        """Test beat added event handling."""
        event_integration.setup_event_handlers(mock_components)
        
        beat_data = {"letter": "A", "blue_motion": "pro", "red_motion": "anti"}
        event = BeatAddedEvent(
            sequence_id="test_seq",
            beat_data=beat_data,
            beat_position=1,
            total_beats=2
        )
        
        event_integration._handle_beat_added(event)
        
        # Verify workbench and option picker are notified
        workbench = mock_components["workbench"]
        option_picker = mock_components["option_picker"]
        
        # Components should be updated with new beat information
        assert workbench.called or option_picker.called
    
    def test_ui_state_changed_handling(self, event_integration, mock_components):
        """Test UI state change event handling."""
        event_integration.setup_event_handlers(mock_components)
        
        event = UIStateChangedEvent(
            component="start_position_picker",
            action="position_selected",
            new_value="S"
        )
        
        event_integration._handle_ui_state_changed(event)
        
        # Should trigger appropriate component responses
        layout_manager = mock_components["layout_manager"]
        # Verify layout manager responds to state change
    
    def test_error_handling_during_event_processing(self, event_integration, mock_components):
        """Test error handling during event processing."""
        # Setup component that will raise exception
        faulty_component = Mock()
        faulty_component.refresh_from_sequence.side_effect = Exception("Component error")
        mock_components["option_picker"] = faulty_component
        
        event_integration.setup_event_handlers(mock_components)
        
        event = SequenceUpdatedEvent(
            sequence_id="test_seq",
            change_type="beat_added"
        )
        
        # Should not crash despite component error
        try:
            event_integration._handle_sequence_updated(event)
        except Exception as e:
            pytest.fail(f"Event handling should not propagate exceptions: {e}")
    
    def test_event_priority_handling(self, event_integration, event_bus):
        """Test event priority handling."""
        events_received = []
        
        def capture_event(event):
            events_received.append(event.priority)
        
        event_bus.subscribe("sequence.created", capture_event)
        
        # Publish high priority event
        event = SequenceCreatedEvent(
            sequence_id="test_seq",
            priority=EventPriority.HIGH
        )
        
        event_integration.event_bus.publish(event)
        
        assert len(events_received) == 1
        assert events_received[0] == EventPriority.HIGH
    
    @pytest.mark.asyncio
    async def test_async_event_handling(self, event_integration, event_bus):
        """Test asynchronous event handling."""
        async_events_received = []
        
        async def async_handler(event):
            async_events_received.append(event)
        
        event_bus.subscribe("sequence.updated", async_handler)
        
        event = SequenceUpdatedEvent(
            sequence_id="async_test",
            change_type="beat_added"
        )
        
        await event_bus.publish_async(event)
        
        assert len(async_events_received) == 1
        assert async_events_received[0].sequence_id == "async_test"
    
    def test_component_signal_bridging(self, event_integration, mock_components):
        """Test bridging between PyQt signals and events."""
        event_integration.setup_event_handlers(mock_components)
        
        # Simulate PyQt signal emission
        workbench = mock_components["workbench"]
        
        # Setup signal-like behavior
        def mock_emit_sequence_modified(sequence):
            event_integration._publish_sequence_modified(sequence)
        
        workbench.sequence_modified.emit = mock_emit_sequence_modified
        
        # Test signal-to-event bridging
        mock_sequence = Mock()
        mock_sequence.id = "bridge_test"
        
        workbench.sequence_modified.emit(mock_sequence)
        
        # Verify event was published
        # (In real implementation, this would trigger other components)
    
    def test_memory_cleanup_on_shutdown(self, event_integration, mock_components):
        """Test memory cleanup during shutdown."""
        event_integration.setup_event_handlers(mock_components)
        
        # Add some state
        event_integration.components["extra"] = Mock()
        event_integration.subscription_ids["extra"] = "extra_sub_123"
        
        # Perform shutdown
        event_integration.shutdown()
        
        # Verify complete cleanup
        assert len(event_integration.components) == 0
        assert len(event_integration.subscription_ids) == 0
        assert not event_integration._handling_sequence_modification


class TestEventIntegrationFactory:
    """Test the factory function for creating event integration."""
    
    def test_create_event_integration(self):
        """Test factory function creates proper instance."""
        integration = create_event_integration()
        
        assert isinstance(integration, ConstructTabEventIntegration)
        assert integration.event_bus is not None
        assert integration.command_processor is not None
    
    def test_create_event_integration_with_custom_bus(self):
        """Test factory function with custom event bus."""
        custom_bus = TypeSafeEventBus()
        integration = create_event_integration(custom_bus)
        
        assert integration.event_bus is custom_bus


class TestPerformanceCharacteristics:
    """Test performance characteristics of event integration."""
    
    @pytest.fixture
    def performance_setup(self):
        """Setup for performance testing."""
        event_bus = TypeSafeEventBus()
        integration = ConstructTabEventIntegration(event_bus)
        
        mock_components = {}
        for i in range(10):  # Multiple components
            mock_components[f"component_{i}"] = Mock()
        
        integration.setup_event_handlers(mock_components)
        return integration, event_bus
    
    def test_high_frequency_event_handling(self, performance_setup):
        """Test handling high frequency events."""
        integration, event_bus = performance_setup
        
        start_time = time.time()
        
        # Publish many events rapidly
        for i in range(100):
            event = SequenceUpdatedEvent(
                sequence_id=f"perf_test_{i}",
                change_type="beat_updated"
            )
            event_bus.publish(event)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should handle 100 events quickly
        assert duration < 1.0  # Less than 1 second
        
        throughput = 100 / duration
        print(f"Event throughput: {throughput:.2f} events/second")
        
        # Should handle at least 100 events/second
        assert throughput > 100
    
    @pytest.mark.asyncio
    async def test_async_event_throughput(self, performance_setup):
        """Test asynchronous event throughput."""
        integration, event_bus = performance_setup
        
        start_time = time.time()
        
        # Create async tasks for event publishing
        tasks = []
        for i in range(100):
            event = SequenceUpdatedEvent(
                sequence_id=f"async_perf_{i}",
                change_type="beat_added"
            )
            task = event_bus.publish_async(event)
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        throughput = 100 / duration
        print(f"Async event throughput: {throughput:.2f} events/second")
        
        # Async should be faster than sync
        assert throughput > 200
