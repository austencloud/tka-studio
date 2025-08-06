"""
Navigation Handler Service

Service for handling navigation and scrolling within the sequence browser.
"""

from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QGridLayout, QLabel, QScrollArea

from desktop.modern.core.interfaces.browse_services import INavigationHandler


class NavigationHandlerService(INavigationHandler):
    """Service for handling navigation and scrolling."""

    def __init__(
        self,
        scroll_area: QScrollArea,
        grid_layout: QGridLayout,
        navigation_sidebar: Optional = None,
    ):
        """Initialize with UI components."""
        self.scroll_area = scroll_area
        self.grid_layout = grid_layout
        self.navigation_sidebar = navigation_sidebar

    def scroll_to_section(self, section_name: str) -> None:
        """Scroll to a specific section in the grid."""
        print(f"🧭 Navigating to section: {section_name}")

        # Find the section header widget
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()

                # Check if this widget contains a label with the section name
                if (
                    hasattr(widget, "findChild")
                    and widget.findChild(QLabel)
                    and widget.findChild(QLabel).text() == section_name
                ):
                    # Calculate scroll position
                    header_global_pos = widget.mapToGlobal(QPoint(0, 0))
                    content_widget_pos = self.scroll_area.widget().mapFromGlobal(
                        header_global_pos
                    )
                    vertical_pos = content_widget_pos.y()

                    # Scroll to the section
                    self.scroll_area.verticalScrollBar().setValue(vertical_pos)
                    return

        # If section not found, scroll to top
        self.scroll_area.verticalScrollBar().setValue(0)

    def update_navigation_sections(
        self, section_names: list[str], sort_method: str
    ) -> None:
        """Update the navigation sidebar with new sections."""
        if self.navigation_sidebar:
            self.navigation_sidebar.update_sections(section_names, sort_method)

    def set_scroll_position(self, position: int) -> None:
        """Set the vertical scroll position."""
        self.scroll_area.verticalScrollBar().setValue(position)
