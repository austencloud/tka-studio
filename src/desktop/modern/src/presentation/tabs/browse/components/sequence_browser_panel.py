"""
Sequence Browser Panel - Thumbnail Grid and Preview

Displays filtered sequences in a responsive thumbnail grid.
Handles the complex thumbnail management identified in the Legacy audit.
"""

from typing import List, Optional

from domain.models.sequence_data import SequenceData
from presentation.tabs.browse.services.browse_service import BrowseService
from presentation.tabs.browse.services.browse_state_service import BrowseStateService
from PyQt6.QtCore import QSize, Qt, pyqtSignal
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
        usable_width = actual_scroll_width - scrollbar_width - content_margins - grid_margins
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
        """Setup the browser UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header with back button and title
        header = self._create_header()
        layout.addWidget(header)

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

        # Results info
        self.results_label = QLabel("No sequences loaded")
        self.results_label.setFont(QFont("Segoe UI", 12))
        self.results_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        content_layout.addWidget(self.results_label)

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

        # Grid widget
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(15)

        # Set column stretch factors to ensure 3 equal columns
        for col in range(3):
            self.grid_layout.setColumnStretch(col, 1)

        self.scroll_area.setWidget(self.grid_widget)

        content_layout.addWidget(self.scroll_area)
        layout.addWidget(content_panel)

    def _create_header(self) -> QWidget:
        """Create the header with back button and title."""
        header = QFrame()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        # Back button
        self.back_button = QPushButton("← Back to Filters")
        self.back_button.setFont(QFont("Segoe UI", 12))
        self.back_button.setStyleSheet(
            """
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """
        )
        layout.addWidget(self.back_button)

        layout.addStretch()

        # Title
        self.title_label = QLabel("Sequence Browser")
        self.title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: white;")
        layout.addWidget(self.title_label)

        layout.addStretch()

        return header

    def _connect_signals(self) -> None:
        """Connect component signals."""
        self.back_button.clicked.connect(self.back_to_filters.emit)

    def show_sequences(self, sequences: List[SequenceData]) -> None:
        """Display sequences in the thumbnail grid."""
        self.current_sequences = sequences

        # Update results label
        count = len(sequences)
        if count == 0:
            self.results_label.setText(
                "No sequences found matching the filter criteria"
            )
        elif count == 1:
            self.results_label.setText("1 sequence found")
        else:
            self.results_label.setText(f"{count} sequences found")

        # Clear existing grid
        self._clear_grid()
        self.thumbnail_widgets.clear()

        # Create thumbnails with initial minimal sizing
        # The actual sizing will be done after layout is complete
        for i, sequence in enumerate(sequences):
            thumbnail = self._create_sequence_thumbnail(sequence)
            self.thumbnail_widgets.append(thumbnail)

            # Use 3-column grid layout (legacy style)
            row = i // 3
            col = i % 3
            self.grid_layout.addWidget(thumbnail, row, col)
            
            # DEBUG: Log initial thumbnail creation
            print(f"📏 Initial thumbnail {i} ({sequence.word}): size={thumbnail.size()}")

        # Add stretch to bottom
        self.grid_layout.setRowStretch(self.grid_layout.rowCount(), 1)

        # Schedule sizing after layout is complete
        from PyQt6.QtCore import QTimer

        QTimer.singleShot(10, self._calculate_and_apply_sizes)

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
        """Update the image size in a specific thumbnail based on its actual width."""
        layout = thumbnail.layout()
        if layout:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    # Look for the image container (it has a specific background style)
                    if isinstance(widget, QWidget) and widget.styleSheet().startswith(
                        "background: rgba(0, 0, 0, 0.2)"
                    ):
                        # This is our image container
                        actual_thumbnail_width = thumbnail.width()
                        if actual_thumbnail_width > 0:
                            # Account for margins and use the actual available width
                            available_width = (
                                actual_thumbnail_width - 20
                            )  # 10px margin each side

                            # Check if this container has a stored pixmap path
                            if hasattr(widget, "_thumbnail_path"):
                                pixmap = QPixmap(widget._thumbnail_path)
                                if not pixmap.isNull():
                                    # Re-scale the pixmap to new width (legacy behavior)
                                    scaled_pixmap = pixmap.scaledToWidth(
                                        available_width,
                                        Qt.TransformationMode.SmoothTransformation,
                                    )
                                    
                                    # Set the container size to match the image
                                    widget.setFixedSize(scaled_pixmap.width(), scaled_pixmap.height())
                                    
                                    # Find the image label inside the container and update it
                                    container_layout = widget.layout()
                                    if container_layout and container_layout.count() > 0:
                                        image_label = container_layout.itemAt(0).widget()
                                        if isinstance(image_label, QLabel):
                                            image_label.setPixmap(scaled_pixmap)
                                    
                                    # DEBUG: Log size measurements
                                    container_height = thumbnail.height()
                                    image_height = scaled_pixmap.height()
                                    print(f"📏 Thumbnail debug: Container={actual_thumbnail_width}x{container_height}, Image={available_width}x{image_height}, Pixmap={scaled_pixmap.width()}x{scaled_pixmap.height()}")
                                else:
                                    # Fallback for failed image load
                                    widget.setFixedSize(available_width, 60)
                                    container_layout = widget.layout()
                                    if container_layout and container_layout.count() > 0:
                                        image_label = container_layout.itemAt(0).widget()
                                        if isinstance(image_label, QLabel):
                                            image_label.setText("🎭")
                                            image_label.setStyleSheet(
                                                "background: transparent; color: rgba(255, 255, 255, 0.7); font-size: 24px;"
                                            )
                            else:
                                # This is a fallback container without image
                                widget.setFixedSize(available_width, 60)
                                container_layout = widget.layout()
                                if container_layout and container_layout.count() > 0:
                                    image_label = container_layout.itemAt(0).widget()
                                    if isinstance(image_label, QLabel):
                                        image_label.setText("🎭")
                                        image_label.setStyleSheet(
                                            "background: transparent; color: rgba(255, 255, 255, 0.7); font-size: 24px;"
                                        )
                        break

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

        # Actual thumbnail image
        image_label = self._create_thumbnail_image(sequence)
        layout.addWidget(image_label)

        # Sequence info
        info_text = f"Length: {sequence.sequence_length}"
        if sequence.difficulty_level:
            info_text += f"\\n{sequence.difficulty_level}"

        info_label = QLabel(info_text)
        info_label.setFont(QFont("Segoe UI", 9))
        info_label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        # Make clickable
        thumbnail.mousePressEvent = (
            lambda event, seq_id=sequence.id: self._on_thumbnail_clicked(seq_id)
        )

        return thumbnail

    def _create_thumbnail_image(self, sequence: SequenceData) -> QWidget:
        """Create thumbnail image container with proper sizing like legacy version."""
        # Create a container widget for the image (like legacy thumbnail box)
        image_container = QWidget()
        image_container.setStyleSheet("background: rgba(0, 0, 0, 0.2); border-radius: 4px;")
        
        # Use a simple layout for the container
        container_layout = QVBoxLayout(image_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Create the actual image label
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("background: transparent;")  # No background - container handles it
        
        # Set initial size - will be updated later
        image_container.setMinimumSize(130, 40)  # Basic fallback size
        
        # Load actual thumbnail if available
        if sequence.thumbnails and len(sequence.thumbnails) > 0:
            thumbnail_path = sequence.thumbnails[0]  # Use first thumbnail
            # Store the path for later use
            image_container._thumbnail_path = thumbnail_path
            
            # Load and set a basic version of the image
            pixmap = QPixmap(thumbnail_path)
            if not pixmap.isNull():
                # Create a temporary scaled version at basic size
                scaled_pixmap = pixmap.scaledToWidth(
                    130, Qt.TransformationMode.SmoothTransformation
                )
                image_label.setPixmap(scaled_pixmap)
                # Container manages the size, not the label
                image_container.setFixedSize(scaled_pixmap.width(), scaled_pixmap.height())
            else:
                # Fallback to text if image fails to load
                image_label.setText("🎭")
                image_label.setStyleSheet("background: transparent; color: rgba(255, 255, 255, 0.7); font-size: 24px;")
                image_container.setFixedSize(130, 60)
        else:
            # No thumbnails available - use fallback
            image_label.setText("🎭")
            image_label.setStyleSheet("background: transparent; color: rgba(255, 255, 255, 0.7); font-size: 24px;")
            image_container.setFixedSize(130, 60)
        
        # Add the image label to the container
        container_layout.addWidget(image_label)
        
        return image_container

    def _on_thumbnail_clicked(self, sequence_id: str) -> None:
        """Handle thumbnail click."""
        self.sequence_selected.emit(sequence_id)
        # For now, also emit open in construct
        self.open_in_construct.emit(sequence_id)
