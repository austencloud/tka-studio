"""
Qt Adapter for Sequence State Tracker Service

This adapter wraps the pure SequenceStateTrackerService to provide Qt-specific signal coordination.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from PyQt6.QtCore import QObject, pyqtSignal
from shared.application.services.sequence.sequence_state_tracker_service import (
    SequenceStateTrackerService,
)

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


logger = logging.getLogger(__name__)


class QtSequenceStateTrackerAdapter(QObject):
    """
    Qt adapter for SequenceStateTrackerService.

    This adapter provides Qt signal coordination for the pure service.
    """

    # Qt signals for state updates (these replace the complex signal chains)
    sequence_updated = pyqtSignal(object)  # SequenceData
    start_position_updated = pyqtSignal(object)  # BeatData
    state_changed = pyqtSignal()  # General state change notification

    def __init__(self, event_bus, command_processor):
        super().__init__()

        # Create the pure service
        self.service = SequenceStateTrackerService(event_bus, command_processor)

        # Connect service callbacks to Qt signals
        self.service.add_sequence_updated_callback(self._on_sequence_updated)
        self.service.add_start_position_updated_callback(
            self._on_start_position_updated
        )
        self.service.add_state_changed_callback(self._on_state_changed)

    def get_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence"""
        return self.service.get_sequence()

    def get_start_position(self) -> Optional[BeatData]:
        """Get the current start position"""
        return self.service.get_start_position()

    def has_sequence(self) -> bool:
        """Check if there's a current sequence"""
        return self.service.has_sequence()

    def has_start_position(self) -> bool:
        """Check if there's a start position set"""
        return self.service.has_start_position()

    def is_empty(self) -> bool:
        """Check if both sequence and start position are empty"""
        return self.service.is_empty()

    def set_sequence_direct(self, sequence: Optional[SequenceData]):
        """Set sequence directly (for loading scenarios, bypasses commands)"""
        self.service.set_sequence_direct(sequence)

    def set_start_position_direct(self, start_position: Optional[BeatData]):
        """Set start position directly (for loading scenarios, bypasses commands)"""
        self.service.set_start_position_direct(start_position)

    def get_state_summary(self) -> dict[str, Any]:
        """Get a summary of current state."""
        return self.service.get_state_summary()

    def cleanup(self):
        """Cleanup resources when the state manager is being destroyed"""
        self.service.cleanup()

    def _on_sequence_updated(self, sequence: Optional[SequenceData]):
        """Handle sequence updated callback from service."""
        self.sequence_updated.emit(sequence)

    def _on_start_position_updated(self, start_position: Optional[BeatData]):
        """Handle start position updated callback from service."""
        self.start_position_updated.emit(start_position)

    def _on_state_changed(self):
        """Handle state changed callback from service."""
        self.state_changed.emit()

    # Pass-through methods for direct service access
    def add_sequence_updated_callback(self, callback):
        """Add callback for when sequence is updated."""
        self.service.add_sequence_updated_callback(callback)

    def add_start_position_updated_callback(self, callback):
        """Add callback for when start position is updated."""
        self.service.add_start_position_updated_callback(callback)

    def add_state_changed_callback(self, callback):
        """Add callback for when state changes."""
        self.service.add_state_changed_callback(callback)
