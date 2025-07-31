"""
Base class for modern generation controls.

Provides common UI structure and styling for generation control components.
"""

from typing import Optional

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
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self._title = title
        self._description = description
        self._center_title = center_title
        self._setup_base_ui()

    def _setup_base_ui(self):
        """Setup the base UI structure with minimal styling"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Title with clean styling
        title_label = QLabel(self._title)
        title_font = QFont("Segoe UI", 10, QFont.Weight.Medium)
        title_label.setFont(title_font)

        # Center title if requested
        if self._center_title:
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                padding: 0px;
                background: transparent;
                border: none;
            }
        """
        )
        layout.addWidget(title_label)

        # Description (if provided) with subtle styling
        if self._description:
            desc_label = QLabel(self._description)
            desc_label.setFont(QFont("Segoe UI", 8))
            desc_label.setStyleSheet(
                """
                QLabel {
                    color: rgba(255, 255, 255, 0.6);
                    padding: 0px;
                    background: transparent;
                    border: none;
                }
            """
            )
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        # Content area (to be filled by subclasses)
        self._content_layout = QVBoxLayout()
        self._content_layout.setContentsMargins(0, 4, 0, 0)
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
