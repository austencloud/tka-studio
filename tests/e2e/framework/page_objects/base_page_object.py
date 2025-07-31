"""
Base Page Object

Provides common functionality for all page objects in the E2E testing framework.
"""

import logging
from typing import Optional

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class BasePageObject:
    """
    Base class for all page objects.

    Provides common functionality for:
    - Element finding and interaction
    - Visibility checking
    - Error handling
    - Logging
    """

    def __init__(self, parent: QWidget):
        self.parent = parent
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.element_selectors: dict[str, str] = {}

    # ========================================
    # ELEMENT FINDING METHODS
    # ========================================

    def get_element(self, element_name: str) -> Optional[QWidget]:
        """
        Get an element by name using the element selectors.

        Args:
            element_name: Name of the element to find

        Returns:
            QWidget or None if not found
        """
        if element_name not in self.element_selectors:
            self.logger.warning(f"Element selector not defined: {element_name}")
            return None

        selector = self.element_selectors[element_name]
        return self._find_element_by_selector(selector)

    def _find_element_by_selector(self, selector: str) -> Optional[QWidget]:
        """
        Find an element using a selector string.

        Args:
            selector: Selector string (class name, object name, etc.)

        Returns:
            QWidget or None if not found
        """
        try:
            # Try to find by object name first
            element = self._find_by_object_name(selector)
            if element:
                return element

            # Try to find by class name
            element = self._find_by_class_name(selector)
            if element:
                return element

            # Try to find by text content
            element = self._find_by_text_content(selector)
            if element:
                return element

            self.logger.debug(f"Element not found with selector: {selector}")
            return None

        except Exception as e:
            self.logger.warning(
                f"Error finding element with selector '{selector}': {e}"
            )
            return None

    def _find_by_object_name(self, object_name: str) -> Optional[QWidget]:
        """Find element by object name."""
        if hasattr(self.parent, "findChild"):
            return self.parent.findChild(QWidget, object_name)
        return None

    def _find_by_class_name(self, class_name: str) -> Optional[QWidget]:
        """Find element by class name."""
        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                if class_name.lower() in child.__class__.__name__.lower():
                    return child
        return None

    def _find_by_text_content(self, text: str) -> Optional[QWidget]:
        """Find element by text content."""
        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QObject)
            for child in children:
                if hasattr(child, "text") and text.lower() in child.text().lower():
                    return child
        return None

    # ========================================
    # VISIBILITY AND STATE METHODS
    # ========================================

    def is_element_visible(self, element_name: str) -> bool:
        """
        Check if an element is visible.

        Args:
            element_name: Name of the element to check

        Returns:
            bool: True if element is visible, False otherwise
        """
        element = self.get_element(element_name)
        if element and hasattr(element, "isVisible"):
            return element.isVisible()
        return False

    def is_element_enabled(self, element_name: str) -> bool:
        """
        Check if an element is enabled.

        Args:
            element_name: Name of the element to check

        Returns:
            bool: True if element is enabled, False otherwise
        """
        element = self.get_element(element_name)
        if element and hasattr(element, "isEnabled"):
            return element.isEnabled()
        return False

    def wait_for_element_visible(self, element_name: str, timeout: int = 5) -> bool:
        """
        Wait for an element to become visible.

        Args:
            element_name: Name of the element to wait for
            timeout: Maximum time to wait in seconds

        Returns:
            bool: True if element became visible, False if timeout
        """
        import time

        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_element_visible(element_name):
                return True
            time.sleep(0.1)

        self.logger.warning(
            f"Element '{element_name}' did not become visible within {timeout}s"
        )
        return False

    # ========================================
    # INTERACTION METHODS
    # ========================================

    def click_element(self, element_name: str) -> bool:
        """
        Click an element.

        Args:
            element_name: Name of the element to click

        Returns:
            bool: True if click was successful, False otherwise
        """
        element = self.get_element(element_name)
        if element and hasattr(element, "click"):
            try:
                element.click()
                self.logger.debug(f"Successfully clicked element: {element_name}")
                return True
            except Exception as e:
                self.logger.error(f"Error clicking element '{element_name}': {e}")
                return False

        self.logger.warning(f"Element '{element_name}' not found or not clickable")
        return False

    def set_element_text(self, element_name: str, text: str) -> bool:
        """
        Set text on an element.

        Args:
            element_name: Name of the element to set text on
            text: Text to set

        Returns:
            bool: True if text was set successfully, False otherwise
        """
        element = self.get_element(element_name)
        if element and hasattr(element, "setText"):
            try:
                element.setText(text)
                self.logger.debug(
                    f"Successfully set text on element '{element_name}': {text}"
                )
                return True
            except Exception as e:
                self.logger.error(
                    f"Error setting text on element '{element_name}': {e}"
                )
                return False

        self.logger.warning(
            f"Element '{element_name}' not found or does not support text setting"
        )
        return False

    def get_element_text(self, element_name: str) -> Optional[str]:
        """
        Get text from an element.

        Args:
            element_name: Name of the element to get text from

        Returns:
            str or None: Element text or None if not found
        """
        element = self.get_element(element_name)
        if element and hasattr(element, "text"):
            try:
                return element.text()
            except Exception as e:
                self.logger.error(
                    f"Error getting text from element '{element_name}': {e}"
                )
                return None

        self.logger.warning(
            f"Element '{element_name}' not found or does not support text getting"
        )
        return None

    # ========================================
    # UTILITY METHODS
    # ========================================

    def take_screenshot(self, filename: Optional[str] = None) -> bool:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename for the screenshot

        Returns:
            bool: True if screenshot was taken successfully
        """
        try:
            if hasattr(self.parent, "grab"):
                pixmap = self.parent.grab()
                if filename:
                    return pixmap.save(filename)
                else:
                    # Generate default filename
                    import datetime

                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    default_filename = (
                        f"screenshot_{self.__class__.__name__}_{timestamp}.png"
                    )
                    return pixmap.save(default_filename)
            return False
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {e}")
            return False

    def get_all_child_elements(self) -> list[QWidget]:
        """
        Get all child elements of the parent widget.

        Returns:
            List of QWidget objects
        """
        children = []
        if hasattr(self.parent, "findChildren"):
            children = self.parent.findChildren(QWidget)
        return children

    def log_element_hierarchy(self, max_depth: int = 3) -> None:
        """
        Log the element hierarchy for debugging.

        Args:
            max_depth: Maximum depth to traverse
        """
        self.logger.info(f"Element hierarchy for {self.__class__.__name__}:")
        self._log_element_recursive(self.parent, 0, max_depth)

    def _log_element_recursive(
        self, element: QWidget, depth: int, max_depth: int
    ) -> None:
        """Recursively log element hierarchy."""
        if depth > max_depth:
            return

        indent = "  " * depth
        class_name = element.__class__.__name__
        object_name = getattr(element, "objectName", lambda: "")()
        visible = getattr(element, "isVisible", lambda: "Unknown")()

        self.logger.info(
            f"{indent}{class_name} (name: {object_name}, visible: {visible})"
        )

        if hasattr(element, "children"):
            for child in element.children():
                if isinstance(child, QWidget):
                    self._log_element_recursive(child, depth + 1, max_depth)

    # ========================================
    # VALIDATION METHODS
    # ========================================

    def validate_page_loaded(self) -> bool:
        """
        Validate that the page is properly loaded.
        Should be overridden by subclasses.

        Returns:
            bool: True if page is loaded, False otherwise
        """
        return self.parent is not None

    def validate_required_elements(
        self, required_elements: list[str]
    ) -> dict[str, bool]:
        """
        Validate that required elements are present.

        Args:
            required_elements: List of element names that must be present

        Returns:
            Dict mapping element names to their presence status
        """
        validation_results = {}

        for element_name in required_elements:
            element = self.get_element(element_name)
            validation_results[element_name] = element is not None

            if element is None:
                self.logger.warning(f"Required element missing: {element_name}")

        return validation_results
