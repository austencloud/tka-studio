"""Sparkle Manager - Qt Presentation Layer

Thin wrapper for sparkle rendering - business logic delegated to AuroraSparkleAnimation service.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter

from desktop.modern.application.services.backgrounds.aurora.sparkle_animation import (
    AuroraSparkleAnimation,
)


class SparkleManager:
    """Thin Qt wrapper for sparkle rendering - business logic in AuroraSparkleAnimation service."""

    def __init__(self, num_sparkles=50):
        self._animation_service = AuroraSparkleAnimation(num_sparkles)

    def animate(self):
        """Delegate animation logic to service."""
        self._animation_service.update_sparkles()

    def draw(self, widget, painter: QPainter):
        """Draw sparkles using Qt - get state from service."""
        sparkle_states = self._animation_service.get_sparkle_states()

        for sparkle in sparkle_states:
            x = int(sparkle.position.x * widget.width())
            y = int(sparkle.position.y * widget.height())
            size = int(sparkle.size)

            painter.setOpacity(sparkle.opacity)
            painter.setBrush(QColor(255, 255, 255, int(sparkle.opacity * 255)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(x, y, size, size)

        painter.setOpacity(1.0)  # Reset opacity
