"""
Option Picker Data Service

Pure service for managing option picker data operations.
Extracted to follow single responsibility principle.

This service handles:
- Pictograph option loading and caching
- Sequence-based option refreshing
- Pictograph data management
- Option retrieval for specific IDs

No UI dependencies, completely testable in isolation.
Works exclusively with PictographData - no beat data conversions.
"""

import logging
from typing import Any, Dict, List, Optional

from core.interfaces.option_picker_services import IOptionPickerDataService
from domain.models.pictograph_models import PictographData
from domain.models.sequence_models import SequenceData

logger = logging.getLogger(__name__)


class OptionPickerDataService(IOptionPickerDataService):
    """
    Pure service for option picker data management.

    Handles pictograph option loading, caching, and management operations
    without any UI dependencies. Works exclusively with PictographData.
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
            from application.services.option_picker.option_provider import (
                OptionProvider,
            )

            self._option_service = OptionProvider()
            logger.debug("Option service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize option service: {e}")
            self._option_service = None

        try:
            from application.services.positioning.arrows.utilities.position_matching_service import (
                PositionMatchingService,
            )

            self._position_service = PositionMatchingService()
            logger.debug("Position matching service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize position service: {e}")
            self._position_service = None

    def load_pictograph_options(self) -> List[PictographData]:
        """
        Load initial pictograph options (the proper way).

        Returns:
            List of available pictograph data options
        """
        try:
            if not self._position_service:
                logger.warning(
                    "Position service not available, returning sample options"
                )
                return self._get_sample_pictograph_options()

            # Get sample options from position service
            try:
                # Get options for a default start position
                pictograph_options = self._position_service.get_next_options("alpha1")
                self._cached_pictographs = pictograph_options

                logger.debug(
                    f"Loaded {len(pictograph_options)} initial pictograph options"
                )
                return pictograph_options
            except Exception as e:
                logger.warning(f"Failed to load from position service: {e}")
                return self._get_sample_pictograph_options()

        except Exception as e:
            logger.error(f"Error loading pictograph options: {e}")
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
            logger.debug(
                f"Refreshed {len(self._cached_pictographs)} pictograph options"
            )
            return self._cached_pictographs.copy()

        except Exception as e:
            logger.error(f"Error refreshing pictograph options: {e}")
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
            pictograph_options = self._option_service.load_options_from_sequence(
                sequence_data
            )
            self._cached_pictographs = pictograph_options

            logger.debug(
                f"Refreshed {len(pictograph_options)} pictographs from legacy sequence data"
            )
            return pictograph_options

        except Exception as e:
            logger.error(f"Error refreshing pictographs from sequence data: {e}")
            return []

    def refresh_pictographs_from_sequence(
        self, sequence: SequenceData
    ) -> List[PictographData]:
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

    def get_pictograph_for_option(self, option_id: str) -> Optional[PictographData]:
        """
        Get pictograph data for a specific option ID.

        Args:
            option_id: Option identifier (e.g., 'option_0', 'option_J')

        Returns:
            PictographData if found, None otherwise
        """
        try:
            # Parse option ID to extract index or letter
            if option_id.startswith("option_"):
                identifier = option_id[7:]  # Remove "option_" prefix

                # Try to parse as index first
                try:
                    index = int(identifier)
                    if 0 <= index < len(self._cached_pictographs):
                        return self._cached_pictographs[index]
                except ValueError:
                    # Not an index, try as letter
                    for pictograph in self._cached_pictographs:
                        if pictograph.letter == identifier:
                            return pictograph

            logger.debug(f"Pictograph not found for ID: {option_id}")
            return None

        except Exception as e:
            logger.error(f"Error getting pictograph for option {option_id}: {e}")
            return None

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

    def _convert_sequence_to_legacy_format(
        self, sequence: SequenceData
    ) -> List[Dict[str, Any]]:
        """
        Convert modern sequence to legacy format for compatibility.

        Args:
            sequence: Modern sequence data

        Returns:
            Legacy format sequence data
        """
        try:
            from application.services.data.sequence_data_converter import (
                SequenceDataConverter,
            )

            converter = SequenceDataConverter()
            legacy_data = converter.convert_sequence_to_legacy_format(sequence)

            logger.debug(
                f"Converted modern sequence to legacy format: {len(legacy_data)} items"
            )
            return legacy_data

        except Exception as e:
            logger.error(f"Error converting sequence to legacy format: {e}")
            return []

    def get_option_count(self) -> int:
        """Get the number of currently cached pictograph options."""
        return len(self._cached_pictographs)

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
