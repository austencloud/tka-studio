"""
Modern Metadata Extraction Service for Sequence Cards

Extracts metadata from sequence image files without legacy dependencies.
Replaces the legacy MetaDataExtractor with a clean, modern implementation.
"""

import json
import logging
from pathlib import Path
from typing import Any, Optional

from PIL import Image, PngImagePlugin

logger = logging.getLogger(__name__)


class SequenceMetadataExtractionService:
    """Modern service for extracting metadata from sequence card images."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def extract_metadata_from_image(self, image_path: str) -> dict[str, Any]:
        """
        Extract all metadata from a sequence image file.

        Args:
            image_path: Path to the sequence image file

        Returns:
            Dictionary containing extracted metadata
        """
        if not image_path or not Path(image_path).exists():
            return self._get_default_metadata()

        try:
            with Image.open(image_path) as img:
                metadata_json = img.info.get("metadata")
                if metadata_json:
                    raw_metadata = json.loads(metadata_json)
                    return self._process_raw_metadata(raw_metadata, image_path)
                else:
                    self.logger.debug(f"No metadata found in image: {image_path}")
                    return self._extract_fallback_metadata(image_path)

        except Exception as e:
            self.logger.warning(f"Error extracting metadata from {image_path}: {e}")
            return self._extract_fallback_metadata(image_path)

    def _process_raw_metadata(
        self, raw_metadata: dict[str, Any], image_path: str
    ) -> dict[str, Any]:
        """Process raw metadata into standardized format."""
        processed = {
            "sequence_length": self._extract_sequence_length(raw_metadata),
            "is_favorite": raw_metadata.get("is_favorite", False),
            "tags": raw_metadata.get("tags", []),
            "level": self._extract_level(raw_metadata),
            "start_position": self._extract_start_position(raw_metadata),
            "grid_mode": self._extract_grid_mode(raw_metadata),
            "word": self._extract_word_from_path(image_path),
            "full_sequence": raw_metadata.get("sequence", []),
            "raw_metadata": raw_metadata,  # Keep original for advanced use cases
        }

        return processed

    def _extract_sequence_length(self, metadata: dict[str, Any]) -> int:
        """Extract sequence length from metadata."""
        if "sequence" in metadata and isinstance(metadata["sequence"], list):
            # Sequence length is total beats minus start/end positions
            return max(0, len(metadata["sequence"]) - 2)
        return 0

    def _extract_level(self, metadata: dict[str, Any]) -> Optional[int]:
        """Extract difficulty level from metadata."""
        if "sequence" in metadata and isinstance(metadata["sequence"], list):
            if len(metadata["sequence"]) > 0:
                first_beat = metadata["sequence"][0]
                if isinstance(first_beat, dict):
                    return first_beat.get("level")
        return None

    def _extract_start_position(self, metadata: dict[str, Any]) -> Optional[str]:
        """Extract start position (alpha, beta, gamma) from metadata."""
        if "sequence" in metadata and isinstance(metadata["sequence"], list):
            if len(metadata["sequence"]) > 1:
                start_pos_entry = metadata["sequence"][1]
                if isinstance(start_pos_entry, dict):
                    # Try sequence_start_position first
                    if "sequence_start_position" in start_pos_entry:
                        return start_pos_entry["sequence_start_position"]

                    # Fallback to deriving from end_pos
                    if "end_pos" in start_pos_entry:
                        end_pos = start_pos_entry["end_pos"]
                        if isinstance(end_pos, str):
                            for pos in ["alpha", "beta", "gamma"]:
                                if end_pos.startswith(pos):
                                    return pos
        return None

    def _extract_grid_mode(self, metadata: dict[str, Any]) -> str:
        """Extract grid mode from metadata."""
        if "sequence" in metadata and isinstance(metadata["sequence"], list):
            if len(metadata["sequence"]) > 0:
                first_beat = metadata["sequence"][0]
                if isinstance(first_beat, dict):
                    return first_beat.get("grid_mode", "diamond")
        return "diamond"  # Default

    def _extract_word_from_path(self, image_path: str) -> str:
        """Extract word from image file path."""
        path = Path(image_path)
        # Word is typically the parent directory name
        return path.parent.name if path.parent.name != "." else path.stem

    def _extract_fallback_metadata(self, image_path: str) -> dict[str, Any]:
        """Extract metadata using filename patterns when no embedded metadata exists."""
        path = Path(image_path)
        filename = path.stem
        word = self._extract_word_from_path(image_path)

        # Try to extract length from filename patterns
        sequence_length = self._extract_length_from_filename(filename)

        return {
            "sequence_length": sequence_length,
            "is_favorite": False,
            "tags": [],
            "level": None,
            "start_position": None,
            "grid_mode": "diamond",
            "word": word,
            "full_sequence": [],
            "raw_metadata": {},
        }

    def _extract_length_from_filename(self, filename: str) -> int:
        """Extract sequence length from filename patterns."""
        # Common patterns: word_16.png, word_length_8.png, etc.
        # Check in reverse order (largest to smallest) to avoid partial matches
        for length in [16, 12, 10, 8, 6, 5, 4, 3, 2]:
            if (
                f"_{length}_" in filename
                or f"length_{length}" in filename
                or filename.endswith(f"_{length}")
            ):
                return length
        return 16  # Default fallback

    def _get_default_metadata(self) -> dict[str, Any]:
        """Get default metadata structure."""
        return {
            "sequence_length": 0,
            "is_favorite": False,
            "tags": [],
            "level": None,
            "start_position": None,
            "grid_mode": "diamond",
            "word": "",
            "full_sequence": [],
            "raw_metadata": {},
        }

    def get_sequence_length(self, image_path: str) -> int:
        """Get just the sequence length from an image."""
        metadata = self.extract_metadata_from_image(image_path)
        return metadata.get("sequence_length", 0)

    def get_tags(self, image_path: str) -> list[str]:
        """Get tags from an image."""
        metadata = self.extract_metadata_from_image(image_path)
        return metadata.get("tags", [])

    def get_favorite_status(self, image_path: str) -> bool:
        """Get favorite status from an image."""
        metadata = self.extract_metadata_from_image(image_path)
        return metadata.get("is_favorite", False)

    def get_level(self, image_path: str) -> Optional[int]:
        """Get difficulty level from an image."""
        metadata = self.extract_metadata_from_image(image_path)
        return metadata.get("level")

    def get_start_position(self, image_path: str) -> Optional[str]:
        """Get start position from an image."""
        metadata = self.extract_metadata_from_image(image_path)
        return metadata.get("start_position")

    def set_tags(self, image_path: str, tags: list[str]) -> bool:
        """
        Set tags in image metadata.

        Args:
            image_path: Path to the image file
            tags: List of tags to set

        Returns:
            True if successful, False otherwise
        """
        try:
            with Image.open(image_path) as img:
                # Get existing metadata or create new
                existing_metadata = self.extract_metadata_from_image(image_path)
                raw_metadata = existing_metadata.get("raw_metadata", {})

                # Update tags
                raw_metadata["tags"] = tags

                # Save back to image
                pnginfo = PngImagePlugin.PngInfo()
                pnginfo.add_text("metadata", json.dumps(raw_metadata))
                img.save(image_path, pnginfo=pnginfo)

                return True

        except Exception as e:
            self.logger.error(f"Error saving tags to {image_path}: {e}")
            return False

    def set_favorite_status(self, image_path: str, is_favorite: bool) -> bool:
        """
        Set favorite status in image metadata.

        Args:
            image_path: Path to the image file
            is_favorite: Favorite status to set

        Returns:
            True if successful, False otherwise
        """
        try:
            with Image.open(image_path) as img:
                # Get existing metadata or create new
                existing_metadata = self.extract_metadata_from_image(image_path)
                raw_metadata = existing_metadata.get("raw_metadata", {})

                # Update favorite status
                raw_metadata["is_favorite"] = is_favorite

                # Save back to image
                pnginfo = PngImagePlugin.PngInfo()
                pnginfo.add_text("metadata", json.dumps(raw_metadata))
                img.save(image_path, pnginfo=pnginfo)

                return True

        except Exception as e:
            self.logger.error(f"Error saving favorite status to {image_path}: {e}")
            return False
