"""
Modern Dictionary Data Manager - Consolidated Data Model

This module provides real dictionary data loading functionality for the modern browse tab.
Simplified to use SequenceData directly instead of separate SequenceRecord.
"""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
from typing import Any

from PIL import Image
from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.domain.models.browse_errors import DataLoadError
from desktop.modern.domain.models.sequence_data import SequenceData


class DictionaryDataManager(QObject):
    """
    Modern dictionary data manager that loads real sequence data from the dictionary folder.

    Simplified to use SequenceData directly throughout, eliminating conversion overhead.
    """

    # Signals
    data_loaded = pyqtSignal(int)  # Emitted when data is loaded with count
    loading_progress = pyqtSignal(str, int, int)  # message, current, total

    def __init__(self, data_directory: Path | None = None):
        super().__init__()
        self.data_directory = data_directory or self._find_data_directory()
        self.dictionary_dir = self.data_directory / "dictionary"
        self._loaded_sequences: list[SequenceData] = []
        self._has_loaded = False
        self._loading_errors: list[str] = []

    def _find_data_directory(self) -> Path:
        """Find the data directory using the same logic as legacy."""
        # Start from current file and search upward
        current_path = Path(__file__).resolve().parent

        while current_path.parent != current_path:
            # Check if this is the TKA root
            if current_path.name == "TKA":
                data_dir = current_path / "data"
                if data_dir.exists():
                    return data_dir

            # Check for data directory at current level
            data_dir = current_path / "data"
            if data_dir.exists() and (data_dir / "dictionary").exists():
                return data_dir

            current_path = current_path.parent

        # Fallback to current working directory
        return Path.cwd() / "data"

    def load_all_sequences(self) -> None:
        """Load all sequences from the dictionary folder."""
        if self._has_loaded:
            return

        if not self.dictionary_dir.exists():
            raise DataLoadError(
                f"Dictionary directory not found: {self.dictionary_dir}"
            )

        # Get all sequence directories
        sequence_dirs = [
            d
            for d in self.dictionary_dir.iterdir()
            if d.is_dir() and d.name != "__pycache__"
        ]

        total_dirs = len(sequence_dirs)

        for i, sequence_dir in enumerate(sequence_dirs):
            try:
                # Emit progress
                self.loading_progress.emit(
                    f"Loading {sequence_dir.name}...", i, total_dirs
                )

                # Find thumbnails in this directory
                thumbnails = self._find_thumbnails(sequence_dir)

                if not thumbnails:
                    continue

                # Extract metadata from the first thumbnail
                metadata = self._extract_metadata_from_thumbnail(thumbnails[0])

                # Create SequenceData directly with deterministic ID based on word + thumbnail paths
                # This ensures the same sequence always has the same ID across loads
                deterministic_id = self._generate_deterministic_id(
                    sequence_dir.name, thumbnails
                )

                sequence_data = SequenceData(
                    id=deterministic_id,
                    word=sequence_dir.name,
                    thumbnails=thumbnails,
                    author=metadata.get("author") if metadata else None,
                    level=metadata.get("level") if metadata else None,
                    sequence_length=(
                        metadata.get("sequence_length")
                        if metadata
                        else len(sequence_dir.name)
                    ),
                    date_added=metadata.get("date_added") if metadata else None,
                    grid_mode=(
                        metadata.get("grid_mode", "diamond") if metadata else "diamond"
                    ),
                    prop_type=metadata.get("prop_type") if metadata else None,
                    is_favorite=(
                        metadata.get("is_favorite", False) if metadata else False
                    ),
                    is_circular=(
                        metadata.get("is_circular", False) if metadata else False
                    ),
                    starting_position=(
                        metadata.get("starting_position") if metadata else None
                    ),
                    difficulty_level=self._map_level_to_difficulty(
                        metadata.get("level") if metadata else None
                    ),
                    tags=metadata.get("tags", []) if metadata else [],
                )

                self._loaded_sequences.append(sequence_data)

            except Exception as e:
                error_msg = f"Error loading {sequence_dir.name}: {e}"
                self._loading_errors.append(error_msg)

        self._has_loaded = True
        loaded_count = len(self._loaded_sequences)

        self.data_loaded.emit(loaded_count)

    def _find_thumbnails(self, sequence_dir: Path) -> list[str]:
        """Find all thumbnail files in a sequence directory."""
        thumbnails = []

        for file_path in sequence_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in [
                ".png",
                ".jpg",
                ".jpeg",
            ]:
                thumbnails.append(str(file_path))

        return sorted(thumbnails)

    def _extract_metadata_from_thumbnail(
        self, thumbnail_path: str
    ) -> dict[str, Any] | None:
        """Extract metadata from a thumbnail image."""
        try:
            with Image.open(thumbnail_path) as img:
                metadata_json = img.info.get("metadata")
                if not metadata_json:
                    return None

                metadata = json.loads(metadata_json)

                # Extract metadata from the sequence structure
                if metadata.get("sequence"):
                    first_entry = metadata["sequence"][0]

                    result = {
                        "author": first_entry.get("author"),
                        "level": first_entry.get("level"),
                        "grid_mode": first_entry.get("grid_mode", "diamond"),
                        "prop_type": first_entry.get("prop_type"),
                        "is_favorite": first_entry.get("is_favorite", False),
                        "is_circular": first_entry.get("is_circular", False),
                        "starting_position": first_entry.get("sequence_start_position"),
                        "word": first_entry.get("word"),
                        "sequence_length": len(metadata["sequence"])
                        - 2,  # Exclude metadata entries
                        "tags": metadata.get("tags", []),
                    }

                    # Handle date_added
                    date_str = first_entry.get("date_added")
                    if date_str:
                        try:
                            result["date_added"] = datetime.fromisoformat(date_str)
                        except ValueError:
                            result["date_added"] = None

                    return result

        except FileNotFoundError:
            pass  # Thumbnail not found
        except Exception:
            pass  # Error extracting metadata

        return None

    def _generate_deterministic_id(self, word: str, thumbnails: list[str]) -> str:
        """
        Generate a deterministic ID based on word and thumbnail paths.

        This ensures the same sequence always has the same ID across loads,
        following the pattern used in the legacy system where sequences are
        identified by word + thumbnail paths rather than random UUIDs.

        Args:
            word: The sequence word (directory name)
            thumbnails: List of thumbnail file paths

        Returns:
            A deterministic string ID that uniquely identifies this sequence
        """
        import hashlib

        # Create a stable identifier using word + sorted thumbnail paths
        # Sort thumbnail paths to ensure consistent ordering
        sorted_thumbnails = sorted(thumbnails)

        # Create a string combining word and thumbnail paths
        identifier_parts = [word] + sorted_thumbnails
        identifier_string = "|".join(identifier_parts)

        # Generate a hash to create a shorter, deterministic ID
        hash_object = hashlib.sha256(identifier_string.encode("utf-8"))
        deterministic_id = hash_object.hexdigest()

        return deterministic_id

    def _map_level_to_difficulty(self, level: int | None) -> str | None:
        """Map numeric level to difficulty string."""
        if level is None:
            return None
        if level <= 1:
            return "beginner"
        if level <= 3:
            return "intermediate"
        return "advanced"

    # Query methods for filtering - now return SequenceData directly

    def get_all_sequences(self) -> list[SequenceData]:
        """Get all sequence data."""
        self.load_all_sequences()
        return self._loaded_sequences.copy()

    def get_sequences_by_starting_letter(self, letter: str) -> list[SequenceData]:
        """Get sequences starting with the specified letter."""
        self.load_all_sequences()
        return [
            s
            for s in self._loaded_sequences
            if s.word and s.word.upper().startswith(letter.upper())
        ]

    def get_sequences_by_starting_letters(
        self, letters: list[str]
    ) -> list[SequenceData]:
        """Get sequences starting with any of the specified letters."""
        self.load_all_sequences()
        letter_set = {letter.upper() for letter in letters}
        return [
            s
            for s in self._loaded_sequences
            if s.word and s.word[0].upper() in letter_set
        ]

    def get_sequences_by_length(self, length: int) -> list[SequenceData]:
        """Get sequences with the specified length."""
        self.load_all_sequences()
        return [s for s in self._loaded_sequences if s.sequence_length == length]

    def get_sequences_by_difficulty(self, difficulty: str) -> list[SequenceData]:
        """Get sequences with the specified difficulty level."""
        self.load_all_sequences()
        return [
            s
            for s in self._loaded_sequences
            if s.difficulty_level == difficulty.lower()
        ]

    def get_sequences_by_level(self, level: int) -> list[SequenceData]:
        """Get sequences with the specified numeric level."""
        self.load_all_sequences()
        return [s for s in self._loaded_sequences if s.level == level]

    def get_sequences_by_starting_position(self, position: str) -> list[SequenceData]:
        """Get sequences with the specified starting position."""
        self.load_all_sequences()
        return [
            s for s in self._loaded_sequences if s.starting_position == position.lower()
        ]

    def get_sequences_by_author(self, author: str) -> list[SequenceData]:
        """Get sequences by the specified author."""
        self.load_all_sequences()
        return [s for s in self._loaded_sequences if s.author == author]

    def get_sequences_by_grid_mode(self, grid_mode: str) -> list[SequenceData]:
        """Get sequences with the specified grid mode."""
        self.load_all_sequences()
        return [s for s in self._loaded_sequences if s.grid_mode == grid_mode.lower()]

    def get_favorite_sequences(self) -> list[SequenceData]:
        """Get all favorite sequences."""
        self.load_all_sequences()
        return [s for s in self._loaded_sequences if s.is_favorite]

    def get_recent_sequences(self, limit: int = 20) -> list[SequenceData]:
        """Get the most recently added sequences."""
        self.load_all_sequences()

        # Filter sequences with valid dates and sort by date
        dated_sequences = [
            s for s in self._loaded_sequences if s.date_added is not None
        ]
        dated_sequences.sort(key=lambda x: x.date_added, reverse=True)

        return dated_sequences[:limit]

    def get_sequences_containing_letters(
        self, letters: list[str]
    ) -> list[SequenceData]:
        """Get sequences containing any of the specified letters."""
        self.load_all_sequences()
        letter_set = {letter.upper() for letter in letters}
        return [
            s
            for s in self._loaded_sequences
            if s.word and any(char.upper() in letter_set for char in s.word)
        ]

    # Utility methods

    def get_distinct_authors(self) -> list[str]:
        """Get list of all unique authors."""
        self.load_all_sequences()
        authors = {s.author for s in self._loaded_sequences if s.author}
        return sorted(authors)

    def get_sequence_count(self) -> int:
        """Get total number of loaded sequences."""
        return len(self._loaded_sequences)

    def get_loading_errors(self) -> list[str]:
        """Get list of errors that occurred during loading."""
        return self._loading_errors.copy()

    def refresh_data(self) -> None:
        """Refresh the data by reloading from disk."""
        self._loaded_sequences.clear()
        self._loading_errors.clear()
        self._has_loaded = False
        self.load_all_sequences()
