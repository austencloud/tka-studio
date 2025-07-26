"""
Shared Picker Title Section - Simple reusable title component
===========================================================

Creates a standardized title section for picker components with glassmorphism styling.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


def create_picker_title_section(title: str, subtitle: str) -> QWidget:
    """
    Create a standardized title section for picker components.

    Args:
        title: Main title text
        subtitle: Subtitle text

    Returns:
        QWidget with title section styling
    """
    title_section = QWidget()
    title_layout = QVBoxLayout(title_section)
    title_layout.setSpacing(8)
    title_layout.setContentsMargins(16, 16, 16, 16)

    # Title
    title_label = QLabel(title)
    title_label.setFont(QFont("Monotype Corsiva", 24, QFont.Weight.Bold))
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setObjectName("UnifiedTitle")
    title_layout.addWidget(title_label)

    # Subtitle
    subtitle_label = QLabel(subtitle)
    subtitle_label.setFont(QFont("Monotype Corsiva", 14))
    subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    subtitle_label.setObjectName("UnifiedSubtitle")
    title_layout.addWidget(subtitle_label)

    title_section.setObjectName("TitleSection")

    # Apply shared styling
    title_section.setStyleSheet(
        """
        QWidget#TitleSection {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 16px;
        }
        
        QLabel#UnifiedTitle {
            color: black;
            background: transparent;
            font-weight: 700;
        }
        
        QLabel#UnifiedSubtitle {
            color: black;
            background: transparent;
            font-weight: 400;
        }
    """
    )

    return title_section


def update_picker_title_section(
    title_section: QWidget, title: str, subtitle: str
) -> None:
    """
    Update an existing title section with new text.

    Args:
        title_section: The title section widget to update
        title: New title text
        subtitle: New subtitle text
    """
    # Find the labels by object name and update their text
    title_label = title_section.findChild(QLabel, "UnifiedTitle")
    subtitle_label = title_section.findChild(QLabel, "UnifiedSubtitle")

    if title_label:
        title_label.setText(title)
    if subtitle_label:
        subtitle_label.setText(subtitle)
