"""
Beat Data Loader - UI Adapter for Beat Loading

This is now a thin UI adapter that delegates business logic to the
BeatLoadingService. It maintains backward compatibility while using
the extracted business service and handles Qt-specific concerns.
"""

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from PyQt6.QtCore import QObject

from domain.models.core_models import BeatData
from core.interfaces.core_services import IBeatLoadingService
from presentation.components.option_picker.services.data.position_matcher import (
    PositionMatcher,
)

if TYPE_CHECKING:
    from domain.models.core_models import SequenceData

logger = logging.getLogger(__name__)


class BeatDataLoader(QObject):
    """
    UI adapter for beat loading operations.

    This class now delegates all business logic to the IBeatLoadingService
    while maintaining Qt-specific functionality and the same public interface
    for backward compatibility.
    """

    def __init__(self, beat_loading_service: Optional[IBeatLoadingService] = None):
        """
        Initialize beat data loader with injected business service.

        Args:
            beat_loading_service: Injected beat loading service
        """
        super().__init__()
        self._beat_options: List[BeatData] = []
        self._beat_loading_service = beat_loading_service

        # Fallback for legacy compatibility - will be removed in future versions
        if not self._beat_loading_service:
            try:
                from application.services.data.beat_loading_service import (
                    BeatLoadingService,
                )

                self._beat_loading_service = BeatLoadingService()
                logger.warning(
                    "Using fallback beat loading service - consider using DI container"
                )
            except ImportError:
                logger.error("Beat loading service not available")
                self._beat_loading_service = None

        # Initialize legacy services for backward compatibility
        try:
            from application.services.positioning.arrows.utilities.position_matching_service import (
                PositionMatchingService,
            )
            from application.services.positioning.position_matching_service import (
                PositionMatchingService as NewPositionMatchingService,
            )
            from application.services.data.data_conversion_service import (
                DataConversionService,
            )
            from application.services.option_picker.orientation_update_service import (
                OptionOrientationUpdateService,
            )

            self.position_service = PositionMatchingService()
            self.conversion_service = DataConversionService()
            self.orientation_update_service = OptionOrientationUpdateService()

            # Initialize position matcher with the new service
            new_position_service = NewPositionMatchingService()
            self.position_matcher = PositionMatcher(new_position_service)

        except Exception as e:
            logger.error(f"Error initializing legacy services: {e}")
            self.position_service = None
            self.conversion_service = None
            self.orientation_update_service = None
            # Fallback position matcher without service injection
            self.position_matcher = PositionMatcher()

    def load_motion_combinations(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[BeatData]:
        """
        Load motion combinations using data-driven position matching.

        Args:
            sequence_data: Sequence data in legacy format

        Returns:
            List of beat data options
        """
        if not self._beat_loading_service:
            logger.error("Beat loading service not available")
            return self._load_sample_beat_options()

        try:
            # Delegate to business service
            beat_options = self._beat_loading_service.load_motion_combinations(
                sequence_data
            )

            # Cache the options for UI purposes
            self._beat_options = beat_options

            logger.debug(f"Loaded {len(beat_options)} motion combinations via service")
            return beat_options

        except Exception as e:
            logger.error(f"Error loading motion combinations: {e}")
            return self._load_sample_beat_options()

    def refresh_options_from_sequence(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[BeatData]:
        """
        Refresh options based on provided sequence data (Legacy-compatible).

        Args:
            sequence_data: Sequence data in legacy format

        Returns:
            List of refreshed beat data options
        """
        if not self._beat_loading_service:
            logger.error("Beat loading service not available")
            return self._load_sample_beat_options()

        try:
            # Delegate to business service (same as load_motion_combinations for now)
            beat_options = self._beat_loading_service.load_motion_combinations(
                sequence_data
            )

            logger.debug(
                f"Refreshed {len(beat_options)} options from sequence via service"
            )
            return beat_options

        except Exception as e:
            logger.error(f"Error refreshing options from sequence: {e}")
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
