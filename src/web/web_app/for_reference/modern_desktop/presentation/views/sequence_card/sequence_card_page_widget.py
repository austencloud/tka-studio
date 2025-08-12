"""
Sequence Card Page Widget

Widget representing a page of sequence cards with letter-sized dimensions.
"""

from __future__ import annotations

import logging
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QWidget

from desktop.modern.core.interfaces.sequence_card_services import (
    GridDimensions,
    ISequenceCardCacheService,
    ISequenceCardLayoutService,
    SequenceCardData,
)

from .image_loader import ImageLoader
from .sequence_card_widget import SequenceCardWidget


logger = logging.getLogger(__name__)


class SequenceCardPageWidget(QFrame):
    """Widget representing a page of sequence cards with letter-sized dimensions."""

    def __init__(
        self,
        sequences: list[SequenceCardData],
        grid_dimensions: GridDimensions,
        layout_service: ISequenceCardLayoutService,
        image_loader: ImageLoader | None = None,
        cache_service: ISequenceCardCacheService | None = None,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self.sequences: list[SequenceCardData] = sequences
        self.grid_dimensions: GridDimensions = grid_dimensions
        self.layout_service: ISequenceCardLayoutService = layout_service
        self.image_loader: ImageLoader | None = image_loader
        self.cache_service: ISequenceCardCacheService | None = cache_service
        self.card_widgets: list[SequenceCardWidget] = []
        self.setFrameStyle(QFrame.Shape.Box)  # Visual page boundary
        self.setObjectName("printableSequenceCardPage")  # Match legacy naming
        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self) -> None:
        """Setup page UI with letter-sized layout and proper margins."""
        # Get letter-sized page dimensions and set initial fixed size
        page_size = self.layout_service.get_letter_page_size_px()
        self.setFixedSize(page_size)  # Initial size - will be scaled later

        # Setup grid layout with responsive margins
        self.grid_layout = QGridLayout(self)
        self._update_layout_margins()
        self.grid_layout.setSpacing(5)  # Legacy spacing
        self.grid_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        # Add sequence cards to grid
        for i, sequence in enumerate(self.sequences):
            if i >= self.grid_dimensions.total_positions:
                break

            row = i // self.grid_dimensions.columns
            col = i % self.grid_dimensions.columns

            card_widget = SequenceCardWidget(
                sequence, self.image_loader, self.cache_service
            )
            self.card_widgets.append(card_widget)
            self.grid_layout.addWidget(card_widget, row, col)

        # Fill remaining positions with empty space
        for i in range(len(self.sequences), self.grid_dimensions.total_positions):
            row = i // self.grid_dimensions.columns
            col = i % self.grid_dimensions.columns

            spacer = QLabel()
            # FIXED: Remove minimum size for spacers too (legacy behavior)
            # spacer.setMinimumSize(150, 100)  # REMOVED
            self.grid_layout.addWidget(spacer, row, col)

        # Set appropriate minimum sizes for cards based on available space
        self._update_card_minimum_sizes()

    def _update_layout_margins(self) -> None:
        """Update layout margins based on current page size (responsive behavior)."""
        current_size = self.size()

        # Calculate proportional margins based on current size vs original letter size
        original_size = self.layout_service.get_letter_page_size_px()
        original_content_rect = self.layout_service.get_content_rect_px()

        # Calculate scale factors
        scale_x = current_size.width() / original_size.width()
        scale_y = current_size.height() / original_size.height()

        # Scale margins proportionally
        left_margin = int(original_content_rect.left() * scale_x)
        top_margin = int(original_content_rect.top() * scale_y)
        right_margin = int(
            (original_size.width() - original_content_rect.right()) * scale_x
        )
        bottom_margin = int(
            (original_size.height() - original_content_rect.bottom()) * scale_y
        )

        # Apply scaled margins
        self.grid_layout.setContentsMargins(
            left_margin, top_margin, right_margin, bottom_margin
        )

        logger.debug(
            f"Updated margins for size {current_size.width()}x{current_size.height()}: "
            f"({left_margin}, {top_margin}, {right_margin}, {bottom_margin})"
        )

        # Update card minimum sizes based on new layout
        self._update_card_minimum_sizes()

    def _update_card_minimum_sizes(self) -> None:
        """Update card minimum sizes based on available cell space."""
        if not hasattr(self, "card_widgets") or not self.card_widgets:
            return

        # Calculate available space for each grid cell (LEGACY APPROACH)
        current_size = self.size()
        margins = self.grid_layout.contentsMargins()

        # Calculate content area (available space for grid)
        available_width = current_size.width() - margins.left() - margins.right()
        available_height = current_size.height() - margins.top() - margins.bottom()

        # Grid dimensions (2x3 for 16-beat sequences)
        grid_cols = self.grid_dimensions.columns
        grid_rows = self.grid_dimensions.rows

        # LEGACY APPROACH: Calculate cell size directly from content area
        # Legacy formula: cell_width = content_rect.width() // cols (no spacing subtraction)
        cell_width = available_width // grid_cols
        cell_height = available_height // grid_rows

        # LEGACY APPROACH: Cards fill the entire cell (no arbitrary percentage reduction)
        # The grid layout naturally provides proper spacing and proportions
        target_card_width = max(60, cell_width)  # Minimum 60px for readability
        target_card_height = max(45, cell_height)  # Minimum 45px for readability

        # Set card sizes to fill their grid cells (legacy behavior)
        for card_widget in self.card_widgets:
            card_widget.setMinimumSize(target_card_width, target_card_height)
            card_widget.setMaximumSize(target_card_width, target_card_height)

        logger.debug(
            f"LEGACY SIZING: Cards {target_card_width}x{target_card_height} "
            f"(cell: {cell_width}x{cell_height}, grid: {grid_cols}x{grid_rows})"
        )

    def resizeEvent(self, event) -> None:
        """Handle resize events to update layout margins (responsive behavior)."""
        super().resizeEvent(event)
        if hasattr(self, "grid_layout"):
            self._update_layout_margins()

    def _apply_styling(self) -> None:
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
