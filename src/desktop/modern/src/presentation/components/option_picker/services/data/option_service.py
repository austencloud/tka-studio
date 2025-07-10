"""
Option Service - Direct Pictograph Option Management

This service directly uses the PositionMatchingService to get pictograph options
and manages them for the option picker. No unnecessary delegation layers.

ARCHITECTURE:
OptionPicker → OptionService → PositionMatchingService
"""

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from domain.models import PictographData
from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from domain.models import SequenceData

logger = logging.getLogger(__name__)


class OptionService(QObject):
    """
    Service for managing pictograph options.
    
    This service directly uses the PositionMatchingService to manage
    pictograph options for the option picker.
    """
    
    # Signals
    options_loaded = pyqtSignal(list)  # Emitted when new options are loaded
    options_cleared = pyqtSignal()     # Emitted when options are cleared

    def __init__(self):
        """Initialize the option service."""
        super().__init__()
        self._pictograph_options: List[PictographData] = []
        self._position_service = None
        self._initialize_position_service()

    def _initialize_position_service(self):
        """Initialize the position matching service."""
        try:
            from application.services.positioning.arrows.utilities.position_matching_service import (
                PositionMatchingService,
            )
            
            self._position_service = PositionMatchingService()
            logger.debug("Position matching service initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize position service: {e}")
            self._position_service = None

    def load_options_from_sequence(self, sequence_data: List[Dict[str, Any]]) -> List[PictographData]:
        """
        Load pictograph options based on legacy sequence data.
        
        Args:
            sequence_data: Legacy sequence data format
            
        Returns:
            List of pictograph options
        """
        try:
            if not self._position_service:
                logger.warning("Position service not available")
                return self._clear_and_return_empty()

            if not sequence_data:
                logger.debug("No sequence data provided")
                return self._clear_and_return_empty()

            # Extract end position from last beat
            last_beat = sequence_data[-1] if sequence_data else None
            if not last_beat:
                logger.debug("No last beat found in sequence")
                return self._clear_and_return_empty()

            # Get end position from beat data
            end_position = self._extract_end_position_from_beat(last_beat)
            if not end_position:
                logger.debug("Could not extract end position from last beat")
                return self._clear_and_return_empty()

            # Get options from position service
            options = self._position_service.get_next_options(end_position)
            
            # Cache and emit
            self._pictograph_options = options
            self.options_loaded.emit(options)
            
            logger.debug(f"Loaded {len(options)} pictograph options from sequence")
            return options

        except Exception as e:
            logger.error(f"Error loading options from sequence: {e}")
            return self._clear_and_return_empty()

    def load_options_from_modern_sequence(self, sequence: "SequenceData") -> List[PictographData]:
        """
        Load pictograph options based on modern sequence data.
        
        Args:
            sequence: Modern SequenceData object
            
        Returns:
            List of pictograph options
        """
        try:
            if not self._position_service:
                logger.warning("Position service not available")
                return self._clear_and_return_empty()

            if not sequence or sequence.length == 0:
                logger.debug("Empty or invalid sequence provided")
                return self._clear_and_return_empty()

            # Get last beat from sequence
            last_beat = sequence.beats[-1] if sequence.beats else None
            if not last_beat or last_beat.is_blank:
                logger.debug("No valid last beat in sequence")
                return self._clear_and_return_empty()

            # Extract end position from beat data
            end_position = self._extract_end_position_from_modern_beat(last_beat)
            if not end_position:
                logger.debug("Could not extract end position from modern beat")
                return self._clear_and_return_empty()

            # Get options from position service
            options = self._position_service.get_next_options(end_position)
            
            # Cache and emit
            self._pictograph_options = options
            self.options_loaded.emit(options)
            
            logger.debug(f"Loaded {len(options)} pictograph options from modern sequence")
            return options

        except Exception as e:
            logger.error(f"Error loading options from modern sequence: {e}")
            return self._clear_and_return_empty()

    def get_current_options(self) -> List[PictographData]:
        """Get the currently loaded pictograph options."""
        return self._pictograph_options.copy()

    def clear_options(self):
        """Clear all loaded options."""
        self._pictograph_options = []
        self.options_cleared.emit()
        logger.debug("Cleared all pictograph options")

    def get_option_count(self) -> int:
        """Get the number of currently loaded options."""
        return len(self._pictograph_options)

    def get_option_by_index(self, index: int) -> Optional[PictographData]:
        """Get option by index."""
        if 0 <= index < len(self._pictograph_options):
            return self._pictograph_options[index]
        return None

    def filter_options_by_letter(self, letter: str) -> List[PictographData]:
        """Filter current options by letter."""
        return [opt for opt in self._pictograph_options if opt.letter == letter]

    def get_available_letters(self) -> List[str]:
        """Get list of available letters in current options."""
        letters = {opt.letter for opt in self._pictograph_options if opt.letter}
        return sorted(list(letters))

    def _extract_end_position_from_beat(self, beat_data: Dict[str, Any]) -> Optional[str]:
        """Extract end position from legacy beat data."""
        # Try direct end_pos field first
        if "end_pos" in beat_data:
            return beat_data["end_pos"]
            
        # Try to calculate from motion attributes
        try:
            from presentation.components.option_picker.services.data.position_matcher import (
                PositionMatcher,
            )
            
            position_matcher = PositionMatcher()
            return position_matcher.extract_end_position(beat_data, self._position_service)
            
        except Exception as e:
            logger.debug(f"Could not extract end position: {e}")
            return None

    def _extract_end_position_from_modern_beat(self, beat_data) -> Optional[str]:
        """Extract end position from modern beat data."""
        try:
            # Check metadata first
            if hasattr(beat_data, 'metadata') and beat_data.metadata:
                if 'end_position' in beat_data.metadata:
                    return beat_data.metadata['end_position']
                    
            # Try to calculate from motion data
            from presentation.components.option_picker.services.data.position_matcher import (
                PositionMatcher,
            )
            
            position_matcher = PositionMatcher()
            return position_matcher.extract_modern_end_position(beat_data)
            
        except Exception as e:
            logger.debug(f"Could not extract end position from modern beat: {e}")
            return None

    def _clear_and_return_empty(self) -> List[PictographData]:
        """Clear options and return empty list."""
        self._pictograph_options = []
        self.options_cleared.emit()
        return []

    def is_service_available(self) -> bool:
        """Check if the position service is available."""
        return self._position_service is not None
