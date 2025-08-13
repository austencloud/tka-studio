"""
Workbench Coordination Service

Handles coordination between workbench components and external systems.
Extracted from the large workbench component and signal coordinator.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.application.services.workbench.workbench_operation_coordinator import (
    OperationType,
    WorkbenchOperationCoordinator,
)
from desktop.modern.application.services.workbench.workbench_state_manager import (
    WorkbenchStateManager,
)
from desktop.modern.domain.models import BeatData, SequenceData


if TYPE_CHECKING:
    from desktop.modern.application.services.workbench.workbench_ui_service import (
        WorkbenchUIService,
    )


class WorkbenchCoordinationService(QObject):
    """
    Service for coordinating workbench operations and state changes.

    Responsibilities:
    - Signal connection management
    - Operation coordination
    - State synchronization
    - Event handling
    """

    # Signals for external coordination
    sequence_modified = pyqtSignal(object)
    operation_completed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    beat_selected = pyqtSignal(int)

    def __init__(
        self,
        state_manager: WorkbenchStateManager,
        operation_coordinator: WorkbenchOperationCoordinator,
        ui_service: WorkbenchUIService,
    ):
        super().__init__()
        self._state_manager = state_manager
        self._operation_coordinator = operation_coordinator
        self._ui_service = ui_service

    def setup_workbench_signals(self, workbench: Any) -> None:
        """Set up workbench signal connections."""
        beat_frame_section = self._ui_service.get_beat_frame_section()
        if not beat_frame_section:
            return

        # Connect beat frame signals to handlers
        beat_frame_section.beat_selected.connect(self._on_beat_selected)
        beat_frame_section.beat_modified.connect(self._on_beat_modified)
        beat_frame_section.sequence_modified.connect(self._on_sequence_modified)

        # Connect operation signals
        beat_frame_section.add_to_dictionary_requested.connect(
            lambda: self._execute_operation(OperationType.ADD_TO_DICTIONARY)
        )
        beat_frame_section.view_fullscreen_requested.connect(
            lambda: self._execute_operation(OperationType.VIEW_FULLSCREEN)
        )
        beat_frame_section.mirror_sequence_requested.connect(
            lambda: self._execute_operation(OperationType.MIRROR_SEQUENCE)
        )
        beat_frame_section.swap_colors_requested.connect(
            lambda: self._execute_operation(OperationType.SWAP_COLORS)
        )
        beat_frame_section.rotate_sequence_requested.connect(
            lambda: self._execute_operation(OperationType.ROTATE_SEQUENCE)
        )
        beat_frame_section.copy_json_requested.connect(
            lambda: self._execute_operation(OperationType.COPY_JSON)
        )
        beat_frame_section.delete_beat_requested.connect(self._handle_delete_beat)
        beat_frame_section.clear_sequence_requested.connect(self._handle_clear)

    def handle_workbench_operation(self, operation_type: str, **kwargs) -> None:
        """Handle workbench operations."""
        try:
            operation_enum = OperationType(operation_type)
            self._execute_operation(operation_enum, **kwargs)
        except ValueError:
            self.error_occurred.emit(f"Unknown operation type: {operation_type}")

    def update_workbench_state(self, sequence: SequenceData | None) -> None:
        """Update workbench state."""
        if sequence:
            self._state_manager.set_sequence(sequence)
        self._ui_service.update_sequence_display(sequence)

    def _execute_operation(self, operation_type: OperationType, **kwargs):
        """Execute a workbench operation."""
        try:
            result = self._operation_coordinator.execute_operation(
                operation_type, **kwargs
            )

            if result.success:
                self._ui_service.show_operation_feedback(
                    operation_type.value, f"✅ {result.message}", 3000
                )
                self.operation_completed.emit(result.message)

                # Update UI if sequence was modified
                if result.updated_sequence:
                    self.update_workbench_state(result.updated_sequence)
                    self.sequence_modified.emit(result.updated_sequence)
            else:
                self._ui_service.show_operation_feedback(
                    operation_type.value, f"❌ {result.message}", 3000
                )
                self.error_occurred.emit(result.message)

        except Exception as e:
            error_msg = f"Operation failed: {e}"
            self._ui_service.show_operation_feedback(
                operation_type.value, f"❌ {error_msg}", 3000
            )
            self.error_occurred.emit(error_msg)

    def _on_beat_selected(self, beat_index: int):
        """Handle beat selection from UI."""
        self._ui_service.update_beat_selection(beat_index)
        self.beat_selected.emit(beat_index)

    def _on_beat_modified(self, beat_index: int, beat_data: BeatData):
        """Handle beat modification from UI."""
        sequence = self._state_manager.get_current_sequence()
        if sequence and beat_index < len(sequence.beats):
            new_beats = list(sequence.beats)
            new_beats[beat_index] = beat_data
            updated_sequence = sequence.update(beats=new_beats)

            self.update_workbench_state(updated_sequence)
            self.sequence_modified.emit(updated_sequence)

    def _on_sequence_modified(self, sequence: SequenceData):
        """Handle sequence modification from UI."""
        self.update_workbench_state(sequence)
        self.sequence_modified.emit(sequence)

    def _handle_delete_beat(self):
        """Handle delete beat request."""
        self._execute_operation(OperationType.DELETE_BEAT)

    def _handle_clear(self):
        """Handle clear sequence request."""
        self._execute_operation(OperationType.CLEAR_SEQUENCE)
