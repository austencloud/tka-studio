"""
Framework-Agnostic Image Export Service

This service handles image generation logic without Qt dependencies.
It generates image export commands and data that can be executed
by any image processing framework.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from shared.application.services.core.types import (
    Color,
    ImageData,
    ImageFormat,
    Point,
    Size,
)

logger = logging.getLogger(__name__)


class IImageExportService(ABC):
    """Interface for framework-agnostic image export."""

    @abstractmethod
    def create_export_commands(
        self, sequence_data: dict[str, Any], export_options: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Create image export commands."""

    @abstractmethod
    def calculate_layout_dimensions(
        self, beat_count: int, export_options: dict[str, Any]
    ) -> tuple[Size, dict[str, Any]]:
        """Calculate layout dimensions for export."""

    @abstractmethod
    def generate_export_data(
        self, sequence_data: dict[str, Any], export_options: dict[str, Any]
    ) -> ImageData:
        """Generate image export data."""


class CoreImageExportService(IImageExportService):
    """
    Framework-agnostic image export service.

    Handles all image export logic without Qt dependencies:
    - Layout calculations
    - Beat positioning
    - Text rendering specifications
    - Background and border definitions
    """

    def __init__(self):
        """Initialize the image export service."""
        self._performance_stats = {
            "exports_created": 0,
            "layouts_calculated": 0,
            "errors": 0,
        }

    def create_export_commands(
        self, sequence_data: dict[str, Any], export_options: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """
        Create image export commands.

        Args:
            sequence_data: Complete sequence data with beats
            export_options: Export configuration options

        Returns:
            List of export commands for each element
        """
        try:
            commands = []

            # Calculate layout
            beat_count = len(sequence_data.get("beats", []))
            canvas_size, layout_info = self.calculate_layout_dimensions(
                beat_count, export_options
            )

            # Create background command
            background_cmd = self._create_background_command(
                canvas_size, export_options
            )
            commands.append(background_cmd)

            # Create header commands (title, difficulty, etc.)
            header_commands = self._create_header_commands(
                sequence_data, layout_info, export_options
            )
            commands.extend(header_commands)

            # Create beat commands
            beat_commands = self._create_beat_commands(
                sequence_data.get("beats", []), layout_info, export_options
            )
            commands.extend(beat_commands)

            # Create footer commands (if any)
            footer_commands = self._create_footer_commands(
                sequence_data, layout_info, export_options
            )
            commands.extend(footer_commands)

            self._performance_stats["exports_created"] += 1
            logger.debug(f"Created {len(commands)} export commands")

            return commands

        except Exception as e:
            self._performance_stats["errors"] += 1
            logger.error(f"Failed to create export commands: {e}")
            return []

    def calculate_layout_dimensions(
        self, beat_count: int, export_options: dict[str, Any]
    ) -> tuple[Size, dict[str, Any]]:
        """
        Calculate layout dimensions for export.

        Args:
            beat_count: Number of beats to layout
            export_options: Export configuration

        Returns:
            Tuple of (canvas_size, layout_info)
        """
        try:
            # Get export settings
            beats_per_row = export_options.get("beats_per_row", 4)
            beat_size = export_options.get("beat_size", 200)
            margin = export_options.get("margin", 50)
            header_height = export_options.get("header_height", 100)
            footer_height = export_options.get("footer_height", 50)

            # Calculate grid dimensions
            rows = (beat_count + beats_per_row - 1) // beats_per_row  # Ceiling division
            cols = min(beat_count, beats_per_row)

            # Calculate canvas size
            content_width = cols * beat_size + (cols - 1) * margin
            content_height = rows * beat_size + (rows - 1) * margin

            canvas_width = content_width + 2 * margin
            canvas_height = content_height + header_height + footer_height + 2 * margin

            canvas_size = Size(canvas_width, canvas_height)

            # Layout info for positioning
            layout_info = {
                "beat_size": beat_size,
                "beats_per_row": beats_per_row,
                "margin": margin,
                "header_height": header_height,
                "footer_height": footer_height,
                "content_start_x": margin,
                "content_start_y": margin + header_height,
                "rows": rows,
                "cols": cols,
            }

            self._performance_stats["layouts_calculated"] += 1
            logger.debug(f"Calculated layout: {canvas_size} for {beat_count} beats")

            return canvas_size, layout_info

        except Exception as e:
            self._performance_stats["errors"] += 1
            logger.error(f"Failed to calculate layout: {e}")
            return Size(800, 600), {}

    def generate_export_data(
        self, sequence_data: dict[str, Any], export_options: dict[str, Any]
    ) -> ImageData:
        """
        Generate image export data.

        Args:
            sequence_data: Complete sequence data
            export_options: Export configuration

        Returns:
            ImageData with all rendering specifications
        """
        try:
            # Create export commands
            commands = self.create_export_commands(sequence_data, export_options)

            # Get canvas size
            beat_count = len(sequence_data.get("beats", []))
            canvas_size, layout_info = self.calculate_layout_dimensions(
                beat_count, export_options
            )

            # Create image data
            image_data = ImageData(
                width=canvas_size.width,
                height=canvas_size.height,
                format=ImageFormat.PNG,  # Default format
                background_color=Color.from_hex(
                    export_options.get("background_color", "#FFFFFF")
                ),
                render_commands=commands,
                metadata={
                    "sequence_name": sequence_data.get("name", "Untitled"),
                    "beat_count": beat_count,
                    "layout_info": layout_info,
                    "export_options": export_options,
                },
            )

            return image_data

        except Exception as e:
            self._performance_stats["errors"] += 1
            logger.error(f"Failed to generate export data: {e}")
            return ImageData(
                width=800,
                height=600,
                format=ImageFormat.PNG,
                background_color=Color.WHITE,
                render_commands=[],
                metadata={"error": str(e)},
            )

    def _create_background_command(
        self, canvas_size: Size, export_options: dict[str, Any]
    ) -> dict[str, Any]:
        """Create background drawing command."""
        return {
            "type": "background",
            "position": Point(0, 0),
            "size": canvas_size,
            "color": export_options.get("background_color", "#FFFFFF"),
            "layer_order": 0,
        }

    def _create_header_commands(
        self,
        sequence_data: dict[str, Any],
        layout_info: dict[str, Any],
        export_options: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Create header drawing commands (title, difficulty, etc.)."""
        commands = []

        # Title command
        if sequence_data.get("name"):
            title_cmd = {
                "type": "text",
                "text": sequence_data["name"],
                "position": Point(layout_info["margin"], layout_info["margin"]),
                "font_size": export_options.get("title_font_size", 24),
                "font_weight": "bold",
                "color": "#000000",
                "layer_order": 10,
            }
            commands.append(title_cmd)

        # Difficulty command
        if sequence_data.get("difficulty"):
            difficulty_cmd = {
                "type": "text",
                "text": f"Difficulty: {sequence_data['difficulty']}",
                "position": Point(layout_info["margin"], layout_info["margin"] + 30),
                "font_size": export_options.get("info_font_size", 14),
                "color": "#666666",
                "layer_order": 10,
            }
            commands.append(difficulty_cmd)

        return commands

    def _create_beat_commands(
        self,
        beats: list[dict[str, Any]],
        layout_info: dict[str, Any],
        export_options: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Create beat drawing commands."""
        commands = []

        for i, beat_data in enumerate(beats):
            # Calculate beat position
            row = i // layout_info["beats_per_row"]
            col = i % layout_info["beats_per_row"]

            x = layout_info["content_start_x"] + col * (
                layout_info["beat_size"] + layout_info["margin"]
            )
            y = layout_info["content_start_y"] + row * (
                layout_info["beat_size"] + layout_info["margin"]
            )

            # Create beat command
            beat_cmd = {
                "type": "beat",
                "beat_data": beat_data,
                "position": Point(x, y),
                "size": Size(layout_info["beat_size"], layout_info["beat_size"]),
                "layer_order": 5,
                "beat_index": i,
            }
            commands.append(beat_cmd)

        return commands

    def _create_footer_commands(
        self,
        sequence_data: dict[str, Any],
        layout_info: dict[str, Any],
        export_options: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Create footer drawing commands."""
        commands = []

        # Add footer elements if needed (copyright, timestamp, etc.)
        footer_y = layout_info["content_start_y"] + layout_info["rows"] * (
            layout_info["beat_size"] + layout_info["margin"]
        )

        if export_options.get("include_timestamp", False):
            from datetime import datetime

            timestamp_cmd = {
                "type": "text",
                "text": f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                "position": Point(layout_info["margin"], footer_y),
                "font_size": 10,
                "color": "#999999",
                "layer_order": 10,
            }
            commands.append(timestamp_cmd)

        return commands

    def get_performance_stats(self) -> dict[str, Any]:
        """Get performance statistics."""
        return self._performance_stats.copy()

    def reset_performance_stats(self):
        """Reset performance statistics."""
        self._performance_stats = {
            "exports_created": 0,
            "layouts_calculated": 0,
            "errors": 0,
        }


# Factory function
def create_image_export_service() -> CoreImageExportService:
    """Create framework-agnostic image export service."""
    return CoreImageExportService()
