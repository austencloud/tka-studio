"""
Component-specific view pools for optimal performance.

Each component type (option picker, beat frame, etc.) gets its own pool of
pre-sized views to eliminate resizing overhead.
"""

import logging
from queue import Queue
from typing import Dict, Optional, Set, Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsView, QWidget

logger = logging.getLogger(__name__)


class ComponentPictographView(QGraphicsView):
    """
    Component-specific pictograph view with pre-configured sizing.
    """
    
    def __init__(self, component_type: str, size: Tuple[int, int], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.component_type = component_type
        self.target_size = size
        self._setup_view_properties()
        
    def _setup_view_properties(self) -> None:
        """Configure view properties for optimal pictograph display."""
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameStyle(0)
        self.setContentsMargins(0, 0, 0, 0)
        
        viewport = self.viewport()
        if viewport:
            viewport.setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Set fixed size for this component type
        self.setFixedSize(self.target_size[0], self.target_size[1])
        
    def resizeEvent(self, event):
        """Handle resizing and maintain aspect ratio."""
        super().resizeEvent(event)
        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)


class ComponentSpecificViewPool:
    """
    Pool manager for component-specific views.
    """
    
    def __init__(self, component_type: str, view_count: int, view_size: Tuple[int, int]):
        self.component_type = component_type
        self.view_count = view_count
        self.view_size = view_size
        self._pool: Queue[ComponentPictographView] = Queue()
        self._checked_out: Set[ComponentPictographView] = set()
        self._initialized = False
        
    def initialize_pool(self) -> None:
        """Initialize the component-specific view pool."""
        if self._initialized:
            return
            
        logger.info(f"🎯 [{self.component_type}] Initializing view pool with {self.view_count} views ({self.view_size[0]}x{self.view_size[1]})")
        
        # Create pre-sized views for this component
        for i in range(self.view_count):
            view = ComponentPictographView(self.component_type, self.view_size)
            view.hide()  # Keep hidden until needed
            self._pool.put(view)
            
        self._initialized = True
        logger.info(f"✅ [{self.component_type}] View pool initialized with {self._pool.qsize()} views")
        
    def checkout_view(self, parent: Optional[QWidget] = None) -> Optional[ComponentPictographView]:
        """
        Get a pre-sized view from the component pool.
        
        Args:
            parent: Optional parent widget for the view
            
        Returns:
            ComponentPictographView or None if pool is exhausted
        """
        if not self._initialized:
            self.initialize_pool()
            
        if self._pool.empty():
            logger.warning(f"⚠️ [{self.component_type}] Pool exhausted, creating view on-demand")
            view = ComponentPictographView(self.component_type, self.view_size, parent)
            view.hide()
            return view
            
        view = self._pool.get()
        self._checked_out.add(view)
        
        # Set parent if provided
        if parent:
            view.setParent(parent)
            
        logger.debug(f"🔄 [{self.component_type}] Checked out view (pool: {self._pool.qsize()}, out: {len(self._checked_out)})")
        return view
        
    def checkin_view(self, view: ComponentPictographView) -> None:
        """
        Return a view to the component pool.
        
        Args:
            view: The view to return to the pool
        """
        if view not in self._checked_out:
            # Handle on-demand views
            logger.debug(f"🔄 [{self.component_type}] Destroying on-demand view")
            view.setScene(None)
            view.setParent(None)
            view.deleteLater()
            return
            
        # Reset view state
        view.setScene(None)
        view.setParent(None)
        view.hide()
        
        # Return to pool
        self._checked_out.remove(view)
        self._pool.put(view)
        
        logger.debug(f"🔄 [{self.component_type}] Checked in view (pool: {self._pool.qsize()}, out: {len(self._checked_out)})")
        
    def get_pool_stats(self) -> Dict[str, int]:
        """Get current pool statistics."""
        return {
            "pool_size": self._pool.qsize(),
            "checked_out": len(self._checked_out),
            "total_capacity": self.view_count,
            "utilization_percent": int((len(self._checked_out) / self.view_count) * 100) if self.view_count > 0 else 0,
        }
        
    def cleanup_pool(self) -> None:
        """Clean up the pool and all views."""
        logger.info(f"🧹 [{self.component_type}] Cleaning up view pool...")
        
        # Clean up checked out views
        for view in list(self._checked_out):
            self.checkin_view(view)
            
        # Clear the pool
        while not self._pool.empty():
            view = self._pool.get()
            view.setScene(None)
            view.setParent(None)
            view.deleteLater()
            
        self._checked_out.clear()
        self._initialized = False
        
        logger.info(f"✅ [{self.component_type}] View pool cleanup complete")


