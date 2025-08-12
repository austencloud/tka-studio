"""
Category Group Component for Filter Selection Panel

Creates individual category sections with 3-column grids of buttons.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget

from desktop.modern.domain.models.browse_models import FilterType

from .category_button import CategoryButton


class CategoryGroup(QWidget):
    """Category group with title and 3-column grid of buttons."""

    filter_selected = pyqtSignal(FilterType, object)

    def __init__(
        self,
        title: str,
        filter_type: FilterType,
        options: list,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.title = title
        self.filter_type = filter_type
        self.options = options
        self.buttons = {}  # {(filter_type, value): button}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the category group layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Category title
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 15, QFont.Weight.Medium))
        title_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.85); margin-bottom: 12px;"
        )
        layout.addWidget(title_label)

        # Options in centered 3-column grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ensure we have exactly 3 or 6 items for clean grid
        display_options = self.options[:6] if len(self.options) > 6 else self.options

        for i, option in enumerate(display_options):
            row = i // 3  # 3 columns
            col = i % 3

            if isinstance(option, tuple):
                label, value = option
            else:
                label, value = option, option

            button = CategoryButton(label)
            button.clicked.connect(lambda _, v=value: self._select_filter(v))
            self.buttons[(self.filter_type, value)] = button

            grid_layout.addWidget(button, row, col)

        layout.addLayout(grid_layout)

    def _select_filter(self, filter_value) -> None:
        """Handle filter selection."""
        self.filter_selected.emit(self.filter_type, filter_value)

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
