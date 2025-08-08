"""
Background service interfaces for dependency injection.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class IBackgroundService(ABC):
    """Interface for background management service."""

    @abstractmethod
    def get_available_backgrounds(self) -> list[str]:
        """Get list of available background types."""

    @abstractmethod
    def get_current_background(self) -> str:
        """Get the currently selected background type."""

    @abstractmethod
    def set_background(self, background_type: str) -> bool:
        """Set the background type. Returns True if successful."""

    @abstractmethod
    def is_valid_background(self, background_type: str) -> bool:
        """Check if the background type is valid."""
