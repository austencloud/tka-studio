"""
Sequence Restoration Service

Domain-specific service for sequence restoration logic.
Extracted from ApplicationLifecycleManager to follow single responsibility principle.

PROVIDES:
- Sequence restoration from session data
- Sequence name calculation from beats
- Word simplification for circular sequences
"""

from abc import ABC, abstractmethod
from typing import Optional

from desktop.modern.core.interfaces.session_services import SessionState
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


class ISequenceRestorer(ABC):
    """Interface for sequence restoration operations."""

    @abstractmethod
    def restore_sequence_from_session(
        self, session_data: SessionState
    ) -> Optional[SequenceData]:
        """Restore sequence from session data."""

    @abstractmethod
    def calculate_sequence_name(self, beat_objects: list[BeatData]) -> str:
        """Calculate sequence name from beat letters."""


class SequenceRestorer(ISequenceRestorer):
    """
    Domain-specific service for sequence restoration logic.

    Handles sequence data reconstruction from session and sequence name calculation
    without any UI or window management dependencies.
    """

    def restore_sequence_from_session(
        self, session_data: SessionState
    ) -> Optional[SequenceData]:
        """Restore sequence from session data."""
        if (
            not session_data.current_sequence_id
            or not session_data.current_sequence_data
        ):
            return None

        try:
            # Convert sequence data back to SequenceData object if needed
            sequence_data = session_data.current_sequence_data
            if isinstance(sequence_data, dict):
                beats_data = sequence_data.get("beats", [])

                # Convert beat dicts back to BeatData objects
                beat_objects = []
                for beat_dict in beats_data:
                    if isinstance(beat_dict, dict):
                        beat_obj = BeatData.from_dict(beat_dict)
                        beat_objects.append(beat_obj)
                    else:
                        beat_objects.append(beat_dict)

                # Convert dict back to SequenceData object
                sequence_data = SequenceData(
                    id=sequence_data.get("id", session_data.current_sequence_id),
                    name=sequence_data.get("name", "Restored Sequence"),
                    beats=beat_objects,
                )

                # CRITICAL FIX: Recalculate sequence name from beat letters exactly like legacy
                if beat_objects:
                    calculated_word = self.calculate_sequence_name(beat_objects)
                    sequence_data = sequence_data.update(name=calculated_word)
            else:
                # CRITICAL FIX: Also recalculate name for existing SequenceData objects
                if sequence_data.beats:
                    calculated_word = self.calculate_sequence_name(sequence_data.beats)
                    sequence_data = sequence_data.update(name=calculated_word)

            return sequence_data

        except Exception as e:
            print(f"⚠️ Failed to restore sequence from session: {e}")
            return None

    def calculate_sequence_name(self, beat_objects: list[BeatData]) -> str:
        """Calculate sequence word from beat letters exactly like legacy SequencePropertiesManager"""
        if not beat_objects:
            return ""

        # Extract letters from beats exactly like legacy calculate_word method
        word = "".join(
            beat.pictograph_data.letter
            for beat in beat_objects
            if hasattr(beat, "pictograph_data")
        )

        # Apply word simplification for circular sequences like legacy
        return self._simplify_repeated_word(word)

    def _simplify_repeated_word(self, word: str) -> str:
        """Simplify repeated patterns exactly like legacy WordSimplifier"""

        def can_form_by_repeating(s: str, pattern: str) -> bool:
            pattern_len = len(pattern)
            return all(s[i] == pattern[i % pattern_len] for i in range(len(s)))

        if not word:
            return word

        # Try patterns from length 1 to half the word length
        for pattern_len in range(1, len(word) // 2 + 1):
            pattern = word[:pattern_len]
            if can_form_by_repeating(word, pattern):
                # Check if the pattern repeats at least twice
                if len(word) >= pattern_len * 2:
                    return pattern

        return word
