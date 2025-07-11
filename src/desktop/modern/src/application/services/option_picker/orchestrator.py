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
from core.interfaces.option_picker_interfaces import (
    IOptionPickerDataManager,
    IOptionPickerDisplayService,
    IOptionPickerEventService,
    IOptionPickerInitializer,
)
from domain.models.pictograph_models import PictographData
from domain.models.sequence_models import SequenceData
from presentation.components.option_picker.components.sections.section_widget import (
    OptionPickerSection,
)
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class OptionPickerOrchestrator(QObject):
    """
    Orchestrates the complete option picker pipeline.

    This is a thin coordination layer that delegates to specialized services:
    - Initialization service for component setup
    - Data service for pictograph data management
    - Display service for UI updates
    - Event service for interaction handling

    Follows TKA's clean architecture and dependency injection patterns.
    Works exclusively with PictographData.
    """

    # Signals for external communication
    option_selected = pyqtSignal(str)
    pictograph_selected = pyqtSignal(object)  # PictographData object

    def __init__(
        self,
        container: DIContainer,
        initialization_service: Optional[IOptionPickerInitializer] = None,
        data_service: Optional[IOptionPickerDataManager] = None,
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
            from application.services.option_picker.option_picker_initializer import (
                OptionPickerInitializer,
            )

            initialization_service = OptionPickerInitializer()

        if display_service is None:
            from application.services.option_picker.option_picker_display_manager import (
                OptionPickerDisplayManager,
            )

            display_service = OptionPickerDisplayManager()

        if event_service is None:
            from application.services.option_picker.option_picker_event_service import (
                OptionPickerEventService,
            )

            event_service = OptionPickerEventService()

        self.initialization_service = initialization_service
        self.display_service = display_service
        self.event_service = event_service

        # Data service will be created after beat loader is available
        self.data_service = data_service
        self.option_service = None

        # Component references
        self.option_picker_widget: Optional[QWidget] = None
        self.sections_container: Optional[QWidget] = None
        self.sections_layout = None
        self.filter_widget: Optional[QWidget] = None
        self.pool_manager = None
        self.dimension_analyzer = None

        # Section management (following legacy pattern)
        self.sections: Dict[str, "OptionPickerSection"] = {}

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
                self.option_picker_widget,
                self._handle_option_click,
                self._handle_pictograph_click,
            )

            if self.progress_callback:
                self.progress_callback("Initializing data service", 0.4)

            # Step 4: Get option service
            self.option_service = components["option_service"]

            if self.progress_callback:
                self.progress_callback("Setting up display", 0.5)

            # Step 5: Initialize display service
            self.display_service.initialize_display(
                self.sections_container,
                self.sections_layout,
                self.pool_manager,
                self._create_size_provider(),
            )

            # Step 5.5: Create actual section widgets (missing piece!)
            self._create_sections()

            # Step 5.6: Make widgets visible
            self._make_widgets_visible()

            if self.progress_callback:
                self.progress_callback("Creating dimension analyzer", 0.6)

            # Step 6: Create dimension analyzer
            self.dimension_analyzer = (
                self.initialization_service.create_dimension_calculator(
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
                self._handle_option_click,
                self._handle_pictograph_click,
                self._on_filter_changed,
            )

            # Step 10: Setup filter connections
            self.initialization_service.setup_filter_connections(
                self.filter_widget, self._on_filter_changed, self.progress_callback
            )

            if self.progress_callback:
                self.progress_callback("Loading initial options", 0.95)

            # Step 11: Load initial pictograph options
            pictograph_options = self.option_service.get_current_options()
            self.display_service.update_pictograph_display(pictograph_options)

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

            pictograph_options = self.option_service.load_options_from_sequence(
                sequence_data
            )
            display_result = self.display_service.update_pictograph_display(
                pictograph_options
            )

            # Apply the display strategy to actually show the options
            if display_result.get("success", False):
                self._apply_display_strategy(display_result["display_strategy"])

            self.display_service.ensure_sections_visible()

            logger.debug(
                f"Loaded motion combinations: {len(pictograph_options)} options"
            )

        except Exception as e:
            logger.error(f"Error loading motion combinations: {e}")

    def _apply_display_strategy(self, display_strategy: dict) -> None:
        """
        Apply the display strategy to actually show the options in the UI.

        Args:
            display_strategy: The calculated display strategy from DisplayManager
        """
        try:
            if not self.sections_container or not self.pool_manager:
                logger.warning(
                    "UI components not available for display strategy application"
                )
                return

            # Get the pictograph assignments from the strategy
            pictograph_assignments = display_strategy.get("pictograph_assignments", {})
            organized_pictographs = display_strategy.get("organized_pictographs", {})

            logger.debug(
                f"Applying display strategy for {len(organized_pictographs)} letter types"
            )

            # Apply assignments for each letter type section
            for letter_type in organized_pictographs:
                pictographs_for_type = organized_pictographs[letter_type]
                if not pictographs_for_type:
                    continue

                # Get or create section for this letter type
                section = self._get_or_create_section(letter_type)
                if not section:
                    continue

                # Remove existing pictographs from section (without destroying them for pool reuse)
                section.remove_pictographs_for_reuse()

                # Add new pictographs to the section
                frames_to_add = []
                for pool_index, pictograph_data in pictographs_for_type:
                    # Get frame from pool
                    frame = self.pool_manager.get_pictograph_from_pool(pool_index)
                    if frame:
                        # Debug: Check frame state before update
                        has_component_before = (
                            hasattr(frame, "pictograph_component")
                            and frame.pictograph_component
                        )
                        logger.debug(
                            f"🔍 Frame {id(frame)} from pool: has_component={has_component_before}"
                        )

                        # Update frame with new pictograph data
                        frame.update_pictograph_data(pictograph_data)
                        frames_to_add.append(frame)

                # Add all frames to the section at once (batch operation)
                if frames_to_add:
                    # Debug: Check frame states before passing to section
                    for i, frame in enumerate(frames_to_add):
                        has_component = (
                            hasattr(frame, "pictograph_component")
                            and frame.pictograph_component
                        )
                        logger.debug(
                            f"   📦 Frame {i} before section: has_component={has_component}"
                        )

                    section.add_multiple_pictographs_from_pool(frames_to_add)
                    logger.debug(
                        f"Added {len(frames_to_add)} options to {letter_type} section"
                    )

            logger.debug("Display strategy applied successfully")

        except Exception as e:
            logger.error(f"Error applying display strategy: {e}")
            import traceback

            traceback.print_exc()

    def _create_sections(self) -> None:
        """
        Create actual section widgets and add them to the layout.

        This implements the missing piece from the modern architecture:
        creating actual OptionPickerSection widgets and storing them
        for later access, following the legacy pattern.
        """
        try:
            logger.debug("Creating section widgets...")

            # Get section creation specifications from display service
            section_specs_result = self.display_service.create_sections()
            if not section_specs_result.get("success", False):
                logger.error(
                    f"Failed to get section specifications: {section_specs_result}"
                )
                return

            section_specs = section_specs_result["section_specifications"]
            bottom_row_config = section_specs_result["bottom_row_configuration"]

            # Import section widget class
            from presentation.components.option_picker.components.sections.section_widget import (
                OptionPickerSection,
            )
            from presentation.components.option_picker.types.letter_types import (
                LetterType,
            )
            from PyQt6.QtWidgets import QHBoxLayout

            # Create individual sections (Types 1-3)
            individual_sections = []
            for letter_type in [LetterType.TYPE1, LetterType.TYPE2, LetterType.TYPE3]:
                if letter_type in section_specs:
                    section = OptionPickerSection(
                        letter_type=letter_type,
                        parent=self.sections_container,
                        option_picker_size_provider=self._create_size_provider(),
                    )
                    self.sections[letter_type] = section
                    individual_sections.append(section)

                    # Add to main layout
                    self.sections_layout.addWidget(section)
                    logger.debug(f"Created and added individual section: {letter_type}")

            # Create bottom row sections (Types 4-6) in shared layout
            bottom_row_sections = []
            for letter_type in [LetterType.TYPE4, LetterType.TYPE5, LetterType.TYPE6]:
                if letter_type in section_specs:
                    section = OptionPickerSection(
                        letter_type=letter_type,
                        parent=self.sections_container,
                        option_picker_size_provider=self._create_size_provider(),
                    )
                    self.sections[letter_type] = section
                    bottom_row_sections.append(section)
                    logger.debug(f"Created bottom row section: {letter_type}")

            # Add bottom row sections to shared horizontal layout
            if bottom_row_sections:
                bottom_row_layout = QHBoxLayout()
                bottom_row_layout.addStretch()  # Center the sections

                for section in bottom_row_sections:
                    bottom_row_layout.addWidget(section)

                bottom_row_layout.addStretch()  # Center the sections
                self.sections_layout.addLayout(bottom_row_layout)
                logger.debug(
                    f"Added {len(bottom_row_sections)} sections to bottom row layout"
                )

            logger.debug(f"Successfully created {len(self.sections)} section widgets")

        except Exception as e:
            logger.error(f"Error creating sections: {e}")
            import traceback

            traceback.print_exc()

    def _make_widgets_visible(self) -> None:
        """
        Make the option picker widgets visible.

        This ensures that the main widget and all sections are visible
        so that the frames can be displayed to the user.
        """
        try:
            logger.debug("Making widgets visible...")

            # Make main option picker widget visible
            if self.option_picker_widget:
                self.option_picker_widget.setVisible(True)
                self.option_picker_widget.show()
                logger.debug("Main option picker widget made visible")

            # Make sections container visible
            if self.sections_container:
                self.sections_container.setVisible(True)
                self.sections_container.show()
                logger.debug("Sections container made visible")

            # Make all sections visible
            for letter_type, section in self.sections.items():
                if section:
                    section.setVisible(True)
                    section.show()

                    # Also make the section container visible
                    if hasattr(section, "section_pictograph_container"):
                        section.section_pictograph_container.setVisible(True)
                        section.section_pictograph_container.show()

                    logger.debug(f"Section {letter_type} made visible")

            logger.debug(f"Successfully made {len(self.sections)} sections visible")

        except Exception as e:
            logger.error(f"Error making widgets visible: {e}")
            import traceback

            traceback.print_exc()

    def _get_or_create_section(self, letter_type: str):
        """Get existing section widget for the letter type."""
        # Return the actual section widget that was created during initialization
        logger.debug(f"🔍 Looking for section: {letter_type}")
        logger.debug(f"   📋 Available sections: {list(self.sections.keys())}")
        logger.debug(f"   🔢 Total sections: {len(self.sections)}")

        section = self.sections.get(letter_type)
        if section:
            logger.debug(
                f"✅ Found existing section for {letter_type}: {type(section)}"
            )
            return section
        else:
            logger.warning(
                f"❌ No section found for {letter_type} - sections available: {list(self.sections.keys())}"
            )
            return None

    def refresh_options(self) -> None:
        """Refresh the option picker with latest pictograph options."""
        try:
            if not self._initialized:
                logger.warning("Orchestrator not initialized")
                return

            pictograph_options = self.option_service.get_current_options()
            display_result = self.display_service.update_pictograph_display(
                pictograph_options
            )

            # Apply the display strategy to actually show the options
            if display_result.get("success", False):
                self._apply_display_strategy(display_result["display_strategy"])

            logger.debug(f"Refreshed options: {len(pictograph_options)} options")

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

            pictograph_options = self.option_service.load_options_from_modern_sequence(
                sequence
            )
            display_result = self.display_service.update_pictograph_display(
                pictograph_options
            )

            # Apply the display strategy to actually show the options
            if display_result.get("success", False):
                self._apply_display_strategy(display_result["display_strategy"])

            logger.debug(
                f"Refreshed from modern sequence: {len(pictograph_options)} options"
            )

        except Exception as e:
            logger.error(f"Error refreshing from modern sequence: {e}")

    def get_pictograph_for_option(self, option_id: str) -> Optional[PictographData]:
        """
        Get pictograph data for a specific option ID.

        Args:
            option_id: Option identifier

        Returns:
            PictographData if found, None otherwise
        """
        try:
            if not self._initialized:
                logger.warning("Orchestrator not initialized")
                return None

            # Extract index from option_id (e.g., "option_0" -> 0)
            try:
                index = int(option_id.split("_")[-1])
                pictograph_options = self.option_service.get_current_options()
                if 0 <= index < len(pictograph_options):
                    return pictograph_options[index]
            except (ValueError, IndexError):
                logger.warning(f"Invalid option_id format: {option_id}")
            return None

        except Exception as e:
            logger.error(f"Error getting pictograph for option: {e}")
            return None

    def cleanup(self) -> None:
        """Clean up option picker resources."""
        try:
            if self.event_service:
                self.event_service.cleanup()

            if self.display_service:
                self.display_service.cleanup()

            if self.option_service:
                self.option_service.clear_options()

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

    def _handle_option_click(self, option_id: str) -> None:
        """Handle option selection clicks."""
        self.option_selected.emit(option_id)

    def _handle_pictograph_click(self, pictograph_data: PictographData) -> None:
        """Handle pictograph data selection clicks."""
        self.pictograph_selected.emit(pictograph_data)

    def _on_widget_resize(self) -> None:
        """Handle widget resize events."""
        if self._initialized:
            self.event_service.handle_widget_resize(
                self.pool_manager, self.display_service
            )

    def _on_filter_changed(self, filter_text: str) -> None:
        """Handle filter changes."""
        if self._initialized:
            # TODO: Update to use option_service instead of data_service
            self.event_service.handle_filter_change(
                filter_text, self.data_service, self.display_service
            )
