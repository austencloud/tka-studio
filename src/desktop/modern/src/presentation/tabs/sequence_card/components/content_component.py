"""
Sequence Card Content Component

Modern implementation of the scrollable content display area.
"""

import logging
from typing import Optional, List
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QFrame, 
    QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPen, QBrush

from core.interfaces.sequence_card_services import (
    ISequenceCardDisplayService, ISequenceCardCacheService, 
    ISequenceCardLayoutService, SequenceCardData
)

logger = logging.getLogger(__name__)


class SequenceCardWidget(QLabel):
    """Widget for displaying individual sequence card."""
    
    def __init__(self, sequence_data: SequenceCardData, parent=None):
        super().__init__(parent)
        self.sequence_data = sequence_data
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(150, 100)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._apply_styling()
        self._load_image()
    
    def _apply_styling(self):
        """Apply card styling."""
        self.setStyleSheet("""
            QLabel {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 5px;
                margin: 5px;
            }
            
            QLabel:hover {
                border: 2px solid #3498db;
                background: #f8f9fa;
            }
        """)
    
    def _load_image(self):
        """Load and display the sequence image."""
        try:
            if self.sequence_data.path.exists():
                pixmap = QPixmap(str(self.sequence_data.path))
                if not pixmap.isNull():
                    # Scale pixmap to fit while maintaining aspect ratio
                    scaled_pixmap = pixmap.scaled(
                        self.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.setPixmap(scaled_pixmap)
                else:
                    self._set_placeholder_text(f"Could not load:\n{self.sequence_data.word}")
            else:
                self._set_placeholder_text(f"Missing:\n{self.sequence_data.word}")
        except Exception as e:
            logger.warning(f"Error loading image {self.sequence_data.path}: {e}")
            self._set_placeholder_text(f"Error:\n{self.sequence_data.word}")
    
    def _set_placeholder_text(self, text: str):
        """Set placeholder text when image cannot be loaded."""
        self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)


