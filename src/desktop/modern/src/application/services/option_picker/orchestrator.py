"""
Option Picker Orchestrator

Thin coordination layer that orchestrates the complete option picker pipeline.
Extracted from OptionPicker to follow single responsibility principle.

This orchestrator:
- Coordinates initialization, data, display, and event services
- Implements the complete option picker interface
- Maintains clean separation between services
- Provides the main option picker interface for UI components

Follows TKA's dependency injection patterns and clean architecture.
"""

import logging
from typing import Any, Callable, Dict, List, Optional


from core.dependency_injection.di_container import DIContainer
from core.interfaces.option_picker_services import (
    IOptionPickerDataService,
    IOptionPickerDisplayService,
    IOptionPickerEventService,
    IOptionPickerInitializationService,
)
from domain.models.core_models import BeatData, SequenceData
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class OptionPickerOrchestrator(QObject):
    """
    Orchestrates the complete option picker pipeline.

    This is a thin coordination layer that delegates to specialized services:
    - Initialization service for component setup
    - Data service for beat data management
    - Display service for UI updates
    - Event service for interaction handling

    Follows TKA's clean architecture and dependency injection patterns.
    """

    # Signals for external communication
    option_selected = pyqtSignal(str)
    beat_data_selected = pyqtSignal(object)

    def __init__(
        self,
        container: DIContainer,
        initialization_service: Optional[IOptionPickerInitializationService] = None,
        data_service: Optional[IOptionPickerDataService] = None,
        display_service: Optional[IOptionPickerDisplayService] = None,
        event_service: Optional[IOptionPickerEventService] = None,
        progress_callback: Optional[Callable[[str, float], None]] = None,
    ):
        """
        Initialize the orchestrator with injected dependencies.

        Args:
            container: DI container for service resolution
            initialization_service: Service for initialization logic
            data_service: Service for data management
            display_service: Service for display management
            event_service: Service for event handling
            progress_callback: Optional progress reporting callback
        """
        super().__init__()

        self.container = container
        self.progress_callback = progress_callback

        # Initialize services with dependency injection
        if initialization_service is None:
            from application.services.option_picker.initialization_service import (
                OptionPickerInitializationService,
            )

            initialization_service = OptionPickerInitializationService()

        if display_service is None:
            from application.services.option_picker.display_service import (
                OptionPickerDisplayService,
            )

            display_service = OptionPickerDisplayService()

        if event_service is None:
            from application.services.option_picker.event_service import (
                OptionPickerEventService,
            )

            event_service = OptionPickerEventService()

        self.initialization_service = initialization_service
        self.display_service = display_service
        self.event_service = event_service

        # Data service will be created after beat loader is available
        self.data_service = data_service

        # Component references
        self.option_picker_widget: Optional[QWidget] = None
        self.sections_container: Optional[QWidget] = None
        self.sections_layout = None
        self.filter_widget: Optional[QWidget] = None
        self.pool_manager = None
        self.dimension_analyzer = None

        # Initialization state
        self._initialized = False

    def initialize(
        self, progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> None:
        """
        Initialize the option picker with all components.

        Args:
            progress_callback: Optional progress reporting callback
        """
        try:
            if progress_callback:
                self.progress_callback = progress_callback

            if self.progress_callback:
                self.progress_callback("Initializing components", 0.1)

            # Step 1: Initialize core components
            components = self.initialization_service.initialize_components(
                self.container, self.progress_callback
            )

            if self.progress_callback:
                self.progress_callback("Creating widget hierarchy", 0.2)

            # Step 2: Create widget hierarchy
            (
                self.option_picker_widget,
                self.sections_container,
                self.sections_layout,
                self.filter_widget,
            ) = self.initialization_service.create_widget_hierarchy(
                self.container, self._on_widget_resize
            )

            if self.progress_callback:
                self.progress_callback("Setting up pool manager", 0.3)

            # Step 3: Create pool manager
            self.pool_manager = self.initialization_service.create_pool_manager(
                self.option_picker_widget, self._handle_beat_click, self._handle_beat_data_click
            )

            if self.progress_callback:
                self.progress_callback("Initializing data service", 0.4)

            # Step 4: Create data service with beat loader
            beat_loader = components["beat_loader"]
            if self.data_service is None:
                from application.services.option_picker.data_service import (
                    OptionPickerDataService,
                )

                self.data_service = OptionPickerDataService(beat_loader)

            if self.progress_callback:
                self.progress_callback("Setting up display", 0.5)

            # Step 5: Initialize display service
            self.display_service.initialize_display(
                self.sections_container,
                self.sections_layout,
                self.pool_manager,
                self._create_size_provider(),
            )

            if self.progress_callback:
                self.progress_callback("Creating dimension analyzer", 0.6)

            # Step 6: Create dimension analyzer
            self.dimension_analyzer = (
                self.initialization_service.create_dimension_analyzer(
                    self.option_picker_widget,
                    self.sections_container,
                    self.sections_layout,
                    self.display_service,
                )
            )

            if self.progress_callback:
                self.progress_callback("Initializing pool", 0.7)

            # Step 7: Initialize pool
            self.initialization_service.initialize_pool(
                self.pool_manager, self.progress_callback
            )

            if self.progress_callback:
                self.progress_callback("Creating sections", 0.8)

            # Step 8: Create display sections
            self.display_service.create_sections()

            if self.progress_callback:
                self.progress_callback("Setting up events", 0.9)

            # Step 9: Setup event handlers
            self.event_service.setup_event_handlers(
                self.pool_manager,
                self.filter_widget,
                self._handle_beat_click,
                self._handle_beat_data_click,
                self._on_filter_changed,
            )

            # Step 10: Setup filter connections
            self.initialization_service.setup_filter_connections(
                self.filter_widget, self._on_filter_changed, self.progress_callback
            )

            if self.progress_callback:
                self.progress_callback("Loading initial options", 0.95)

            # Step 11: Load initial beat options
            beat_options = self.data_service.load_beat_options()
            self.display_service.update_beat_display(beat_options)

            if self.progress_callback:
                self.progress_callback("Initialization complete", 1.0)

            self._initialized = True
            logger.info("Option picker orchestrator initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize option picker orchestrator: {e}")
            raise

    def get_widget(self) -> QWidget:
        """
        Get the main widget for this component.

        Returns:
            Main option picker widget
        """
        if not self._initialized or not self.option_picker_widget:
            raise RuntimeError(
                "OptionPickerOrchestrator not initialized - call initialize() first"
            )
        return self.option_picker_widget

    def load_motion_combinations(self, sequence_data: List[Dict[str, Any]]) -> None:
        """
        Load motion combinations from sequence data.

        Args:
            sequence_data: Sequence data to load combinations from
        """
        try:
            if not self._initialized:
                logger.warning("Orchestrator not initialized")
                return

            beat_options = self.data_service.refresh_from_sequence_data(sequence_data)
            self.display_service.update_beat_display(beat_options)
            self.display_service.ensure_sections_visible()

            logger.debug(f"Loaded motion combinations: {len(beat_options)} options")

        except Exception as e:
            logger.error(f"Error loading motion combinations: {e}")

    def refresh_options(self) -> None:
        """Refresh the option picker with latest beat options."""
        try:
            if not self._initialized:
                logger.warning("Orchestrator not initialized")
                return

            beat_options = self.data_service.refresh_options()
            self.display_service.update_beat_display(beat_options)

            logger.debug(f"Refreshed options: {len(beat_options)} options")

        except Exception as e:
            logger.error(f"Error refreshing options: {e}")

    def refresh_from_sequence(self, sequence: SequenceData) -> None:
        """
        Refresh options based on modern sequence data.

        Args:
            sequence: Modern sequence data
        """
        try:
            if not self._initialized:
                logger.warning("Orchestrator not initialized")
                return

            beat_options = self.data_service.refresh_from_sequence(sequence)
            self.display_service.update_beat_display(beat_options)

            logger.debug(f"Refreshed from modern sequence: {len(beat_options)} options")

        except Exception as e:
            logger.error(f"Error refreshing from modern sequence: {e}")

    def get_beat_data_for_option(self, option_id: str) -> Optional[BeatData]:
        """
        Get beat data for a specific option ID.

        Args:
            option_id: Option identifier

        Returns:
            BeatData if found, None otherwise
        """
        try:
            if not self._initialized:
                logger.warning("Orchestrator not initialized")
                return None

            return self.data_service.get_beat_data_for_option(option_id)

        except Exception as e:
            logger.error(f"Error getting beat data for option: {e}")
            return None

    def cleanup(self) -> None:
        """Clean up option picker resources."""
        try:
            if self.event_service:
                self.event_service.cleanup()

            if self.display_service:
                self.display_service.cleanup()

            if self.data_service:
                self.data_service.clear_cache()

            # Clear references
            self.option_picker_widget = None
            self.sections_container = None
            self.sections_layout = None
            self.filter_widget = None
            self.pool_manager = None
            self.dimension_analyzer = None

            self._initialized = False
            logger.debug("Option picker orchestrator cleaned up")

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    def _create_size_provider(self) -> Callable:
        """Create size provider function for display manager."""

        def size_provider():
            from PyQt6.QtCore import QSize

            if self.option_picker_widget and self.option_picker_widget.width() > 0:
                actual_width = self.option_picker_widget.width()
                actual_height = self.option_picker_widget.height()
                return QSize(actual_width, actual_height)
            else:
                return QSize(1200, 800)

        return size_provider

    def _handle_beat_click(self, beat_id: str) -> None:
        """Handle beat selection clicks (legacy compatibility)."""
        self.event_service.emit_option_selected(beat_id, self)

    def _handle_beat_data_click(self, beat_data: BeatData) -> None:
        """Handle beat data selection clicks (modern method)."""
        self.event_service.emit_beat_data_selected(beat_data, self)

    def _on_widget_resize(self) -> None:
        """Handle widget resize events."""
        if self._initialized:
            self.event_service.handle_widget_resize(
                self.pool_manager, self.display_service
            )

    def _on_filter_changed(self, filter_text: str) -> None:
        """Handle filter changes."""
        if self._initialized:
            self.event_service.handle_filter_change(
                filter_text, self.data_service, self.display_service
            )
