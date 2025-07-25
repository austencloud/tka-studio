"""
Qt Adapter for Pictograph Rendering Service

This adapter bridges the framework-agnostic core orchestration service
with Qt-specific presentation, maintaining backward compatibility while
enabling framework independence.
"""

import logging
from typing import Any, Dict, Optional

from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsScene

# Import the framework-agnostic services
from application.services.core.pictograph_orchestration_service import (
    CorePictographOrchestrationService
)
from application.services.core.pictograph_rendering.real_asset_provider import (
    create_real_asset_provider
)
from application.services.core.types import Size, Point

# Import the Qt render engine from existing adapter
from application.adapters.qt_pictograph_adapter import QtRenderEngine, QtTypeConverter

from domain.models import MotionData, PictographData

logger = logging.getLogger(__name__)


class QtPictographRenderingServiceAdapter:
    """
    Qt adapter that maintains the same interface as the original Qt-dependent service
    but uses the framework-agnostic core service internally.
    
    This enables a drop-in replacement that removes Qt dependencies from business logic
    while maintaining backward compatibility for existing Qt code.
    """
    
    _instance = None
    _creation_logged = False
    
    def __new__(cls, *args, **kwargs):
        """Ensure only one instance is created (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if not cls._creation_logged:
                logger.info("🎭 [QT_ADAPTER] Created Qt Pictograph Rendering Service Adapter")
                cls._creation_logged = True
        return cls._instance
    
    def __init__(self):
        """Initialize the adapter with core services."""
        # Prevent re-initialization of singleton
        if hasattr(self, "_initialized"):
            return
            
        # Initialize core services (framework-agnostic)
        self._asset_provider = create_real_asset_provider()
        self._core_service = CorePictographOrchestrationService(self._asset_provider)
        
        # Initialize Qt render engine
        self._qt_render_engine = QtRenderEngine()
        
        # Performance tracking
        self._render_count = 0
        
        # Mark as initialized
        self._initialized = True
        
        logger.debug("🎭 [QT_ADAPTER] Initialized Qt adapter with core services")
    
    # ========================================================================
    # LEGACY INTERFACE COMPATIBILITY (Qt-dependent signatures)
    # ========================================================================
    
    def render_grid(
        self, scene: QGraphicsScene, grid_mode: str = "diamond"
    ) -> Optional[QGraphicsSvgItem]:
        """
        Render grid using core service + Qt execution (legacy interface).
        
        This maintains the exact same signature as the original service
        but uses framework-agnostic logic internally.
        """
        try:
            # Convert Qt scene to framework-agnostic size
            scene_rect = scene.sceneRect()
            target_size = Size(
                width=int(scene_rect.width()) if scene_rect.width() > 0 else 950,
                height=int(scene_rect.height()) if scene_rect.height() > 0 else 950
            )
            
            # Use core service to create render command
            grid_command = self._core_service.create_grid_command(
                grid_mode, 
                target_size, 
                Point(0, 0)
            )
            
            # Execute command with Qt render engine
            target = QtTypeConverter.create_render_target_from_scene(scene)
            success = self._qt_render_engine.execute_command(grid_command, target)
            
            if success:
                # Return the created Qt item for legacy compatibility
                return self._qt_render_engine._created_items.get(grid_command.command_id)
            
            return None
            
        except Exception as e:
            logger.error(f"❌ [QT_ADAPTER] Failed to render grid: {e}")
            return None
    
    def render_prop(
        self,
        scene: QGraphicsScene,
        color: str,
        motion_data: MotionData,
        pictograph_data: Optional[PictographData] = None,
    ) -> Optional[QGraphicsSvgItem]:
        """
        Render prop using core service + Qt execution (legacy interface).
        
        This maintains the exact same signature as the original service
        but uses framework-agnostic logic internally.
        """
        try:
            # Convert motion data to dict for core service
            motion_dict = {
                "motion_type": motion_data.motion_type.value if motion_data.motion_type else "pro",
                "end_x": getattr(motion_data, "end_x", 475),  # Default center
                "end_y": getattr(motion_data, "end_y", 475),
                "prop_type": "staff"  # Default prop type
            }
            
            # Calculate position
            position = Point(motion_dict["end_x"], motion_dict["end_y"])
            
            # Use core service to create render command
            prop_command = self._core_service.create_prop_command(
                color,
                motion_dict,
                position,
                self._convert_pictograph_data_to_dict(pictograph_data) if pictograph_data else None
            )
            
            # Execute command with Qt render engine
            target = QtTypeConverter.create_render_target_from_scene(scene)
            success = self._qt_render_engine.execute_command(prop_command, target)
            
            if success:
                self._render_count += 1
                logger.debug(f"🎭 [QT_ADAPTER] Rendered {color} prop")
                return self._qt_render_engine._created_items.get(prop_command.command_id)
            
            return None
            
        except Exception as e:
            logger.error(f"❌ [QT_ADAPTER] Failed to render prop: {e}")
            return None
    
    def render_glyph(
        self, scene: QGraphicsScene, glyph_type: str, glyph_data: Any
    ) -> Optional[QGraphicsSvgItem]:
        """
        Render glyph using core service + Qt execution (legacy interface).
        
        This maintains the exact same signature as the original service
        but uses framework-agnostic logic internally.
        """
        try:
            # Convert glyph data to dict format
            if isinstance(glyph_data, dict):
                glyph_dict = glyph_data
            else:
                # Handle other glyph data types (convert to dict)
                glyph_dict = {"id": str(glyph_data), "type": glyph_type}
            
            # Default position and size
            position = Point(
                glyph_dict.get("x", 100),
                glyph_dict.get("y", 100)
            )
            size = Size(
                glyph_dict.get("width", 50),
                glyph_dict.get("height", 50)
            )
            
            # Use core service to create render command
            glyph_command = self._core_service.create_glyph_command(
                glyph_type,
                glyph_dict,
                position,
                size
            )
            
            # Execute command with Qt render engine
            target = QtTypeConverter.create_render_target_from_scene(scene)
            success = self._qt_render_engine.execute_command(glyph_command, target)
            
            if success:
                return self._qt_render_engine._created_items.get(glyph_command.command_id)
            
            return None
            
        except Exception as e:
            logger.error(f"❌ [QT_ADAPTER] Failed to render glyph: {e}")
            return None
    
    # ========================================================================
    # NEW CAPABILITIES (Framework-agnostic)
    # ========================================================================
    
    def render_complete_pictograph(
        self, 
        scene: QGraphicsScene, 
        pictograph_data: PictographData,
        options: Optional[Dict] = None
    ) -> bool:
        """
        Render complete pictograph using core service.
        
        This is a new capability that leverages the framework-agnostic
        orchestration service.
        """
        try:
            # Clear previous items
            self._qt_render_engine.clear_created_items(scene)
            
            # Convert to dict format
            pictograph_dict = self._convert_pictograph_data_to_dict(pictograph_data)
            
            # Get scene size
            scene_rect = scene.sceneRect()
            target_size = Size(
                width=int(scene_rect.width()) if scene_rect.width() > 0 else 950,
                height=int(scene_rect.height()) if scene_rect.height() > 0 else 950
            )
            
            # Generate all render commands
            commands = self._core_service.create_pictograph_commands(
                pictograph_dict, 
                target_size, 
                options
            )
            
            # Execute all commands
            target = QtTypeConverter.create_render_target_from_scene(scene)
            success_count = 0
            for command in commands:
                if self._qt_render_engine.execute_command(command, target):
                    success_count += 1
            
            logger.info(f"🎭 [QT_ADAPTER] Rendered {success_count}/{len(commands)} pictograph elements")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"❌ [QT_ADAPTER] Failed to render complete pictograph: {e}")
            return False
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        core_stats = self._core_service.get_performance_stats()
        return {
            **core_stats,
            "qt_renders": self._render_count,
            "qt_cache_items": len(self._qt_render_engine._created_items)
        }
    
    def clear_scene_items(self, scene: QGraphicsScene) -> None:
        """Clear all items created by this adapter."""
        self._qt_render_engine.clear_created_items(scene)
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def _convert_pictograph_data_to_dict(self, pictograph_data: PictographData) -> Dict[str, Any]:
        """Convert PictographData to dictionary format for core service."""
        try:
            result = {
                "grid_mode": "diamond",  # Default
                "motions": {},
                "glyphs": []
            }
            
            # Extract motion data
            if hasattr(pictograph_data, 'motions') and pictograph_data.motions:
                for color, motion_data in pictograph_data.motions.items():
                    result["motions"][color] = {
                        "motion_type": motion_data.motion_type.value if motion_data.motion_type else "pro",
                        "end_x": getattr(motion_data, "end_x", 475),
                        "end_y": getattr(motion_data, "end_y", 475),
                        "prop_type": "staff"
                    }
            
            # Extract glyph data (if any)
            if hasattr(pictograph_data, 'letter') and pictograph_data.letter:
                result["glyphs"].append({
                    "type": "letter",
                    "id": pictograph_data.letter,
                    "x": 450,  # Default position
                    "y": 50,
                    "width": 50,
                    "height": 50
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to convert pictograph data: {e}")
            return {"grid_mode": "diamond", "motions": {}, "glyphs": []}


# Factory function for drop-in replacement
def create_qt_pictograph_rendering_service() -> QtPictographRenderingServiceAdapter:
    """
    Create Qt pictograph rendering service adapter.
    
    This can be used as a drop-in replacement for the original
    Qt-dependent PictographRenderingService.
    """
    return QtPictographRenderingServiceAdapter()
