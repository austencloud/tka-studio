"""
Base class for modern generation controls.

Provides common UI structure and styling for generation control components.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class GenerationControlBase(QWidget):
    """Base class for modern generation controls with minimal styling"""

    def __init__(
        self,
        title: str,
        description: str = "",
        center_title: bool = False,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self._title = title
        self._description = description
        self._center_title = center_title
        self._setup_base_ui()

    def _setup_base_ui(self):
        """Setup base UI following 8px grid system and modern design principles"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # No margins - spacing handled by parent
        layout.setSpacing(4)  # 0.5x base unit between title and content

        # Title with proper typography hierarchy
        title_label = QLabel(self._title)
        title_font = QFont(
            "Segoe UI", 12, QFont.Weight.Medium
        )  # Larger, more readable size
        title_label.setFont(title_font)

        # Center title if requested
        if self._center_title:
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.95);
                padding: 0px;
                background: transparent;
                border: none;
                margin-bottom: 4px;
                font-size: 15px;
                font-weight: 500;
            }
        """
        )
        layout.addWidget(title_label)

        # Skip description for compact layout - rely on tooltips instead
        # This follows the principle of maximizing information density

        # Content area (to be filled by subclasses)
        self._content_layout = QVBoxLayout()
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._create_content_widget())

        # Remove background and borders for clean look
        self.setStyleSheet(
            """
            ModernControlBase {
                background: transparent;
                border: none;
            }
        """
        )

    def _create_content_widget(self) -> QWidget:
        """Create the content widget (override in subclasses)"""
        content_widget = QWidget()
        content_widget.setLayout(self._content_layout)
        content_widget.setStyleSheet("background: transparent;")
        return content_widget
