"""
Prop rendering microservice for pictograph rendering - REFACTORED VERSION

This service now generates framework-agnostic prop render commands instead of
directly manipulating Qt objects. This enables:

- Web service reuse of the same prop logic
- Better testability without Qt dependencies
- Clean separation between business logic and presentation
- Maintained backward compatibility through Qt adapters

ARCHITECTURE:
- Generates PropRenderCommand objects (framework-agnostic)
- Delegates Qt rendering to QtPropRenderingAdapter
- Maintains same public interface for compatibility
"""

from __future__ import annotations

import logging
from pathlib import Path
import sys


# Add project root to path using pathlib (standardized approach)
def _get_project_root() -> Path:
    """Find the TKA project root by looking for pyproject.toml or main.py."""
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / "pyproject.toml").exists() or (parent / "main.py").exists():
            return parent
    # Fallback: assume TKA is 7 levels up from this file
    return current_path.parents[6]


# Add project paths for imports
_project_root = _get_project_root()
sys.path.insert(0, str(_project_root))
sys.path.insert(0, str(_project_root / "src"))

from PyQt6.QtSvgWidgets import QGraphicsSvgItem

# Qt imports for compatibility
from PyQt6.QtWidgets import QGraphicsScene

from desktop.modern.application.adapters.qt_prop_rendering_service_adapter import (
    QtPropRenderingServiceAdapter,
)

# Import framework-agnostic core services (using established import pattern)
from desktop.modern.application.services.core.prop_rendering_service import (
    CorePropRenderingService,
)

# Support dependencies for existing functionality
from desktop.modern.application.services.pictograph.prop_rendering.asset_manager import (
    PropAssetManager,
)
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData


logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)


class PropRenderingService:
    """
    Qt adapter for prop rendering - REFACTORED VERSION

    This service now acts as a Qt adapter that delegates prop rendering to the
    framework-agnostic core services. This provides:

    - Same public interface for existing Qt code compatibility
    - Framework-agnostic business logic for web service reuse
    - Clean separation between Qt presentation and core logic
    - Better testability and maintainability

    Architecture:
    1. Receives Qt prop rendering requests (same interface as before)
    2. Delegates to framework-agnostic core prop service for business logic
    3. Uses Qt adapter to execute render commands on Qt scenes
    """

    def __init__(
        self,
        asset_manager: PropAssetManager,
        # Framework-agnostic dependencies
        core_service: CorePropRenderingService = None,
        qt_adapter: QtPropRenderingServiceAdapter = None,
    ):
        """Initialize the service with framework-agnostic core and Qt adapter."""
        # Keep asset manager for compatibility
        self._asset_manager = asset_manager

        # Framework-agnostic core service for prop rendering logic
        self._core_service = core_service or CorePropRenderingService()

        # Qt adapter for executing render commands
        self._qt_adapter = qt_adapter or QtPropRenderingServiceAdapter()

        logger.info(
            "✅ [PROP_SERVICE] Initialized with framework-agnostic architecture"
        )

    def render_prop(
        self,
        scene: QGraphicsScene,
        color: str,
        motion_data: MotionData,
        pictograph_data: PictographData | None = None,
    ) -> QGraphicsSvgItem | None:
        """
        Render prop to Qt scene - REFACTORED to use framework-agnostic adapter.

        This method maintains the exact same interface as before but now delegates
        to the Qt adapter which uses framework-agnostic core services internally.
        """
        logger.debug(
            f"🎭 [PROP_SERVICE] Delegating {color} prop rendering to Qt adapter"
        )

        # Delegate to Qt adapter (maintains same interface, uses framework-agnostic core)
        return self._qt_adapter.render_prop(scene, color, motion_data, pictograph_data)

    def preload_common_props(self) -> None:
        """Pre-load commonly used prop renderers for better performance."""
        try:
            logger.info("🚀 [PROP_SERVICE] Pre-loading delegated to Qt adapter")
            # The Qt adapter and core service handle their own optimization

        except Exception as e:
            logger.warning(
                f"⚠️ [PROP_SERVICE] Failed to pre-load some prop renderers: {e}"
            )

    def get_supported_colors(self) -> list[str]:
        """Get list of supported prop colors."""
        return self._asset_manager.get_supported_colors()

    def validate_color(self, color: str) -> bool:
        """Validate if the color is supported."""
        return color in self.get_supported_colors()

    def get_prop_stats(self) -> dict:
        """Get prop rendering statistics."""
        return {
            "supported_colors": self.get_supported_colors(),
            "service_status": "active (framework-agnostic adapter)",
            "architecture": "core_service_with_qt_adapter",
        }

    # ============================================================================
    # LEGACY COMPATIBILITY METHODS (Maintained for transition)
    # ============================================================================

    def _get_prop_renderer(self, color: str):
        """DEPRECATED: Direct Qt renderer access - use adapter instead."""
        logger.warning(
            "_get_prop_renderer() is deprecated - using Qt adapter internally"
        )

    def _create_prop_renderer(self, color: str):
        """DEPRECATED: Direct Qt renderer creation - use adapter instead."""
        logger.warning(
            "_create_prop_renderer() is deprecated - using Qt adapter internally"
        )

    def _position_prop(self, prop_item, motion_data, color, pictograph_data=None):
        """DEPRECATED: Direct prop positioning - handled by adapter internally."""
        logger.warning(
            "_position_prop() is deprecated - Qt adapter handles positioning"
        )
        # Qt adapter handles this internally
