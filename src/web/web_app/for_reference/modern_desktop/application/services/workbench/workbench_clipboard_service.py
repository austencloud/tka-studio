"""
Workbench Clipboard Service Implementation

Framework-agnostic implementation of clipboard operations for workbench.
Provides clipboard functionality without direct Qt dependencies in the service layer.
"""

from __future__ import annotations

import logging

from desktop.modern.core.interfaces.workbench_services import IClipboardAdapter


logger = logging.getLogger(__name__)


class WorkbenchClipboardService:
    """
    Framework-agnostic implementation of clipboard operations.

    Note: This service provides the business logic interface but delegates
    actual clipboard operations to an injected clipboard adapter.
    This allows the service to remain framework-agnostic while still
    providing clipboard functionality.
    """

    def __init__(self, clipboard_adapter=None):
        """
        Initialize clipboard service.

        Args:
            clipboard_adapter: Framework-specific clipboard adapter (e.g., Qt-based)
        """
        self._clipboard_adapter = clipboard_adapter
        logger.debug("WorkbenchClipboardService initialized")

    def copy_text_to_clipboard(self, text: str) -> tuple[bool, str]:
        """
        Copy text to system clipboard.

        Args:
            text: Text to copy

        Returns:
            Tuple of (success, message)
        """
        try:
            if not text:
                return False, "No text provided to copy"

            if not self._clipboard_adapter:
                logger.warning("No clipboard adapter available")
                return False, "Clipboard not available"

            # Validate text
            if not isinstance(text, str):
                text = str(text)

            # Use adapter to perform actual clipboard operation
            success = self._clipboard_adapter.set_text(text)

            if success:
                logger.info(f"Text copied to clipboard: {len(text)} characters")
                return True, "Text copied to clipboard"
            logger.error("Clipboard adapter failed to copy text")
            return False, "Failed to copy text to clipboard"

        except Exception as e:
            logger.error(f"Clipboard copy operation failed: {e}")
            return False, f"Clipboard operation failed: {e}"

    def get_clipboard_text(self) -> tuple[bool, str]:
        """
        Get text from system clipboard.

        Returns:
            Tuple of (success, text/error_message)
        """
        try:
            if not self._clipboard_adapter:
                logger.warning("No clipboard adapter available")
                return False, "Clipboard not available"

            # Use adapter to get clipboard text
            text = self._clipboard_adapter.get_text()

            if text is not None:
                logger.info(f"Text retrieved from clipboard: {len(text)} characters")
                return True, text
            logger.warning("No text available in clipboard")
            return False, "No text in clipboard"

        except Exception as e:
            logger.error(f"Clipboard get operation failed: {e}")
            return False, f"Clipboard operation failed: {e}"

    def is_clipboard_available(self) -> bool:
        """Check if clipboard is available for operations."""
        try:
            return (
                self._clipboard_adapter is not None
                and self._clipboard_adapter.is_available()
            )
        except Exception as e:
            logger.error(f"Clipboard availability check failed: {e}")
            return False

    def get_clipboard_stats(self) -> dict:
        """Get clipboard statistics for debugging."""
        try:
            return {
                "adapter_available": self._clipboard_adapter is not None,
                "clipboard_available": self.is_clipboard_available(),
                "adapter_type": type(self._clipboard_adapter).__name__
                if self._clipboard_adapter
                else None,
            }
        except Exception as e:
            return {
                "error": str(e),
                "adapter_available": False,
                "clipboard_available": False,
            }


class QtClipboardAdapter(IClipboardAdapter):
    """
    Qt-specific clipboard adapter.

    This adapter handles the Qt-specific clipboard operations,
    keeping the framework dependency isolated from the business service.
    """

    def __init__(self):
        """Initialize Qt clipboard adapter."""
        self._clipboard = None
        self._initialize_clipboard()

    def _initialize_clipboard(self):
        """Initialize Qt clipboard if available."""
        try:
            # Import Qt here to keep the dependency localized
            from PyQt6.QtWidgets import QApplication

            app = QApplication.instance()
            if app:
                self._clipboard = app.clipboard()
                logger.debug("Qt clipboard adapter initialized")
            else:
                logger.warning("No QApplication instance available for clipboard")

        except ImportError:
            logger.warning("PyQt6 not available, clipboard operations disabled")
        except Exception as e:
            logger.error(f"Failed to initialize Qt clipboard: {e}")

    def set_text(self, text: str) -> bool:
        """Set text in Qt clipboard."""
        try:
            if not self._clipboard:
                return False

            self._clipboard.setText(text)
            return True

        except Exception as e:
            logger.error(f"Qt clipboard set_text failed: {e}")
            return False

    def get_text(self) -> str:
        """Get text from Qt clipboard."""
        try:
            if not self._clipboard:
                return ""

            return self._clipboard.text()

        except Exception as e:
            logger.error(f"Qt clipboard get_text failed: {e}")
            return ""

    def is_available(self) -> bool:
        """Check if Qt clipboard is available."""
        return self._clipboard is not None


class MockClipboardAdapter(IClipboardAdapter):
    """
    Mock clipboard adapter for testing.

    Provides clipboard functionality without requiring Qt or system clipboard.
    """

    def __init__(self):
        """Initialize mock clipboard."""
        self._clipboard_text = ""
        logger.debug("Mock clipboard adapter initialized")

    def set_text(self, text: str) -> bool:
        """Set text in mock clipboard."""
        try:
            self._clipboard_text = str(text)
            return True
        except Exception:
            return False

    def get_text(self) -> str:
        """Get text from mock clipboard."""
        return self._clipboard_text

    def is_available(self) -> bool:
        """Mock clipboard is always available."""
        return True
