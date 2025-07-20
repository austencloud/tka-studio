"""
Sequence Browser Panel - Thumbnail Grid and Preview

Displays filtered sequences in a responsive thumbnail grid.
Handles the complex thumbnail management identified in the Legacy audit.
"""

from datetime import datetime
from typing import List, Optional

from domain.models.sequence_data import SequenceData
from presentation.tabs.browse.models import FilterType
from presentation.tabs.browse.services.browse_service import BrowseService
from presentation.tabs.browse.services.browse_state_service import BrowseStateService
from PyQt6.QtCore import QPoint, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QResizeEvent
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .modern_browse_control_panel import ModernBrowseControlPanel
from .modern_navigation_sidebar import ModernNavigationSidebar


class SequenceBrowserPanel(QWidget):
    """
    Sequence browser with thumbnail grid.

    Handles the complex thumbnail management and responsive layout
    identified as real complexity in the Legacy audit.
    """

    # Signals
    sequence_selected = pyqtSignal(str)  # sequence_id
    open_in_construct = pyqtSignal(str)  # sequence_id
    back_to_filters = pyqtSignal()

    def __init__(
        self,
        browse_service: BrowseService,
        state_service: BrowseStateService,
        parent: Optional[QWidget] = None,
    ):
        """Initialize the sequence browser panel."""
        super().__init__(parent)

        self.browse_service = browse_service
        self.state_service = state_service
        self.current_sequences: List[SequenceData] = []

        # Responsive sizing properties
        self.thumbnail_width = 150  # Minimum width
        self.thumbnail_height = 120  # Base height
        self.thumbnail_widgets: List[QWidget] = []

        # Navigation sidebar
        self.navigation_sidebar: Optional[ModernNavigationSidebar] = None

        # Control panel
        self.control_panel: Optional[ModernBrowseControlPanel] = None

        # Current filter state
        self.current_filter_type: Optional[FilterType] = None
        self.current_filter_values: any = None

        self._setup_ui()
        self._connect_signals()

    def _calculate_thumbnail_size(self) -> tuple[int, int]:
        """Calculate responsive thumbnail size based on available width."""
        # Get available width from scroll area
        available_width = self.scroll_area.width()

        # Account for margins and scrollbar
        scrollbar_width = 20  # Approximate scrollbar width
        content_margins = 40  # Content layout margins (20px each side)
        grid_margins = 30  # Grid layout margins (15px each side)

        # Calculate usable width
        usable_width = (
            available_width - scrollbar_width - content_margins - grid_margins
        )

        # Legacy formula: 3-column grid with minimum 150px width
        # Account for grid spacing (15px between columns)
        grid_spacing = 15 * 2  # 2 spaces between 3 columns
        width_per_column = (usable_width - grid_spacing) // 3

        # Apply minimum width constraint
        thumbnail_width = max(150, width_per_column)

        # Calculate proportional height (maintain 5:4 aspect ratio)
        thumbnail_height = int(thumbnail_width * 0.8)

        return thumbnail_width, thumbnail_height

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize event to update thumbnail sizes."""
        super().resizeEvent(event)

        # Only update if we have thumbnails to update
        if self.thumbnail_widgets:
            # Recalculate and apply sizes
            from PyQt6.QtCore import QTimer

            QTimer.singleShot(5, self._update_thumbnail_sizes)

    def _update_thumbnail_sizes(self) -> None:
        """Update sizes of existing thumbnail widgets."""
        # Recalculate thumbnail width based on current scroll area
        actual_scroll_width = self.scroll_area.width()
        scrollbar_width = 20
        content_margins = 40
        grid_margins = 30
        usable_width = (
            actual_scroll_width - scrollbar_width - content_margins - grid_margins
        )
        grid_spacing = 15 * 2
        width_per_column = (usable_width - grid_spacing) // 3
        thumbnail_width = max(150, width_per_column)

        # Update stored values
        self.thumbnail_width = thumbnail_width

        for thumbnail in self.thumbnail_widgets:
            # Set the thumbnail container to the calculated width
            thumbnail.setFixedWidth(thumbnail_width)
            # Don't set a fixed height - let it expand based on content
            thumbnail.setMinimumHeight(50)  # Just prevent collapse

            # Update the image inside based on the actual thumbnail width
            self._update_image_in_thumbnail(thumbnail)

    def _setup_ui(self) -> None:
        """Setup the browser UI with control panel and navigation sidebar."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Control panel (replaces the old header)
        self.control_panel = ModernBrowseControlPanel(self.state_service)
        layout.addWidget(self.control_panel)

        # Main content area with horizontal layout (sidebar + grid)
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

        # Main browsing area: sidebar + grid
        browsing_layout = QHBoxLayout()
        browsing_layout.setSpacing(15)

        # Navigation sidebar (15% of width)
        self.navigation_sidebar = ModernNavigationSidebar()
        self.navigation_sidebar.set_minimum_width(150)
        self.navigation_sidebar.setMaximumWidth(250)
        browsing_layout.addWidget(self.navigation_sidebar, 0)  # Fixed size

        # Thumbnail grid scroll area (85% of width)
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
        browsing_layout.addWidget(self.scroll_area, 1)  # Takes remaining space

        content_layout.addLayout(browsing_layout)

        # Grid widget
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(15)

        # Set column stretch factors to ensure 3 equal columns
        for col in range(3):
            self.grid_layout.setColumnStretch(col, 1)

        self.scroll_area.setWidget(self.grid_widget)

        layout.addWidget(content_panel)

    def _connect_signals(self) -> None:
        """Connect component signals."""
        # Control panel signals
        if self.control_panel:
            self.control_panel.back_to_filters.connect(self.back_to_filters.emit)
            self.control_panel.sort_changed.connect(self._on_sort_changed)

        # Navigation sidebar signals
        if self.navigation_sidebar:
            self.navigation_sidebar.section_selected.connect(self._on_section_selected)

    def _on_sort_changed(self, sort_method: str) -> None:
        """Handle sort method change from control panel."""
        print(f"🔄 Sort method changed to: {sort_method}")

        # Debug: Check if we have sequences with dates
        if sort_method == "date_added" and self.current_sequences:
            date_count = 0
            for seq in self.current_sequences:
                if seq.date_added:
                    date_count += 1
                    print(f"  DEBUG: {seq.word} has date: {seq.date_added}")
                else:
                    print(f"  DEBUG: {seq.word} has no date_added")
            print(
                f"  DEBUG: Found {date_count} sequences with dates out of {len(self.current_sequences)}"
            )

        # Re-sort and re-display current sequences
        if self.current_sequences:
            self._sort_and_display_sequences(self.current_sequences, sort_method)

    def _sort_and_display_sequences(
        self, sequences: List[SequenceData], sort_method: str
    ) -> None:
        """Sort sequences and display them with section headers."""
        # Sort sequences based on the selected method
        sorted_sequences = self._sort_sequences(sequences, sort_method)

        # Group sequences into sections
        sections = self._group_sequences_into_sections(sorted_sequences, sort_method)

        # Update navigation sidebar
        if self.navigation_sidebar:
            section_names = list(sections.keys())
            self.navigation_sidebar.update_sections(section_names, sort_method)

        # Clear existing grid
        self._clear_grid()
        self.thumbnail_widgets.clear()

        # Display sequences with section headers
        current_row = 0
        thumbnail_count = 0

        for section_name, section_sequences in sections.items():
            # Add section header for all sections (including first section)
            current_row = self._add_section_header(section_name, current_row)

            # Move to next row for thumbnails after header
            current_row += 1

            # Add sequences for this section
            for sequence in section_sequences:
                thumbnail = self._create_sequence_thumbnail(sequence)
                self.thumbnail_widgets.append(thumbnail)

                # Calculate position in 3-column grid
                col = thumbnail_count % 3
                if col == 0 and thumbnail_count > 0:  # Start new row
                    current_row += 1

                self.grid_layout.addWidget(thumbnail, current_row, col)
                thumbnail_count += 1

            # If we finished a section and have incomplete row, start fresh for next section
            if thumbnail_count % 3 != 0:
                current_row += 1
                thumbnail_count = (
                    (thumbnail_count // 3) + 1
                ) * 3  # Round up to next multiple of 3

        # Add stretch to bottom
        self.grid_layout.setRowStretch(self.grid_layout.rowCount(), 1)

        # Schedule sizing after layout is complete
        from PyQt6.QtCore import QTimer

        QTimer.singleShot(10, self._calculate_and_apply_sizes)

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
        elif sort_method == "level":
            result = sorted(sequences, key=lambda s: s.level if s.level else 0)
        elif sort_method == "date_added":
            print("  DEBUG: Sorting by date_added")
            result = sorted(
                sequences,
                key=lambda s: s.date_added if s.date_added else datetime.min,
                reverse=True,
            )
            print(f"  DEBUG: Sorted order: {[seq.word for seq in result]}")
        else:
            # Default to alphabetical
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
                # Format date exactly like legacy: "%m-%d-%Y"
                return sequence.date_added.strftime("%m-%d-%Y")
            else:
                return "Unknown"
        else:
            return sequence.word[0].upper() if sequence.word else "?"

    def _add_section_header(self, section_name: str, current_row: int) -> int:
        """Add a section header to the grid."""
        # Create section header widget
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

        # Section title
        title_label = QLabel(section_name)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.9); background: transparent; border: none;"
        )
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Add header spanning all 3 columns
        # For the first section (current_row == 0), place header at row 0
        # For subsequent sections, increment row first
        if current_row > 0:
            current_row += 1
        self.grid_layout.addWidget(header_widget, current_row, 0, 1, 3)

        return current_row

    def _on_section_selected(self, section: str) -> None:
        """Handle navigation sidebar section selection."""
        print(f"🧭 Navigating to section: {section}")

        # Find the section header in the grid
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                # Check if this is a section header
                if (
                    hasattr(widget, "findChild")
                    and widget.findChild(QLabel)
                    and widget.findChild(QLabel).text() == section
                ):
                    # Use precise positioning like legacy system
                    # Calculate the exact position to place header at top of scroll area
                    header_global_pos = widget.mapToGlobal(QPoint(0, 0))
                    content_widget_pos = self.scroll_area.widget().mapFromGlobal(
                        header_global_pos
                    )
                    vertical_pos = content_widget_pos.y()
                    self.scroll_area.verticalScrollBar().setValue(vertical_pos)
                    break
        else:
            # If no section found, scroll to top
            self.scroll_area.verticalScrollBar().setValue(0)

    def show_sequences(
        self,
        sequences: List[SequenceData],
        filter_type: Optional[FilterType] = None,
        filter_values: any = None,
    ) -> None:
        """Display sequences in the thumbnail grid."""
        self.current_sequences = sequences
        self.current_filter_type = filter_type
        self.current_filter_values = filter_values

        # Update control panel
        if self.control_panel:
            self.control_panel.update_filter_description(filter_type, filter_values)
            self.control_panel.update_count(len(sequences))

        # Get current sort method
        sort_method = (
            self.state_service.get_sort_order()
            if self.state_service
            else "alphabetical"
        )

        # Sort and display sequences with proper sectioning
        self._sort_and_display_sequences(sequences, sort_method)

    def _calculate_and_apply_sizes(self) -> None:
        """Calculate thumbnail sizes based on actual scroll area width and apply them."""
        # Now get the actual scroll area width after layout is complete
        actual_scroll_width = self.scroll_area.width()

        # Account for margins and scrollbar
        scrollbar_width = 20  # Approximate scrollbar width
        content_margins = 40  # Content layout margins (20px each side)
        grid_margins = 30  # Grid layout margins (15px each side)

        # Calculate usable width
        usable_width = (
            actual_scroll_width - scrollbar_width - content_margins - grid_margins
        )

        # Legacy formula: 3-column grid with minimum 150px width
        # Account for grid spacing (15px between columns)
        grid_spacing = 15 * 2  # 2 spaces between 3 columns
        width_per_column = (usable_width - grid_spacing) // 3

        # Apply minimum width constraint
        thumbnail_width = max(150, width_per_column)

        # Calculate proportional height (maintain 5:4 aspect ratio)
        thumbnail_height = int(thumbnail_width * 0.8)

        # Update stored values
        self.thumbnail_width = thumbnail_width
        self.thumbnail_height = thumbnail_height

        # Apply sizes to all thumbnails
        for thumbnail in self.thumbnail_widgets:
            # Set the thumbnail container to the calculated width
            thumbnail.setFixedWidth(thumbnail_width)
            # Don't set a fixed height - let it expand based on content
            thumbnail.setMinimumHeight(50)  # Just a minimal height to prevent collapse

            # Update the image inside based on the actual thumbnail width
            self._update_image_in_thumbnail(thumbnail)

    def _update_image_in_thumbnail(self, thumbnail: QWidget) -> None:
        """Update the image size in a thumbnail based on its actual width."""
        if not hasattr(thumbnail, "_image_box"):
            return

        image_box = thumbnail._image_box
        image_label = image_box._image_label

        # Calculate available width for the image
        actual_thumbnail_width = thumbnail.width()
        if actual_thumbnail_width <= 0:
            return

        # Account for thumbnail margins (10px each side)
        available_width = actual_thumbnail_width - 20

        # Update the image box width
        image_box.setFixedWidth(available_width)

        # Update the image inside the box
        if hasattr(image_box, "_thumbnail_path"):
            pixmap = QPixmap(image_box._thumbnail_path)
            if not pixmap.isNull():
                # Scale the image to fit the available width
                scaled_pixmap = pixmap.scaledToWidth(
                    available_width, Qt.TransformationMode.SmoothTransformation
                )
                image_label.setPixmap(scaled_pixmap)
                image_label.setFixedSize(scaled_pixmap.size())

                # Update the image box height to match the image
                image_box.setFixedHeight(scaled_pixmap.height())

                # Force the container to recalculate its size
                # Remove any height constraints that might be preventing expansion
                thumbnail.setMinimumHeight(0)
                thumbnail.setMaximumHeight(16777215)  # Qt's maximum

                # Calculate the required container height
                layout = thumbnail.layout()
                word_height = thumbnail._word_label.height()
                info_height = thumbnail._info_label.height()
                spacing = layout.spacing()
                margins = layout.contentsMargins()

                required_height = (
                    word_height
                    + scaled_pixmap.height()
                    + info_height
                    + (spacing * 2)
                    + margins.top()
                    + margins.bottom()
                )

                # Set the container to the required height
                thumbnail.setMinimumHeight(required_height)

                # Force layout update
                thumbnail.updateGeometry()

                # DEBUG: Log size measurements
                container_height = thumbnail.height()
                image_height = scaled_pixmap.height()
                box_height = image_box.height()

            else:
                # Fallback for failed image load
                image_label.setText("🎭")
                image_label.setFixedSize(available_width, 60)
                image_box.setFixedHeight(60)
                image_label.setStyleSheet(
                    "background: transparent; border: none; color: rgba(255, 255, 255, 0.7); font-size: 24px;"
                )
        else:
            # This is a fallback without image
            image_label.setText("🎭")
            image_label.setFixedSize(available_width, 60)
            image_box.setFixedHeight(60)
            image_label.setStyleSheet(
                "background: transparent; border: none; color: rgba(255, 255, 255, 0.7); font-size: 24px;"
            )

    def _clear_grid(self) -> None:
        """Clear all items from the grid layout."""
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _create_sequence_thumbnail(self, sequence: SequenceData) -> QWidget:
        """Create a thumbnail widget for a sequence."""
        thumbnail = QFrame()
        # Only set minimum width, let height expand naturally based on content
        thumbnail.setMinimumWidth(150)
        thumbnail.setStyleSheet(
            """
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
            }
            QFrame:hover {
                border: 2px solid rgba(255, 255, 255, 0.4);
            }
        """
        )
        layout = QVBoxLayout(thumbnail)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Sequence word
        word_label = QLabel(sequence.word or "Unknown")
        word_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        word_label.setStyleSheet("color: white;")
        word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(word_label)

        # Thumbnail image box (like legacy version)
        image_box = self._create_thumbnail_image_box(sequence)
        layout.addWidget(image_box)

        # Sequence info
        info_text = f"Length: {sequence.sequence_length}"
        if sequence.difficulty_level:
            info_text += f"\\n{sequence.difficulty_level}"

        info_label = QLabel(info_text)
        info_label.setFont(QFont("Segoe UI", 9))
        info_label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        # Store references for easier access
        thumbnail._word_label = word_label
        thumbnail._image_box = image_box
        thumbnail._info_label = info_label

        # Make clickable
        thumbnail.mousePressEvent = (
            lambda event, seq_id=sequence.id: self._on_thumbnail_clicked(seq_id)
        )

        return thumbnail

    def _create_thumbnail_image_box(self, sequence: SequenceData) -> QWidget:
        """Create a thumbnail image box (container) similar to legacy version."""
        # Create the image box container
        image_box = QFrame()
        image_box.setStyleSheet(
            """
            QFrame {
                background: rgba(0, 0, 0, 0.2);
                border-radius: 4px;
            }
            """
        )

        # Use a layout to center the image within the box
        box_layout = QVBoxLayout(image_box)
        box_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.setSpacing(0)

        # Create the actual image label
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("background: transparent; border: none;")

        # Store sequence data for later use
        image_box._sequence = sequence
        image_box._image_label = image_label

        # Set initial size - will be updated later
        image_box.setMinimumHeight(80)  # Minimum height to prevent collapse

        # Load actual thumbnail if available
        if sequence.thumbnails and len(sequence.thumbnails) > 0:
            thumbnail_path = sequence.thumbnails[0]  # Use first thumbnail
            image_box._thumbnail_path = thumbnail_path

            # Load and set a basic version of the image
            pixmap = QPixmap(thumbnail_path)
            if not pixmap.isNull():
                # Create a temporary scaled version at basic size
                scaled_pixmap = pixmap.scaledToWidth(
                    130, Qt.TransformationMode.SmoothTransformation
                )
                image_label.setPixmap(scaled_pixmap)
                image_label.setFixedSize(scaled_pixmap.size())
            else:
                # Fallback to text if image fails to load
                image_label.setText("🎭")
                image_label.setFixedSize(130, 60)
                image_label.setStyleSheet(
                    "background: transparent; border: none; color: rgba(255, 255, 255, 0.7); font-size: 24px;"
                )
        else:
            # No thumbnails available - use fallback
            image_label.setText("🎭")
            image_label.setFixedSize(130, 60)
            image_label.setStyleSheet(
                "background: transparent; border: none; color: rgba(255, 255, 255, 0.7); font-size: 24px;"
            )

        box_layout.addWidget(image_label)

        return image_box

    def _on_thumbnail_clicked(self, sequence_id: str) -> None:
        """Handle thumbnail click."""
        self.sequence_selected.emit(sequence_id)
        # For now, also emit open in construct
        self.open_in_construct.emit(sequence_id)

    def _extract_sections(self, sequences: List[SequenceData]) -> List[str]:
        """Extract navigation sections from sequences based on current sort order."""
        if not sequences:
            return []

        # Get current sort order
        sort_order = (
            self.state_service.get_sort_order()
            if self.state_service
            else "alphabetical"
        )

        sections = set()

        for sequence in sequences:
            if sort_order == "alphabetical":
                # Group by first letter
                if sequence.word:
                    sections.add(sequence.word[0].upper())
            elif sort_order == "length":
                # Group by sequence length
                if hasattr(sequence, "length") and sequence.length:
                    sections.add(str(sequence.length))
            elif sort_order == "level":
                # Group by difficulty level
                if hasattr(sequence, "level") and sequence.level:
                    sections.add(str(sequence.level))
            elif sort_order == "date_added":
                # Group by date (simplified - could be more sophisticated)
                if hasattr(sequence, "date_added") and sequence.date_added:
                    sections.add(sequence.date_added.strftime("%Y-%m"))
            else:
                # Default to alphabetical
                if sequence.word:
                    sections.add(sequence.word[0].upper())

        # Sort sections appropriately
        if sort_order == "alphabetical":
            return sorted(list(sections))
        elif sort_order in ["length", "level"]:
            return sorted(list(sections), key=lambda x: int(x) if x.isdigit() else 0)
        else:
            return sorted(list(sections))
