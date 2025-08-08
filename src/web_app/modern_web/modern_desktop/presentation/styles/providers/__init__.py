"""
Style provider base classes and interfaces.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..core.types import StyleVariant


class StyleProvider(ABC):
    """Abstract base class for component style providers."""

    @abstractmethod
    def generate_style(
        self, variant: StyleVariant = StyleVariant.DEFAULT, **kwargs
    ) -> str:
        """Generate CSS style string for the component."""
