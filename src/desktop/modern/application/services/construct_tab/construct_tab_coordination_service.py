"""
Construct Tab Coordination Service

Handles coordination between construct tab components.
Replaces the large SignalCoordinator with focused coordination logic.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.application.services.sequence.sequence_beat_operations import (
    SequenceBeatOperations,
)
from desktop.modern.application.services.sequence.sequence_start_position_manager import (
    SequenceStartPositionManager,
)
from desktop.modern.domain.models import BeatData, SequenceData


class ConstructTabCoordinationService(QObject):
    """
    Service for coordinating construct tab components.

    Responsibilities:
    - Component signal coordination
    - Sequence state management
    - UI transition coordination
    - Event handling and forwarding

    Replaces the 531-line SignalCoordinator with focused logic.
    """

    # External signals
    sequence_created = pyqtSignal(object)
    sequence_modified = pyqtSignal(object)
    start_position_set = pyqtSignal(str)
    generation_completed = pyqtSignal(bool, str)

    def __init__(
        self,
        beat_operations: SequenceBeatOperations,
        start_position_manager: SequenceStartPositionManager,
        layout_service,  # IConstructTabLayoutService
    ):
        super().__init__()
        self._beat_operations = beat_operations
        self._start_position_manager = start_position_manager
        self._layout_service = layout_service

        # Component references
        self._components: dict[str, Any] = {}

        # State tracking
        self._handling_sequence_modification = False

    def setup_component_coordination(self, components: dict[str, Any]) -> None:
        """Set up coordination between components."""
        self._components = components

        # Connect component signals
        self._connect_start_position_picker_signals()
        self._connect_option_picker_signals()
        self._connect_workbench_signals()
        self._connect_beat_operations_signals()
        self._connect_start_position_manager_signals()

    def _connect_start_position_picker_signals(self):
        """Connect start position picker signals."""
        start_position_picker = self._components.get("start_position_picker")
        if start_position_picker and hasattr(
            start_position_picker, "start_position_selected"
        ):
            start_position_picker.start_position_selected.connect(
                self._handle_start_position_selected
            )

    def _connect_option_picker_signals(self):
        """Connect option picker signals."""
        option_picker = self._components.get("option_picker")
        if option_picker and hasattr(option_picker, "pictograph_selected"):
            # Prevent duplicate connections
            try:
                option_picker.pictograph_selected.disconnect(
                    self._beat_operations.add_pictograph_to_sequence
                )
            except TypeError:
                pass  # Signal was not connected

            option_picker.pictograph_selected.connect(
                self._beat_operations.add_pictograph_to_sequence
            )

    def _connect_workbench_signals(self):
        """Connect workbench signals."""
        workbench = self._components.get("workbench")
        if workbench:
            if hasattr(workbench, "sequence_modified"):
                workbench.sequence_modified.connect(self._handle_workbench_modified)
            if hasattr(workbench, "operation_completed"):
                workbench.operation_completed.connect(self._handle_operation_completed)

    def _connect_beat_operations_signals(self):
        """Connect beat operations signals."""
        self._beat_operations.beat_added.connect(self._on_beat_modified)
        self._beat_operations.beat_removed.connect(self._on_beat_modified)
        self._beat_operations.beat_updated.connect(self._on_beat_modified)

    def _connect_start_position_manager_signals(self):
        """Connect start position manager signals."""
        self._start_position_manager.start_position_set.connect(
            self._on_start_position_set
        )
        self._start_position_manager.start_position_updated.connect(
            self._on_start_position_updated
        )

    def handle_sequence_modified(self, sequence: SequenceData) -> None:
        """Handle sequence modification events."""
        if self._handling_sequence_modification:
            return

        try:
            self._handling_sequence_modification = True
            self._update_ui_based_on_sequence(sequence)
            self.sequence_modified.emit(sequence)
        finally:
            self._handling_sequence_modification = False

    def handle_start_position_set(self, start_position: BeatData) -> None:
        """Handle start position set events."""
        self._start_position_manager.set_start_position(start_position)

    def handle_beat_added(self, beat_data: BeatData) -> None:
        """Handle beat added events."""
        self._beat_operations.add_pictograph_to_sequence(beat_data)

    def handle_generation_request(self, generation_config: dict[str, Any]) -> None:
        """Handle generation request events."""
        # For now, just emit completion signal
        # Actual generation logic would be implemented here
        self.generation_completed.emit(True, "Generation completed")

    def handle_ui_transition_request(self, target_panel: str) -> None:
        """Handle UI transition requests."""
        transition_map = {
            "start_position_picker": self._layout_service.transition_to_start_position_picker,
            "option_picker": self._layout_service.transition_to_option_picker,
            "graph_editor": self._layout_service.transition_to_graph_editor,
            "generate_controls": self._layout_service.transition_to_generate_controls,
            "export_panel": self._layout_service.transition_to_export_panel,
        }

        transition_method = transition_map.get(target_panel)
        if transition_method:
            transition_method()

    def _handle_start_position_selected(
        self, position_key: str, start_position_data: BeatData
    ):
        """Handle start position selection."""
        self._start_position_manager.set_start_position(start_position_data)
        self._layout_service.transition_to_option_picker()
        self.start_position_set.emit(position_key)

    def _handle_workbench_modified(self, sequence: SequenceData):
        """Handle workbench sequence modification."""
        self.handle_sequence_modified(sequence)

    def _handle_operation_completed(self, message: str):
        """Handle workbench operation completion."""
        # Could emit operation completed signal if needed
        pass

    def _on_beat_modified(self, *args):
        """Handle beat modification events."""
        # Get current sequence and update UI
        if len(args) >= 3:
            # beat_added signal with updated sequence
            updated_sequence = args[2]
            self.handle_sequence_modified(updated_sequence)
        else:
            # Other beat modification signals - get current sequence
            workbench = self._components.get("workbench")
            if workbench and hasattr(workbench, "get_sequence"):
                current_sequence = workbench.get_sequence()
                if current_sequence:
                    self.handle_sequence_modified(current_sequence)

    def _on_start_position_set(self, start_position_data: BeatData):
        """Handle start position set."""
        workbench = self._components.get("workbench")
        if workbench and hasattr(workbench, "set_start_position"):
            workbench.set_start_position(start_position_data)

    def _on_start_position_updated(self, start_position_data: BeatData):
        """Handle start position updated."""
        self._on_start_position_set(start_position_data)  # Same handling

    def _update_ui_based_on_sequence(self, sequence: SequenceData):
        """Update UI based on sequence state."""
        # Determine which panel to show based on sequence state
        has_start_position = self._start_position_manager.has_start_position()
        has_beats = sequence and sequence.length > 0 and not sequence.is_empty()

        if has_start_position or has_beats:
            self._layout_service.transition_to_option_picker()
        else:
            self._layout_service.transition_to_start_position_picker()
