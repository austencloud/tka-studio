"""
Option Picker Data Service

Pure service for managing option picker data operations.
Extracted to follow single responsibility principle.

This service handles:
- Beat option loading and caching
- Sequence-based option refreshing
- Option data conversion and management
- Beat data retrieval for specific options

No UI dependencies, completely testable in isolation.
"""

import logging
from typing import Any, Dict, List, Optional

from core.interfaces.option_picker_services import IOptionPickerDataService
from domain.models.beat_data import BeatData
from domain.models.pictograph_models import PictographData
from domain.models.sequence_models import SequenceData

logger = logging.getLogger(__name__)


class OptionPickerDataService(IOptionPickerDataService):
    """
    Pure service for option picker data management.
    
    Handles beat option loading, caching, and conversion operations
    without any UI dependencies.
    """

    def __init__(self):
        """Initialize the option picker data service."""
        self._cached_pictographs: List[PictographData] = []
        self._option_service = None
        self._position_service = None
        self._initialize_dependencies()

    def _initialize_dependencies(self):
        """Initialize required dependencies."""
        try:
            from presentation.components.option_picker.services.data.option_service import OptionService
            self._option_service = OptionService()
            logger.debug("Option service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize option service: {e}")
            self._option_service = None

        try:
            from application.services.positioning.arrows.utilities.position_matching_service import PositionMatchingService
            self._position_service = PositionMatchingService()
            logger.debug("Position matching service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize position service: {e}")
            self._position_service = None

    def load_beat_options(self) -> List[BeatData]:
        """
        Load initial pictograph options and convert to BeatData only for interface compatibility.

        Note: This method maintains BeatData return type for interface compatibility,
        but internally works with PictographData as it should.

        Returns:
            List of BeatData (converted from pictographs for compatibility)
        """
        try:
            pictographs = self.load_pictograph_options()
            # Convert to BeatData only for interface compatibility
            return self._convert_pictographs_to_beats_for_compatibility(pictographs)

        except Exception as e:
            logger.error(f"Error loading beat options: {e}")
            return []

    def load_pictograph_options(self) -> List[PictographData]:
        """
        Load initial pictograph options (the proper way).

        Returns:
            List of available pictograph data options
        """
        try:
            if not self._position_service:
                logger.warning("Position service not available, returning sample options")
                return self._get_sample_pictograph_options()

            # Get sample options from position service
            try:
                # Get options for a default start position
                pictograph_options = self._position_service.get_next_options("alpha1")
                self._cached_pictographs = pictograph_options

                logger.debug(f"Loaded {len(pictograph_options)} initial pictograph options")
                return pictograph_options
            except Exception as e:
                logger.warning(f"Failed to load from position service: {e}")
                return self._get_sample_pictograph_options()

        except Exception as e:
            logger.error(f"Error loading pictograph options: {e}")
            return []

    def refresh_options(self) -> List[BeatData]:
        """
        Refresh pictograph options and convert to BeatData for interface compatibility.

        Returns:
            Updated list of beat data options (converted from pictographs)
        """
        try:
            pictographs = self.refresh_pictograph_options()
            return self._convert_pictographs_to_beats_for_compatibility(pictographs)

        except Exception as e:
            logger.error(f"Error refreshing options: {e}")
            return []

    def refresh_pictograph_options(self) -> List[PictographData]:
        """
        Refresh pictograph options (the proper way).

        Returns:
            Updated list of pictograph data options
        """
        try:
            # For now, just return cached pictographs
            # In the future, this could reload from external sources
            logger.debug(f"Refreshed {len(self._cached_pictographs)} pictograph options")
            return self._cached_pictographs.copy()

        except Exception as e:
            logger.error(f"Error refreshing pictograph options: {e}")
            return []

    def refresh_from_sequence_data(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[BeatData]:
        """
        Refresh options based on legacy sequence data.

        Args:
            sequence_data: Legacy sequence data format

        Returns:
            Updated list of beat data options (converted from pictographs)
        """
        try:
            pictographs = self.refresh_pictographs_from_sequence_data(sequence_data)
            return self._convert_pictographs_to_beats_for_compatibility(pictographs)

        except Exception as e:
            logger.error(f"Error refreshing from sequence data: {e}")
            return []

    def refresh_pictographs_from_sequence_data(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[PictographData]:
        """
        Refresh pictograph options based on legacy sequence data (the proper way).

        Args:
            sequence_data: Legacy sequence data format

        Returns:
            Updated list of pictograph data options
        """
        try:
            if not self._option_service:
                logger.warning("Option service not available")
                return []

            if not sequence_data:
                logger.debug("No sequence data provided, returning empty options")
                self._cached_pictographs = []
                return []

            # Load pictograph options from sequence data
            pictograph_options = self._option_service.load_options_from_sequence(sequence_data)
            self._cached_pictographs = pictograph_options

            logger.debug(f"Refreshed {len(pictograph_options)} pictographs from legacy sequence data")
            return pictograph_options

        except Exception as e:
            logger.error(f"Error refreshing pictographs from sequence data: {e}")
            return []

    def refresh_from_sequence(self, sequence: SequenceData) -> List[BeatData]:
        """
        Refresh options based on modern sequence data.

        Args:
            sequence: Modern sequence data

        Returns:
            Updated list of beat data options (converted from pictographs)
        """
        try:
            pictographs = self.refresh_pictographs_from_sequence(sequence)
            return self._convert_pictographs_to_beats_for_compatibility(pictographs)

        except Exception as e:
            logger.error(f"Error refreshing from modern sequence: {e}")
            return []

    def refresh_pictographs_from_sequence(self, sequence: SequenceData) -> List[PictographData]:
        """
        Refresh pictograph options based on modern sequence data (the proper way).

        Args:
            sequence: Modern sequence data

        Returns:
            Updated list of pictograph data options
        """
        try:
            if not sequence or sequence.length == 0:
                logger.debug("Empty sequence provided, returning empty options")
                self._cached_pictographs = []
                return []

            # Convert modern sequence to legacy format for compatibility
            legacy_data = self._convert_sequence_to_legacy_format(sequence)

            # Use legacy refresh method
            return self.refresh_pictographs_from_sequence_data(legacy_data)

        except Exception as e:
            logger.error(f"Error refreshing pictographs from modern sequence: {e}")
            return []

    def get_beat_data_for_option(self, option_id: str) -> Optional[BeatData]:
        """
        Get beat data for a specific option ID.

        Args:
            option_id: Option identifier (e.g., 'beat_J')

        Returns:
            BeatData if found, None otherwise
        """
        try:
            # Parse option ID to extract letter
            if option_id.startswith("beat_"):
                letter = option_id[5:]  # Remove "beat_" prefix
                
                # Find option with matching letter
                for option in self._cached_options:
                    if option.letter == letter:
                        return option
                        
            logger.debug(f"Option not found for ID: {option_id}")
            return None

        except Exception as e:
            logger.error(f"Error getting beat data for option {option_id}: {e}")
            return None

    def get_current_options(self) -> List[BeatData]:
        """
        Get currently loaded options as BeatData for interface compatibility.

        Returns:
            Current list of beat data options (converted from pictographs)
        """
        return self._convert_pictographs_to_beats_for_compatibility(self._cached_pictographs)

    def get_current_pictographs(self) -> List[PictographData]:
        """
        Get currently loaded pictograph options (the proper way).

        Returns:
            Current list of pictograph data options
        """
        return self._cached_pictographs.copy()

    def clear_cache(self) -> None:
        """Clear cached options."""
        self._cached_pictographs = []
        logger.debug("Cleared option cache")

    def _convert_sequence_to_legacy_format(self, sequence: SequenceData) -> List[Dict[str, Any]]:
        """
        Convert modern sequence to legacy format for compatibility.
        
        Args:
            sequence: Modern sequence data
            
        Returns:
            Legacy format sequence data
        """
        try:
            from application.services.data.sequence_data_converter import SequenceDataConverter
            
            converter = SequenceDataConverter()
            legacy_data = converter.convert_sequence_to_legacy_format(sequence)
            
            logger.debug(f"Converted modern sequence to legacy format: {len(legacy_data)} items")
            return legacy_data

        except Exception as e:
            logger.error(f"Error converting sequence to legacy format: {e}")
            return []

    def get_option_count(self) -> int:
        """Get the number of currently cached pictograph options."""
        return len(self._cached_pictographs)

    def filter_options_by_letter(self, letter: str) -> List[BeatData]:
        """
        Filter current pictographs by letter and return as BeatData for compatibility.

        Args:
            letter: Letter to filter by

        Returns:
            List of BeatData options matching the letter
        """
        try:
            filtered_pictographs = [opt for opt in self._cached_pictographs if opt.letter == letter]
            logger.debug(f"Filtered {len(filtered_pictographs)} pictographs for letter '{letter}'")
            return self._convert_pictographs_to_beats_for_compatibility(filtered_pictographs)

        except Exception as e:
            logger.error(f"Error filtering options by letter {letter}: {e}")
            return []

    def filter_pictographs_by_letter(self, letter: str) -> List[PictographData]:
        """
        Filter current pictographs by letter (the proper way).

        Args:
            letter: Letter to filter by

        Returns:
            List of pictograph options matching the letter
        """
        try:
            filtered = [opt for opt in self._cached_pictographs if opt.letter == letter]
            logger.debug(f"Filtered {len(filtered)} pictographs for letter '{letter}'")
            return filtered

        except Exception as e:
            logger.error(f"Error filtering pictographs by letter {letter}: {e}")
            return []

    def get_available_letters(self) -> List[str]:
        """
        Get list of available letters in current pictograph options.

        Returns:
            Sorted list of unique letters
        """
        try:
            letters = {opt.letter for opt in self._cached_pictographs if opt.letter}
            return sorted(list(letters))

        except Exception as e:
            logger.error(f"Error getting available letters: {e}")
            return []

    def _convert_pictographs_to_beats_for_compatibility(self, pictograph_options) -> List[BeatData]:
        """
        Convert pictograph options to beat data ONLY for interface compatibility.

        This method exists solely to maintain backward compatibility with interfaces
        that expect BeatData. The proper approach is to work with PictographData directly.

        Args:
            pictograph_options: List of PictographData objects

        Returns:
            List of BeatData objects (for compatibility only)
        """
        try:
            from application.services.data.pictograph_factory import PictographFactory

            factory = PictographFactory()
            beat_options = []

            for i, pictograph in enumerate(pictograph_options):
                try:
                    beat_data = factory.convert_pictograph_to_beat_data(pictograph, i + 1)
                    beat_options.append(beat_data)
                except Exception as e:
                    logger.warning(f"Failed to convert pictograph to beat for compatibility: {e}")
                    continue

            return beat_options

        except Exception as e:
            logger.error(f"Error converting pictographs to beats for compatibility: {e}")
            return []

    def _get_sample_pictograph_options(self) -> List[PictographData]:
        """
        Get sample pictograph options as fallback (the proper way).

        Returns:
            List of sample PictographData objects
        """
        try:
            from domain.models.motion_models import MotionData
            from domain.models.pictograph_models import ArrowData, GridData, GridMode

            # Create sample pictograph options
            sample_options = []
            letters = ["A", "B", "C", "D", "E"]

            for letter in letters:
                # Create sample motion data
                motion_data = MotionData(
                    motion_type="static",
                    start_loc="n",
                    end_loc="n",
                    start_ori="in",
                    end_ori="in",
                    prop_rot_dir="no_rot",
                    turns=0,
                )

                # Create arrow data
                arrows = {
                    "blue": ArrowData(motion_data=motion_data, color="blue"),
                    "red": ArrowData(motion_data=motion_data, color="red"),
                }

                # Create grid data
                grid_data = GridData(grid_mode=GridMode.DIAMOND)

                # Create sample pictograph
                pictograph_data = PictographData(
                    grid_data=grid_data,
                    arrows=arrows,
                    props={},
                    letter=letter,
                    start_position="alpha1",
                    end_position="alpha1",
                    metadata={"source": "sample"},
                )

                sample_options.append(pictograph_data)

            self._cached_pictographs = sample_options
            logger.debug(f"Created {len(sample_options)} sample pictograph options")
            return sample_options

        except Exception as e:
            logger.error(f"Error creating sample pictograph options: {e}")
            return []
