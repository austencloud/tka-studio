"""
SequenceBeatOperations - Refactored to Use Focused Services

This class now serves as a thin adapter that delegates to focused services
via the BeatOperationCoordinator. The God Object has been broken down into:

- BeatCreationService: Beat creation logic
- BeatSequenceService: Sequence manipulation
- SequenceWordCalculator: Word calculation
- SequencePersistenceAdapter: Save/load logic
- BeatOperationCoordinator: Orchestrates the above

REFACTORING COMPLETE: From 21KB God Object to clean coordinator pattern!
"""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtCore import QObject, pyqtSignal
from shared.application.services.data.modern_to_legacy_converter import (
    ModernToLegacyConverter,
)

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData

from .beat_operation_coordinator import BeatOperationCoordinator


class SequenceBeatOperations(QObject):
    """
    Service for handling beat-level operations on sequences.

    REFACTORED: Now delegates to focused services via BeatOperationCoordinator.

    Responsibilities:
    - Providing backward-compatible API
    - Delegating to focused services
    - Emitting Qt signals for UI integration
    """

    # Delegate signals from coordinator
    beat_added = pyqtSignal(object, int, object)  # BeatData, position, SequenceData
    beat_removed = pyqtSignal(int)  # position
    beat_updated = pyqtSignal(object, int)  # BeatData, position

    def __init__(
        self,
        workbench_getter: Callable[[], object] | None = None,
        workbench_setter: Callable[[SequenceData], None] | None = None,
        modern_to_legacy_converter: ModernToLegacyConverter | None = None,
    ):
        super().__init__()

        # Create the coordinator with focused services
        self.coordinator = BeatOperationCoordinator(
            workbench_getter=workbench_getter,
            workbench_setter=workbench_setter,
        )

        # Connect coordinator signals to our signals for backward compatibility
        self.coordinator.beat_added.connect(self.beat_added.emit)
        self.coordinator.beat_removed.connect(self.beat_removed.emit)
        self.coordinator.beat_updated.connect(self.beat_updated.emit)

        # Legacy properties for backward compatibility
        self.workbench_getter = workbench_getter
        self.workbench_setter = workbench_setter
        self.modern_to_legacy_converter = (
            modern_to_legacy_converter or ModernToLegacyConverter()
        )

    # DELEGATION METHODS - All delegate to coordinator

    def add_pictograph_to_sequence(self, pictograph_data: PictographData):
        """Add pictograph to sequence by creating beat with embedded pictograph."""
        return self.coordinator.add_pictograph_to_sequence(pictograph_data)

    def add_beat_to_sequence(self, beat_data: BeatData):
        """Add beat to sequence using the most appropriate method"""
        return self.coordinator.add_beat_to_sequence(beat_data)

    def update_beat_turns(self, beat_index: int, color: str, new_turns: int):
        """Update the number of turns for a specific beat - exactly like legacy"""
        return self.coordinator.update_beat_turns(beat_index, color, new_turns)

    def update_beat_orientation(
        self, beat_index: int, color: str, new_orientation: int
    ):
        """Update the orientation for a specific beat"""
        return self.coordinator.update_beat_orientation(
            beat_index, color, new_orientation
        )

    def remove_beat(self, beat_index: int):
        """Remove a beat from the sequence"""
        return self.coordinator.remove_beat(beat_index)

    def delete_beat(self, sequence: SequenceData, beat_index: int) -> SequenceData:
        """Delete beat and all following beats from the sequence (legacy behavior)."""
        return self.coordinator.delete_beat(sequence, beat_index)

    def get_current_sequence(self) -> SequenceData | None:
        """Get the current sequence from workbench"""
        return self.coordinator.get_current_sequence()

    # LEGACY METHODS - Keep for backward compatibility

    def _calculate_next_beat_number(self, current_sequence: SequenceData | None) -> int:
        """Calculate the next beat number for a new beat."""
        return self.coordinator.beat_creator.calculate_next_beat_number(
            current_sequence
        )

    def _add_beat_direct(self, beat_data: BeatData):
        """Fallback method: Add beat via direct manipulation (original logic)"""
        # This is now handled by the coordinator's add_beat_to_sequence method
        return self.coordinator.add_beat_to_sequence(beat_data)

    def _save_sequence_to_persistence(self, sequence: SequenceData):
        """Convert modern SequenceData to legacy format and save to current_sequence.json"""
        word = self.coordinator.word_calculator.calculate_word(sequence)
        return self.coordinator.persistence.save_sequence(sequence, word)

    def _calculate_sequence_word(self, sequence: SequenceData) -> str:
        """Calculate sequence word from beat letters exactly like legacy"""
        return self.coordinator.word_calculator.calculate_word(sequence)

    def _simplify_repeated_word(self, word: str) -> str:
        """Simplify repeated patterns exactly like legacy WordSimplifier"""
        return self.coordinator.word_calculator.simplify_repeated_word(word)

    def get_beat_service(self):
        """Get the pure beat service for interface-based operations."""
        # Return the sequence service from coordinator
        return self.coordinator.sequence_service
