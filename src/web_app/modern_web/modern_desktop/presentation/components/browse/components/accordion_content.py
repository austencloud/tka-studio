"""
Accordion Content Component

Expandable content area for accordion sections.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtProperty, pyqtSignal
from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget

from desktop.modern.domain.models.browse_models import FilterType
from desktop.modern.presentation.styles.mixins import StyleMixin

from .category_button import CategoryButton


class AccordionContent(QFrame, StyleMixin):
    """Expandable content area for accordion sections."""

    # Signal emitted when a filter option is selected
    filter_selected = pyqtSignal(FilterType, object)

    def __init__(
        self,
        filter_type: FilterType,
        options: list,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.filter_type = filter_type
        self.options = options
        self.buttons = {}  # {value: button}
        self._content_height = 0
        self._setup_ui()
        self._apply_styling()

    def _create_legacy_letter_layout(self, main_layout: QVBoxLayout) -> None:
        """Create letter layout matching the legacy browse tab organization."""

        # Legacy letter organization from starting_letter_section.py
        LETTER_SECTIONS = [
            [
                ["A", "B", "C", "D", "E", "F"],
                ["G", "H", "I", "J", "K", "L"],
                ["M", "N", "O", "P", "Q", "R"],
                ["S", "T", "U", "V"],
            ],
            [["W", "X", "Y", "Z"], ["Σ", "Δ", "θ", "Ω"]],
            [["W-", "X-", "Y-", "Z-"], ["Σ-", "Δ-", "θ-", "Ω-"]],
            [["Φ", "Ψ", "Λ"]],
            [["Φ-", "Ψ-", "Λ-"]],
            [["α", "β", "Γ"]],
        ]

        # Create option lookup for available letters
        option_dict = {}
        for option in self.options:
            if isinstance(option, tuple):
                label, value = option
            else:
                label, value = option, option
            option_dict[value] = label

        # Create rows exactly like legacy
        for section in LETTER_SECTIONS:
            for row in section:
                # Create horizontal layout for this row
                row_layout = QHBoxLayout()
                row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                row_layout.setSpacing(12)  # More space between buttons in row

                # Add buttons for letters that exist in our data
                for letter in row:
                    if letter in option_dict:
                        button = CategoryButton(letter)
                        button.clicked.connect(
                            lambda _, v=letter: self._select_filter(v)
                        )
                        self.buttons[letter] = button
                        row_layout.addWidget(button)

                # Only add the row if it has buttons
                if row_layout.count() > 0:
                    main_layout.addLayout(row_layout)

    def _setup_ui(self) -> None:
        """Setup the content layout."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 8, 16, 16)
        main_layout.setSpacing(8)

        # Grid layout for options
        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center all buttons

        # Use 6 columns for starting letters, 3 for others
        columns = 6 if self.filter_type.value == "starting_letter" else 3

        # Special handling for starting letters with legacy row-based layout
        if self.filter_type.value == "starting_letter":
            self._create_legacy_letter_layout(main_layout)
        else:
            # Standard grid layout for other filter types
            for i, option in enumerate(self.options):
                row = i // columns
                col = i % columns

                if isinstance(option, tuple):
                    label, value = option
                else:
                    label, value = option, option

                button = CategoryButton(label)
                button.clicked.connect(lambda _, v=value: self._select_filter(v))
                self.buttons[value] = button

                grid_layout.addWidget(button, row, col)

            main_layout.addLayout(grid_layout)

        main_layout.addLayout(grid_layout)

        # Calculate and store content height
        self._calculate_content_height()

    def _calculate_content_height(self) -> None:
        """Calculate the natural height of the content."""
        # Force layout calculation
        self.updateGeometry()
        self.adjustSize()

        # Get the minimum size hint
        size_hint = self.sizeHint()

        # Give starting letter section extra height for better layout
        if self.filter_type.value == "starting_letter":
            self._content_height = (
                size_hint.height() + 120
            )  # More space for legacy rows
        else:
            self._content_height = size_hint.height()

    def _select_filter(self, value) -> None:
        """Handle filter selection."""
        print(f"🎯 [ACCORDION CONTENT] {self.filter_type.value} = {value}")
        self.filter_selected.emit(self.filter_type, value)

    def _apply_styling(self) -> None:
        """Apply glassmorphism styling to the content using standard patterns."""
        self.setStyleSheet(
            """
            AccordionContent {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                margin: 0px 4px 4px 4px;
                padding: 0px;
            }
        """
        )

    @pyqtProperty(int)
    def content_height(self) -> int:
        """Get the natural content height for animations."""
        return self._content_height

    def get_buttons(self) -> dict:
        """Get all buttons for external access."""
        return self.buttons.copy()

    def clear_selection(self) -> None:
        """Clear any visual selection state from buttons."""
        # This can be implemented later if needed for visual feedback
        pass
