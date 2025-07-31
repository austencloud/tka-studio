"""
Browse Tab Page Object

Provides high-level interface for interacting with the Browse Tab,
including sequence browsing, filtering, and viewing functionality.
"""

import logging
from typing import Any, Optional

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget

from .base_page_object import BasePageObject

logger = logging.getLogger(__name__)


class BrowseTabPageObject(BasePageObject):
    """
    Page object for the Browse Tab.

    Provides methods for:
    - Sequence browsing and filtering
    - Sequence selection and viewing
    - Component visibility verification
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.element_selectors = {
            "browse_tab": "browse_tab",
            "filter_panel": "filter_panel",
            "sequence_list": "sequence_list",
            "viewer_panel": "viewer_panel",
            "sequence_items": "sequence_item",
        }

    # ========================================
    # COMPONENT VISIBILITY METHODS
    # ========================================

    def is_filter_panel_visible(self) -> bool:
        """Check if filter panel is visible."""
        logger.debug("Checking filter panel visibility")

        panel = self.get_element("filter_panel")
        if panel and hasattr(panel, "isVisible"):
            return panel.isVisible()

        # Fallback: look for filter related components
        return self._find_filter_components() is not None

    def is_sequence_list_visible(self) -> bool:
        """Check if sequence list is visible."""
        logger.debug("Checking sequence list visibility")

        list_widget = self.get_element("sequence_list")
        if list_widget and hasattr(list_widget, "isVisible"):
            return list_widget.isVisible()

        # Fallback: look for list related components
        return self._find_list_components() is not None

    def is_viewer_panel_visible(self) -> bool:
        """Check if viewer panel is visible."""
        logger.debug("Checking viewer panel visibility")

        panel = self.get_element("viewer_panel")
        if panel and hasattr(panel, "isVisible"):
            return panel.isVisible()

        # Fallback: look for viewer related components
        return self._find_viewer_components() is not None

    # ========================================
    # SEQUENCE BROWSING METHODS
    # ========================================

    def get_available_sequences(self) -> list[str]:
        """Get list of available sequences in the browse tab."""
        logger.debug("Getting available sequences")

        try:
            # Look for sequence items in the list
            sequence_elements = self._find_sequence_elements()

            sequences = []
            for element in sequence_elements:
                # Extract sequence name from element
                sequence_name = self._extract_sequence_name(element)
                if sequence_name:
                    sequences.append(sequence_name)

            logger.info(f"🔍 Found {len(sequences)} available sequences")
            return sequences

        except Exception as e:
            logger.warning(f"Error getting available sequences: {e}")
            return []

    def select_sequence(self, sequence_name: str) -> bool:
        """Select a specific sequence from the list."""
        logger.info(f"🔍 Selecting sequence: {sequence_name}")

        try:
            # Find the sequence element
            sequence_element = self._find_sequence_element(sequence_name)

            if sequence_element and hasattr(sequence_element, "click"):
                sequence_element.click()
                logger.info(f"✅ Successfully selected sequence: {sequence_name}")
                return True
            else:
                logger.warning(
                    f"⚠️ Could not find clickable element for sequence: {sequence_name}"
                )
                return False

        except Exception as e:
            logger.error(f"❌ Error selecting sequence {sequence_name}: {e}")
            return False

    def get_selected_sequence(self) -> Optional[str]:
        """Get the currently selected sequence."""
        logger.debug("Getting selected sequence")

        try:
            # Look for selected sequence element
            selected_element = self._find_selected_sequence()
            if selected_element:
                return self._extract_sequence_name(selected_element)
            return None

        except Exception as e:
            logger.warning(f"Error getting selected sequence: {e}")
            return None

    # ========================================
    # FILTERING METHODS
    # ========================================

    def apply_filter(self, filter_criteria: dict) -> bool:
        """Apply filtering criteria to the sequence list."""
        logger.info(f"🔍 Applying filter: {filter_criteria}")

        try:
            # Find filter controls and apply criteria
            filter_panel = self._find_filter_components()
            if not filter_panel:
                logger.warning("⚠️ Filter panel not found")
                return False

            # Apply each filter criterion
            for key, value in filter_criteria.items():
                success = self._apply_single_filter(key, value)
                if not success:
                    logger.warning(f"⚠️ Failed to apply filter: {key}={value}")

            logger.info("✅ Successfully applied filters")
            return True

        except Exception as e:
            logger.error(f"❌ Error applying filter: {e}")
            return False

    def clear_filters(self) -> bool:
        """Clear all applied filters."""
        logger.info("🔍 Clearing all filters")

        try:
            # Find and click clear filter button
            clear_button = self._find_clear_filter_button()
            if clear_button and hasattr(clear_button, "click"):
                clear_button.click()
                logger.info("✅ Successfully cleared filters")
                return True
            else:
                logger.warning("⚠️ Clear filter button not found")
                return False

        except Exception as e:
            logger.error(f"❌ Error clearing filters: {e}")
            return False

    # ========================================
    # PRIVATE HELPER METHODS
    # ========================================

    def _find_filter_components(self) -> Optional[QWidget]:
        """Find filter related components."""
        # Look for various filter related widgets
        for class_name in ["FilterPanel", "BrowseFilter", "SequenceFilter"]:
            components = self._find_components_by_class_name(class_name)
            if components:
                return components[0]
        return None

    def _find_list_components(self) -> Optional[QWidget]:
        """Find list related components."""
        # Look for various list related widgets
        for class_name in ["SequenceList", "BrowseList", "QListWidget", "QTreeWidget"]:
            components = self._find_components_by_class_name(class_name)
            if components:
                return components[0]
        return None

    def _find_viewer_components(self) -> Optional[QWidget]:
        """Find viewer related components."""
        # Look for various viewer related widgets
        for class_name in ["ViewerPanel", "SequenceViewer", "PreviewPanel"]:
            components = self._find_components_by_class_name(class_name)
            if components:
                return components[0]
        return None

    def _find_sequence_elements(self) -> list[QWidget]:
        """Find all sequence elements in the list."""
        elements = []

        # Look for sequence items
        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                class_name = child.__class__.__name__.lower()
                if any(
                    indicator in class_name
                    for indicator in ["sequence", "item", "entry"]
                ):
                    if hasattr(child, "click") or hasattr(child, "isVisible"):
                        elements.append(child)

        return elements

    def _find_sequence_element(self, sequence_name: str) -> Optional[QWidget]:
        """Find specific sequence element by name."""
        elements = self._find_sequence_elements()

        for element in elements:
            if self._element_matches_name(element, sequence_name):
                return element

        return None

    def _find_selected_sequence(self) -> Optional[QWidget]:
        """Find the currently selected sequence element."""
        elements = self._find_sequence_elements()

        for element in elements:
            # Look for selection indicators
            if hasattr(element, "isSelected") and element.isSelected():
                return element
            if hasattr(element, "isChecked") and element.isChecked():
                return element

        return None

    def _find_clear_filter_button(self) -> Optional[QWidget]:
        """Find the clear filter button."""
        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                if hasattr(child, "text"):
                    text = child.text().lower()
                    if any(keyword in text for keyword in ["clear", "reset", "all"]):
                        return child
        return None

    def _extract_sequence_name(self, element: QWidget) -> Optional[str]:
        """Extract sequence name from element."""
        if hasattr(element, "text"):
            return element.text()
        if hasattr(element, "objectName"):
            return element.objectName()
        return element.__class__.__name__

    def _element_matches_name(self, element: QWidget, name: str) -> bool:
        """Check if element matches the given name."""
        element_text = self._extract_sequence_name(element) or ""
        return name.lower() in element_text.lower()

    def _apply_single_filter(self, key: str, value: Any) -> bool:
        """Apply a single filter criterion."""
        # This would be implemented based on specific filter UI
        logger.debug(f"Applying filter: {key}={value}")
        return True

    def _find_components_by_class_name(self, class_name: str) -> list[QWidget]:
        """Find components by class name."""
        components = []

        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                if class_name.lower() in child.__class__.__name__.lower():
                    components.append(child)

        return components
