"""
Pictograph Pool Manager for high-performance option picker.

This service manages a pool of pre-created PictographComponent instances
to avoid the expensive creation/destruction cycle during option loading.
"""

import logging
import threading
from queue import Queue
from typing import Any, Dict, List, Optional, Set

from core.dependency_injection.di_container import DIContainer
from core.interfaces.pool_manager_services import IPictographPoolManager
from domain.models.pictograph_data import PictographData
from presentation.components.pictograph.simplified_pictograph import (
    SimplifiedPictographWidget,
    create_simplified_pictograph_widget,
)
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)


class PictographPoolManager(IPictographPoolManager):
    """Manages a pool of reusable PictographComponent instances for performance."""

    def __init__(self, container: Optional[DIContainer] = None):
        self.container = container
        self._pool: Queue[SimplifiedPictographWidget] = Queue()
        self._checked_out: Set[SimplifiedPictographWidget] = set()
        self._on_demand_components: Set[SimplifiedPictographWidget] = (
            set()
        )  # Track on-demand components
        # PERFORMANCE OPTIMIZATION: Increased pool size to handle option picker demand
        # Option picker needs 50 widgets, so pool must be larger
        self._initial_pool_size = (
            60  # Increased to handle option picker (50) + other components
        )
        self._max_pool_size = 100  # Restore original working size

        self._lock = threading.Lock()
        self._initialized = False
        self._lazy_initialization = True  # Enable lazy initialization by default
        self._progress_callback = None  # Progress callback for initialization
        self._background_initialization_started = False
        self._startup_complete = False  # Track if startup is complete
        self._expansion_in_progress = False  # Prevent infinite expansion loops

    def initialize_pool(self, progress_callback=None, lazy=None) -> None:
        """Initialize the pictograph pool with pre-created components (public method)."""
        from presentation.components.pictograph.component_specific_view_pools import (
            initialize_component_view_pools,
        )

        # Initialize component-specific view pools
        initialize_component_view_pools()
        self._progress_callback = progress_callback

        # Use lazy initialization setting if not explicitly specified
        if lazy is None:
            lazy = self._lazy_initialization

        if lazy:
            # Lazy initialization: create minimal pool and defer the rest
            self._initialize_minimal_pool()
            # DISABLED: Background initialization causes 30+ second delays
            # self._start_background_initialization()
        else:
            # Full initialization during startup (original behavior)
            with self._lock:
                self._initialize_pool_internal()

    def _initialize_minimal_pool(self) -> None:
        """Initialize full pool during startup to eliminate on-demand creation."""
        with self._lock:
            if self._initialized:
                return

            logger.info(
                f"🏊 [POOL] Initializing full pictograph pool ({self._initial_pool_size} components) to eliminate on-demand creation..."
            )

            # AGGRESSIVE OPTIMIZATION: Create full pool during splash to prevent option picker delays
            self._create_pool_components(
                self._initial_pool_size, progress_range=(57, 58)
            )

            self._initialized = True
            logger.info(
                f"✅ [POOL] Full pool ready with {self._pool.qsize()} components - no on-demand creation needed"
            )

    def _start_background_initialization(self) -> None:
        """Start background initialization of the remaining pool components."""
        if self._background_initialization_started:
            return

        self._background_initialization_started = True

        # THREADING FIX: Use QTimer to run on main thread instead of background thread
        from PyQt6.QtCore import QTimer

        def main_thread_init():
            """Main thread function to complete pool initialization."""
            try:
                with self._lock:
                    remaining_size = self._initial_pool_size - self._pool.qsize()
                    if remaining_size > 0:
                        logger.info(
                            f"🏊 [POOL] Background initialization of {remaining_size} components..."
                        )
                        self._create_pool_components(
                            remaining_size, progress_range=(58, 59)
                        )
                        logger.info(
                            f"✅ [POOL] Background initialization complete. Pool size: {self._pool.qsize()}"
                        )
            except Exception as e:
                logger.error(f"❌ [POOL] Background initialization failed: {e}")

        # Schedule on main thread with 500ms delay to let UI settle
        QTimer.singleShot(500, main_thread_init)

    def _initialize_pool_internal(self) -> None:
        """Internal pool initialization method (called with lock held)."""
        if self._initialized:
            logger.debug("🏊 [POOL] Pool already initialized")
            return

        logger.info(
            f"🏊 [POOL] Initializing pictograph pool with {self._initial_pool_size} components..."
        )

        # Create the full initial pool
        self._create_pool_components(self._initial_pool_size, progress_range=(57, 59))
        self._initialized = True

    def _create_pool_components(
        self, count: int, progress_range: tuple = (57, 59)
    ) -> None:
        """Create a specified number of pool components with progress reporting."""
        if count <= 0:
            return

        import time

        start_time = time.perf_counter()
        start_progress, end_progress = progress_range

        # Report initialization start
        if self._progress_callback:
            self._progress_callback(
                start_progress, f"Creating {count} pictograph components..."
            )

        # Pre-create lightweight components (scenes only)
        created_count = 0
        for i in range(count):
            try:
                # Create lightweight widget (scene + view wrapper)
                component = create_simplified_pictograph_widget()
                self._pool.put(component)
                created_count += 1

                # Enhanced progress reporting every 5 components for smoother feedback
                if i % 5 == 0 or i == count - 1:
                    progress_percent = int(
                        start_progress
                        + (i + 1) / count * (end_progress - start_progress)
                    )
                    if self._progress_callback:
                        self._progress_callback(
                            progress_percent,
                            f"Created {created_count}/{count} lightweight components",
                        )

                    logger.debug(
                        f"🏊 [POOL] Created {created_count}/{count} lightweight components"
                    )

            except Exception as e:
                logger.error(f"❌ [POOL] Failed to create component {i}: {e}")

        init_time = (time.perf_counter() - start_time) * 1000

        # Report completion
        if self._progress_callback:
            self._progress_callback(end_progress, f"Created {created_count} components")

        logger.info(
            f"✅ [POOL] Created {created_count} lightweight components in {init_time:.1f}ms. Pool size: {self._pool.qsize()}"
        )

    def mark_startup_complete(self) -> None:
        """Mark startup as complete to allow pool expansion."""
        self._startup_complete = True
        logger.info("🏊 [POOL] Startup complete - pool expansion now enabled")

    def checkout_pictograph(self, parent=None) -> Optional[SimplifiedPictographWidget]:
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
                component = create_simplified_pictograph_widget()
                self._on_demand_components.add(component)
                return component

            if self._pool.empty():
                # SIMPLIFIED: Only expand if we have very few components and startup is complete
                total_created = (
                    len(self._checked_out)
                    + len(self._on_demand_components)
                    + self._pool.qsize()
                )
                # CRITICAL FIX: Disable automatic pool expansion to prevent post-startup freezing
                # Pool expansion was causing 30+ second delays after "Application ready"
                if False:  # Completely disable automatic expansion
                    self._expansion_in_progress = True
                    try:
                        expand_count = min(
                            10, self._max_pool_size - total_created
                        )  # Reasonable expansion for functionality
                        if expand_count > 0:
                            logger.info(
                                f"🏊 [POOL] Expanding pool by {expand_count} components (total: {total_created}/{self._max_pool_size})..."
                            )
                            self._create_pool_components(
                                expand_count, progress_range=(0, 0)
                            )  # No progress callback for expansion
                    finally:
                        self._expansion_in_progress = False

                    # Try to get component from expanded pool
                    if not self._pool.empty():
                        component = self._pool.get()
                        self._checked_out.add(component)

                        # Set parent and configure component
                        if parent:
                            component.setParent(parent)
                            component.setWindowFlags(Qt.WindowType.Widget)
                            component.setAttribute(
                                Qt.WidgetAttribute.WA_DontShowOnScreen, False
                            )

                        logger.debug(
                            f"🏊 [POOL] Checked out component from expanded pool"
                        )
                        return component

                # Pool still empty or at max size, create on-demand
                logger.warning("⚠️ [POOL] Pool exhausted, creating component on-demand")
                component = create_simplified_pictograph_widget()
                self._on_demand_components.add(component)
                return component

            component = self._pool.get()
            self._checked_out.add(component)

            # Component is now lightweight scene - no need for parenting or visibility

            # Only log in debug mode to avoid string formatting overhead
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(
                    f"🔄 [POOL] Checked out component (pool: {self._pool.qsize()}, out: {len(self._checked_out)})"
                )
            return component

    def checkin_pictograph(self, component: SimplifiedPictographWidget) -> None:
        """Return a pictograph component to the pool."""
        with self._lock:
            # Check if it's an on-demand component first
            if component in self._on_demand_components:
                logger.debug("🔄 [POOL] Destroying on-demand component")
                self._on_demand_components.remove(component)
                try:
                    component.cleanup()
                except Exception as e:
                    logger.warning(f"Error destroying on-demand component: {e}")
                return

            if component not in self._checked_out:
                logger.warning(
                    "⚠️ [POOL] Attempting to check in component not from pool - destroying it"
                )
                # For unknown components, just destroy them
                try:
                    component.cleanup()
                except Exception as e:
                    logger.warning(f"Error destroying unknown component: {e}")
                return

            # Reset component state (minimal operations for performance)
            # Component is now lightweight scene - just clear the data
            component.clear()

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
                "total_capacity": self._initial_pool_size,
                "utilization_percent": (
                    int((len(self._checked_out) / self._initial_pool_size) * 100)
                    if self._initial_pool_size > 0
                    else 0
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
                component.cleanup()

            self._checked_out.clear()
            self._initialized = False

            logger.info("✅ [POOL] Pool cleanup complete")

    # Interface implementation methods
    def get_pictograph(self, pictograph_data: Any) -> Any:
        """Get pictograph from pool (interface implementation)."""
        return self.checkout_pictograph(pictograph_data)

    def return_pictograph(self, pictograph: Any) -> None:
        """Return pictograph to pool (interface implementation)."""
        self.checkin_pictograph(pictograph)

    def preload_pictographs(self, pictograph_types: List[str], count: int) -> None:
        """Preload pictographs into pool (interface implementation)."""
        # Current implementation already preloads during initialization
        # This could be extended to support dynamic preloading
        if not self._initialized:
            self.initialize_pool()

    def get_pictograph_count(self) -> int:
        """Get total count of pictographs in pool (interface implementation)."""
        with self._lock:
            return self._pool.qsize()

    def clear_pictographs(self) -> None:
        """Clear all pictographs from pool (interface implementation)."""
        self.cleanup()

    def reset_pictograph(self, pictograph: Any) -> None:
        """Reset pictograph to default state (interface implementation)."""
        if pictograph and hasattr(pictograph, "reset"):
            pictograph.reset()

    def configure_pictograph(self, pictograph: Any, config: Dict[str, Any]) -> None:
        """Configure pictograph with properties (interface implementation)."""
        if not pictograph:
            return

        # Apply configuration properties
        for key, value in config.items():
            if key == "position":
                pictograph.setPos(value[0], value[1])
            elif key == "rotation":
                pictograph.setRotation(value)
            elif key == "scale":
                pictograph.setScale(value)
            elif key == "visible":
                pictograph.setVisible(value)
            elif key == "opacity":
                pictograph.setOpacity(value)


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
