"""
Event Integration for ConstructTab

Replaces signal_coordinator.py with event-driven architecture using existing TypeSafeEventBus.
Provides bridge between PyQt signals and modern event system.
"""

from __future__ import annotations

import logging
from typing import Any

from desktop.modern.core.commands.command_system import CommandProcessor
from desktop.modern.core.events.domain_events import (
    BeatAddedEvent,
    BeatRemovedEvent,
    BeatUpdatedEvent,
    LayoutRecalculatedEvent,
    SequenceCreatedEvent,
    SequenceUpdatedEvent,
    UIStateChangedEvent,
)
from desktop.modern.core.events.event_bus import TypeSafeEventBus, get_event_bus
from desktop.modern.domain.models import SequenceData


logger = logging.getLogger(__name__)


class ConstructTabEventIntegration:
    """
    Event-driven integration for ConstructTab components.

    Replaces signal_coordinator.py with modern event architecture.
    Bridges PyQt signals to TypeSafeEventBus and provides event handlers.
    """

    def __init__(self, event_bus: TypeSafeEventBus | None = None):
        self.event_bus = event_bus or get_event_bus()
        self.command_processor = CommandProcessor(self.event_bus)
        self.logger = logging.getLogger(__name__)

        # Component references
        self.components: dict[str, Any] = {}

        # Event subscription IDs for cleanup
        self.subscription_ids: dict[str, str] = {}

        # State tracking
        self._handling_sequence_modification = False
        self._current_operation_type = None

    def setup_event_handlers(self, components: dict[str, Any]):
        """Setup event handlers for all components."""
        self.components = components
        self._subscribe_to_events()
        self._connect_component_signals()

        self.logger.info("Event integration setup complete")

    def _subscribe_to_events(self):
        """Subscribe to domain events."""

        # Sequence events
        self.subscription_ids["sequence_created"] = self.event_bus.subscribe(
            "sequence.created", self._handle_sequence_created
        )

        self.subscription_ids["sequence_updated"] = self.event_bus.subscribe(
            "sequence.updated", self._handle_sequence_updated
        )

        self.subscription_ids["beat_added"] = self.event_bus.subscribe(
            "sequence.beat_added", self._handle_beat_added
        )

        self.subscription_ids["beat_updated"] = self.event_bus.subscribe(
            "sequence.beat_updated", self._handle_beat_updated
        )

        self.subscription_ids["beat_removed"] = self.event_bus.subscribe(
            "sequence.beat_removed", self._handle_beat_removed
        )

        # UI events
        self.subscription_ids["ui_state_changed"] = self.event_bus.subscribe(
            "ui.start_position_picker.state_changed",
            self._handle_start_position_selected,
        )

        self.subscription_ids["layout_recalculated"] = self.event_bus.subscribe(
            "layout.beat_frame_recalculated", self._handle_layout_recalculated
        )

        self.logger.info(f"Subscribed to {len(self.subscription_ids)} event types")

    def _connect_component_signals(self):
        """Connect component PyQt signals to event publishing."""

        # Start position picker signals → events
        start_position_picker = self.components.get("start_position_picker")
        if start_position_picker and hasattr(
            start_position_picker, "start_position_selected"
        ):
            start_position_picker.start_position_selected.connect(
                self._publish_start_position_selected
            )

        # Option picker signals → events
        option_picker = self.components.get("option_picker")
        if option_picker and hasattr(option_picker, "pictograph_selected"):
            option_picker.pictograph_selected.connect(self._publish_pictograph_selected)

        # Workbench signals → events
        workbench = self.components.get("workbench")
        if workbench:
            if hasattr(workbench, "sequence_modified"):
                workbench.sequence_modified.connect(self._publish_sequence_modified)

            if hasattr(workbench, "picker_mode_requested"):
                workbench.picker_mode_requested.connect(
                    self._publish_picker_mode_requested
                )

            if hasattr(workbench, "clear_sequence_requested"):
                workbench.clear_sequence_requested.connect(
                    self._publish_clear_sequence_requested
                )

        self.logger.info("Component signals connected to event publishing")

    # Event Publishers (PyQt Signal → Event Bus)

    def _publish_start_position_selected(self, position_key: str):
        """Publish start position selection event."""
        event = UIStateChangedEvent(
            component="start_position_picker",
            state_key="position_selected",
            old_value=None,
            new_value=position_key,
            source="construct_tab",
        )
        self.event_bus.publish(event)
        self.logger.info(f"Published start position selected: {position_key}")

    def _publish_pictograph_selected(self, pictograph_data: dict[str, Any]):
        """Publish pictograph selection event."""
        event = UIStateChangedEvent(
            component="option_picker",
            state_key="pictograph_selected",
            old_value=None,
            new_value=pictograph_data,
            source="construct_tab",
        )
        self.event_bus.publish(event)
        self.logger.info(
            f"Published pictograph selected: {pictograph_data.get('letter', 'unknown')}"
        )

    def _publish_sequence_modified(self, sequence: SequenceData):
        """Publish sequence modification event."""
        if self._handling_sequence_modification:
            return

        try:
            self._handling_sequence_modification = True

            event = SequenceUpdatedEvent(
                sequence_id=sequence.id,
                change_type="modified",
                previous_state=None,
                new_state={
                    "length": sequence.length,
                    "beat_count": len(sequence.beats) if sequence.beats else 0,
                    "metadata": sequence.metadata,
                },
                source="workbench",
            )
            self.event_bus.publish(event)
            self.logger.info(f"Published sequence modified: {sequence.id}")

        finally:
            self._handling_sequence_modification = False

    def _publish_picker_mode_requested(self):
        """Publish picker mode request event."""
        event = UIStateChangedEvent(
            component="workbench",
            state_key="mode_requested",
            old_value=None,
            new_value="picker_mode",
            source="workbench",
        )
        self.event_bus.publish(event)
        self.logger.info("Published picker mode request")

    def _publish_clear_sequence_requested(self):
        """Publish clear sequence request event."""
        event = UIStateChangedEvent(
            component="workbench",
            state_key="action_requested",
            old_value=None,
            new_value="clear_sequence",
            source="workbench",
        )
        self.event_bus.publish(event)
        self.logger.info("Published clear sequence request")

    def publish_ui_state_change(
        self, component: str, state_key: str, old_value: Any, new_value: Any
    ):
        """Generic method to publish UI state changes."""
        event = UIStateChangedEvent(
            component=component,
            state_key=state_key,
            old_value=old_value,
            new_value=new_value,
            source="construct_tab",
        )
        self.event_bus.publish(event)

    # Event Handlers (Event Bus → Component Actions)

    def _handle_sequence_created(self, event: SequenceCreatedEvent):
        """Handle sequence creation event."""
        self.logger.info(f"Handling sequence created: {event.sequence_id}")

        # Trigger layout manager transition to appropriate view
        layout_manager = self.components.get("layout_manager")
        if layout_manager:
            layout_manager.transition_to_option_picker()

    def _handle_sequence_updated(self, event: SequenceUpdatedEvent):
        """Handle sequence update event."""
        self.logger.info(
            f"Handling sequence updated: {event.sequence_id} - {event.change_type}"
        )

        # Update option picker if needed
        option_picker = self.components.get("option_picker")
        layout_manager = self.components.get("layout_manager")

        if option_picker and layout_manager:
            # Get current sequence and update option picker
            # This replaces the signal coordinator's refresh logic
            self._smart_picker_transition(event.new_state)

    def _handle_beat_added(self, event: BeatAddedEvent):
        """Handle beat added event."""
        self.logger.info(
            f"Handling beat added: sequence {event.sequence_id}, beat {event.beat_position}"
        )

        # Refresh option picker with new sequence state
        option_picker = self.components.get("option_picker")
        if option_picker and hasattr(option_picker, "refresh_from_sequence"):
            # Get current sequence from workbench
            workbench = self.components.get("workbench")
            if workbench and hasattr(workbench, "get_current_sequence"):
                current_sequence = workbench.get_current_sequence()
                if current_sequence:
                    option_picker.refresh_from_sequence(current_sequence)

    def _handle_beat_updated(self, event: BeatUpdatedEvent):
        """Handle beat updated event."""
        self.logger.info(
            f"Handling beat updated: sequence {event.sequence_id}, beat {event.beat_number}"
        )

        # Similar refresh logic as beat added
        self._refresh_option_picker_from_workbench()

    def _handle_beat_removed(self, event: BeatRemovedEvent):
        """Handle beat removed event."""
        self.logger.info(
            f"Handling beat removed: sequence {event.sequence_id}, position {event.old_position}"
        )

        # Check if sequence is now empty and transition accordingly
        if event.remaining_beats == 0:
            layout_manager = self.components.get("layout_manager")
            if layout_manager:
                layout_manager.transition_to_start_position_picker()
        else:
            self._refresh_option_picker_from_workbench()

    def _handle_start_position_selected(self, event: UIStateChangedEvent):
        """Handle start position selection event."""
        if event.state_key == "position_selected":
            position_key = event.new_value
            self.logger.info(f"Handling start position selected: {position_key}")

            # Trigger start position handler
            start_position_handler = self.components.get("start_position_handler")
            if start_position_handler:
                # This replaces the signal coordinator's _handle_start_position_created
                start_position_handler.handle_start_position_selected(position_key)

    def _handle_layout_recalculated(self, event: LayoutRecalculatedEvent):
        """Handle layout recalculation event."""
        self.logger.info(f"Handling layout recalculated: {event.layout_type}")

        # Update component layouts if needed
        layout_manager = self.components.get("layout_manager")
        if layout_manager and hasattr(layout_manager, "handle_layout_update"):
            layout_manager.handle_layout_update(event.layout_data)

    # Helper Methods

    def _smart_picker_transition(self, sequence_state: dict[str, Any] | None):
        """Smart transition logic based on sequence state."""
        layout_manager = self.components.get("layout_manager")
        if not layout_manager:
            return

        # Check if start position is set
        start_position_set = self._is_start_position_set()

        # Check if sequence has beats
        has_beats = False
        if sequence_state:
            beat_count = sequence_state.get("beat_count", 0)
            has_beats = beat_count > 0

        if start_position_set or has_beats:
            # Pre-load option picker content before transition
            option_picker = self.components.get("option_picker")
            if option_picker and hasattr(option_picker, "refresh_from_sequence"):
                workbench = self.components.get("workbench")
                if workbench and hasattr(workbench, "get_current_sequence"):
                    current_sequence = workbench.get_current_sequence()
                    if current_sequence:
                        option_picker.refresh_from_sequence(current_sequence)

            layout_manager.transition_to_option_picker()
        else:
            layout_manager.transition_to_start_position_picker()

    def _is_start_position_set(self) -> bool:
        """Check if start position is set in workbench."""
        workbench = self.components.get("workbench")
        if workbench and hasattr(workbench, "_beat_frame_section"):
            beat_frame_section = workbench._beat_frame_section
            if beat_frame_section and hasattr(
                beat_frame_section, "_start_position_data"
            ):
                return beat_frame_section._start_position_data is not None
        return False

    def _refresh_option_picker_from_workbench(self):
        """Refresh option picker with current sequence from workbench."""
        option_picker = self.components.get("option_picker")
        workbench = self.components.get("workbench")

        if option_picker and workbench:
            if hasattr(option_picker, "refresh_from_sequence") and hasattr(
                workbench, "get_current_sequence"
            ):
                current_sequence = workbench.get_current_sequence()
                if current_sequence:
                    option_picker.refresh_from_sequence(current_sequence)

    # Command Integration

    def execute_command(self, command):
        """Execute command through command processor."""
        result = self.command_processor.execute(command)
        if result.success:
            self.logger.info(f"Command executed successfully: {command.description}")
        else:
            self.logger.error(f"Command execution failed: {result.error_message}")
        return result

    def undo_last_command(self):
        """Undo last command."""
        result = self.command_processor.undo()
        if result.success:
            self.logger.info("Command undone successfully")
        else:
            self.logger.error(f"Undo failed: {result.error_message}")
        return result

    # Cleanup
