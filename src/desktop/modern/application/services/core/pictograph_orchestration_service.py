"""
Framework-Agnostic Pictograph Orchestration Service

This service orchestrates pictograph rendering by generating render commands
instead of directly manipulating Qt objects. It can be used by both desktop
and web services.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from .pictograph_renderer import CorePictographRenderer, IPictographAssetProvider
from .types import Point, RenderCommand, Size

logger = logging.getLogger(__name__)


class IPictographOrchestrationService(ABC):
    """Interface for framework-agnostic pictograph orchestration."""

    @abstractmethod
    def create_pictograph_commands(
        self,
        pictograph_data: dict[str, Any],
        target_size: Size,
        options: dict | None = None,
    ) -> list[RenderCommand]:
        """Create render commands for complete pictograph."""

    @abstractmethod
    def create_grid_command(
        self, grid_mode: str, size: Size, position: Point = Point(0, 0)
    ) -> RenderCommand:
        """Create render command for grid."""

    @abstractmethod
    def create_prop_command(
        self,
        color: str,
        motion_data: dict[str, Any],
        position: Point,
        pictograph_data: dict | None = None,
    ) -> RenderCommand:
        """Create render command for prop."""

    @abstractmethod
    def create_glyph_command(
        self, glyph_type: str, glyph_data: dict[str, Any], position: Point, size: Size
    ) -> RenderCommand:
        """Create render command for glyph."""


class CorePictographOrchestrationService(IPictographOrchestrationService):
    """
    Framework-agnostic pictograph orchestration service.

    This service coordinates the creation of render commands for all
    pictograph elements without any Qt dependencies.
    """

    def __init__(self, asset_provider: IPictographAssetProvider):
        """Initialize with asset provider."""
        self.core_renderer = CorePictographRenderer(asset_provider)
        self._performance_stats = {"commands_created": 0, "errors": 0}

    def create_pictograph_commands(
        self,
        pictograph_data: dict[str, Any],
        target_size: Size,
        options: dict | None = None,
    ) -> list[RenderCommand]:
        """
        Create render commands for complete pictograph.

        Args:
            pictograph_data: Complete pictograph data
            target_size: Target rendering size
            options: Optional rendering options

        Returns:
            List of render commands to execute
        """
        try:
            commands = []

            # Create grid command
            grid_mode = pictograph_data.get("grid_mode", "diamond")
            grid_cmd = self.create_grid_command(grid_mode, target_size)
            commands.append(grid_cmd)

            # Create prop commands
            motions = pictograph_data.get("motions", {})
            if "blue" in motions:
                blue_cmd = self.create_prop_command(
                    "blue",
                    motions["blue"],
                    self._calculate_prop_position(motions["blue"], target_size),
                    pictograph_data,
                )
                commands.append(blue_cmd)

            if "red" in motions:
                red_cmd = self.create_prop_command(
                    "red",
                    motions["red"],
                    self._calculate_prop_position(motions["red"], target_size),
                    pictograph_data,
                )
                commands.append(red_cmd)

            # Create glyph commands
            glyphs = pictograph_data.get("glyphs", [])
            for glyph in glyphs:
                glyph_cmd = self.create_glyph_command(
                    glyph.get("type", "letter"),
                    glyph,
                    Point(glyph.get("x", 0), glyph.get("y", 0)),
                    Size(glyph.get("width", 50), glyph.get("height", 50)),
                )
                commands.append(glyph_cmd)

            self._performance_stats["commands_created"] += len(commands)
            logger.debug(f"Created {len(commands)} render commands")

            return commands

        except Exception as e:
            self._performance_stats["errors"] += 1
            logger.error(f"Failed to create pictograph commands: {e}")
            return []

    def create_grid_command(
        self, grid_mode: str, size: Size, position: Point = Point(0, 0)
    ) -> RenderCommand:
        """Create render command for grid."""
        return self.core_renderer.render_grid(grid_mode, size, position)

    def create_prop_command(
        self,
        color: str,
        motion_data: dict[str, Any],
        position: Point,
        pictograph_data: dict | None = None,
    ) -> RenderCommand:
        """Create render command for prop."""
        prop_type = motion_data.get("prop_type", "staff")
        return self.core_renderer.render_prop(prop_type, color, position, motion_data)

    def create_glyph_command(
        self, glyph_type: str, glyph_data: dict[str, Any], position: Point, size: Size
    ) -> RenderCommand:
        """Create render command for glyph."""
        glyph_id = glyph_data.get("id", "")
        return self.core_renderer.render_glyph(glyph_type, glyph_id, position, size)

    def _calculate_prop_position(
        self, motion_data: dict[str, Any], target_size: Size
    ) -> Point:
        """Calculate prop position from motion data."""
        # Extract position from motion data or use defaults
        x = motion_data.get("end_x", target_size.width / 2)
        y = motion_data.get("end_y", target_size.height / 2)
        return Point(x, y)

    def get_performance_stats(self) -> dict[str, Any]:
        """Get performance statistics."""
        return self._performance_stats.copy()

    def reset_performance_stats(self):
        """Reset performance statistics."""
        self._performance_stats = {"commands_created": 0, "errors": 0}