class ComponentViewPoolManager:
    """
    Manager for all component-specific view pools.
    """
    
    def __init__(self):
        self._component_pools: Dict[str, ComponentSpecificViewPool] = {}
        self._initialized = False
        
    def initialize_all_pools(self) -> None:
        """Initialize all component-specific pools."""
        if self._initialized:
            return
            
        logger.info("🎯 [VIEW_MANAGER] Initializing all component-specific view pools...")
        
        # Define component-specific requirements
        component_specs = {
            "option_picker": {
                "view_count": 36,
                "view_size": (120, 120)  # Small square views for option picker
            },
            "start_position_picker": {
                "view_count": 19,
                "view_size": (100, 100)  # Small views for start positions
            },
            "beat_frame": {
                "view_count": 64,
                "view_size": (150, 150)  # Medium views for beat frame
            },
            "graph_editor": {
                "view_count": 1,
                "view_size": (400, 400)  # Large view for graph editor
            },
            "preview": {
                "view_count": 5,
                "view_size": (200, 200)  # Medium views for previews
            }
        }
        
        # Create pools for each component
        for component_type, spec in component_specs.items():
            pool = ComponentSpecificViewPool(
                component_type=component_type,
                view_count=spec["view_count"],
                view_size=spec["view_size"]
            )
            pool.initialize_pool()
            self._component_pools[component_type] = pool
            
        self._initialized = True
        logger.info("✅ [VIEW_MANAGER] All component-specific view pools initialized")
        
    def get_pool(self, component_type: str) -> Optional[ComponentSpecificViewPool]:
        """Get the pool for a specific component type."""
        if not self._initialized:
            self.initialize_all_pools()
            
        return self._component_pools.get(component_type)
        
    def cleanup_all_pools(self) -> None:
        """Clean up all component pools."""
        logger.info("🧹 [VIEW_MANAGER] Cleaning up all component view pools...")
        
        for pool in self._component_pools.values():
            pool.cleanup_pool()
            
        self._component_pools.clear()
        self._initialized = False
        
        logger.info("✅ [VIEW_MANAGER] All component view pools cleaned up")
        
    def get_all_stats(self) -> Dict[str, Dict[str, int]]:
        """Get statistics for all component pools."""
        stats = {}
        for component_type, pool in self._component_pools.items():
            stats[component_type] = pool.get_pool_stats()
        return stats


# Global pool manager instance
_global_view_manager: Optional[ComponentViewPoolManager] = None


def get_component_view_manager() -> ComponentViewPoolManager:
    """Get the global component view pool manager."""
    global _global_view_manager
    if _global_view_manager is None:
        _global_view_manager = ComponentViewPoolManager()
    return _global_view_manager


def initialize_component_view_pools() -> None:
    """Initialize all component-specific view pools."""
    manager = get_component_view_manager()
    manager.initialize_all_pools()


def get_component_view_pool(component_type: str) -> Optional[ComponentSpecificViewPool]:
    """Get the view pool for a specific component type."""
    manager = get_component_view_manager()
    return manager.get_pool(component_type)


# Convenience functions for specific components
def get_option_picker_view_pool() -> Optional[ComponentSpecificViewPool]:
    """Get the option picker view pool."""
    return get_component_view_pool("option_picker")


def get_beat_frame_view_pool() -> Optional[ComponentSpecificViewPool]:
    """Get the beat frame view pool."""
    return get_component_view_pool("beat_frame")


def get_start_position_picker_view_pool() -> Optional[ComponentSpecificViewPool]:
    """Get the start position picker view pool."""
    return get_component_view_pool("start_position_picker")


def get_graph_editor_view_pool() -> Optional[ComponentSpecificViewPool]:
    """Get the graph editor view pool."""
    return get_component_view_pool("graph_editor")


def get_preview_view_pool() -> Optional[ComponentSpecificViewPool]:
    """Get the preview view pool."""
    return get_component_view_pool("preview")
