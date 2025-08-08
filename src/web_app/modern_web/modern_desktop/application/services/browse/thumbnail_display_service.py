"""
Thumbnail Display Service

Handles thumbnail creation, positioning, and display logic for the sequence browser.
Manages the coordination between thumbnail factory and grid layout positioning.
"""

from __future__ import annotations

from collections.abc import Callable
import logging

from PyQt6.QtWidgets import QApplication, QWidget

from desktop.modern.application.services.browse.grid_layout_service import (
    GridLayoutService,
)
from desktop.modern.application.services.browse.thumbnail_factory_service import (
    ThumbnailFactoryService,
)
from desktop.modern.domain.models.sequence_data import SequenceData


logger = logging.getLogger(__name__)


class ThumbnailDisplayService:
    """
    Service for managing thumbnail display operations.

    Handles:
    - Thumbnail creation and positioning
    - Section-based grouping and display
    - Progressive thumbnail addition
    - Click event coordination
    """

    def __init__(
        self,
        grid_layout_service: GridLayoutService,
        thumbnail_factory: ThumbnailFactoryService,
        thumbnail_width: int = 150,
    ):
        """
        Initialize the thumbnail display service.

        Args:
            grid_layout_service: Service for managing grid layout
            thumbnail_factory: Factory for creating thumbnails
            thumbnail_width: Width for thumbnails
        """
        self.grid_layout_service = grid_layout_service
        self.thumbnail_factory = thumbnail_factory
        self.thumbnail_width = thumbnail_width

        # Callback for thumbnail clicks
        self.thumbnail_click_callback: Callable[[str], None] | None = None

    def set_thumbnail_click_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for thumbnail click events."""
        self.thumbnail_click_callback = callback

    def set_thumbnail_width(self, width: int) -> None:
        """Update the thumbnail width."""
        self.thumbnail_width = width

    def display_sequences_with_stable_layout(
        self, sequences: list[SequenceData], sort_method: str
    ) -> None:
        """
        Display sequences with stable layout (all at once).

        Args:
            sequences: List of sequences to display
            sort_method: Method for sorting and grouping sequences
        """
        logger.info(
            f"🎨 [THUMBNAIL_DISPLAY] Displaying {len(sequences)} sequences with stable layout"
        )

        # Clear existing layout
        self.grid_layout_service.clear_grid()

        # Group sequences by section
        sections = self._group_sequences_by_section(sequences, sort_method)

        # Display all sections
        self._display_sections(sections, sort_method)

    def add_sequences_progressively(
        self, chunk_sequences: list[SequenceData], sort_method: str
    ) -> None:
        """
        Add sequences progressively to the layout.

        Args:
            chunk_sequences: Chunk of sequences to add
            sort_method: Method for sorting and grouping sequences
        """
        if not chunk_sequences:
            return

        logger.info(
            f"📦 [THUMBNAIL_DISPLAY] Adding {len(chunk_sequences)} sequences progressively"
        )

        # Group sequences by section
        sections_to_add = self._group_sequences_by_section(chunk_sequences, sort_method)

        # Get current layout state
        current_row = self.grid_layout_service.get_row_count()

        # Add each section progressively
        for section_name, section_sequences in sections_to_add.items():
            # Add section header
            current_row = self.grid_layout_service.add_section_header(
                section_name, current_row
            )
            current_row += 1

            # Add thumbnails for this section
            column_index = 0

            for sequence in section_sequences:
                # Create thumbnail
                thumbnail = self._create_thumbnail(sequence, sort_method)

                # Add to grid layout
                self.grid_layout_service.add_thumbnail_to_grid(
                    thumbnail, current_row, column_index
                )

                # Show immediately
                thumbnail.show()

                # Move to next position
                column_index = (column_index + 1) % 3  # 3 columns
                if column_index == 0:
                    current_row += 1

                # Process events to keep UI responsive
                QApplication.processEvents()

    def _display_sections(
        self, sections: dict[str, list[SequenceData]], sort_method: str
    ) -> None:
        """Display all sections in the grid."""
        current_row = 0
        thumbnail_count = 0

        for section_name, section_sequences in sections.items():
            # Add section header
            current_row = self.grid_layout_service.add_section_header(
                section_name, current_row
            )
            current_row += 1

            # Create thumbnails for this section
            for sequence in section_sequences:
                thumbnail = self._create_thumbnail(sequence, sort_method)

                # Calculate position in 3-column grid
                col = thumbnail_count % 3
                if col == 0 and thumbnail_count > 0:
                    current_row += 1

                self.grid_layout_service.add_thumbnail_to_grid(
                    thumbnail, current_row, col
                )
                thumbnail_count += 1

    def _create_thumbnail(self, sequence: SequenceData, sort_method: str) -> QWidget:
        """Create a thumbnail widget for a sequence."""
        thumbnail = self.thumbnail_factory.create_thumbnail(
            sequence, self.thumbnail_width, sort_method
        )

        # Make clickable if callback is set
        if self.thumbnail_click_callback:
            thumbnail.mousePressEvent = (
                lambda event, seq_id=sequence.id: self.thumbnail_click_callback(seq_id)
            )

        return thumbnail

    def _group_sequences_by_section(
        self, sequences: list[SequenceData], sort_method: str
    ) -> dict[str, list[SequenceData]]:
        """
        Group sequences by section based on sort method.

        Args:
            sequences: List of sequences to group
            sort_method: Method for grouping (alphabetical, difficulty, etc.)

        Returns:
            Dictionary mapping section names to sequence lists
        """
        sections: dict[str, list[SequenceData]] = {}

        for sequence in sequences:
            section_name = self._get_section_name(sequence, sort_method)

            if section_name not in sections:
                sections[section_name] = []

            sections[section_name].append(sequence)

        # Sort sections by name
        return dict(sorted(sections.items()))

    def _get_section_name(self, sequence: SequenceData, sort_method: str) -> str:
        """
        Get the section name for a sequence based on sort method.

        Args:
            sequence: The sequence to categorize
            sort_method: The sorting method

        Returns:
            Section name for the sequence
        """
        if sort_method == "difficulty":
            return sequence.difficulty or "Unknown Difficulty"
        if sort_method == "length":
            return f"Length {sequence.length or 'Unknown'}"
        if sort_method == "alphabetical":
            if sequence.word:
                first_letter = sequence.word[0].upper()
                return f"Starting with {first_letter}"
            return "Unknown"
        return "All Sequences"

    def add_empty_state(self) -> None:
        """Add empty state to the display."""
        self.grid_layout_service.add_empty_state()

    def add_loading_fallback(self) -> None:
        """Add loading fallback to the display."""
        self.grid_layout_service.add_loading_fallback()

    def clear_display(self) -> None:
        """Clear all thumbnails from the display."""
        self.grid_layout_service.clear_grid()
