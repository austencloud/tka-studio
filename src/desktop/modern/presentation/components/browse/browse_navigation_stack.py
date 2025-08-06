"""
Browse Navigation Stack - Panel Switching Logic

Simple stack widget for switching between filter selection and sequence browser.
Handles smooth transitions between the two main browse modes.
"""

from __future__ import annotations

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, pyqtSignal
from PyQt6.QtWidgets import QStackedWidget, QWidget


class BrowseNavigationStack(QStackedWidget):
    """
    Simple stack widget for browse tab navigation.

    Manages switching between filter selection and sequence browser panels
    with smooth animations when transitioning.
    """

    # Signals
    panel_changed = pyqtSignal(str)  # panel_name

    def __init__(self, parent: QWidget | None = None):
        """Initialize the navigation stack."""
        super().__init__(parent)

        self._panels: dict[str, QWidget] = {}
        self._current_panel: str | None = None

        # Setup animations
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(300)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_current_panel(self) -> str | None:
        """Get the name of the currently visible panel."""
        return self._current_panel

    def _animate_to_panel(self, target_widget: QWidget) -> None:
        """Animate transition to target panel."""
        # For now, just do instant switch - can add slide animation later
        self.setCurrentWidget(target_widget)
