"""
Simplified Option Picker Widget - Clean UI Layer

Pure Qt presentation component with business logic extracted to services.
Uses dependency injection for clean separation of concerns.

Key principles:
- Pure Qt UI logic only - no business logic
- Clean dependency injection of services
- Qt widget management in presentation layer
- Coordination between UI and services
"""

from __future__ import annotations

from collections.abc import Callable
import logging
import traceback
from typing import TYPE_CHECKING

from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from desktop.modern.application.services.option_picker.option_picker_size_calculator import (
    OptionPickerSizeCalculator,
)
from desktop.modern.application.services.option_picker.option_pool_service import (
    OptionPoolService,
)
from desktop.modern.application.services.option_picker.sequence_option_service import (
    SequenceOptionService,
)
from desktop.modern.core.interfaces.animation_core_interfaces import (
    IAnimationOrchestrator,
)
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.components.option_picker.components.option_pictograph import (
    OptionPictograph,
)
from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)

# Import our new focused components
from .option_picker_animator import OptionPickerAnimator
from .option_picker_layout_orchestrator import OptionPickerLayoutOrchestrator
from .option_picker_refresh_orchestrator import OptionPickerRefreshOrchestrator
from .option_picker_section_manager import OptionPickerSectionManager
from .option_picker_size_manager import OptionPickerSizeManager


if TYPE_CHECKING:
    from desktop.modern.application.services.option_picker.option_configuration_service import (
        OptionConfigurationService,
    )
    from desktop.modern.presentation.components.option_picker.components.option_picker_section import (
        OptionPickerSection,
    )


