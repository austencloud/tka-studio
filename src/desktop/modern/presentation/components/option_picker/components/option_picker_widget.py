"""
Option Picker Widget - Clean Service Integration

Main option picker widget that coordinates between services and UI components.
Uses dependency injection to obtain services from DI container.

Key principles:
- Service resolution from DI container
- Clean coordination between services and UI
- No business logic - pure widget composition
"""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

# Services are resolved via DI container - no direct imports needed
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.presentation.components.option_picker.components.option_picker_scroll import (
    OptionPickerScroll,
)


class OptionPickerWidget(QWidget):
    """
    Clean option picker widget with service integration.

    Resolves services from DI container and coordinates UI components.
    """

    # Signal emitted when a pictograph is selected
    pictograph_selected = pyqtSignal(object)  # PictographData

    def __init__(
        self,
        parent=None,
        mw_size_provider: Callable[[], QSize] = None,
        progress_callback: Callable[[str, float], None] | None = None,
        container: DIContainer | None = None,
    ):
        """Initialize with service resolution from DI container."""
        super().__init__(parent)

        self.mw_size_provider = mw_size_provider
        self.progress_callback = progress_callback
        self.container = container

        # ✅ Use DI container to create OptionPickerScroll with injected services
        if not container:
            raise ValueError(
                "DI container is required for OptionPickerWidget - no fallback available"
            )

        try:
            # Use the DI container factory to create OptionPickerScroll with proper service injection
            self.option_picker_scroll = container.resolve(OptionPickerScroll)
            # Set the parent and size provider after creation
            self.option_picker_scroll.setParent(self)
            self.option_picker_scroll.mw_size_provider = self.mw_size_provider
        except Exception as e:
            print(
                f"❌ [OPTION_WIDGET] Failed to resolve OptionPickerScroll from container: {e}"
            )
            raise RuntimeError(f"Failed to create OptionPickerScroll: {e}") from e

        # ✅ Connect Qt signals
        self.option_picker_scroll.pictograph_selected.connect(
            self.pictograph_selected.emit
        )

        # ✅ Add the label to the scroll area at the top
        self.option_picker_scroll.add_header_label(self._create_option_label())

        # ✅ Setup Qt layout with just the scroll area
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)  # No spacing needed since label is inside scroll area

        # Add only the scroll area
        layout.addWidget(self.option_picker_scroll)

        # Report progress
        if self.progress_callback:
            self.progress_callback("Option picker initialized", 1.0)

    def _create_option_label(self) -> QWidget:
        """Create the option label with start position picker styling."""
        # Create title section with same styling as start position picker
        title_section = QWidget()
        title_layout = QVBoxLayout(title_section)
        title_layout.setSpacing(8)
        title_layout.setContentsMargins(16, 16, 16, 16)

        # Title
        title_label = QLabel("Choose Your Next Option")
        title_label.setFont(QFont("Monotype Corsiva", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("UnifiedTitle")
        title_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Select an option to continue building your sequence")
        subtitle_label.setFont(QFont("Monotype Corsiva", 14))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setObjectName("UnifiedSubtitle")
        title_layout.addWidget(subtitle_label)

        title_section.setObjectName("TitleSection")

        # Apply the same styling as start position picker
        title_section.setStyleSheet(self._get_label_styles())

        return title_section

    def _get_label_styles(self) -> str:
        """Get label styling matching start position picker."""
        return """
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

    def refresh_options(self) -> None:
        """Refresh options - clear all sections."""
        self.option_picker_scroll.clear_all_sections()

    def get_widget(self) -> QWidget:
        """Get the main widget for integration."""
        return self

    def load_motion_combinations(self, sequence_data) -> None:
        """Load motion combinations based on sequence data."""
        self.option_picker_scroll.load_options_from_sequence(sequence_data)

    def refresh_from_sequence(self, sequence) -> None:
        """Refresh from sequence data."""
        self.option_picker_scroll.load_options_from_sequence(sequence)

    def prepare_content_for_transition(self) -> None:
        """Prepare content for widget transition by loading without fade animations."""
        if hasattr(self.option_picker_scroll, "prepare_for_transition"):
            self.option_picker_scroll.prepare_for_transition()

    def initialize(self) -> None:
        """Initialize - already done in constructor."""

    def cleanup(self) -> None:
        """Cleanup resources."""
        if hasattr(self, "option_picker_scroll") and self.option_picker_scroll:
            self.option_picker_scroll.clear_all_sections()
