"""
Simplified Sequence Browser Panel - Direct PyQt Operations

Simplified sequence browser that uses PyQt directly instead of thin service wrappers.
Focuses on core functionality without unnecessary abstraction layers.
"""

import logging
from typing import List, Optional

from PyQt6.QtCore import QPoint, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QResizeEvent
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
)

from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.tabs.browse.models import FilterType
from desktop.modern.presentation.tabs.browse.services import (
    BrowseService,
    BrowseStateService,
    ProgressiveLoadingService,
    SequenceSorterService,
    ThumbnailFactoryService,
)

from .modern_browse_control_panel import ModernBrowseControlPanel
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
        progressive_loading_service: Optional[ProgressiveLoadingService] = None,
        parent: Optional[QWidget] = None,
    ):
        """Initialize the sequence browser panel with core services only."""
        super().__init__(parent)

        # Core services (keep the ones with real logic)
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

        # Direct PyQt components (no service wrappers)
        self.grid_layout: Optional[QGridLayout] = None
        self.scroll_area = None
        self.loading_widget = None
        self.browsing_widget = None
        self.loading_progress_bar = None
        self.loading_label = None

        # Keep only services with real business logic
        self.thumbnail_factory: Optional[ThumbnailFactoryService] = None
        self.sequence_sorter: Optional[SequenceSorterService] = None

        # Loading state (direct management)
        self._is_loading = False
        self._loading_cancelled = False

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
        """Initialize only the services with real business logic."""
        # Keep services that provide real value
        self.thumbnail_factory = ThumbnailFactoryService()
        self.sequence_sorter = SequenceSorterService()

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

        # Loading cancel button
        if hasattr(self.ui_setup, "cancel_button"):
            self.ui_setup.cancel_button.clicked.connect(self._cancel_loading)

    # === Direct PyQt Grid Layout Methods (replacing LayoutManagerService) ===

    def _ensure_grid_layout_valid(self) -> bool:
        """Ensure grid layout is valid and recreate if necessary."""
        if self.grid_layout is None or not bool(self.grid_layout):
            logger.warning(
                "⚠️ [GRID_LAYOUT] Invalid grid layout, attempting to recreate"
            )
            if self.ui_setup and self.ui_setup.grid_widget:
                from PyQt6.QtWidgets import QGridLayout

                self.grid_layout = QGridLayout(self.ui_setup.grid_widget)
                self.grid_layout.setSpacing(15)
                for col in range(3):
                    self.grid_layout.setColumnStretch(col, 1)
                self.ui_setup.grid_layout = self.grid_layout
                logger.info(
                    f"🔧 [GRID_LAYOUT] Recreated grid layout: {self.grid_layout}"
                )
                return True
            else:
                logger.error("❌ [GRID_LAYOUT] Cannot recreate grid layout")
                return False
        return True

    def clear_grid(self) -> None:
        """Clear all items from the grid layout."""
        if not self._ensure_grid_layout_valid():
            logger.warning(
                "⚠️ [CLEAR_GRID] Cannot ensure valid grid layout, skipping clear"
            )
            return

        item_count = self.grid_layout.count()
        logger.info(f"🔍 [CLEAR_GRID] Clearing {item_count} items from grid")
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def add_section_header(self, section_name: str, current_row: int) -> int:
        """Add a section header to the grid."""
        if not self._ensure_grid_layout_valid():
            logger.warning(
                "⚠️ [ADD_SECTION_HEADER] Grid layout invalid, skipping header"
            )
            return current_row

        header_widget = QFrame()
        header_widget.setStyleSheet(
            """
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                margin: 10px 0px;
            }
        """
        )

        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(15, 8, 15, 8)

        title_label = QLabel(section_name)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.9); background: transparent; border: none;"
        )
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        if current_row > 0:
            current_row += 1
        self.grid_layout.addWidget(header_widget, current_row, 0, 1, 3)

        return current_row

    def add_thumbnail_to_grid(self, thumbnail: QWidget, row: int, col: int) -> None:
        """Add a thumbnail widget to the grid at specified position."""
        if not self._ensure_grid_layout_valid():
            logger.warning("⚠️ [ADD_THUMBNAIL] Grid layout invalid, skipping thumbnail")
            return
        self.grid_layout.addWidget(thumbnail, row, col)

    def add_empty_state(self) -> None:
        """Add empty state message to the grid."""
        if not self.grid_layout:
            return

        empty_label = QLabel("No sequences found")
        empty_label.setFont(QFont("Segoe UI", 14))
        empty_label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_layout.addWidget(empty_label, 0, 0, 1, 3)

    def add_loading_fallback(self) -> None:
        """Add loading fallback message to the grid."""
        if not self.grid_layout:
            return

        loading_label = QLabel("Loading sequences...")
        loading_label.setFont(QFont("Segoe UI", 14))
        loading_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_layout.addWidget(loading_label, 0, 0, 1, 3)

    # === Direct Loading State Methods (replacing LoadingStateManagerService) ===

    def show_loading_state(self) -> None:
        """Show loading UI and hide main content."""
        self._is_loading = True
        self._loading_cancelled = False

        if self.loading_widget:
            self.loading_widget.show()
        if self.browsing_widget:
            self.browsing_widget.hide()

        # Reset progress
        if self.loading_progress_bar:
            self.loading_progress_bar.setValue(0)
            self.loading_progress_bar.setMaximum(100)

        if self.loading_label:
            self.loading_label.setText("Preparing to load sequences...")

    def hide_loading_state(self) -> None:
        """Hide loading UI and show main content."""
        self._is_loading = False

        if self.loading_widget:
            self.loading_widget.hide()
        if self.browsing_widget:
            self.browsing_widget.show()

    def update_loading_progress(
        self, current: int, total: int, message: str = ""
    ) -> None:
        """Update loading progress."""
        if self._loading_cancelled:
            return

        if self.loading_progress_bar:
            self.loading_progress_bar.setMaximum(total)
            self.loading_progress_bar.setValue(current)

        if self.loading_label and message:
            self.loading_label.setText(message)

    # === Direct Navigation Methods (replacing NavigationHandlerService) ===

    def scroll_to_section(self, section_name: str) -> None:
        """Scroll to a specific section in the grid."""
        if not self.scroll_area or not self.grid_layout:
            return

        logger.info(f"🧭 Navigating to section: {section_name}")

        # Find the section header widget
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()

                # Check if this widget contains a label with the section name
                if (
                    hasattr(widget, "findChild")
                    and widget.findChild(QLabel)
                    and widget.findChild(QLabel).text() == section_name
                ):
                    # Calculate scroll position
                    header_global_pos = widget.mapToGlobal(QPoint(0, 0))
                    content_widget_pos = self.scroll_area.widget().mapFromGlobal(
                        header_global_pos
                    )
                    vertical_pos = content_widget_pos.y()

                    # Scroll to the section
                    self.scroll_area.verticalScrollBar().setValue(vertical_pos)
                    return

        # If section not found, scroll to top
        self.scroll_area.verticalScrollBar().setValue(0)

    def update_navigation_sections(
        self, section_names: List[str], sort_method: str
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
        self.current_sequences.clear()
        self.all_loaded_sequences.clear()

        # Keep browsing widget visible for progressive loading
        self.hide_loading_state()

        # Start progressive loading
        if self.progressive_loading_service:
            self.progressive_loading_service.start_progressive_loading(
                filter_type, filter_value, chunk_size
            )
        else:
            logger.warning("⚠️ No progressive loading service available")
            self.add_loading_fallback()

    def show_sequences(
        self,
        sequences: List[SequenceData],
        filter_type: Optional[FilterType] = None,
        filter_values: any = None,
    ) -> None:
        """Display sequences with stable layout."""
        self.current_sequences = sequences
        self.all_loaded_sequences = sequences.copy()
        self.current_filter_type = filter_type
        self.current_filter_values = filter_values

        # Update control panel
        if self.control_panel:
            self.control_panel.update_filter_description(filter_type, filter_values)
            self.control_panel.update_count(len(sequences))

        # Hide loading state
        self.hide_loading_state()

        # Display sequences
        sort_method = self._get_current_sort_method()
        self._display_sequences_with_stable_layout(sequences, sort_method)

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
        self.current_sequences.clear()
        self.all_loaded_sequences.clear()
        self.clear_grid()

        # Ensure browsing widget is visible
        self.hide_loading_state()

        # Clear navigation sidebar
        if self.navigation_sidebar:
            self.navigation_sidebar.update_sections([], "alphabetical")

        logger.info(
            f"🎨 Prepared for progressive loading: {filter_type.value}: {filter_value}"
        )

    # === Private Implementation Methods ===

    def _display_sequences_with_stable_layout(
        self, sequences: List[SequenceData], sort_method: str
    ) -> None:
        """Display sequences using stable layout with sections."""
        if not sequences:
            self.add_empty_state()
            return

        # Sort sequences
        sorted_sequences = self.sequence_sorter.sort_sequences(sequences, sort_method)

        # Group into sections
        sections = self.sequence_sorter.group_sequences_into_sections(
            sorted_sequences, sort_method
        )

        # Update navigation sidebar
        section_names = list(sections.keys())
        self.update_navigation_sections(section_names, sort_method)

        # Clear and rebuild with stable layout
        self.clear_grid()

        current_row = 0
        thumbnail_count = 0

        for section_name, section_sequences in sections.items():
            # Add section header
            current_row = self.add_section_header(section_name, current_row)
            current_row += 1

            # Create thumbnails for this section
            for sequence in section_sequences:
                thumbnail = self.thumbnail_factory.create_thumbnail(
                    sequence, self.thumbnail_width, sort_method
                )

                # Make clickable
                thumbnail.mousePressEvent = (
                    lambda event, seq_id=sequence.id: self._on_thumbnail_clicked(seq_id)
                )

                # Calculate position in 3-column grid
                col = thumbnail_count % 3
                if col == 0 and thumbnail_count > 0:
                    current_row += 1

                self.add_thumbnail_to_grid(thumbnail, current_row, col)
                thumbnail_count += 1

            # Start fresh row for next section
            if thumbnail_count % 3 != 0:
                current_row += 1
                thumbnail_count = ((thumbnail_count // 3) + 1) * 3

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
            self._loading_cancelled = True
            self.progressive_loading_service.cancel_loading()

    def _on_loading_started(self, total_count: int) -> None:
        """Handle loading started signal - keep browsing area visible."""
        # Keep browsing area visible for progressive loading
        self.hide_loading_state()
        logger.info(f"🚀 Started progressive loading: {total_count} sequences to load")

    def _on_sequences_chunk_loaded(self, chunk_sequences: List[SequenceData]) -> None:
        """Handle chunk loading with progressive layout addition."""
        logger.info(f"📦 Processing chunk of {len(chunk_sequences)} sequences")

        if self._loading_cancelled:
            logger.info("⛔ Loading cancelled, skipping chunk")
            return

        self.all_loaded_sequences.extend(chunk_sequences)
        total_loaded = len(self.all_loaded_sequences)

        # Update progress
        self.update_loading_progress(
            total_loaded, total_loaded, f"Loaded {total_loaded} sequences..."
        )

        if self.control_panel:
            self.control_panel.update_count(total_loaded)

        # Add sequences progressively to layout
        sort_method = self._get_current_sort_method()
        self._add_sequences_progressively_to_layout(chunk_sequences, sort_method)

        # Update navigation as we add sections
        self._update_navigation_progressively()

        # Process events to keep UI responsive
        QApplication.processEvents()

    def _on_loading_progress(self, current: int, total: int) -> None:
        """Handle loading progress update."""
        self.update_loading_progress(current, total)

    def _on_loading_completed(self, final_sequences: List[SequenceData]) -> None:
        """Handle loading completion."""
        if self._loading_cancelled:
            return

        self.current_sequences = final_sequences

        # Update final count and navigation
        if self.control_panel:
            self.control_panel.update_count(len(final_sequences))

        self._update_navigation_progressively()
        logger.info(
            f"✅ Progressive loading completed: {len(final_sequences)} sequences loaded"
        )

    def _on_loading_cancelled(self) -> None:
        """Handle loading cancellation."""
        self._loading_cancelled = True

        if self.all_loaded_sequences:
            self.current_sequences = self.all_loaded_sequences
            if self.control_panel:
                self.control_panel.update_count(len(self.all_loaded_sequences))
            self._update_navigation_progressively()
            logger.info(
                f"⚠️ Loading cancelled: {len(self.all_loaded_sequences)} sequences partially loaded"
            )
        else:
            if self.control_panel:
                self.control_panel.update_count(0)
            logger.info("❌ Loading cancelled: No sequences loaded")

    def _on_sort_changed(self, sort_method: str) -> None:
        """Handle sort method change."""
        logger.info(f"🔄 Sort changed to: {sort_method}")
        if self.current_sequences:
            self._display_sequences_with_stable_layout(
                self.current_sequences, sort_method
            )

    def _on_section_selected(self, section: str) -> None:
        """Handle navigation sidebar section selection."""
        self.scroll_to_section(section)

    def _on_thumbnail_clicked(self, sequence_id: str) -> None:
        """Handle thumbnail click."""
        self.sequence_selected.emit(sequence_id)
        self.open_in_construct.emit(sequence_id)

    def _add_sequences_progressively_to_layout(
        self, chunk_sequences: List[SequenceData], sort_method: str
    ) -> None:
        """Add sequences to layout progressively."""
        if not chunk_sequences or not self.grid_layout:
            return

        # Group sequences by section
        sections_to_add = self._group_sequences_by_section(chunk_sequences, sort_method)

        # Get current layout state
        current_row = self.grid_layout.rowCount()

        # Add each section progressively
        for section_name, section_sequences in sections_to_add.items():
            # Add section header
            current_row = self.add_section_header(section_name, current_row)
            current_row += 1

            # Add thumbnails for this section
            column_index = 0

            for sequence in section_sequences:
                # Create thumbnail
                thumbnail = self.thumbnail_factory.create_thumbnail(
                    sequence, self.thumbnail_width, sort_method
                )

                # Make clickable
                thumbnail.mousePressEvent = (
                    lambda event, seq_id=sequence.id: self._on_thumbnail_clicked(seq_id)
                )

                # Add to grid layout
                self.add_thumbnail_to_grid(thumbnail, current_row, column_index)

                # Show immediately
                thumbnail.show()

                # Move to next position
                column_index = (column_index + 1) % 3  # 3 columns
                if column_index == 0:
                    current_row += 1

                # Process events to keep UI responsive
                QApplication.processEvents()

    def _group_sequences_by_section(
        self, sequences: List[SequenceData], sort_method: str
    ) -> dict:
        """Group sequences by section."""
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
        self.thumbnail_width = new_width

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize event by updating thumbnail dimensions."""
        super().resizeEvent(event)
        QTimer.singleShot(100, self._update_thumbnail_width)
