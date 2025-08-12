"""
Window Discovery Service

Pure service for window discovery and size provider functionality.
Extracted from option picker presentation layer to follow single responsibility principle.

PROVIDES:
- Main window registration and discovery
- Size provider functionality without complex hierarchy walking
- Clean fallback logic for window size detection
- Testable window discovery without UI dependencies

This service complements WindowManagementService by focusing on discovery
rather than positioning/management.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
import logging

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QWidget


logger = logging.getLogger(__name__)


class IWindowDiscoveryService(ABC):
    """Interface for window discovery operations."""

    @abstractmethod
    def register_main_window(self, window: QWidget) -> None:
        """Register the main window during application startup."""

    @abstractmethod
    def find_main_window(self) -> QWidget | None:
        """Find the main window using discovery logic."""

    @abstractmethod
    def get_main_window_size(self) -> QSize:
        """Get main window size with proper fallbacks."""

    @abstractmethod
    def create_size_provider(self) -> Callable[[], QSize]:
        """Create a size provider function for components."""

    @abstractmethod
    def validate_main_window(self) -> bool:
        """Validate that main window is properly registered and accessible."""


class WindowDiscoveryService(IWindowDiscoveryService):
    """
    Pure service for window discovery and size provider functionality.

    Handles main window registration, discovery, and size provider creation
    without complex hierarchy walking or presentation layer dependencies.
    """

    def __init__(self):
        """Initialize the window discovery service."""
        self._main_window: QWidget | None = None
        self._fallback_size = QSize(1200, 800)

    def register_main_window(self, window: QWidget) -> None:
        """Register the main window during application startup."""
        if window is None:
            logger.warning("Attempted to register None as main window")
            return

        self._main_window = window
        logger.info(f"Main window registered: {window.__class__.__name__}")

    def find_main_window(self) -> QWidget | None:
        """Find the main window using discovery logic."""
        # First, check if we have a registered main window
        if self._main_window and not self._main_window.isHidden():
            return self._main_window

        # Fallback: try to find through QApplication
        app = QApplication.instance()
        if app:
            # Try active window first
            active_window = app.activeWindow()
            if active_window and self._is_main_window(active_window):
                return active_window

            # Try all top-level widgets
            for widget in app.topLevelWidgets():
                if self._is_main_window(widget):
                    return widget

        logger.warning("Could not find main window through discovery")
        return None

    def _is_main_window(self, widget: QWidget) -> bool:
        """Check if a widget is likely the main window."""
        if not widget or widget.isHidden():
            return False

        class_name = widget.__class__.__name__

        # Check for main window indicators
        if "MainWindow" in class_name:
            return True

        # Check for menu bar (QMainWindow feature)
        if hasattr(widget, "menuBar") and widget.menuBar():
            return True

        # Check for reasonable size (main windows are typically large)
        size = widget.size()
        if size.width() > 800 and size.height() > 600:
            return True

        return False

    def get_main_window_size(self) -> QSize:
        """Get main window size with proper fallbacks."""
        # Try registered main window first
        if self._main_window and not self._main_window.isHidden():
            size = self._main_window.size()
            if self._is_valid_size(size):
                return size

        # Try discovery
        discovered_window = self.find_main_window()
        if discovered_window:
            size = discovered_window.size()
            if self._is_valid_size(size):
                return size

        # Try QApplication active window
        app = QApplication.instance()
        if app and app.activeWindow():
            size = app.activeWindow().size()
            if self._is_valid_size(size):
                return size

        # Try primary screen size as last resort
        if app:
            screen = app.primaryScreen()
            if screen:
                screen_size = screen.size()
                # Return a reasonable portion of screen size
                return QSize(
                    int(screen_size.width() * 0.8), int(screen_size.height() * 0.8)
                )

        # Final fallback
        logger.warning(f"Using fallback size: {self._fallback_size}")
        return self._fallback_size

    def _is_valid_size(self, size: QSize) -> bool:
        """Check if a size is valid (not too small)."""
        return size.width() > 100 and size.height() > 100

    def create_size_provider(self) -> Callable[[], QSize]:
        """Create a size provider function for components."""

        def size_provider() -> QSize:
            return self.get_main_window_size()

        return size_provider

    def validate_main_window(self) -> bool:
        """Validate that main window is properly registered and accessible."""
        try:
            # Check if we can get a valid size
            size = self.get_main_window_size()

            # Check if size is not the fallback (indicates real window found)
            is_fallback = (
                size.width() == self._fallback_size.width()
                and size.height() == self._fallback_size.height()
            )

            if is_fallback:
                logger.warning("Main window validation failed - using fallback size")
                return False

            # Check if we can find the actual window
            window = self.find_main_window()
            if not window:
                logger.warning("Main window validation failed - no window found")
                return False

            logger.info(
                f"Main window validation passed: {size.width()}x{size.height()}"
            )
            return True

        except Exception as e:
            logger.error(f"Main window validation error: {e}")
            return False
