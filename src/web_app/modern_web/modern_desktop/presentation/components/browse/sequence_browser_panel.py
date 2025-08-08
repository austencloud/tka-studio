"""
Simplified Sequence Browser Panel - Direct PyQt Operations

Simplified sequence browser that uses PyQt directly instead of thin service wrappers.
Focuses on core functionality without unnecessary abstraction layers.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QGridLayout, QWidget

from desktop.modern.application.services.browse import (
    BrowseService,
    BrowseStateService,
    ProgressiveLoadingService,
)
from desktop.modern.application.services.browse.progressive_loading_event_handler import (
    ProgressiveLoadingEventHandler,
)
from desktop.modern.application.services.browse.sequence_display_coordinator_service import (
    SequenceDisplayCoordinatorService,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.browse_services import (
    ILayoutManager,
    ILoadingStateManager,
    INavigationHandler,
    ISequenceSorter,
    IThumbnailFactory,
)
from desktop.modern.domain.models.browse_models import FilterType
from desktop.modern.domain.models.sequence_data import SequenceData

from .browse_control_panel import BrowseControlPanel
from .modern_navigation_sidebar import ModernNavigationSidebar
from .ui_setup import SequenceBrowserUISetup


logger = logging.getLogger(__name__)


class SequenceBrowserPanel(QWidget):
    """
    Simplified sequence browser with direct PyQt operations.

    Removed thin service wrappers and uses PyQt directly for:
    - Grid layout management
    - Loading state management
    - Navigation/scrolling
    - Thumbnail display coordination
    """

    # Signals
    sequence_selected = pyqtSignal(str)  # sequence_id
    open_in_construct = pyqtSignal(str)  # sequence_id
    back_to_filters = pyqtSignal()

    def __init__(
        self,
        browse_service: BrowseService,
        state_service: BrowseStateService,
        progressive_loading_service: ProgressiveLoadingService | None = None,
        container: DIContainer | None = None,
        parent: QWidget | None = None,
    ):
        """Initialize the sequence browser panel with dependency injection."""
        super().__init__(parent)

        # Core services (keep the ones with real logic)
        self.browse_service = browse_service
        self.state_service = state_service
        self.progressive_loading_service = progressive_loading_service
        self.container = container

        # Current state
        self.current_filter_type: FilterType | None = None
        self.current_filter_values: any = None
        self.thumbnail_width = 150

        # UI components (will be set by UI setup)
        self.control_panel: BrowseControlPanel | None = None
        self.navigation_sidebar: ModernNavigationSidebar | None = None
        self.ui_setup: SequenceBrowserUISetup | None = None

        # Direct PyQt components (no service wrappers)
        self.grid_layout: QGridLayout | None = None
        self.scroll_area = None
        self.loading_widget = None
        self.browsing_widget = None
        self.loading_progress_bar = None
        self.loading_label = None

        # Injected services (will be resolved from container)
        self.thumbnail_factory: IThumbnailFactory | None = None
        self.sequence_sorter: ISequenceSorter | None = None
        self.layout_manager: ILayoutManager | None = None
        self.loading_state_manager: ILoadingStateManager | None = None
        self.navigation_handler: INavigationHandler | None = None
        self.sequence_display_coordinator: SequenceDisplayCoordinatorService | None = (
            None
        )
        self.progressive_loading_handler: ProgressiveLoadingEventHandler | None = None

        # Loading state (direct management)
        self._is_loading = False

        self._setup_ui()
        self._update_thumbnail_width()  # Calculate initial thumbnail width
        self._initialize_services()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup the UI using the UI setup class."""
        self.ui_setup = SequenceBrowserUISetup(self)
        self.ui_setup.setup_ui()

        # Get references to UI components
        self.control_panel = self.ui_setup.control_panel
        self.navigation_sidebar = self.ui_setup.navigation_sidebar

        # Get direct PyQt component references
        self.grid_layout = self.ui_setup.grid_layout
        self.scroll_area = self.ui_setup.scroll_area
        self.loading_widget = self.ui_setup.loading_widget
        self.browsing_widget = self.ui_setup.browsing_widget
        self.loading_progress_bar = self.ui_setup.loading_progress_bar
        self.loading_label = self.ui_setup.loading_label

        # Debug: Verify grid_layout assignment
        logger.info(f"🔧 [UI_SETUP] Grid layout assigned: {self.grid_layout}")
        logger.info(f"🔧 [UI_SETUP] UI setup grid layout: {self.ui_setup.grid_layout}")
        logger.info(
            f"🔧 [UI_SETUP] Grid layout same object: {self.grid_layout is self.ui_setup.grid_layout}"
        )
        logger.info(
            f"🔍 [UI_SETUP] Grid layout same object: {self.grid_layout is self.ui_setup.grid_layout}"
        )

    def _initialize_services(self) -> None:
        """Initialize all required services using hybrid DI approach."""
        try:
            # Use DI container for core business services (no UI dependencies)
            if self.container:
                from desktop.modern.application.services.browse.sequence_sorter_service import (
                    SequenceSorterService,
                )
                from desktop.modern.application.services.browse.thumbnail_factory_service import (
                    ThumbnailFactoryService,
                )

                # Register and resolve core services
                self.container.register_singleton(
                    IThumbnailFactory, ThumbnailFactoryService
                )
                self.container.register_singleton(
                    ISequenceSorter, SequenceSorterService
                )

                self.thumbnail_factory = self.container.resolve(IThumbnailFactory)
                self.sequence_sorter = self.container.resolve(ISequenceSorter)
            else:
                # Fallback to direct instantiation
                from desktop.modern.application.services.browse.sequence_sorter_service import (
                    SequenceSorterService,
                )
                from desktop.modern.application.services.browse.thumbnail_factory_service import (
                    ThumbnailFactoryService,
                )

                self.thumbnail_factory = ThumbnailFactoryService()
                self.sequence_sorter = SequenceSorterService()

            # Create UI-dependent services directly (avoiding DI complexity for UI components)
            from desktop.modern.application.services.browse.layout_manager_service import (
                LayoutManagerService,
            )
            from desktop.modern.application.services.browse.loading_state_manager_service import (
                LoadingStateManagerService,
            )
            from desktop.modern.application.services.browse.navigation_handler_service import (
                NavigationHandlerService,
            )

            self.layout_manager = LayoutManagerService(self.grid_layout)
            self.loading_state_manager = LoadingStateManagerService(
                loading_widget=self.loading_widget,
                browsing_widget=self.browsing_widget,
                loading_progress_bar=self.loading_progress_bar,
                loading_label=self.loading_label,
                layout_manager=self.layout_manager,
            )
            self.navigation_handler = NavigationHandlerService(
                scroll_area=self.scroll_area,
                grid_layout=self.grid_layout,
                navigation_sidebar=self.navigation_sidebar,
            )

            # Create coordinator services
            self.sequence_display_coordinator = SequenceDisplayCoordinatorService(
                thumbnail_factory=self.thumbnail_factory,
                layout_manager=self.layout_manager,
                loading_state_manager=self.loading_state_manager,
                sequence_sorter=self.sequence_sorter,
                navigation_handler=self.navigation_handler,
                thumbnail_width=self.thumbnail_width,  # Use calculated width, not hardcoded 150
            )

            self.progressive_loading_handler = ProgressiveLoadingEventHandler(
                loading_state_manager=self.loading_state_manager,
                sequence_display_coordinator=self.sequence_display_coordinator,
                sequence_sorter=self.sequence_sorter,
                control_panel=self.control_panel,
                navigation_sidebar=self.navigation_sidebar,
            )

            # Set callbacks
            self.sequence_display_coordinator.set_thumbnail_click_callback(
                self._on_thumbnail_clicked
            )
            self.progressive_loading_handler.set_get_sort_method_callback(
                self._get_current_sort_method
            )
            self.progressive_loading_handler.set_update_navigation_callback(
                self._update_navigation_progressively
            )

            logger.info("✅ Services initialized successfully with hybrid DI approach")

        except Exception as e:
            logger.error(f"❌ Failed to initialize services: {e}", exc_info=True)
            raise

    def _connect_signals(self) -> None:
        """Connect component signals."""
        # Control panel signals
        if self.control_panel:
            self.control_panel.back_to_filters.connect(self.back_to_filters.emit)
            self.control_panel.sort_changed.connect(self._on_sort_changed)

        # Navigation sidebar signals
        if self.navigation_sidebar:
            self.navigation_sidebar.section_selected.connect(self._on_section_selected)

        # Progressive loading signals - delegate to event handler
        if self.progressive_loading_service:
            self.progressive_loading_service.loading_started.connect(
                self.progressive_loading_handler.on_loading_started
            )
            self.progressive_loading_service.sequences_chunk_loaded.connect(
                self.progressive_loading_handler.on_sequences_chunk_loaded
            )
            self.progressive_loading_service.loading_progress.connect(
                self.progressive_loading_handler.on_loading_progress
            )
            self.progressive_loading_service.loading_completed.connect(
                self.progressive_loading_handler.on_loading_completed
            )
            self.progressive_loading_service.loading_cancelled.connect(
                self.progressive_loading_handler.on_loading_cancelled
            )

        # Loading cancel button
        if hasattr(self.ui_setup, "cancel_button"):
            self.ui_setup.cancel_button.clicked.connect(self._cancel_loading)

    # === Service-Based Methods (using proper architecture) ===

    # === Service Delegation Methods ===

    def scroll_to_section(self, section_name: str) -> None:
        """Scroll to a specific section using navigation service."""
        self.navigation_handler.scroll_to_section(section_name)

    def update_navigation_sections(
        self, section_names: list[str], sort_method: str
    ) -> None:
        """Update the navigation sidebar with new sections."""
        if self.navigation_sidebar:
            self.navigation_sidebar.update_sections(section_names, sort_method)

    # === Main Interface Methods ===

    def show_sequences_progressive(
        self,
        filter_type: FilterType,
        filter_value: any,
        chunk_size: int = 6,
    ) -> None:
        """Start progressive loading with visible layout."""
        # Store filter state
        self.current_filter_type = filter_type
        self.current_filter_values = filter_value

        # Update control panel
        if self.control_panel:
            self.control_panel.update_filter_description(filter_type, filter_value)
            self.control_panel.update_count("Loading...")

        # Clear current data
        self.progressive_loading_handler.clear_sequences()

        # Initialize progressive layout
        sort_method = self._get_current_sort_method()
        self.sequence_display_coordinator.initialize_progressive_layout(sort_method)

        # Keep browsing widget visible for progressive loading
        self.loading_state_manager.hide_loading_state()

        # Start progressive loading
        if self.progressive_loading_service:
            self.progressive_loading_service.start_progressive_loading(
                filter_type, filter_value, chunk_size
            )
        else:
            logger.warning("⚠️ No progressive loading service available")
            self.sequence_display_coordinator.show_loading_fallback()

    def show_sequences(
        self,
        sequences: list[SequenceData],
        filter_type: FilterType | None = None,
        filter_values: any | None = None,
    ) -> None:
        """Display sequences with stable layout."""
        # Update sequences in event handler
        self.progressive_loading_handler.current_sequences = sequences
        self.progressive_loading_handler.all_loaded_sequences = sequences.copy()
        self.current_filter_type = filter_type
        self.current_filter_values = filter_values

        # Update control panel
        if self.control_panel:
            self.control_panel.update_filter_description(filter_type, filter_values)
            self.control_panel.update_count(len(sequences))

        # Hide loading state
        self.loading_state_manager.hide_loading_state()

        # Display sequences using service coordinator
        sort_method = self._get_current_sort_method()
        self.sequence_display_coordinator.display_sequences_with_stable_layout(
            sequences, sort_method
        )

    def prepare_stable_layout_for_filter(
        self, filter_type: FilterType, filter_value
    ) -> None:
        """Prepare for progressive loading with immediate UI setup."""
        # Store filter state
        self.current_filter_type = filter_type
        self.current_filter_values = filter_value

        # Update control panel immediately
        if self.control_panel:
            self.control_panel.update_filter_description(filter_type, filter_value)
            self.control_panel.update_count("Loading...")

        # Clear current data and layout
        self.progressive_loading_handler.clear_sequences()
        self.layout_manager.clear_grid()

        # Ensure browsing widget is visible
        self.loading_state_manager.hide_loading_state()

        # Clear navigation sidebar
        if self.navigation_sidebar:
            self.navigation_sidebar.update_sections([], "alphabetical")

        logger.info(
            f"🎨 Prepared for progressive loading: {filter_type.value}: {filter_value}"
        )

    # === Private Implementation Methods ===

    def _get_current_sort_method(self) -> str:
        """Get the current sort method from state service."""
        return (
            self.state_service.get_sort_order()
            if self.state_service
            else "alphabetical"
        )

    def _cancel_loading(self) -> None:
        """Cancel the current loading operation."""
        if self.progressive_loading_service and self._is_loading:
            self.progressive_loading_handler.cancel_loading()
            self.progressive_loading_service.cancel_loading()

    def _on_sort_changed(self, sort_method: str) -> None:
        """Handle sort method change."""
        logger.info(f"🔄 Sort changed to: {sort_method}")
        current_sequences = self.progressive_loading_handler.get_current_sequences()
        if current_sequences:
            self.sequence_display_coordinator.display_sequences_with_stable_layout(
                current_sequences, sort_method
            )

    def _on_section_selected(self, section: str) -> None:
        """Handle navigation sidebar section selection."""
        self.scroll_to_section(section)

    def _on_thumbnail_clicked(self, sequence_id: str) -> None:
        """Handle thumbnail click."""
        logger.info(
            f"🖱️ [BROWSER_PANEL] Thumbnail clicked with sequence_id: {sequence_id}"
        )
        # Emit sequence_selected to show the sequence in the viewer panel
        self.sequence_selected.emit(sequence_id)
        # Note: open_in_construct is only emitted for explicit edit actions, not thumbnail clicks

    def _update_navigation_progressively(self) -> None:
        """Update navigation as sections are added."""
        all_loaded = self.progressive_loading_handler.get_all_loaded_sequences()
        if not self.navigation_sidebar or not all_loaded:
            return

        # Get unique sections from loaded sequences using service
        sort_method = self._get_current_sort_method()
        sections_dict = self.sequence_sorter.group_sequences_into_sections(
            all_loaded, sort_method
        )

        # Update navigation with current sections
        sections_list = list(sections_dict.keys())
        self.update_navigation_sections(sections_list, sort_method)

    def _update_thumbnail_width(self) -> None:
        """Update thumbnail width based on available space."""
        if not self.scroll_area:
            return

        # Calculate optimal width based on available space
        available_width = self.scroll_area.width()
        scrollbar_width = 20
        content_margins = 40
        grid_margins = 30

        usable_width = (
            available_width - scrollbar_width - content_margins - grid_margins
        )
        grid_spacing = 15 * 2  # 2 spaces between 3 columns
        width_per_column = (usable_width - grid_spacing) // 3

        new_width = max(150, width_per_column)

        # Only update if width changed significantly
        if abs(self.thumbnail_width - new_width) > 5:
            self.thumbnail_width = new_width

            # Update coordinator if it exists
            if (
                hasattr(self, "sequence_display_coordinator")
                and self.sequence_display_coordinator
            ):
                self.sequence_display_coordinator.update_thumbnail_width(new_width)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize event by updating thumbnail dimensions."""
        super().resizeEvent(event)
        QTimer.singleShot(100, self._update_thumbnail_width)
