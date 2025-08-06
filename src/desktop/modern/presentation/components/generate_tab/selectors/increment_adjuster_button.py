"""
Increment adjuster button component.

A simple round button for incrementing/decrementing values.
"""

from __future__ import annotations

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton


class IncrementAdjusterButton(QPushButton):
    """A custom perfectly round button with hover effects and dynamic styling."""

    def __init__(self, symbol: str, parent=None):
        super().__init__(symbol, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(
            self.sizePolicy().Policy.Fixed, self.sizePolicy().Policy.Fixed
        )
        self.setFixedSize(35, 35)
        self.setFont(QFont("Georgia", 18, QFont.Weight.Bold))
        self._update_style()

    def enterEvent(self, event):
        self.setStyleSheet(self._get_hover_style())

    def leaveEvent(self, event):
        self._update_style()

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        self.setFixedSize(QSize(size, size))
        self._update_style()

    def _update_style(self):
        radius = self.width() // 2
        self.setStyleSheet(self._get_style(radius))

    def _get_style(self, radius):
        return f"""
            QPushButton {{
                background-color: rgba(46, 46, 46, 0.8);
                border: 2px solid rgba(170, 170, 170, 0.6);
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: {radius}px;
                text-align: center;
                padding: 0px;
                margin: 0px;
                line-height: {radius * 2}px;
            }}
            QPushButton:pressed {{
                background-color: rgba(85, 85, 85, 0.8);
                border: 2px solid rgba(221, 221, 221, 0.8);
            }}
        """

    def _get_hover_style(self):
        radius = self.width() // 2
        return f"""
            QPushButton {{
                background-color: rgba(68, 68, 68, 0.8);
                border: 2px solid rgba(255, 255, 255, 0.8);
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: {radius}px;
                text-align: center;
                padding: 0px;
                margin: 0px;
                line-height: {radius * 2}px;
            }}
        """
