"""
Simplified Option Picker - Direct Copy of Legacy Success Pattern

This is the main simplified option picker that directly copies the successful Legacy pattern,
replacing the complex Modern approach with simple Qt widget management.

Key principles from Legacy:
- Simple widget composition without complex orchestration
- Direct factory-based object pool creation
- Natural Qt layout management without business logic interference
- Minimal dependency injection and service complexity
"""

from typing import Callable, Optional

from core.dependency_injection.di_container import DIContainer
from presentation.components.option_picker.core.option_picker_scroll import (
    OptionPickerScroll,
)
from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class OptionPickerWidget(QWidget):
    """
    Simplified option picker using Legacy success pattern.

    Direct replacement for complex Modern OptionPicker with minimal orchestration.
    """

    # Signal emitted when a pictograph is selected
    pictograph_selected = pyqtSignal(object)  # PictographData

    def __init__(
        self,
        parent=None,
        mw_size_provider: Callable[[], QSize] = None,
        progress_callback: Optional[Callable[[str, float], None]] = None,
        container: Optional[DIContainer] = None,
    ):
        super().__init__(parent)
        self.mw_size_provider = mw_size_provider or self._default_size_provider
        self.progress_callback = progress_callback
        self.container = container

        # Note: Factory no longer needed - sections create their own pictographs

        # Create the main widget
        self.option_picker_widget = OptionPickerScroll(
            parent=self, mw_size_provider=self.mw_size_provider, container=container
        )

        # Connect scroll widget's pictograph selection signal to our signal
        self.option_picker_widget.pictograph_selected.connect(
            self.pictograph_selected.emit
        )

        # Setup layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.option_picker_widget)

        # Note: Sections now handle their own pictograph loading via _load_pictographs method

        # Report progress if callback provided
        if self.progress_callback:
            self.progress_callback("Option picker initialized", 1.0)

    def _default_size_provider(self) -> QSize:
        """Default size provider if none provided."""
        return QSize(800, 600)

    def refresh_options(self) -> None:
        """Refresh options - simplified version."""
        # Clear all sections
        self.option_picker_widget.clear_all_sections()

        # Sections will reload their own pictographs automatically
        # No factory needed - sections handle their own data loading

    def clear_options(self) -> None:
        """Clear all options."""
        self.option_picker_widget.clear_all_sections()

    def get_widget(self) -> QWidget:
        """Get the main widget for integration."""
        return self.option_picker_widget

    # Compatibility methods for existing integration points
    def load_motion_combinations(self, sequence_data) -> None:
        """Load motion combinations based on actual sequence data."""
        # Load real options based on sequence state
        self.option_picker_widget.load_options_from_sequence(sequence_data)

    def refresh_from_sequence(self, sequence) -> None:
        """Refresh from sequence with actual data."""
        # Load real options based on sequence state
        self.option_picker_widget.load_options_from_sequence(sequence)

    def initialize(self) -> None:
        """Initialize - already done in constructor."""

    def cleanup(self) -> None:
        """Cleanup resources."""
        # Clear all sections - they handle their own cleanup
        if hasattr(self, "option_picker_widget") and self.option_picker_widget:
            self.option_picker_widget.clear_all_sections()
