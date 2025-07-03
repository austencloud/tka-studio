from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout

if TYPE_CHECKING:
    from presentation.components.option_picker.components.sections.section_widget import (
        OptionPickerSection,
    )


class OptionPickerSectionHeader(QWidget):
    """
    Header widget for option picker sections.
    Contains the type button and handles header-specific layout.
    """

    def __init__(self, section: "OptionPickerSection"):
        super().__init__()
        self.section = section
        self._setup_ui()

    def _setup_ui(self):
        """Setup header layout with centered button."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add stretches to center the button
        layout.addStretch(1)

        # Import and create the button

        from presentation.components.option_picker.components.sections.buttons.section_button import (
            OptionPickerSectionButton,
        )

        self.type_button = OptionPickerSectionButton(self.section)
        layout.addWidget(self.type_button)

        layout.addStretch(1)

        # Connect button signal
        self.type_button.clicked.connect(self._on_button_clicked)

        # Set transparent background
        self.setStyleSheet("background: transparent; border: none;")

    def _on_button_clicked(self):
        """Handle button click to toggle section visibility."""
        self.type_button.toggle_expansion()
        # Signal to parent section to toggle pictograph container
        if hasattr(self.section, "pictograph_container"):
            self.section.section_pictograph_container.setVisible(
                self.type_button.is_expanded
            )

    def get_calculated_height(self) -> int:
        """Calculate the height this header should have."""
        if (
            hasattr(self.section, "mw_size_provider")
            and self.section.option_picker_size_provider
        ):
            parent_height = self.section.option_picker_size_provider().height()
            font_size = max(parent_height // 70, 10)
            # Use legacy calculation: font_size * 3
            return max(int(font_size * 3), 20)
        return 30  # Fallback

    def resize_to_fit(self):
        """Resize header to proper size based on legacy calculation."""
        calculated_height = self.get_calculated_height()
        self.setFixedHeight(calculated_height)

        # Force button to resize as well
        if hasattr(self, "type_button"):
            self.type_button.resize_to_fit()