class OptionPickerScroll(QScrollArea):
    """
    Clean UI component for option picker.

    All business logic extracted to injected services.
    """

    # Signal emitted when a pictograph is selected in any section
    pictograph_selected = pyqtSignal(object)  # PictographData

    def __init__(
        self,
        sequence_option_service: SequenceOptionService,
        option_pool_service: OptionPoolService,
        option_sizing_service: OptionPickerSizeCalculator,
        option_config_service: OptionConfigurationService,
        parent=None,
        mw_size_provider: Callable[[], QSize] | None = None,
        animation_orchestrator: IAnimationOrchestrator | None = None,
    ):
        """Initialize with injected services - no service location."""
        super().__init__(parent)

        # ✅ Clean dependency injection - no service location
        self._sequence_option_service = sequence_option_service
        self._option_pool_service = option_pool_service
        self._option_sizing_service = option_sizing_service
        self._option_config_service = option_config_service
        self._animation_orchestrator = animation_orchestrator

        # DEBUG: Log animation orchestrator availability
        logger = logging.getLogger(__name__)
        if self._animation_orchestrator:
            logger.info("✅ OptionPickerScroll initialized WITH animation orchestrator")
        else:
            logger.warning(
                "⚠️ OptionPickerScroll initialized WITHOUT animation orchestrator"
            )

        self._mw_size_provider = mw_size_provider or self._default_size_provider

        # State tracking
        self._loading_options = False

        # UI setup
        self._setup_layout()
        self._initialize_components()
        self._setup_ui_properties()

        # Fade transition state (legacy compatibility)
        self._pending_fade_sequence_data = None
        self._pending_fade_pictograph_frames = None

        # Initialization state
        self._all_sections_initialized = False

        # Initial size update (deferred to allow parent layout to complete)
        QTimer.singleShot(100, self._update_size)

    @property
    def mw_size_provider(self) -> Callable[[], QSize]:
        """Get the main window size provider."""
        return self._mw_size_provider

    @mw_size_provider.setter
    def mw_size_provider(self, value: Callable[[], QSize]):
        """Set the main window size provider and update all sections."""
        self._mw_size_provider = value
        # CRITICAL: Update all existing sections with the new size provider
        if hasattr(self, "sections"):
            for section in self.sections.values():
                section.mw_size_provider = value

    def _default_size_provider(self) -> QSize:
        """Default size provider if none provided."""
        return QSize(800, 600)

    def _initialize_components(self):
        """Initialize all focused components."""
        # Initialize size manager
        self._size_manager = OptionPickerSizeManager(
            self.container, self._mw_size_provider
        )

        # Initialize layout orchestrator
        self._layout_orchestrator = OptionPickerLayoutOrchestrator(
            self.layout, self.container, self._option_config_service
        )

        # Initialize animator
        self._animator = OptionPickerAnimator(self.container)

        # Initialize widget pool with lazy loading for better memory efficiency
        self._widget_pool: dict[int, OptionPictograph] = {}
        self._max_widgets = self._option_config_service.get_total_max_pictographs()

        # OPTIMIZED: Use lazy initialization instead of pre-creating all widgets
        # Widgets will be created on-demand when requested

        # Initialize sections and section manager
        self._initialize_sections()
        self._section_manager = OptionPickerSectionManager(self.sections)

        # Initialize refresh orchestrator
        self._refresh_orchestrator = OptionPickerRefreshOrchestrator(
            self._option_config_service, self._handle_refresh_request
        )

    def _setup_layout(self):
        """Setup Qt layout - pure UI logic."""
        self.setWidgetResizable(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: transparent; border: none;")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.container = QWidget()
        self.container.setAutoFillBackground(True)
        self.container.setStyleSheet("background: transparent;")
        self.container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # FIXED: Ensure container fills the full scroll area width
        from PyQt6.QtWidgets import QSizePolicy

        self.container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

        self.container.setLayout(self.layout)
        self.setWidget(self.container)

    def _setup_ui_properties(self):
        """Setup Qt-specific UI properties."""
        # Disable scroll bars like Legacy
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Enable scroll bars for content overflow
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Transparency setup
        self.viewport().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _initialize_sections(self) -> None:
        """Create and add sections - Qt layout management."""
        from desktop.modern.presentation.components.option_picker.components.group_widget import (
            OptionPickerGroupWidget,
        )

        self.sections: dict[LetterType, OptionPickerSection] = {}
        individual_sections = []
        grouped_sections = []

        for letter_type in LetterType.ALL_TYPES:
            # Pass services to sections via dependency injection
            from desktop.modern.presentation.components.option_picker.components.option_picker_section import (
                OptionPickerSection,
            )

            section = OptionPickerSection(
                letter_type=letter_type,
                scroll_area=self,
                mw_size_provider=self._mw_size_provider,
                option_pool_service=self._option_pool_service,
                option_config_service=self._option_config_service,
                size_calculator=self._option_sizing_service,
                animation_orchestrator=self._animation_orchestrator,
            )
            self.sections[letter_type] = section
            section.setup_components()

            # Connect Qt signals
            section.pictograph_selected.connect(self._on_pictograph_selected)

            # Organize sections by type
            if self._option_config_service.is_groupable_type(letter_type):
                grouped_sections.append(section)
            else:
                individual_sections.append(section)

        # Add individual sections first (Type 1, 2, 3)
        for section in individual_sections:
            self.layout.addWidget(section)

        # Add grouped sections in a horizontal layout (Type 4, 5, 6)
        if grouped_sections:
            group_widget = OptionPickerGroupWidget(self)
            for section in grouped_sections:
                group_widget.add_section_widget(section)
            self.layout.addWidget(group_widget)

        # Layout orchestrator will handle spacing when header is added

        # Mark all sections as initialized
        self._all_sections_initialized = True

    def add_header_label(self, header_widget: QWidget) -> None:
        """Add a header label widget at the top of the scroll area with balanced spacing."""
        # Delegate to layout orchestrator
        self._layout_orchestrator.add_header_widget(header_widget)
        self._layout_orchestrator.apply_balanced_spacing()

    def clear_all_sections(self):
        """Clear all pictographs from all sections using section manager."""
        self._section_manager.clear_all_sections()
        self._option_pool_service.reset_pool()

    def _reset_widget_cache(self) -> None:
        """Reset widget pool by hiding and cleaning up all widgets."""
        for widget in self._widget_pool.values():
            widget.hide()
            # CRITICAL FIX: Remove widget from parent to prevent findChildren() from finding it
            if widget.parent():
                widget.setParent(None)

        # OPTIMIZED: Clear the pool completely for better memory management
        # Widgets will be recreated on-demand when needed
        self._widget_pool.clear()

    def _update_size(self):
        """Update picker size using legacy-style approach, but defer until main window is properly shown."""
        try:
            # Check if main window is properly shown before sizing
            if not self._is_main_window_ready():
                QTimer.singleShot(200, self._update_size)
                return

            # Legacy approach: use parent container width directly
            # This mimics: self.option_scroll.setFixedWidth(self.parent().parent().width() // 2)

            # Try to get parent width first (immediate parent)
            if self.parent():
                parent_width = self.parent().width()

                if parent_width > 622:  # Valid parent width (not splash screen size)
                    # Use the full parent width (the parent should be sized correctly)
                    width = parent_width
                else:
                    # Fallback to main window calculation
                    main_window_size = self._mw_size_provider()
                    width = main_window_size.width() // 2
            else:
                # No parent, use main window calculation
                main_window_size = self._mw_size_provider()
                width = main_window_size.width() // 2

            # Set the width
            self.setFixedWidth(width)

            # Ensure container also uses full width
            if hasattr(self, "container"):
                self.container.setMinimumWidth(width)

            # Update all sections with the new picker width
            self._section_manager.update_all_sections_picker_width(width)

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.warning(f"Error in _update_size: {e}")
            # Fallback to a reasonable default
            self.setFixedWidth(400)

    def _is_main_window_ready(self) -> bool:
        """Check if the main window is properly shown and ready for sizing."""
        try:
            from PyQt6.QtWidgets import QApplication

            # Get the main window from QApplication
            app = QApplication.instance()
            if not app:
                return False

            # Find the main window
            for widget in app.topLevelWidgets():
                if widget.objectName() == "TKAMainWindow" or "MainWindow" in str(
                    type(widget)
                ):
                    # Check if main window is visible and has proper size
                    if widget.isVisible() and widget.width() > 800:
                        return True

            return False

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.warning(f"Error checking main window readiness: {e}")
            return False

    def load_options_from_sequence(self, sequence_data: SequenceData) -> None:
        """Load options with debouncing - delegated to refresh orchestrator."""
        self._refresh_orchestrator.load_options_from_sequence(sequence_data)

    def prepare_for_transition(self) -> None:
        """Prepare content for widget transition - delegated to refresh orchestrator."""
        self._refresh_orchestrator.prepare_for_transition()

    def _handle_refresh_request(self, sequence_data: SequenceData) -> None:
        """Handle refresh request from orchestrator."""
        logger = logging.getLogger(__name__)

        try:
            # Set UI loading state
            self._set_loading_state(True)

            # Skip fade animations if preparing for widget transition
            if self._refresh_orchestrator.is_preparing_for_transition():
                self._update_all_sections_directly(sequence_data)
                return

            # Check if we have existing content to fade
            existing_sections = [
                section for section in self.sections.values() if section.pictographs
            ]

            # DEBUG: Log animation decision
            logger.debug(
                f"Animation orchestrator available: {self._animation_orchestrator is not None}"
            )
            logger.debug(f"Existing sections count: {len(existing_sections)}")

            if self._animation_orchestrator and existing_sections:
                logger.info("🎭 Using fade animations for option update")
                self._fade_and_update_all_sections(sequence_data)
            else:
                if not self._animation_orchestrator:
                    logger.warning("⚠️ No animation orchestrator - using direct update")
                if not existing_sections:
                    logger.debug("No existing sections - using direct update")
                self._update_all_sections_directly(sequence_data)

        except Exception as e:
            logger.exception(f"Error during refresh: {e}")
            traceback.print_exc()
            # Fallback to direct update to ensure UI doesn't get stuck
            try:
                self._update_all_sections_directly(sequence_data)
            except Exception as fallback_error:
                logger.exception(f"Fallback update also failed: {fallback_error}")
        finally:
            # Always reset loading state
            self._set_loading_state(False)

    def _update_all_sections_directly(self, sequence_data: SequenceData) -> None:
        """Update all sections directly without animation using section manager."""
        try:
            # ✅ Use service to get options (pure business logic)
            options_by_type = self._sequence_option_service.get_options_for_sequence(
                sequence_data
            )

            if not options_by_type:
                logger = logging.getLogger(__name__)
                logger.warning("No options received from service")
                return

            # DEBUG: Check if orientations are preserved when options reach the UI (simplified)
            total_options = sum(
                len(options_list) for options_list in options_by_type.values()
            )
            logger = logging.getLogger(__name__)
            logger.debug(
                f"UI received {total_options} total options across {len(options_by_type)} letter types"
            )

            # PAGINATION FIX: Reset widget cache to ensure clean state
            # This prevents pool exhaustion that causes the pagination issue
            self._reset_widget_cache()

            # ✅ Update UI sections using section manager
            self._section_manager.update_all_sections_directly(
                sequence_data, options_by_type
            )

            # ✅ Apply sizing using service (defer with longer delay during startup)
            # Use longer delay during sequence restoration to ensure UI is fully initialized
            delay = 500 if self._size_manager.should_defer_sizing() else 50
            QTimer.singleShot(delay, self._apply_sizing_to_all_frames)

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(f"Error in direct update: {e}")

    def _fade_and_update_all_sections(self, sequence_data: SequenceData) -> None:
        """Fade pictographs only (keeping headers stable) using animator component."""
        try:
            # Get all pictograph frames (not the whole sections)
            pictograph_frames = self._section_manager.get_all_pictograph_frames()

            if not pictograph_frames:
                self._update_all_sections_directly(sequence_data)
                return

            # Use animator component for fade transition
            def update_callback():
                self._update_all_sections_directly(sequence_data)

            def fade_in_callback():
                # Get the new frames after content update and fade them in
                new_frames = self._section_manager.get_all_pictograph_frames()
                if new_frames:
                    # Use the section animation handler to fade in the new frames
                    for section in self._section_manager._sections.values():
                        if hasattr(section, "_animation_handler"):
                            section_frames = (
                                section._widget_manager.get_active_widgets()
                            )
                            if section_frames:
                                section._animation_handler.fade_in_frames(
                                    section_frames
                                )

            self._animator.fade_out_and_update(
                pictograph_frames, update_callback, fade_in_callback
            )

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(f"Fade transition failed: {e}")
            # Fallback to direct update
            self._update_all_sections_directly(sequence_data)

    def _set_loading_state(self, loading: bool):
        """Set loading state for UI - prevents resize events during loading."""
        self._loading_options = loading
        # Delegate to section manager
        self._section_manager.set_loading_state_for_all_sections(loading)

    def _apply_sizing_to_all_frames(self):
        """Apply sizing to all frames using size manager and section manager."""
        # Delegate sizing logic to size manager
        if not self._size_manager.is_ui_ready_for_sizing():
            QTimer.singleShot(100, self._apply_sizing_to_all_frames)
            return

        main_window_size = self._mw_size_provider()
        picker_width = self.width()

        if not self._size_manager.is_width_accurate(picker_width):
            QTimer.singleShot(200, self._apply_sizing_to_all_frames)
            return

        # Get layout config and apply sizing through section manager
        layout_config = self._option_config_service.get_layout_config()
        # CRITICAL FIX: Pass the full layout_config dict, not just spacing value
        self._section_manager.apply_sizing_to_all_sections(
            main_window_size, picker_width, layout_config
        )

    def resizeEvent(self, event):
        """Handle Qt resize events."""
        if self._loading_options:
            return

        super().resizeEvent(event)
        self._update_size()

    def _on_pictograph_selected(self, pictograph_data: PictographData):
        """Handle pictograph selection - emit Qt signal."""
        self.pictograph_selected.emit(pictograph_data)
