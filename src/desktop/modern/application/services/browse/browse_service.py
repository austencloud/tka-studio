"""
Browse Service Implementation - Enhanced for Organized Filters

Handles data loading and filtering for the browse tab.
Enhanced to support organized filter structure with letter ranges,
difficulty levels, and other categorized options.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from desktop.modern.domain.models.browse_models import FilterType, SortMethod
from desktop.modern.domain.models.sequence_data import SequenceData


class BrowseService:
    """
    Enhanced browse service supporting organized filter categories.

    Now handles:
    - Letter ranges (A-D, E-H, etc.)
    - Difficulty levels with proper matching
    - Length filtering with "All" options
    - Author filtering with "All Authors" option
    """

    def __init__(self, sequences_dir: Path):
        """Initialize with sequence directory path."""
        self.sequences_dir = sequences_dir
        self._cached_sequences: list[SequenceData] | None = None

    def load_sequences(self) -> list[SequenceData]:
        """
        Load all sequences from the sequences directory.

        Returns:
            List of SequenceData objects with thumbnail paths and metadata
        """
        if self._cached_sequences is not None:
            return self._cached_sequences

        sequences = []

        # For demo purposes, create some test sequences if no real sequences exist
        sequences = self._create_test_sequences()

        # Scan sequences directory for sequence folders (if it exists)
        if self.sequences_dir.exists():
            for sequence_folder in self.sequences_dir.iterdir():
                if not sequence_folder.is_dir():
                    continue

                try:
                    sequence_data = self._load_sequence_from_folder(sequence_folder)
                    if sequence_data:
                        sequences.append(sequence_data)
                except Exception as e:
                    # Log error but continue loading other sequences
                    print(f"Error loading sequence from {sequence_folder}: {e}")
                    continue

        self._cached_sequences = sequences
        return sequences

    def apply_filter(
        self, filter_type: FilterType, filter_value: Any
    ) -> list[SequenceData]:
        """
        Apply filter to sequences - enhanced for organized filter structure.

        Args:
            filter_type: Type of filter to apply
            filter_value: Value to filter by (supports ranges, "All" options, etc.)

        Returns:
            Filtered list of sequences
        """
        sequences = self.load_sequences()

        if filter_type == FilterType.ALL_SEQUENCES:
            return sequences

        if filter_type == FilterType.STARTING_LETTER:
            return self._filter_by_starting_letter(sequences, filter_value)

        if filter_type == FilterType.CONTAINS_LETTERS:
            if filter_value is None:
                return sequences
            return [s for s in sequences if filter_value.lower() in s.word.lower()]

        if filter_type == FilterType.LENGTH:
            return self._filter_by_length(sequences, filter_value)

        if filter_type == FilterType.DIFFICULTY:
            return self._filter_by_difficulty(sequences, filter_value)

        if filter_type == FilterType.STARTING_POSITION:
            return self._filter_by_starting_position(sequences, filter_value)

        if filter_type == FilterType.AUTHOR:
            return self._filter_by_author(sequences, filter_value)

        if filter_type == FilterType.GRID_MODE:
            return self._filter_by_grid_mode(sequences, filter_value)

        if filter_type == FilterType.FAVORITES:
            # Return sequences marked as favorites
            return [s for s in sequences if s.is_favorite]

        if filter_type == FilterType.RECENT:
            # Sort by date and return recent sequences (for demo, return all)
            return sorted(sequences, key=lambda s: s.date_added, reverse=True)

        return sequences

    def _filter_by_starting_letter(
        self, sequences: list[SequenceData], filter_value: Any
    ) -> list[SequenceData]:
        """Filter by starting letter, supporting ranges like A-D."""
        if filter_value is None or filter_value == "All Letters":
            return sequences

        if "-" in str(filter_value):  # Handle ranges like "A-D"
            start_letter, end_letter = filter_value.split("-")
            return [
                s
                for s in sequences
                if s.word and start_letter <= s.word[0].upper() <= end_letter
            ]

        # Handle single letters
        return [
            s for s in sequences if s.word and s.word[0].upper() == filter_value.upper()
        ]

    def _filter_by_length(
        self, sequences: list[SequenceData], filter_value: Any
    ) -> list[SequenceData]:
        """Filter by sequence length, supporting 'All' option."""
        if filter_value is None or filter_value == "All":
            return sequences

        try:
            target_length = int(filter_value)
            return [s for s in sequences if s.sequence_length == target_length]
        except (ValueError, TypeError):
            return sequences

    def _filter_by_difficulty(
        self, sequences: list[SequenceData], filter_value: Any
    ) -> list[SequenceData]:
        """Filter by difficulty level, supporting 'All Levels' option."""
        if (
            filter_value is None
            or filter_value == "all"
            or filter_value == "All Levels"
        ):
            return sequences

        return [s for s in sequences if s.difficulty_level == filter_value]

    def _filter_by_starting_position(
        self, sequences: list[SequenceData], filter_value: Any
    ) -> list[SequenceData]:
        """Filter by starting position, supporting 'All Positions' option."""
        if filter_value is None or filter_value == "All Positions":
            return sequences

        return [
            s for s in sequences if self._matches_starting_position(s, filter_value)
        ]

    def _filter_by_author(
        self, sequences: list[SequenceData], filter_value: Any
    ) -> list[SequenceData]:
        """Filter by author, supporting 'All Authors' option."""
        if filter_value is None or filter_value == "All Authors":
            return sequences

        return [s for s in sequences if s.author == filter_value]

    def _filter_by_grid_mode(
        self, sequences: list[SequenceData], filter_value: Any
    ) -> list[SequenceData]:
        """Filter by grid mode, supporting 'All Styles' option."""
        if (
            filter_value is None
            or filter_value == "all"
            or filter_value == "All Styles"
        ):
            return sequences

        return [s for s in sequences if self._matches_grid_mode(s, filter_value)]

    def sort_sequences(
        self, sequences: list[SequenceData], sort_method: SortMethod
    ) -> list[SequenceData]:
        """
        Sort sequences according to the specified method.

        Args:
            sequences: List of sequences to sort
            sort_method: Method to sort by

        Returns:
            Sorted list of sequences
        """
        if sort_method == SortMethod.ALPHABETICAL:
            return sorted(sequences, key=lambda s: s.word.lower())
        if sort_method == SortMethod.DATE_ADDED:
            return sorted(sequences, key=lambda s: s.date_added, reverse=True)
        if sort_method == SortMethod.DIFFICULTY_LEVEL:
            return sorted(sequences, key=lambda s: s.difficulty_level)
        if sort_method == SortMethod.SEQUENCE_LENGTH:
            return sorted(sequences, key=lambda s: s.sequence_length)
        if sort_method == SortMethod.AUTHOR:
            return sorted(sequences, key=lambda s: s.author.lower())
        if sort_method == SortMethod.POPULARITY:
            # Could be based on usage count or favorites
            return sorted(sequences, key=lambda s: s.is_favorite, reverse=True)
        return sequences

    def _load_sequence_from_folder(self, folder_path: Path) -> SequenceData | None:
        """
        Load a single sequence from its folder.

        Args:
            folder_path: Path to the sequence folder

        Returns:
            SequenceData object or None if loading failed
        """
        # Look for sequence.json file
        json_file = folder_path / "sequence.json"
        if not json_file.exists():
            return None

        try:
            # Load sequence data from JSON
            with open(json_file) as f:
                import json

                data = json.load(f)

            # Create SequenceData from the loaded data
            sequence = SequenceData.from_dict(data)

            # Find thumbnail files in the folder
            thumbnail_paths = []
            for ext in [".png", ".jpg", ".jpeg"]:
                for thumb_file in folder_path.glob(f"*{ext}"):
                    thumbnail_paths.append(str(thumb_file))

            # Update sequence with thumbnail paths
            sequence = sequence.update(thumbnail_paths=thumbnail_paths)

            return sequence

        except Exception as e:
            print(f"Error loading sequence from {json_file}: {e}")
            return None

    def _matches_starting_position(
        self, sequence: SequenceData, position_filter: Any
    ) -> bool:
        """Check if sequence matches starting position filter."""
        # This would check the start_position beat data
        if not sequence.start_position:
            return False
        # Implementation depends on how positions are represented
        return True  # Placeholder

    def _matches_grid_mode(self, sequence: SequenceData, grid_mode: Any) -> bool:
        """Check if sequence matches grid mode filter."""
        # This would check sequence metadata for grid mode
        return sequence.metadata.get("grid_mode") == grid_mode

    def clear_cache(self):
        """Clear the cached sequences to force reload."""
        self._cached_sequences = None

    def _create_test_sequences(self) -> list[SequenceData]:
        """Create enhanced test sequences for demo purposes."""
        test_sequences = []

        # Sample sequence data for testing organized filters
        sample_data = [
            ("ALPHA", 3, "beginner", "Demo Author", True),
            ("BETA", 5, "intermediate", "Demo Author", False),
            ("GAMMA", 4, "beginner", "Test User", True),
            ("DELTA", 6, "advanced", "Demo Author", False),
            ("EPSILON", 3, "intermediate", "Test User", False),
            ("ZETA", 8, "advanced", "Expert User", True),
            ("ETA", 4, "beginner", "Demo Author", False),
            ("THETA", 10, "intermediate", "Test User", True),
            ("IOTA", 12, "advanced", "Expert User", False),
            ("KAPPA", 5, "beginner", "Demo Author", True),
            ("LAMBDA", 6, "intermediate", "Test User", False),
            ("MU", 8, "advanced", "Expert User", True),
            ("NU", 3, "beginner", "Demo Author", False),
            ("XI", 16, "advanced", "Expert User", True),
            ("OMICRON", 4, "intermediate", "Test User", False),
        ]

        for i, (word, length, difficulty, author, is_favorite) in enumerate(
            sample_data
        ):
            sequence = SequenceData(
                id=f"test_seq_{i}",
                name=f"Test Sequence {word}",
                word=word,
                beats=[],  # Empty for now
                start_position=None,
                thumbnail_paths=[],  # No actual thumbnails for test data
                sequence_length=length,
                author=author,
                difficulty_level=difficulty,
                date_added="2024-01-01",
                is_favorite=is_favorite,
                metadata={"created_by": "test_data_generator", "grid_mode": "diamond"},
            )
            test_sequences.append(sequence)

        return test_sequences
