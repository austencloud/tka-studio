"""
Qt Image Export Adapter

Bridges between the framework-agnostic core image export service and Qt-specific
image generation. Converts image export commands to Qt painting operations.
"""

import logging
from typing import Any, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QImage, QPainter, QPen

from desktop.modern.application.services.core.image_export_service import CoreImageExportService
from desktop.modern.application.services.core.types import (
    Color,
    ImageData,
    ImageFormat,
    Point,
    Size,
)

logger = logging.getLogger(__name__)


# ============================================================================
# QT TYPE CONVERTERS
# ============================================================================


class QtImageExportConverter:
    """Converts between framework-agnostic types and Qt types for image export."""

    @staticmethod
    def color_to_qt(color: Color) -> QColor:
        """Convert Color to QColor."""
        return QColor(color.red, color.green, color.blue, color.alpha)

    @staticmethod
    def point_to_qt(point: Point) -> tuple[int, int]:
        """Convert Point to Qt coordinates."""
        return (point.x, point.y)

    @staticmethod
    def size_to_qt(size: Size) -> tuple[int, int]:
        """Convert Size to Qt dimensions."""
        return (size.width, size.height)

    @staticmethod
    def format_to_qt(format: ImageFormat) -> QImage.Format:
        """Convert ImageFormat to Qt image format."""
        format_map = {
            ImageFormat.PNG: QImage.Format.Format_ARGB32,
            ImageFormat.JPEG: QImage.Format.Format_RGB32,
            ImageFormat.SVG: QImage.Format.Format_ARGB32,
            ImageFormat.WEBP: QImage.Format.Format_ARGB32,
        }
        return format_map.get(format, QImage.Format.Format_ARGB32)


# ============================================================================
# QT IMAGE EXPORT ENGINE
# ============================================================================


