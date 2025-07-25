"""
Refactored Sequence Browser Panel - Slim and Service-Oriented

Simplified sequence browser that delegates responsibilities to focused services.
This reduces the main class from 900+ lines to a focused orchestrator.
"""

from typing import List, Optional

from domain.models.sequence_data import SequenceData
from presentation.tabs.browse.models import FilterType
from presentation.tabs.browse.services import (
    BrowseService,
    BrowseStateService,
    LayoutManagerService,
    LoadingStateManagerService,
    NavigationHandlerService,
    ProgressiveLoadingService,
    SequenceDisplayCoordinatorService,
    SequenceSorterService,
    ThumbnailFactoryService,
)
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QWidget

from .modern_browse_control_panel import ModernBrowseControlPanel
from .modern_navigation_sidebar import ModernNavigationSidebar
from .ui_setup import SequenceBrowserUISetup


class SequenceBrowserPanel(QWidget):
    """
    Refactored sequence browser with service-oriented architecture.

    This class now focuses on:
    - UI setup and component coordination
    - Signal handling and event routing
    - Service orchestration
    - Progressive loading coordination

    All heavy lifting is delegated to specialized services.
    """

    # Signals
    sequence_selected = pyqtSignal(str)  # sequence_id
    open_in_construct = pyqtSignal(str)  # sequence_id
    back_to_filters = pyqtSignal()

    def __init__(
        self,
        browse_service: BrowseService,
        state_service: BrowseStateService,
        progressive_loading_service: Optional[ProgressiveLoadingService] = None,
        parent: Optional[QWidget] = None,
    ):
        """Initialize the sequence browser panel with service dependencies."""
        super().__init__(parent)

        # Core services
        self.browse_service = browse_service
        self.state_service = state_service
        self.progressive_loading_service = progressive_loading_service

        # Current state
        self.current_sequences: List[SequenceData] = []
        self.all_loaded_sequences: List[SequenceData] = []
        self.current_filter_type: Optional[FilterType] = None
        self.current_filter_values: any = None
        self.thumbnail_width = 150

        # UI components (will be set by UI setup)
        self.control_panel: Optional[ModernBrowseControlPanel] = None
        self.navigation_sidebar: Optional[ModernNavigationSidebar] = None
        self.ui_setup: Optional[SequenceBrowserUISetup] = None

        # Specialized services (will be initialized after UI setup)
        self.thumbnail_factory: Optional[ThumbnailFactoryService] = None
        self.layout_manager: Optional[LayoutManagerService] = None
        self.loading_state_manager: Optional[LoadingStateManagerService] = None
        self.sequence_sorter: Optional[SequenceSorterService] = None
        self.navigation_handler: Optional[NavigationHandlerService] = None
        self.display_coordinator: Optional[SequenceDisplayCoordinatorService] = None

        self._setup_ui()
        self._initialize_services()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup the UI using the UI setup class."""
        self.ui_setup = SequenceBrowserUISetup(self)
        self.ui_setup.setup_ui()

        # Get references to UI components
        self.control_panel = self.ui_setup.control_panel
        self.navigation_sidebar = self.ui_setup.navigation_sidebar

    def _initialize_services(self) -> None:
        """Initialize all the specialized services."""
        # Get UI components from setup
        grid_layout = self.ui_setup.grid_layout
        scroll_area = self.ui_setup.scroll_area
        loading_widget = self.ui_setup.loading_widget
        browsing_widget = self.ui_setup.browsing_widget
        loading_progress_bar = self.ui_setup.loading_progress_bar
        loading_label = self.ui_setup.loading_label

        # Initialize services
        self.thumbnail_factory = ThumbnailFactoryService()
        self.layout_manager = LayoutManagerService(grid_layout)
        self.loading_state_manager = LoadingStateManagerService(
            loading_widget,
            browsing_widget,
            loading_progress_bar,
            loading_label,
            self.layout_manager,
        )
        self.sequence_sorter = SequenceSorterService()
        self.navigation_handler = NavigationHandlerService(
            scroll_area, grid_layout, self.navigation_sidebar
        )

        # Initialize display coordinator
        self.display_coordinator = SequenceDisplayCoordinatorService(
            self.thumbnail_factory,
            self.layout_manager,
            self.loading_state_manager,
            self.sequence_sorter,
            self.navigation_handler,
            self.thumbnail_width,
        )

        # Set up thumbnail click callback
        self.display_coordinator.set_thumbnail_click_callback(
            self._on_thumbnail_clicked
        )

    def _connect_signals(self) -> None:
        """Connect component signals."""
        # Control panel signals
        if self.control_panel:
            self.control_panel.back_to_filters.connect(self.back_to_filters.emit)
            self.control_panel.sort_changed.connect(self._on_sort_changed)

        # Navigation sidebar signals
        if self.navigation_sidebar:
            self.navigation_sidebar.section_selected.connect(self._on_section_selected)

        # Progressive loading signals
        if self.progressive_loading_service:
            self.progressive_loading_service.loading_started.connect(
                self._on_loading_started
            )
            self.progressive_loading_service.sequences_chunk_loaded.connect(
                self._on_sequences_chunk_loaded
            )
            self.progressive_loading_service.loading_progress.connect(
                self._on_loading_progress
            )
            self.progressive_loading_service.loading_completed.connect(
                self._on_loading_completed
            )
            self.progressive_loading_service.loading_cancelled.connect(
                self._on_loading_cancelled
            )

        # Loading state manager cancel button
        if hasattr(self.ui_setup, "cancel_button"):
            self.ui_setup.cancel_button.clicked.connect(self._cancel_loading)

    def show_sequences_progressive(
        self,
        filter_type: FilterType,
        filter_value: any,
        chunk_size: int = 6,
    ) -> None:
        """Start progressive loading with stable layout."""

        # Store filter state
        self.current_filter_type = filter_type
        self.current_filter_values = filter_value

        # Update control panel
        if self.control_panel:
            self.control_panel.update_filter_description(filter_type, filter_value)
            self.control_panel.update_count(0)

        # Clear current data
        self.current_sequences.clear()
        self.all_loaded_sequences.clear()

        # Show loading state
        self.loading_state_manager.show_loading_state()

        # Start progressive loading
        if self.progressive_loading_service:
            self.progressive_loading_service.start_progressive_loading(
                filter_type, filter_value, chunk_size
            )
        else:
            print("⚠️ No progressive loading service available")
            self.display_coordinator.show_loading_fallback()

    def show_sequences(
        self,
        sequences: List[SequenceData],
        filter_type: Optional[FilterType] = None,
        filter_values: any = None,
    ) -> None:
        """Display sequences with stable layout (legacy compatibility)."""

        self.current_sequences = sequences
        self.all_loaded_sequences = sequences.copy()
        self.current_filter_type = filter_type
        self.current_filter_values = filter_values

        # Update control panel
        if self.control_panel:
            self.control_panel.update_filter_description(filter_type, filter_values)
            self.control_panel.update_count(len(sequences))

        # Hide loading state
        self.loading_state_manager.hide_loading_state()

        # Get current sort method and display
        sort_method = self._get_current_sort_method()
        self.display_coordinator.display_sequences_with_stable_layout(
            sequences, sort_method
        )

    def _get_current_sort_method(self) -> str:
        """Get the current sort method from state service."""
        return (
            self.state_service.get_sort_order()
            if self.state_service
            else "alphabetical"
        )

    def _cancel_loading(self) -> None:
        """Cancel the current loading operation."""
        if self.progressive_loading_service and self.loading_state_manager.is_loading:
            self.loading_state_manager.cancel_loading()
            self.progressive_loading_service.cancel_loading()

    def _on_loading_started(self, total_count: int) -> None:
        """Handle loading started signal."""
        self.loading_state_manager.set_loading_started(total_count)

    def _on_sequences_chunk_loaded(self, chunk_sequences: List[SequenceData]) -> None:
        """Handle chunk loading."""
        if self.loading_state_manager.is_cancelled:
            return

        self.all_loaded_sequences.extend(chunk_sequences)
        chunk_size = len(chunk_sequences)
        total_loaded = len(self.all_loaded_sequences)

        # Update progress
        self.loading_state_manager.update_progress(
            total_loaded, total_loaded, f"Loaded {total_loaded} sequences..."
        )

        if self.control_panel:
            self.control_panel.update_count(total_loaded)

        # For first chunk, initialize layout
        if total_loaded == chunk_size:
            self.loading_state_manager.hide_loading_state()
            sort_method = self._get_current_sort_method()
            self.display_coordinator.initialize_progressive_layout(sort_method)

        # Add sequences progressively
        sort_method = self._get_current_sort_method()
        self.display_coordinator.add_sequences_progressively(
            chunk_sequences, sort_method
        )

    def _on_loading_progress(self, current: int, total: int) -> None:
        """Handle loading progress update."""
        self.loading_state_manager.update_progress(current, total)

    def _on_loading_completed(self, final_sequences: List[SequenceData]) -> None:
        """Handle loading completion."""
        if self.loading_state_manager.is_cancelled:
            return

        self.current_sequences = final_sequences
        self.loading_state_manager.set_loading_completed(len(final_sequences))

        # Finalize layout with proper sections
        sort_method = self._get_current_sort_method()
        self.display_coordinator.finalize_progressive_layout(
            final_sequences, sort_method
        )

    def _on_loading_cancelled(self) -> None:
        """Handle loading cancellation."""
        self.loading_state_manager.set_loading_cancelled()

        if self.all_loaded_sequences:
            self.current_sequences = self.all_loaded_sequences
            sort_method = self._get_current_sort_method()
            self.display_coordinator.finalize_progressive_layout(
                self.current_sequences, sort_method
            )
        else:
            self.display_coordinator.show_empty_state()

    def _on_sort_changed(self, sort_method: str) -> None:
        """Handle sort method change."""
        print(f"🔄 Sort changed to: {sort_method}")

        if self.current_sequences:
            self.display_coordinator.display_sequences_with_stable_layout(
                self.current_sequences, sort_method
            )

    def _on_section_selected(self, section: str) -> None:
        """Handle navigation sidebar section selection."""
        self.navigation_handler.scroll_to_section(section)

    def _on_thumbnail_clicked(self, sequence_id: str) -> None:
        """Handle thumbnail click."""
        self.sequence_selected.emit(sequence_id)
        self.open_in_construct.emit(sequence_id)

    def _update_thumbnail_width(self) -> None:
        """Update thumbnail width based on available space."""
        # Calculate optimal width based on available space
        available_width = self.ui_setup.scroll_area.width()
        scrollbar_width = 20
        content_margins = 40
        grid_margins = 30

        usable_width = (
            available_width - scrollbar_width - content_margins - grid_margins
        )
        grid_spacing = 15 * 2  # 2 spaces between 3 columns
        width_per_column = (usable_width - grid_spacing) // 3

        new_width = max(150, width_per_column)
        self.thumbnail_width = new_width

        if self.display_coordinator:
            self.display_coordinator.update_thumbnail_width(new_width)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize event by updating thumbnail dimensions."""
        super().resizeEvent(event)
        QTimer.singleShot(100, self._update_thumbnail_width)
