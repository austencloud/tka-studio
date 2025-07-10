"""
Sequence Manager Qt Adapter - Presentation Layer Interface

This adapter provides Qt signal functionality for the SequenceManager business service.
It implements the adapter pattern to maintain separation between presentation and application layers.
"""

import logging
from typing import Callable, Optional

from application.services.core.sequence_manager import (
    ISequenceManagerSignals,
    SequenceManager,
)
from domain.models.beat_data import BeatData
from domain.models.sequence_models import SequenceData
from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)


class SequenceManagerQtAdapter(QObject, ISequenceManagerSignals):
    """
    Qt adapter for the SequenceManager service.

    This adapter handles Qt-specific signal emission while delegating
    all business logic to the SequenceManager service.
    """

    sequence_modified = pyqtSignal(object)  # SequenceData object
    sequence_cleared = pyqtSignal()

    def __init__(
        self,
        workbench_getter: Optional[Callable[[], object]] = None,
        workbench_setter: Optional[Callable[[SequenceData], None]] = None,
        start_position_handler: Optional[object] = None,
    ):
        """
        Initialize the Qt adapter with the sequence manager.

        Args:
            workbench_getter: Function to get current workbench
            workbench_setter: Function to set workbench sequence
            start_position_handler: Handler for start position operations
        """
        super().__init__()

        # Create the business service with this adapter as signal emitter
        self._sequence_manager = SequenceManager(
            workbench_getter=workbench_getter,
            workbench_setter=workbench_setter,
            start_position_handler=start_position_handler,
            signal_emitter=self,
        )

    # ISequenceManagerSignals implementation
    def emit_sequence_modified(self, sequence: SequenceData) -> None:
        """Emit Qt signal when sequence is modified."""
        self.sequence_modified.emit(sequence)

    def emit_sequence_cleared(self) -> None:
        """Emit Qt signal when sequence is cleared."""
        self.sequence_cleared.emit()

    # Public API - delegate to business service
    def add_beat_to_sequence(self, beat_data: BeatData):
        """Add a beat to the current sequence"""
        self._sequence_manager.add_beat_to_sequence(beat_data)

    def clear_sequence(self):
        """Clear the current sequence"""
        self._sequence_manager.clear_sequence()

    def handle_workbench_modified(self, sequence: SequenceData):
        """Handle workbench sequence modification"""
        self._sequence_manager.handle_workbench_modified(sequence)

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int):
        """Update the number of turns for a specific beat"""
        self._sequence_manager.update_beat_turns(beat_index, color, new_turns)

    def remove_beat(self, beat_index: int):
        """Remove a beat from the sequence"""
        self._sequence_manager.remove_beat(beat_index)

    def set_start_position(self, start_position_data: BeatData):
        """Set the start position"""
        self._sequence_manager.set_start_position(start_position_data)

    def load_sequence_on_startup(self):
        """Load sequence from current_sequence.json on startup"""
        self._sequence_manager.load_sequence_on_startup()

    def get_current_sequence_length(self) -> int:
        """Get the length of the current sequence"""
        return self._sequence_manager.get_current_sequence_length()

    @property
    def sequence_manager(self) -> SequenceManager:
        """Access to the underlying business service (use sparingly)"""
        return self._sequence_manager
