"""
SequenceDataConverter

Facade service that delegates to focused conversion services.
Maintains backward compatibility while using the new focused architecture.
"""

from domain.models.beat_data import BeatData
from domain.models.sequence_models import SequenceData

from .legacy_to_modern_converter import LegacyToModernConverter
from .modern_to_legacy_converter import ModernToLegacyConverter
from .sequence_format_adapter import SequenceFormatAdapter


class SequenceDataConverter:
    """
    Facade service for converting between legacy JSON format and modern domain models.

    This service delegates to focused services while maintaining the same public interface
    for backward compatibility.
    """

    def __init__(self):
        """Initialize the sequence data converter with focused services."""
        self.legacy_to_modern = LegacyToModernConverter()
        self.modern_to_legacy = ModernToLegacyConverter()
        self.sequence_adapter = SequenceFormatAdapter()

    def convert_legacy_to_beat_data(
        self, beat_dict: dict, beat_number: int
    ) -> BeatData:
        """Convert legacy JSON format back to modern BeatData with full pictograph data"""
        return self.legacy_to_modern.convert_legacy_to_beat_data(beat_dict, beat_number)

    def convert_legacy_start_position_to_beat_data(
        self, start_pos_dict: dict
    ) -> BeatData:
        """Convert legacy start position JSON back to modern BeatData with full data"""
        return self.legacy_to_modern.convert_legacy_start_position_to_beat_data(
            start_pos_dict
        )

    def convert_beat_data_to_legacy_format(
        self, beat: BeatData, beat_number: int
    ) -> dict:
        """Convert modern BeatData to legacy JSON format exactly like legacy pictograph_data"""
        return self.modern_to_legacy.convert_beat_data_to_legacy_format(
            beat, beat_number
        )

    def convert_start_position_to_legacy_format(
        self, start_position_data: BeatData
    ) -> dict:
        """Convert start position BeatData to legacy format exactly like JsonStartPositionHandler"""
        return self.modern_to_legacy.convert_start_position_to_legacy_format(
            start_position_data
        )

    def convert_sequence_to_legacy_format(self, sequence: SequenceData) -> list:
        """Convert modern SequenceData back to legacy JSON format"""
        return self.sequence_adapter.convert_sequence_to_legacy_format(sequence)

    def _convert_beat_to_legacy_dict(self, beat: BeatData) -> dict:
        """Convert a single BeatData to legacy dictionary format"""
        return self.modern_to_legacy.convert_beat_to_legacy_dict(beat)
