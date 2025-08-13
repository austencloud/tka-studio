from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget

from desktop.modern.application.services.backgrounds.starfield.comet_trajectory import (
    CometTrajectory,
)
from desktop.modern.application.services.backgrounds.starfield.moon_positioning import (
    MoonPositioning,
)
from desktop.modern.application.services.backgrounds.starfield.star_twinkling import (
    StarTwinkling,
)
from desktop.modern.application.services.backgrounds.starfield.ufo_behavior import (
    UFOBehavior,
)

from .base_background import BaseBackground


class StarfieldBackground(BaseBackground):
    """
    Enhanced starfield background with stars, comets, moon, and UFOs.

    This is the full-featured starfield that matches the legacy implementation
    with all the sophisticated space scene elements.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize all starfield services
        self.star_twinkling = StarTwinkling()
        self.comet_trajectory = CometTrajectory()
        self.moon_positioning = MoonPositioning()
        self.ufo_behavior = UFOBehavior()

    def animate_background(self):
        """Animate all starfield services."""
        self.star_twinkling.update_stars()
        self.comet_trajectory.update_comet()
        self.ufo_behavior.update_ufo()
        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        """Paint the complete starfield scene."""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Paint deep space background
        painter.fillRect(widget.rect(), QColor(5, 5, 15))  # Very dark blue-black

        # Paint all starfield elements in proper order (back to front)
        self._draw_stars(painter, widget)
        self._draw_comet(painter, widget)
        self._draw_moon(painter, widget)
        self._draw_ufo(painter, widget)

    def _draw_stars(self, painter: QPainter, widget: QWidget):
        """Draw stars using service data"""
        star_states = self.star_twinkling.get_star_states()
        twinkle_states = self.star_twinkling.get_twinkle_states()

        for i, star in enumerate(star_states):
            x = int(star.position.x * widget.width())
            y = int(star.position.y * widget.height())
            size = int(star.size * twinkle_states[i])

            # Set star color with twinkle intensity
            color = QColor(*star.color)
            color.setAlpha(int(twinkle_states[i] * 255))
            painter.setBrush(color)
            painter.setPen(color)

            # Draw star based on spikiness
            if star.spikiness == 0:  # Round star
                painter.drawEllipse(x, y, size, size)
            else:  # Star shape - simplified representation
                painter.drawEllipse(x, y, size, size)

    def _draw_comet(self, painter: QPainter, widget: QWidget):
        """Draw comet using service data"""
        comet = self.comet_trajectory.get_comet_state()
        if comet:
            # Draw comet tail
            painter.setPen(Qt.PenStyle.NoPen)
            for i, (x, y, size) in enumerate(comet.tail):
                tail_x = x * widget.width()
                tail_y = y * widget.height()
                alpha = int((1 - i / len(comet.tail)) * 128)  # Fade tail
                color = QColor(*comet.color, alpha)
                painter.setBrush(color)
                painter.drawEllipse(int(tail_x), int(tail_y), int(size), int(size))

            # Draw comet head
            head_x = comet.position.x * widget.width()
            head_y = comet.position.y * widget.height()
            painter.setBrush(QColor(*comet.color, 255))
            painter.drawEllipse(
                int(head_x), int(head_y), int(comet.size), int(comet.size)
            )

    def _draw_moon(self, painter: QPainter, widget: QWidget):
        """Draw moon using service data"""
        moon_x, moon_y, moon_size = self.moon_positioning.calculate_moon_position(
            widget.width(), widget.height()
        )

        if self.moon_positioning.should_use_image():
            # Draw actual moon image
            moon_image = self.moon_positioning.get_moon_image()
            if not moon_image.isNull():
                # Scale the image to the moon size
                scaled_image = moon_image.scaled(
                    moon_size,
                    moon_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

                # Draw the moon image
                painter.drawPixmap(moon_x, moon_y, scaled_image)
        else:
            # Fallback to procedural moon
            # Draw moon
            painter.setBrush(QColor(220, 220, 200))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(moon_x, moon_y, moon_size, moon_size)

            # Draw craters
            painter.setBrush(QColor(180, 180, 160))
            for (
                crater_x,
                crater_y,
                crater_size,
            ) in self.moon_positioning.get_crater_positions(moon_x, moon_y, moon_size):
                painter.drawEllipse(crater_x, crater_y, crater_size, crater_size)

    def _draw_ufo(self, painter: QPainter, widget: QWidget):
        """Draw UFO using service data"""
        ufo = self.ufo_behavior.get_ufo_state()
        if ufo:
            ufo_x = ufo.position.x * widget.width()
            ufo_y = ufo.position.y * widget.height()

            if self.ufo_behavior.should_use_image():
                # Draw actual UFO image
                ufo_image = self.ufo_behavior.get_ufo_image()
                if not ufo_image.isNull():
                    # Scale the image to the UFO size
                    scaled_image = ufo_image.scaled(
                        int(ufo.size),
                        int(ufo.size * 0.6),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )

                    # Apply glow effect with opacity
                    glow_intensity = self.ufo_behavior.get_glow_intensity()
                    painter.setOpacity(0.7 + glow_intensity * 0.3)

                    # Draw the UFO image
                    painter.drawPixmap(
                        int(ufo_x - ufo.size / 2),
                        int(ufo_y - ufo.size * 0.3),
                        scaled_image,
                    )

                    painter.setOpacity(1.0)
            else:
                # Fallback to procedural UFO
                glow_intensity = self.ufo_behavior.get_glow_intensity()
                color = QColor(100, 255, 100, int(glow_intensity * 255))
                painter.setBrush(color)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(ufo_x), int(ufo_y), int(ufo.size), int(ufo.size * 0.6)
                )
