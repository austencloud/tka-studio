"""
Header Component for Filter Selection Panel

Displays the main title with proper centering and styling.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QWidget


class FilterHeader(QLabel):
    """Centered, prominent header for the filter panel."""

    def __init__(self, title: str = "Sequence Library", parent: QWidget | None = None):
        super().__init__(title, parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the header styling and alignment."""
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.setStyleSheet("color: white; margin-bottom: 12px;")
