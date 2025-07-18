"""
Tab Management Service

Service for managing application tabs in the modern TKA desktop app.
Handles tab creation, switching, and lifecycle management.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Optional

from PyQt6.QtWidgets import QTabWidget, QWidget

if TYPE_CHECKING:
    from core.dependency_injection.di_container import DIContainer


class ITabManagementService(ABC):
    """Interface for tab management operations."""

    @abstractmethod
    def initialize_tabs(self, tab_widget: QTabWidget, container: "DIContainer") -> None:
        """Initialize all application tabs."""

    @abstractmethod
    def switch_to_tab(self, tab_name: str) -> bool:
        """Switch to the specified tab."""

    @abstractmethod
    def get_current_tab_name(self) -> Optional[str]:
        """Get the name of the currently active tab."""

    @abstractmethod
    def get_available_tabs(self) -> list[str]:
        """Get list of available tab names."""


class TabManagementService(ITabManagementService):
    """Implementation of tab management service."""

    def __init__(self):
        self._tab_widget: Optional[QTabWidget] = None
        self._tabs: Dict[str, QWidget] = {}
        self._tab_index_map: Dict[str, int] = {}
        self._current_tab = "construct"  # Default tab

        # Define available tabs
        self._available_tabs = [
            "construct",
            "browse",
            "learn",
            "sequence_card",
        ]

    def initialize_tabs(self, tab_widget: QTabWidget, container: "DIContainer") -> None:
        """Initialize all application tabs."""
        self._tab_widget = tab_widget

        # Keep tab bar hidden since we use menu bar navigation
        self._tab_widget.tabBar().setVisible(False)

        # Create construct tab (already loaded)
        # Additional tabs will be created on-demand

    def switch_to_tab(self, tab_name: str) -> bool:
        """Switch to the specified tab."""
        if not self._tab_widget:
            print(f"Warning: Tab widget not initialized, cannot switch to {tab_name}")
            return False

        if tab_name not in self._available_tabs:
            print(f"Warning: Unknown tab name: {tab_name}")
            return False

        # If tab doesn't exist yet, create it
        if tab_name not in self._tabs:
            success = self._create_tab_on_demand(tab_name)
            if not success:
                return False

        # Switch to the tab
        if tab_name in self._tab_index_map:
            tab_index = self._tab_index_map[tab_name]
            self._tab_widget.setCurrentIndex(tab_index)
            self._current_tab = tab_name
            print(f"✅ Switched to {tab_name} tab")
            return True

        return False

    def _create_tab_on_demand(self, tab_name: str) -> bool:
        """Create a tab on-demand when first accessed."""
        if tab_name == "construct":
            # Construct tab should already be loaded
            return True

        # Create actual tab implementations
        if tab_name == "browse":
            tab_widget = self._create_browse_tab()
        else:
            # Create placeholder for other tabs
            tab_widget = self._create_placeholder_tab(tab_name)

        # Get display name with emoji
        display_names = {
            "browse": "🔍 Browse",
            "learn": "🧠 Learn",
            "sequence_card": "📋 Sequence Card",
        }

        display_name = display_names.get(tab_name, tab_name.title())

        # Add tab to widget
        tab_index = self._tab_widget.addTab(tab_widget, display_name)

        # Track the tab
        self._tabs[tab_name] = tab_widget
        self._tab_index_map[tab_name] = tab_index

        print(f"✅ Created {tab_name} tab on-demand")
        return True

    def _create_placeholder_tab(self, tab_name: str) -> QWidget:
        """Create a placeholder tab widget."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont
        from PyQt6.QtWidgets import QLabel, QVBoxLayout

        placeholder = QWidget()
        layout = QVBoxLayout(placeholder)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create coming soon message
        label = QLabel(f"🚧 {tab_name.replace('_', ' ').title()} Tab\n\nComing Soon!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Segoe UI", 18, QFont.Weight.Medium))
        label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                background: rgba(40, 40, 40, 0.3);
                border: 2px dashed rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 40px;
                margin: 20px;
            }
        """
        )

        layout.addWidget(label)
        return placeholder

    def _create_browse_tab(self) -> QWidget:
        """Create the actual browse tab widget."""
        from pathlib import Path

        from presentation.tabs.browse import ModernBrowseTab

        # Create browse tab with default paths
        # In a real implementation, these paths would come from configuration
        sequences_dir = Path("data/sequences")  # Default sequences directory
        settings_file = Path("settings.json")  # Default settings file

        browse_tab = ModernBrowseTab(sequences_dir, settings_file)
        return browse_tab

    def get_current_tab_name(self) -> Optional[str]:
        """Get the name of the currently active tab."""
        return self._current_tab

    def get_available_tabs(self) -> list[str]:
        """Get list of available tab names."""
        return self._available_tabs.copy()

    def register_existing_tab(self, tab_name: str, tab_widget: QWidget, tab_index: int):
        """Register an existing tab (like the construct tab that's already loaded)."""
        self._tabs[tab_name] = tab_widget
        self._tab_index_map[tab_name] = tab_index
