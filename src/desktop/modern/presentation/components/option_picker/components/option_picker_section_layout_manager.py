"""
OptionPickerSectionLayoutManager

Handles all layout management and sizing calculations for OptionPickerSection including:
- Grid layout setup and management
- Widget positioning and spacing
- Resize event handling
- Dimension calculations
- Scroll area readiness detection

Extracted from OptionPickerSection to follow Single Responsibility Principle.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import QFrame, QGridLayout, QGroupBox, QSizePolicy, QVBoxLayout
from shared.application.services.option_picker.option_configuration_service import (
    OptionConfigurationService,
)
from shared.application.services.option_picker.option_picker_size_calculator import (
    OptionPickerSizeCalculator,
)

from desktop.modern.presentation.components.option_picker.components.option_pictograph import (
    OptionPictograph,
)
from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)


if TYPE_CHECKING:
    from desktop.modern.presentation.components.option_picker.components.option_picker_scroll import (
        OptionPickerScroll,
    )


class OptionPickerSectionLayoutManager:
    """
    Handles layout management and sizing for OptionPickerSection.

    Responsibilities:
    - Grid layout setup and management
    - Widget positioning calculations
    - Resize event handling
    - Dimension calculations
    - Scroll area readiness detection
    """

    def __init__(
        self,
        section_widget: QGroupBox,
        letter_type: LetterType,
        scroll_area: OptionPickerScroll,
        option_config_service: OptionConfigurationService,
        size_calculator: OptionPickerSizeCalculator,
        mw_size_provider: Callable[[], QSize] | None = None,
    ):
        """Initialize layout manager."""
        self._section_widget = section_widget
        self._letter_type = letter_type
        self._scroll_area = scroll_area
        self._option_config_service = option_config_service
        self._size_calculator = size_calculator
        self._mw_size_provider = mw_size_provider

        # Layout components
        self._main_layout: QVBoxLayout | None = None
        self._pictograph_frame: QFrame | None = None
        self._pictographs_layout: QGridLayout | None = None

        # State tracking
        self._ui_initialized = False
        self._scroll_area_ready = False
        self._calculated_width: int | None = None

    def setup_layout(self, header_widget) -> None:
        """Setup the complete layout structure."""
        # Main vertical layout for header + pictographs
        self._main_layout = QVBoxLayout(self._section_widget)
        self._main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self._main_layout.setSpacing(0)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        # Create container frame for pictographs
        self._pictograph_frame = QFrame(self._section_widget)
        self._pictograph_frame.setStyleSheet("QFrame {border: none;}")

        # Set expanding size policy like legacy
        self._pictograph_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        # Get layout config from service
        layout_config = self._option_config_service.get_layout_config()

        # Grid layout for pictographs
        self._pictographs_layout = QGridLayout(self._pictograph_frame)
        self._pictographs_layout.setSpacing(layout_config["spacing"])
        self._pictographs_layout.setContentsMargins(0, 0, 0, 0)
        self._pictographs_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add header first, then pictograph frame
        self._main_layout.addWidget(header_widget)
        self._main_layout.addWidget(self._pictograph_frame)

        # Mark UI as initialized
        self._ui_initialized = True
        self._check_scroll_area_readiness()

    def add_widget_to_grid(self, widget: OptionPictograph, position: int) -> None:
        """Add widget to grid layout at calculated position."""
        if not self.is_layout_initialized():
            raise RuntimeError("Layout not initialized. Call setup_layout() first.")

        # Use service for grid layout calculation
        layout_config = self._option_config_service.get_layout_config()
        column_count = layout_config["column_count"]

        # Calculate grid position (position is 0-based)
        row, col = divmod(position, column_count)

        # Add to Qt grid layout
        self._pictographs_layout.addWidget(widget, row, col)
        widget.setVisible(True)

    def remove_widget_from_grid(self, widget: OptionPictograph) -> None:
        """Remove widget from grid layout."""
        if self._pictographs_layout:
            self._pictographs_layout.removeWidget(widget)
            widget.setVisible(False)

    def clear_grid_layout(self) -> None:
        """Clear all widgets from grid layout."""
        if not self._pictographs_layout:
            return

        # Remove all widgets from layout
        while self._pictographs_layout.count():
            child = self._pictographs_layout.takeAt(0)
            if child.widget():
                widget = child.widget()
                widget.setVisible(False)
                # CRITICAL FIX: Remove widget from parent to prevent findChildren() from finding it
                if widget.parent():
                    widget.setParent(None)

    def handle_resize_event(self, loading_options: bool) -> bool:
        """
        Handle resize events with proper initialization checks.

        Returns:
            True if resize was handled, False if it should be skipped
        """
        # Skip resizing during option loading
        if loading_options:
            return False

        # Only proceed if UI is properly initialized and scroll area is ready
        if not self._ui_initialized:
            return False

        # Check if scroll area is ready, and if not, try to make it ready
        if not self._scroll_area_ready:
            self._check_scroll_area_readiness()
            if not self._scroll_area_ready:
                return False

        # If we get here, everything is ready - perform the resize
        self._perform_delayed_resize()
        return True

    def update_option_picker_width(self, width: int) -> None:
        """Update the stored option picker width and check readiness."""
        # Store the width for potential future use
        self._option_picker_width = width

        # Check if scroll area is now ready for sizing
        self._check_scroll_area_readiness()

    def _check_scroll_area_readiness(self) -> None:
        """Check if scroll area has valid dimensions and mark as ready."""
        if not self._ui_initialized:
            return

        if not self._scroll_area:
            return

        scroll_width = self._scroll_area.width()
        parent_width = (
            self._scroll_area.parent().width() if self._scroll_area.parent() else 0
        )

        # More robust validation - check if we have a reasonable width
        is_reasonable_width = (
            scroll_width > 800
        )  # Should be much larger than 640px default
        is_not_default = scroll_width != 640  # Avoid the default fallback value
        has_parent_width = parent_width > 800  # Parent should also be properly sized

        if is_reasonable_width and is_not_default and has_parent_width:
            if not self._scroll_area_ready:
                self._scroll_area_ready = True
                # Trigger a resize now that we're ready
                self._perform_delayed_resize()

    def _perform_delayed_resize(self) -> None:
        """Perform resize calculation now that scroll area is ready."""
        if not self._scroll_area_ready or not self._ui_initialized:
            return

        scroll_area_width = self._scroll_area.width()

        # Calculate dimensions using only scroll area width
        dimensions = self._size_calculator.calculate_section_dimensions(
            letter_type=self._letter_type,
            main_window_width=scroll_area_width,  # Use scroll area width directly
        )

        # Store the calculated width
        self._calculated_width = dimensions["width"]

        # Apply the calculated width
        self._section_widget.setFixedWidth(dimensions["width"])

        # Show actual dimensions after Qt applies them
        QTimer.singleShot(10, self._show_actual_dimensions)

    def _show_actual_dimensions(self) -> None:
        """Show actual widget dimensions after Qt applies them (for debugging)."""
        actual_width = self._section_widget.width()
        actual_height = self._section_widget.height()

        # Calculate layout metrics if we have pictographs
        if self._pictographs_layout and self._pictographs_layout.count() > 0:
            # Get first widget for size reference
            first_item = self._pictographs_layout.itemAt(0)
            if first_item and first_item.widget():
                frame_width = first_item.widget().width()
                frame_height = first_item.widget().height()

                # Calculate if 8 frames + spacing fit within section width
                spacing = self._option_config_service.get_layout_config()["spacing"]
                total_frames_width = 8 * frame_width + 7 * spacing
                fits = total_frames_width <= actual_width

                # This could be used for debugging or metrics
                # Currently just calculated for potential future use

    def get_pictograph_frame(self) -> QFrame | None:
        """Get the pictograph container frame."""
        return self._pictograph_frame

    def get_pictographs_layout(self) -> QGridLayout | None:
        """Get the pictographs grid layout."""
        return self._pictographs_layout

    def is_ui_initialized(self) -> bool:
        """Check if UI components are initialized."""
        return self._ui_initialized

    def is_scroll_area_ready(self) -> bool:
        """Check if scroll area is ready for sizing calculations."""
        return self._scroll_area_ready

    def get_calculated_width(self) -> int | None:
        """Get the last calculated width."""
        return self._calculated_width

    def is_layout_initialized(self) -> bool:
        """Check if the layout has been initialized."""
        return self._pictographs_layout is not None and self._ui_initialized

    def toggle_pictograph_frame_visibility(self) -> None:
        """Toggle visibility of the pictograph frame."""
        if self._pictograph_frame:
            is_visible = not self._pictograph_frame.isVisible()
            self._pictograph_frame.setVisible(is_visible)
