"""
OptionPickerLayoutOrchestrator

Orchestrates layout operations and spacing management.
Handles Qt layout management and widget organization.
"""

from typing import TYPE_CHECKING, Optional

from PyQt6.QtWidgets import QVBoxLayout, QWidget

if TYPE_CHECKING:
    from shared.application.services.option_picker.option_configuration_service import (
        OptionConfigurationService,
    )


class OptionPickerLayoutOrchestrator:
    """
    Orchestrates layout operations for option picker.

    Responsibilities:
    - Managing Qt layout structure
    - Handling spacing and alignment
    - Coordinating header and section placement
    - Managing layout updates
    """

    def __init__(
        self,
        layout: QVBoxLayout,
        container: QWidget,
        option_config_service: "OptionConfigurationService",
    ):
        self._layout = layout
        self._container = container
        self._option_config_service = option_config_service
        self._header_widget: Optional[QWidget] = None
        self._section_widgets: list[QWidget] = []
        self._group_widgets: list[QWidget] = []

    def add_header_widget(self, header_widget: QWidget) -> None:
        """Add a header widget at the top of the layout."""

        # Store reference for spacing calculations
        self._header_widget = header_widget

        # Insert at the very top
        self._layout.insertWidget(0, header_widget)

        # Apply balanced spacing
        self.apply_balanced_spacing()

    def add_section_widget(self, section_widget: QWidget) -> None:
        """Add a section widget to the layout."""
        self._section_widgets.append(section_widget)
        self._layout.addWidget(section_widget)

    def add_group_widget(self, group_widget: QWidget) -> None:
        """Add a group widget to the layout."""
        self._group_widgets.append(group_widget)
        self._layout.addWidget(group_widget)

    def apply_balanced_spacing(self) -> None:
        """Apply balanced spacing between header-section pairs."""
        if not self._header_widget:
            return

        # Step 1: Remove all existing stretches
        items_to_remove = []
        for i in range(self._layout.count()):
            item = self._layout.itemAt(i)
            if item and item.spacerItem():
                items_to_remove.append(item)

        for item in items_to_remove:
            self._layout.removeItem(item)

        # Step 2: Get all widgets in layout order
        all_widgets = []
        for i in range(self._layout.count()):
            item = self._layout.itemAt(i)
            if item and item.widget():
                all_widgets.append((i, item.widget()))

        # Step 3: Find header-section pair boundaries
        pair_end_indices = []

        for i, (index, widget) in enumerate(all_widgets):
            # Skip the main header
            if widget == self._header_widget:
                continue

            # Check if this is a section or group widget (end of a pair)
            if self._is_section_or_group_widget(widget):
                pair_end_indices.append(index)

        # Step 4: Add stretches after each pair (work backwards to preserve indices)
        for pair_end_index in reversed(pair_end_indices):
            self._layout.insertStretch(pair_end_index + 1)

        # Step 5: Add initial stretch after main header
        header_index = self._find_header_index(all_widgets)
        if header_index >= 0:
            self._layout.insertStretch(header_index + 1)

    def _is_section_or_group_widget(self, widget: QWidget) -> bool:
        """Check if widget is a section or group widget."""
        widget_type = str(type(widget))
        return (
            hasattr(widget, "letter_type")
            or "OptionPickerGroupWidget" in widget_type
            or "OptionPickerSection" in widget_type
        )

    def _find_header_index(self, all_widgets: list[tuple]) -> int:
        """Find the index of the header widget in the layout."""
        for i, (index, widget) in enumerate(all_widgets):
            if widget == self._header_widget:
                return index
        return -1

    def clear_layout(self) -> None:
        """Clear all widgets from the layout."""

        # Remove all widgets
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().hide()

        # Clear references
        self._header_widget = None
        self._section_widgets.clear()
        self._group_widgets.clear()

    def get_layout_info(self) -> dict:
        """Get information about the current layout."""
        return {
            "total_items": self._layout.count(),
            "header_widget": self._header_widget is not None,
            "section_count": len(self._section_widgets),
            "group_count": len(self._group_widgets),
        }

    def validate_layout_integrity(self) -> bool:
        """Validate that layout is in a consistent state."""
        try:
            # Check that layout count matches tracked widgets
            expected_count = 0
            if self._header_widget:
                expected_count += 1
            expected_count += len(self._section_widgets)
            expected_count += len(self._group_widgets)

            # Account for stretches (they're not widgets)
            actual_widget_count = sum(
                1
                for i in range(self._layout.count())
                if self._layout.itemAt(i).widget()
            )

            if actual_widget_count != expected_count:
                print(
                    f"❌ [LAYOUT] Widget count mismatch: expected {expected_count}, found {actual_widget_count}"
                )
                return False

            return True

        except Exception as e:
            print(f"❌ [LAYOUT] Error validating layout: {e}")
            return False
