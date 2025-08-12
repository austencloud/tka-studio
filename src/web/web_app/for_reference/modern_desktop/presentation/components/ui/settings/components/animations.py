"""
Settings dialog animations component.

Handles fade and other animations for the settings dialog.
"""

from __future__ import annotations

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation
from PyQt6.QtWidgets import QWidget


class SettingsAnimations:
    """Animation handler for the settings dialog."""

    def __init__(self, dialog: QWidget):
        self.dialog = dialog
        self._setup_animations()

    def _setup_animations(self):
        """Setup fade animation for dialog."""
        self.fade_animation = QPropertyAnimation(self.dialog, b"windowOpacity")
        self.fade_animation.setDuration(250)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def fade_in(self):
        """Fade in the dialog."""
        self.dialog.setWindowOpacity(0)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()
