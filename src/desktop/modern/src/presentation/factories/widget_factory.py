"""
Widget Factory for TKA Modern Desktop Application

This module provides factory classes for creating various UI widgets
with proper dependency injection and configuration.
"""

from typing import Optional, TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

if TYPE_CHECKING:
    from core.dependency_injection.di_container import DIContainer


class OptionPickerWidgetFactory:
    """Factory for creating option picker widgets."""
    
    def __init__(self, container: "DIContainer"):
        """Initialize the factory with a DI container."""
        self.container = container
    
    def create_option_picker(self, parent: Optional[QWidget] = None) -> QWidget:
        """Create an option picker widget."""
        from presentation.components.option_picker.core.option_picker_widget import OptionPickerWidget
        return OptionPickerWidget(parent)
    
    def create_filter_widget(self, parent: Optional[QWidget] = None) -> QWidget:
        """Create a filter widget for the option picker."""
        from presentation.components.option_picker.components.filters.option_filter import OptionPickerFilter
        return OptionPickerFilter(parent)


class WidgetFactory:
    """Main widget factory for the application."""
    
    def __init__(self, container: "DIContainer"):
        """Initialize the factory with a DI container."""
        self.container = container
        self.option_picker_factory = OptionPickerWidgetFactory(container)
    
    def create_option_picker(self, parent: Optional[QWidget] = None) -> QWidget:
        """Create an option picker widget."""
        return self.option_picker_factory.create_option_picker(parent)
    
    def create_filter_widget(self, parent: Optional[QWidget] = None) -> QWidget:
        """Create a filter widget."""
        return self.option_picker_factory.create_filter_widget(parent)


# Export the main classes
__all__ = [
    "WidgetFactory",
    "OptionPickerWidgetFactory",
]
