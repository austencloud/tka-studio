"""
Arrow Rendering Service - Pure Business Logic

Handles SVG caching, asset management, color transforms, and positioning
calculations without any Qt dependencies.
"""

import logging
from functools import lru_cache

from desktop.modern.core.interfaces.arrow_rendering_services import (
    IArrowRenderingService,
)
from desktop.modern.domain.models import MotionData
from shared.application.services.assets.asset_manager import AssetManager

logger = logging.getLogger(__name__)


class ArrowRenderingService(IArrowRenderingService):
    """
    Pure business service for arrow rendering operations.

    Handles asset management, caching, color transformations, and positioning
    calculations without any Qt dependencies.
    """

    _cached_files: set[str] = set()

    def __init__(
        self,
        asset_manager: AssetManager | None = None,
    ):
        self.asset_manager = asset_manager or AssetManager()

    # Caching Operations
    @lru_cache(maxsize=128)
    def load_cached_svg_data(self, svg_path: str) -> str | None:
        try:
            svg_data = self.asset_manager.load_and_cache_asset(svg_path)
            self._cached_files.add(svg_path)
            logger.debug(f"Cached SVG data for: {svg_path}")
            return svg_data
        except Exception as e:
            logger.error(f"Failed to load SVG data from {svg_path}: {e}")
            return None

    def validate_motion_visibility(self, motion_data: MotionData) -> bool:
        if hasattr(motion_data, "is_visible") and not motion_data.is_visible:
            return False
        return True
