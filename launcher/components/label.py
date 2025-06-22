"""
ModernLabel component for TKA Launcher.

This component provides a modern label with Inter typography and 
multiple text styles (title, subtitle, body, caption).
"""

import logging
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont

logger = logging.getLogger(__name__)


class ModernLabel(QLabel):
    """Modern label with Inter typography."""

    def __init__(self, text="", label_type="body", parent=None):
        super().__init__(text, parent)
        self.label_type = label_type
        self._setup_typography()

    def _setup_typography(self):
        """Apply Inter typography based on label type."""
        font = QFont("Inter", 10)
        font.setStyleHint(QFont.StyleHint.SansSerif)

        if self.label_type == "title":
            font.setPointSize(24)
            font.setWeight(QFont.Weight.Bold)
            color = "#ffffff"
        elif self.label_type == "subtitle":
            font.setPointSize(16)
            font.setWeight(QFont.Weight.Medium)
            color = "rgba(255, 255, 255, 0.8)"
        elif self.label_type == "caption":
            font.setPointSize(12)
            font.setWeight(QFont.Weight.Normal)
            color = "rgba(255, 255, 255, 0.6)"
        else:  # body
            font.setPointSize(14)
            font.setWeight(QFont.Weight.Normal)
            color = "rgba(255, 255, 255, 0.9)"

        self.setFont(font)
        self.setStyleSheet(f"color: {color}; font-family: 'Inter', sans-serif;")
