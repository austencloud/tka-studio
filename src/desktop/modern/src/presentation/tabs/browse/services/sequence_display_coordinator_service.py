"""
Sequence Display Coordinator Service

Service for coordinating the display of sequences using other services.
"""

from typing import List, Optional, Callable

from PyQt6.QtWidgets import QApplication, QWidget

from core.interfaces.browse_services import (
    IThumbnailFactory,
    ILayoutManager,
    ILoadingStateManager,
    ISequenceSorter,
    INavigationHandler
)
from domain.models.sequence_data import SequenceData


class SequenceDisplayCoordinatorService:
    """Coordinates sequence display using various services."""

    def __init__(
        self,
        thumbnail_factory: IThumbnailFactory,
        layout_manager: ILayoutManager,
        loading_state_manager: ILoadingStateManager,
        sequence_sorter: ISequenceSorter,
        navigation_handler: INavigationHandler,
        thumbnail_width: int = 150
    ):
        """Initialize with service dependencies."""
        self.thumbnail_factory = thumbnail_factory
        self.layout_manager = layout_manager
        self.loading_state_manager = loading_state_manager
        self.sequence_sorter = sequence_sorter
        self.navigation_handler = navigation_handler
        self.thumbnail_width = thumbnail_width
        
        # Callback for when thumbnails are clicked
        self.thumbnail_click_callback: Optional[Callable[[str], None]] = None

    def set_thumbnail_click_callback(self, callback: Callable[[str], None]) -> None:
        """Set the callback for when thumbnails are clicked."""
        self.thumbnail_click_callback = callback

    def display_sequences_with_stable_layout(
        self, 
        sequences: List[SequenceData], 
        sort_method: str
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
            current_row = self.layout_manager.add_section_header(section_name, current_row)
            current_row += 1

            # Create thumbnails for this section
            for sequence in section_sequences:
                thumbnail = self.thumbnail_factory.create_thumbnail(
                    sequence, self.thumbnail_width, sort_method
                )

                # Make clickable
                if self.thumbnail_click_callback:
                    thumbnail.mousePressEvent = (
                        lambda event, seq_id=sequence.id: self.thumbnail_click_callback(seq_id)
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
        self, 
        sequences: List[SequenceData], 
        sort_method: str
    ) -> None:
        """Add sequences using progressive loading approach."""
        if not sequences:
            return

        # Create thumbnails for the new sequences
        for i, sequence in enumerate(sequences):
            thumbnail = self.thumbnail_factory.create_thumbnail(
                sequence, self.thumbnail_width, sort_method
            )

            # Make clickable
            if self.thumbnail_click_callback:
                thumbnail.mousePressEvent = (
                    lambda event, seq_id=sequence.id: self.thumbnail_click_callback(seq_id)
                )

            # Add to grid layout (simple approach for progressive loading)
            row = i // 3  # 3 columns
            col = i % 3
            self.layout_manager.add_thumbnail_to_grid(thumbnail, row, col)

        # Process events to keep UI responsive
        QApplication.processEvents()

        print(f"🖼️ Added {len(sequences)} sequences progressively")

    def initialize_progressive_layout(self, sort_method: str) -> None:
        """Initialize the layout system for progressive loading."""
        self.layout_manager.clear_grid()
        print(f"🎨 Layout initialized for {sort_method} sorting")

    def finalize_progressive_layout(
        self, 
        all_sequences: List[SequenceData], 
        sort_method: str
    ) -> None:
        """Finalize the layout after progressive loading is complete."""
        if not all_sequences:
            return

        print(f"🎯 Finalizing layout with {len(all_sequences)} sequences")
        self.display_sequences_with_stable_layout(all_sequences, sort_method)

    def show_empty_state(self) -> None:
        """Show empty state when no sequences are found."""
        self.loading_state_manager.show_empty_state()

    def show_loading_fallback(self) -> None:
        """Show loading fallback when progressive loading is unavailable."""
        self.loading_state_manager.show_loading_fallback()

    def update_thumbnail_width(self, new_width: int) -> None:
        """Update the thumbnail width for future thumbnail creation."""
        self.thumbnail_width = new_width
        print(f"🔧 Updated thumbnail width to {new_width}px")
