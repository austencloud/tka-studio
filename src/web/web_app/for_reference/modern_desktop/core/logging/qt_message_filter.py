"""
Qt Message Handler for filtering out CSS property warnings and other noise.

This module provides Qt message filtering specifically for PyQt6 applications
to suppress warnings about unsupported CSS properties and other non-critical messages.
"""

from __future__ import annotations

import logging
import re
from re import Pattern

from PyQt6.QtCore import QtMsgType, qInstallMessageHandler


logger = logging.getLogger(__name__)


class QtMessageFilter:
    """Filter for Qt debug messages to suppress CSS warnings and other noise."""

    def __init__(self):
        """Initialize the message filter with default patterns."""
        # Compile regex patterns for better performance
        self.suppressed_patterns: list[Pattern] = [
            # CSS property warnings
            re.compile(r"Unknown property\s+.*", re.IGNORECASE),
            re.compile(r"unknown property\s+.*", re.IGNORECASE),
            # Specific CSS properties that PyQt6 doesn't support
            re.compile(r".*transition.*", re.IGNORECASE),
            re.compile(r".*box-shadow.*", re.IGNORECASE),
            re.compile(r".*transform.*", re.IGNORECASE),
            # Other common Qt noise
            re.compile(r".*QSslSocket.*", re.IGNORECASE),
            re.compile(r".*Qt WebEngine.*", re.IGNORECASE),
            re.compile(r".*not available.*", re.IGNORECASE),
        ]

        # Track suppressed message counts for debugging
        self.suppressed_count = 0
        self.original_handler = None

    def should_suppress_message(self, message: str) -> bool:
        """Check if a message should be suppressed based on patterns."""
        for pattern in self.suppressed_patterns:
            if pattern.search(message):
                self.suppressed_count += 1
                return True
        return False

    def qt_message_handler(self, msg_type: QtMsgType, context, message: str):
        """Custom Qt message handler that filters unwanted messages."""
        # Suppress messages matching our patterns
        if self.should_suppress_message(message):
            return

        # For critical messages, always let them through
        if msg_type == QtMsgType.QtCriticalMsg or msg_type == QtMsgType.QtFatalMsg:
            if self.original_handler:
                self.original_handler(msg_type, context, message)
            else:
                print(f"Qt Critical: {message}")
            return

        # For debug and info messages, apply more filtering
        if msg_type == QtMsgType.QtDebugMsg or msg_type == QtMsgType.QtInfoMsg:
            # Suppress debug messages by default unless they're important
            important_keywords = ["error", "failed", "critical", "exception"]
            if any(keyword in message.lower() for keyword in important_keywords):
                logger.debug(f"Qt Debug: {message}")
            return

        # Let warnings through but as debug level
        if msg_type == QtMsgType.QtWarningMsg:
            logger.debug(f"Qt Warning: {message}")
            return

        # Default handling for other message types
        if self.original_handler:
            self.original_handler(msg_type, context, message)
        else:
            logger.info(f"Qt: {message}")

    def install(self):
        """Install the Qt message handler."""
        try:
            # Store original handler if any
            self.original_handler = None  # PyQt6 doesn't expose the current handler

            # Install our custom handler
            qInstallMessageHandler(self.qt_message_handler)

            logger.debug("Qt message filter installed successfully")

        except Exception as e:
            logger.warning(f"Failed to install Qt message filter: {e}")

    def get_stats(self) -> dict:
        """Get statistics about filtered messages."""
        return {
            "suppressed_count": self.suppressed_count,
            "patterns_count": len(self.suppressed_patterns),
        }


# Global instance
_qt_message_filter: QtMessageFilter = None


def install_qt_message_filter():
    """Install the global Qt message filter."""
    global _qt_message_filter

    if _qt_message_filter is None:
        _qt_message_filter = QtMessageFilter()
        _qt_message_filter.install()
        logger.info("Qt message filtering enabled")
    else:
        logger.debug("Qt message filter already installed")


def get_qt_message_filter_stats() -> dict:
    """Get statistics from the Qt message filter."""
    if _qt_message_filter:
        return _qt_message_filter.get_stats()
    return {"suppressed_count": 0, "patterns_count": 0}


def disable_qt_message_filter():
    """Disable the Qt message filter by installing None handler."""
    qInstallMessageHandler(None)
    logger.info("Qt message filtering disabled")
