"""
OptionPickerLayoutOrchestrator

Orchestrates layout operations and spacing management.
Handles Qt layout management and widget organization.
"""

from __future__ import annotations

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
        option_config_service: OptionConfigurationService,
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
