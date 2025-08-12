"""
Settings dialog sidebar component.

Provides navigation between different settings tabs.
"""

from __future__ import annotations

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QListWidget, QListWidgetItem


class SettingsSidebar(QListWidget):
    """Sidebar navigation component for the settings dialog."""

    tab_selected = pyqtSignal(int, str)  # index, tab_name

    def __init__(self, tab_names: list[str], parent=None):
        super().__init__(parent)
        self.tab_names = tab_names
        self._setup_ui()
        self._populate_items()

    def _setup_ui(self):
        """Setup the sidebar UI properties with responsive width."""
        self.setObjectName("settings_sidebar")
        # Reduced width for better responsive fit
        self.setFixedWidth(220)
        self.setSpacing(6)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setIconSize(QSize(24, 24))
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setMouseTracking(True)

        # Connect selection change
        self.currentRowChanged.connect(self._on_selection_changed)

    def _populate_items(self):
        """Populate the sidebar with tab items using accessibility-compliant sizing."""
        for tab_name in self.tab_names:
            item = QListWidgetItem(tab_name)
            # Set 48px height for better touch targets (WCAG compliant)
            item.setSizeHint(QSize(0, 48))
            self.addItem(item)

        # Select first tab by default
        if self.tab_names:
            self.setCurrentRow(0)

    def _on_selection_changed(self, index: int):
        """Handle tab selection change."""
        if 0 <= index < len(self.tab_names):
            tab_name = self.tab_names[index]
            self.tab_selected.emit(index, tab_name)

    def select_tab(self, index: int):
        """Programmatically select a tab by index."""
        if 0 <= index < self.count():
            self.setCurrentRow(index)
