"""
Signal Integration Adapter

Provides a drop-in replacement for event bus integration using Qt signals.
Maintains the same interface as ConstructTabEventIntegration but uses Qt signals internally.
"""

import logging
from typing import Any

from PyQt6.QtCore import QObject

from .qt_signal_coordinator import ConstructTabSignalCoordinator

logger = logging.getLogger(__name__)


class SignalIntegrationAdapter(QObject):
    """
    Drop-in replacement for ConstructTabEventIntegration using Qt signals.

    Provides the same interface as the event bus version but uses Qt signals internally.
    This allows existing code to work without changes while using Qt signals.
    """

    def __init__(self, signal_coordinator: ConstructTabSignalCoordinator | None = None):
        super().__init__()
        self.signal_coordinator = signal_coordinator or ConstructTabSignalCoordinator()
        self.logger = logging.getLogger(__name__)

        # Component references
        self.components: dict[str, Any] = {}

        # Connect to coordinator signals for handling
        self._connect_coordinator_signals()

        self.logger.info("Signal integration adapter initialized")

    def _connect_coordinator_signals(self):
        """Connect to signal coordinator signals for event handling."""
        # Sequence signals
        self.signal_coordinator.sequence_created.connect(self._handle_sequence_created)
        self.signal_coordinator.beat_added.connect(self._handle_beat_added)
        self.signal_coordinator.beat_updated.connect(self._handle_beat_updated)
        self.signal_coordinator.beat_removed.connect(self._handle_beat_removed)

        # UI signals
        self.signal_coordinator.start_position_selected.connect(
            self._handle_start_position_selected
        )
        self.signal_coordinator.option_picker_selection.connect(
            self._handle_option_picker_selection
        )

        # Layout signals
        self.signal_coordinator.layout_recalculated.connect(
            self._handle_layout_recalculated
        )
        self.signal_coordinator.component_resized.connect(
            self._handle_component_resized
        )
        self.signal_coordinator.layout_transition_requested.connect(
            self._handle_layout_transition
        )

    def setup_event_handlers(self, components: dict[str, Any]):
        """Setup event handlers for all components (maintains interface compatibility)."""
        self.components = components

        # Register components with coordinator
        for name, component in components.items():
            self.signal_coordinator.register_component(name, component)

        self.logger.info("Signal integration setup complete")

    # Event handlers (Qt signal slots)

    def _handle_sequence_created(self, sequence_id: str, name: str, length: int):
        """Handle sequence creation signal."""
        self.logger.info(f"Handling sequence created: {sequence_id}")

        # Trigger layout manager transition to option picker
        layout_manager = self.components.get("layout_manager")
        if layout_manager and hasattr(layout_manager, "transition_to_option_picker"):
            layout_manager.transition_to_option_picker()

    def _handle_beat_added(
        self, sequence_id: str, beat_data: Any, position: int, total_beats: int
    ):
        """Handle beat addition signal."""
        self.logger.info(
            f"Handling beat added: sequence {sequence_id}, position {position}"
        )

        # Update option picker
        option_picker_manager = self.components.get("option_picker_manager")
        if option_picker_manager and hasattr(
            option_picker_manager, "refresh_from_beat_addition"
        ):
            # Create a mock event object for compatibility
            mock_event = type(
                "MockEvent",
                (),
                {
                    "sequence_id": sequence_id,
                    "beat_data": beat_data,
                    "beat_position": position,
                    "total_beats": total_beats,
                },
            )()
            option_picker_manager.refresh_from_beat_addition(mock_event)

        # Ensure we're showing the option picker when beats exist
        layout_manager = self.components.get("layout_manager")
        if (
            layout_manager
            and total_beats > 0
            and hasattr(layout_manager, "transition_to_option_picker")
        ):
            layout_manager.transition_to_option_picker()

    def _handle_beat_updated(
        self,
        sequence_id: str,
        beat_number: int,
        field: str,
        old_value: Any,
        new_value: Any,
    ):
        """Handle beat update signal."""
        self.logger.info(
            f"Handling beat updated: sequence {sequence_id}, beat {beat_number}"
        )

        # Refresh workbench visualization
        workbench = self.components.get("workbench")
        if workbench and hasattr(workbench, "refresh_beat_visualization"):
            workbench.refresh_beat_visualization(beat_number, field)

    def _handle_beat_removed(
        self, sequence_id: str, beat_number: int, remaining_beats: int
    ):
        """Handle beat removal signal."""
        self.logger.info(
            f"Handling beat removed: sequence {sequence_id}, beat {beat_number}"
        )

        if remaining_beats == 0:
            # No beats left, transition to start position picker
            layout_manager = self.components.get("layout_manager")
            if layout_manager and hasattr(
                layout_manager, "transition_to_start_position_picker"
            ):
                layout_manager.transition_to_start_position_picker()

    def _handle_start_position_selected(self, position_key: str):
        """Handle start position selection signal."""
        self.logger.info(f"Handling start position selected: {position_key}")

        # Prepare option picker
        option_picker_manager = self.components.get("option_picker_manager")
        if option_picker_manager and hasattr(
            option_picker_manager, "prepare_from_start_position"
        ):
            option_picker_manager.prepare_from_start_position(position_key)

        # Transition to option picker
        layout_manager = self.components.get("layout_manager")
        if layout_manager and hasattr(layout_manager, "transition_to_option_picker"):
            layout_manager.transition_to_option_picker()

    def _handle_option_picker_selection(self, pictograph_data: Any):
        """Handle option picker selection signal."""
        self.logger.info(
            f"Handling option picker selection: {getattr(pictograph_data, 'letter', 'unknown')}"
        )

        # Emit beat addition (this will trigger the beat_added signal)
        self.publish_beat_added(pictograph_data, 0, {"id": "current", "length": 1})

    def _handle_layout_recalculated(self, layout_data: dict):
        """Handle layout recalculation signal."""
        self.logger.info("Handling layout recalculated")

        # Apply layout changes to workbench
        workbench = self.components.get("workbench")
        if workbench and hasattr(workbench, "apply_layout_changes"):
            workbench.apply_layout_changes(layout_data)

    def _handle_component_resized(self, component_name: str, new_size: Any):
        """Handle component resize signal."""
        self.logger.info(f"Handling component resized: {component_name}")

        # Trigger layout updates
        layout_manager = self.components.get("layout_manager")
        if layout_manager and hasattr(layout_manager, "handle_component_resize"):
            layout_manager.handle_component_resize(component_name, new_size)

    def _handle_layout_transition(self, target_view: str):
        """Handle layout transition request signal."""
        self.logger.info(f"Handling layout transition: {target_view}")

        layout_manager = self.components.get("layout_manager")
        if layout_manager:
            if target_view == "option_picker" and hasattr(
                layout_manager, "transition_to_option_picker"
            ):
                layout_manager.transition_to_option_picker()
            elif target_view == "start_position_picker" and hasattr(
                layout_manager, "transition_to_start_position_picker"
            ):
                layout_manager.transition_to_start_position_picker()

    # Publishing methods (maintains interface compatibility)

    def publish_sequence_created(self, sequence_data):
        """Publish sequence creation (emits Qt signal)."""
        sequence_id = sequence_data.get("id", "")
        name = sequence_data.get("name", "")
        length = sequence_data.get("length", 0)
        self.signal_coordinator.emit_sequence_created(sequence_id, name, length)

    def publish_beat_added(self, beat_data, position, sequence):
        """Publish beat addition (emits Qt signal)."""
        sequence_id = sequence.get("id", "")
        total_beats = sequence.get("length", 0)
        self.signal_coordinator.emit_beat_added(
            sequence_id, beat_data, position, total_beats
        )

    def publish_beat_updated(
        self, sequence_id, beat_number, field, old_value, new_value
    ):
        """Publish beat update (emits Qt signal)."""
        self.signal_coordinator.emit_beat_updated(
            sequence_id, beat_number, field, old_value, new_value
        )

    def publish_ui_state_change(self, component, state_key, old_value, new_value):
        """Publish UI state change (emits Qt signal)."""
        if component == "start_position_picker" and state_key == "position_selected":
            self.signal_coordinator.emit_start_position_selected(new_value)
        elif component == "option_picker" and state_key == "pictograph_selected":
            self.signal_coordinator.emit_option_picker_selection(new_value)

    # Cleanup

    def shutdown(self):
        """Cleanup signal integration."""
        self.signal_coordinator.cleanup()
        self.components.clear()
        self.logger.info("Signal integration adapter shutdown complete")
