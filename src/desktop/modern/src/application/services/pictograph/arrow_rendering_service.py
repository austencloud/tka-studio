"""
Arrow Rendering Service - Pure Business Logic

Handles SVG caching, asset management, color transforms, and positioning
calculations without any Qt dependencies.
"""

import logging
import os
import re
from functools import lru_cache
from typing import TYPE_CHECKING, Dict, Optional, Set, Tuple

from application.services.assets.asset_manager import AssetManager
from core.interfaces.arrow_rendering_services import IArrowRenderingService
from domain.models import Location, MotionData
from domain.models.arrow_data import ArrowData
from domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from application.services.positioning.arrows.orchestration.arrow_positioning_orchestrator import (
        ArrowPositioningOrchestrator,
    )


class ArrowRenderingService(IArrowRenderingService):
    """
    Pure business service for arrow rendering operations.

    Handles asset management, caching, color transformations, and positioning
    calculations without any Qt dependencies.
    """

    # Class-level cache statistics for monitoring
    _cache_stats: Dict[str, int] = {"hits": 0, "misses": 0, "total_files_cached": 0}

    # Track cached files for cache management
    _cached_files: Set[str] = set()

    def __init__(self):
        """Initialize the arrow rendering service."""
        self.asset_manager = AssetManager()

        # Fallback coordinates for when coordinate system service is not available
        self.HAND_RADIUS = 143.1
        self._fallback_location_coordinates = {
            Location.NORTH.value: (0, -self.HAND_RADIUS),
            Location.EAST.value: (self.HAND_RADIUS, 0),
            Location.SOUTH.value: (0, self.HAND_RADIUS),
            Location.WEST.value: (-self.HAND_RADIUS, 0),
            Location.NORTHEAST.value: (
                self.HAND_RADIUS * 0.707,
                -self.HAND_RADIUS * 0.707,
            ),
            Location.SOUTHEAST.value: (
                self.HAND_RADIUS * 0.707,
                self.HAND_RADIUS * 0.707,
            ),
            Location.SOUTHWEST.value: (
                -self.HAND_RADIUS * 0.707,
                self.HAND_RADIUS * 0.707,
            ),
            Location.NORTHWEST.value: (
                -self.HAND_RADIUS * 0.707,
                -self.HAND_RADIUS * 0.707,
            ),
        }

        logger.debug("Arrow rendering service initialized")

    # Asset Management
    def get_arrow_svg_path(self, motion_data: MotionData, color: str) -> str:
        """
        Get the SVG asset path for an arrow.

        Args:
            motion_data: Motion data for the arrow
            color: Color of the arrow

        Returns:
            str: Path to the SVG asset
        """
        return self.asset_manager.get_arrow_asset_path(motion_data, color)

    def get_fallback_arrow_svg_path(self, motion_data: MotionData) -> str:
        """
        Get the fallback SVG asset path for an arrow.

        Args:
            motion_data: Motion data for the arrow

        Returns:
            str: Path to the fallback SVG asset
        """
        return self.asset_manager.get_fallback_arrow_asset_path(motion_data)

    def svg_path_exists(self, path: str) -> bool:
        """
        Check if an SVG path exists.

        Args:
            path: Path to check

        Returns:
            bool: True if path exists
        """
        return os.path.exists(path)

    # Caching Operations
    @lru_cache(maxsize=128)
    def load_cached_svg_data(self, svg_path: str) -> Optional[str]:
        """
        Load and cache SVG data from file.

        Args:
            svg_path: Path to SVG file

        Returns:
            Optional[str]: SVG data if successful, None otherwise
        """
        try:
            self._cache_stats["misses"] += 1
            svg_data = self.asset_manager.load_and_cache_asset(svg_path)
            self._cached_files.add(svg_path)
            self._cache_stats["total_files_cached"] = len(self._cached_files)
            logger.debug(f"Cached SVG data for: {svg_path}")
            return svg_data
        except Exception as e:
            logger.error(f"Failed to load SVG data from {svg_path}: {e}")
            return None

    def apply_color_transformation(self, svg_data: str, color: str) -> str:
        """
        Apply color transformation to SVG data.

        Args:
            svg_data: Original SVG data
            color: Target color

        Returns:
            str: Color-transformed SVG data
        """
        return self.asset_manager.apply_color_transformation(svg_data, color)

    # Position Calculations
    def calculate_arrow_position(
        self,
        arrow_data: ArrowData,
        pictograph_data: Optional[PictographData] = None,
        positioning_orchestrator: "ArrowPositioningOrchestrator" = None,
        coordinate_system=None,
    ) -> Tuple[float, float, float]:
        """
        Calculate arrow position using available positioning services.

        Args:
            arrow_data: Arrow data for positioning
            pictograph_data: Full pictograph data for context
            positioning_orchestrator: Optional positioning orchestrator service
            coordinate_system: Optional coordinate system service

        Returns:
            Tuple[float, float, float]: (x, y, rotation) position data
        """
        logger.info(
            f"🎯 [ARROW_RENDERING_SERVICE] calculate_arrow_position called for {arrow_data.color} arrow"
        )
        logger.info(
            f"🎯 [ARROW_RENDERING_SERVICE] positioning_orchestrator available: {positioning_orchestrator is not None}"
        )
        logger.info(
            f"🎯 [ARROW_RENDERING_SERVICE] pictograph_data available: {pictograph_data is not None}"
        )

        # Use positioning orchestrator if available
        if positioning_orchestrator and pictograph_data:
            try:
                logger.info(
                    f"🎯 [ARROW_RENDERING_SERVICE] Calling positioning orchestrator..."
                )

                # Extract motion data for this arrow
                motion_data = None
                if hasattr(pictograph_data, "motions") and pictograph_data.motions:
                    motion_data = pictograph_data.motions.get(arrow_data.color)
                    logger.info(
                        f"🎯 [ARROW_RENDERING_SERVICE] Found motion data for {arrow_data.color}: {motion_data is not None}"
                    )

                result = positioning_orchestrator.calculate_arrow_position(
                    arrow_data, pictograph_data, motion_data
                )
                logger.info(
                    f"🎯 [ARROW_RENDERING_SERVICE] Orchestrator returned: {result}"
                )
                return result
            except Exception as e:
                logger.error(
                    f"❌ [ARROW_RENDERING_SERVICE] Positioning orchestrator failed: {e}"
                )
                import traceback

                traceback.print_exc()

        # Fallback to basic positioning
        logger.warning(
            f"⚠️ [ARROW_RENDERING_SERVICE] Using fallback arrow positioning (center)"
        )
        return (475.0, 475.0, 0.0)  # Center of scene

    # Cache Management
    @classmethod
    def get_cache_statistics(cls) -> Dict[str, int]:
        """
        Get current cache statistics for monitoring.

        Returns:
            Dict[str, int]: Cache statistics
        """
        # Delegate to AssetManager for actual stats
        asset_stats = AssetManager.get_cache_stats()

        # Combine with our local stats
        combined_stats = cls._cache_stats.copy()
        combined_stats.update(asset_stats)

        return combined_stats

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the SVG file cache and reset statistics."""
        # Clear LRU cache
        cls.load_cached_svg_data.cache_clear()

        # Clear AssetManager cache
        AssetManager.clear_cache()

        # Reset local statistics
        cls._cache_stats = {"hits": 0, "misses": 0, "total_files_cached": 0}
        cls._cached_files.clear()

        logger.info("Arrow rendering cache cleared and statistics reset")

    @classmethod
    def get_cache_info(cls) -> str:
        """
        Get detailed cache information for debugging.

        Returns:
            str: Detailed cache information
        """
        asset_info = AssetManager.get_cache_info()
        lru_info = cls.load_cached_svg_data.cache_info()

        return (
            f"Arrow Rendering Cache Info:\n"
            f"  LRU Cache: {lru_info}\n"
            f"  Local Stats: {cls._cache_stats}\n"
            f"  Asset Manager: {asset_info}"
        )

    # Validation and Utilities
    def validate_motion_visibility(self, motion_data: MotionData) -> bool:
        """
        Validate if a motion should be rendered as visible.

        Args:
            motion_data: Motion data to validate

        Returns:
            bool: True if motion should be visible
        """
        # Note: Static motions with 0 turns should still show arrows in TKA
        # Only filter out if explicitly marked as invisible
        if hasattr(motion_data, "is_visible") and not motion_data.is_visible:
            return False

        return True

    def get_service_summary(self) -> Dict[str, any]:
        """
        Get a summary of the service state.

        Returns:
            Dict: Service state information
        """
        return {
            "cached_files_count": len(self._cached_files),
            "cache_statistics": self._cache_stats,
            "asset_manager_available": self.asset_manager is not None,
            "fallback_coordinates_count": len(self._fallback_location_coordinates),
            "lru_cache_info": self.load_cached_svg_data.cache_info()._asdict(),
        }
