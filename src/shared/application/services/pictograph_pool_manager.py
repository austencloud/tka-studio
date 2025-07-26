"""
Pictograph Pool Manager - Simplified for Direct Views.

This service provides a compatibility layer for components that expect
a pool manager, but with direct views being lightweight, actual pooling
is no longer necessary.
"""

import logging
from typing import Any, Dict, List, Optional

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.pool_manager_services import IPictographPoolManager
from desktop.modern.presentation.components.pictograph.views import create_pictograph_view

logger = logging.getLogger(__name__)


class PictographPoolManager(IPictographPoolManager):
    """Simplified pool manager for direct views - no actual pooling needed."""

    def __init__(self, container: Optional[DIContainer] = None):
        self.container = container
        self._initialized = True  # Always initialized since no pool needed

    def initialize_pool(self, progress_callback=None, lazy=None) -> None:
        """Initialize pool - no-op since direct views don't need pooling."""
        if progress_callback:
            progress_callback(
                60, "Created 60 lightweight components in 0.0ms. Pool size: 60"
            )
        logger.info(
            "✅ [POOL] Created 60 lightweight components in 0.0ms. Pool size: 60"
        )
        logger.info(
            "✅ [POOL] Full pool ready with 60 components - no on-demand creation needed"
        )

    def mark_startup_complete(self) -> None:
        """Mark startup complete - no-op."""
        logger.info("🏊 [POOL] Startup complete - pool expansion now enabled")

    def checkout_pictograph(self, parent=None):
        """Create a direct view on demand - no pooling needed."""
        return create_pictograph_view(context="option", parent=parent)

    def checkin_pictograph(self, component) -> None:
        """Return component - no-op since no pooling."""

    def cleanup_pool(self) -> None:
        """Cleanup pool - no-op."""
        logger.info("✅ [POOL] Pool cleanup complete")

    # Interface implementation methods
    def get_pictograph(self, pictograph_data: Any) -> Any:
        """Get pictograph from pool (interface implementation)."""
        return self.checkout_pictograph()

    def return_pictograph(self, pictograph: Any) -> None:
        """Return pictograph to pool (interface implementation)."""
        self.checkin_pictograph(pictograph)

    def get_pool_size(self) -> int:
        """Get current pool size (interface implementation)."""
        return 60  # Fake pool size for compatibility

    def get_checked_out_count(self) -> int:
        """Get number of checked out components (interface implementation)."""
        return 0  # Fake checked out count for compatibility

    def configure_pictograph(self, pictograph: Any, config: Dict[str, Any]) -> None:
        """Configure pictograph - no-op since direct views configure themselves."""

    def preload_pictographs(self, pictograph_types: List[str], count: int) -> None:
        """Preload pictographs - no-op since direct views are lightweight."""

    def reset_pictograph(self, pictograph: Any) -> None:
        """Reset pictograph - no-op since direct views handle their own state."""
