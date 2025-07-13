"""
Pictograph Pool Manager for high-performance option picker.

This service manages a pool of pre-created PictographComponent instances
to avoid the expensive creation/destruction cycle during option loading.
"""

import logging
import threading
from queue import Queue
from typing import Dict, List, Optional, Set

from core.dependency_injection.di_container import DIContainer
from domain.models.pictograph_data import PictographData
from presentation.components.pictograph.pictograph_component import (
    PictographComponent,
    create_pictograph_component,
)

logger = logging.getLogger(__name__)


class PictographPoolManager:
    """Manages a pool of reusable PictographComponent instances for performance."""

    def __init__(self, container: Optional[DIContainer] = None):
        self.container = container
        self._pool: Queue[PictographComponent] = Queue()
        self._checked_out: Set[PictographComponent] = set()
        self._pool_size = 50  # Pre-create 50 components to match option picker frames
        self._lock = threading.Lock()
        self._initialized = False

    def initialize_pool(self) -> None:
        """Initialize the pictograph pool with pre-created components (public method)."""
        with self._lock:
            self._initialize_pool_internal()

    def _initialize_pool_internal(self) -> None:
        """Internal pool initialization method (called with lock held)."""
        if self._initialized:
            logger.debug("🏊 [POOL] Pool already initialized")
            return

        logger.info(
            f"🏊 [POOL] Initializing pictograph pool with {self._pool_size} components..."
        )

        import time

        start_time = time.perf_counter()

        # Pre-create components
        for i in range(self._pool_size):
            try:
                component = create_pictograph_component(container=self.container)
                # Set a reasonable default size
                component.setFixedSize(100, 100)
                # Hide initially
                component.setVisible(False)
                self._pool.put(component)

                if i % 10 == 0:  # Log progress every 10 components
                    logger.debug(
                        f"🏊 [POOL] Created {i+1}/{self._pool_size} components"
                    )

            except Exception as e:
                logger.error(f"❌ [POOL] Failed to create component {i}: {e}")

        init_time = (time.perf_counter() - start_time) * 1000
        logger.info(
            f"✅ [POOL] Pool initialized in {init_time:.1f}ms with {self._pool.qsize()} components"
        )
        self._initialized = True

    def checkout_pictograph(self, parent=None) -> Optional[PictographComponent]:
        """
        Get an available pictograph component from the pool.

        Args:
            parent: Optional parent widget for the component

        Returns:
            PictographComponent or None if pool is exhausted
        """
        with self._lock:
            if not self._initialized:
                logger.info("🔧 [POOL] Auto-initializing pool on first use...")
                self._initialize_pool_internal()

            if not self._initialized:
                logger.warning(
                    "⚠️ [POOL] Pool initialization failed, creating component on-demand"
                )
                return create_pictograph_component(
                    parent=parent, container=self.container
                )

            if self._pool.empty():
                logger.warning("⚠️ [POOL] Pool exhausted, creating component on-demand")
                return create_pictograph_component(
                    parent=parent, container=self.container
                )

            component = self._pool.get()
            self._checked_out.add(component)

            # Set parent if provided
            if parent:
                component.setParent(parent)

            # Make component visible (components are hidden during pool initialization)
            # This is necessary but much faster than calling show()
            component.setVisible(True)

            # Only log in debug mode to avoid string formatting overhead
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(
                    f"🔄 [POOL] Checked out component (pool: {self._pool.qsize()}, out: {len(self._checked_out)})"
                )
            return component

    def checkin_pictograph(self, component: PictographComponent) -> None:
        """Return a pictograph component to the pool."""
        with self._lock:
            if component not in self._checked_out:
                logger.warning(
                    "⚠️ [POOL] Attempting to check in component not from pool"
                )
                return

            # Reset component state (minimal operations for performance)
            component.setParent(None)
            component.setVisible(False)
            # Clear any pictograph data
            if hasattr(component, "scene") and component.scene:
                component.scene.clear()

            self._checked_out.remove(component)
            self._pool.put(component)

            # Only log in debug mode to avoid overhead
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(
                    f"🔄 [POOL] Checked in component (pool: {self._pool.qsize()}, out: {len(self._checked_out)})"
                )

    def get_pool_stats(self) -> Dict[str, int]:
        """Get current pool statistics."""
        with self._lock:
            return {
                "pool_size": self._pool.qsize(),
                "checked_out": len(self._checked_out),
                "total_capacity": self._pool_size,
                "utilization_percent": int(
                    (len(self._checked_out) / self._pool_size) * 100
                ),
            }

    def cleanup_pool(self) -> None:
        """Clean up the pool and all components."""
        with self._lock:
            logger.info("🧹 [POOL] Cleaning up pictograph pool...")

            # Return all checked out components
            for component in list(self._checked_out):
                self.checkin_pictograph(component)

            # Clear the pool
            while not self._pool.empty():
                component = self._pool.get()
                component.deleteLater()

            self._checked_out.clear()
            self._initialized = False

            logger.info("✅ [POOL] Pool cleanup complete")


# Global pool instance
_global_pool: Optional[PictographPoolManager] = None


def get_pictograph_pool(
    container: Optional[DIContainer] = None,
) -> PictographPoolManager:
    """Get the global pictograph pool instance."""
    global _global_pool
    if _global_pool is None:
        _global_pool = PictographPoolManager(container)
    return _global_pool


def initialize_pictograph_pool(container: Optional[DIContainer] = None) -> None:
    """Initialize the global pictograph pool."""
    pool = get_pictograph_pool(container)
    pool.initialize_pool()
