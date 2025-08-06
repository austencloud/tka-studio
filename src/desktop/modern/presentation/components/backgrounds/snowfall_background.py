from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QLinearGradient, QPainter, QPixmap
from PyQt6.QtWidgets import QWidget
from shared.application.services.backgrounds.snowfall.santa_movement import (
    SantaMovement,
)
from shared.application.services.backgrounds.snowfall.shooting_star import ShootingStar
from shared.application.services.backgrounds.snowfall.snowflake_physics import (
    SnowflakePhysics,
)

from .base_background import BaseBackground


if TYPE_CHECKING:
    pass


class SnowfallBackground(BaseBackground):
    snowflake_count = 100

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent

        self.widget_width = 800  # Default width
        self.widget_height = 600  # Default height

        if parent:
            self.widget_width = parent.width()
            self.widget_height = parent.height()

        asset_resolver = AssetPathResolver()
        self.snowflake_images = [
            QPixmap(asset_resolver.get_image_path(f"snowflakes/snowflake{i}.png"))
            for i in range(1, 21)
        ]

        # Use services instead of managers and workers
        self.snowflake_physics = SnowflakePhysics(
            self.snowflake_count,
            self.widget_width,
            self.widget_height,
            len(self.snowflake_images),
        )
        self.shooting_star = ShootingStar()
        self.santa_movement = SantaMovement()

    def paint_background(self, widget: QWidget, painter: QPainter):
        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0, QColor(20, 30, 48))
        gradient.setColorAt(1, QColor(50, 80, 120))
        painter.fillRect(widget.rect(), gradient)

        # Draw snowflakes using service data
        for snowflake in self.snowflake_physics.get_snowflake_states():
            if 0 <= snowflake.image_index < len(self.snowflake_images):
                image = self.snowflake_images[snowflake.image_index]
                size = snowflake.size
                scaled_image = image.scaled(
                    size,
                    size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                painter.drawPixmap(int(snowflake.x), int(snowflake.y), scaled_image)

        # Draw shooting stars and Santa using service data
        self._draw_shooting_star(painter, widget)
        self._draw_santa(painter, widget)

    def _draw_shooting_star(self, painter: QPainter, widget: QWidget):
        """Draw shooting star using service data"""
        shooting_star = self.shooting_star.get_shooting_star_state()
        if shooting_star:
            # Draw shooting star tail
            painter.setBrush(
                QColor(255, 255, 255, int(shooting_star.tail_opacity * 255))
            )
            painter.setPen(Qt.PenStyle.NoPen)

            for i, (x, y, size) in enumerate(shooting_star.tail):
                tail_x = x * widget.width()
                tail_y = y * widget.height()
                alpha = int(
                    (shooting_star.tail_opacity * (i + 1) / len(shooting_star.tail))
                    * 255
                )
                painter.setBrush(QColor(255, 255, 255, alpha))
                painter.drawEllipse(int(tail_x), int(tail_y), int(size), int(size))

            # Draw shooting star head
            head_x = shooting_star.position.x * widget.width()
            head_y = shooting_star.position.y * widget.height()
            painter.setBrush(
                QColor(255, 255, 255, int(shooting_star.tail_opacity * 255))
            )
            painter.drawEllipse(
                int(head_x),
                int(head_y),
                int(shooting_star.size),
                int(shooting_star.size),
            )

    def _draw_santa(self, painter: QPainter, widget: QWidget):
        """Draw Santa using service data"""
        santa = self.santa_movement.get_santa_state()
        if santa:
            # Simple Santa representation - you can replace with actual Santa image
            painter.setBrush(QColor(255, 0, 0, int(santa.opacity * 255)))
            painter.setPen(Qt.PenStyle.NoPen)

            santa_x = santa.x * widget.width()
            santa_y = santa.y * widget.height()
            painter.drawEllipse(int(santa_x), int(santa_y), 40, 40)

    def animate_background(self):
        """Animate background effects using services"""
        self.snowflake_physics.update_snowflakes()
        self.shooting_star.update_shooting_star()
        self.santa_movement.update_santa()
        self.update_required.emit()

    def update_bounds(self, width, height):
        """Handle resizing of the widget and update service bounds"""
        self.widget_width = width
        self.widget_height = height
        self.snowflake_physics.update_bounds(width, height)

    def cleanup(self):
        """Clean up resources - no longer needed with services"""
