"""
Browse Service Implementation

Handles data loading and filtering for the browse tab.
Simple service that mirrors the complexity found in legacy BrowseTabFilterManager.
"""

from pathlib import Path
from typing import Any, List, Optional, Tuple

from domain.models.sequence_data import SequenceData
from presentation.tabs.browse.models import FilterType, SortMethod


class BrowseService:
    """
    Handles data loading and filtering - mirrors legacy BrowseTabFilterManager complexity.

    Based on audit findings that legacy filtering is mostly basic list comprehensions
    and data access rather than complex algorithms.
    """

    def __init__(self, sequences_dir: Path):
        """Initialize with sequence directory path."""
        self.sequences_dir = sequences_dir
        self._cached_sequences: Optional[List[SequenceData]] = None

    def load_sequences(self) -> List[SequenceData]:
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
    ) -> List[SequenceData]:
        """
        Apply filter to sequences - mirrors legacy filter logic.

        Args:
            filter_type: Type of filter to apply
            filter_value: Value to filter by

        Returns:
            Filtered list of sequences
        """
        sequences = self.load_sequences()

        if filter_type == FilterType.ALL_SEQUENCES:
            return sequences
        elif filter_type == FilterType.STARTING_LETTER:
            if filter_value is None:
                # Return all sequences when no specific letter is chosen
                return sequences
            return [
                s
                for s in sequences
                if s.word and s.word[0].upper() == filter_value.upper()
            ]
        elif filter_type == FilterType.CONTAINS_LETTERS:
            if filter_value is None:
                return sequences
            return [s for s in sequences if filter_value.lower() in s.word.lower()]
        elif filter_type == FilterType.SEQUENCE_LENGTH:
            if filter_value is None:
                return sequences
            return [s for s in sequences if s.sequence_length == filter_value]
        elif filter_type == FilterType.DIFFICULTY_LEVEL:
            if filter_value is None:
                return sequences
            return [s for s in sequences if s.difficulty_level == filter_value]
        elif filter_type == FilterType.STARTING_POSITION:
            if filter_value is None:
                return sequences
            return [
                s for s in sequences if self._matches_starting_position(s, filter_value)
            ]
        elif filter_type == FilterType.AUTHOR:
            if filter_value is None:
                return sequences
            return [s for s in sequences if s.author == filter_value]
        elif filter_type == FilterType.GRID_MODE:
            if filter_value is None:
                return sequences
            return [s for s in sequences if self._matches_grid_mode(s, filter_value)]
        elif filter_type == FilterType.FAVORITES:
            # For now, return all sequences as favorites
            return sequences
        elif filter_type == FilterType.MOST_RECENT:
            # For now, return all sequences as most recent
            return sequences
        else:
            return sequences

    def sort_sequences(
        self, sequences: List[SequenceData], sort_method: SortMethod
    ) -> List[SequenceData]:
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
        elif sort_method == SortMethod.DATE_ADDED:
            return sorted(sequences, key=lambda s: s.date_added, reverse=True)
        elif sort_method == SortMethod.DIFFICULTY_LEVEL:
            return sorted(sequences, key=lambda s: s.difficulty_level)
        elif sort_method == SortMethod.SEQUENCE_LENGTH:
            return sorted(sequences, key=lambda s: s.sequence_length)
        elif sort_method == SortMethod.AUTHOR:
            return sorted(sequences, key=lambda s: s.author.lower())
        elif sort_method == SortMethod.POPULARITY:
            # Could be based on usage count or favorites
            return sorted(sequences, key=lambda s: s.is_favorite, reverse=True)
        else:
            return sequences

    def get_sequence_metadata(self, sequence_id: str) -> Optional[SequenceData]:
        """
        Get detailed metadata for a specific sequence.

        Args:
            sequence_id: ID of the sequence to get metadata for

        Returns:
            SequenceData object or None if not found
        """
        sequences = self.load_sequences()
        for sequence in sequences:
            if sequence.id == sequence_id:
                return sequence
        return None

    def get_filter_options(self, filter_type: FilterType) -> List[Any]:
        """
        Get available options for a specific filter type.

        Args:
            filter_type: Type of filter to get options for

        Returns:
            List of available filter values
        """
        sequences = self.load_sequences()

        if filter_type == FilterType.STARTING_LETTER:
            letters = set()
            for seq in sequences:
                if seq.word:
                    letters.add(seq.word[0].upper())
            return sorted(list(letters))
        elif filter_type == FilterType.SEQUENCE_LENGTH:
            lengths = set(seq.sequence_length for seq in sequences)
            return sorted(list(lengths))
        elif filter_type == FilterType.DIFFICULTY_LEVEL:
            levels = set(
                seq.difficulty_level for seq in sequences if seq.difficulty_level
            )
            return sorted(list(levels))
        elif filter_type == FilterType.AUTHOR:
            authors = set(seq.author for seq in sequences if seq.author)
            return sorted(list(authors))
        else:
            return []

    def _load_sequence_from_folder(self, folder_path: Path) -> Optional[SequenceData]:
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
            with open(json_file, "r") as f:
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

    def _create_test_sequences(self) -> List[SequenceData]:
        """Create test sequences for demo purposes."""
        test_sequences = []

        # Sample sequence data for testing
        sample_data = [
            ("ALPHA", 3, "beginner", "Demo Author", True),
            ("BETA", 5, "intermediate", "Demo Author", False),
            ("GAMMA", 4, "beginner", "Test User", True),
            ("DELTA", 6, "advanced", "Demo Author", False),
            ("EPSILON", 3, "intermediate", "Test User", False),
            ("ZETA", 7, "advanced", "Expert User", True),
            ("ETA", 4, "beginner", "Demo Author", False),
            ("THETA", 5, "intermediate", "Test User", True),
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
                metadata={"created_by": "test_data_generator"},
            )
            test_sequences.append(sequence)

        return test_sequences
