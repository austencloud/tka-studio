"""
Prominent Button Component for Filter Selection Panel

Large, accent-colored buttons for quick access options.
"""

from __future__ import annotations

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QWidget


class ProminentButton(QPushButton):
    """Centered, naturally-sized prominent button with accent styling."""

    def __init__(
        self,
        label: str,
        accent_color: str = "#4ECDC4",
        parent: QWidget | None = None,
    ):
        super().__init__(label, parent)
        self.accent_color = accent_color
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the prominent button styling."""
        self.setMinimumHeight(60)
        self.setMinimumWidth(180)  # Minimum width for shorter text
        self.setMaximumWidth(400)  # Maximum width for longer text
        self.setSizePolicy(
            self.sizePolicy().horizontalPolicy(), self.sizePolicy().verticalPolicy()
        )
        self.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self._apply_styling()

    def _apply_styling(self) -> None:
        """Apply the prominent button styles."""
        self.setStyleSheet(f"""
            QPushButton {{
                background: rgba(255, 255, 255, 0.12);
                border: 2px solid {self.accent_color}60;
                border-radius: 14px;
                color: white;
                font-weight: bold;
                padding: 18px 32px;
                text-align: center;
            }}
            QPushButton:hover {{
                background: {self.accent_color}25;
                border: 2px solid {self.accent_color}80;
            }}
            QPushButton:pressed {{
                background: {self.accent_color}35;
            }}
            QPushButton[active="true"] {{
                background: {self.accent_color}40;
                border: 2px solid {self.accent_color};
                box-shadow: 0 6px 20px {self.accent_color}30;
            }}
        """)

    def set_active(self, active: bool) -> None:
        """Set the active state of the button."""
        self.setProperty("active", active)
        style = self.style()
        if style is not None:
            style.polish(self)

    def update_accent_color(self, color: str) -> None:
        """Update the accent color and refresh styling."""
        self.accent_color = color
        self._apply_styling()
