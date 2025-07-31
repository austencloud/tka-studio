"""
ConstructTab Event Integration

Integrates the existing TypeSafeEventBus into ConstructTab components,
replacing signal coordination with event-driven architecture.
"""

from typing import TYPE_CHECKING

from desktop.modern.core.commands.command_system import CommandProcessor
from desktop.modern.core.events.domain_events import (
    BeatAddedEvent,
    BeatRemovedEvent,
    BeatUpdatedEvent,
    ComponentResizedEvent,
    LayoutRecalculatedEvent,
    SequenceCreatedEvent,
    UIStateChangedEvent,
)
from desktop.modern.core.events.event_bus import IEventBus

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer


class ConstructTabEventIntegration:
    """
    Integrates ConstructTab with existing event-driven architecture.

    Replaces signal_coordinator.py with event bus integration.
    """

    def __init__(self, container: "DIContainer"):
        """Initialize with existing event infrastructure."""
        # Get existing event bus from DI container
        self.event_bus: IEventBus = container.resolve(IEventBus)
        self.command_processor: CommandProcessor = container.resolve(CommandProcessor)

        # Component references (will be set during initialization)
        self.layout_manager = None
        self.option_picker_manager = None
        self.start_position_handler = None
        self.workbench = None

    def setup_event_handlers(self, components: dict):
        """Setup event handlers for all components."""
        # Store component references
        self.layout_manager = components.get("layout_manager")
        self.option_picker_manager = components.get("option_picker_manager")
        self.start_position_handler = components.get("start_position_handler")
        self.workbench = components.get("workbench")

        # Subscribe to domain events
        self._subscribe_to_sequence_events()
        self._subscribe_to_layout_events()
        self._subscribe_to_ui_events()

    def _subscribe_to_sequence_events(self):
        """Subscribe to sequence-related events."""
        # Sequence creation/updates
        self.event_bus.subscribe("sequence.created", self._handle_sequence_created)

        self.event_bus.subscribe("sequence.beat_added", self._handle_beat_added)

        self.event_bus.subscribe("sequence.beat_updated", self._handle_beat_updated)

        self.event_bus.subscribe("sequence.beat_removed", self._handle_beat_removed)

    def _subscribe_to_layout_events(self):
        """Subscribe to layout-related events."""
        self.event_bus.subscribe(
            "layout.component_resized", self._handle_component_resized
        )

        self.event_bus.subscribe(
            "layout.beat_frame_recalculated", self._handle_layout_recalculated
        )

    def _subscribe_to_ui_events(self):
        """Subscribe to UI state events."""
        self.event_bus.subscribe(
            "ui.start_position.state_changed", self._handle_start_position_state_change
        )

        self.event_bus.subscribe(
            "ui.option_picker.state_changed", self._handle_option_picker_state_change
        )

    # Event Handlers (replace signal coordinator logic)

    def _handle_sequence_created(self, event: SequenceCreatedEvent):
        """Handle sequence creation - update UI components."""
        if self.option_picker_manager:
            # Refresh option picker with new sequence
            self.option_picker_manager.refresh_from_sequence_creation(event)

        if self.layout_manager:
            # Transition to option picker if sequence created
            self.layout_manager.transition_to_option_picker()

    def _handle_beat_added(self, event: BeatAddedEvent):
        """Handle beat addition - update related components."""
        if self.option_picker_manager:
            self.option_picker_manager.refresh_from_beat_addition(event)

        # Ensure we're showing the option picker when beats exist
        if self.layout_manager and event.total_beats > 0:
            self.layout_manager.transition_to_option_picker()

    def _handle_beat_updated(self, event: BeatUpdatedEvent):
        """Handle beat updates - refresh visualizations."""
        if self.workbench:
            self.workbench.refresh_beat_visualization(
                event.beat_number, event.field_changed
            )

    def _handle_beat_removed(self, event: BeatRemovedEvent):
        """Handle beat removal - update UI state."""
        if event.remaining_beats == 0:
            # No beats left, transition to start position picker
            if self.layout_manager:
                self.layout_manager.transition_to_start_position_picker()

    def _handle_component_resized(self, event: ComponentResizedEvent):
        """Handle component resize - trigger layout updates."""
        if self.layout_manager:
            self.layout_manager.handle_component_resize(
                event.component_name, event.new_size
            )

    def _handle_layout_recalculated(self, event: LayoutRecalculatedEvent):
        """Handle layout recalculation - update components."""
        if self.workbench:
            self.workbench.apply_layout_changes(event.layout_data)

    def _handle_start_position_state_change(self, event: UIStateChangedEvent):
        """Handle start position state changes."""
        if event.state_key == "position_selected" and event.new_value:
            # Start position selected, prepare option picker
            if self.option_picker_manager:
                self.option_picker_manager.prepare_from_start_position(event.new_value)
            # Transition to option picker
            if self.layout_manager:
                self.layout_manager.transition_to_option_picker()

    def _handle_option_picker_state_change(self, event: UIStateChangedEvent):
        """Handle option picker state changes."""
        if event.state_key == "pictograph_selected":
            # Pictograph selected, update sequence
            self._publish_beat_addition(event.new_value)

    # Event Publishing (replace signal emissions)

    def publish_sequence_created(self, sequence_data):
        """Publish sequence creation event."""
        event = SequenceCreatedEvent(
            sequence_id=sequence_data.get("id", ""),
            sequence_name=sequence_data.get("name", ""),
            sequence_length=sequence_data.get("length", 0),
            source="construct_tab",
        )
        self.event_bus.publish(event)

    def publish_beat_added(self, beat_data, position, sequence):
        """Publish beat addition event."""
        event = BeatAddedEvent(
            sequence_id=sequence.get("id", ""),
            beat_data=beat_data,
            beat_position=position,
            total_beats=sequence.get("length", 0),
            source="construct_tab",
        )
        self.event_bus.publish(event)

    def publish_beat_updated(
        self, sequence_id, beat_number, field, old_value, new_value
    ):
        """Publish beat update event."""
        event = BeatUpdatedEvent(
            sequence_id=sequence_id,
            beat_number=beat_number,
            field_changed=field,
            old_value=old_value,
            new_value=new_value,
            source="construct_tab",
        )
        self.event_bus.publish(event)

    def publish_ui_state_change(self, component, state_key, old_value, new_value):
        """Publish UI state change event."""
        event = UIStateChangedEvent(
            component=component,
            state_key=state_key,
            old_value=old_value,
            new_value=new_value,
            source="construct_tab",
        )
        self.event_bus.publish(event)

    def publish_layout_recalculated(self, layout_type, layout_data, trigger_reason):
        """Publish layout recalculation event."""
        event = LayoutRecalculatedEvent(
            layout_type=layout_type,
            layout_data=layout_data,
            trigger_reason=trigger_reason,
            source="construct_tab",
        )
        self.event_bus.publish(event)

    # Command Integration

    def execute_command(self, command):
        """Execute command through command processor."""
        return self.command_processor.execute(command)

    def undo_last_command(self):
        """Undo last command."""
        return self.command_processor.undo()

    def redo_last_command(self):
        """Redo last command."""
        return self.command_processor.redo()
