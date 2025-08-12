"""
Core Pictograph Rendering Service - Framework Agnostic

This service generates rendering commands instead of directly manipulating Qt objects.
It can be used by both Qt desktop applications and web services.

This replaces the Qt-dependent PictographRenderingService with a clean,
framework-agnostic implementation that follows the same pattern as your
existing core services.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol

from desktop.modern.core.types import Point, Size
from desktop.modern.domain.models import MotionData, PictographData

logger = logging.getLogger(__name__)


class RenderCommandType(Enum):
    """Types of render commands that can be generated."""

    GRID = "grid"
    PROP = "prop"
    ARROW = "arrow"
    GLYPH = "glyph"
    BACKGROUND = "background"


@dataclass
class RenderCommand:
    """Framework-agnostic render command."""

    command_id: str
    command_type: RenderCommandType
    position: Point
    size: Size
    svg_content: str | None = None
    svg_path: str | None = None
    color: str | None = None
    rotation: float = 0.0
    opacity: float = 1.0
    z_index: int = 0
    metadata: dict[str, Any] | None = None


@dataclass
class RenderContext:
    """Context information for rendering operations."""

    target_size: Size
    background_color: str = "white"
    grid_mode: str = "diamond"
    show_grid: bool = True
    show_props: bool = True
    show_arrows: bool = True
    show_glyphs: bool = True


class IRenderCommandGenerator(Protocol):
    """Protocol for services that generate render commands."""

    def generate_render_commands(
        self, pictograph_data: PictographData, context: RenderContext
    ) -> list[RenderCommand]:
        """Generate render commands for the pictograph."""
        ...


class IAssetProvider(ABC):
    """Abstract interface for asset providers."""

    @abstractmethod
    def get_grid_svg(self, grid_mode: str) -> str | None:
        """Get grid SVG content."""

    @abstractmethod
    def get_prop_svg(self, prop_type: str, color: str) -> str | None:
        """Get prop SVG content with color applied."""

    @abstractmethod
    def get_arrow_svg(self, arrow_data: dict[str, Any]) -> str | None:
        """Get arrow SVG content."""

    @abstractmethod
    def get_glyph_svg(self, glyph_type: str, glyph_data: dict[str, Any]) -> str | None:
        """Get glyph SVG content."""


class CorePictographRenderingService:
    """
    Framework-agnostic core pictograph rendering service.

    Generates render commands instead of Qt objects, enabling use in:
    - Qt desktop applications (via adapter)
    - Web services
    - Headless image generation
    - Testing environments

    This service follows the same clean architecture pattern as your
    existing core services in src/application/services/core/.
    """

    def __init__(self, asset_provider: IAssetProvider):
        """Initialize with asset provider."""
        self._asset_provider = asset_provider

    def generate_complete_pictograph_commands(
        self, pictograph_data: PictographData, context: RenderContext
    ) -> list[RenderCommand]:
        """
        Generate all render commands for a complete pictograph.

        Returns list of render commands that can be executed by
        framework-specific adapters.
        """
        commands = []
        command_counter = 0

        try:
            # 1. Generate grid command
            if context.show_grid:
                grid_command = self._generate_grid_command(
                    context, f"grid_{command_counter}"
                )
                if grid_command:
                    commands.append(grid_command)
                    command_counter += 1

            # 2. Generate prop commands
            if context.show_props and pictograph_data.motions:
                prop_commands = self._generate_prop_commands(
                    pictograph_data, context, command_counter
                )
                commands.extend(prop_commands)
                command_counter += len(prop_commands)

            # 3. Generate arrow commands
            if context.show_arrows and pictograph_data.motions:
                arrow_commands = self._generate_arrow_commands(
                    pictograph_data, context, command_counter
                )
                commands.extend(arrow_commands)
                command_counter += len(arrow_commands)

            # 4. Generate glyph commands
            if context.show_glyphs:
                glyph_commands = self._generate_glyph_commands(
                    pictograph_data, context, command_counter
                )
                commands.extend(glyph_commands)

            logger.debug(f"Generated {len(commands)} render commands for pictograph")
            return commands

        except Exception as e:
            logger.error(f"Failed to generate pictograph commands: {e}")
            return []

    def _generate_grid_command(
        self, context: RenderContext, command_id: str
    ) -> RenderCommand | None:
        """Generate grid render command."""
        try:
            svg_content = self._asset_provider.get_grid_svg(context.grid_mode)
            if not svg_content:
                return None

            return RenderCommand(
                command_id=command_id,
                command_type=RenderCommandType.GRID,
                position=Point(0, 0),  # Grid fills entire area
                size=context.target_size,
                svg_content=svg_content,
                z_index=0,  # Grid in background
                metadata={"grid_mode": context.grid_mode},
            )
        except Exception as e:
            logger.error(f"Failed to generate grid command: {e}")
            return None

    def _generate_prop_commands(
        self,
        pictograph_data: PictographData,
        context: RenderContext,
        start_counter: int,
    ) -> list[RenderCommand]:
        """Generate prop render commands for all motions."""
        commands = []

        try:
            for color, motion_data in pictograph_data.motions.items():
                if motion_data:
                    prop_command = self._generate_single_prop_command(
                        motion_data, color, context, f"prop_{color}_{start_counter}"
                    )
                    if prop_command:
                        commands.append(prop_command)
                        start_counter += 1
        except Exception as e:
            logger.error(f"Failed to generate prop commands: {e}")

        return commands

    def _generate_single_prop_command(
        self,
        motion_data: MotionData,
        color: str,
        context: RenderContext,
        command_id: str,
    ) -> RenderCommand | None:
        """Generate render command for a single prop."""
        try:
            # Get prop type from motion data or default to staff
            prop_type = getattr(motion_data, "prop_type", "staff")

            # Get SVG content for prop
            svg_content = self._asset_provider.get_prop_svg(prop_type, color)
            if not svg_content:
                return None

            # Calculate prop position from motion data
            position = self._calculate_prop_position(motion_data, context)

            # Calculate prop rotation
            rotation = self._calculate_prop_rotation(motion_data)

            # Standard prop size (can be made configurable)
            prop_size = Size(50, 200)  # Typical staff dimensions

            return RenderCommand(
                command_id=command_id,
                command_type=RenderCommandType.PROP,
                position=position,
                size=prop_size,
                svg_content=svg_content,
                color=color,
                rotation=rotation,
                z_index=2,  # Props above grid
                metadata={
                    "motion_type": motion_data.motion_type.value,
                    "end_location": motion_data.end_loc.value,
                    "end_orientation": motion_data.end_ori.value,
                },
            )
        except Exception as e:
            logger.error(f"Failed to generate prop command for {color}: {e}")
            return None

    def _generate_arrow_commands(
        self,
        pictograph_data: PictographData,
        context: RenderContext,
        start_counter: int,
    ) -> list[RenderCommand]:
        """Generate arrow render commands."""
        commands = []

        try:
            for color, motion_data in pictograph_data.motions.items():
                if motion_data:
                    arrow_command = self._generate_single_arrow_command(
                        motion_data, color, context, f"arrow_{color}_{start_counter}"
                    )
                    if arrow_command:
                        commands.append(arrow_command)
                        start_counter += 1
        except Exception as e:
            logger.error(f"Failed to generate arrow commands: {e}")

        return commands

    def _generate_single_arrow_command(
        self,
        motion_data: MotionData,
        color: str,
        context: RenderContext,
        command_id: str,
    ) -> RenderCommand | None:
        """Generate render command for a single arrow."""
        try:
            # Create arrow data for asset provider
            arrow_data = {
                "motion_type": motion_data.motion_type.value,
                "start_location": motion_data.start_loc.value,
                "end_location": motion_data.end_loc.value,
                "turns": motion_data.turns,
                "color": color,
            }

            # Get SVG content for arrow
            svg_content = self._asset_provider.get_arrow_svg(arrow_data)
            if not svg_content:
                return None

            # Calculate arrow position (center of motion path)
            position = self._calculate_arrow_position(motion_data, context)

            # Arrow size
            arrow_size = Size(100, 100)  # Standard arrow size

            return RenderCommand(
                command_id=command_id,
                command_type=RenderCommandType.ARROW,
                position=position,
                size=arrow_size,
                svg_content=svg_content,
                color=color,
                z_index=1,  # Arrows between grid and props
                metadata=arrow_data,
            )
        except Exception as e:
            logger.error(f"Failed to generate arrow command for {color}: {e}")
            return None

    def _generate_glyph_commands(
        self,
        pictograph_data: PictographData,
        context: RenderContext,
        start_counter: int,
    ) -> list[RenderCommand]:
        """Generate glyph render commands."""
        commands = []

        try:
            # Letter glyph
            if pictograph_data.letter:
                letter_command = self._generate_letter_glyph_command(
                    pictograph_data.letter, context, f"letter_{start_counter}"
                )
                if letter_command:
                    commands.append(letter_command)
                    start_counter += 1

            # Additional glyphs can be added here
            # (elemental, VTG, TKA, etc.)

        except Exception as e:
            logger.error(f"Failed to generate glyph commands: {e}")

        return commands

    def _generate_letter_glyph_command(
        self, letter: str, context: RenderContext, command_id: str
    ) -> RenderCommand | None:
        """Generate render command for letter glyph."""
        try:
            glyph_data = {"letter": letter, "type": "letter"}
            svg_content = self._asset_provider.get_glyph_svg("letter", glyph_data)

            if not svg_content:
                return None

            # Position letter glyph at top-left
            position = Point(10, 10)
            size = Size(40, 40)

            return RenderCommand(
                command_id=command_id,
                command_type=RenderCommandType.GLYPH,
                position=position,
                size=size,
                svg_content=svg_content,
                z_index=3,  # Glyphs on top
                metadata=glyph_data,
            )
        except Exception as e:
            logger.error(f"Failed to generate letter glyph command for {letter}: {e}")
            return None

    # Helper methods for position and rotation calculations

    def _calculate_prop_position(
        self, motion_data: MotionData, context: RenderContext
    ) -> Point:
        """Calculate prop position based on motion data."""
        # This would use the same logic as your PropManagementService
        # For now, using center as placeholder
        center_x = context.target_size.width / 2
        center_y = context.target_size.height / 2
        return Point(center_x, center_y)

    def _calculate_prop_rotation(self, motion_data: MotionData) -> float:
        """Calculate prop rotation based on motion data."""
        # This would use the same logic as your PropManagementService
        # For now, return 0 as placeholder
        return 0.0

    def _calculate_arrow_position(
        self, motion_data: MotionData, context: RenderContext
    ) -> Point:
        """Calculate arrow position based on motion data."""
        # This would use arrow positioning logic
        # For now, using center as placeholder
        center_x = context.target_size.width / 2
        center_y = context.target_size.height / 2
        return Point(center_x, center_y)
