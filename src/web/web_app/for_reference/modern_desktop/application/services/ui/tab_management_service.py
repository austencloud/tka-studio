"""
Tab Management Service - SIMPLIFIED VERSION

REFACTORED:
- ✅ Removed complex on-demand tab creation (100+ lines)
- ✅ Simplified switch_to_tab method
- ✅ Tabs are now created upfront by TabFactory
- ✅ Single responsibility: tab switching and registration only

Service for managing application tabs in the modern TKA desktop app.
Handles tab switching and registration - tab creation is handled by TabFactory.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import logging
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QTabWidget, QWidget


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class ITabManagementService(ABC):
    """Interface for tab management operations."""

    @abstractmethod
    def initialize_tabs(self, tab_widget: QTabWidget, container: DIContainer) -> None:
        """Initialize all application tabs."""

    @abstractmethod
    def switch_to_tab(self, tab_name: str) -> bool:
        """Switch to the specified tab."""

    @abstractmethod
    def get_current_tab_name(self) -> str | None:
        """Get the name of the currently active tab."""

    @abstractmethod
    def get_available_tabs(self) -> list[str]:
        """Get list of available tab names."""


class TabManagementService(ITabManagementService):
    """
    SIMPLIFIED tab management service.

    REFACTORED: Removed complex on-demand creation - tabs are now created upfront by TabFactory.
    Single responsibility: Switch between tabs and track current tab.
    """

    def __init__(self):
        self._tab_widget: QTabWidget | None = None
        self._tabs: dict[str, QWidget] = {}
        self._tab_index_map: dict[str, int] = {}
        self._current_tab = "construct"  # Default tab

    def initialize_tabs(self, tab_widget: QTabWidget, container: DIContainer) -> None:
        """
        Initialize tab widget reference.

        SIMPLIFIED: TabFactory handles actual tab creation.
        """
        self._tab_widget = tab_widget

        # Keep tab bar hidden since we use menu bar navigation
        self._tab_widget.tabBar().setVisible(False)

    def switch_to_tab(self, tab_name: str) -> bool:
        """
        Switch to the specified tab.

        SIMPLIFIED: No more on-demand creation - tabs are created upfront.
        """
        if not self._tab_widget:
            logger.warning(f"Tab widget not initialized, cannot switch to {tab_name}")
            return False

        # Check if tab exists
        if tab_name not in self._tabs:
            logger.warning(
                f"Tab {tab_name} not found. Available tabs: {list(self._tabs.keys())}"
            )
            return False

        # Switch to the tab
        if tab_name in self._tab_index_map:
            tab_index = self._tab_index_map[tab_name]
            self._tab_widget.setCurrentIndex(tab_index)
            self._current_tab = tab_name

            return True

        logger.error(
            f"Tab {tab_name} exists but not in index map - this shouldn't happen"
        )
        return False

    def get_current_tab_name(self) -> str | None:
        """Get the name of the currently active tab."""
        return self._current_tab

    def get_available_tabs(self) -> list[str]:
        """Get list of available tab names."""
        return list(self._tabs.keys())

    def register_existing_tab(
        self, tab_name: str, tab_widget: QWidget, tab_index: int
    ) -> None:
        """
        Register an existing tab (called by UISetupManager after TabFactory creates tabs).

        SIMPLIFIED: This is the only way tabs are added now.
        """
        self._tabs[tab_name] = tab_widget
        self._tab_index_map[tab_name] = tab_index
