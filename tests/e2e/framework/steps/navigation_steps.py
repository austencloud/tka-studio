"""
Navigation Steps for TKA Modern E2E Testing Framework

This module provides the NavigationSteps class that encapsulates
common navigation operations and workflows, making tests more
readable and maintainable.
"""

import logging
from typing import Optional

from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QTabWidget, QWidget

logger = logging.getLogger(__name__)


class NavigationSteps:
    """
    Reusable navigation operations for TKA E2E tests.

    This class provides high-level navigation methods that combine
    multiple page object interactions into meaningful workflow steps.
    """

    def __init__(self, main_window: QWidget):
        """
        Initialize navigation steps.

        Args:
            main_window: Main application window widget
        """
        self.main_window = main_window
        self.start_position_picker = None  # Will be set when needed
        self._construct_tab = None  # Cache for construct tab page object

        logger.debug("NavigationSteps initialized with main window")

    def _ensure_start_position_picker(self) -> bool:
        """
        Ensure start position picker is initialized.

        Returns:
            bool: True if picker is available, False otherwise
        """
        if self.start_position_picker is not None:
            return True

        # Get construct tab page object
        if self._construct_tab is None:
            from tests.e2e.framework.page_objects.construct_tab import ConstructTabPage

            self._construct_tab = ConstructTabPage(self.main_window)

        # Navigate to construct tab if not already there
        if not self._construct_tab.is_loaded():
            if not self._construct_tab.navigate_to_tab():
                logger.error("Failed to navigate to construct tab")
                return False

        # Get start position picker
        self.start_position_picker = self._construct_tab.get_start_position_picker()
        if self.start_position_picker is None:
            logger.error("Failed to get start position picker")
            return False

        logger.debug("Start position picker initialized successfully")
        return True

    def select_start_position(self, position: str) -> bool:
        """
        Select a start position to begin sequence building.

        This is typically the first step in any sequence building workflow.

        Args:
            position: Position identifier (e.g., "alpha1_alpha1")

        Returns:
            bool: True if position selected successfully, False otherwise
        """
        logger.info(f"Navigation: Selecting start position '{position}'")

        if not self._ensure_start_position_picker():
            logger.error("Start position picker not available")
            return False

        # Ensure start position picker is loaded
        if not self.start_position_picker.wait_for_load():
            logger.error("Start position picker failed to load")
            return False

        # Select the position
        if not self.start_position_picker.select_position(position):
            logger.error(f"Failed to select start position '{position}'")
            return False

        logger.info(f"Successfully selected start position '{position}'")
        return True

    def select_first_available_position(self) -> Optional[str]:
        """
        Select the first available start position.

        Useful for tests that don't care about the specific position.

        Returns:
            str or None: Selected position identifier or None if failed
        """
        logger.info("Navigation: Selecting first available start position")

        if not self._ensure_start_position_picker():
            logger.error("Start position picker not available")
            return None

        # Get available positions
        positions = self.start_position_picker.get_available_positions()
        if not positions:
            logger.error("No start positions available")
            return None

        # Select the first position
        first_position = positions[0]
        if self.select_start_position(first_position):
            logger.info(f"Selected first available position: '{first_position}'")
            return first_position

        logger.error("Failed to select first available position")
        return None

    def select_random_position(self) -> Optional[str]:
        """
        Select a random available start position.

        Useful for tests that want to vary the starting position.

        Returns:
            str or None: Selected position identifier or None if failed
        """
        import random

        logger.info("Navigation: Selecting random start position")

        if not self._ensure_start_position_picker():
            logger.error("Start position picker not available")
            return None

        # Get available positions
        positions = self.start_position_picker.get_available_positions()
        if not positions:
            logger.error("No start positions available")
            return None

        # Select a random position
        random_position = random.choice(positions)
        if self.select_start_position(random_position):
            logger.info(f"Selected random position: '{random_position}'")
            return random_position

        logger.error("Failed to select random position")
        return None

    def verify_position_selected(self, expected_position: str) -> bool:
        """
        Verify that the expected position is currently selected.

        Args:
            expected_position: Position that should be selected

        Returns:
            bool: True if position is selected, False otherwise
        """
        logger.debug(f"Verifying position '{expected_position}' is selected")

        if not self._ensure_start_position_picker():
            logger.error("Start position picker not available")
            return False

        current_position = self.start_position_picker.get_current_position()
        if current_position == expected_position:
            logger.debug(f"Position verification successful: '{expected_position}'")
            return True

        logger.warning(
            f"Position verification failed: expected '{expected_position}', got '{current_position}'"
        )
        return False

    def get_available_positions(self) -> list[str]:
        """
        Get list of available start positions.

        Returns:
            List[str]: Available position identifiers
        """
        logger.debug("Getting available start positions")

        if not self._ensure_start_position_picker():
            logger.error("Start position picker not available")
            return []

        positions = self.start_position_picker.get_available_positions()
        logger.debug(f"Found {len(positions)} available positions")

        return positions

    def ensure_position_picker_ready(self) -> bool:
        """
        Ensure the start position picker is ready for interaction.

        Returns:
            bool: True if picker is ready, False otherwise
        """
        logger.debug("Ensuring start position picker is ready")

        if not self._ensure_start_position_picker():
            logger.error("Start position picker not available")
            return False

        # Check if picker is loaded
        if not self.start_position_picker.is_loaded():
            logger.debug("Start position picker not loaded, waiting...")
            if not self.start_position_picker.wait_for_load():
                logger.error("Start position picker failed to load")
                return False

        # Check if positions are available
        positions = self.get_available_positions()
        if not positions:
            logger.error("No start positions available")
            return False

        logger.debug("Start position picker is ready")
        return True

    def navigate_to_position_by_criteria(self, criteria: dict) -> Optional[str]:
        """
        Navigate to a position based on specific criteria.

        Args:
            criteria: Dictionary with selection criteria
                     e.g., {"contains": "alpha"}, {"index": 0}

        Returns:
            str or None: Selected position or None if not found
        """
        logger.info(f"Navigation: Selecting position by criteria: {criteria}")

        positions = self.get_available_positions()
        if not positions:
            logger.error("No positions available for criteria selection")
            return None

        selected_position = None

        # Handle different criteria types
        if "contains" in criteria:
            search_term = criteria["contains"].lower()
            for position in positions:
                if search_term in position.lower():
                    selected_position = position
                    break

        elif "index" in criteria:
            index = criteria["index"]
            if 0 <= index < len(positions):
                selected_position = positions[index]

        elif "exact" in criteria:
            exact_match = criteria["exact"]
            if exact_match in positions:
                selected_position = exact_match

        # Select the found position
        if selected_position:
            if self.select_start_position(selected_position):
                logger.info(f"Selected position by criteria: '{selected_position}'")
                return selected_position
            else:
                logger.error(f"Failed to select position: '{selected_position}'")
        else:
            logger.error(f"No position found matching criteria: {criteria}")

        return None

    def reset_position_selection(self) -> bool:
        """
        Reset or clear the current position selection.

        Returns:
            bool: True if reset successful, False otherwise
        """
        logger.info("Navigation: Resetting position selection")

        # This would depend on the actual UI implementation
        # For now, we'll just refresh the picker state
        if self.start_position_picker:
            self.start_position_picker.clear_cache()
            self.start_position_picker.refresh()

        logger.info("Position selection reset completed")
        return True

    # ========================================
    # TAB NAVIGATION METHODS
    # ========================================

    def navigate_to_construct_tab(self) -> bool:
        """
        Navigate to the construct tab.

        Returns:
            bool: True if navigation successful, False otherwise
        """
        logger.info("Navigating to construct tab")
        return self._navigate_to_tab_by_name("construct", 0)

    def navigate_to_browse_tab(self) -> bool:
        """
        Navigate to the browse tab.

        Returns:
            bool: True if navigation successful, False otherwise
        """
        logger.info("Navigating to browse tab")
        return self._navigate_to_tab_by_name("browse", 1)

    def navigate_to_learn_tab(self) -> bool:
        """
        Navigate to the learn tab.

        Returns:
            bool: True if navigation successful, False otherwise
        """
        logger.info("Navigating to learn tab")
        return self._navigate_to_tab_by_name("learn", 2)

    def navigate_to_sequence_card_tab(self) -> bool:
        """
        Navigate to the sequence card tab.

        Returns:
            bool: True if navigation successful, False otherwise
        """
        logger.info("Navigating to sequence card tab")
        return self._navigate_to_tab_by_name("sequence_card", 3)

    # ========================================
    # HELPER METHODS
    # ========================================

    def _navigate_to_tab_by_name(self, tab_name: str, fallback_index: int) -> bool:
        """
        Navigate to a tab by name or fallback index.

        Args:
            tab_name: Name of the tab to find
            fallback_index: Index to use if name search fails

        Returns:
            bool: True if navigation successful, False otherwise
        """
        tab_widget = self._find_tab_widget()
        if not tab_widget:
            logger.error("Could not find tab widget for navigation")
            return False

        # Try to find tab by name first
        tab_index = self._find_tab_index_by_name(tab_widget, tab_name)
        if tab_index == -1:
            # Fall back to using the provided index
            if fallback_index < tab_widget.count():
                tab_index = fallback_index
                logger.debug(
                    f"Using fallback index {fallback_index} for tab '{tab_name}'"
                )
            else:
                logger.error(
                    f"Tab '{tab_name}' not found and fallback index {fallback_index} is out of range"
                )
                return False

        # Switch to the tab
        current_index = tab_widget.currentIndex()
        if current_index != tab_index:
            logger.debug(f"Switching from tab {current_index} to tab {tab_index}")
            tab_widget.setCurrentIndex(tab_index)
            QTest.qWait(500)  # Wait for tab switch

        # Verify navigation was successful
        if tab_widget.currentIndex() == tab_index:
            logger.info(f"Successfully navigated to {tab_name} tab")
            return True
        else:
            logger.error(f"Failed to navigate to {tab_name} tab")
            return False

    def _find_tab_widget(self) -> Optional[QTabWidget]:
        """
        Find the main tab widget using multiple strategies.

        Returns:
            QTabWidget or None: The main tab widget or None if not found
        """
        # Strategy 1: Direct findChild (fastest)
        tab_widget = self.main_window.findChild(QTabWidget)
        if tab_widget:
            logger.debug("Found tab widget via direct findChild")
            return tab_widget

        # Strategy 2: Search all children
        children = self.main_window.findChildren(QTabWidget)
        if children:
            logger.debug(
                f"Found tab widget in children: {children[0].__class__.__name__}"
            )
            return children[0]

        # Strategy 3: Check central widget
        if hasattr(self.main_window, "centralWidget"):
            central_widget = self.main_window.centralWidget()
            if central_widget:
                central_children = central_widget.findChildren(QTabWidget)
                if central_children:
                    logger.debug(
                        f"Found tab widget in central widget: {central_children[0].__class__.__name__}"
                    )
                    return central_children[0]

        logger.debug("No tab widget found")
        return None

    def _find_tab_index_by_name(self, tab_widget: QTabWidget, tab_name: str) -> int:
        """
        Find the index of a tab by name.

        Args:
            tab_widget: The tab widget to search in
            tab_name: Name of the tab to find

        Returns:
            int: Index of the tab, or -1 if not found
        """
        for i in range(tab_widget.count()):
            tab_text = tab_widget.tabText(i)
            logger.debug(f"Tab {i}: '{tab_text}'")

            # Check for tab by text (case insensitive)
            if tab_name.lower() in tab_text.lower():
                logger.debug(f"Found {tab_name} tab at index {i}")
                return i

        logger.debug(f"{tab_name} tab not found")
        return -1

    def get_current_tab(self) -> str:
        """
        Get the name of the currently active tab.

        Returns:
            str: Name of the current tab, or empty string if not found
        """
        tab_widget = self._find_tab_widget()
        if not tab_widget:
            logger.error("Tab widget not found")
            return ""

        current_index = tab_widget.currentIndex()
        if current_index < 0:
            logger.error("No current tab")
            return ""

        tab_text = tab_widget.tabText(current_index)

        # Map tab text to standard names
        tab_mapping = {
            "🔧 Construct": "construct",
            "🔍 Browse": "browse",
            "🧠 Learn": "learn",
            "📋 Sequence Card": "sequence_card",
        }

        for display_name, standard_name in tab_mapping.items():
            if display_name in tab_text:
                logger.debug(f"Current tab: {standard_name} (display: {tab_text})")
                return standard_name

        # Fallback - return cleaned tab text
        clean_name = tab_text.lower().replace(" ", "_")
        logger.debug(f"Current tab (fallback): {clean_name}")
        return clean_name
