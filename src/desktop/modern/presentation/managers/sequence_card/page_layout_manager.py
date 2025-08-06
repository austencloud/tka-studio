"""
Page Layout Manager

Manages the layout and organization of sequence card pages.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QCoreApplication, QSize
from PyQt6.QtWidgets import QHBoxLayout, QScrollArea, QVBoxLayout, QWidget

from desktop.modern.core.interfaces.sequence_card_services import (
    ISequenceCardCacheService,
    ISequenceCardLayoutService,
    SequenceCardData,
)
from desktop.modern.presentation.views.sequence_card.image_loader import ImageLoader
from desktop.modern.presentation.views.sequence_card.sequence_card_page_widget import (
    SequenceCardPageWidget,
)


logger = logging.getLogger(__name__)


class PageLayoutManager:
    """Manages the layout and organization of sequence card pages."""

    def __init__(
        self,
        layout_service: ISequenceCardLayoutService,
        content_layout: QVBoxLayout,
        image_loader: ImageLoader,
        cache_service: ISequenceCardCacheService | None = None,
    ):
        self.layout_service = layout_service
        self.content_layout = content_layout
        self.image_loader = image_loader
        self.cache_service = cache_service
        self.page_widgets: list[SequenceCardPageWidget] = []
        self.current_page_row_layout: QHBoxLayout | None = None

    def _get_scroll_area_width(self) -> int:
        """Get the available width of the scroll area for page sizing calculations."""
        # Find the scroll area by traversing up the widget hierarchy
        current_widget = self.content_layout.parentWidget()
        while current_widget:
            if isinstance(current_widget, QScrollArea):
                scroll_area_width = current_widget.width()

                # Account for scroll bar width if vertical scrollbar is visible
                if current_widget.verticalScrollBar().isVisible():
                    scroll_bar_width = current_widget.verticalScrollBar().width()
                    scroll_area_width -= scroll_bar_width

                return scroll_area_width
            current_widget = current_widget.parentWidget()

        # Fallback if no scroll area found
        logger.warning("Could not find scroll area, using default width")
        return 800

    def _calculate_optimal_page_size(self, column_count: int) -> QSize:
        """Calculate optimal page size based on available width and column count."""
        # Get available width
        scroll_area_width = self._get_scroll_area_width()

        # Use the layout service's calculate_page_size method
        optimal_width, optimal_height = self.layout_service.calculate_page_size(
            scroll_area_width, column_count
        )

        return QSize(optimal_width, optimal_height)

    def _scale_page_to_optimal_size(
        self, page_widget: SequenceCardPageWidget, column_count: int
    ) -> None:
        """Scale page widget to optimal size based on column count (legacy behavior)."""
        # Calculate optimal size
        optimal_size = self._calculate_optimal_page_size(column_count)

        # Get original size
        original_size = page_widget.size()

        # Calculate scale factor
        scale_factor = self.layout_service.calculate_scale_factor(
            (original_size.width(), original_size.height()),
            (optimal_size.width(), optimal_size.height()),
        )

        # Apply scaling
        new_width = int(original_size.width() * scale_factor)
        new_height = int(original_size.height() * scale_factor)
        page_widget.setFixedSize(new_width, new_height)
        page_widget.setProperty("scale_factor", scale_factor)

        logger.debug(
            f"Scaled page from {original_size.width()}x{original_size.height()} "
            f"to {new_width}x{new_height} (scale: {scale_factor:.3f})"
        )

    def display_sequences_in_pages(
        self, sequences: list[SequenceCardData], column_count: int
    ) -> list[SequenceCardPageWidget]:
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

            # Create page widget with image loader, cache service, and layout service
            page_widget = SequenceCardPageWidget(
                page_sequences,
                grid_dims,
                self.layout_service,
                self.image_loader,
                self.cache_service,
            )

            # CRITICAL: Scale page to optimal size based on column count (legacy behavior)
            self._scale_page_to_optimal_size(page_widget, column_count)

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
            if (
                self.current_page_row_layout
                and self.current_page_row_layout.parentWidget()
            ):
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
        self, sequences: list[SequenceCardData], column_count: int
    ) -> list[SequenceCardPageWidget]:
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
                page_sequences,
                grid_dims,
                self.layout_service,
                None,  # No image loader yet
                self.cache_service,  # But include cache service for future use
            )

            # CRITICAL: Scale page to optimal size based on column count (legacy behavior)
            self._scale_page_to_optimal_size(page_widget, column_count)

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
        """Assign image loaders and cache services to all page widgets and cards."""
        for page_widget in self.page_widgets:
            page_widget.image_loader = self.image_loader
            page_widget.cache_service = self.cache_service
            for card_widget in page_widget.card_widgets:
                card_widget.set_image_loader(self.image_loader)
                if self.cache_service:
                    card_widget.set_cache_service(self.cache_service)

    def clear_all_pages(self) -> None:
        """Clear all page widgets and reset internal state (legacy behavior)."""
        logger.debug(f"Clearing {len(self.page_widgets)} existing page widgets")

        # Clear page widgets from layout and delete them
        for page_widget in self.page_widgets:
            if page_widget and page_widget.parent():
                # Remove from parent layout
                parent_layout = page_widget.parent().layout()
                if parent_layout:
                    parent_layout.removeWidget(page_widget)

                # Set parent to None and schedule for deletion
                page_widget.setParent(None)
                page_widget.deleteLater()

        # Clear internal state
        self.page_widgets.clear()
        self.current_page_row_layout = None

        logger.debug("All page widgets cleared and internal state reset")
