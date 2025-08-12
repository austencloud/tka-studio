"""
Sequence Sorter Service

Service for sorting sequences and grouping them into sections.
"""

from __future__ import annotations

from datetime import datetime

from desktop.modern.core.interfaces.browse_services import ISequenceSorter
from desktop.modern.domain.models.sequence_data import SequenceData


class SequenceSorterService(ISequenceSorter):
    """Service for sorting sequences and organizing them into sections."""

    def sort_sequences(
        self, sequences: list[SequenceData], sort_method: str
    ) -> list[SequenceData]:
        """Sort sequences based on the selected method."""

        if sort_method == "alphabetical":
            result = sorted(sequences, key=lambda s: s.word.lower() if s.word else "")
        elif sort_method == "length":
            result = sorted(
                sequences, key=lambda s: s.sequence_length if s.sequence_length else 0
            )

        elif sort_method == "level":
            result = sorted(sequences, key=lambda s: s.level if s.level else 0)
        elif sort_method == "date_added":
            result = sorted(
                sequences,
                key=lambda s: s.date_added if s.date_added else datetime.min,
                reverse=True,
            )
        else:
            # Default to alphabetical
            result = sorted(sequences, key=lambda s: s.word.lower() if s.word else "")

        return result

    def group_sequences_into_sections(
        self, sequences: list[SequenceData], sort_method: str
    ) -> dict[str, list[SequenceData]]:
        """Group sequences into sections based on sort method."""
        sections = {}

        for sequence in sequences:
            section_key = self.get_section_key(sequence, sort_method)
            if section_key not in sections:
                sections[section_key] = []
            sections[section_key].append(sequence)

        return sections

    def get_section_key(self, sequence: SequenceData, sort_method: str) -> str:
        """Get the section key for a sequence based on sort method."""
        if sort_method == "alphabetical":
            return sequence.word[0].upper() if sequence.word else "?"
        if sort_method == "length":
            return (
                f"Length {sequence.sequence_length}"
                if sequence.sequence_length
                else "Unknown Length"
            )
        if sort_method == "level":
            return f"Level {sequence.level}" if sequence.level else "Unknown Level"
        if sort_method == "date_added":
            if sequence.date_added:
                return sequence.date_added.strftime("%m-%d-%Y")
            return "Unknown"
        return sequence.word[0].upper() if sequence.word else "?"

    def get_section_display_order(self, sort_method: str) -> list[str]:
        """Get the preferred display order for sections based on sort method."""
        if sort_method == "alphabetical":
            # Return alphabetical order A-Z, with special characters at end
            letters = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
            return [*letters, "?"]
        if sort_method == "length":
            # Return numerical order for lengths
            # This would need to be determined dynamically from actual data
            return []  # Let natural dict order handle this
        if sort_method == "level":
            # Return level order 1, 2, 3, etc.
            return [f"Level {i}" for i in range(1, 11)] + ["Unknown Level"]
        if sort_method == "date_added":
            # Return reverse chronological order (most recent first)
            return []  # Let natural dict order handle this
        return []
