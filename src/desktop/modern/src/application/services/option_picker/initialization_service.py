"""
Option Picker Initialization Service

Pure service for handling complex option picker initialization logic.
Extracted from OptionPicker to follow single responsibility principle.

This service handles:
- Component creation and dependency resolution
- Widget hierarchy setup
- Service initialization coordination
- Progress reporting during initialization

Uses dependency injection and follows TKA's clean architecture.
"""

import logging
from typing import Dict, Any, Optional, Callable, Tuple
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from core.interfaces.option_picker_services import (
    IOptionPickerInitializationService,
)
from core.interfaces.core_services import ILayoutService
from core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class OptionPickerInitializationService(IOptionPickerInitializationService):
    """
    Pure service for option picker initialization logic.

    Handles the complex initialization sequence without any UI concerns.
    Coordinates service creation and dependency resolution.
    """

    def __init__(self):
        """Initialize the initialization service."""

    def initialize_components(
        self,
        container: DIContainer,
        progress_callback: Optional[Callable[[str, float], None]] = None,
    ) -> Dict[str, Any]:
        """
        Initialize all option picker components.

        Args:
            container: DI container for service resolution
            progress_callback: Optional progress reporting callback

        Returns:
            Dictionary containing initialized components
        """
        components = {}

        try:
            if progress_callback:
                progress_callback("Resolving layout service", 0.1)

            # Resolve core services
            layout_service = container.resolve(ILayoutService)
            components["layout_service"] = layout_service

            if progress_callback:
                progress_callback("Creating widget factory", 0.15)

            # Create widget factory
            from application.services.option_picker.option_picker_widget_factory import OptionPickerWidgetFactory

            widget_factory = OptionPickerWidgetFactory(container)
            components["widget_factory"] = widget_factory

            if progress_callback:
                progress_callback("Initializing pool manager", 0.25)

            # Pool manager will be created after widget hierarchy
            components["pool_manager"] = None

            if progress_callback:
                progress_callback("Initializing beat data loader", 0.35)

            # Create beat data loader
            from presentation.components.option_picker.services.data.beat_loader import (
                BeatDataLoader,
            )

            beat_loader = BeatDataLoader()
            components["beat_loader"] = beat_loader

            if progress_callback:
                progress_callback("Components initialized", 0.4)

            return components

        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise

    def create_widget_hierarchy(
        self, container: DIContainer, resize_callback: Callable[[], None]
    ) -> Tuple[QWidget, QWidget, QVBoxLayout, QWidget]:
        """
        Create the widget hierarchy for option picker.

        Args:
            container: DI container for service resolution
            resize_callback: Callback for widget resize events

        Returns:
            Tuple of (main_widget, sections_container, sections_layout, filter_widget)
        """
        try:
            from application.services.option_picker.option_picker_widget_factory import OptionPickerWidgetFactory

            widget_factory = OptionPickerWidgetFactory(container)

            return widget_factory.create_widget(resize_callback)

        except Exception as e:
            logger.error(f"Error creating widget hierarchy: {e}")
            raise

    def create_pool_manager(
        self,
        main_widget: QWidget,
        beat_click_handler: Callable[[str], None],
        beat_data_click_handler: Callable[[object], None],
    ) -> Any:
        """
        Create and configure the pictograph pool manager.

        Args:
            main_widget: Main widget for pool manager
            beat_click_handler: Handler for beat clicks
            beat_data_click_handler: Handler for beat data clicks

        Returns:
            Configured pool manager
        """
        try:
            from presentation.components.option_picker.services.data.pool_manager import (
                PictographPoolManager,
            )

            pool_manager = PictographPoolManager(main_widget)
            pool_manager.set_click_handler(beat_click_handler)
            pool_manager.set_beat_data_click_handler(beat_data_click_handler)

            return pool_manager

        except Exception as e:
            logger.error(f"Error creating pool manager: {e}")
            raise

    def create_dimension_analyzer(
        self,
        main_widget: QWidget,
        sections_container: QWidget,
        sections_layout: QVBoxLayout,
        display_manager: Any,
    ) -> Any:
        """
        Create and configure the dimension analyzer.

        Args:
            main_widget: Main widget
            sections_container: Sections container
            sections_layout: Sections layout
            display_manager: Display manager

        Returns:
            Configured dimension analyzer
        """
        try:
            from presentation.components.option_picker.services.layout.dimension_calculator import (
                DimensionCalculator,
            )

            dimension_analyzer = DimensionCalculator()

            return dimension_analyzer

        except Exception as e:
            logger.error(f"Error creating dimension analyzer: {e}")
            raise

    def initialize_pool(
        self,
        pool_manager: Any,
        progress_callback: Optional[Callable[[str, float], None]] = None,
    ) -> None:
        """
        Initialize the pictograph pool.

        Args:
            pool_manager: Pool manager to initialize
            progress_callback: Optional progress reporting callback
        """
        try:
            if progress_callback:
                progress_callback("Initializing pictograph pool", 0.45)

            pool_manager.initialize_pool(progress_callback)

        except Exception as e:
            logger.error(f"Error initializing pool: {e}")
            raise

    def setup_filter_connections(
        self,
        filter_widget: QWidget,
        filter_change_handler: Callable[[str], None],
        progress_callback: Optional[Callable[[str, float], None]] = None,
    ) -> None:
        """
        Setup filter widget connections.

        Args:
            filter_widget: Filter widget
            filter_change_handler: Handler for filter changes
            progress_callback: Optional progress reporting callback
        """
        try:
            if progress_callback:
                progress_callback("Setting up filter connections", 0.9)

            filter_widget.filter_changed.connect(filter_change_handler)

        except Exception as e:
            logger.error(f"Error setting up filter connections: {e}")
            raise

    def validate_initialization(self, components: Dict[str, Any]) -> bool:
        """
        Validate that all required components were initialized.

        Args:
            components: Dictionary of initialized components

        Returns:
            True if all components are valid
        """
        required_components = ["layout_service", "widget_factory", "beat_loader"]

        for component_name in required_components:
            if component_name not in components or components[component_name] is None:
                logger.error(f"Required component not initialized: {component_name}")
                return False

        return True

    def get_initialization_info(self, components: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get information about the initialization process.

        Args:
            components: Dictionary of initialized components

        Returns:
            Dictionary with initialization information
        """
        return {
            "components_count": len(components),
            "components_initialized": list(components.keys()),
            "validation_passed": self.validate_initialization(components),
            "layout_service_available": components.get("layout_service") is not None,
            "widget_factory_available": components.get("widget_factory") is not None,
            "beat_loader_available": components.get("beat_loader") is not None,
        }
