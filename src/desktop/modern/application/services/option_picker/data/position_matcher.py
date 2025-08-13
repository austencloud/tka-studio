"""
Position Matcher - UI Adapter for Position Matching

This is now a thin UI adapter that delegates business logic to the
PositionMatchingService. It maintains backward compatibility while
using the extracted business service.
"""

import logging
from typing import TYPE_CHECKING, Any

from desktop.modern.core.interfaces.positioning_services import IPositionMapper

if TYPE_CHECKING:
    from desktop.modern.application.services.positioning.arrows.utilities.pictograph_position_matcher import (
        PictographPositionMatcher,
    )
    from desktop.modern.domain.models import BeatData

logger = logging.getLogger(__name__)


class PositionMatcher:
    """
    UI adapter for position matching logic.

    This class now delegates all business logic to the IPositionMatchingService
    while maintaining the same public interface for backward compatibility.
    """

    def __init__(self, position_service: IPositionMapper):
        """
        Initialize position matcher with injected business service.

        Args:
            position_service: Required injected position matching service
        """
        if not position_service:
            raise ValueError(
                "Position service is required and must be injected via DI container"
            )

        self._position_service = position_service

    def extract_end_position(
        self, last_beat: dict[str, Any], position_service: "PictographPositionMatcher"
    ) -> str | None:
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

    def extract_modern_end_position(self, beat_data: "BeatData") -> str | None:
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

    def has_motion_attributes(self, beat_data: dict[str, Any]) -> bool:
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

    def get_position_from_locations(self, start_loc: str, end_loc: str) -> str | None:
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
