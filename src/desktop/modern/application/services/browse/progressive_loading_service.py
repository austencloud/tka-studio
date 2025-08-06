"""
Progressive Loading Service - Incremental Sequence Loading

This service handles progressive loading of sequences with visual feedback,
ensuring the UI remains responsive during heavy operations.

Updated to work directly with SequenceData (no more SequenceRecord conversion).
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication

from application.services.browse.dictionary_data_manager import (
    DictionaryDataManager,
)
from desktop.modern.domain.models.browse_errors import DataLoadError
from desktop.modern.domain.models.browse_models import FilterType
from desktop.modern.domain.models.sequence_data import SequenceData


logger = logging.getLogger(__name__)


class ProgressiveLoadingService(QObject):
    """
    Service that handles progressive loading of sequences with UI responsiveness.

    Instead of loading all sequences at once, this service breaks the process
    into chunks and allows the UI to update between chunks.

    Simplified: Now works directly with SequenceData, no conversion needed.
    """

    # Signals
    loading_started = pyqtSignal(int)  # total_count
    sequences_chunk_loaded = pyqtSignal(list)  # List[SequenceData] chunk
    loading_progress = pyqtSignal(int, int)  # current, total
    loading_completed = pyqtSignal(list)  # List[SequenceData] final_result
    loading_cancelled = pyqtSignal()

    def __init__(self, dictionary_manager: DictionaryDataManager):
        super().__init__()
        self.dictionary_manager = dictionary_manager
        self._loading_timer = QTimer()
        self._loading_timer.timeout.connect(self._process_next_chunk)

        # Loading state
        self._is_loading = False
        self._pending_sequences: list[SequenceData] = []
        self._processed_sequences: list[SequenceData] = []
        self._chunk_size = 10  # Process 10 sequences at a time
        self._current_chunk_index = 0

    def start_progressive_loading(
        self, filter_type: FilterType, filter_value: Any, chunk_size: int = 10
    ) -> None:
        """
        Start progressive loading of sequences based on filter.

        Args:
            filter_type: The type of filter to apply
            filter_value: The filter value
            chunk_size: Number of sequences to process per chunk
        """
        if self._is_loading:
            self.cancel_loading()

        self._chunk_size = chunk_size
        self._is_loading = True
        self._processed_sequences.clear()
        self._current_chunk_index = 0

        try:
            # Get filtered sequences directly (no conversion needed)
            self._pending_sequences = self._get_filtered_sequences(
                filter_type, filter_value
            )

            total_count = len(self._pending_sequences)
            logger.info(f"🚀 Starting progressive loading: {total_count} sequences")

            # Emit started signal
            self.loading_started.emit(total_count)

            if total_count == 0:
                self.loading_completed.emit([])
                return

            # Start processing timer
            self._loading_timer.start(50)  # Process chunk every 50ms

        except Exception as e:
            logger.error(f"❌ Failed to start progressive loading: {e}")
            self._finish_loading_with_error(str(e))

    def cancel_loading(self) -> None:
        """Cancel the current loading operation."""
        if self._is_loading:
            self._loading_timer.stop()
            self._is_loading = False
            self._pending_sequences.clear()
            logger.info("❌ Progressive loading cancelled")
            self.loading_cancelled.emit()

    def _process_next_chunk(self) -> None:
        """Process the next chunk of sequences."""
        if not self._is_loading or not self._pending_sequences:
            self._finish_loading()
            return

        # Calculate chunk boundaries
        start_idx = self._current_chunk_index * self._chunk_size
        end_idx = min(start_idx + self._chunk_size, len(self._pending_sequences))

        if start_idx >= len(self._pending_sequences):
            self._finish_loading()
            return

        # Process current chunk - no conversion needed since we already have SequenceData
        chunk_sequences = self._pending_sequences[start_idx:end_idx]
        self._processed_sequences.extend(chunk_sequences)

        # Emit chunk loaded
        self.sequences_chunk_loaded.emit(chunk_sequences)

        # Update progress
        current_progress = end_idx
        total_progress = len(self._pending_sequences)
        self.loading_progress.emit(current_progress, total_progress)

        logger.debug(
            f"📦 Processed chunk {self._current_chunk_index + 1}: "
            f"{len(chunk_sequences)} sequences ({current_progress}/{total_progress})"
        )

        # Allow UI to update
        QApplication.processEvents()

        # Move to next chunk
        self._current_chunk_index += 1

        # Check if we're done
        if end_idx >= len(self._pending_sequences):
            self._finish_loading()

    def _finish_loading(self) -> None:
        """Finish the loading process."""
        self._loading_timer.stop()
        self._is_loading = False

        total_loaded = len(self._processed_sequences)
        logger.info(f"✅ Progressive loading completed: {total_loaded} sequences")

        # Emit completion signal
        self.loading_completed.emit(self._processed_sequences.copy())

    def _finish_loading_with_error(self, error_message: str) -> None:
        """Finish loading with an error."""
        self._loading_timer.stop()
        self._is_loading = False
        self._pending_sequences.clear()

        # Could emit an error signal here if needed
        logger.error(f"❌ Progressive loading failed: {error_message}")
        self.loading_completed.emit([])

    def _get_filtered_sequences(
        self, filter_type: FilterType, filter_value: Any
    ) -> list[SequenceData]:
        """Get filtered sequences from dictionary manager."""
        logger.info(
            f"🔍 [PROGRESSIVE] Getting filtered sequences: {filter_type.value} = {filter_value} (type: {type(filter_value)})"
        )

        try:
            sequences = []

            if filter_type == FilterType.STARTING_LETTER:
                sequences = self._apply_starting_letter_filter(filter_value)
            elif filter_type == FilterType.LENGTH:
                sequences = self._apply_length_filter(filter_value)
            elif filter_type == FilterType.DIFFICULTY:
                sequences = self._apply_difficulty_filter(filter_value)
            elif filter_type == FilterType.AUTHOR:
                sequences = self._apply_author_filter(filter_value)
            elif filter_type == FilterType.GRID_MODE:
                sequences = self._apply_grid_mode_filter(filter_value)
            elif filter_type == FilterType.FAVORITES:
                logger.info("⭐ [PROGRESSIVE] Getting favorite sequences")
                sequences = self.dictionary_manager.get_favorite_sequences()
            elif filter_type == FilterType.RECENT:
                logger.info("🔥 [PROGRESSIVE] Getting recent sequences")
                sequences = self.dictionary_manager.get_recent_sequences()
            else:
                logger.info("📊 [PROGRESSIVE] Getting all sequences (default)")
                sequences = self.dictionary_manager.get_all_sequences()

            # Ensure we always return a list, never None
            if sequences is None:
                logger.warning(
                    f"⚠️ [PROGRESSIVE] Dictionary manager returned None for {filter_type.value}"
                )
                sequences = []

            logger.info(f"📊 [PROGRESSIVE] Filter returned {len(sequences)} sequences")
            return sequences

        except Exception as e:
            logger.error(f"❌ [PROGRESSIVE] Error filtering sequences: {e}")
            raise DataLoadError(f"Failed to filter sequences: {e}") from e

    def _apply_starting_letter_filter(self, filter_value) -> list[SequenceData]:
        """Apply starting letter filter logic."""
        if isinstance(filter_value, str):
            if "-" in filter_value and len(filter_value) == 3:
                start_letter, end_letter = filter_value.split("-")
                letters = [
                    chr(i) for i in range(ord(start_letter), ord(end_letter) + 1)
                ]
                logger.info(
                    f"📝 [PROGRESSIVE] Letter range {filter_value} -> {letters}"
                )
                return self.dictionary_manager.get_sequences_by_starting_letters(
                    letters
                )
            if filter_value == "All Letters":
                return self.dictionary_manager.get_all_sequences()
            return self.dictionary_manager.get_sequences_by_starting_letter(
                filter_value
            )
        if isinstance(filter_value, list):
            return self.dictionary_manager.get_sequences_by_starting_letters(
                filter_value
            )
        logger.warning(
            f"⚠️ [PROGRESSIVE] Unexpected starting letter filter value: {filter_value}"
        )
        return []

    def _apply_length_filter(self, filter_value) -> list[SequenceData]:
        """Apply length filter logic."""
        if isinstance(filter_value, str):
            if filter_value == "All":
                return self.dictionary_manager.get_all_sequences()
            try:
                length_value = int(filter_value)
                logger.info(
                    f"📏 [PROGRESSIVE] Converting length '{filter_value}' to {length_value}"
                )
                return self.dictionary_manager.get_sequences_by_length(length_value)
            except ValueError:
                logger.warning(f"⚠️ [PROGRESSIVE] Invalid length value: {filter_value}")
                return []
        elif isinstance(filter_value, int):
            return self.dictionary_manager.get_sequences_by_length(filter_value)
        else:
            logger.warning(
                f"⚠️ [PROGRESSIVE] Unexpected length filter value: {filter_value}"
            )
            return []

    def _apply_difficulty_filter(self, filter_value) -> list[SequenceData]:
        """Apply difficulty filter logic."""
        if filter_value == "All" or filter_value == "All Levels":
            return self.dictionary_manager.get_all_sequences()
        logger.info(f"📊 [PROGRESSIVE] Filtering by difficulty: {filter_value}")
        return self.dictionary_manager.get_sequences_by_difficulty(filter_value)

    def _apply_author_filter(self, filter_value) -> list[SequenceData]:
        """Apply author filter logic."""
        if filter_value == "All Authors":
            return self.dictionary_manager.get_all_sequences()
        return self.dictionary_manager.get_sequences_by_author(filter_value)

    def _apply_grid_mode_filter(self, filter_value) -> list[SequenceData]:
        """Apply grid mode filter logic."""
        if filter_value == "All" or filter_value == "All Styles":
            return self.dictionary_manager.get_all_sequences()
        return self.dictionary_manager.get_sequences_by_grid_mode(filter_value)

    def is_loading(self) -> bool:
        """Check if currently loading."""
        return self._is_loading
