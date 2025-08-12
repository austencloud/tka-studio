"""
Sequence Display Coordinator Service

Service for coordinating the display of sequences using other services.
"""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtWidgets import QApplication

from desktop.modern.core.interfaces.browse_services import (
    ILayoutManager,
    ILoadingStateManager,
    INavigationHandler,
    ISequenceSorter,
    IThumbnailFactory,
)
from desktop.modern.domain.models.sequence_data import SequenceData


class SequenceDisplayCoordinatorService:
    """Coordinates sequence display using various services."""

    def __init__(
        self,
        thumbnail_factory: IThumbnailFactory,
        layout_manager: ILayoutManager,
        loading_state_manager: ILoadingStateManager,
        sequence_sorter: ISequenceSorter,
        navigation_handler: INavigationHandler,
        thumbnail_width: int = 150,
    ):
        """Initialize with service dependencies."""
        self.thumbnail_factory = thumbnail_factory
        self.layout_manager = layout_manager
        self.loading_state_manager = loading_state_manager
        self.sequence_sorter = sequence_sorter
        self.navigation_handler = navigation_handler
        self.thumbnail_width = thumbnail_width

        # Callback for when thumbnails are clicked
        self.thumbnail_click_callback: Callable[[str], None] | None = None

        # Track progressive loading state
        self._added_sections: set = set()
        self._last_row_used: int = -1

    def set_thumbnail_click_callback(self, callback: Callable[[str], None]) -> None:
        """Set the callback for when thumbnails are clicked."""
        self.thumbnail_click_callback = callback

    def display_sequences_with_stable_layout(
        self, sequences: list[SequenceData], sort_method: str
    ) -> None:
        """Display sequences using stable layout with sections."""
        # Sort sequences
        sorted_sequences = self.sequence_sorter.sort_sequences(sequences, sort_method)

        # Group into sections
        sections = self.sequence_sorter.group_sequences_into_sections(
            sorted_sequences, sort_method
        )

        # Update navigation sidebar
        section_names = list(sections.keys())
        self.navigation_handler.update_navigation_sections(section_names, sort_method)

        # Clear and rebuild with stable layout
        self.layout_manager.clear_grid()

        current_row = 0
        thumbnail_count = 0

        for section_name, section_sequences in sections.items():
            # Add section header
            current_row = self.layout_manager.add_section_header(
                section_name, current_row
            )
            current_row += 1

            # Create thumbnails for this section
            for sequence in section_sequences:
                thumbnail = self.thumbnail_factory.create_thumbnail(
                    sequence, self.thumbnail_width, sort_method
                )

                # Make clickable
                if self.thumbnail_click_callback:
                    thumbnail.mousePressEvent = (
                        lambda event, seq_id=sequence.id: self.thumbnail_click_callback(
                            seq_id
                        )
                    )

                # Calculate position in 3-column grid
                col = thumbnail_count % 3
                if col == 0 and thumbnail_count > 0:
                    current_row += 1

                self.layout_manager.add_thumbnail_to_grid(thumbnail, current_row, col)
                thumbnail_count += 1

            # Start fresh row for next section
            if thumbnail_count % 3 != 0:
                current_row += 1
                thumbnail_count = ((thumbnail_count // 3) + 1) * 3

        # Add stretch to bottom
        self.layout_manager.set_row_stretch(self.layout_manager.get_row_count(), 1)

    def add_sequences_progressively(
        self, sequences: list[SequenceData], sort_method: str
    ) -> None:
        """Add sequences using true progressive loading approach with proper headers."""
        if not sequences:
            return

        # Sort the new sequences to maintain proper order
        sorted_sequences = self.sequence_sorter.sort_sequences(sequences, sort_method)

        # Group sequences by section
        sections = self.sequence_sorter.group_sequences_into_sections(
            sorted_sequences, sort_method
        )

        # Get current layout state
        current_row = self._get_next_available_row()
        current_col = self._get_current_column_position(current_row)

        # Add each section progressively
        for section_name, section_sequences in sections.items():
            # Check if this section already exists
            if not self._section_exists(section_name):
                # Start new row for header if we're not at column 0
                if current_col > 0:
                    current_row += 1
                    current_col = 0

                # Add section header
                current_row = self.layout_manager.add_section_header(
                    section_name, current_row
                )
                current_row += 1
                current_col = 0

                # Track that this section now exists
                self._mark_section_as_added(section_name)

            # Add thumbnails for this section
            for sequence in section_sequences:
                thumbnail = self.thumbnail_factory.create_thumbnail(
                    sequence, self.thumbnail_width, sort_method
                )

                # Make clickable
                if self.thumbnail_click_callback:
                    thumbnail.mousePressEvent = (
                        lambda event, seq_id=sequence.id: self.thumbnail_click_callback(
                            seq_id
                        )
                    )

                # Add to grid layout at current position
                self.layout_manager.add_thumbnail_to_grid(
                    thumbnail, current_row, current_col
                )

                # Show immediately
                thumbnail.show()

                # Move to next position
                current_col += 1
                if current_col >= 3:  # 3 columns
                    current_col = 0
                    current_row += 1

                # Process events to keep UI responsive
                QApplication.processEvents()


    def initialize_progressive_layout(self, sort_method: str) -> None:
        """Initialize the layout system for progressive loading."""
        self.layout_manager.clear_grid()
        self._reset_progressive_state()

    def finalize_progressive_layout(
        self, all_sequences: list[SequenceData], sort_method: str
    ) -> None:
        """Finalize the layout after progressive loading is complete."""
        if not all_sequences:
            return

        print(f"🎯 Finalizing layout with {len(all_sequences)} sequences")
        self.display_sequences_with_stable_layout(all_sequences, sort_method)

    # === Progressive Loading Helper Methods ===

    def _get_next_available_row(self) -> int:
        """Get the next available row for adding content."""
        # Get current row count from layout manager
        current_rows = (
            self.layout_manager.get_row_count()
            if hasattr(self.layout_manager, "get_row_count")
            else 0
        )
        return max(current_rows, self._last_row_used + 1)

    def _get_current_column_position(self, row: int) -> int:
        """Get the current column position for the given row."""
        # Count existing items in the current row
        if hasattr(self.layout_manager, "get_items_in_row"):
            return self.layout_manager.get_items_in_row(row) % 3
        return 0

    def _section_exists(self, section_name: str) -> bool:
        """Check if a section header has already been added."""
        return section_name in self._added_sections

    def _mark_section_as_added(self, section_name: str) -> None:
        """Mark a section as having been added."""
        self._added_sections.add(section_name)

    def _reset_progressive_state(self) -> None:
        """Reset progressive loading state for a fresh start."""
        self._added_sections.clear()
        self._last_row_used = -1

    def show_empty_state(self) -> None:
        """Show empty state when no sequences are found."""
        self.loading_state_manager.show_empty_state()

    def show_loading_fallback(self) -> None:
        """Show loading fallback when progressive loading is unavailable."""
        self.loading_state_manager.show_loading_fallback()

    def update_thumbnail_width(self, new_width: int) -> None:
        """Update the thumbnail width for future thumbnail creation."""
        self.thumbnail_width = new_width
