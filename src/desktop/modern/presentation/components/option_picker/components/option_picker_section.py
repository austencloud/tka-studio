"""
Option Picker Section Widget - Clean Component Architecture

Qt presentation component that orchestrates specialized manager components.
Uses clean separation of concerns with focused, testable components.

Architecture:
- OptionPickerSectionStateManager: Handles all state management
- OptionPickerSectionLayoutManager: Handles layout and sizing
- OptionPickerSectionWidgetManager: Handles widget pooling and lifecycle
- OptionPickerSectionAnimationHandler: Handles animations
- OptionPickerSectionContentLoader: Orchestrates content loading
"""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QGroupBox

from desktop.modern.application.services.option_picker.option_configuration_service import (
    OptionConfigurationService,
)
from desktop.modern.application.services.option_picker.option_picker_size_calculator import (
    OptionPickerSizeCalculator,
)
from desktop.modern.application.services.option_picker.option_pool_service import (
    OptionPoolService,
)
from desktop.modern.core.interfaces.animation_core_interfaces import (
    IAnimationOrchestrator,
)
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.components.option_picker.components.option_picker_section_animation_handler import (
    OptionPickerSectionAnimationHandler,
)
from desktop.modern.presentation.components.option_picker.components.option_picker_section_content_loader import (
    OptionPickerSectionContentLoader,
)
from desktop.modern.presentation.components.option_picker.components.option_picker_section_layout_manager import (
    OptionPickerSectionLayoutManager,
)
from desktop.modern.presentation.components.option_picker.components.option_picker_section_state_manager import (
    OptionPickerSectionStateManager,
)
from desktop.modern.presentation.components.option_picker.components.option_picker_section_widget_manager import (
    OptionPickerSectionWidgetManager,
)
from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)


class OptionPickerSection(QGroupBox):
    """
    Option Picker Section with clean component architecture.

    Delegates responsibilities to specialized manager components
    for maintainable, testable code.
    """

    # Signal emitted when a pictograph is selected in this section
    pictograph_selected = pyqtSignal(object)  # PictographData

    def __init__(
        self,
        letter_type: LetterType,
        scroll_area,  # Parent scroll area
        mw_size_provider: Callable[[], QSize] | None = None,
        option_pool_service: OptionPoolService = None,
        option_config_service: OptionConfigurationService = None,
        size_calculator: OptionPickerSizeCalculator = None,
        animation_orchestrator: IAnimationOrchestrator | None = None,
    ):
        """Initialize with injected services."""
        super().__init__(None)

        # Store dependencies
        self.letter_type = letter_type
        self.scroll_area = scroll_area
        self.mw_size_provider = mw_size_provider

        # Initialize manager components
        self._state_manager = OptionPickerSectionStateManager(
            letter_type, scroll_area, option_config_service
        )

        self._widget_manager = OptionPickerSectionWidgetManager(
            letter_type, scroll_area, option_pool_service, self._on_pictograph_selected
        )

        self._layout_manager = OptionPickerSectionLayoutManager(
            self,
            letter_type,
            scroll_area,
            option_config_service,
            size_calculator,
            mw_size_provider,
        )

        self._animation_handler = OptionPickerSectionAnimationHandler(
            self, letter_type, animation_orchestrator
        )

        self._content_loader = OptionPickerSectionContentLoader(
            letter_type,
            self._state_manager,
            self._widget_manager,
            self._layout_manager,
            self._animation_handler,
        )

        # Header will be set during setup_components
        self.header = None

    def setup_components(self) -> None:
        """Setup Qt components."""
        self._setup_header()
        self._layout_manager.setup_layout(self.header)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._state_manager.set_ui_initialized(True)

    def _setup_header(self) -> None:
        """Setup section header."""
        from desktop.modern.presentation.components.option_picker.components.option_picker_section_header import (
            OptionPickerSectionHeader,
        )

        self.header = OptionPickerSectionHeader(self)
        self.header.type_button.clicked.connect(self.toggle_section)

    def load_options_from_sequence(
        self, pictographs_for_section: list[PictographData]
    ) -> None:
        """Load options for this section."""
        self._content_loader.load_options_from_sequence(pictographs_for_section)

    def clear_pictographs(self) -> None:
        """Clear pictographs."""
        self._content_loader.clear_all_content()

    def toggle_section(self) -> None:
        """Toggle section visibility."""
        self._layout_manager.toggle_pictograph_frame_visibility()

    def update_option_picker_width(self, width: int) -> None:
        """Update option picker width."""
        self._state_manager.update_option_picker_width(width)
        self._layout_manager.update_option_picker_width(width)

    def resizeEvent(self, event) -> None:
        """Handle Qt resize events."""
        if self._layout_manager.handle_resize_event(self._state_manager.is_loading()):
            super().resizeEvent(event)

    def _on_pictograph_selected(self, pictograph_data: PictographData) -> None:
        """Handle pictograph selection - emit Qt signal."""
        self.pictograph_selected.emit(pictograph_data)

    # Compatibility properties and methods for backward compatibility

    @property
    def pictographs(self):
        """Get pictographs dict for compatibility."""
        return self._widget_manager.get_widgets_dict()

    @property
    def pictograph_frames(self) -> list:
        """Get list of pictograph frames for compatibility."""
        return self._widget_manager.get_active_widgets()

    @property
    def pictograph_frame(self):
        """Get pictograph frame for compatibility."""
        return self._layout_manager.get_pictograph_frame()

    @property
    def pictographs_layout(self):
        """Get pictographs layout for compatibility."""
        return self._layout_manager.get_pictographs_layout()

    @property
    def is_groupable(self):
        """Get groupable status for compatibility."""
        return self._state_manager.is_groupable()

    @property
    def calculated_width(self):
        """Get calculated width for compatibility."""
        return self._layout_manager.get_calculated_width()

    @property
    def option_picker_width(self):
        """Get option picker width for compatibility."""
        return self._state_manager.get_option_picker_width()

    # Additional compatibility methods that may be called externally

    def add_pictograph(self, pictograph_frame) -> None:
        """Add pictograph for compatibility - delegates to layout manager."""
        # Check if layout is initialized before adding
        if not self._layout_manager.is_layout_initialized():
            print(
                f"❌ [SECTION] Layout not initialized for {self.letter_type}, skipping add_pictograph"
            )
            return

        position = self._widget_manager.get_active_widget_count()
        self._layout_manager.add_widget_to_grid(pictograph_frame, position)

    def _loading_options(self) -> bool:
        """Get loading state for compatibility."""
        return self._state_manager.is_loading()

    def _ui_initialized(self) -> bool:
        """Get UI initialized state for compatibility."""
        return self._state_manager.is_ui_initialized()

    def _scroll_area_ready(self) -> bool:
        """Get scroll area ready state for compatibility."""
        return self._state_manager.is_scroll_area_ready()

    def cleanup(self) -> None:
        """Clean up all manager components."""
        self._content_loader.cleanup()
        self._animation_handler.cleanup()
        self._widget_manager.cleanup()
        self._state_manager.cleanup()
