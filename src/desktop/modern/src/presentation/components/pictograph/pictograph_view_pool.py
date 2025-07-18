"""
Pictograph View Pool for high-performance display management.

This service manages a pool of reusable QGraphicsView instances to eliminate
the expensive view creation/destruction cycle. Views are lightweight and can
be attached to different scenes as needed.
"""

import logging
from queue import Queue
from typing import Dict, Optional, Set

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsView, QWidget

logger = logging.getLogger(__name__)


class PictographView(QGraphicsView):
    """
    Optimized pictograph view for pool management.
    
    This view can be attached to different scenes and reused efficiently.
    """
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
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
        
    def resizeEvent(self, event):
        """Handle resizing and maintain aspect ratio."""
        super().resizeEvent(event)
        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)


class PictographViewPool:
    """
    Pool manager for reusable QGraphicsView instances.
    
    This provides a small number of views that can be attached to different
    scenes as needed, eliminating the expensive view creation bottleneck.
    """
    
    def __init__(self, initial_pool_size: int = 10):
        self._pool: Queue[PictographView] = Queue()
        self._checked_out: Set[PictographView] = set()
        self._initial_pool_size = initial_pool_size
        self._initialized = False
        
    def initialize_pool(self) -> None:
        """Initialize the view pool with pre-created views."""
        if self._initialized:
            return
            
        logger.info(f"🎯 [VIEW_POOL] Initializing view pool with {self._initial_pool_size} views...")
        
        # Create lightweight views
        for i in range(self._initial_pool_size):
            view = PictographView()
            view.hide()  # Keep hidden until needed
            self._pool.put(view)
            
        self._initialized = True
        logger.info(f"✅ [VIEW_POOL] View pool initialized with {self._pool.qsize()} views")
        
    def checkout_view(self, parent: Optional[QWidget] = None) -> Optional[PictographView]:
        """
        Get an available view from the pool.
        
        Args:
            parent: Optional parent widget for the view
            
        Returns:
            PictographView or None if pool is exhausted
        """
        if not self._initialized:
            self.initialize_pool()
            
        if self._pool.empty():
            # Create on-demand view if pool is exhausted
            logger.warning("⚠️ [VIEW_POOL] Pool exhausted, creating view on-demand")
            view = PictographView(parent)
            view.hide()
            return view
            
        view = self._pool.get()
        self._checked_out.add(view)
        
        # Set parent if provided
        if parent:
            view.setParent(parent)
            
        logger.debug(f"🔄 [VIEW_POOL] Checked out view (pool: {self._pool.qsize()}, out: {len(self._checked_out)})")
        return view
        
    def checkin_view(self, view: PictographView) -> None:
        """
        Return a view to the pool.
        
        Args:
            view: The view to return to the pool
        """
        if view not in self._checked_out:
            # Handle on-demand views
            logger.debug("🔄 [VIEW_POOL] Destroying on-demand view")
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
        
        logger.debug(f"🔄 [VIEW_POOL] Checked in view (pool: {self._pool.qsize()}, out: {len(self._checked_out)})")
        
    def get_pool_stats(self) -> Dict[str, int]:
        """Get current pool statistics."""
        return {
            "pool_size": self._pool.qsize(),
            "checked_out": len(self._checked_out),
            "total_capacity": self._initial_pool_size,
            "utilization_percent": int((len(self._checked_out) / self._initial_pool_size) * 100) if self._initial_pool_size > 0 else 0,
        }
        
    def cleanup_pool(self) -> None:
        """Clean up the pool and all views."""
        logger.info("🧹 [VIEW_POOL] Cleaning up view pool...")
        
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
        
        logger.info("✅ [VIEW_POOL] View pool cleanup complete")


# Global view pool instance
_global_view_pool: Optional[PictographViewPool] = None


def get_pictograph_view_pool() -> PictographViewPool:
    """Get the global pictograph view pool instance."""
    global _global_view_pool
    if _global_view_pool is None:
        _global_view_pool = PictographViewPool()
    return _global_view_pool


def initialize_pictograph_view_pool() -> None:
    """Initialize the global pictograph view pool."""
    pool = get_pictograph_view_pool()
    pool.initialize_pool()
