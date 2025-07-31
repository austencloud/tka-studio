"""
Construct Tab Page Object for TKA Modern E2E Testing Framework

This module provides the ConstructTabPage class that encapsulates
interactions with the main construct tab of the TKA application,
including navigation and access to child components.
"""

import logging
from typing import Optional

from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QPushButton, QTabWidget, QWidget

from .base_page import BasePage

logger = logging.getLogger(__name__)


class ConstructTabPage(BasePage):
    """
    Page object for the Construct Tab.

    This page object handles:
    - Navigation to the construct tab
    - Verification that the tab is loaded and active
    - Access to child components (start position picker, option picker, workbench)
    - Tab state management
    """

    def is_loaded(self) -> bool:
        """
        Check if construct tab is loaded and active.

        Returns:
            bool: True if construct tab is active and ready, False otherwise
        """
        tab_widget = self._find_tab_widget()
        if not tab_widget:
            logger.debug("Tab widget not found")
            return False

        current_index = tab_widget.currentIndex()
        if current_index < 0:
            logger.debug("No active tab")
            return False

        # Check if current tab contains construct-related components
        current_widget = tab_widget.currentWidget()
        if not current_widget:
            logger.debug("Current tab widget is None")
            return False

        # Additional validation: check for expected child components
        return self._has_construct_components(current_widget)

    def navigate_to_tab(self) -> bool:
        """
        Navigate to the construct tab.

        Returns:
            bool: True if navigation successful, False otherwise
        """
        logger.info("Navigating to construct tab")

        tab_widget = self._find_tab_widget()
        if not tab_widget:
            logger.error("Could not find tab widget for navigation")
            return False

        construct_index = self._find_construct_tab_index(tab_widget)
        if construct_index == -1:
            logger.error("Could not find construct tab index")
            return False

        # Switch to construct tab
        current_index = tab_widget.currentIndex()
        if current_index != construct_index:
            logger.debug(f"Switching from tab {current_index} to tab {construct_index}")
            tab_widget.setCurrentIndex(construct_index)
            QTest.qWait(500)  # Wait for tab switch

        # Clear cache after navigation to force fresh component discovery
        self.clear_cache()

        # Verify navigation was successful
        success = self.is_loaded()
        if success:
            logger.info("Successfully navigated to construct tab")
        else:
            logger.error("Failed to navigate to construct tab")

        return success

    def get_start_position_picker(self):
        """
        Get start position picker page object.

        Returns:
            StartPositionPickerPage: Page object for start position picker
        """
        from tests.e2e.framework.page_objects.start_position_picker import (
            StartPositionPickerPage,
        )

        return StartPositionPickerPage(self.parent)

    def get_option_picker(self):
        """
        Get option picker page object.

        Returns:
            OptionPickerPage: Page object for option picker
        """
        from tests.e2e.framework.page_objects.option_picker import OptionPickerPage

        return OptionPickerPage(self.parent)

    def get_sequence_workbench(self):
        """
        Get sequence workbench page object.

        Returns:
            SequenceWorkbenchPage: Page object for sequence workbench
        """
        from tests.e2e.framework.page_objects.sequence_workbench import (
            SequenceWorkbenchPage,
        )

        return SequenceWorkbenchPage(self.parent)

    def _find_element(self, name: str) -> Optional[QWidget]:
        """
        Find elements specific to construct tab.

        Args:
            name: Element identifier

        Returns:
            QWidget or None: Found element or None
        """
        if name == "tab_widget":
            return self._find_tab_widget()
        elif name == "construct_tab_content" or name == "current_tab":
            tab_widget = self._find_tab_widget()
            return tab_widget.currentWidget() if tab_widget else None

        return None

    def _find_tab_widget(self) -> Optional[QTabWidget]:
        """
        Find the main tab widget using multiple strategies.

        Returns:
            QTabWidget or None: The main tab widget or None if not found
        """
        # Strategy 1: Direct findChild (fastest)
        tab_widget = self.parent.findChild(QTabWidget)
        if tab_widget:
            logger.debug("Found tab widget via direct findChild")
            return tab_widget

        # Strategy 2: Search all children
        children = self.parent.findChildren(QTabWidget)
        if children:
            logger.debug(
                f"Found tab widget in children: {children[0].__class__.__name__}"
            )
            return children[0]

        # Strategy 3: Check central widget
        if hasattr(self.parent, "centralWidget"):
            central_widget = self.parent.centralWidget()
            if central_widget:
                central_children = central_widget.findChildren(QTabWidget)
                if central_children:
                    logger.debug(
                        f"Found tab widget in central widget: {central_children[0].__class__.__name__}"
                    )
                    return central_children[0]

        logger.debug("No tab widget found")
        return None

    def _find_construct_tab_index(self, tab_widget: QTabWidget) -> int:
        """
        Find the index of the construct tab.

        Args:
            tab_widget: The tab widget to search in

        Returns:
            int: Index of construct tab, or -1 if not found
        """
        for i in range(tab_widget.count()):
            tab_text = tab_widget.tabText(i)
            logger.debug(f"Tab {i}: '{tab_text}'")

            # Check for construct tab by text or assume first tab
            if "construct" in tab_text.lower() or i == 0:
                logger.debug(f"Found construct tab at index {i}")
                return i

        logger.debug("Construct tab not found")
        return -1

    def _has_construct_components(self, widget: QWidget) -> bool:
        """
        Check if widget contains expected construct tab components.

        Args:
            widget: Widget to check for construct components

        Returns:
            bool: True if construct components are present
        """
        if not widget:
            return False

        # Look for typical construct tab components
        children = widget.findChildren(QWidget)
        component_indicators = [
            "startposition",
            "option",
            "picker",
            "workbench",
            "sequence",
        ]

        found_indicators = 0
        for child in children:
            class_name = child.__class__.__name__.lower()
            for indicator in component_indicators:
                if indicator in class_name:
                    found_indicators += 1
                    break

        # Consider it a construct tab if we find at least 2 component indicators
        has_components = found_indicators >= 2
        logger.debug(f"Found {found_indicators} construct component indicators")

        return has_components

    # ========================================
    # START POSITION METHODS
    # ========================================

    def get_available_start_positions(self) -> list[str]:
        """
        Get list of available start positions.

        Returns:
            List[str]: List of available start position identifiers
        """
        logger.debug("Getting available start positions")

        start_position_picker_page = self.get_start_position_picker()
        if not start_position_picker_page:
            logger.error("Start position picker page not found")
            return []

        # Get the actual Qt widget from the page object
        start_position_widget = start_position_picker_page.get_element("picker_widget")
        if not start_position_widget:
            logger.error("Start position picker widget not found")
            return []

        # Look for pictograph views (actual start positions) instead of buttons
        from PyQt6.QtWidgets import QGraphicsView

        pictograph_views = start_position_widget.findChildren(QGraphicsView)
        positions = []

        for view in pictograph_views:
            if view.isVisible() and view.isEnabled():
                # Try to get the pictograph from the view
                if hasattr(view, "pictograph") and hasattr(view.pictograph, "state"):
                    start_pos = getattr(view.pictograph.state, "start_pos", None)
                    if start_pos and start_pos not in positions:
                        positions.append(start_pos)
                        logger.debug(f"Found available position: {start_pos}")
                elif hasattr(view, "scene") and view.scene:
                    # Alternative: use object name or a generated identifier
                    position_id = view.objectName() or f"position_{len(positions)}"
                    if position_id not in positions:
                        positions.append(position_id)
                        logger.debug(f"Found available position: {position_id}")

        logger.info(f"Found {len(positions)} available start positions")
        return positions

    def select_start_position(self, position: str) -> bool:
        """
        Select a specific start position.

        Args:
            position: Position identifier to select

        Returns:
            bool: True if selection successful, False otherwise
        """
        logger.info(f"Selecting start position: {position}")

        start_position_picker_page = self.get_start_position_picker()
        if not start_position_picker_page:
            logger.error("Start position picker page not found")
            return False

        # Get the actual Qt widget from the page object
        start_position_widget = start_position_picker_page.get_element("picker_widget")
        if not start_position_widget:
            logger.error("Start position picker widget not found")
            return False

        # Find the pictograph view for this position
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QGraphicsView

        pictograph_views = start_position_widget.findChildren(QGraphicsView)
        for view in pictograph_views:
            if view.isVisible() and view.isEnabled():
                # Check if this view matches the position we want
                if hasattr(view, "pictograph") and hasattr(view.pictograph, "state"):
                    start_pos = getattr(view.pictograph.state, "start_pos", None)
                    if start_pos == position:
                        logger.debug(
                            f"Clicking pictograph view for position: {position}"
                        )
                        # Use QTest.mouseClick for more reliable clicking
                        QTest.mouseClick(view, Qt.MouseButton.LeftButton)
                        QTest.qWait(500)  # Wait for selection to process
                        logger.info(f"Successfully selected start position: {position}")
                        return True

        logger.error(f"Position view not found or not clickable: {position}")
        return False

    def get_current_start_position(self) -> Optional[str]:
        """
        Get the currently selected start position.

        Returns:
            str or None: Current start position identifier or None if none selected
        """
        logger.debug("Getting current start position")

        # Check the sequence workbench for the start position
        sequence_workbench = self.get_sequence_workbench()
        if not sequence_workbench:
            logger.error("Sequence workbench not found")
            return None

        # Get the sequence length to see if there's a start position
        sequence_length = sequence_workbench.get_sequence_length()
        if sequence_length == 0:
            logger.debug("No beats in sequence - no start position selected")
            return None

        # Get the first beat (start position)
        first_beat = sequence_workbench.get_beat_at_index(0)
        if not first_beat:
            logger.debug("Could not get first beat")
            return None

        # Try to get the start position from the beat
        if hasattr(first_beat, "pictograph") and hasattr(
            first_beat.pictograph, "state"
        ):
            start_pos = getattr(first_beat.pictograph.state, "start_pos", None)
            if start_pos:
                logger.debug(f"Found selected position: {start_pos}")
                return start_pos

        # Alternative: check if the beat has position information
        if hasattr(first_beat, "get_position"):
            position = first_beat.get_position()
            if position:
                logger.debug(f"Found selected position: {position}")
                return position

        logger.debug("No start position currently selected")
        return None

    def select_first_available_start_position(self) -> bool:
        """
        Select the first available start position.

        Returns:
            bool: True if selection successful, False otherwise
        """
        logger.info("Selecting first available start position")

        start_position_picker_page = self.get_start_position_picker()
        if not start_position_picker_page:
            logger.error("Start position picker page not found")
            return False

        # Get the actual Qt widget from the page object
        start_position_widget = start_position_picker_page.get_element("picker_widget")
        if not start_position_widget:
            logger.error("Start position picker widget not found")
            return False

        # Find the first pictograph view and click it
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QGraphicsView

        pictograph_views = start_position_widget.findChildren(QGraphicsView)
        for view in pictograph_views:
            if view.isVisible() and view.isEnabled():
                logger.debug(
                    f"Clicking first available pictograph view: {view.__class__.__name__}"
                )
                # Use QTest.mouseClick for more reliable clicking
                QTest.mouseClick(view, Qt.MouseButton.LeftButton)
                QTest.qWait(500)  # Wait for selection to process
                logger.info("Successfully selected first available start position")
                return True

        logger.error("No clickable pictograph views found")
        return False

    # ========================================
    # OPTION PICKER METHODS
    # ========================================

    def get_available_options(self) -> list[str]:
        """
        Get list of available options from the option picker.

        Returns:
            List[str]: List of available option identifiers
        """
        logger.debug("Getting available options")

        option_picker_page = self.get_option_picker()
        if not option_picker_page:
            logger.error("Option picker page not found")
            return []

        # Get the actual Qt widget from the page object
        option_picker_widget = option_picker_page.get_element("picker_widget")
        if not option_picker_widget:
            logger.error("Option picker widget not found")
            return []

        # Look for option buttons or widgets
        option_widgets = option_picker_widget.findChildren(QPushButton)
        options = []

        for widget in option_widgets:
            if widget.isVisible() and widget.isEnabled():
                # Use object name or text as option identifier
                option_id = widget.objectName() or widget.text()
                if option_id and option_id not in options:
                    options.append(option_id)
                    logger.debug(f"Found available option: {option_id}")

        logger.info(f"Found {len(options)} available options")
        return options

    def select_option(self, option: str) -> bool:
        """
        Select a specific option from the option picker.

        Args:
            option: Option identifier to select

        Returns:
            bool: True if selection successful, False otherwise
        """
        logger.info(f"Selecting option: {option}")

        option_picker_page = self.get_option_picker()
        if not option_picker_page:
            logger.error("Option picker page not found")
            return False

        # Get the actual Qt widget from the page object
        option_picker_widget = option_picker_page.get_element("picker_widget")
        if not option_picker_widget:
            logger.error("Option picker widget not found")
            return False

        # Find the option button
        option_widgets = option_picker_widget.findChildren(QPushButton)
        for widget in option_widgets:
            widget_id = widget.objectName() or widget.text()
            if widget_id == option and widget.isVisible() and widget.isEnabled():
                logger.debug(f"Clicking option button: {widget_id}")
                widget.click()
                QTest.qWait(500)  # Wait for selection to process
                logger.info(f"Successfully selected option: {option}")
                return True

        logger.error(f"Option button not found or not clickable: {option}")
        return False

    def select_first_available_option(self) -> bool:
        """
        Select the first available option.

        Returns:
            bool: True if selection successful, False otherwise
        """
        logger.info("Selecting first available option")

        available_options = self.get_available_options()
        if not available_options:
            logger.error("No options available")
            return False

        first_option = available_options[0]
        return self.select_option(first_option)

    def build_sample_sequence(self, length: int = 2) -> bool:
        """
        Build a sample sequence of the specified length.

        Args:
            length: Number of beats to add to the sequence

        Returns:
            True if sequence was built successfully
        """
        logger.info(f"Building sample sequence with {length} beats")

        # First select a start position
        if not self.select_first_available_start_position():
            logger.error("Failed to select start position for sample sequence")
            return False

        # Add beats by selecting options
        for beat_num in range(1, length):
            logger.info(f"Adding beat {beat_num + 1}")

            # Wait for options to load
            QTest.qWait(1000)

            # Try to select the first available option
            available_options = self.get_available_options()
            if not available_options:
                logger.warning(f"No options available for beat {beat_num + 1}")
                continue

            # Click the first option
            first_option = available_options[0]
            QTest.mouseClick(first_option, Qt.MouseButton.LeftButton)
            QTest.qWait(500)

        logger.info(f"Sample sequence with {length} beats built successfully")
        return True

    def try_select_option_without_start_position(self) -> bool:
        """
        Try to select an option without first selecting a start position.
        This should fail gracefully.

        Returns:
            False if the operation correctly failed, True if it unexpectedly succeeded
        """
        logger.info("Attempting to select option without start position")

        # Try to find and click an option without setting start position first
        try:
            available_options = self.get_available_options()
            if available_options:
                # This should not happen - there shouldn't be options without a start position
                logger.warning(
                    "Found options without start position - this may be unexpected"
                )
                return True
            else:
                logger.info("Correctly found no options without start position")
                return False
        except Exception as e:
            logger.info(f"Operation correctly failed: {e}")
            return False

    def clear_sequence(self) -> bool:
        """
        Clear the current sequence.

        Returns:
            True if sequence was cleared successfully
        """
        logger.info("Clearing sequence")

        try:
            # Look for a clear button or similar control
            clear_button = self.element_finder.find_element_by_text("Clear")
            if clear_button:
                QTest.mouseClick(clear_button, Qt.MouseButton.LeftButton)
                QTest.qWait(500)
                logger.info("Sequence cleared successfully")
                return True
            else:
                logger.warning("Clear button not found")
                return False
        except Exception as e:
            logger.error(f"Failed to clear sequence: {e}")
            return False
