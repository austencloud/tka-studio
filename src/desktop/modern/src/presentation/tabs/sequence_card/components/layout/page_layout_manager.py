"""
Page Layout Manager

Manages the layout and organization of sequence card pages.
"""

import logging
from typing import List, Optional

from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout
from PyQt6.QtCore import QCoreApplication

from core.interfaces.sequence_card_services import (
    SequenceCardData,
    ISequenceCardLayoutService,
)
from ..widgets.sequence_card_page_widget import SequenceCardPageWidget
from ..image_loading.image_loader import ImageLoader

logger = logging.getLogger(__name__)


class PageLayoutManager:
    """Manages the layout and organization of sequence card pages."""

    def __init__(
        self,
        layout_service: ISequenceCardLayoutService,
        content_layout: QVBoxLayout,
        image_loader: ImageLoader,
    ):
        self.layout_service = layout_service
        self.content_layout = content_layout
        self.image_loader = image_loader
        self.page_widgets: List[SequenceCardPageWidget] = []
        self.current_page_row_layout: Optional[QHBoxLayout] = None

    def display_sequences_in_pages(
        self, sequences: List[SequenceCardData], column_count: int
    ) -> List[SequenceCardPageWidget]:
        """Display sequences organized into pages."""
        if not sequences:
            logger.warning("No sequences to display")
            return []

        logger.info(f"Displaying {len(sequences)} sequences in pages")

        # Get grid dimensions for the sequence length
        sequence_length = sequences[0].length if sequences else 16
        grid_dims = self.layout_service.calculate_grid_dimensions(sequence_length)
        logger.info(
            f"Grid dimensions: {grid_dims.columns}x{grid_dims.rows} = {grid_dims.total_positions}"
        )

        # Calculate how many sequences per page based on column count
        sequences_per_page = grid_dims.total_positions

        # Create pages
        page_count = 0
        self.page_widgets = []  # Reset page widgets list

        for i in range(0, len(sequences), sequences_per_page):
            page_sequences = sequences[i : i + sequences_per_page]
            logger.info(
                f"Creating page {page_count + 1} with {len(page_sequences)} sequences"
            )

            # Create page widget with image loader and layout service
            page_widget = SequenceCardPageWidget(
                page_sequences, grid_dims, self.layout_service, self.image_loader
            )
            self.page_widgets.append(page_widget)
            logger.info(f"Page widget created: {page_widget}")
            logger.info(f"Page widget size: {page_widget.size()}")
            logger.info(f"Page widget visible: {page_widget.isVisible()}")

            # Create page layout with multiple columns if needed
            if page_count % column_count == 0:
                # Start new row of pages
                page_row_layout = QHBoxLayout()
                page_row_layout.setContentsMargins(0, 0, 0, 0)
                page_row_layout.setSpacing(10)

                # Add this row layout to main content
                page_row_widget = QWidget()
                page_row_widget.setLayout(page_row_layout)
                self.content_layout.addWidget(page_row_widget)
                logger.info(
                    f"Page row widget added to content layout. Content layout count: {self.content_layout.count()}"
                )

                # Make sure the row widget is visible
                page_row_widget.show()
                logger.info(
                    f"Page row widget shown. Visible: {page_row_widget.isVisible()}"
                )

                # Store reference for adding more pages to this row
                self.current_page_row_layout = page_row_layout

            # Add page to current row
            self.current_page_row_layout.addWidget(page_widget)
            logger.info(
                f"Page widget added to layout. Layout count: {self.current_page_row_layout.count()}"
            )

            # Make sure the page widget is visible
            page_widget.show()

            # Force layout updates to ensure visibility
            page_widget.updateGeometry()
            page_widget.repaint()

            # Force parent layout updates
            if self.current_page_row_layout and self.current_page_row_layout.parentWidget():
                self.current_page_row_layout.parentWidget().updateGeometry()

            logger.info(f"Page widget shown. Visible: {page_widget.isVisible()}")

            page_count += 1

            # If we've filled the current row, start a new one
            if page_count % column_count == 0:
                self.current_page_row_layout = None

        # Add stretch to push content to top
        self.content_layout.addStretch()

        # Force final layout updates for the entire content component
        logger.info("Forcing final layout updates...")

        # Process pending events to ensure layout changes are applied
        QCoreApplication.processEvents()

        logger.info(
            f"Final page layout state: {len(self.page_widgets)} pages created, layout_count={self.content_layout.count()}"
        )

        return self.page_widgets

    def display_page_structure_immediately(
        self, sequences: List[SequenceCardData], column_count: int
    ) -> List[SequenceCardPageWidget]:
        """Display page structure immediately with placeholder cards for instant UI response."""
        if not sequences:
            logger.warning("No sequences to display")
            return []

        logger.info(
            f"Displaying page structure immediately for {len(sequences)} sequences"
        )

        # Get grid dimensions for the sequence length
        sequence_length = sequences[0].length if sequences else 16
        grid_dims = self.layout_service.calculate_grid_dimensions(sequence_length)
        
        # Calculate how many sequences per page based on column count
        sequences_per_page = grid_dims.total_positions

        # Create pages with placeholder cards immediately
        page_count = 0
        self.page_widgets = []  # Reset page widgets list

        for i in range(0, len(sequences), sequences_per_page):
            page_sequences = sequences[i : i + sequences_per_page]
            
            # Create page widget with placeholders only (no image loading yet)
            page_widget = SequenceCardPageWidget(
                page_sequences, grid_dims, self.layout_service, None  # No image loader yet
            )
            self.page_widgets.append(page_widget)

            # Create page layout with multiple columns if needed
            if page_count % column_count == 0:
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
            page_widget.show()

            page_count += 1

            # If we've filled the current row, start a new one
            if page_count % column_count == 0:
                self.current_page_row_layout = None

        # Add stretch to push content to top
        self.content_layout.addStretch()

        # Show all placeholder cards immediately
        for page_widget in self.page_widgets:
            for card_widget in page_widget.card_widgets:
                card_widget.show_placeholder()

        # Process events to ensure immediate display
        QCoreApplication.processEvents()

        return self.page_widgets

    def assign_image_loaders(self):
        """Assign image loaders to all page widgets and cards."""
        for page_widget in self.page_widgets:
            page_widget.image_loader = self.image_loader
            for card_widget in page_widget.card_widgets:
                card_widget.set_image_loader(self.image_loader)
