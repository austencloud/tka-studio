"""
Widget Factory for TKA Modern Desktop Application

This module provides factory classes for creating various UI widgets
with proper dependency injection and configuration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from PyQt6.QtWidgets import QWidget


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer


class OptionPickerWidgetFactory:
    """Factory for creating option picker widgets."""

    def __init__(self, container: DIContainer):
        """Initialize the factory with a DI container."""
        self.container = container

    def create_option_picker(self, parent: Optional[QWidget] = None) -> QWidget:
        """Create an option picker widget."""
        from desktop.modern.presentation.components.option_picker.components.option_picker_widget import (
            OptionPickerWidget,
        )

        return OptionPickerWidget(parent)

    def create_filter_widget(self, parent: Optional[QWidget] = None) -> QWidget:
        """Create a filter widget for the option picker."""
        from desktop.modern.presentation.components.option_picker.components.option_filter import (
            OptionPickerFilter,
        )

        return OptionPickerFilter(parent)


class WidgetFactory:
    """Main widget factory for the application."""

    def __init__(self, container: DIContainer):
        """Initialize the factory with a DI container."""
        self.container = container
        self.option_picker_factory = OptionPickerWidgetFactory(container)

    def create_option_picker(self, parent: Optional[QWidget] = None) -> QWidget:
        """Create an option picker widget."""
        return self.option_picker_factory.create_option_picker(parent)

    def create_filter_widget(self, parent: Optional[QWidget] = None) -> QWidget:
        """Create a filter widget."""
        return self.option_picker_factory.create_filter_widget(parent)

    def create_pictograph_widget(self, parent: Optional[QWidget] = None):
        """Create a pictograph view with injected dependencies."""
        from desktop.modern.presentation.components.pictograph.views import (
            create_pictograph_view,
        )

        return create_pictograph_view("base", parent=parent)


# Export the main classes
__all__ = [
    "OptionPickerWidgetFactory",
    "WidgetFactory",
]
