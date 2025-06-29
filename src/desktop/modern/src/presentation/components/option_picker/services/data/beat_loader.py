"""
Beat Data Loader - Main Loading Orchestration
Split from beat_data_loader.py - contains high-level loading logic
"""

from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional
from PyQt6.QtCore import QObject

from domain.models.core_models import BeatData
from application.services.data.data_conversion_service import DataConversionService
from application.services.option_picker.option_orientation_update_service import (
    OptionOrientationUpdateService,
)
from presentation.components.option_picker.services.data.position_matcher import (
    PositionMatcher,
)

if TYPE_CHECKING:
    from domain.models.core_models import SequenceData


class BeatDataLoader(QObject):
    """Handles loading beat options and orchestrates position matching logic."""

    def __init__(self):
        super().__init__()
        self._beat_options: List[BeatData] = []
        self.position_matcher = PositionMatcher()

        try:
            from application.services.positioning.arrows.utilities.position_matching_service import (
                PositionMatchingService,
            )

            self.position_service = PositionMatchingService()
            self.conversion_service = DataConversionService()
            self.orientation_update_service = OptionOrientationUpdateService()
        except Exception:
            self.position_service = None
            self.conversion_service = None
            self.orientation_update_service = None

    def load_motion_combinations(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[BeatData]:
        """Load motion combinations using data-driven position matching."""
        try:
            if not self.position_service or not self.conversion_service:
                return self._load_sample_beat_options()

            if not sequence_data or len(sequence_data) < 2:
                return self._load_sample_beat_options()

            last_beat = sequence_data[-1]
            last_end_pos = self.position_matcher.extract_end_position(
                last_beat, self.position_service
            )

            if not last_end_pos:
                return self._load_sample_beat_options()

            next_options = self.position_service.get_next_options(last_end_pos)
            if not next_options:
                return self._load_sample_beat_options()

            beat_options = self._batch_convert_options(next_options)

            if self.orientation_update_service and len(sequence_data) >= 2:
                beat_options = self._apply_orientation_updates(
                    sequence_data, beat_options
                )

            self._beat_options = beat_options
            return beat_options

        except Exception:
            return self._load_sample_beat_options()

    def refresh_options_from_sequence(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[BeatData]:
        """Refresh options based on provided sequence data (Legacy-compatible)."""
        if not sequence_data or len(sequence_data) <= 1:
            return self._load_sample_beat_options()

        last_beat = sequence_data[-1]

        try:
            if not self.position_service or not self.conversion_service:
                return self._load_sample_beat_options()

            end_position = self.position_matcher.extract_end_position(
                last_beat, self.position_service
            )

            if not end_position:
                return self._load_sample_beat_options()

            next_options = self.position_service.get_next_options(end_position)
            if not next_options:
                return self._load_sample_beat_options()

            beat_options = self._batch_convert_options(next_options)
            return beat_options

        except Exception:
            return self._load_sample_beat_options()

    def refresh_options_from_modern_sequence(
        self, sequence: "SequenceData"
    ) -> List[BeatData]:
        """PURE Modern: Refresh options based on Modern SequenceData."""
        try:
            if not sequence or sequence.length == 0:
                return self._load_sample_beat_options()

            last_beat = sequence.beats[-1] if sequence.beats else None
            if not last_beat or last_beat.is_blank:
                return self._load_sample_beat_options()

            end_position = self.position_matcher.extract_modern_end_position(last_beat)
            if not end_position:
                return self._load_sample_beat_options()

            if not self.position_service:
                return self._load_sample_beat_options()

            next_options = self.position_service.get_next_options(end_position)
            if not next_options:
                return self._load_sample_beat_options()

            if self.orientation_update_service:
                next_options = (
                    self.orientation_update_service.update_option_orientations(
                        sequence, next_options
                    )
                )

            return next_options

        except Exception:
            return self._load_sample_beat_options()

    def _batch_convert_options(self, options_list: List[Any]) -> List[BeatData]:
        """Optimized batch conversion of options to BeatData format."""
        from domain.models.core_models import BeatData

        beat_options = []
        beat_data_objects = []
        dict_objects = []
        other_objects = []

        for option_data in options_list:
            if isinstance(option_data, BeatData):
                beat_data_objects.append(option_data)
            elif hasattr(option_data, "get"):
                dict_objects.append(option_data)
            elif hasattr(option_data, "letter"):
                other_objects.append(option_data)

        beat_options.extend(beat_data_objects)

        if dict_objects:
            try:
                for option_data in dict_objects:
                    beat_data = self.conversion_service.convert_external_pictograph_to_beat_data(
                        option_data
                    )
                    beat_options.append(beat_data)
            except Exception:
                pass

        beat_options.extend(other_objects)
        return beat_options

    def _apply_orientation_updates(
        self, sequence_data: List[Dict[str, Any]], beat_options: List[BeatData]
    ) -> List[BeatData]:
        """Apply orientation updates to beat options."""
        try:
            start_position_dict = sequence_data[-1]
            if (
                isinstance(start_position_dict, dict)
                and "letter" in start_position_dict
            ):
                start_beat = (
                    self.conversion_service.convert_external_pictograph_to_beat_data(
                        start_position_dict
                    )
                )
                from domain.models.core_models import SequenceData

                temp_sequence = SequenceData.empty().update(beats=[start_beat])
                beat_options = (
                    self.orientation_update_service.update_option_orientations(
                        temp_sequence, beat_options
                    )
                )
        except Exception:
            pass
        return beat_options

    def _load_sample_beat_options(self) -> List[BeatData]:
        """Load sample beat options as fallback."""
        self._beat_options = []
        return self._beat_options

    def get_beat_options(self) -> List[BeatData]:
        """Get current beat options."""
        return self._beat_options

    def refresh_options(self) -> List[BeatData]:
        """Refresh beat options."""
        self._beat_options = []
        return self._beat_options
