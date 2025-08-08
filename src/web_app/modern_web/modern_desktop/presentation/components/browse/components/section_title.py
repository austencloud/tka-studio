"""
Section Title Component for Filter Selection Panel

Reusable component for section headers with consistent styling.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QWidget


class SectionTitle(QLabel):
    """Centered section title with consistent styling."""

    def __init__(self, title: str, parent: QWidget | None = None):
        super().__init__(title, parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the section title styling."""
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Segoe UI", 18, QFont.Weight.DemiBold))
        self.setStyleSheet("color: rgba(255, 255, 255, 0.9); margin-bottom: 16px;")
