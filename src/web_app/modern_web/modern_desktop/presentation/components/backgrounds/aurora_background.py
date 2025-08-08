from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath
from PyQt6.QtWidgets import QWidget
from shared.application.services.backgrounds.aurora.blob_animation import (
    AuroraBlobAnimation,
)
from shared.application.services.backgrounds.aurora.sparkle_animation import (
    AuroraSparkleAnimation,
)
from shared.application.services.backgrounds.aurora.wave_effects import (
    AuroraWaveEffects,
)

from .base_background import BaseBackground


class AuroraBackground(BaseBackground):
    def __init__(self, parent=None) -> None:
        super().__init__(parent or QWidget())

        # Use services instead of managers
        self.blob_animation = AuroraBlobAnimation(3)
        self.sparkle_animation = AuroraSparkleAnimation(50)
        self.wave_effects = AuroraWaveEffects()

    def animate_background(self) -> None:
        # Update all animation services
        self.blob_animation.update_blobs()
        self.sparkle_animation.update_sparkles()
        self.wave_effects.update_wave_effects()

        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw wavy gradient background using wave effects service
        gradient = QLinearGradient(0, widget.height(), widget.width(), 0)
        colors = [(255, 0, 255, 100), (0, 255, 255, 100), (255, 255, 0, 100)]

        for i, (r, g, b, a) in enumerate(colors):
            hue = self.wave_effects.get_color_hue(0, i)
            color = QColor.fromHsv(hue, 255, 255, a)

            wave_shift = self.wave_effects.calculate_wave_shift(i, len(colors))
            position = min(max(i / len(colors) + wave_shift, 0), 1)
            gradient.setColorAt(position, color)

        painter.fillRect(widget.rect(), gradient)

        # Draw blobs using service data
        self._draw_blobs(painter, widget)

        # Draw sparkles using service data
        self._draw_sparkles(painter, widget)

    def _draw_blobs(self, painter: QPainter, widget: QWidget) -> None:
        """Draw blobs using service data"""
        for blob in self.blob_animation.get_blob_states():
            blob_path = QPainterPath()
            blob_x = blob.position.x * widget.width()
            blob_y = blob.position.y * widget.height()

            blob_path.addEllipse(blob_x, blob_y, blob.size, blob.size)

            painter.setOpacity(blob.opacity)
            painter.setBrush(QColor(255, 255, 255, int(blob.opacity * 255)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPath(blob_path)

        painter.setOpacity(1.0)

    def _draw_sparkles(self, painter: QPainter, widget: QWidget) -> None:
        """Draw sparkles using service data"""
        for sparkle in self.sparkle_animation.get_sparkle_states():
            x = int(sparkle.position.x * widget.width())
            y = int(sparkle.position.y * widget.height())
            size = int(sparkle.size)

            painter.setOpacity(sparkle.opacity)
            painter.setBrush(QColor(255, 255, 255, int(sparkle.opacity * 255)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(x, y, size, size)

        painter.setOpacity(1.0)
