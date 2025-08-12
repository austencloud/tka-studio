"""
Position Resolver

Handles position key parsing and start position mapping logic.
Focused solely on position-related operations and mappings.
"""

import logging
from typing import Any, Optional

from desktop.modern.core.interfaces.data_builder_services import IPositionResolver

logger = logging.getLogger(__name__)


class PositionResolver(IPositionResolver):
    """
    Resolves position keys and manages start position mappings.

    Responsible for:
    - Parsing position keys (e.g., "alpha1_alpha1")
    - Providing available start positions for each grid mode
    - Validating position key formats
    - Converting between position formats
    """

    # Available start positions for each grid mode
    DIAMOND_START_POSITIONS = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
    BOX_START_POSITIONS = ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]

    def parse_position_key(self, position_key: str) -> Optional[tuple[str, str]]:
        """
        Parse a position key into start and end positions.

        Args:
            position_key: Position key like "alpha1_alpha1", "beta5_beta5"

        Returns:
            Tuple of (start_pos, end_pos) or None if invalid format
        """
        if not isinstance(position_key, str):
            logger.warning(f"Position key must be string, got {type(position_key)}")
            return None

        if "_" not in position_key:
            logger.warning(f"Invalid position key format: {position_key}")
            return None

        try:
            parts = position_key.split("_")
            if len(parts) != 2:
                logger.warning(
                    f"Position key must have exactly one underscore: {position_key}"
                )
                return None

            start_pos, end_pos = parts

            if not start_pos or not end_pos:
                logger.warning(f"Position key parts cannot be empty: {position_key}")
                return None

            return start_pos, end_pos

        except Exception as e:
            logger.error(f"Error parsing position key {position_key}: {e}")
            return None

    def get_start_positions(self, grid_mode: str) -> list[str]:
        """
        Get available start position keys for a grid mode.

        Args:
            grid_mode: "diamond" or "box"

        Returns:
            List of available start position keys
        """
        if grid_mode == "diamond":
            return self.DIAMOND_START_POSITIONS.copy()
        elif grid_mode == "box":
            return self.BOX_START_POSITIONS.copy()
        else:
            logger.warning(f"Unknown grid mode: {grid_mode}")
            return []

    # Interface implementation methods
    def resolve_position(self, position_key: str) -> Optional[Any]:
        """Resolve position from key (interface implementation)."""
        start_pos, end_pos = self.parse_position_key(position_key)
        if start_pos and end_pos:
            return {
                "start_position": start_pos,
                "end_position": end_pos,
                "position_key": position_key,
            }
        return None

    def get_valid_positions(self) -> list[str]:
        """Get list of valid position keys (interface implementation)."""
        # Return all diamond positions as default
        return self.get_start_positions("diamond")

    def validate_position_key(self, position_key: str) -> bool:
        """Validate position key format (interface implementation)."""
        try:
            start_pos, end_pos = self.parse_position_key(position_key)
            return start_pos is not None and end_pos is not None
        except Exception:
            return False
