"""
Sequence Format Adapter

Handles sequence-level format adaptation between modern and legacy formats.
Focused solely on sequence structure and metadata handling.
"""

import logging
from typing import List

from domain.models.beat_data import BeatData
from domain.models.sequence_models import SequenceData
from .modern_to_legacy_converter import ModernToLegacyConverter

logger = logging.getLogger(__name__)


class SequenceFormatAdapter:
    """
    Adapts sequence formats between modern and legacy representations.
    
    Responsible for:
    - Converting SequenceData to legacy JSON format
    - Handling sequence metadata and structure
    - Managing start position separation and integration
    - Maintaining sequence-level compatibility
    """

    def __init__(self):
        """Initialize the sequence format adapter."""
        self.modern_to_legacy = ModernToLegacyConverter()

    def convert_sequence_to_legacy_format(self, sequence: SequenceData) -> list:
        """
        Convert modern SequenceData to legacy JSON format.
        
        Args:
            sequence: SequenceData object to convert
            
        Returns:
            List in legacy JSON format with metadata, start position, and beats
        """
        try:
            legacy_data = []

            # Separate start position from regular beats
            start_position_beat, regular_beats = self._separate_start_position_and_beats(sequence)

            # Add sequence metadata as first item [0]
            metadata = self._create_sequence_metadata(sequence, regular_beats)
            legacy_data.append(metadata)

            # Only add start position if it actually exists (user selected one)
            if start_position_beat:
                start_pos_dict = self.modern_to_legacy.convert_start_position_to_legacy_format(
                    start_position_beat
                )
                legacy_data.append(start_pos_dict)

            # Convert regular beats to legacy format (starting at index [2])
            for beat in regular_beats:
                beat_dict = self.modern_to_legacy.convert_beat_to_legacy_dict(beat)
                legacy_data.append(beat_dict)

            return legacy_data

        except Exception as e:
            logger.error(f"Failed to convert sequence to legacy format: {e}")
            return self._create_fallback_legacy_sequence(sequence)

    def _separate_start_position_and_beats(self, sequence: SequenceData) -> tuple:
        """
        Separate start position from regular beats in a sequence.
        
        Args:
            sequence: SequenceData object
            
        Returns:
            Tuple of (start_position_beat, regular_beats)
        """
        start_position_beat = None
        regular_beats = []

        for beat in sequence.beats:
            if self._is_start_position_beat(beat):
                start_position_beat = beat
            else:
                regular_beats.append(beat)

        return start_position_beat, regular_beats

    def _is_start_position_beat(self, beat: BeatData) -> bool:
        """
        Check if a beat represents a start position.
        
        Args:
            beat: BeatData to check
            
        Returns:
            True if it's a start position beat
        """
        # Check beat number and metadata
        if beat.beat_number == 0:
            return True
            
        if beat.metadata and beat.metadata.get("is_start_position", False):
            return True
            
        return False

    def _create_sequence_metadata(self, sequence: SequenceData, regular_beats: List[BeatData]) -> dict:
        """
        Create sequence metadata for legacy format.
        
        Args:
            sequence: SequenceData object
            regular_beats: List of regular beats (excluding start position)
            
        Returns:
            Dictionary with sequence metadata
        """
        # Extract sequence start position from first beat or default
        sequence_start_position = "alpha"
        if regular_beats and regular_beats[0].glyph_data:
            start_pos = regular_beats[0].glyph_data.get("start_position", "")
            if start_pos:
                sequence_start_position = self._extract_position_type(start_pos)

        return {
            "sequence_name": sequence.name,
            "beat_count": len(regular_beats),  # Only count regular beats
            "length": len(regular_beats),
            "level": 1,
            "sequence_start_position": sequence_start_position,
        }

    def _extract_position_type(self, position_string: str) -> str:
        """
        Extract position type from position string.
        
        Args:
            position_string: Position string like "alpha1", "beta5"
            
        Returns:
            Position type ("alpha", "beta", "gamma")
        """
        if not position_string:
            return "alpha"
            
        position_string = str(position_string).lower()
        
        if position_string.startswith("alpha"):
            return "alpha"
        elif position_string.startswith("beta"):
            return "beta"
        elif position_string.startswith("gamma"):
            return "gamma"
        else:
            return "alpha"

    def _create_fallback_legacy_sequence(self, sequence: SequenceData) -> list:
        """
        Create fallback legacy sequence when conversion fails.
        
        Args:
            sequence: Original sequence data
            
        Returns:
            Minimal legacy sequence format
        """
        try:
            return [
                {
                    "sequence_name": sequence.name if sequence else "Unknown",
                    "beat_count": 0,
                    "length": 0,
                    "level": 1,
                    "sequence_start_position": "alpha",
                }
            ]
        except Exception:
            return [
                {
                    "sequence_name": "Unknown",
                    "beat_count": 0,
                    "length": 0,
                    "level": 1,
                    "sequence_start_position": "alpha",
                }
            ]

    def validate_sequence_for_conversion(self, sequence: SequenceData) -> bool:
        """
        Validate that a sequence can be converted to legacy format.
        
        Args:
            sequence: SequenceData to validate
            
        Returns:
            True if conversion is possible, False otherwise
        """
        if not isinstance(sequence, SequenceData):
            return False

        # Check for required fields
        if not hasattr(sequence, 'name') or not hasattr(sequence, 'beats'):
            return False

        # Check that beats is iterable
        try:
            iter(sequence.beats)
        except TypeError:
            return False

        return True

    def get_legacy_sequence_structure(self) -> dict:
        """
        Get the expected structure of legacy sequence format.
        
        Returns:
            Dictionary describing the legacy sequence structure
        """
        return {
            "index_0": "sequence_metadata",
            "index_1": "start_position (optional)",
            "index_2_plus": "regular_beats",
            "metadata_fields": [
                "sequence_name",
                "beat_count",
                "length",
                "level",
                "sequence_start_position",
            ],
            "start_position_fields": [
                "beat",
                "sequence_start_position",
                "letter",
                "end_pos",
                "timing",
                "direction",
                "blue_attributes",
                "red_attributes",
            ],
            "beat_fields": [
                "beat",
                "letter",
                "duration",
                "start_pos",
                "end_pos",
                "timing",
                "direction",
                "blue_attributes",
                "red_attributes",
            ],
        }

    def extract_sequence_info_from_legacy(self, legacy_data: list) -> dict:
        """
        Extract sequence information from legacy format.
        
        Args:
            legacy_data: Legacy sequence data list
            
        Returns:
            Dictionary with extracted sequence information
        """
        if not legacy_data or not isinstance(legacy_data, list):
            return {"error": "Invalid legacy data format"}

        try:
            # First item should be metadata
            metadata = legacy_data[0] if legacy_data else {}
            
            # Check if second item is start position
            has_start_position = False
            if len(legacy_data) > 1:
                second_item = legacy_data[1]
                if isinstance(second_item, dict) and second_item.get("beat") == 0:
                    has_start_position = True

            # Count regular beats
            beat_start_index = 2 if has_start_position else 1
            regular_beat_count = max(0, len(legacy_data) - beat_start_index)

            return {
                "sequence_name": metadata.get("sequence_name", "Unknown"),
                "beat_count": metadata.get("beat_count", regular_beat_count),
                "has_start_position": has_start_position,
                "total_items": len(legacy_data),
                "regular_beat_count": regular_beat_count,
                "sequence_start_position": metadata.get("sequence_start_position", "alpha"),
            }

        except Exception as e:
            logger.error(f"Error extracting sequence info from legacy data: {e}")
            return {"error": f"Failed to extract sequence info: {e}"}
