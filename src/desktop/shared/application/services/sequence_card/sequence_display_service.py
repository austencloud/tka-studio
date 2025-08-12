"""
Sequence Card Display Service Implementation

Coordinates display operations with batch processing and state management.
Framework-agnostic service layer.
"""

import logging
from collections.abc import Callable
from pathlib import Path

from desktop.modern.core.interfaces.sequence_card_services import (
    DisplayState,
    ISequenceCardCacheService,
    ISequenceCardDataService,
    ISequenceCardDisplayService,
    ISequenceCardLayoutService,
    SequenceCardData,
)

logger = logging.getLogger(__name__)


class SequenceCardDisplayService(ISequenceCardDisplayService):
    """Implementation of sequence card display coordination."""

    def __init__(
        self,
        data_service: ISequenceCardDataService,
        cache_service: ISequenceCardCacheService,
        layout_service: ISequenceCardLayoutService,
        dictionary_path: Path | None = None,
    ):
        self.data_service = data_service
        self.cache_service = cache_service
        self.layout_service = layout_service

        # Get dictionary path
        if dictionary_path:
            self.dictionary_path = dictionary_path
        else:
            # Use modern path service
            from .path_service import SequenceCardPathService

            path_service = SequenceCardPathService()
            self.dictionary_path = path_service.get_dictionary_path()

        self.display_state = DisplayState()
        self.progress_callback: Callable[[int, int], None] | None = None
        self.sequences_loaded_callback: (
            Callable[[list[SequenceCardData]], None] | None
        ) = None
        self.loading_state_callback: Callable[[bool], None] | None = None
        self._cancel_requested = False
        self._current_sequences: list[SequenceCardData] = []

        # Batch processing settings
        self.batch_size = 20
        self.batch_delay_ms = 50  # Delay between batches for UI responsiveness

    def display_sequences(self, length: int, column_count: int) -> None:
        """Display sequences of specified length."""
        self._cancel_requested = False
        self.display_state.is_loading = True
        self.display_state.current_length = length
        self.display_state.current_column_count = column_count

        # Notify loading state change
        if self.loading_state_callback:
            self.loading_state_callback(True)

        logger.info(
            f"Starting display of length {length} sequences with {column_count} columns"
        )

        try:
            # Get sequences for specified length
            sequences = self.data_service.get_sequences_by_length(
                self.dictionary_path, length
            )
            self.display_state.total_sequences = len(sequences)
            self.display_state.processed_sequences = 0
            self._current_sequences = sequences

            if not sequences:
                logger.warning(f"No sequences found for length {length}")
                self.display_state.is_loading = False
                if self.loading_state_callback:
                    self.loading_state_callback(False)
                # Still notify with empty list
                if self.sequences_loaded_callback:
                    self.sequences_loaded_callback([])
                return

            logger.info(f"Found {len(sequences)} sequences for length {length}")

            # Process in batches
            self._process_sequences_in_batches(sequences)

        except Exception as e:
            logger.error(f"Error displaying sequences: {e}")
            self.display_state.is_loading = False
            if self.loading_state_callback:
                self.loading_state_callback(False)

    def get_display_state(self) -> DisplayState:
        """Get current display state."""
        # Update cache stats
        try:
            cache_stats = self.cache_service.get_cache_stats()
            self.display_state.cache_hit_ratio = cache_stats.hit_ratio
        except Exception as e:
            logger.warning(f"Error getting cache stats: {e}")
            self.display_state.cache_hit_ratio = 0.0
        return self.display_state

    def cancel_current_operation(self) -> None:
        """Cancel current loading operation."""
        self._cancel_requested = True
        self.display_state.is_loading = False
        logger.info("Display operation cancelled")

    def set_progress_callback(self, callback: Callable[[int, int], None]) -> None:
        """Set progress update callback."""
        self.progress_callback = callback

    def set_sequences_loaded_callback(
        self, callback: Callable[[list[SequenceCardData]], None]
    ) -> None:
        """Set callback for when sequences are loaded."""
        self.sequences_loaded_callback = callback

    def set_loading_state_callback(self, callback: Callable[[bool], None]) -> None:
        """Set callback for loading state changes."""
        self.loading_state_callback = callback

    def get_current_sequences(self) -> list[SequenceCardData]:
        """Get currently loaded sequences."""
        return self._current_sequences

    def _process_sequences_in_batches(self, sequences: list[SequenceCardData]) -> None:
        """Process sequences with legacy-style responsiveness."""
        if self._cancel_requested:
            return

        # Process sequences immediately with frequent progress updates (legacy style)
        for i, sequence in enumerate(sequences):
            if self._cancel_requested:
                return

            # Try to get from cache first
            cached_image = self.cache_service.get_cached_image(sequence.path)
            if not cached_image:
                # Load and cache image
                try:
                    with open(sequence.path, "rb") as f:
                        image_data = f.read()
                    self.cache_service.cache_image(sequence.path, image_data)
                except Exception as e:
                    logger.warning(f"Error loading image {sequence.path}: {e}")
                    continue

            self.display_state.processed_sequences += 1

            # Update progress more frequently (legacy style)
            if self.progress_callback:
                self.progress_callback(
                    self.display_state.processed_sequences,
                    self.display_state.total_sequences,
                )

            # Legacy-style frequent progress updates every 10 sequences
            if i % 10 == 0 and i > 0:
                logger.debug(f"Processed {i}/{len(sequences)} sequences")

        self.display_state.is_loading = False

        # Notify loading state change
        if self.loading_state_callback:
            self.loading_state_callback(False)

        # Notify sequences loaded
        if self.sequences_loaded_callback:
            self.sequences_loaded_callback(self._current_sequences)

        logger.info(
            f"Display complete: {self.display_state.processed_sequences} sequences processed"
        )
