"""
Sequence Card Tab Page Object

Provides high-level interface for interacting with the Sequence Card Tab,
including card display, navigation, and layout management.
"""

import logging
from typing import Any, Optional

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget

from .base_page_object import BasePageObject

logger = logging.getLogger(__name__)


class SequenceCardTabPageObject(BasePageObject):
    """
    Page object for the Sequence Card Tab.

    Provides methods for:
    - Card display and navigation
    - Layout management
    - Sequence card interaction
    - Component visibility verification
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.element_selectors = {
            "sequence_card_tab": "sequence_card_tab",
            "header": "header",
            "navigation": "navigation",
            "content_area": "content_area",
            "sequence_cards": "sequence_card",
            "length_selector": "length_selector",
            "column_selector": "column_selector",
        }

    # ========================================
    # COMPONENT VISIBILITY METHODS
    # ========================================

    def is_header_visible(self) -> bool:
        """Check if header is visible."""
        logger.debug("Checking header visibility")

        header = self.get_element("header")
        if header and hasattr(header, "isVisible"):
            return header.isVisible()

        # Fallback: look for header related components
        return self._find_header_components() is not None

    def is_navigation_visible(self) -> bool:
        """Check if navigation is visible."""
        logger.debug("Checking navigation visibility")

        navigation = self.get_element("navigation")
        if navigation and hasattr(navigation, "isVisible"):
            return navigation.isVisible()

        # Fallback: look for navigation related components
        return self._find_navigation_components() is not None

    def is_content_area_visible(self) -> bool:
        """Check if content area is visible."""
        logger.debug("Checking content area visibility")

        content = self.get_element("content_area")
        if content and hasattr(content, "isVisible"):
            return content.isVisible()

        # Fallback: look for content related components
        return self._find_content_components() is not None

    # ========================================
    # CARD DISPLAY METHODS
    # ========================================

    def get_displayed_cards(self) -> list[str]:
        """Get list of currently displayed sequence cards."""
        logger.debug("Getting displayed cards")

        try:
            # Look for card elements in the content area
            card_elements = self._find_card_elements()

            cards = []
            for element in card_elements:
                # Extract card identifier from element
                card_id = self._extract_card_id(element)
                if card_id:
                    cards.append(card_id)

            logger.info(f"📋 Found {len(cards)} displayed cards")
            return cards

        except Exception as e:
            logger.warning(f"Error getting displayed cards: {e}")
            return []

    def select_card(self, card_id: str) -> bool:
        """Select a specific sequence card."""
        logger.info(f"📋 Selecting card: {card_id}")

        try:
            # Find the card element
            card_element = self._find_card_element(card_id)

            if card_element and hasattr(card_element, "click"):
                card_element.click()
                logger.info(f"✅ Successfully selected card: {card_id}")
                return True
            else:
                logger.warning(
                    f"⚠️ Could not find clickable element for card: {card_id}"
                )
                return False

        except Exception as e:
            logger.error(f"❌ Error selecting card {card_id}: {e}")
            return False

    def get_selected_card(self) -> Optional[str]:
        """Get the currently selected card."""
        logger.debug("Getting selected card")

        try:
            # Look for selected card element
            selected_element = self._find_selected_card()
            if selected_element:
                return self._extract_card_id(selected_element)
            return None

        except Exception as e:
            logger.warning(f"Error getting selected card: {e}")
            return None

    # ========================================
    # NAVIGATION METHODS
    # ========================================

    def set_length_filter(self, length: int) -> bool:
        """Set the sequence length filter."""
        logger.info(f"📋 Setting length filter to: {length}")

        try:
            # Find length selector
            length_selector = self._find_length_selector()

            if length_selector:
                # Set the length value
                success = self._set_selector_value(length_selector, str(length))
                if success:
                    logger.info(f"✅ Successfully set length filter: {length}")
                    return True

            logger.warning(f"⚠️ Could not set length filter: {length}")
            return False

        except Exception as e:
            logger.error(f"❌ Error setting length filter: {e}")
            return False

    def set_column_count(self, columns: int) -> bool:
        """Set the number of columns for card display."""
        logger.info(f"📋 Setting column count to: {columns}")

        try:
            # Find column selector
            column_selector = self._find_column_selector()

            if column_selector:
                # Set the column value
                success = self._set_selector_value(column_selector, str(columns))
                if success:
                    logger.info(f"✅ Successfully set column count: {columns}")
                    return True

            logger.warning(f"⚠️ Could not set column count: {columns}")
            return False

        except Exception as e:
            logger.error(f"❌ Error setting column count: {e}")
            return False

    def refresh_display(self) -> bool:
        """Refresh the card display."""
        logger.info("📋 Refreshing display")

        try:
            # Find and click refresh button
            refresh_button = self._find_refresh_button()
            if refresh_button and hasattr(refresh_button, "click"):
                refresh_button.click()
                logger.info("✅ Successfully refreshed display")
                return True
            else:
                logger.warning("⚠️ Refresh button not found")
                return False

        except Exception as e:
            logger.error(f"❌ Error refreshing display: {e}")
            return False

    # ========================================
    # LAYOUT METHODS
    # ========================================

    def get_current_layout_info(self) -> dict:
        """Get current layout information."""
        logger.debug("Getting current layout info")

        try:
            layout_info = {
                "length_filter": 0,
                "column_count": 1,
                "total_cards": 0,
                "visible_cards": 0,
            }

            # Get length filter
            length_selector = self._find_length_selector()
            if length_selector:
                layout_info["length_filter"] = self._get_selector_value(length_selector)

            # Get column count
            column_selector = self._find_column_selector()
            if column_selector:
                layout_info["column_count"] = self._get_selector_value(column_selector)

            # Get card counts
            displayed_cards = self.get_displayed_cards()
            layout_info["visible_cards"] = len(displayed_cards)

            return layout_info

        except Exception as e:
            logger.warning(f"Error getting layout info: {e}")
            return {}

    # ========================================
    # PRIVATE HELPER METHODS
    # ========================================

    def _find_header_components(self) -> Optional[QWidget]:
        """Find header related components."""
        # Look for various header related widgets
        for class_name in ["Header", "SequenceCardHeader", "TitleBar"]:
            components = self._find_components_by_class_name(class_name)
            if components:
                return components[0]
        return None

    def _find_navigation_components(self) -> Optional[QWidget]:
        """Find navigation related components."""
        # Look for various navigation related widgets
        for class_name in ["Navigation", "SequenceCardNavigation", "ControlPanel"]:
            components = self._find_components_by_class_name(class_name)
            if components:
                return components[0]
        return None

    def _find_content_components(self) -> Optional[QWidget]:
        """Find content related components."""
        # Look for various content related widgets
        for class_name in ["Content", "SequenceCardContent", "CardArea"]:
            components = self._find_components_by_class_name(class_name)
            if components:
                return components[0]
        return None

    def _find_card_elements(self) -> list[QWidget]:
        """Find all card elements."""
        elements = []

        # Look for card items
        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                class_name = child.__class__.__name__.lower()
                if any(
                    indicator in class_name
                    for indicator in ["card", "sequence", "item"]
                ):
                    if hasattr(child, "click") or hasattr(child, "isVisible"):
                        elements.append(child)

        return elements

    def _find_card_element(self, card_id: str) -> Optional[QWidget]:
        """Find specific card element by ID."""
        elements = self._find_card_elements()

        for element in elements:
            if self._element_matches_id(element, card_id):
                return element

        return None

    def _find_selected_card(self) -> Optional[QWidget]:
        """Find the currently selected card element."""
        elements = self._find_card_elements()

        for element in elements:
            # Look for selection indicators
            if hasattr(element, "isSelected") and element.isSelected():
                return element
            if hasattr(element, "isChecked") and element.isChecked():
                return element

        return None

    def _find_length_selector(self) -> Optional[QWidget]:
        """Find the length selector widget."""
        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                class_name = child.__class__.__name__.lower()
                if any(
                    indicator in class_name
                    for indicator in ["length", "filter", "combo"]
                ):
                    return child
        return None

    def _find_column_selector(self) -> Optional[QWidget]:
        """Find the column selector widget."""
        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                class_name = child.__class__.__name__.lower()
                if any(
                    indicator in class_name
                    for indicator in ["column", "grid", "layout"]
                ):
                    return child
        return None

    def _find_refresh_button(self) -> Optional[QWidget]:
        """Find the refresh button."""
        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                if hasattr(child, "text"):
                    text = child.text().lower()
                    if any(
                        keyword in text for keyword in ["refresh", "reload", "update"]
                    ):
                        return child
        return None

    def _extract_card_id(self, element: QWidget) -> Optional[str]:
        """Extract card ID from element."""
        if hasattr(element, "text"):
            return element.text()
        if hasattr(element, "objectName"):
            return element.objectName()
        return element.__class__.__name__

    def _element_matches_id(self, element: QWidget, card_id: str) -> bool:
        """Check if element matches the given card ID."""
        element_text = self._extract_card_id(element) or ""
        return card_id.lower() in element_text.lower()

    def _set_selector_value(self, selector: QWidget, value: str) -> bool:
        """Set value on a selector widget."""
        try:
            if hasattr(selector, "setCurrentText"):
                selector.setCurrentText(value)
                return True
            elif hasattr(selector, "setValue"):
                selector.setValue(int(value))
                return True
            elif hasattr(selector, "setText"):
                selector.setText(value)
                return True
            return False
        except Exception as e:
            logger.warning(f"Error setting selector value: {e}")
            return False

    def _get_selector_value(self, selector: QWidget) -> Any:
        """Get value from a selector widget."""
        try:
            if hasattr(selector, "currentText"):
                return selector.currentText()
            elif hasattr(selector, "value"):
                return selector.value()
            elif hasattr(selector, "text"):
                return selector.text()
            return None
        except Exception as e:
            logger.warning(f"Error getting selector value: {e}")
            return None

    def _find_components_by_class_name(self, class_name: str) -> list[QWidget]:
        """Find components by class name."""
        components = []

        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                if class_name.lower() in child.__class__.__name__.lower():
                    components.append(child)

        return components
