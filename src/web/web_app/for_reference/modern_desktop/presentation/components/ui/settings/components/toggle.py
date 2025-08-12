"""
Toggle switch component with glassmorphism styling.
"""

from __future__ import annotations

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QRect, Qt
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen
from PyQt6.QtWidgets import QCheckBox


class Toggle(QCheckBox):
    """Modern toggle switch with smooth animations."""

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)

        self._switch_width = 50
        self._switch_height = 25
        self._thumb_radius = 10
        self._track_radius = 12
        self._margin = 3
        self._thumb_position = 0.0

        # Animation
        self._animation = QPropertyAnimation(self, b"thumb_position")
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._animation.setDuration(200)

        self.stateChanged.connect(self._animate_toggle)

        self.setFixedSize(self._switch_width, self._switch_height)

    @property
    def thumb_position(self):
        """Get the thumb position for animation."""
        return self._thumb_position

    @thumb_position.setter
    def thumb_position(self, value):
        """Set the thumb position for animation."""
        self._thumb_position = value
        self.update()

    def _animate_toggle(self, checked):
        """Animate toggle switch."""
        start_pos = 0.0 if not checked else 1.0
        end_pos = 1.0 if checked else 0.0

        self._animation.setStartValue(start_pos)
        self._animation.setEndValue(end_pos)
        self._animation.start()

    def paintEvent(self, event):
        """Custom paint event for toggle switch."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Track
        track_color = (
            QColor(42, 130, 218, 150)
            if self.isChecked()
            else QColor(100, 100, 100, 100)
        )
        painter.setBrush(QBrush(track_color))
        painter.setPen(Qt.PenStyle.NoPen)

        track_rect = QRect(0, 0, self._switch_width, self._switch_height)
        painter.drawRoundedRect(track_rect, self._track_radius, self._track_radius)

        # Thumb
        thumb_x = (
            self._margin
            + (self._switch_width - 2 * self._margin - 2 * self._thumb_radius)
            * self._thumb_position
        )
        thumb_y = self._margin

        thumb_color = QColor(255, 255, 255, 240)
        painter.setBrush(QBrush(thumb_color))
        painter.setPen(QPen(QColor(200, 200, 200, 100), 1))

        painter.drawEllipse(
            int(thumb_x), int(thumb_y), 2 * self._thumb_radius, 2 * self._thumb_radius
        )

    def mousePressEvent(self, event):
        """Handle mouse press."""
        super().mousePressEvent(event)
        self.setChecked(not self.isChecked())
