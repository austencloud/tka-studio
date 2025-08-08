"""
Filter Category Section - Organized category with title and sub-options

Features:
- Category title with icon
- Grid of related filter options
- Glass-morphism container styling
- Responsive layout
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.domain.models.browse_models import FilterType


class FilterCategorySection(QFrame):
    """A category section containing related filter options."""

    # Signal emitted when a filter option is selected
    filter_selected = pyqtSignal(FilterType, object)

    def __init__(
        self,
        title: str,
        filter_type: FilterType,
        options: list[str | tuple[str, str, str]],
        grid_columns: int = 3,
        parent: QWidget | None = None,
    ):
        """
        Initialize filter category section.

        Args:
            title: Display title for the category (e.g., "📝 By Sequence Name")
            filter_type: Base filter type for this category
            options: List of filter options - can be strings or (label, value, color) tuples
            grid_columns: Number of columns in the option grid
            parent: Parent widget
        """
        super().__init__(parent)

        self.title = title
        self.filter_type = filter_type
        self.options = options
        self.grid_columns = grid_columns

        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self) -> None:
        """Setup the category UI layout."""
        # Main vertical layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Category title
        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet(
            """
            QLabel {
                color: white;
                background: transparent;
                margin-bottom: 8px;
                padding: 4px;
            }
        """
        )
        layout.addWidget(self.title_label)

        # Options grid
        self.options_widget = QWidget()
        self.options_layout = QGridLayout(self.options_widget)
        self.options_layout.setSpacing(8)
        self.options_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._create_option_buttons()
        layout.addWidget(self.options_widget)

    def _create_option_buttons(self) -> None:
        """Create the grid of option buttons."""
        self.option_buttons = {}

        for i, option in enumerate(self.options):
            row = i // self.grid_columns
            col = i % self.grid_columns

            # Parse option data
            if isinstance(option, tuple) and len(option) >= 2:
                # Styled option with custom label and value
                label = option[0]
                value = option[1]
                color = option[2] if len(option) > 2 else None
            else:
                # Simple string option
                label = str(option)
                value = option
                color = None

            # Create button
            button = self._create_option_button(label, value, color)
            self.option_buttons[value] = button
            self.options_layout.addWidget(button, row, col)

    def _create_option_button(
        self, label: str, value: str, color: str | None = None
    ) -> QPushButton:
        """Create a single option button."""
        button = QPushButton(label)
        button.setMinimumSize(80, 35)

        # Set font
        font = QFont("Segoe UI", 11, QFont.Weight.Medium)
        button.setFont(font)

        # Apply styling based on whether color is provided
        if color:
            # Special colored button (for difficulty levels, etc.)
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background: {color}20;
                    border: 1px solid {color}40;
                    border-radius: 10px;
                    color: white;
                    font-weight: bold;
                    padding: 8px 12px;
                }}
                QPushButton:hover {{
                    background: {color}30;
                    border: 1px solid {color}60;
                }}
                QPushButton:pressed {{
                    background: {color}40;
                }}
            """
            )
        else:
            # Standard button styling
            button.setStyleSheet(
                """
                QPushButton {
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 8px;
                    color: white;
                    font-weight: 500;
                    padding: 8px 12px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.2);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }
                QPushButton:pressed {
                    background: rgba(255, 255, 255, 0.15);
                }
            """
            )

        # Connect to filter selection
        button.clicked.connect(lambda: self._on_option_clicked(value))

        return button

    def _apply_styling(self) -> None:
        """Apply glass-morphism container styling."""
        self.setStyleSheet(
            """
            FilterCategorySection {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 16px;
                margin: 4px;
            }
            FilterCategorySection:hover {
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.25);
            }
        """
        )

    def _on_option_clicked(self, option_value: str) -> None:
        """Handle option button click."""
        print(f"📂 [CATEGORY] {self.filter_type.value} -> {option_value}")
        self.filter_selected.emit(self.filter_type, option_value)

    def set_active_option(self, option_value: str | None) -> None:
        """Highlight the active option button."""
        for value, button in self.option_buttons.items():
            if value == option_value:
                # Add active state
                button.setProperty("active", True)
                button.style().polish(button)
            else:
                # Remove active state
                button.setProperty("active", False)
                button.style().polish(button)
