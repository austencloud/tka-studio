"""
Base Page Object for TKA Modern E2E Testing Framework

This module provides the foundational BasePage class that all page objects
inherit from, providing common functionality for element discovery, caching,
wait conditions, and error handling.
"""

from abc import ABC, abstractmethod
import logging
from typing import Dict, List, Optional

from PyQt6.QtCore import QObject
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class BasePage(ABC):
    """
    Base class for all page objects in the TKA testing framework.

    Provides common functionality for:
    - Element discovery and caching
    - Wait conditions and timeouts
    - Error handling and logging
    - Common UI interaction patterns

    All page objects should inherit from this class and implement
    the abstract methods for their specific functionality.
    """

    def __init__(self, parent_widget: QWidget):
        """
        Initialize the base page object.

        Args:
            parent_widget: The parent Qt widget that contains this page's elements
        """
        self.parent = parent_widget
        self._elements: Dict[str, QWidget] = {}
        self._loaded = False

        logger.debug(f"Initialized {self.__class__.__name__} page object")

    def wait_for_load(self, timeout: int = 5000) -> bool:
        """
        Wait for page to be fully loaded.

        Args:
            timeout: Maximum time to wait in milliseconds

        Returns:
            bool: True if page loaded successfully, False if timeout
        """
        logger.debug(
            f"Waiting for {self.__class__.__name__} to load (timeout: {timeout}ms)"
        )

        start_time = 0
        while not self.is_loaded() and start_time < timeout:
            QTest.qWait(100)
            start_time += 100

        self._loaded = self.is_loaded()

        if self._loaded:
            logger.debug(f"{self.__class__.__name__} loaded successfully")
        else:
            logger.warning(
                f"{self.__class__.__name__} failed to load within {timeout}ms"
            )

        return self._loaded

    def get_element(self, name: str, force_refresh: bool = False) -> Optional[QWidget]:
        """
        Get element by name with caching.

        Args:
            name: Element identifier
            force_refresh: If True, bypass cache and search again

        Returns:
            QWidget or None: The found element or None if not found
        """
        if name not in self._elements or force_refresh:
            logger.debug(f"Searching for element '{name}' in {self.__class__.__name__}")
            self._elements[name] = self._find_element(name)

            if self._elements[name]:
                logger.debug(
                    f"Found element '{name}': {self._elements[name].__class__.__name__}"
                )
            else:
                logger.debug(f"Element '{name}' not found")

        return self._elements[name]

    def wait_for_element(self, element_name: str, timeout: int = 5000) -> bool:
        """
        Wait for a specific element to be available.

        Args:
            element_name: Name of the element to wait for
            timeout: Maximum time to wait in milliseconds

        Returns:
            bool: True if element becomes available, False if timeout
        """
        logger.debug(f"Waiting for element '{element_name}' (timeout: {timeout}ms)")

        start_time = 0
        while start_time < timeout:
            element = self.get_element(element_name, force_refresh=True)
            if element:
                logger.debug(f"Element '{element_name}' is now available")
                return True

            QTest.qWait(100)
            start_time += 100

        logger.warning(f"Element '{element_name}' not available after {timeout}ms")
        return False

    def clear_cache(self):
        """Clear cached elements to force fresh discovery."""
        logger.debug(f"Clearing element cache for {self.__class__.__name__}")
        self._elements.clear()
        self._loaded = False

    def refresh(self):
        """Refresh the page state by clearing cache and re-checking load status."""
        self.clear_cache()
        self.wait_for_load()

    # Abstract methods that must be implemented by subclasses

    @abstractmethod
    def is_loaded(self) -> bool:
        """
        Check if page is fully loaded and ready for interaction.

        Returns:
            bool: True if page is loaded, False otherwise
        """

    @abstractmethod
    def _find_element(self, name: str) -> Optional[QWidget]:
        """
        Find element implementation specific to this page.

        Args:
            name: Element identifier

        Returns:
            QWidget or None: The found element or None if not found
        """

    # Helper methods for common element discovery patterns

    def _find_widget_by_class_name(self, class_name_contains: str) -> Optional[QWidget]:
        """
        Helper to find widget by class name pattern.

        Args:
            class_name_contains: String that should be contained in the class name

        Returns:
            QWidget or None: First matching widget or None
        """
        if not hasattr(self.parent, "findChildren"):
            logger.debug("Parent widget does not support findChildren")
            return None

        children = self.parent.findChildren(QObject)
        for child in children:
            if class_name_contains.lower() in child.__class__.__name__.lower():
                logger.debug(f"Found widget by class name: {child.__class__.__name__}")
                return child

        logger.debug(f"No widget found containing class name: {class_name_contains}")
        return None

    def _find_widgets_by_class_name(self, class_name_contains: str) -> List[QWidget]:
        """
        Helper to find all widgets matching a class name pattern.

        Args:
            class_name_contains: String that should be contained in the class name

        Returns:
            List[QWidget]: List of matching widgets (may be empty)
        """
        if not hasattr(self.parent, "findChildren"):
            return []

        children = self.parent.findChildren(QObject)
        matches = []

        for child in children:
            if class_name_contains.lower() in child.__class__.__name__.lower():
                matches.append(child)

        logger.debug(
            f"Found {len(matches)} widgets containing class name: {class_name_contains}"
        )
        return matches

    def _find_widget_by_object_name(self, object_name: str) -> Optional[QWidget]:
        """
        Helper to find widget by Qt object name.

        Args:
            object_name: Qt object name to search for

        Returns:
            QWidget or None: Matching widget or None
        """
        if not hasattr(self.parent, "findChild"):
            return None

        widget = self.parent.findChild(QWidget, object_name)
        if widget:
            logger.debug(
                f"Found widget by object name '{object_name}': {widget.__class__.__name__}"
            )
        else:
            logger.debug(f"No widget found with object name: {object_name}")

        return widget
