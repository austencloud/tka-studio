"""
Position Resolver

Handles position key parsing and start position mapping logic.
Focused solely on position-related operations and mappings.
"""

import logging
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


class PositionResolver:
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

    def parse_position_key(self, position_key: str) -> Optional[Tuple[str, str]]:
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
                logger.warning(f"Position key must have exactly one underscore: {position_key}")
                return None
                
            start_pos, end_pos = parts
            
            if not start_pos or not end_pos:
                logger.warning(f"Position key parts cannot be empty: {position_key}")
                return None
                
            return start_pos, end_pos
            
        except Exception as e:
            logger.error(f"Error parsing position key {position_key}: {e}")
            return None

    def is_start_position_key(self, position_key: str) -> bool:
        """
        Check if a position key represents a start position (start == end).
        
        Args:
            position_key: Position key to check
            
        Returns:
            True if it's a start position key
        """
        parsed = self.parse_position_key(position_key)
        if not parsed:
            return False
            
        start_pos, end_pos = parsed
        return start_pos == end_pos

    def get_start_positions(self, grid_mode: str) -> List[str]:
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

    def get_all_start_positions(self) -> dict:
        """
        Get all available start positions for all grid modes.
        
        Returns:
            Dictionary mapping grid modes to their start positions
        """
        return {
            "diamond": self.get_start_positions("diamond"),
            "box": self.get_start_positions("box"),
        }

    def is_valid_start_position(self, position_key: str, grid_mode: str) -> bool:
        """
        Check if a position key is a valid start position for the given grid mode.
        
        Args:
            position_key: Position key to validate
            grid_mode: "diamond" or "box"
            
        Returns:
            True if it's a valid start position for the grid mode
        """
        if not self.is_start_position_key(position_key):
            return False
            
        valid_positions = self.get_start_positions(grid_mode)
        return position_key in valid_positions

    def normalize_position_key(self, position_key: str) -> Optional[str]:
        """
        Normalize a position key to ensure consistent format.
        
        Args:
            position_key: Position key to normalize
            
        Returns:
            Normalized position key or None if invalid
        """
        parsed = self.parse_position_key(position_key)
        if not parsed:
            return None
            
        start_pos, end_pos = parsed
        return f"{start_pos.strip()}_{end_pos.strip()}"

    def extract_base_position(self, position_key: str) -> Optional[str]:
        """
        Extract the base position from a position key.
        
        For start positions like "alpha1_alpha1", returns "alpha1".
        For movement positions like "alpha1_beta5", returns the start position "alpha1".
        
        Args:
            position_key: Position key to extract from
            
        Returns:
            Base position string or None if invalid
        """
        parsed = self.parse_position_key(position_key)
        if not parsed:
            return None
            
        start_pos, _ = parsed
        return start_pos

    def extract_end_position(self, position_key: str) -> Optional[str]:
        """
        Extract the end position from a position key.
        
        Args:
            position_key: Position key to extract from
            
        Returns:
            End position string or None if invalid
        """
        parsed = self.parse_position_key(position_key)
        if not parsed:
            return None
            
        _, end_pos = parsed
        return end_pos

    def create_position_key(self, start_pos: str, end_pos: str) -> str:
        """
        Create a position key from start and end positions.
        
        Args:
            start_pos: Start position
            end_pos: End position
            
        Returns:
            Formatted position key
        """
        return f"{start_pos}_{end_pos}"

    def get_position_info(self, position_key: str) -> dict:
        """
        Get detailed information about a position key.
        
        Args:
            position_key: Position key to analyze
            
        Returns:
            Dictionary with position information
        """
        parsed = self.parse_position_key(position_key)
        if not parsed:
            return {
                "valid": False,
                "error": "Invalid position key format"
            }
            
        start_pos, end_pos = parsed
        is_start_position = start_pos == end_pos
        
        # Check which grid modes this position is valid for
        valid_for_diamond = self.is_valid_start_position(position_key, "diamond") if is_start_position else False
        valid_for_box = self.is_valid_start_position(position_key, "box") if is_start_position else False
        
        return {
            "valid": True,
            "start_position": start_pos,
            "end_position": end_pos,
            "is_start_position": is_start_position,
            "valid_for_diamond": valid_for_diamond,
            "valid_for_box": valid_for_box,
            "normalized": self.normalize_position_key(position_key),
        }
