"""Star Manager - Qt Presentation Layer

Qt rendering for stars - business logic delegated to StarTwinkling service.
"""

from __future__ import annotations

import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import QWidget

from desktop.modern.application.services.backgrounds.starfield.star_twinkling import (
    StarTwinkling,
)


# A+ Enhancement: Import Qt resource pooling - Temporarily disabled
# try:
#     from desktop.modern.presentation.qt_integration import qt_resources, pooled_pen, pooled_brush
#     QT_RESOURCES_AVAILABLE = True
# except ImportError:
#     QT_RESOURCES_AVAILABLE = False

# Temporary fallback
QT_RESOURCES_AVAILABLE = False


class StarManager:
    """
    Qt wrapper for star rendering - business logic in StarTwinkling service.

    Handles Qt-specific rendering while delegating star creation,
    animation, and twinkling logic to the service.
    """

    def __init__(self):
        self._twinkling_service = StarTwinkling(150)  # 150 stars for rich sky

    def animate_stars(self):
        """Delegate animation logic to service."""
        self._twinkling_service.update_stars()

    def draw_stars(self, painter: QPainter, widget: QWidget):
        """Draw all stars using Qt - get state from service."""
        star_states = self._twinkling_service.get_star_states()
        twinkle_states = self._twinkling_service.get_twinkle_states()

        for i, star in enumerate(star_states):
            x = int(star.position.x * widget.width())
            y = int(star.position.y * widget.height())

            # Apply twinkling to size and opacity
            twinkle = twinkle_states[i]
            size = int(star.size * (1 + twinkle * 0.5))

            # Convert service color tuple to QColor
            color = QColor(*star.color)
            color.setAlphaF(twinkle)

            # A+ Enhancement: Use resource pooling - Temporarily disabled
            # if QT_RESOURCES_AVAILABLE:
            #     with pooled_brush(color) as brush:
            #         painter.setBrush(brush)
            #         painter.setPen(Qt.PenStyle.NoPen)
            # else:
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)

            # Draw star based on its type
            if star.spikiness == 0:  # Round stars
                painter.drawEllipse(x - size // 2, y - size // 2, size, size)
            elif star.spikiness == 1:  # Star-shaped stars
                self._draw_star_shape(painter, x, y, size, color)
            else:  # Spiky stars
                self._draw_spiky_star(painter, x, y, size, color)

    def _draw_star_shape(
        self, painter: QPainter, x: int, y: int, size: int, color: QColor
    ):
        """Draw a classic 6-pointed star shape."""
        path = QPainterPath()
        radius = size / 2
        angle_step = math.pi / 3  # 6 points

        # Create star rays
        for i in range(6):
            angle = i * angle_step
            x1 = x + radius * math.cos(angle)
            y1 = y + radius * math.sin(angle)
            path.moveTo(x, y)
            path.lineTo(x1, y1)

        # A+ Enhancement: Use resource pooling - Temporarily disabled
        # if QT_RESOURCES_AVAILABLE:
        #     with pooled_pen(color, 1) as pen:
        #         painter.setPen(pen)
        #         painter.drawPath(path)
        # else:
        painter.setPen(color)
        painter.drawPath(path)

    def _draw_spiky_star(
        self, painter: QPainter, x: int, y: int, size: int, color: QColor
    ):
        """Draw a spiky multi-pointed star."""
        path = QPainterPath()
        radius = size / 2
        small_radius = radius * 0.6
        angle_step = math.pi / 6  # 12 points

        # Create alternating long and short points
        for i in range(12):
            angle = i * angle_step
            r = radius if i % 2 == 0 else small_radius
            x1 = x + r * math.cos(angle)
            y1 = y + r * math.sin(angle)
            if i == 0:
                path.moveTo(x1, y1)
            else:
                path.lineTo(x1, y1)
        path.closeSubpath()

        # A+ Enhancement: Use resource pooling - Temporarily disabled
        # if QT_RESOURCES_AVAILABLE:
        #     with pooled_brush(color) as brush:
        #         painter.setBrush(brush)
        #         painter.setPen(Qt.PenStyle.NoPen)
        #         painter.drawPath(path)
        # else:
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)
