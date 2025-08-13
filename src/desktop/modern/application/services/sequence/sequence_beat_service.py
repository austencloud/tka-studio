"""
Pure Sequence Beat Service

Clean service implementation without Qt dependencies that implements ISequenceBeatOperations.
This service handles beat operations on sequences using pure business logic.
"""

from collections.abc import Callable
from typing import Any

from desktop.modern.application.services.data.modern_to_legacy_converter import (
    ModernToLegacyConverter,
)
from desktop.modern.application.services.sequence.beat_factory import BeatFactory
from desktop.modern.application.services.sequence.sequence_persister import (
    SequencePersister,
)
from desktop.modern.core.interfaces.sequence_operation_services import (
    ISequenceBeatOperations,
)
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData


class SequenceBeatService(ISequenceBeatOperations):
    """
    Pure service for handling beat-level operations on sequences.

    This is a clean implementation without Qt dependencies that focuses
    solely on business logic for beat operations.
    """

    def __init__(
        self,
        sequence_getter: Callable[[], SequenceData] | None = None,
        sequence_setter: Callable[[SequenceData], None] | None = None,
        persister: SequencePersister | None = None,
    ):
        """
        Initialize the sequence beat service.

        Args:
            sequence_getter: Function to get current sequence
            sequence_setter: Function to set current sequence
            persister: Service for persisting sequences
        """
        self.sequence_getter = sequence_getter
        self.sequence_setter = sequence_setter
        self.persister = persister or SequencePersister()
        self.converter = ModernToLegacyConverter()

    def get_current_sequence(self) -> SequenceData | None:
        """Get the current sequence."""
        if self.sequence_getter:
            return self.sequence_getter()
        return None

    def set_current_sequence(self, sequence: SequenceData) -> None:
        """Set the current sequence."""
        if self.sequence_setter:
            self.sequence_setter(sequence)

    # Interface implementation methods
    def add_beat(self, sequence: Any, beat: Any, position: int | None = None) -> Any:
        """Add beat to sequence (interface implementation)."""
        if not isinstance(sequence, SequenceData):
            sequence = self.get_current_sequence()
            if not sequence:
                raise ValueError("No current sequence available")

        # Calculate position if not provided
        if position is None:
            position = len(sequence.beats)

        # Create new beats list with inserted beat
        new_beats = sequence.beats.copy()
        new_beats.insert(position, beat)

        # Create updated sequence
        updated_sequence = sequence.update(beats=new_beats)

        # Update current sequence
        self.set_current_sequence(updated_sequence)

        # Persist changes
        self._save_sequence_to_persistence(updated_sequence)

        return updated_sequence

    def remove_beat(self, sequence: Any, position: int) -> Any:
        """Remove beat from sequence (interface implementation)."""
        if not isinstance(sequence, SequenceData):
            sequence = self.get_current_sequence()
            if not sequence:
                raise ValueError("No current sequence available")

        if position < 0 or position >= len(sequence.beats):
            raise IndexError(f"Beat position {position} out of range")

        # Create new beats list without the removed beat
        new_beats = sequence.beats.copy()
        del new_beats[position]

        # Create updated sequence
        updated_sequence = sequence.update(beats=new_beats)

        # Update current sequence
        self.set_current_sequence(updated_sequence)

        # Persist changes
        self._save_sequence_to_persistence(updated_sequence)

        return updated_sequence

    def update_beat(self, sequence: Any, position: int, beat: Any) -> Any:
        """Update beat in sequence (interface implementation)."""
        if not isinstance(sequence, SequenceData):
            sequence = self.get_current_sequence()
            if not sequence:
                raise ValueError("No current sequence available")

        if position < 0 or position >= len(sequence.beats):
            raise IndexError(f"Beat position {position} out of range")

        # Create new beats list with updated beat
        new_beats = sequence.beats.copy()
        new_beats[position] = beat

        # Create updated sequence
        updated_sequence = sequence.update(beats=new_beats)

        # Update current sequence
        self.set_current_sequence(updated_sequence)

        # Persist changes
        self._save_sequence_to_persistence(updated_sequence)

        return updated_sequence

    def get_beat_count(self, sequence: Any) -> int:
        """Get number of beats in sequence (interface implementation)."""
        if hasattr(sequence, "beats"):
            return len(sequence.beats)
        return 0

    def validate_beat_addition(
        self, sequence: Any, beat: Any, position: int | None = None
    ) -> bool:
        """Validate if beat can be added (interface implementation)."""
        try:
            # Basic validation - check if beat has required attributes
            if not hasattr(beat, "letter"):
                return False

            # Check position validity
            if position is not None:
                beat_count = self.get_beat_count(sequence)
                if position < 0 or position > beat_count:
                    return False

            return True
        except Exception:
            return False

    def add_pictograph_to_sequence(self, pictograph_data: PictographData) -> BeatData:
        """Add pictograph to sequence by creating beat with embedded pictograph."""
        current_sequence = self.get_current_sequence()
        if not current_sequence:
            raise ValueError("No current sequence available")

        # Calculate beat number
        beat_number = len(current_sequence.beats) + 1

        # Create beat data with embedded pictograph using factory
        beat_data = BeatFactory.create_from_pictograph(
            pictograph_data=pictograph_data, beat_number=beat_number
        )

        # Add beat to sequence
        self.add_beat(current_sequence, beat_data)

        return beat_data

    def update_beat_turns(self, beat: BeatData, color: str, new_turns: Any) -> None:
        """Update turns for a specific beat and color."""
        current_sequence = self.get_current_sequence()
        if not current_sequence:
            raise ValueError("No current sequence available")

        # Find beat index
        beat_index = None
        for i, seq_beat in enumerate(current_sequence.beats):
            if seq_beat == beat:
                beat_index = i
                break

        if beat_index is None:
            raise ValueError("Beat not found in current sequence")

        # Update beat with new turns
        if color.lower() == "blue" and beat.blue_motion:
            updated_motion = beat.blue_motion.update(turns=new_turns)
            updated_beat = beat.update(blue_motion=updated_motion)
        elif color.lower() == "red" and beat.red_motion:
            updated_motion = beat.red_motion.update(turns=new_turns)
            updated_beat = beat.update(red_motion=updated_motion)
        else:
            raise ValueError(f"Invalid color or motion not found: {color}")

        # Update sequence
        self.update_beat(current_sequence, beat_index, updated_beat)

    def _save_sequence_to_persistence(self, sequence: SequenceData) -> None:
        """Save sequence to persistence layer."""
        try:
            if self.persister:
                # Convert to legacy format for persistence
                legacy_data = self.converter.convert_sequence_to_legacy(sequence)
                self.persister.save_sequence(legacy_data)
        except Exception as e:
            # Log error but don't fail the operation
            print(f"Warning: Failed to persist sequence: {e}")

    def _calculate_next_beat_number(self, sequence: SequenceData) -> int:
        """Calculate the next beat number for the sequence."""
        if not sequence.beats:
            return 1
        return len(sequence.beats) + 1
