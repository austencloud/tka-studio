"""
Core Pictograph Rendering Service

Framework-agnostic pictograph rendering service that generates render commands
instead of directly manipulating UI frameworks. Can be used by both desktop (QT)
and web services.
"""

import logging
from abc import ABC, abstractmethod
from typing import Protocol

from .types import (
    Color,
    Colors,
    Point,
    RenderCommand,
    Size,
    SvgAsset,
)

logger = logging.getLogger(__name__)


# ============================================================================
# INTERFACES
# ============================================================================


class IPictographAssetProvider(Protocol):
    """Protocol for providing pictograph assets."""

    def get_grid_asset(self, grid_mode: str) -> SvgAsset | None:
        """Get grid SVG asset."""
        ...

    def get_prop_asset(self, prop_type: str, color: str) -> SvgAsset | None:
        """Get prop SVG asset."""
        ...

    def get_glyph_asset(self, glyph_type: str, glyph_id: str) -> SvgAsset | None:
        """Get glyph SVG asset."""
        ...

    def get_arrow_asset(self, arrow_type: str) -> SvgAsset | None:
        """Get arrow SVG asset."""
        ...


class IPictographRenderer(ABC):
    """Interface for pictograph rendering operations."""

    @abstractmethod
    def create_render_commands(
        self, pictograph_data: dict, target_size: Size, options: dict | None = None
    ) -> list[RenderCommand]:
        """Create list of render commands for pictograph."""

    @abstractmethod
    def render_grid(
        self, grid_mode: str, target_size: Size, position: Point = Point(0, 0)
    ) -> RenderCommand:
        """Create render command for grid."""

    @abstractmethod
    def render_prop(
        self,
        prop_type: str,
        color: str,
        position: Point,
        motion_data: dict | None = None,
    ) -> RenderCommand:
        """Create render command for prop."""

    @abstractmethod
    def render_glyph(
        self, glyph_type: str, glyph_id: str, position: Point, size: Size
    ) -> RenderCommand:
        """Create render command for glyph."""


# ============================================================================
# CORE SERVICE IMPLEMENTATION
# ============================================================================


