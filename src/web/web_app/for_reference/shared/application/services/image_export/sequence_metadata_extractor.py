"""
Modern Metadata Extractor

This service extracts metadata and sequence data from sequence files,
providing the data needed for image export.
"""

import json
import logging
from pathlib import Path
from typing import Any, Optional

from desktop.modern.core.interfaces.image_export_services import (
    ISequenceMetadataExtractor,
)

logger = logging.getLogger(__name__)


class SequenceMetadataExtractor(ISequenceMetadataExtractor):
    """
    Modern implementation of metadata extractor.

    This extractor reads sequence data from files and calculates metadata
    needed for image export, including difficulty levels.
    """

    def __init__(self):
        pass

    def extract_sequence_data(self, file_path: Path) -> Optional[list[dict[str, Any]]]:
        """Extract sequence data from a file."""
        try:
            logger.debug(f"Extracting sequence data from {file_path}")

            # For PNG files, we need to look for corresponding JSON files
            if file_path.suffix.lower() == ".png":
                # Look for JSON file with same name
                json_path = file_path.with_suffix(".json")
                if json_path.exists():
                    return self._extract_from_json(json_path)

                # Look for JSON file with sequence data in the name
                # Legacy naming: word_length_16.png -> word_length_16.json
                json_path = file_path.with_suffix(".json")
                if json_path.exists():
                    return self._extract_from_json(json_path)

                # If no JSON found, return empty sequence (will be handled by caller)
                logger.warning(f"No JSON file found for {file_path}")
                return []

            elif file_path.suffix.lower() == ".json":
                return self._extract_from_json(file_path)

            else:
                logger.warning(f"Unsupported file format: {file_path.suffix}")
                return None

        except Exception as e:
            logger.error(
                f"Error extracting sequence data from {file_path}: {e}", exc_info=True
            )
            return None

    def extract_metadata(self, file_path: Path) -> Optional[dict[str, Any]]:
        """Extract metadata from a sequence file."""
        try:
            logger.debug(f"Extracting metadata from {file_path}")

            # Look for JSON file
            json_path = file_path
            if file_path.suffix.lower() == ".png":
                json_path = file_path.with_suffix(".json")

            if not json_path.exists():
                logger.warning(f"No metadata file found for {file_path}")
                return None

            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)

            # Extract relevant metadata
            metadata = {
                "file_path": str(file_path),
                "word": self._extract_word_from_path(file_path),
                "sequence_length": len(data.get("sequence", [])),
                "difficulty_level": self._calculate_difficulty_from_data(data),
                "creation_date": data.get("creation_date", ""),
                "author": data.get("author", "Unknown"),
                "notes": data.get("notes", ""),
            }

            logger.debug(f"Extracted metadata: {metadata}")
            return metadata

        except Exception as e:
            logger.error(
                f"Error extracting metadata from {file_path}: {e}", exc_info=True
            )
            return None

    def get_difficulty_level(self, sequence_data: list[dict[str, Any]]) -> int:
        """Calculate difficulty level for a sequence."""
        try:
            if not sequence_data:
                return 1  # Default difficulty for empty sequences

            # Simple difficulty calculation based on sequence length and complexity
            # This replicates the legacy difficulty calculation logic

            sequence_length = len(sequence_data)

            # Base difficulty on sequence length
            if sequence_length <= 4:
                base_difficulty = 1
            elif sequence_length <= 8:
                base_difficulty = 2
            elif sequence_length <= 12:
                base_difficulty = 3
            elif sequence_length <= 16:
                base_difficulty = 4
            else:
                base_difficulty = 5

            # Analyze sequence complexity
            complexity_score = self._calculate_complexity_score(sequence_data)

            # Adjust difficulty based on complexity
            if complexity_score > 0.8:
                base_difficulty = min(5, base_difficulty + 1)
            elif complexity_score > 0.6:
                # Keep base difficulty
                pass
            else:
                base_difficulty = max(1, base_difficulty - 1)

            logger.debug(
                f"Calculated difficulty level: {base_difficulty} for sequence of length {sequence_length}"
            )
            return base_difficulty

        except Exception as e:
            logger.error(f"Error calculating difficulty level: {e}", exc_info=True)
            return 1  # Default to easiest difficulty on error

    def _extract_from_json(self, json_path: Path) -> Optional[list[dict[str, Any]]]:
        """Extract sequence data from a JSON file."""
        try:
            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)

            # Handle different JSON structures
            if "sequence" in data:
                return data["sequence"]
            elif isinstance(data, list):
                return data
            else:
                logger.warning(f"Unexpected JSON structure in {json_path}")
                return []

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {json_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading JSON file {json_path}: {e}")
            return None

    def _extract_word_from_path(self, file_path: Path) -> str:
        """Extract word from file path."""
        # Word is typically the parent directory name
        return file_path.parent.name

    def _calculate_difficulty_from_data(self, data: dict[str, Any]) -> int:
        """Calculate difficulty level from JSON data."""
        # If difficulty is explicitly stored, use it
        if "difficulty_level" in data:
            return int(data["difficulty_level"])

        # Otherwise calculate from sequence
        sequence = data.get("sequence", [])
        return self.get_difficulty_level(sequence)

    def _calculate_complexity_score(self, sequence_data: list[dict[str, Any]]) -> float:
        """
        Calculate complexity score for a sequence.

        This analyzes various factors to determine sequence complexity:
        - Number of different positions/movements
        - Frequency of direction changes
        - Presence of complex movements

        Returns a score between 0.0 (simple) and 1.0 (complex).
        """
        if not sequence_data:
            return 0.0

        try:
            complexity_factors = []

            # Factor 1: Unique positions/movements
            unique_movements = set()
            for beat in sequence_data:
                # Extract movement identifiers (this would depend on the actual data structure)
                if "movement" in beat:
                    unique_movements.add(str(beat["movement"]))
                elif "position" in beat:
                    unique_movements.add(str(beat["position"]))

            movement_diversity = len(unique_movements) / len(sequence_data)
            complexity_factors.append(movement_diversity)

            # Factor 2: Direction changes (if available in data)
            direction_changes = 0
            prev_direction = None
            for beat in sequence_data:
                current_direction = beat.get("direction")
                if (
                    current_direction
                    and prev_direction
                    and current_direction != prev_direction
                ):
                    direction_changes += 1
                prev_direction = current_direction

            if len(sequence_data) > 1:
                direction_change_rate = direction_changes / (len(sequence_data) - 1)
                complexity_factors.append(direction_change_rate)

            # Factor 3: Presence of complex elements (if available)
            complex_elements = 0
            for beat in sequence_data:
                # Look for indicators of complex movements
                if beat.get("is_complex", False) or beat.get("difficulty", 0) > 3:
                    complex_elements += 1

            complex_element_ratio = complex_elements / len(sequence_data)
            complexity_factors.append(complex_element_ratio)

            # Calculate average complexity score
            if complexity_factors:
                complexity_score = sum(complexity_factors) / len(complexity_factors)
            else:
                complexity_score = 0.5  # Default moderate complexity

            # Ensure score is between 0 and 1
            complexity_score = max(0.0, min(1.0, complexity_score))

            logger.debug(f"Calculated complexity score: {complexity_score}")
            return complexity_score

        except Exception as e:
            logger.error(f"Error calculating complexity score: {e}", exc_info=True)
            return 0.5  # Default to moderate complexity on error
