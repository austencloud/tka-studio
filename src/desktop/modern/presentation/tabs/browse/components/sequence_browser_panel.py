"""
Refactored Sequence Browser Panel - Slim and Service-Oriented

Simplified sequence browser that delegates responsibilities to focused services.
This reduces the main class from 900+ lines to a focused orchestrator.
"""

import logging
from typing import List, Optional

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QApplication, QWidget

from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.tabs.browse.models import FilterType
from desktop.modern.presentation.tabs.browse.services import (
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
        """Start progressive loading with visible layout (like legacy)."""

        # Store filter state
        self.current_filter_type = filter_type
        self.current_filter_values = filter_value

        # Update control panel
        if self.control_panel:
            self.control_panel.update_filter_description(filter_type, filter_value)
            self.control_panel.update_count("Loading...")

        # Clear current data
        self.current_sequences.clear()
        self.all_loaded_sequences.clear()

        # CRITICAL: Keep browsing widget visible (like legacy) - don't show loading widget
        self.loading_state_manager.hide_loading_state()  # Ensure browsing area is visible

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

    def prepare_stable_layout_for_filter(
        self, filter_type: FilterType, filter_value
    ) -> None:
        """Prepare for progressive loading with immediate UI setup (like legacy)."""
        # Store filter state
        self.current_filter_type = filter_type
        self.current_filter_values = filter_value

        # Update control panel immediately with filter info
        if self.control_panel:
            self.control_panel.update_filter_description(filter_type, filter_value)
            self.control_panel.update_count("Loading...")

        # Clear current data and layout (like legacy clear_layout)
        self.current_sequences.clear()
        self.all_loaded_sequences.clear()
        
        # Clear the grid layout completely (like legacy)
        if self.layout_manager:
            self.layout_manager.clear_grid()
            print(f"🧹 Cleared grid layout")
        
        # CRITICAL: Ensure browsing widget is visible immediately
        if hasattr(self, 'loading_state_manager'):
            self.loading_state_manager.hide_loading_state()
            print(f"👁️ Ensured browsing widget is visible")
        
        # Clear navigation sidebar
        if self.navigation_sidebar:
            self.navigation_sidebar.update_sections([], "alphabetical")
            print(f"🧭 Cleared navigation sidebar")

        print(
            f"🎨 Prepared for progressive loading: {filter_type.value}: {filter_value}"
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
        """Handle loading started signal - keep browsing area visible."""
        # DON'T show loading state - keep browsing area visible for progressive loading
        # self.loading_state_manager.set_loading_started(total_count)
        
        # Just ensure browsing area is visible
        self.loading_state_manager.hide_loading_state()
        
        print(f"🚀 Started progressive loading: {total_count} sequences to load")

    def _on_sequences_chunk_loaded(self, chunk_sequences: List[SequenceData]) -> None:
        """Handle chunk loading with progressive layout addition (like legacy)."""
        print(f"📦 _on_sequences_chunk_loaded called with {len(chunk_sequences)} sequences")
        
        if self.loading_state_manager.is_cancelled:
            print(f"⛔ Loading cancelled, skipping chunk")
            return

        self.all_loaded_sequences.extend(chunk_sequences)
        chunk_size = len(chunk_sequences)
        total_loaded = len(self.all_loaded_sequences)
        
        print(f"📈 Progress: {total_loaded} total sequences loaded so far")

        # Update progress
        self.loading_state_manager.update_progress(
            total_loaded, total_loaded, f"Loaded {total_loaded} sequences..."
        )

        if self.control_panel:
            self.control_panel.update_count(total_loaded)
            print(f"📋 Updated count to {total_loaded}")

        # PROGRESSIVE ADDITION: Add new sequences to layout one by one (like legacy)
        sort_method = self._get_current_sort_method()
        print(f"🔄 About to add sequences to layout with sort method: {sort_method}")
        
        self._add_sequences_progressively_to_layout(chunk_sequences, sort_method)
        
        # Update navigation as we add sections
        self._update_navigation_progressively()
        
        # Process events to keep UI responsive (like legacy)
        QApplication.processEvents()
        print(f"✅ Completed processing chunk of {chunk_size} sequences")

    def _on_loading_progress(self, current: int, total: int) -> None:
        """Handle loading progress update."""
        self.loading_state_manager.update_progress(current, total)

    def _on_loading_completed(self, final_sequences: List[SequenceData]) -> None:
        """Handle loading completion."""
        if self.loading_state_manager.is_cancelled:
            return

        self.current_sequences = final_sequences
        self.loading_state_manager.set_loading_completed(len(final_sequences))

        # Update final count and navigation
        if self.control_panel:
            self.control_panel.update_count(len(final_sequences))

        # Final navigation update
        self._update_navigation_progressively()

        print(
            f"✅ Progressive loading completed: {len(final_sequences)} sequences loaded"
        )

    def _on_loading_cancelled(self) -> None:
        """Handle loading cancellation."""
        self.loading_state_manager.set_loading_cancelled()

        if self.all_loaded_sequences:
            self.current_sequences = self.all_loaded_sequences
            # Update count and navigation with what we have
            if self.control_panel:
                self.control_panel.update_count(len(self.all_loaded_sequences))
            self._update_navigation_progressively()
            print(
                f"⚠️ Loading cancelled: {len(self.all_loaded_sequences)} sequences partially loaded"
            )
        else:
            # Show empty state
            if self.control_panel:
                self.control_panel.update_count(0)
            print(f"❌ Loading cancelled: No sequences loaded")

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

    def _add_sequences_progressively_to_layout(
        self, chunk_sequences: List[SequenceData], sort_method: str
    ) -> None:
        """Add sequences to layout progressively, one by one (like legacy)."""
        if not chunk_sequences or not self.layout_manager:
            return

        # Group sequences by section (like legacy grouping)
        sections_to_add = self._group_sequences_by_section(chunk_sequences, sort_method)

        # Get current layout state
        current_row = self.layout_manager.get_row_count()

        # Add each section progressively
        for section_name, section_sequences in sections_to_add.items():
            # Check if we need to add a section header
            if self._should_add_section_header(section_name):
                current_row = self.layout_manager.add_section_header(
                    section_name, current_row
                )
                current_row += 1

            # Add thumbnails for this section one by one
            column_index = self._get_current_column_for_row(current_row)

            for sequence in section_sequences:
                # Create thumbnail (like legacy add_thumbnail_box)
                thumbnail = self.thumbnail_factory.create_thumbnail(
                    sequence, self.thumbnail_width, sort_method
                )

                # Make clickable
                if self.display_coordinator and hasattr(
                    self.display_coordinator, "thumbnail_click_callback"
                ):
                    thumbnail.mousePressEvent = (
                        lambda event, seq_id=sequence.id: self._on_thumbnail_clicked(
                            seq_id
                        )
                    )

                # Add to grid layout (like legacy)
                self.layout_manager.add_thumbnail_to_grid(
                    thumbnail, current_row, column_index
                )

                # Show immediately (like legacy)
                thumbnail.show()

                # Move to next position
                column_index = (column_index + 1) % 3  # 3 columns
                if column_index == 0:
                    current_row += 1

                # Process events to keep UI responsive (critical for legacy-like behavior)
                QApplication.processEvents()

        print(f"🔄 Added {len(chunk_sequences)} sequences progressively to layout")

    def _group_sequences_by_section(
        self, sequences: List[SequenceData], sort_method: str
    ) -> dict:
        """Group sequences by section (like legacy)."""
        sections = {}

        for sequence in sequences:
            section_name = self._get_section_name_for_sequence(sequence, sort_method)
            if section_name not in sections:
                sections[section_name] = []
            sections[section_name].append(sequence)

        return sections

    def _get_section_name_for_sequence(
        self, sequence: SequenceData, sort_method: str
    ) -> str:
        """Get section name for a sequence based on sort method."""
        if sort_method == "alphabetical":
            return sequence.word[0].upper() if sequence.word else "#"
        elif sort_method == "length":
            if sequence.sequence_length <= 3:
                return "Short (1-3)"
            elif sequence.sequence_length <= 6:
                return "Medium (4-6)"
            else:
                return "Long (7+)"
        elif sort_method == "level":
            return f"Level {sequence.level if sequence.level else 'Unknown'}"
        elif sort_method == "date_added":
            return sequence.date_added if sequence.date_added else "Unknown"
        else:
            return "Other"

    def _should_add_section_header(self, section_name: str) -> bool:
        """Check if we should add a section header."""
        # For now, always add headers (could be optimized to check if section already exists)
        return True

    def _get_current_column_for_row(self, row: int) -> int:
        """Get the current column index for a row (based on existing items)."""
        # For simplicity, start at column 0 for new rows
        # Could be enhanced to check existing items in the row
        return 0

    def _update_navigation_progressively(self) -> None:
        """Update navigation as sections are added."""
        if not self.navigation_sidebar or not self.all_loaded_sequences:
            return

        # Get unique sections from loaded sequences
        sort_method = self._get_current_sort_method()
        sections = set()

        for sequence in self.all_loaded_sequences:
            section_name = self._get_section_name_for_sequence(sequence, sort_method)
            sections.add(section_name)

        # Update navigation with current sections
        sections_list = sorted(list(sections))
        self.navigation_sidebar.update_sections(sections_list, sort_method)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize event by updating thumbnail dimensions."""
        super().resizeEvent(event)
        QTimer.singleShot(100, self._update_thumbnail_width)