class CorePictographRenderer(IPictographRenderer):
    """
    Framework-agnostic core pictograph renderer.

    Generates render commands instead of directly manipulating UI frameworks.
    Can be used by both QT desktop applications and web services.
    """

    def __init__(self, asset_provider: IPictographAssetProvider):
        """Initialize with asset provider."""
        self.asset_provider = asset_provider
        self._command_counter = 0

    def create_render_commands(
        self, pictograph_data: dict, target_size: Size, options: dict | None = None
    ) -> list[RenderCommand]:
        """
        Create complete list of render commands for pictograph.

        Args:
            pictograph_data: Pictograph data dictionary
            target_size: Target rendering size
            options: Optional rendering options

        Returns:
            List of render commands to execute
        """
        commands = []
        options = options or {}

        try:
            # 1. Render grid (background)
            grid_mode = pictograph_data.get("grid_mode", "diamond")
            if options.get("show_grid", True):
                grid_command = self.render_grid(grid_mode, target_size)
                commands.append(grid_command)

            # 2. Render props
            props_data = pictograph_data.get("props", [])
            for prop_data in props_data:
                prop_command = self.render_prop(
                    prop_data.get("type", "staff"),
                    prop_data.get("color", "blue"),
                    Point(prop_data.get("x", 0), prop_data.get("y", 0)),
                    prop_data.get("motion_data"),
                )
                commands.append(prop_command)

            # 3. Render glyphs
            glyphs_data = pictograph_data.get("glyphs", [])
            for glyph_data in glyphs_data:
                glyph_command = self.render_glyph(
                    glyph_data.get("type", "letter"),
                    glyph_data.get("id", ""),
                    Point(glyph_data.get("x", 0), glyph_data.get("y", 0)),
                    Size(glyph_data.get("width", 50), glyph_data.get("height", 50)),
                )
                commands.append(glyph_command)

            # 4. Render arrows
            arrows_data = pictograph_data.get("arrows", [])
            for arrow_data in arrows_data:
                arrow_command = self._render_arrow(
                    arrow_data.get("type", "motion"),
                    Point(arrow_data.get("start_x", 0), arrow_data.get("start_y", 0)),
                    Point(arrow_data.get("end_x", 100), arrow_data.get("end_y", 100)),
                    arrow_data.get("color", "black"),
                )
                commands.append(arrow_command)

            logger.info(f"Created {len(commands)} render commands for pictograph")
            return commands

        except Exception as e:
            logger.error(f"Failed to create render commands: {e}")
            return []

    def render_grid(
        self, grid_mode: str, target_size: Size, position: Point = Point(0, 0)
    ) -> RenderCommand:
        """Create render command for grid background."""
        try:
            logger.debug(
                f"🔲 [CORE_RENDERER] render_grid called with mode: {grid_mode}"
            )
            logger.debug(
                f"🔲 [CORE_RENDERER] Asset provider: {type(self.asset_provider)}"
            )

            grid_asset = self.asset_provider.get_grid_asset(grid_mode)
            logger.debug(f"🔲 [CORE_RENDERER] Grid asset result: {grid_asset}")

            if not grid_asset:
                logger.warning(f"Grid asset not found for mode: {grid_mode}")
                return self._create_error_command("grid", position, target_size)

            return RenderCommand(
                command_id=self._next_command_id(),
                target_id="background",
                render_type="svg",
                position=position,
                size=target_size,
                properties={
                    "asset_id": grid_asset.asset_id,
                    "svg_content": grid_asset.svg_content,
                    "layer": "background",
                    "z_index": 0,
                },
            )

        except Exception as e:
            logger.error(f"Failed to create grid render command: {e}")
            return self._create_error_command("grid", position, target_size)

    def render_prop(
        self,
        prop_type: str,
        color: str,
        position: Point,
        motion_data: dict | None = None,
        pictograph_data: dict | None = None,
    ) -> RenderCommand:
        """Create render command for prop."""
        try:
            # Pass pictograph_data to get_prop_asset for beta positioning support
            prop_asset = self.asset_provider.get_prop_asset(
                prop_type, color, pictograph_data
            )
            if not prop_asset:
                logger.warning(f"Prop asset not found: {prop_type}/{color}")
                return self._create_error_command("prop", position, Size(50, 200))

            # The SVG content should already have the correct color applied by the asset provider
            colored_svg = prop_asset.svg_content

            # Calculate size, position, and rotation using existing modern services
            prop_size = self._calculate_prop_size(motion_data)
            base_position = self._calculate_prop_position(position, motion_data)

            # Apply beta positioning if needed
            final_position = self._apply_beta_positioning(
                base_position, color, motion_data, pictograph_data
            )

            rotation = self._calculate_prop_rotation(motion_data)

            return RenderCommand(
                command_id=self._next_command_id(),
                target_id=f"prop_{self._command_counter}",
                render_type="svg",
                position=final_position,
                size=prop_size,
                properties={
                    "asset_id": prop_asset.asset_id,
                    "svg_content": colored_svg,
                    "layer": "props",
                    "z_index": 10,
                    "prop_type": prop_type,
                    "color": color,
                    "rotation": rotation,
                    "motion_data": motion_data or {},
                },
            )

        except Exception as e:
            logger.error(f"Failed to create prop render command: {e}")
            return self._create_error_command("prop", position, Size(50, 200))

    def render_glyph(
        self, glyph_type: str, glyph_id: str, position: Point, size: Size
    ) -> RenderCommand:
        """Create render command for glyph."""
        try:
            glyph_asset = self.asset_provider.get_glyph_asset(glyph_type, glyph_id)
            if not glyph_asset:
                logger.warning(f"Glyph asset not found: {glyph_type}:{glyph_id}")
                return self._create_error_command("glyph", position, size)

            return RenderCommand(
                command_id=self._next_command_id(),
                target_id=f"glyph_{self._command_counter}",
                render_type="svg",
                position=position,
                size=size,
                properties={
                    "asset_id": glyph_asset.asset_id,
                    "svg_content": glyph_asset.svg_content,
                    "layer": "glyphs",
                    "z_index": 20,
                    "glyph_type": glyph_type,
                    "glyph_id": glyph_id,
                },
            )

        except Exception as e:
            logger.error(f"Failed to create glyph render command: {e}")
            return self._create_error_command("glyph", position, size)

    def _render_arrow(
        self, arrow_type: str, start_pos: Point, end_pos: Point, color: str
    ) -> RenderCommand:
        """Create render command for arrow."""
        try:
            arrow_asset = self.asset_provider.get_arrow_asset(arrow_type)
            if not arrow_asset:
                logger.warning(f"Arrow asset not found: {arrow_type}")
                return self._create_error_command("arrow", start_pos, Size(100, 20))

            # Calculate arrow size and rotation
            arrow_size, rotation = self._calculate_arrow_transform(start_pos, end_pos)
            color_obj = self._parse_color(color)
            colored_svg = arrow_asset.get_colored_svg(
                {"stroke": color_obj, "fill": color_obj}
            )

            return RenderCommand(
                command_id=self._next_command_id(),
                target_id=f"arrow_{self._command_counter}",
                render_type="svg",
                position=start_pos,
                size=arrow_size,
                properties={
                    "asset_id": arrow_asset.asset_id,
                    "svg_content": colored_svg,
                    "layer": "arrows",
                    "z_index": 15,
                    "arrow_type": arrow_type,
                    "rotation": rotation,
                    "start_pos": start_pos,
                    "end_pos": end_pos,
                },
            )

        except Exception as e:
            logger.error(f"Failed to create arrow render command: {e}")
            return self._create_error_command("arrow", start_pos, Size(100, 20))

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def _next_command_id(self) -> str:
        """Generate next command ID."""
        self._command_counter += 1
        return f"cmd_{self._command_counter:04d}"

    def _create_error_command(
        self, item_type: str, position: Point, size: Size
    ) -> RenderCommand:
        """Create error placeholder command."""
        return RenderCommand(
            command_id=self._next_command_id(),
            target_id=f"error_{self._command_counter}",
            render_type="error",
            position=position,
            size=size,
            properties={
                "error": True,
                "item_type": item_type,
                "error_message": f"Failed to render {item_type}",
            },
        )

    def _parse_color(self, color_str: str) -> Color:
        """Parse color string to Color object."""
        try:
            if color_str.startswith("#"):
                return Color.from_hex(color_str)
            elif color_str == "red":
                return Colors.RED
            elif color_str == "blue":
                return Colors.BLUE
            else:
                logger.warning(f"Unknown color: {color_str}, using black")
                return Colors.BLACK
        except Exception as e:
            logger.error(f"Failed to parse color {color_str}: {e}")
            return Colors.BLACK

    def _calculate_prop_size(self, motion_data: dict | None) -> Size:
        """
        Calculate prop size - LEGACY COMPATIBLE approach.

        Legacy doesn't calculate prop sizes - it uses the SVG's natural dimensions.
        This method should return the natural SVG size, not a calculated size.
        The actual sizing is handled by the Qt renderer using the SVG's viewBox.
        """
        # Return the natural staff.svg dimensions (252.8x77.8)
        # This matches legacy behavior where props use their natural SVG size
        return Size(253, 78)  # Rounded natural staff.svg dimensions

    def _calculate_prop_rotation(self, motion_data: dict | None) -> float:
        """
        Calculate prop rotation using existing modern rotation services.

        Integrates with the carefully crafted prop rotation logic.
        """
        if not motion_data:
            return 0.0

        try:
            # Import and use the existing modern prop rotation calculator
            from desktop.modern.domain.models import MotionData, Orientation
            from desktop.modern.domain.models.enums import Location, MotionType
            from shared.application.services.positioning.props.calculation.prop_rotation_calculator import (
                PropRotationCalculator,
            )

            # Convert dict to MotionData object with proper value mapping
            location_map = {
                "north": "n",
                "east": "e",
                "south": "s",
                "west": "w",
                "northeast": "ne",
                "southeast": "se",
                "southwest": "sw",
                "northwest": "nw",
            }

            start_loc_str = motion_data.get("start_loc", "north")
            end_loc_str = motion_data.get("end_loc", "north")

            from desktop.modern.domain.models.enums import RotationDirection

            motion_obj = MotionData(
                motion_type=MotionType(motion_data.get("motion_type", "pro")),
                start_loc=Location(location_map.get(start_loc_str, start_loc_str)),
                end_loc=Location(location_map.get(end_loc_str, end_loc_str)),
                start_ori=Orientation(motion_data.get("start_ori", "in")),
                end_ori=Orientation(motion_data.get("end_ori", "in")),
                prop_rot_dir=RotationDirection(motion_data.get("prop_rot_dir", "cw")),
                turns=motion_data.get("turns", 1),
            )

            # Use the existing rotation calculator
            rotation_calculator = PropRotationCalculator()
            return rotation_calculator.calculate_prop_rotation_angle(motion_obj)

        except (ImportError, ValueError, KeyError) as e:
            logger.warning(f"Failed to use modern rotation calculator: {e}")
            # Fallback to basic rotation logic
            return self._basic_prop_rotation(motion_data)

    def _basic_prop_rotation(self, motion_data: dict) -> float:
        """Basic fallback rotation logic."""
        end_loc = motion_data.get("end_loc", "north")
        end_ori = motion_data.get("end_ori", "in")

        # Basic rotation mapping
        location_rotations = {
            "north": 90.0 if end_ori == "in" else 270.0,
            "east": 180.0 if end_ori == "in" else 0.0,
            "south": 270.0 if end_ori == "in" else 90.0,
            "west": 0.0 if end_ori == "in" else 180.0,
        }

        return location_rotations.get(end_loc, 0.0)

    def _apply_beta_positioning(
        self,
        base_position: Point,
        color: str,
        motion_data: dict | None,
        pictograph_data: dict | None,
    ) -> Point:
        """
        Apply beta positioning logic using existing modern services.

        Integrates with the carefully crafted beta positioning system.
        """
        if not pictograph_data or not motion_data:
            return base_position

        try:
            # Import beta positioning services
            from desktop.modern.domain.models.beat_data import BeatData
            from shared.application.services.positioning.props.detection.beta_positioning_detector import (
                BetaPositioningDetector,
            )
            from shared.application.services.positioning.props.orchestration.prop_management_service import (
                PropManagementService,
            )

            # Handle both dictionary and PictographData object formats
            if hasattr(pictograph_data, "letter"):
                # PictographData object
                letter = pictograph_data.letter
                pictograph_obj = pictograph_data
            elif hasattr(pictograph_data, "get"):
                # Dictionary format
                letter = pictograph_data.get("letter")
                if not letter:
                    return base_position
                # Create PictographData object from dictionary
                from desktop.modern.domain.models.pictograph_data import PictographData

                pictograph_obj = PictographData.from_dict(pictograph_data)
            else:
                logger.warning(
                    f"Unknown pictograph_data format: {type(pictograph_data)}"
                )
                return base_position

            if not letter:
                return base_position

            # Check if beta positioning should be applied
            detector = BetaPositioningDetector()

            # Create BeatData with proper parameters
            beat_data = BeatData(
                beat_number=1,
                pictograph_data=pictograph_obj,  # Default beat number
            )

            if not detector.should_apply_beta_positioning(beat_data):
                return base_position

            # Apply beta positioning using management service
            prop_service = PropManagementService()
            blue_offset, red_offset = prop_service.calculate_separation_offsets(
                pictograph_obj
            )

            # Apply the appropriate offset based on color
            if color == "blue":
                return Point(
                    base_position.x + blue_offset.x, base_position.y + blue_offset.y
                )
            elif color == "red":
                return Point(
                    base_position.x + red_offset.x, base_position.y + red_offset.y
                )
            else:
                return base_position

        except (ImportError, AttributeError, Exception) as e:
            logger.warning(f"Beta positioning failed: {e}")
            return base_position

    def _calculate_prop_position(
        self, base_position: Point, motion_data: dict | None
    ) -> Point:
        """Calculate final prop position based on motion data using legacy coordinates."""
        if not motion_data:
            return base_position

        # Extract positioning data from motion data
        end_loc = motion_data.get("end_loc", "s")

        # EXACT Legacy hand point coordinates from legacy grid data
        # These match the precise coordinates from circleCoordinates.ts and grid_data.py
        legacy_coordinates = {
            "n": {"x": 475.0, "y": 331.9},  # n_diamond_hand_point
            "e": {"x": 618.1, "y": 475.0},  # e_diamond_hand_point
            "s": {"x": 475.0, "y": 618.1},  # s_diamond_hand_point
            "w": {"x": 331.9, "y": 475.0},  # w_diamond_hand_point
            "ne": {"x": 618.1, "y": 331.9},  # Calculated diagonal
            "se": {"x": 618.1, "y": 618.1},  # Calculated diagonal
            "sw": {"x": 331.9, "y": 618.1},  # Calculated diagonal
            "nw": {"x": 331.9, "y": 331.9},  # Calculated diagonal
        }

        # Get coordinates for the location
        if isinstance(end_loc, str):
            location_key = end_loc.lower()
        else:
            # Handle enum values
            location_key = str(end_loc).lower() if end_loc else "s"

        coords = legacy_coordinates.get(
            location_key, {"x": 475, "y": 475}
        )  # Default to center

        logger.debug(
            f"🎯 [RENDERER] Calculated prop position for {end_loc}: ({coords['x']}, {coords['y']})"
        )

        return Point(coords["x"], coords["y"])

    def _calculate_arrow_transform(
        self, start: Point, end: Point
    ) -> tuple[Size, float]:
        """Calculate arrow size and rotation."""
        import math

        # Calculate distance and angle
        dx = end.x - start.x
        dy = end.y - start.y
        length = int(math.sqrt(dx * dx + dy * dy))
        rotation = math.degrees(math.atan2(dy, dx))

        return Size(length, 20), rotation  # 20px height for arrow


# ============================================================================
# REAL ASSET PROVIDER INTEGRATION
# ============================================================================

# REMOVED: Duplicate RealAssetProvider class
# The real implementation is in real_asset_provider.py and implements both
# IAssetProvider and IPictographAssetProvider interfaces


# ============================================================================
# FACTORY FUNCTION
# ============================================================================


def create_pictograph_renderer(
    asset_provider: IPictographAssetProvider | None = None, asset_manager=None
) -> CorePictographRenderer:
    """
    Factory function to create pictograph renderer.

    Args:
        asset_provider: Asset provider implementation (creates real provider if None)
        asset_manager: Existing asset manager to integrate with

    Returns:
        Configured pictograph renderer
    """
    if asset_provider is None:
        # Import the real asset provider from the correct module
        from shared.application.services.core.pictograph_rendering.real_asset_provider import (
            create_real_asset_provider,
        )

        asset_provider = create_real_asset_provider()

    return CorePictographRenderer(asset_provider)
