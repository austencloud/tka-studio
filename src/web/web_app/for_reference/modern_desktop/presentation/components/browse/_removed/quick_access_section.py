"""
Quick Access Section - Prominent buttons for most common filters

Features:
- 3 prominent buttons: Favorites, Recently Added, All Sequences
- Glass-morphism styling with accent colors
- Horizontal layout for quick scanning
"""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QWidget

from desktop.modern.domain.models.browse_models import FilterType


class QuickAccessSection(QFrame):
    """Quick access buttons for the most common browse actions."""

    # Signal emitted when a quick filter is selected
    filter_selected = pyqtSignal(FilterType, object)

    # Quick access filter configurations
    QUICK_FILTERS = [
        (
            FilterType.FAVORITES,
            "⭐ My Favorites",
            "Your favorite sequences",
            "#FFD700",  # Gold
        ),
        (
            FilterType.RECENT,
            "🔥 Recently Added",
            "Latest sequences",
            "#FF6B6B",  # Red
        ),
        (
            FilterType.ALL_SEQUENCES,
            "📊 All Sequences",
            "Browse everything",
            "#4ECDC4",  # Teal
        ),
    ]

    def __init__(self, parent: QWidget | None = None):
        """Initialize the quick access section."""
        super().__init__(parent)
        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self) -> None:
        """Setup the UI layout with quick access buttons."""
        # Horizontal layout for side-by-side buttons
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Create quick access buttons
        self.buttons = {}
        for filter_type, label, tooltip, color in self.QUICK_FILTERS:
            button = self._create_quick_button(filter_type, label, tooltip, color)
            self.buttons[filter_type] = button
            layout.addWidget(button)

    def _create_quick_button(
        self, filter_type: FilterType, label: str, tooltip: str, accent_color: str
    ) -> QPushButton:
        """Create a styled quick access button."""
        button = QPushButton(label)
        button.setMinimumHeight(50)
        button.setToolTip(tooltip)

        # Set font
        font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        button.setFont(font)

        # Apply accent color styling
        button.setStyleSheet(
            f"""
            QPushButton {{
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid {accent_color}40;
                border-radius: 12px;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 12px 20px;
                text-align: center;
            }}
            QPushButton:hover {{
                background: {accent_color}20;
                border: 2px solid {accent_color}60;
            }}
            QPushButton:pressed {{
                background: {accent_color}30;
                border: 2px solid {accent_color}80;
            }}
        """
        )

        # Connect to filter selection
        button.clicked.connect(lambda: self._on_quick_filter_clicked(filter_type))

        return button

    def _apply_styling(self) -> None:
        """Apply glass-morphism container styling."""
        self.setStyleSheet(
            """
            QuickAccessSection {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 16px;
                margin: 8px;
            }
        """
        )

    def _on_quick_filter_clicked(self, filter_type: FilterType) -> None:
        """Handle quick filter button click."""
        print(f"🚀 [QUICK ACCESS] {filter_type.value} selected")
        self.filter_selected.emit(filter_type, None)

    def set_active_filter(self, filter_type: FilterType | None) -> None:
        """Highlight the active filter button."""
        for button_filter_type, button in self.buttons.items():
            if button_filter_type == filter_type:
                # Add active state styling
                button.setProperty("active", True)
                button.style().polish(button)
            else:
                # Remove active state
                button.setProperty("active", False)
                button.style().polish(button)
