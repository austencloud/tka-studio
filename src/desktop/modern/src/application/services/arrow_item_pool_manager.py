"""
Arrow Item Pool Manager

Provides a centralized pool of arrow graphics items that can be shared
across all pictograph scenes for optimal performance.
"""

import logging
from queue import Queue
from threading import Lock
from typing import Dict, List, Optional

from presentation.components.pictograph.graphics_items.arrow_item import ArrowItem

logger = logging.getLogger(__name__)


class ArrowItemPoolManager:
    """
    Centralized manager for arrow graphics item pooling.

    This service provides a shared pool of arrow items that can be used
    by all pictograph scenes, eliminating the need for each scene to
    maintain its own pool.
    """

    def __init__(self):
        """Initialize the arrow item pool manager."""
        self._pools: Dict[str, Queue] = {"blue": Queue(), "red": Queue()}
        self._active_items: Dict[str, List[ArrowItem]] = {"blue": [], "red": []}
        self._lock = Lock()
        self._initialized = False
        self._pool_size_per_color = 20  # Reasonable global pool size

    def initialize_pool(self) -> None:
        """Initialize the global arrow item pool."""
        if self._initialized:
            logger.debug("🏹 [ARROW_POOL] Already initialized")
            return

        logger.info("🏹 [ARROW_POOL] Initializing global arrow item pool...")
        start_time = __import__("time").perf_counter()

        try:
            # Create arrow items without locking to avoid deadlocks during startup
            for color in ["blue", "red"]:
                for i in range(self._pool_size_per_color):
                    arrow_item = ArrowItem()
                    arrow_item.arrow_color = color
                    arrow_item.setVisible(False)
                    self._pools[color].put(arrow_item)

            self._initialized = True
            init_time = (__import__("time").perf_counter() - start_time) * 1000

            total_items = sum(pool.qsize() for pool in self._pools.values())
            logger.info(
                f"✅ [ARROW_POOL] Global pool initialized in {init_time:.1f}ms "
                f"with {total_items} arrow items"
            )

        except Exception as e:
            logger.error(f"❌ [ARROW_POOL] Failed to initialize pool: {e}")
            self._initialized = False

    def checkout_arrow_item(
        self, color: str, scene_id: str = None
    ) -> Optional[ArrowItem]:
        """
        Get an arrow item from the global pool.

        Args:
            color: Arrow color ("blue" or "red")
            scene_id: Optional scene identifier for tracking

        Returns:
            ArrowItem or None if pool is exhausted
        """
        if not self._initialized:
            logger.warning(
                "🏹 [ARROW_POOL] Pool not initialized, creating item on-demand"
            )
            return self._create_arrow_item_on_demand(color)

        with self._lock:
            if not self._pools[color].empty():
                arrow_item = self._pools[color].get()
                self._active_items[color].append(arrow_item)
                arrow_item.setVisible(True)

                logger.debug(
                    f"🔄 [ARROW_POOL] Checked out {color} arrow "
                    f"(pool: {self._pools[color].qsize()}, "
                    f"active: {len(self._active_items[color])})"
                    f"{f' for {scene_id}' if scene_id else ''}"
                )
                return arrow_item
            else:
                logger.warning(
                    f"⚠️ [ARROW_POOL] Pool exhausted for {color}, creating on-demand"
                )
                return self._create_arrow_item_on_demand(color)

    def checkin_arrow_item(self, arrow_item: ArrowItem, scene_id: str = None) -> None:
        """
        Return an arrow item to the global pool.

        Args:
            arrow_item: The arrow item to return
            scene_id: Optional scene identifier for tracking
        """
        if not arrow_item:
            return

        color = getattr(arrow_item, "arrow_color", "unknown")

        with self._lock:
            # Remove from active items
            if color in self._active_items and arrow_item in self._active_items[color]:
                self._active_items[color].remove(arrow_item)

            # Remove from scene if attached
            if arrow_item.scene():
                arrow_item.scene().removeItem(arrow_item)

            # Reset item state
            self._reset_arrow_item(arrow_item)

            # Return to pool if there's space
            if (
                color in self._pools
                and self._pools[color].qsize() < self._pool_size_per_color
            ):
                self._pools[color].put(arrow_item)
                logger.debug(
                    f"🔄 [ARROW_POOL] Returned {color} arrow to pool "
                    f"(pool: {self._pools[color].qsize()})"
                    f"{f' from {scene_id}' if scene_id else ''}"
                )
            else:
                # Pool is full, let item be garbage collected
                logger.debug(f"🗑️ [ARROW_POOL] Pool full, discarding {color} arrow")

    def checkin_all_arrows_for_scene(self, scene_id: str = None) -> None:
        """
        Return all active arrow items to the pool.

        This is useful when clearing a scene or shutting down.

        Args:
            scene_id: Optional scene identifier for tracking
        """
        with self._lock:
            total_returned = 0

            for color in ["blue", "red"]:
                # Make a copy of the list to avoid modification during iteration
                active_items = self._active_items[color].copy()

                for arrow_item in active_items:
                    self.checkin_arrow_item(arrow_item, scene_id)
                    total_returned += 1

            if total_returned > 0:
                logger.debug(
                    f"🔄 [ARROW_POOL] Returned {total_returned} arrows to pool"
                    f"{f' from {scene_id}' if scene_id else ''}"
                )

    def _create_arrow_item_on_demand(self, color: str) -> ArrowItem:
        """Create an arrow item when pool is exhausted."""
        arrow_item = ArrowItem()
        arrow_item.arrow_color = color
        self._active_items[color].append(arrow_item)
        return arrow_item

    def _reset_arrow_item(self, arrow_item: ArrowItem) -> None:
        """Reset arrow item to default state."""
        try:
            arrow_item.setVisible(False)
            arrow_item.setPos(0, 0)
            arrow_item.setRotation(0)
            arrow_item.setScale(1.0)
            arrow_item.setTransform(arrow_item.transform().reset())

            # Clear any renderer
            if hasattr(arrow_item, "setSharedRenderer"):
                arrow_item.setSharedRenderer(None)

        except Exception as e:
            logger.warning(f"⚠️ [ARROW_POOL] Failed to reset arrow item: {e}")

    def get_pool_stats(self) -> Dict[str, int]:
        """Get current pool statistics."""
        with self._lock:
            return {
                "blue_available": self._pools["blue"].qsize(),
                "red_available": self._pools["red"].qsize(),
                "blue_active": len(self._active_items["blue"]),
                "red_active": len(self._active_items["red"]),
                "total_available": sum(pool.qsize() for pool in self._pools.values()),
                "total_active": sum(
                    len(items) for items in self._active_items.values()
                ),
                "initialized": self._initialized,
            }

    def get_pool_info(self) -> str:
        """Get detailed pool information for debugging."""
        stats = self.get_pool_stats()
        return (
            f"Arrow Item Pool Status:\n"
            f"  Initialized: {stats['initialized']}\n"
            f"  Blue: {stats['blue_available']} available, {stats['blue_active']} active\n"
            f"  Red: {stats['red_available']} available, {stats['red_active']} active\n"
            f"  Total: {stats['total_available']} available, {stats['total_active']} active"
        )

    def cleanup(self) -> None:
        """Clean up the pool and release all resources."""
        if not self._initialized:
            return

        logger.debug("🧹 [ARROW_POOL] Cleaning up global arrow item pool...")

        try:
            with self._lock:
                # Return all active items
                self.checkin_all_arrows_for_scene("cleanup")

                # Clear pools without forcing deletion
                for color in ["blue", "red"]:
                    while not self._pools[color].empty():
                        try:
                            self._pools[color].get_nowait()
                        except:
                            break

                    self._active_items[color].clear()

                self._initialized = False
                logger.debug("✅ [ARROW_POOL] Cleanup completed")
        except Exception as e:
            logger.warning(f"⚠️ [ARROW_POOL] Cleanup failed: {e}")

    # Removed __del__ method to prevent premature cleanup during startup
