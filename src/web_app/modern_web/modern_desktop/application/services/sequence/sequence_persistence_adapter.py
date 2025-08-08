"""
SequencePersistenceAdapter - Focused Service for Sequence Persistence

Single Responsibility: Saving and loading sequences with format conversion.
Extracted from SequenceBeatOperations God Object.
"""

from __future__ import annotations

from typing import Any, Optional

from shared.application.services.data.modern_to_legacy_converter import (
    ModernToLegacyConverter,
)
from shared.application.services.sequence.sequence_persister import SequencePersister

from desktop.modern.domain.models.sequence_data import SequenceData


class SequencePersistenceAdapter:
    """
    Service focused solely on sequence persistence operations.

    Responsibilities:
    - Converting modern sequences to legacy format
    - Saving sequences to persistence
    - Loading sequences from persistence
    - Managing sequence metadata
    """

    def __init__(
        self,
        converter: Optional[ModernToLegacyConverter] = None,
        persister: Optional[SequencePersister] = None,
    ):
        self.converter = converter or ModernToLegacyConverter()
        self.persister = persister or SequencePersister()

    def save_sequence(self, sequence: SequenceData, word: str = "") -> None:
        """
        Save sequence to persistence in legacy format.

        Args:
            sequence: The modern sequence to save
            word: Pre-calculated word (optional)
        """
        try:
            # Load existing sequence to preserve start position
            existing_sequence = self.persister.load_current_sequence()

            # Check if there's an existing start position (beat 0)
            existing_start_position = None
            if len(existing_sequence) > 1 and existing_sequence[1].get("beat") == 0:
                existing_start_position = existing_sequence[1]

            # Convert beats to legacy format (these will be beat 1, 2, 3, etc.)
            legacy_beats = self._convert_beats_to_legacy(sequence)

            # Create metadata
            metadata = self._create_sequence_metadata(sequence, word)

            # Build complete sequence
            complete_sequence = [metadata]

            # Add start position if it exists
            if existing_start_position:
                complete_sequence.append(existing_start_position)

            # Add beats
            complete_sequence.extend(legacy_beats)

            # Save to persistence
            self.persister.save_current_sequence(complete_sequence)

        except Exception as e:
            print(f"❌ Failed to save sequence to persistence: {e}")
            import traceback

            traceback.print_exc()

    def _convert_beats_to_legacy(self, sequence: SequenceData) -> list[dict[str, Any]]:
        """
        Convert modern beats to legacy format.

        Args:
            sequence: The sequence containing beats to convert

        Returns:
            List of legacy beat dictionaries
        """
        legacy_beats = []

        for i, beat in enumerate(sequence.beats):
            try:
                beat_dict = self.converter.convert_beat_data_to_legacy_format(
                    beat, i + 1
                )
                legacy_beats.append(beat_dict)
            except Exception as e:
                print(
                    f"❌ [PERSISTENCE] Failed to convert beat {i} ({beat.letter}): {e}"
                )
                import traceback

                traceback.print_exc()

        return legacy_beats

    def _create_sequence_metadata(
        self, sequence: SequenceData, word: str = ""
    ) -> dict[str, Any]:
        """
        Create metadata for the sequence.

        Args:
            sequence: The sequence to create metadata for
            word: Pre-calculated word

        Returns:
            Metadata dictionary
        """
        return {
            "word": word,
            "author": "modern",
            "level": 0,
            "prop_type": "staff",
            "grid_mode": "diamond",
        }

    def load_current_sequence(self) -> list[dict[str, Any]]:
        """
        Load the current sequence from persistence.

        Returns:
            Raw legacy sequence data
        """
        return self.persister.load_current_sequence()

    def preserve_start_position_from_existing(
        self, existing_sequence: list[dict[str, Any]]
    ) -> Optional[dict[str, Any]]:
        """
        Extract start position from existing sequence if present.

        Args:
            existing_sequence: The existing sequence data

        Returns:
            Start position data if found, None otherwise
        """
        if len(existing_sequence) > 1 and existing_sequence[1].get("beat") == 0:
            return existing_sequence[1]
        return None
