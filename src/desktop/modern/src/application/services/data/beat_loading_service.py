"""
Beat Loading Service - Business Logic for Beat Data Loading

This service contains the pure business logic for beat data loading and orchestration,
extracted from the presentation layer. It has no PyQt6 dependencies and can be used
across different UI frameworks.

RESPONSIBILITIES:
- Motion combination loading logic
- Beat option filtering and validation
- Data conversion orchestration
- Orientation update coordination

USAGE:
    service = container.resolve(IBeatLoadingService)
    options = service.load_motion_combinations(sequence_data)
    filtered = service.filter_valid_options(options, end_position)
"""

import logging
from typing import Dict, Any, List, Optional

from core.interfaces.core_services import IBeatLoadingService
from core.interfaces.positioning_services import IPositionMatchingService
from domain.models.core_models import BeatData, SequenceData

logger = logging.getLogger(__name__)


class BeatLoadingService(IBeatLoadingService):
    """
    Business logic service for beat data loading and orchestration.
    
    This service implements the core beat loading logic that was previously
    embedded in the presentation layer. It provides a clean interface for
    beat loading operations without any UI dependencies.
    """

    def __init__(
        self,
        position_service: Optional[IPositionMatchingService] = None,
        conversion_service: Optional[Any] = None,
        orientation_service: Optional[Any] = None,
    ):
        """
        Initialize the beat loading service.
        
        Args:
            position_service: Position matching service for end position extraction
            conversion_service: Data conversion service for format transformations
            orientation_service: Orientation update service for beat orientation updates
        """
        self._position_service = position_service
        self._conversion_service = conversion_service
        self._orientation_service = orientation_service
        
        # Initialize services if not provided (fallback for legacy compatibility)
        if not self._position_service:
            try:
                from application.services.positioning.position_matching_service import PositionMatchingService
                self._position_service = PositionMatchingService()
                logger.warning("Using fallback position service - consider using DI container")
            except ImportError:
                logger.error("Position matching service not available")
                
        if not self._conversion_service:
            try:
                from application.services.data.data_conversion_service import DataConversionService
                self._conversion_service = DataConversionService()
                logger.warning("Using fallback conversion service - consider using DI container")
            except ImportError:
                logger.error("Data conversion service not available")
                
        if not self._orientation_service:
            try:
                from application.services.option_picker.orientation_update_service import OptionOrientationUpdateService
                self._orientation_service = OptionOrientationUpdateService()
                logger.warning("Using fallback orientation service - consider using DI container")
            except ImportError:
                logger.error("Orientation update service not available")

        logger.debug("Beat loading service initialized")

    def load_motion_combinations(self, sequence_data: List[Dict[str, Any]]) -> List[Any]:
        """
        Load motion combinations with position matching.
        
        Args:
            sequence_data: Sequence data in legacy format
            
        Returns:
            List of beat data options
        """
        try:
            # Validate prerequisites
            if not self._position_service or not self._conversion_service:
                logger.warning("Required services not available, returning sample options")
                return self.get_sample_beat_options()

            if not sequence_data or len(sequence_data) < 2:
                logger.debug("Insufficient sequence data, returning sample options")
                return self.get_sample_beat_options()

            # Extract end position from last beat
            last_beat = sequence_data[-1]
            last_end_pos = self._position_service.extract_end_position(last_beat)

            if not last_end_pos:
                logger.debug("No end position found, returning sample options")
                return self.get_sample_beat_options()

            # Get next options from position service
            try:
                from application.services.positioning.arrows.utilities.position_matching_service import PositionMatchingService
                legacy_position_service = PositionMatchingService()
                next_options = legacy_position_service.get_next_options(last_end_pos)
            except Exception as e:
                logger.error(f"Error getting next options: {e}")
                return self.get_sample_beat_options()

            if not next_options:
                logger.debug("No next options found, returning sample options")
                return self.get_sample_beat_options()

            # Convert options to beat data format
            beat_options = self._batch_convert_options(next_options)

            # Apply orientation updates if available
            if self._orientation_service and len(sequence_data) >= 2:
                beat_options = self._apply_orientation_updates(sequence_data, beat_options)

            logger.debug(f"Successfully loaded {len(beat_options)} motion combinations")
            return beat_options

        except Exception as e:
            logger.error(f"Error loading motion combinations: {e}")
            return self.get_sample_beat_options()

    def filter_valid_options(self, beat_options: List[Any], end_position: str) -> List[Any]:
        """
        Filter beat options based on end position.
        
        Args:
            beat_options: List of beat options to filter
            end_position: Required end position for filtering
            
        Returns:
            Filtered list of beat options
        """
        try:
            if not beat_options:
                return []

            filtered_options = []
            for option in beat_options:
                # Check if option matches the required end position
                if hasattr(option, 'metadata') and option.metadata:
                    option_start_pos = option.metadata.get('start_pos')
                    if option_start_pos == end_position:
                        filtered_options.append(option)
                elif hasattr(option, 'get'):
                    option_start_pos = option.get('start_pos')
                    if option_start_pos == end_position:
                        filtered_options.append(option)
                else:
                    # Include option if we can't determine position (safe fallback)
                    filtered_options.append(option)

            logger.debug(f"Filtered {len(filtered_options)} options from {len(beat_options)} total")
            return filtered_options

        except Exception as e:
            logger.error(f"Error filtering options: {e}")
            return beat_options  # Return unfiltered on error

    def get_sample_beat_options(self) -> List[Any]:
        """
        Get fallback sample options.
        
        Returns:
            Empty list as fallback
        """
        logger.debug("Returning empty sample beat options")
        return []

    def _batch_convert_options(self, options_list: List[Any]) -> List[Any]:
        """
        Optimized batch conversion of options to BeatData format.
        
        Args:
            options_list: List of options to convert
            
        Returns:
            List of converted beat data options
        """
        try:
            beat_options = []
            beat_data_objects = []
            dict_objects = []
            other_objects = []

            # Categorize objects by type
            for option_data in options_list:
                if isinstance(option_data, BeatData):
                    beat_data_objects.append(option_data)
                elif hasattr(option_data, "get"):
                    dict_objects.append(option_data)
                elif hasattr(option_data, "letter"):
                    other_objects.append(option_data)

            # Add already converted BeatData objects
            beat_options.extend(beat_data_objects)

            # Convert dictionary objects
            if dict_objects and self._conversion_service:
                try:
                    for option_data in dict_objects:
                        beat_data = self._conversion_service.convert_external_pictograph_to_beat_data(
                            option_data
                        )
                        beat_options.append(beat_data)
                except Exception as e:
                    logger.error(f"Error converting dictionary objects: {e}")

            # Add other objects as-is
            beat_options.extend(other_objects)
            
            logger.debug(f"Batch converted {len(options_list)} options to {len(beat_options)} beat data objects")
            return beat_options

        except Exception as e:
            logger.error(f"Error in batch conversion: {e}")
            return options_list  # Return original on error

    def _apply_orientation_updates(
        self, sequence_data: List[Dict[str, Any]], beat_options: List[Any]
    ) -> List[Any]:
        """
        Apply orientation updates to beat options.
        
        Args:
            sequence_data: Sequence data for context
            beat_options: Beat options to update
            
        Returns:
            Updated beat options with correct orientations
        """
        try:
            if not self._orientation_service or not self._conversion_service:
                logger.debug("Orientation or conversion service not available")
                return beat_options

            start_position_dict = sequence_data[-1]
            if not isinstance(start_position_dict, dict) or "letter" not in start_position_dict:
                logger.debug("Invalid start position data for orientation updates")
                return beat_options

            # Convert start position to beat data
            start_beat = self._conversion_service.convert_external_pictograph_to_beat_data(
                start_position_dict
            )

            # Create temporary sequence for orientation calculation
            temp_sequence = SequenceData.empty().update(beats=[start_beat])
            
            # Apply orientation updates
            updated_options = self._orientation_service.update_option_orientations(
                temp_sequence, beat_options
            )
            
            logger.debug(f"Applied orientation updates to {len(beat_options)} options")
            return updated_options

        except Exception as e:
            logger.error(f"Error applying orientation updates: {e}")
            return beat_options  # Return original on error
