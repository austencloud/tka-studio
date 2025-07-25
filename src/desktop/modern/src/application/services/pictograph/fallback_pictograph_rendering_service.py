"""
Fallback Pictograph Rendering Service

A minimal implementation that provides basic pictograph rendering capabilities
when the full pictograph rendering service is not available. This allows
the application to function and display basic pictograph elements.
"""

import logging
from typing import Any, Dict, Optional

from domain.models import MotionData, PictographData
from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsScene

logger = logging.getLogger(__name__)


class FallbackPictographRenderingService:
    """
    Minimal fallback implementation for pictograph rendering.
    
    Provides basic rendering capabilities when the full service is unavailable:
    - Simple grid rendering (basic rectangles)
    - Basic prop rendering (colored circles)
    - Placeholder glyph rendering (text items)
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance is created (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            logger.info("🔧 [FALLBACK] Created fallback pictograph rendering service")
        return cls._instance

    def __init__(self):
        """Initialize the fallback service."""
        if hasattr(self, "_initialized"):
            return
        
        self._initialized = True
        logger.info("🔧 [FALLBACK] Fallback pictograph rendering service initialized")

    def render_grid(
        self, scene: QGraphicsScene, grid_mode: str = "diamond"
    ) -> Optional[QGraphicsRectItem]:
        """
        Render a basic grid using simple Qt graphics.
        
        Args:
            scene: Target scene to render into
            grid_mode: Grid type ("diamond" or "box")
            
        Returns:
            Created grid item or None if rendering failed
        """
        try:
            # Create a simple grid representation
            grid_size = 400
            grid_rect = QRectF(-grid_size/2, -grid_size/2, grid_size, grid_size)
            
            # Create grid item
            grid_item = QGraphicsRectItem(grid_rect)
            
            # Style the grid
            pen = QPen(QColor(200, 200, 200), 2, Qt.PenStyle.DashLine)
            grid_item.setPen(pen)
            grid_item.setBrush(QBrush(Qt.BrushStyle.NoBrush))
            
            # Add to scene
            scene.addItem(grid_item)
            
            logger.debug(f"🔧 [FALLBACK] Rendered basic {grid_mode} grid")
            return grid_item
            
        except Exception as e:
            logger.error(f"❌ [FALLBACK] Grid rendering failed: {e}")
            return None

    def render_prop(
        self,
        scene: QGraphicsScene,
        color: str,
        motion_data: MotionData,
        pictograph_data: PictographData,
    ) -> Optional[QGraphicsEllipseItem]:
        """
        Render a basic prop using simple Qt graphics.
        
        Args:
            scene: Target scene to render into
            color: Prop color ("blue", "red", etc.)
            motion_data: Motion data for positioning
            pictograph_data: Pictograph context data
            
        Returns:
            Created prop item or None if rendering failed
        """
        try:
            # Create a simple circular prop
            prop_size = 30
            prop_rect = QRectF(-prop_size/2, -prop_size/2, prop_size, prop_size)
            
            # Create prop item
            prop_item = QGraphicsEllipseItem(prop_rect)
            
            # Style based on color
            color_map = {
                "blue": QColor(100, 150, 255),
                "red": QColor(255, 100, 100),
                "green": QColor(100, 255, 100),
                "yellow": QColor(255, 255, 100),
            }
            
            prop_color = color_map.get(color.lower(), QColor(150, 150, 150))
            prop_item.setBrush(QBrush(prop_color))
            prop_item.setPen(QPen(prop_color.darker(150), 2))
            
            # Position based on motion data (simplified)
            if motion_data:
                # Use start location for positioning
                start_loc = motion_data.start_loc.value if motion_data.start_loc else "center"
                position_map = {
                    "center": (0, 0),
                    "left": (-100, 0),
                    "right": (100, 0),
                    "top": (0, -100),
                    "bottom": (0, 100),
                }
                x, y = position_map.get(start_loc, (0, 0))
                prop_item.setPos(x, y)
            
            # Add to scene
            scene.addItem(prop_item)
            
            logger.debug(f"🔧 [FALLBACK] Rendered basic {color} prop")
            return prop_item
            
        except Exception as e:
            logger.error(f"❌ [FALLBACK] Prop rendering failed: {e}")
            return None

    def render_glyph(
        self, scene: QGraphicsScene, glyph_type: str, glyph_data: Any
    ) -> Optional[QGraphicsRectItem]:
        """
        Render a basic glyph placeholder using simple Qt graphics.
        
        Args:
            scene: Target scene to render into
            glyph_type: Type of glyph ("letter", "elemental", "vtg", "tka", "position")
            glyph_data: Glyph-specific data for rendering
            
        Returns:
            Created glyph item or None if rendering failed
        """
        try:
            # Create a simple rectangular placeholder
            glyph_size = 50
            glyph_rect = QRectF(-glyph_size/2, -glyph_size/2, glyph_size, glyph_size)
            
            # Create glyph item
            glyph_item = QGraphicsRectItem(glyph_rect)
            
            # Style based on glyph type
            type_colors = {
                "letter": QColor(255, 200, 100),
                "elemental": QColor(100, 255, 200),
                "vtg": QColor(200, 100, 255),
                "tka": QColor(255, 100, 200),
                "position": QColor(100, 200, 255),
            }
            
            glyph_color = type_colors.get(glyph_type, QColor(200, 200, 200))
            glyph_item.setBrush(QBrush(glyph_color))
            glyph_item.setPen(QPen(glyph_color.darker(150), 2))
            
            # Position in top area (typical for glyphs)
            glyph_item.setPos(0, -150)
            
            # Add to scene
            scene.addItem(glyph_item)
            
            logger.debug(f"🔧 [FALLBACK] Rendered basic {glyph_type} glyph")
            return glyph_item
            
        except Exception as e:
            logger.error(f"❌ [FALLBACK] Glyph rendering failed: {e}")
            return None

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics (fallback returns empty stats)."""
        return {
            "fallback_service": True,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_renders": 0,
        }

    def clear_cache(self) -> None:
        """Clear all caches (no-op for fallback service)."""
        logger.debug("🔧 [FALLBACK] Cache clear requested (no-op)")


# Factory function for easy integration
def create_fallback_pictograph_rendering_service() -> FallbackPictographRenderingService:
    """
    Create fallback pictograph rendering service.
    
    Returns:
        Configured fallback service ready for use
    """
    return FallbackPictographRenderingService()
