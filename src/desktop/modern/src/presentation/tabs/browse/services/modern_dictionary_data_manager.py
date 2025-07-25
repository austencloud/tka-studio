"""
Modern Dictionary Data Manager - Real Data Loading

This module provides real dictionary data loading functionality for the modern browse tab,
based on the legacy dictionary data manager architecture.
"""

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image
from PyQt6.QtCore import QObject, pyqtSignal


@dataclass
class SequenceRecord:
    """Represents a sequence record with all metadata."""

    word: str
    thumbnails: List[str]
    author: Optional[str] = None
    level: Optional[int] = None
    sequence_length: Optional[int] = None
    date_added: Optional[datetime] = None
    grid_mode: Optional[str] = None
    prop_type: Optional[str] = None
    is_favorite: bool = False
    is_circular: bool = False
    starting_position: Optional[str] = None
    difficulty_level: Optional[str] = None
    tags: List[str] = field(default_factory=list)


class ModernDictionaryDataManager(QObject):
    """
    Modern dictionary data manager that loads real sequence data from the dictionary folder.

    Provides the same functionality as the legacy DictionaryDataManager but with modern
    architecture and improved error handling.
    """

    # Signals
    data_loaded = pyqtSignal(int)  # Emitted when data is loaded with count
    loading_progress = pyqtSignal(str, int, int)  # message, current, total

    def __init__(self, data_directory: Optional[Path] = None):
        super().__init__()
        self.data_directory = data_directory or self._find_data_directory()
        self.dictionary_dir = self.data_directory / "dictionary"
        self._loaded_records: List[SequenceRecord] = []
        self._has_loaded = False
        self._loading_errors: List[str] = []

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
            return

        # Get all sequence directories
        sequence_dirs = [
            d
            for d in self.dictionary_dir.iterdir()
            if d.is_dir() and d.name != "__pycache__"
        ]

        total_dirs = len(sequence_dirs)

        for i, sequence_dir in enumerate(sequence_dirs):
            try:

                # Find thumbnails in this directory
                thumbnails = self._find_thumbnails(sequence_dir)

                if not thumbnails:
                    continue

                # Create sequence record
                record = SequenceRecord(word=sequence_dir.name, thumbnails=thumbnails)

                # Extract metadata from the first thumbnail
                metadata = self._extract_metadata_from_thumbnail(thumbnails[0])
                if metadata:
                    record.author = metadata.get("author")
                    record.level = metadata.get("level")
                    record.sequence_length = metadata.get("sequence_length")
                    record.date_added = metadata.get("date_added")
                    record.grid_mode = metadata.get("grid_mode", "diamond")
                    record.prop_type = metadata.get("prop_type")
                    record.is_favorite = metadata.get("is_favorite", False)
                    record.is_circular = metadata.get("is_circular", False)
                    record.starting_position = metadata.get("starting_position")
                    record.difficulty_level = self._map_level_to_difficulty(
                        record.level
                    )
                    record.tags = metadata.get("tags", [])

                # If no sequence length from metadata, use word length as fallback
                if record.sequence_length is None:
                    record.sequence_length = len(record.word)

                self._loaded_records.append(record)

            except Exception as e:
                error_msg = f"Error loading {sequence_dir.name}: {e}"
                self._loading_errors.append(error_msg)

        self._has_loaded = True
        loaded_count = len(self._loaded_records)

        self.data_loaded.emit(loaded_count)

    def _find_thumbnails(self, sequence_dir: Path) -> List[str]:
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
    ) -> Optional[Dict[str, Any]]:
        """Extract metadata from a thumbnail image."""
        try:
            with Image.open(thumbnail_path) as img:
                metadata_json = img.info.get("metadata")
                if not metadata_json:
                    return None

                metadata = json.loads(metadata_json)

                # Extract metadata from the sequence structure
                if "sequence" in metadata and metadata["sequence"]:
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
        except Exception as e:
            pass  # Error extracting metadata

        return None

    def _map_level_to_difficulty(self, level: Optional[int]) -> Optional[str]:
        """Map numeric level to difficulty string."""
        if level is None:
            return None
        if level <= 1:
            return "beginner"
        elif level <= 3:
            return "intermediate"
        else:
            return "advanced"

    # Query methods for filtering

    def get_all_records(self) -> List[SequenceRecord]:
        """Get all sequence records."""
        self.load_all_sequences()
        return self._loaded_records.copy()

    def get_records_by_starting_letter(self, letter: str) -> List[SequenceRecord]:
        """Get sequences starting with the specified letter."""
        self.load_all_sequences()
        return [
            r for r in self._loaded_records if r.word.upper().startswith(letter.upper())
        ]

    def get_records_by_starting_letters(
        self, letters: List[str]
    ) -> List[SequenceRecord]:
        """Get sequences starting with any of the specified letters."""
        self.load_all_sequences()
        letter_set = {letter.upper() for letter in letters}
        return [r for r in self._loaded_records if r.word[0].upper() in letter_set]

    def get_records_by_length(self, length: int) -> List[SequenceRecord]:
        """Get sequences with the specified length."""
        self.load_all_sequences()
        return [r for r in self._loaded_records if r.sequence_length == length]

    def get_records_by_difficulty(self, difficulty: str) -> List[SequenceRecord]:
        """Get sequences with the specified difficulty level."""
        self.load_all_sequences()
        return [
            r for r in self._loaded_records if r.difficulty_level == difficulty.lower()
        ]

    def get_records_by_level(self, level: int) -> List[SequenceRecord]:
        """Get sequences with the specified numeric level."""
        self.load_all_sequences()
        return [r for r in self._loaded_records if r.level == level]

    def get_records_by_starting_position(self, position: str) -> List[SequenceRecord]:
        """Get sequences with the specified starting position."""
        self.load_all_sequences()
        return [
            r for r in self._loaded_records if r.starting_position == position.lower()
        ]

    def get_records_by_author(self, author: str) -> List[SequenceRecord]:
        """Get sequences by the specified author."""
        self.load_all_sequences()
        return [r for r in self._loaded_records if r.author == author]

    def get_records_by_grid_mode(self, grid_mode: str) -> List[SequenceRecord]:
        """Get sequences with the specified grid mode."""
        self.load_all_sequences()
        return [r for r in self._loaded_records if r.grid_mode == grid_mode.lower()]

    def get_favorite_records(self) -> List[SequenceRecord]:
        """Get all favorite sequences."""
        self.load_all_sequences()
        return [r for r in self._loaded_records if r.is_favorite]

    def get_recent_records(self, limit: int = 20) -> List[SequenceRecord]:
        """Get the most recently added sequences."""
        self.load_all_sequences()

        # Filter records with valid dates and sort by date
        dated_records = [r for r in self._loaded_records if r.date_added is not None]
        dated_records.sort(key=lambda x: x.date_added, reverse=True)

        return dated_records[:limit]

    def get_records_containing_letters(
        self, letters: List[str]
    ) -> List[SequenceRecord]:
        """Get sequences containing any of the specified letters."""
        self.load_all_sequences()
        letter_set = {letter.upper() for letter in letters}
        return [
            r
            for r in self._loaded_records
            if any(char.upper() in letter_set for char in r.word)
        ]

    # Utility methods

    def get_distinct_authors(self) -> List[str]:
        """Get list of all unique authors."""
        self.load_all_sequences()
        authors = {r.author for r in self._loaded_records if r.author}
        return sorted(authors)

    def get_distinct_levels(self) -> List[int]:
        """Get list of all unique levels."""
        self.load_all_sequences()
        levels = {r.level for r in self._loaded_records if r.level is not None}
        return sorted(levels)

    def get_distinct_lengths(self) -> List[int]:
        """Get list of all unique sequence lengths."""
        self.load_all_sequences()
        lengths = {
            r.sequence_length
            for r in self._loaded_records
            if r.sequence_length is not None
        }
        return sorted(lengths)

    def get_distinct_starting_positions(self) -> List[str]:
        """Get list of all unique starting positions."""
        self.load_all_sequences()
        positions = {
            r.starting_position for r in self._loaded_records if r.starting_position
        }
        return sorted(positions)

    def get_distinct_grid_modes(self) -> List[str]:
        """Get list of all unique grid modes."""
        self.load_all_sequences()
        modes = {r.grid_mode for r in self._loaded_records if r.grid_mode}
        return sorted(modes)

    def get_sequence_count(self) -> int:
        """Get total number of loaded sequences."""
        return len(self._loaded_records)

    def get_loading_errors(self) -> List[str]:
        """Get list of errors that occurred during loading."""
        return self._loading_errors.copy()

    def refresh_data(self) -> None:
        """Refresh the data by reloading from disk."""
        self._loaded_records.clear()
        self._loading_errors.clear()
        self._has_loaded = False
        self.load_all_sequences()
