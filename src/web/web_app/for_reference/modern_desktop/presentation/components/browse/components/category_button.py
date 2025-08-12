"""
Category Button Component for Filter Selection Panel

Smaller buttons used in category grids with consistent styling.
"""

from __future__ import annotations

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QWidget


class CategoryButton(QPushButton):
    """Naturally-sized category button for grid layouts."""

    def __init__(self, label: str, parent: QWidget | None = None):
        super().__init__(label, parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the category button styling."""
        self.setMinimumSize(90, 40)
        self.setMaximumWidth(140)
        self.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        self._apply_styling()

    def _apply_styling(self) -> None:
        """Apply the category button styles."""
        self.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.10);
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 10px;
                color: rgba(255, 255, 255, 0.9);
                padding: 12px 16px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.18);
                border: 1px solid rgba(255, 255, 255, 0.4);
                color: white;
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.15);
            }
            QPushButton[active="true"] {
                background: rgba(74, 144, 226, 0.6);
                border: 1px solid #4A90E2;
                color: white;
                font-weight: bold;
            }
        """)

    def set_active(self, active: bool) -> None:
        """Set the active state of the button."""
        self.setProperty("active", active)
        style = self.style()
        if style is not None:
            style.polish(self)
