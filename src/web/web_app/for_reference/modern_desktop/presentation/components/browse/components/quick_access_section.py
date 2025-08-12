"""
Quick Access Section Component for Filter Selection Panel

Handles the prominent quick access buttons (Favorites, Recent, All Sequences).
"""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from desktop.modern.domain.models.browse_models import FilterType

from .prominent_button import ProminentButton


class QuickAccessSection(QWidget):
    """Quick access section with prominent buttons."""

    filter_selected = pyqtSignal(FilterType, object)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.buttons = {}  # {(filter_type, value): button}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the quick access section layout."""
        # Just horizontal layout for buttons (no title, no vertical layout)
        buttons_layout = QHBoxLayout(self)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(12)  # Compact spacing between buttons

        quick_options = [
            (FilterType.FAVORITES, "⭐ My Favorites", "#FFD700"),
            (FilterType.RECENT, "🔥 Recently Added", "#FF6B6B"),
            (FilterType.ALL_SEQUENCES, "📊 All Sequences", "#4ECDC4"),
        ]

        for filter_type, label, color in quick_options:
            button = ProminentButton(label, color)
            button.clicked.connect(
                lambda _, ft=filter_type: self._select_filter(ft, None)
            )
            self.buttons[(filter_type, None)] = button
            buttons_layout.addWidget(button)

        buttons_layout.addStretch()  # Right stretch

    def _select_filter(self, filter_type: FilterType, filter_value) -> None:
        """Handle filter selection."""
        self.filter_selected.emit(filter_type, filter_value)

    def set_active_filter(
        self, filter_type: FilterType | None, filter_value=None
    ) -> None:
        """Set the active filter state."""
        for (button_filter_type, button_value), button in self.buttons.items():
            is_active = (
                button_filter_type == filter_type and button_value == filter_value
            )
            button.set_active(is_active)

    def get_buttons(self) -> dict:
        """Get all buttons for external state management."""
        return self.buttons
