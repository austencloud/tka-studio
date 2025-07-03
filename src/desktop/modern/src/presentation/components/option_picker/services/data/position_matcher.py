"""
Position Matcher - UI Adapter for Position Matching

This is now a thin UI adapter that delegates business logic to the
PositionMatchingService. It maintains backward compatibility while
using the extracted business service.
"""

import logging
from typing import TYPE_CHECKING, Any, Dict, Optional

from core.interfaces.positioning_services import IPositionMatchingService

if TYPE_CHECKING:
    from application.services.positioning.arrows.utilities.position_matching_service import (
        PositionMatchingService,
    )
    from domain.models.core_models import BeatData

logger = logging.getLogger(__name__)


class PositionMatcher:
    """
    UI adapter for position matching logic.

    This class now delegates all business logic to the IPositionMatchingService
    while maintaining the same public interface for backward compatibility.
    """

    def __init__(self, position_service: Optional[IPositionMatchingService] = None):
        """
        Initialize position matcher with injected business service.

        Args:
            position_service: Injected position matching service
        """
        self._position_service = position_service

        # Fallback for legacy compatibility - will be removed in future versions
        if not self._position_service:
            try:
                from application.services.positioning.position_matching_service import (
                    PositionMatchingService,
                )

                self._position_service = PositionMatchingService()
                logger.warning(
                    "Using fallback position service - consider using DI container"
                )
            except ImportError:
                logger.error("Position matching service not available")
                self._position_service = None

    def extract_end_position(
        self, last_beat: Dict[str, Any], position_service: "PositionMatchingService"
    ) -> Optional[str]:
        """
        Extract end position from last beat data using Legacy-compatible logic.

        Args:
            last_beat: Beat data dictionary in legacy format
            position_service: Legacy position service (ignored, using injected service)

        Returns:
            End position string if found, None otherwise
        """
        if not self._position_service:
            logger.error("Position service not available")
            return None

        # Delegate to business service
        return self._position_service.extract_end_position(last_beat)

    def extract_modern_end_position(self, beat_data: "BeatData") -> Optional[str]:
        """
        Extract end position directly from Modern BeatData.

        Args:
            beat_data: Modern BeatData object

        Returns:
            End position string if found, None otherwise
        """
        if not self._position_service:
            logger.error("Position service not available")
            return "beta5"  # Safe fallback

        # Delegate to business service
        return self._position_service.extract_modern_end_position(beat_data)

    def has_motion_attributes(self, beat_data: Dict[str, Any]) -> bool:
        """
        Check if beat data has motion attributes for end position calculation.

        Args:
            beat_data: Beat data dictionary to check

        Returns:
            True if motion attributes are present, False otherwise
        """
        if not self._position_service:
            logger.error("Position service not available")
            return False

        # Delegate to business service
        return self._position_service.has_motion_attributes(beat_data)

    def get_position_from_locations(
        self, start_loc: str, end_loc: str
    ) -> Optional[str]:
        """
        Get position key from start and end locations.

        Args:
            start_loc: Start location string
            end_loc: End location string

        Returns:
            Position key if mapping exists, None otherwise
        """
        if not self._position_service:
            logger.error("Position service not available")
            return None

        # Delegate to business service
        return self._position_service.get_position_from_locations(start_loc, end_loc)
