"""
Sequence Card Page Widget

Widget representing a page of sequence cards with letter-sized dimensions.
"""

import logging
from typing import List, Optional

from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel
from PyQt6.QtCore import Qt

from core.interfaces.sequence_card_services import (
    SequenceCardData,
    ISequenceCardLayoutService,
)
from ..image_loading.image_loader import ImageLoader
from .sequence_card_widget import SequenceCardWidget

logger = logging.getLogger(__name__)


class SequenceCardPageWidget(QFrame):
    """Widget representing a page of sequence cards with letter-sized dimensions."""

    def __init__(
        self,
        sequences: List[SequenceCardData],
        grid_dimensions,
        layout_service: ISequenceCardLayoutService,
        image_loader: Optional[ImageLoader] = None,
        parent=None,
    ):
        super().__init__(parent)
        self.sequences = sequences
        self.grid_dimensions = grid_dimensions
        self.layout_service = layout_service
        self.image_loader = image_loader
        self.card_widgets = []
        self.setFrameStyle(QFrame.Shape.Box)  # Visual page boundary
        self.setObjectName("printableSequenceCardPage")  # Match legacy naming
        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self):
        """Setup page UI with letter-sized layout and proper margins."""
        # Get letter-sized page dimensions and set fixed size
        page_size = self.layout_service.get_letter_page_size_px()
        self.setFixedSize(page_size)  # Exact legacy behavior

        # Get content rectangle with proper margins
        content_rect = self.layout_service.get_content_rect_px()

        # Setup grid layout with exact legacy margins
        layout = QGridLayout(self)
        layout.setContentsMargins(
            content_rect.left(),
            content_rect.top(),
            page_size.width() - content_rect.right(),
            page_size.height() - content_rect.bottom(),
        )
        layout.setSpacing(5)  # Legacy spacing
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Add sequence cards to grid
        for i, sequence in enumerate(self.sequences):
            if i >= self.grid_dimensions.total_positions:
                break

            row = i // self.grid_dimensions.columns
            col = i % self.grid_dimensions.columns

            card_widget = SequenceCardWidget(sequence, self.image_loader)
            self.card_widgets.append(card_widget)
            layout.addWidget(card_widget, row, col)

        # Fill remaining positions with empty space
        for i in range(len(self.sequences), self.grid_dimensions.total_positions):
            row = i // self.grid_dimensions.columns
            col = i % self.grid_dimensions.columns

            spacer = QLabel()
            spacer.setMinimumSize(150, 100)
            layout.addWidget(spacer, row, col)

    def load_visible_images(self):
        """Trigger loading of images for all cards in this page."""
        for card_widget in self.card_widgets:
            card_widget.load_image_async()

    def _apply_styling(self):
        """Apply letter-sized page styling to match legacy system."""
        self.setStyleSheet(
            """
            QFrame#printableSequenceCardPage {
                background: white;
                border: 2px solid #ccc;
                border-radius: 4px;
                margin: 5px;
                /* Letter-sized page appearance */
            }

            QFrame#printableSequenceCardPage:hover {
                border-color: #007acc;
            }
        """
        )