class QtImageExportEngine:
    """Qt-specific image export engine that executes export commands."""

    def __init__(self):
        """Initialize Qt image export engine."""
        self._font_cache: dict[str, QFont] = {}
        logger.info("Qt image export engine initialized")

    def render_to_qt_image(self, image_data: ImageData) -> QImage:
        """Render image data to Qt QImage."""
        try:
            # Create Qt image
            qt_format = QtImageExportConverter.format_to_qt(image_data.format)
            qt_image = QImage(image_data.width, image_data.height, qt_format)

            # Fill background
            if image_data.background_color:
                bg_color = QtImageExportConverter.color_to_qt(
                    image_data.background_color
                )
                qt_image.fill(bg_color)
            else:
                qt_image.fill(QColor(255, 255, 255))  # Default white

            # Create painter
            painter = QPainter(qt_image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

            try:
                # Execute render commands
                self._execute_render_commands(painter, image_data.render_commands or [])
            finally:
                painter.end()

            logger.debug(
                f"Successfully rendered image: {image_data.width}x{image_data.height}"
            )
            return qt_image

        except Exception as e:
            logger.error(f"Failed to render Qt image: {e}")
            # Return error image
            error_image = QImage(400, 300, QImage.Format.Format_ARGB32)
            error_image.fill(QColor(255, 200, 200))  # Light red
            return error_image

    def _execute_render_commands(
        self, painter: QPainter, commands: list[dict[str, Any]]
    ):
        """Execute all render commands on the painter."""
        # Sort commands by layer order
        sorted_commands = sorted(commands, key=lambda cmd: cmd.get("layer_order", 0))

        for command in sorted_commands:
            try:
                command_type = command.get("type", "unknown")

                if command_type == "background":
                    self._render_background_command(painter, command)
                elif command_type == "text":
                    self._render_text_command(painter, command)
                elif command_type == "beat":
                    self._render_beat_command(painter, command)
                elif command_type == "rectangle":
                    self._render_rectangle_command(painter, command)
                elif command_type == "border":
                    self._render_border_command(painter, command)
                else:
                    logger.warning(f"Unknown command type: {command_type}")

            except Exception as e:
                logger.error(
                    f"Failed to execute command {command.get('type', 'unknown')}: {e}"
                )

    def _render_background_command(self, painter: QPainter, command: dict[str, Any]):
        """Render background command."""
        try:
            # Background is already filled during image creation
            # This command can be used for additional background effects
            pass
        except Exception as e:
            logger.error(f"Failed to render background: {e}")

    def _render_text_command(self, painter: QPainter, command: dict[str, Any]):
        """Render text command."""
        try:
            text = command.get("text", "")
            position = command.get("position", Point(0, 0))
            font_size = command.get("font_size", 12)
            font_weight = command.get("font_weight", "normal")
            color = command.get("color", "#000000")

            # Create font
            font = self._get_font(font_size, font_weight)
            painter.setFont(font)

            # Set color
            if isinstance(color, str):
                qt_color = QColor(color)
            else:
                qt_color = QtImageExportConverter.color_to_qt(color)
            painter.setPen(QPen(qt_color))

            # Draw text
            x, y = QtImageExportConverter.point_to_qt(position)
            painter.drawText(x, y, text)

        except Exception as e:
            logger.error(f"Failed to render text: {e}")

    def _render_beat_command(self, painter: QPainter, command: dict[str, Any]):
        """Render beat command."""
        try:
            beat_data = command.get("beat_data", {})
            position = command.get("position", Point(0, 0))
            size = command.get("size", Size(100, 100))

            x, y = QtImageExportConverter.point_to_qt(position)
            width, height = QtImageExportConverter.size_to_qt(size)

            # Draw beat border
            painter.setPen(QPen(QColor(200, 200, 200), 2))
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawRect(x, y, width, height)

            # Draw beat number
            beat_index = command.get("beat_index", 0)
            font = self._get_font(14, "bold")
            painter.setFont(font)
            painter.setPen(QPen(QColor(100, 100, 100)))

            # Position number at top-left of beat
            painter.drawText(x + 5, y + 20, str(beat_index + 1))

            # TODO: Add pictograph rendering for the beat
            # This would integrate with the pictograph rendering services

        except Exception as e:
            logger.error(f"Failed to render beat: {e}")

    def _render_rectangle_command(self, painter: QPainter, command: dict[str, Any]):
        """Render rectangle command."""
        try:
            position = command.get("position", Point(0, 0))
            size = command.get("size", Size(100, 100))
            color = command.get("color", "#000000")
            fill_color = command.get("fill_color")
            stroke_width = command.get("stroke_width", 1)

            x, y = QtImageExportConverter.point_to_qt(position)
            width, height = QtImageExportConverter.size_to_qt(size)

            # Set pen and brush
            qt_color = (
                QColor(color)
                if isinstance(color, str)
                else QtImageExportConverter.color_to_qt(color)
            )
            painter.setPen(QPen(qt_color, stroke_width))

            if fill_color:
                qt_fill = (
                    QColor(fill_color)
                    if isinstance(fill_color, str)
                    else QtImageExportConverter.color_to_qt(fill_color)
                )
                painter.setBrush(QBrush(qt_fill))
            else:
                painter.setBrush(QBrush(Qt.BrushStyle.NoBrush))

            painter.drawRect(x, y, width, height)

        except Exception as e:
            logger.error(f"Failed to render rectangle: {e}")

    def _render_border_command(self, painter: QPainter, command: dict[str, Any]):
        """Render border command."""
        try:
            position = command.get("position", Point(0, 0))
            size = command.get("size", Size(100, 100))
            color = command.get("color", "#000000")
            width = command.get("width", 1)

            x, y = QtImageExportConverter.point_to_qt(position)
            rect_width, rect_height = QtImageExportConverter.size_to_qt(size)

            qt_color = (
                QColor(color)
                if isinstance(color, str)
                else QtImageExportConverter.color_to_qt(color)
            )
            painter.setPen(QPen(qt_color, width))
            painter.setBrush(QBrush(Qt.BrushStyle.NoBrush))

            painter.drawRect(x, y, rect_width, rect_height)

        except Exception as e:
            logger.error(f"Failed to render border: {e}")

    def _get_font(self, size: int, weight: str = "normal") -> QFont:
        """Get cached font with specified size and weight."""
        cache_key = f"{size}_{weight}"

        if cache_key not in self._font_cache:
            font = QFont("Arial", size)

            if weight == "bold":
                font.setBold(True)
            elif weight == "light":
                font.setWeight(QFont.Weight.Light)

            self._font_cache[cache_key] = font

        return self._font_cache[cache_key]


# ============================================================================
# MAIN QT IMAGE EXPORT ADAPTER
# ============================================================================


class QtImageExportAdapter:
    """
    Main adapter that bridges core image export service with Qt image generation.

    This adapter:
    1. Uses the framework-agnostic core service to generate export specifications
    2. Converts export commands to Qt painting operations
    3. Provides the same interface as the original Qt service for easy migration
    """

    def __init__(self, core_service: Optional[CoreImageExportService] = None):
        """Initialize the adapter."""
        self.core_service = core_service or CoreImageExportService()
        self.qt_engine = QtImageExportEngine()

        logger.info("Qt image export adapter initialized")

    # ========================================================================
    # LEGACY INTERFACE COMPATIBILITY
    # ========================================================================

    def render_sequence_image(
        self, sequence_data: dict[str, Any], export_options: dict[str, Any]
    ) -> QImage:
        """
        Render sequence image using core service + Qt execution (legacy interface).

        Args:
            sequence_data: Complete sequence data
            export_options: Export configuration options

        Returns:
            Rendered QImage
        """
        try:
            # Use core service to generate export data
            image_data = self.core_service.generate_export_data(
                sequence_data, export_options
            )

            # Execute with Qt engine
            qt_image = self.qt_engine.render_to_qt_image(image_data)

            return qt_image

        except Exception as e:
            logger.error(f"Failed to render sequence image: {e}")
            # Return error image
            error_image = QImage(400, 300, QImage.Format.Format_ARGB32)
            error_image.fill(QColor(255, 200, 200))
            return error_image

    def calculate_image_dimensions(
        self, beat_count: int, export_options: dict[str, Any]
    ) -> tuple[int, int]:
        """Calculate image dimensions (legacy interface)."""
        try:
            canvas_size, _ = self.core_service.calculate_layout_dimensions(
                beat_count, export_options
            )
            return (canvas_size.width, canvas_size.height)
        except Exception as e:
            logger.error(f"Failed to calculate dimensions: {e}")
            return (800, 600)

    # ========================================================================
    # NEW CAPABILITIES
    # ========================================================================

    def generate_export_data(
        self, sequence_data: dict[str, Any], export_options: dict[str, Any]
    ) -> ImageData:
        """Generate framework-agnostic export data (useful for testing/debugging)."""
        return self.core_service.generate_export_data(sequence_data, export_options)

    def get_export_statistics(self) -> dict[str, Any]:
        """Get export statistics."""
        return {
            "core_service_stats": self.core_service.get_performance_stats(),
            "adapter_status": "active",
            "architecture": "framework_agnostic_core_with_qt_adapter",
        }


# ============================================================================
# FACTORY FUNCTION FOR EASY INTEGRATION
# ============================================================================


def create_qt_image_export_adapter() -> QtImageExportAdapter:
    """
    Factory function to create Qt image export adapter.

    Returns:
        Configured Qt adapter ready for use
    """
    core_service = CoreImageExportService()
    adapter = QtImageExportAdapter(core_service)

    logger.info("Created Qt image export adapter with framework-agnostic core")
    return adapter
