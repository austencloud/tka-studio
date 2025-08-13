"""
Framework-Agnostic Prop Rendering Service

This service handles prop rendering logic without Qt dependencies.
It generates render commands and positioning data that can be executed
by any rendering framework.
"""

import logging
from abc import ABC, abstractmethod

from desktop.modern.application.services.core.pictograph_renderer import (
    IPictographAssetProvider,
)
from desktop.modern.application.services.core.types import Point, RenderCommand, Size
from desktop.modern.domain.models import MotionData, PictographData

logger = logging.getLogger(__name__)


class IPropRenderingService(ABC):
    """Interface for framework-agnostic prop rendering."""

    @abstractmethod
    def create_prop_render_command(
        self,
        color: str,
        motion_data: MotionData,
        target_size: Size,
        pictograph_data: PictographData | None = None,
    ) -> RenderCommand:
        """Create render command for prop."""

    @abstractmethod
    def calculate_prop_position(
        self,
        motion_data: MotionData,
        color: str,
        target_size: Size,
        pictograph_data: PictographData | None = None,
    ) -> Point:
        """Calculate prop position based on motion data and beta positioning."""

    @abstractmethod
    def calculate_prop_rotation(self, motion_data: MotionData, color: str) -> float:
        """Calculate prop rotation angle."""


