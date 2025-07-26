"""
Browse Navigation Manager - Handles navigation between Browse Tab panels

This class is responsible for:
- Managing transitions between filter selection, browser, and viewer panels
- Coordinating panel visibility and state
- Handling navigation signals and events
- Maintaining navigation history and state
"""

import logging
from enum import Enum
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QStackedWidget

logger = logging.getLogger(__name__)


class BrowsePanel(Enum):
    """Enumeration of browse tab panels."""
    FILTER_SELECTION = "filter_selection"
    BROWSER = "browser"
    VIEWER = "viewer"


class BrowseNavigationManager(QObject):
    """
    Manages navigation between different panels in the Browse tab.
    
    Handles transitions between filter selection, browser, and viewer panels
    with proper state management and signal coordination.
    """

    # Signals
    panel_changed = pyqtSignal(str)  # Emitted when panel changes
    navigation_requested = pyqtSignal(str, object)  # Emitted when navigation is requested

    def __init__(self, stacked_widget: QStackedWidget):
        """
        Initialize the browse navigation manager.
        
        Args:
            stacked_widget: The stacked widget containing all panels
        """
        super().__init__()
        self.stacked_widget = stacked_widget
        self.current_panel = BrowsePanel.FILTER_SELECTION
        self.previous_panel: Optional[BrowsePanel] = None
        
        # Panel indices in the stacked widget
        self.panel_indices = {
            BrowsePanel.FILTER_SELECTION: 0,
            BrowsePanel.BROWSER: 1,
            BrowsePanel.VIEWER: 2,
        }

    def navigate_to_filter_selection(self) -> None:
        """Navigate to the filter selection panel."""
        self._navigate_to_panel(BrowsePanel.FILTER_SELECTION)

    def navigate_to_browser(self, filter_data=None) -> None:
        """
        Navigate to the browser panel.
        
        Args:
            filter_data: Optional filter data to pass to the browser
        """
        self._navigate_to_panel(BrowsePanel.BROWSER, filter_data)

    def navigate_to_viewer(self, sequence_data=None) -> None:
        """
        Navigate to the viewer panel.
        
        Args:
            sequence_data: Optional sequence data to pass to the viewer
        """
        self._navigate_to_panel(BrowsePanel.VIEWER, sequence_data)

    def go_back(self) -> bool:
        """
        Navigate back to the previous panel.
        
        Returns:
            True if navigation was successful, False if no previous panel
        """
        if self.previous_panel:
            target_panel = self.previous_panel
            self.previous_panel = None  # Clear to avoid infinite loops
            self._navigate_to_panel(target_panel)
            return True
        return False

    def get_current_panel(self) -> BrowsePanel:
        """Get the current active panel."""
        return self.current_panel

    def get_previous_panel(self) -> Optional[BrowsePanel]:
        """Get the previous panel."""
        return self.previous_panel

    def is_at_filter_selection(self) -> bool:
        """Check if currently at filter selection panel."""
        return self.current_panel == BrowsePanel.FILTER_SELECTION

    def is_at_browser(self) -> bool:
        """Check if currently at browser panel."""
        return self.current_panel == BrowsePanel.BROWSER

    def is_at_viewer(self) -> bool:
        """Check if currently at viewer panel."""
        return self.current_panel == BrowsePanel.VIEWER

    def can_go_back(self) -> bool:
        """Check if back navigation is possible."""
        return self.previous_panel is not None

    def reset_to_filter_selection(self) -> None:
        """Reset navigation to filter selection panel."""
        self.previous_panel = None
        self._navigate_to_panel(BrowsePanel.FILTER_SELECTION)

    def _navigate_to_panel(self, target_panel: BrowsePanel, data=None) -> None:
        """
        Internal method to navigate to a specific panel.
        
        Args:
            target_panel: The panel to navigate to
            data: Optional data to pass with the navigation
        """
        try:
            # Don't navigate if already at target panel
            if self.current_panel == target_panel:
                logger.debug(f"Already at {target_panel.value} panel")
                return

            # Store previous panel for back navigation
            self.previous_panel = self.current_panel

            # Get panel index
            panel_index = self.panel_indices.get(target_panel)
            if panel_index is None:
                logger.error(f"❌ Unknown panel: {target_panel}")
                return

            # Validate panel index
            if panel_index < 0 or panel_index >= self.stacked_widget.count():
                logger.error(f"❌ Invalid panel index: {panel_index}")
                return

            # Switch to the target panel
            self.stacked_widget.setCurrentIndex(panel_index)
            self.current_panel = target_panel

            logger.info(f"📍 Navigated to {target_panel.value} panel")

            # Emit signals
            self.panel_changed.emit(target_panel.value)
            if data is not None:
                self.navigation_requested.emit(target_panel.value, data)

        except Exception as e:
            logger.error(f"❌ Failed to navigate to {target_panel.value}: {e}")

    def get_navigation_breadcrumb(self) -> str:
        """
        Get a breadcrumb string showing current navigation state.
        
        Returns:
            String representation of current navigation
        """
        breadcrumb = self.current_panel.value.replace("_", " ").title()
        if self.previous_panel:
            prev_name = self.previous_panel.value.replace("_", " ").title()
            breadcrumb = f"{prev_name} → {breadcrumb}"
        return breadcrumb

    def get_panel_display_name(self, panel: BrowsePanel) -> str:
        """
        Get display name for a panel.
        
        Args:
            panel: The panel to get display name for
            
        Returns:
            Human-readable panel name
        """
        display_names = {
            BrowsePanel.FILTER_SELECTION: "Filter Selection",
            BrowsePanel.BROWSER: "Sequence Browser",
            BrowsePanel.VIEWER: "Sequence Viewer",
        }
        return display_names.get(panel, panel.value)

    def log_navigation_state(self) -> None:
        """Log current navigation state for debugging."""
        logger.debug(f"Navigation State:")
        logger.debug(f"  Current: {self.get_panel_display_name(self.current_panel)}")
        if self.previous_panel:
            logger.debug(f"  Previous: {self.get_panel_display_name(self.previous_panel)}")
        logger.debug(f"  Breadcrumb: {self.get_navigation_breadcrumb()}")
        logger.debug(f"  Can go back: {self.can_go_back()}")
