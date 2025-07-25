"""
Sequence Browser Panel - With Stable Layout and Fixed Length Sorting

Enhanced with comprehensive layout stability system that eliminates all
layout shifts during progressive loading.
"""

from datetime import datetime
from typing import List, Optional

from domain.models.sequence_data import SequenceData
from presentation.tabs.browse.models import FilterType
from presentation.tabs.browse.services.browse_service import BrowseService
from presentation.tabs.browse.services.browse_state_service import BrowseStateService
from presentation.tabs.browse.services.progressive_loading_service import (
    ProgressiveLoadingService,
)
from PyQt6.QtCore import QPoint, QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QPixmap, QResizeEvent
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .modern_browse_control_panel import ModernBrowseControlPanel
from .modern_navigation_sidebar import ModernNavigationSidebar


class SequenceBrowserPanel(QWidget):
    """
    Sequence browser with thumbnail grid and ZERO layout shifts.

    Features:
    - Progressive loading with stable layout
    - Fixed-size thumbnails that never resize
    - Row-by-row display (complete rows only)
    - Length-aware thumbnail sizing
    - Comprehensive layout shift elimination
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
        """Initialize the sequence browser panel with stable layout."""
        super().__init__(parent)

        self.browse_service = browse_service
        self.state_service = state_service
        self.progressive_loading_service = progressive_loading_service

        # Loading state
        self._is_progressive_loading = False
        self._loading_cancelled = False

        # Sequence data
        self.current_sequences: List[SequenceData] = []
        self.all_loaded_sequences: List[SequenceData] = []

        # Layout system
        self.thumbnail_width = 150
        self.row_loader = None

        # Navigation sidebar
        self.navigation_sidebar: Optional[ModernNavigationSidebar] = None

        # Control panel
        self.control_panel: Optional[ModernBrowseControlPanel] = None

        # Loading UI components
        self.loading_widget: Optional[QWidget] = None
        self.loading_progress_bar: Optional[QProgressBar] = None
        self.loading_label: Optional[QLabel] = None
        self.cancel_button: Optional[QPushButton] = None

        # Current filter state
        self.current_filter_type: Optional[FilterType] = None
        self.current_filter_values: any = None

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup the browser UI with stable layout components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Control panel
        self.control_panel = ModernBrowseControlPanel(self.state_service)
        layout.addWidget(self.control_panel)

        # Main content area
        content_panel = QFrame()
        content_panel.setStyleSheet(
            """
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }
        """
        )
        content_layout = QVBoxLayout(content_panel)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # Loading widget (initially hidden)
        self._setup_loading_widget()
        content_layout.addWidget(self.loading_widget)
        self.loading_widget.hide()

        # Main browsing area: sidebar + grid
        self.browsing_layout = QHBoxLayout()
        self.browsing_layout.setSpacing(15)

        # Navigation sidebar
        self.navigation_sidebar = ModernNavigationSidebar()
        self.navigation_sidebar.set_minimum_width(150)
        self.navigation_sidebar.setMaximumWidth(250)
        self.browsing_layout.addWidget(self.navigation_sidebar, 0)

        # Thumbnail grid scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 6px;
            }
        """
        )
        self.browsing_layout.addWidget(self.scroll_area, 1)

        # Grid widget with fixed layout
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(15)

        # Set column stretch factors for 3 equal columns
        for col in range(3):
            self.grid_layout.setColumnStretch(col, 1)

        self.scroll_area.setWidget(self.grid_widget)

        # Browsing widget container
        self.browsing_widget = QWidget()
        self.browsing_widget.setLayout(self.browsing_layout)
        content_layout.addWidget(self.browsing_widget)

        layout.addWidget(content_panel)

    def _setup_loading_widget(self) -> None:
        """Setup loading UI components."""
        self.loading_widget = QFrame()
        self.loading_widget.setStyleSheet(
            """
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 20px;
            }
        """
        )

        loading_layout = QVBoxLayout(self.loading_widget)
        loading_layout.setSpacing(15)
        loading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Loading title
        title_label = QLabel("Loading Sequences...")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(
            "color: white; background: transparent; border: none;"
        )
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_layout.addWidget(title_label)

        # Progress bar
        self.loading_progress_bar = QProgressBar()
        self.loading_progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                background: rgba(0, 0, 0, 0.3);
                text-align: center;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4A90E2, stop:1 #7BB3F0);
                border-radius: 6px;
            }
        """
        )
        self.loading_progress_bar.setMinimumHeight(30)
        loading_layout.addWidget(self.loading_progress_bar)

        # Status label
        self.loading_label = QLabel("Preparing to load sequences...")
        self.loading_label.setFont(QFont("Segoe UI", 12))
        self.loading_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.8); background: transparent; border: none;"
        )
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_layout.addWidget(self.loading_label)

        # Cancel button
        self.cancel_button = QPushButton("Cancel Loading")
        self.cancel_button.setStyleSheet(
            """
            QPushButton {
                background: rgba(255, 100, 100, 0.8);
                border: 1px solid rgba(255, 100, 100, 1.0);
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 100, 100, 1.0);
            }
            QPushButton:pressed {
                background: rgba(200, 80, 80, 1.0);
            }
        """
        )
        self.cancel_button.clicked.connect(self._cancel_loading)
        loading_layout.addWidget(self.cancel_button)

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

    def show_sequences_progressive(
        self,
        filter_type: FilterType,
        filter_value: any,
        chunk_size: int = 6,  # Use multiple of 3 for complete rows
    ) -> None:
        """
        Start progressive loading with stable layout.

        Args:
            filter_type: The filter type to apply
            filter_value: The filter value
            chunk_size: Number of sequences per chunk (multiple of 3 recommended)
        """
        print(f"🚀 Starting stable progressive loading: {filter_type} = {filter_value}")

        # Store filter state
        self.current_filter_type = filter_type
        self.current_filter_values = filter_value

        # Update control panel immediately
        if self.control_panel:
            self.control_panel.update_filter_description(filter_type, filter_value)
            self.control_panel.update_count(0)

        # Clear current data
        self.current_sequences.clear()
        self.all_loaded_sequences.clear()
        self._clear_grid()

        # Show loading UI
        self._show_loading_state()

        # Start progressive loading
        if self.progressive_loading_service:
            self.progressive_loading_service.start_progressive_loading(
                filter_type, filter_value, chunk_size
            )
        else:
            print("⚠️ No progressive loading service available")
            self._show_loading_fallback()

    def show_sequences(
        self,
        sequences: List[SequenceData],
        filter_type: Optional[FilterType] = None,
        filter_values: any = None,
    ) -> None:
        """
        Display sequences with stable layout (legacy compatibility).
        """
        print(f"📋 Showing {len(sequences)} sequences with stable layout")

        self.current_sequences = sequences
        self.all_loaded_sequences = sequences.copy()
        self.current_filter_type = filter_type
        self.current_filter_values = filter_values

        # Update control panel
        if self.control_panel:
            self.control_panel.update_filter_description(filter_type, filter_values)
            self.control_panel.update_count(len(sequences))

        # Hide loading UI
        self._hide_loading_state()

        # Get current sort method
        sort_method = (
            self.state_service.get_sort_order()
            if self.state_service
            else "alphabetical"
        )

        # Display with stable layout So
        self._display_sequences_with_stable_layout(sequences, sort_method)

    def _show_loading_state(self) -> None:
        """Show loading UI and hide browsing UI."""
        self._is_progressive_loading = True
        self._loading_cancelled = False

        self.loading_widget.show()
        self.browsing_widget.hide()

        # Reset progress
        if self.loading_progress_bar:
            self.loading_progress_bar.setValue(0)
            self.loading_progress_bar.setMaximum(100)

        if self.loading_label:
            self.loading_label.setText("Preparing to load sequences...")

    def _hide_loading_state(self) -> None:
        """Hide loading UI and show browsing UI."""
        self._is_progressive_loading = False

        self.loading_widget.hide()
        self.browsing_widget.show()

    def _cancel_loading(self) -> None:
        """Cancel the current loading operation."""
        if self.progressive_loading_service and self._is_progressive_loading:
            print("❌ User cancelled loading")
            self._loading_cancelled = True
            self.progressive_loading_service.cancel_loading()

    def _on_loading_started(self, total_count: int) -> None:
        """Handle loading started signal."""
        print(f"📊 Stable loading started: {total_count} sequences total")

        if self.loading_progress_bar:
            self.loading_progress_bar.setMaximum(total_count)
            self.loading_progress_bar.setValue(0)

        if self.loading_label:
            self.loading_label.setText(f"Loading {total_count} sequences...")

    def _on_sequences_chunk_loaded(self, chunk_sequences: List[SequenceData]) -> None:
        """Handle chunk loading with stable layout."""
        if self._loading_cancelled:
            return

        self.all_loaded_sequences.extend(chunk_sequences)

        chunk_size = len(chunk_sequences)
        total_loaded = len(self.all_loaded_sequences)

        print(
            f"📦 Stable chunk loaded: +{chunk_size} sequences (total: {total_loaded})"
        )

        # Update progress
        if self.loading_label:
            self.loading_label.setText(f"Loaded {total_loaded} sequences...")

        if self.control_panel:
            self.control_panel.update_count(total_loaded)

        # For first chunk, initialize stable layout
        if total_loaded == chunk_size:
            print("🎬 First chunk: initializing stable layout")
            self._hide_loading_state()
            self._initialize_stable_progressive_layout()

        # Add sequences using stable layout
        self._add_sequences_with_stable_layout(chunk_sequences)

    def _on_loading_progress(self, current: int, total: int) -> None:
        """Handle loading progress update."""
        if self._loading_cancelled:
            return

        if self.loading_progress_bar:
            self.loading_progress_bar.setValue(current)

        progress_percent = (current / total * 100) if total > 0 else 0
        print(
            f"📈 Stable loading progress: {current}/{total} ({progress_percent:.1f}%)"
        )

    def _on_loading_completed(self, final_sequences: List[SequenceData]) -> None:
        """Handle loading completion with final stable layout."""
        if self._loading_cancelled:
            print("🚫 Loading cancelled, ignoring completion")
            return

        self.current_sequences = final_sequences
        total_loaded = len(final_sequences)

        print(f"✅ Stable progressive loading completed: {total_loaded} sequences")

        self._hide_loading_state()
        self._finalize_stable_layout()

    def _on_loading_cancelled(self) -> None:
        """Handle loading cancellation."""
        print("❌ Stable loading cancelled")
        self._hide_loading_state()
        self._loading_cancelled = True

        if self.all_loaded_sequences:
            self.current_sequences = self.all_loaded_sequences
            self._finalize_stable_layout()
        else:
            self._show_empty_state()

    def _initialize_stable_progressive_layout(self) -> None:
        """Initialize the stable layout system for progressive loading."""
        self._clear_grid()

        # Get current sort method to determine layout strategy
        sort_method = (
            self.state_service.get_sort_order()
            if self.state_service
            else "alphabetical"
        )

        # Update thumbnail width based on current screen size
        self._update_stable_thumbnail_width()

        # Initialize simple loader
        self.row_loader = None  # Simplified - no complex loader needed

        print(f"🎨 Stable layout initialized for {sort_method} sorting")

    def _update_stable_thumbnail_width(self) -> None:
        """Update the stable layout manager's thumbnail width."""
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

        thumbnail_width = max(150, width_per_column)
        self.thumbnail_width = thumbnail_width

        print(f"🔧 Updated stable thumbnail width to {thumbnail_width}px")

    def _add_sequences_with_stable_layout(self, sequences: List[SequenceData]) -> None:
        """Add sequences using the stable layout system."""
        if not sequences or not self.row_loader:
            return

        # Get current sort method
        sort_method = (
            self.state_service.get_sort_order()
            if self.state_service
            else "alphabetical"
        )

        # Create simple thumbnails
        for i, sequence in enumerate(sequences):
            thumbnail = self._create_simple_thumbnail(sequence, sort_method)

            # Make clickable
            thumbnail.mousePressEvent = (
                lambda event, seq_id=sequence.id: self._on_thumbnail_clicked(seq_id)
            )

            # Add to grid layout
            row = i // 3  # 3 columns
            col = i % 3
            self.grid_layout.addWidget(thumbnail, row, col)

        # Process events to keep UI responsive
        QApplication.processEvents()

        print(f"🖼️ Added {len(sequences)} sequences with stable layout")

    def _finalize_stable_layout(self) -> None:
        """Finalize the stable layout after all loading is complete."""
        if not self.current_sequences:
            return

        # Add any remaining incomplete rows
        if self.row_loader:
            self.row_loader.finalize_remaining_thumbnails()

        # Get current sort method
        sort_method = (
            self.state_service.get_sort_order()
            if self.state_service
            else "alphabetical"
        )

        # For final display, reorganize with proper sections
        print(
            f"🎯 Finalizing stable layout with {len(self.current_sequences)} sequences"
        )
        self._display_sequences_with_stable_layout(self.current_sequences, sort_method)

    def _display_sequences_with_stable_layout(
        self, sequences: List[SequenceData], sort_method: str
    ) -> None:
        """Display sequences using stable layout with sections."""
        # Sort sequences
        sorted_sequences = self._sort_sequences(sequences, sort_method)

        # Group into sections
        sections = self._group_sequences_into_sections(sorted_sequences, sort_method)

        # Update navigation sidebar
        if self.navigation_sidebar:
            section_names = list(sections.keys())
            self.navigation_sidebar.update_sections(section_names, sort_method)

        # Clear and rebuild with stable layout
        self._clear_grid()

        current_row = 0
        thumbnail_count = 0

        for section_name, section_sequences in sections.items():
            # Add section header
            current_row = self._add_section_header(section_name, current_row)
            current_row += 1

            # Create simple thumbnails for this section
            for sequence in section_sequences:
                thumbnail = self._create_simple_thumbnail(sequence, sort_method)

                # Make clickable
                thumbnail.mousePressEvent = (
                    lambda event, seq_id=sequence.id: self._on_thumbnail_clicked(seq_id)
                )

                # Calculate position in 3-column grid
                col = thumbnail_count % 3
                if col == 0 and thumbnail_count > 0:
                    current_row += 1

                self.grid_layout.addWidget(thumbnail, current_row, col)
                thumbnail_count += 1

            # Start fresh row for next section
            if thumbnail_count % 3 != 0:
                current_row += 1
                thumbnail_count = ((thumbnail_count // 3) + 1) * 3

        # Add stretch to bottom
        self.grid_layout.setRowStretch(self.grid_layout.rowCount(), 1)

    def _on_sort_changed(self, sort_method: str) -> None:
        """Handle sort method change with stable layout."""
        print(f"🔄 Sort changed to: {sort_method} (stable layout)")

        if self.current_sequences:
            self._display_sequences_with_stable_layout(
                self.current_sequences, sort_method
            )

    def _sort_sequences(
        self, sequences: List[SequenceData], sort_method: str
    ) -> List[SequenceData]:
        """Sort sequences based on the selected method."""
        print(f"🔄 Sorting {len(sequences)} sequences by {sort_method}")

        if sort_method == "alphabetical":
            result = sorted(sequences, key=lambda s: s.word.lower() if s.word else "")
        elif sort_method == "length":
            result = sorted(
                sequences, key=lambda s: s.sequence_length if s.sequence_length else 0
            )
            print(
                f"  🔢 Length sorted: {[(seq.word, seq.sequence_length) for seq in result[:5]]}"
            )
        elif sort_method == "level":
            result = sorted(sequences, key=lambda s: s.level if s.level else 0)
        elif sort_method == "date_added":
            result = sorted(
                sequences,
                key=lambda s: s.date_added if s.date_added else datetime.min,
                reverse=True,
            )
        else:
            result = sorted(sequences, key=lambda s: s.word.lower() if s.word else "")

        return result

    def _group_sequences_into_sections(
        self, sequences: List[SequenceData], sort_method: str
    ) -> dict[str, List[SequenceData]]:
        """Group sequences into sections based on sort method."""
        sections = {}

        for sequence in sequences:
            section_key = self._get_section_key(sequence, sort_method)
            if section_key not in sections:
                sections[section_key] = []
            sections[section_key].append(sequence)

        return sections

    def _get_section_key(self, sequence: SequenceData, sort_method: str) -> str:
        """Get the section key for a sequence based on sort method."""
        if sort_method == "alphabetical":
            return sequence.word[0].upper() if sequence.word else "?"
        elif sort_method == "length":
            return (
                f"Length {sequence.sequence_length}"
                if sequence.sequence_length
                else "Unknown Length"
            )
        elif sort_method == "level":
            return f"Level {sequence.level}" if sequence.level else "Unknown Level"
        elif sort_method == "date_added":
            if sequence.date_added:
                return sequence.date_added.strftime("%m-%d-%Y")
            else:
                return "Unknown"
        else:
            return sequence.word[0].upper() if sequence.word else "?"

    def _add_section_header(self, section_name: str, current_row: int) -> int:
        """Add a section header to the grid."""
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

    def _on_section_selected(self, section: str) -> None:
        """Handle navigation sidebar section selection."""
        print(f"🧭 Navigating to section: {section}")

        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if (
                    hasattr(widget, "findChild")
                    and widget.findChild(QLabel)
                    and widget.findChild(QLabel).text() == section
                ):
                    header_global_pos = widget.mapToGlobal(QPoint(0, 0))
                    content_widget_pos = self.scroll_area.widget().mapFromGlobal(
                        header_global_pos
                    )
                    vertical_pos = content_widget_pos.y()
                    self.scroll_area.verticalScrollBar().setValue(vertical_pos)
                    break
        else:
            self.scroll_area.verticalScrollBar().setValue(0)

    def _create_simple_thumbnail(
        self, sequence: SequenceData, sort_method: str
    ) -> QWidget:
        """Create a thumbnail widget for a sequence with actual image loading."""
        # Create container frame
        thumbnail = QFrame()
        thumbnail.setFixedSize(self.thumbnail_width, self.thumbnail_width)
        thumbnail.setStyleSheet(
            """
            QFrame {
                border: 1px solid #ccc;
                background-color: #f0f0f0;
                border-radius: 4px;
            }
            QFrame:hover {
                border-color: #007acc;
                background-color: #e6f3ff;
            }
        """
        )

        layout = QVBoxLayout(thumbnail)
        layout.setContentsMargins(4, 4, 4, 4)

        # Try to load actual thumbnail image
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setMinimumHeight(self.thumbnail_width - 40)  # Leave space for text

        # Load thumbnail image if available
        if hasattr(sequence, "thumbnails") and sequence.thumbnails:
            # Use first thumbnail
            thumbnail_path = sequence.thumbnails[0]
            pixmap = QPixmap(thumbnail_path)

            if not pixmap.isNull():
                # Scale image to fit while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    self.thumbnail_width - 8,
                    self.thumbnail_width - 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                image_label.setPixmap(scaled_pixmap)
            else:
                # Fallback to placeholder text if image loading fails
                placeholder_text = f"❌\n{sequence.word or 'Sequence'}"
                image_label.setText(placeholder_text)
                image_label.setStyleSheet(
                    """
                    color: #999;
                    font-size: 12px;
                    background-color: #f8f8f8;
                    border: 1px dashed #ddd;
                    border-radius: 4px;
                    padding: 8px;
                """
                )
        elif hasattr(sequence, "thumbnail_paths") and sequence.thumbnail_paths:
            # Alternative property name
            thumbnail_path = sequence.thumbnail_paths[0]
            pixmap = QPixmap(thumbnail_path)

            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.thumbnail_width - 8,
                    self.thumbnail_width - 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                image_label.setPixmap(scaled_pixmap)
            else:
                placeholder_text = f"❌\n{sequence.word or 'Sequence'}"
                image_label.setText(placeholder_text)
                image_label.setStyleSheet(
                    """
                    color: #999;
                    font-size: 12px;
                    background-color: #f8f8f8;
                    border: 1px dashed #ddd;
                    border-radius: 4px;
                    padding: 8px;
                """
                )
        else:
            # No thumbnail available - show informative placeholder
            placeholder_text = f"📄\n{sequence.word or 'Sequence'}"
            image_label.setText(placeholder_text)
            image_label.setStyleSheet(
                """
                color: #666;
                font-size: 14px;
                font-weight: bold;
                background-color: #f8f8f8;
                border: 1px dashed #ccc;
                border-radius: 4px;
                padding: 10px;
            """
            )

        layout.addWidget(image_label)

        # Sequence name
        name_label = QLabel(sequence.name or f"Sequence {sequence.id[:8]}")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("font-size: 10px; font-weight: bold;")
        layout.addWidget(name_label)

        # Beat count
        beat_count = len(sequence.beats) if sequence.beats else 0
        count_label = QLabel(f"{beat_count} beats")
        count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count_label.setStyleSheet("color: #666; font-size: 9px;")
        layout.addWidget(count_label)

        return thumbnail

    def _on_thumbnail_clicked(self, sequence_id: str) -> None:
        """Handle thumbnail click."""
        self.sequence_selected.emit(sequence_id)
        self.open_in_construct.emit(sequence_id)

    def _clear_grid(self) -> None:
        """Clear all items from the grid layout."""
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _show_empty_state(self) -> None:
        """Show empty state message."""
        self._clear_grid()

        empty_label = QLabel("No sequences found")
        empty_label.setFont(QFont("Segoe UI", 14))
        empty_label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_layout.addWidget(empty_label, 0, 0, 1, 3)

    def _show_loading_fallback(self) -> None:
        """Show basic loading message when progressive loading unavailable."""
        self._clear_grid()

        loading_label = QLabel("Loading sequences...")
        loading_label.setFont(QFont("Segoe UI", 14))
        loading_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_layout.addWidget(loading_label, 0, 0, 1, 3)
        QTimer.singleShot(2000, lambda: self._hide_loading_state())

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize event by updating stable layout dimensions."""
        super().resizeEvent(event)

        # Update stable layout manager's thumbnail width
        QTimer.singleShot(100, self._update_stable_thumbnail_width)