class CorePropRenderingService(IPropRenderingService):
    """
    Framework-agnostic prop rendering service.

    Handles all prop rendering logic without Qt dependencies:
    - Prop positioning calculations
    - Beta positioning integration
    - Rotation calculations
    - Color transformations
    """

    def __init__(self, asset_provider: IPictographAssetProvider):
        """Initialize with asset provider."""
        self._asset_provider = asset_provider
        self._performance_stats = {
            "props_rendered": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors": 0,
        }

    def create_prop_render_command(
        self,
        color: str,
        motion_data: MotionData,
        target_size: Size,
        pictograph_data: PictographData | None = None,
    ) -> RenderCommand:
        """
        Create render command for prop.

        Args:
            color: Prop color ("blue" or "red")
            motion_data: Motion data for positioning
            target_size: Target rendering size
            pictograph_data: Full pictograph data for beta positioning

        Returns:
            RenderCommand for prop rendering
        """
        try:
            # Calculate prop position (includes beta positioning logic)
            position = self.calculate_prop_position(
                motion_data, color, target_size, pictograph_data
            )

            # Calculate prop rotation
            rotation = self.calculate_prop_rotation(motion_data, color)

            # Get prop asset with pictograph_data for beta positioning support
            prop_type = self._determine_prop_type(motion_data, pictograph_data)
            prop_asset = self._asset_provider.get_prop_asset(
                prop_type, color, pictograph_data
            )

            if not prop_asset:
                logger.error(
                    f"❌ [PROP_SERVICE] Failed to get prop asset for {prop_type}/{color}"
                )
                self._performance_stats["errors"] += 1
                return self._create_error_command(position, target_size)

            # Create render command using correct RenderCommand interface
            command = RenderCommand(
                command_id=f"prop_{color}_{motion_data.motion_type.value if motion_data.motion_type else 'unknown'}",
                target_id=f"prop_{color}_{self._performance_stats['props_rendered']}",
                render_type="svg",
                position=position,
                size=Size(width=100, height=100),  # Default prop size
                properties={
                    "element_type": "prop",
                    "asset_id": prop_asset.asset_id,
                    "svg_content": prop_asset.svg_content,
                    "rotation": rotation,
                    "color": color,
                    "layer_order": 2,  # Props above grid but below arrows
                    "prop_type": prop_type,
                    "motion_type": (
                        motion_data.motion_type.value
                        if motion_data.motion_type
                        else None
                    ),
                    "has_beta_positioning": pictograph_data is not None,
                },
            )

            self._performance_stats["props_rendered"] += 1
            logger.debug(
                f"🎭 [PROP_SERVICE] Created render command for {color} {prop_type}"
            )

            return command

        except Exception as e:
            logger.error(f"❌ [PROP_SERVICE] Failed to create prop render command: {e}")
            self._performance_stats["errors"] += 1
            return self._create_error_command(Point(0, 0), target_size)

    def calculate_prop_position(
        self,
        motion_data: MotionData,
        color: str,
        target_size: Size,
        pictograph_data: PictographData | None = None,
    ) -> Point:
        """
        Calculate prop position based on motion data and beta positioning.

        This integrates with the existing PropManagementService for beta positioning
        when pictograph_data is provided.
        """
        try:
            # Base position from motion data
            base_x = getattr(motion_data, "end_x", target_size.width / 2)
            base_y = getattr(motion_data, "end_y", target_size.height / 2)
            base_position = Point(base_x, base_y)

            # Apply beta positioning if available
            if pictograph_data:
                beta_offset = self._calculate_beta_positioning_offset(
                    motion_data, color, pictograph_data
                )
                return Point(
                    base_position.x + beta_offset.x, base_position.y + beta_offset.y
                )

            return base_position

        except Exception as e:
            logger.error(f"❌ [PROP_SERVICE] Failed to calculate prop position: {e}")
            return Point(target_size.width / 2, target_size.height / 2)

    def calculate_prop_rotation(self, motion_data: MotionData, color: str) -> float:
        """
        Calculate prop rotation angle based on motion data.

        This replicates the rotation logic from the original service.
        """
        try:
            # Basic rotation based on motion type and end location
            if not motion_data.end_loc:
                return 0.0

            # Simplified rotation logic (can be enhanced)
            location_rotations = {
                "north": 90.0,
                "east": 180.0,
                "south": 270.0,
                "west": 0.0,
            }

            base_rotation = location_rotations.get(
                motion_data.end_loc.value.lower() if motion_data.end_loc else "north",
                0.0,
            )

            # Adjust for motion type
            if motion_data.motion_type and motion_data.motion_type.value == "anti":
                base_rotation += 180.0

            return base_rotation % 360.0

        except Exception as e:
            logger.error(f"❌ [PROP_SERVICE] Failed to calculate rotation: {e}")
            return 0.0

    def _determine_prop_type(
        self, motion_data: MotionData, pictograph_data: PictographData | None
    ) -> str:
        """Determine prop type from motion data or pictograph settings."""
        # For now, default to staff - this should integrate with settings
        return "staff"

    def _calculate_beta_positioning_offset(
        self, motion_data: MotionData, color: str, pictograph_data: PictographData
    ) -> Point:
        """
        Calculate beta positioning offset.

        This would integrate with the existing PropManagementService
        for consistent beta positioning logic.
        """
        try:
            # This is a simplified version - in practice, this should use
            # the existing PropManagementService.calculate_separation_offsets()

            # Import here to avoid circular dependencies
            from desktop.modern.application.services.positioning.props.orchestration.prop_management_service import (
                PropManagementService,
            )

            # Get beta positioning service
            prop_mgmt_service = PropManagementService()

            # Check if beta positioning should be applied
            if prop_mgmt_service.should_apply_beta_positioning(pictograph_data):
                blue_offset, red_offset = (
                    prop_mgmt_service.calculate_separation_offsets(pictograph_data)
                )

                if color == "blue":
                    return blue_offset
                elif color == "red":
                    return red_offset

            return Point(0, 0)

        except Exception as e:
            logger.warning(f"⚠️ [PROP_SERVICE] Beta positioning calculation failed: {e}")
            return Point(0, 0)

    def _create_error_command(
        self, position: Point, target_size: Size
    ) -> RenderCommand:
        """Create error placeholder command."""
        return RenderCommand(
            command_id="prop_error",
            target_id="error_placeholder",
            render_type="error",
            position=position,
            size=Size(50, 50),
            properties={
                "element_type": "error",
                "asset_id": "error_placeholder",
                "rotation": 0.0,
                "color": "red",
                "layer_order": 1,
                "error": "Failed to render prop",
            },
        )

    def get_performance_stats(self) -> dict[str, int]:
        """Get performance statistics."""
        return self._performance_stats.copy()

    def reset_performance_stats(self):
        """Reset performance statistics."""
        self._performance_stats = {
            "props_rendered": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors": 0,
        }


# Factory function
def create_prop_rendering_service(
    asset_provider: IPictographAssetProvider,
) -> CorePropRenderingService:
    """Create framework-agnostic prop rendering service."""
    return CorePropRenderingService(asset_provider)