class SequenceCardPageWidget(QFrame):
    """Widget representing a page of sequence cards."""
    
    def __init__(self, sequences: List[SequenceCardData], grid_dimensions, parent=None):
        super().__init__(parent)
        self.sequences = sequences
        self.grid_dimensions = grid_dimensions
        self._setup_ui()
        self._apply_styling()
    
    def _setup_ui(self):
        """Setup page UI with grid layout."""
        layout = QGridLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Add sequence cards to grid
        for i, sequence in enumerate(self.sequences):
            if i >= self.grid_dimensions.total_positions:
                break
                
            row = i // self.grid_dimensions.columns
            col = i % self.grid_dimensions.columns
            
            card_widget = SequenceCardWidget(sequence)
            layout.addWidget(card_widget, row, col)
        
        # Fill remaining positions with empty space
        for i in range(len(self.sequences), self.grid_dimensions.total_positions):
            row = i // self.grid_dimensions.columns
            col = i % self.grid_dimensions.columns
            
            spacer = QLabel()
            spacer.setMinimumSize(150, 100)
            layout.addWidget(spacer, row, col)
    
    def _apply_styling(self):
        """Apply page styling."""
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin: 10px;
            }
        """)


class SequenceCardContentComponent(QWidget):
    """Content component for displaying sequence cards."""
    
    sequences_displayed = pyqtSignal(int)  # Number of sequences displayed

    def __init__(
        self, 
        display_service: ISequenceCardDisplayService,
        cache_service: ISequenceCardCacheService,
        layout_service: ISequenceCardLayoutService,
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self.display_service = display_service
        self.cache_service = cache_service
        self.layout_service = layout_service
        
        self.current_sequences: List[SequenceCardData] = []
        self.current_column_count = 2
        
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self) -> None:
        """Setup content UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Content widget for scroll area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(15)
        
        # Initial empty state
        self._show_empty_state()
        
        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)
        
        self._apply_styling()

    def _apply_styling(self) -> None:
        """Apply content area styling."""
        self.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            
            QScrollBar:vertical {
                background: rgba(0,0,0,0.1);
                width: 8px;
                border-radius: 4px;
            }
            
            QScrollBar::handle:vertical {
                background: rgba(0,0,0,0.3);
                border-radius: 4px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: rgba(0,0,0,0.5);
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

    def _setup_connections(self) -> None:
        """Setup signal connections."""
        if hasattr(self.display_service, 'sequences_loaded'):
            self.display_service.sequences_loaded.connect(self._on_sequences_loaded)

    def _show_empty_state(self) -> None:
        """Show empty state message."""
        self._clear_content()
        
        empty_label = QLabel("No sequences to display.\nSelect a sequence length from the sidebar.")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                background: rgba(40, 40, 40, 0.3);
                border: 2px dashed rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 40px;
                margin: 20px;
                font-size: 14px;
                font-style: italic;
            }
        """)
        
        font = QFont()
        font.setPointSize(14)
        font.setItalic(True)
        empty_label.setFont(font)
        
        self.content_layout.addWidget(empty_label)

    def _clear_content(self) -> None:
        """Clear all content widgets."""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _on_sequences_loaded(self, sequences: List[SequenceCardData]) -> None:
        """Handle sequences loaded signal."""
        self.current_sequences = sequences
        self.refresh_display()

    def refresh_display(self) -> None:
        """Refresh the display with current sequences."""
        self._clear_content()
        
        if not self.current_sequences:
            self._show_empty_state()
            return
        
        try:
            # Group sequences by length and organize into pages
            self._display_sequences_in_pages()
            
            self.sequences_displayed.emit(len(self.current_sequences))
            
        except Exception as e:
            logger.error(f"Error refreshing display: {e}")
            self._show_error_state(str(e))

    def _display_sequences_in_pages(self) -> None:
        """Display sequences organized into pages."""
        if not self.current_sequences:
            return
        
        # Get grid dimensions for the sequence length
        sequence_length = self.current_sequences[0].length if self.current_sequences else 16
        grid_dims = self.layout_service.calculate_grid_dimensions(sequence_length)
        
        # Calculate how many sequences per page based on column count
        sequences_per_page = grid_dims.total_positions
        
        # Create pages
        page_count = 0
        for i in range(0, len(self.current_sequences), sequences_per_page):
            page_sequences = self.current_sequences[i:i + sequences_per_page]
            
            # Create page widget
            page_widget = SequenceCardPageWidget(page_sequences, grid_dims)
            
            # Create page layout with multiple columns if needed
            if page_count % self.current_column_count == 0:
                # Start new row of pages
                page_row_layout = QHBoxLayout()
                page_row_layout.setContentsMargins(0, 0, 0, 0)
                page_row_layout.setSpacing(10)
                
                # Add this row layout to main content
                page_row_widget = QWidget()
                page_row_widget.setLayout(page_row_layout)
                self.content_layout.addWidget(page_row_widget)
                
                # Store reference for adding more pages to this row
                self.current_page_row_layout = page_row_layout
            
            # Add page to current row
            self.current_page_row_layout.addWidget(page_widget)
            
            page_count += 1
            
            # If we've filled the current row, start a new one
            if page_count % self.current_column_count == 0:
                self.current_page_row_layout = None
        
        # Add stretch to push content to top
        self.content_layout.addStretch()

    def _show_error_state(self, error_message: str) -> None:
        """Show error state."""
        self._clear_content()
        
        error_label = QLabel(f"Error displaying sequences:\n{error_message}")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet("""
            QLabel {
                color: #e74c3c;
                background: rgba(231, 76, 60, 0.1);
                border: 2px solid #e74c3c;
                border-radius: 10px;
                padding: 20px;
                margin: 20px;
                font-size: 12px;
            }
        """)
        
        self.content_layout.addWidget(error_label)

    def set_column_count(self, column_count: int) -> None:
        """Set the number of columns for page display."""
        self.current_column_count = column_count
        self.refresh_display()

    def get_scroll_position(self) -> int:
        """Get current scroll position."""
        return self.scroll_area.verticalScrollBar().value()

    def set_scroll_position(self, position: int) -> None:
        """Set scroll position."""
        self.scroll_area.verticalScrollBar().setValue(position)
