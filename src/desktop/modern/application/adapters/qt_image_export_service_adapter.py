"""
Qt Adapter for Image Export Service

This adapter bridges the framework-agnostic image export service with Qt's
QPainter-based rendering system, maintaining backward compatibility.
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QImage, QPainter, QPen

from desktop.modern.application.services.core.image_export_service import (
    create_image_export_service,
)
from desktop.modern.application.services.core.types import Point, Size


logger = logging.getLogger(__name__)


class QtImageExportServiceAdapter:
    """
    Qt adapter for image export service.

    Bridges the framework-agnostic core service with Qt's QPainter
    rendering system, maintaining the same interface as the original
    Qt-dependent SequenceImageRenderer.
    """

    def __init__(self, container=None):
        """Initialize the adapter with core services."""
        # Initialize core service (framework-agnostic)
        self._core_service = create_image_export_service()

        # Qt-specific rendering components
        self._painter = None
        self._current_image = None

        # Performance tracking
        self._render_count = 0

        logger.debug("🖼️ [QT_EXPORT_ADAPTER] Initialized Qt image export adapter")

    def render_sequence_image(
        self, sequence_data: dict[str, Any], export_options: dict[str, Any]
    ) -> QImage:
        """
        Render sequence image using core service + Qt execution.

        This maintains compatibility with the original Qt-dependent interface
        while using framework-agnostic logic internally.
        """
        try:
            # Generate export data using core service
            image_data = self._core_service.generate_export_data(
                sequence_data, export_options
            )

            # Create Qt image
            qt_image = QImage(
                image_data.width, image_data.height, QImage.Format.Format_ARGB32
            )
            qt_image.fill(self._convert_color_to_qt(image_data.background_color))

            # Initialize Qt painter
            painter = QPainter(qt_image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

            # Execute render commands
            self._execute_render_commands(painter, image_data.render_commands)

            painter.end()

            self._render_count += 1
            logger.info(
                f"🖼️ [QT_EXPORT_ADAPTER] Rendered sequence image: {image_data.width}x{image_data.height}"
            )

            return qt_image

        except Exception as e:
            logger.exception(f"❌ [QT_EXPORT_ADAPTER] Failed to render sequence image: {e}")
            # Return error image
            error_image = QImage(800, 600, QImage.Format.Format_ARGB32)
            error_image.fill(Qt.GlobalColor.white)
            return error_image

    def _execute_render_commands(
        self, painter: QPainter, commands: list[dict[str, Any]]
    ):
        """Execute render commands using Qt painter."""
        try:
            # Sort commands by layer order
            sorted_commands = sorted(
                commands, key=lambda cmd: cmd.get("layer_order", 0)
            )

            for command in sorted_commands:
                self._execute_single_command(painter, command)

        except Exception as e:
            logger.exception(
                f"❌ [QT_EXPORT_ADAPTER] Failed to execute render commands: {e}"
            )

    def _execute_single_command(self, painter: QPainter, command: dict[str, Any]):
        """Execute a single render command."""
        try:
            command_type = command.get("type", "unknown")

            if command_type == "background":
                self._render_background(painter, command)
            elif command_type == "text":
                self._render_text(painter, command)
            elif command_type == "beat":
                self._render_beat(painter, command)
            else:
                logger.warning(
                    f"⚠️ [QT_EXPORT_ADAPTER] Unknown command type: {command_type}"
                )

        except Exception as e:
            logger.exception(
                f"❌ [QT_EXPORT_ADAPTER] Failed to execute command {command.get('type')}: {e}"
            )

    def _render_background(self, painter: QPainter, command: dict[str, Any]):
        """Render background command."""
        try:
            position = command.get("position", Point(0, 0))
            size = command.get("size", Size(800, 600))
            color = command.get("color", "#FFFFFF")

            # Create brush and fill background
            brush = QBrush(QColor(color))
            painter.fillRect(
                int(position.x),
                int(position.y),
                int(size.width),
                int(size.height),
                brush,
            )

        except Exception as e:
            logger.exception(f"❌ [QT_EXPORT_ADAPTER] Failed to render background: {e}")

    def _render_text(self, painter: QPainter, command: dict[str, Any]):
        """Render text command."""
        try:
            text = command.get("text", "")
            position = command.get("position", Point(0, 0))
            font_size = command.get("font_size", 12)
            font_weight = command.get("font_weight", "normal")
            color = command.get("color", "#000000")

            # Set up font
            font = QFont()
            font.setPointSize(font_size)
            if font_weight == "bold":
                font.setBold(True)
            painter.setFont(font)

            # Set up pen
            pen = QPen(QColor(color))
            painter.setPen(pen)

            # Draw text
            painter.drawText(int(position.x), int(position.y), text)

        except Exception as e:
            logger.exception(f"❌ [QT_EXPORT_ADAPTER] Failed to render text: {e}")

    def _render_beat(self, painter: QPainter, command: dict[str, Any]):
        """Render beat command."""
        try:
            command.get("beat_data", {})
            position = command.get("position", Point(0, 0))
            size = command.get("size", Size(200, 200))

            # For now, render a simple placeholder
            # In practice, this would use the pictograph rendering system

            # Draw beat border
            pen = QPen(QColor("#CCCCCC"))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawRect(
                int(position.x), int(position.y), int(size.width), int(size.height)
            )

            # Draw beat number or identifier
            beat_index = command.get("beat_index", 0)
            font = QFont()
            font.setPointSize(14)
            painter.setFont(font)
            painter.setPen(QPen(QColor("#666666")))
            painter.drawText(
                int(position.x + 10), int(position.y + 25), f"Beat {beat_index + 1}"
            )

            # TODO: Integrate with pictograph rendering system
            # This would render the actual pictograph using the
            # QtPictographRenderingServiceAdapter

        except Exception as e:
            logger.exception(f"❌ [QT_EXPORT_ADAPTER] Failed to render beat: {e}")

    def _convert_color_to_qt(self, color) -> QColor:
        """Convert framework-agnostic color to Qt color."""
        try:
            if hasattr(color, "to_hex"):
                return QColor(color.to_hex())
            if isinstance(color, str):
                return QColor(color)
            return QColor("#FFFFFF")  # Default white
        except Exception:
            return QColor("#FFFFFF")

    def get_performance_stats(self) -> dict[str, Any]:
        """Get performance statistics."""
        core_stats = self._core_service.get_performance_stats()
        return {**core_stats, "qt_renders": self._render_count}

    def clear_cache(self):
        """Clear any caches."""
        self._core_service.reset_performance_stats()
