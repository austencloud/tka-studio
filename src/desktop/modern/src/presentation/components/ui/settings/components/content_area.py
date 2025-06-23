"""
Settings dialog content area component.

Manages the stacked widget that displays different settings tabs.
"""

from typing import Dict
from PyQt6.QtWidgets import QStackedWidget, QWidget


class SettingsContentArea(QStackedWidget):
    """Content area component that manages settings tabs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(500)
        self.tabs: Dict[str, QWidget] = {}
        self.tab_order: list = []

    def add_tab(self, tab_name: str, tab_widget: QWidget):
        """Add a new tab to the content area."""
        if tab_name not in self.tabs:
            self.tabs[tab_name] = tab_widget
            self.tab_order.append(tab_name)
            self.addWidget(tab_widget)

    def select_tab(self, index: int):
        """Select a tab by index."""
        if 0 <= index < self.count():
            self.setCurrentIndex(index)

    def select_tab_by_name(self, tab_name: str):
        """Select a tab by name."""
        if tab_name in self.tabs:
            index = self.tab_order.index(tab_name)
            self.select_tab(index)

    def get_tab(self, tab_name: str) -> QWidget:
        """Get a tab widget by name."""
        return self.tabs.get(tab_name)

    def get_current_tab_name(self) -> str:
        """Get the name of the currently selected tab."""
        current_index = self.currentIndex()
        if 0 <= current_index < len(self.tab_order):
            return self.tab_order[current_index]
        return ""

    def refresh_current_tab(self):
        """Refresh the currently selected tab if it has a refresh method."""
        current_widget = self.currentWidget()
        if current_widget and hasattr(current_widget, "refresh"):
            current_widget.refresh()

    def refresh_all_tabs(self):
        """Refresh all tabs that have a refresh method."""
        for tab_widget in self.tabs.values():
            if hasattr(tab_widget, "refresh"):
                tab_widget.refresh()
