"""
Settings dialog content area component.

Manages the stacked widget that displays different settings tabs.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QStackedWidget, QWidget


class SettingsContentArea(QStackedWidget):
    """Content area component that manages settings tabs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Reduced minimum width for better responsive fit
        self.setMinimumWidth(400)
        self.tabs: dict[str, QWidget] = {}
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

    def get_tab(self, tab_name: str) -> QWidget:
        """Get a tab widget by name."""
        return self.tabs.get(tab_name)

    def refresh_all_tabs(self):
        """Refresh all tabs that have a refresh method."""
        for tab_widget in self.tabs.values():
            if hasattr(tab_widget, "refresh"):
                tab_widget.refresh()
