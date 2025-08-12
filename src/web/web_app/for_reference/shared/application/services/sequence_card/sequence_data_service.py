"""
Sequence Card Data Service Implementation

Handles file system operations, metadata extraction, and data validation.
"""

import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

from desktop.modern.core.interfaces.sequence_card_services import (
    ISequenceCardDataService,
    SequenceCardData,
)

logger = logging.getLogger(__name__)


class SequenceCardDataService(ISequenceCardDataService):
    """Implementation of sequence card data operations."""

    def __init__(self):
        self._file_watchers = {}
        # Use modern metadata extraction service
        from .metadata_extraction_service import SequenceMetadataExtractionService

        self.metadata_extractor = SequenceMetadataExtractionService()

    def get_sequences_by_length(
        self, base_path: Path, length: int
    ) -> list[SequenceCardData]:
        """Get all sequences of specified length."""
        try:
            sequences = self.get_all_sequences(base_path)
            if length <= 0:  # "All" selection
                return sequences
            return [seq for seq in sequences if seq.length == length]
        except Exception as e:
            logger.error(f"Error getting sequences by length {length}: {e}")
            return []

    def get_all_sequences(self, base_path: Path) -> list[SequenceCardData]:
        """Get all sequences regardless of length."""
        sequences = []
        try:
            if not base_path.exists():
                logger.warning(f"Dictionary path does not exist: {base_path}")
                return []

            # Scan dictionary directory structure
            for word_dir in base_path.iterdir():
                if not word_dir.is_dir() or word_dir.name.startswith("__"):
                    continue

                word = word_dir.name
                for image_file in word_dir.glob("*.png"):
                    try:
                        metadata = self.extract_metadata(image_file)
                        sequence_data = SequenceCardData(
                            path=image_file,
                            word=word,
                            length=metadata.get("sequence_length", 0),
                            metadata=metadata,
                            is_favorite=metadata.get("is_favorite", False),
                            tags=metadata.get("tags", []),
                        )
                        sequences.append(sequence_data)
                    except Exception as e:
                        logger.warning(f"Error processing {image_file}: {e}")
                        continue

        except Exception as e:
            logger.error(f"Error scanning sequences from {base_path}: {e}")

        return sequences

    def extract_metadata(self, image_path: Path) -> dict[str, Any]:
        """Extract metadata from sequence image."""
        try:
            return self.metadata_extractor.extract_metadata_from_image(str(image_path))
        except Exception as e:
            logger.warning(f"Error extracting metadata from {image_path}: {e}")
            return {"sequence_length": 0, "is_favorite": False, "tags": []}

    def watch_directory_changes(
        self, path: Path, callback: Callable[[Path], None]
    ) -> None:
        """Watch for directory changes."""
        # Implementation would use QFileSystemWatcher or similar
        # For now, just store the callback for potential future use
        self._file_watchers[str(path)] = callback
        logger.info(f"Directory watcher registered for {path}")

    def validate_sequence_data(self, data: SequenceCardData) -> tuple[bool, list[str]]:
        """Validate sequence data."""
        errors = []

        if not data.path.exists():
            errors.append(f"Image file does not exist: {data.path}")

        if not data.word:
            errors.append("Word is required")

        if data.length <= 0:
            errors.append("Sequence length must be positive")

        return len(errors) == 0, errors
