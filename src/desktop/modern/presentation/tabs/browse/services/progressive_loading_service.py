"""
Progressive Loading Service - Incremental Sequence Loading

This service handles progressive loading of sequences with visual feedback,
ensuring the UI remains responsive during heavy operations.
"""

from typing import Any, List

from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.tabs.browse.models import FilterType
from desktop.modern.presentation.tabs.browse.services.modern_dictionary_data_manager import (
    ModernDictionaryDataManager,
    SequenceRecord,
)
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication


class ProgressiveLoadingService(QObject):
    """
    Service that handles progressive loading of sequences with UI responsiveness.

    Instead of loading all sequences at once, this service breaks the process
    into chunks and allows the UI to update between chunks.
    """

    # Signals
    loading_started = pyqtSignal(int)  # total_count
    sequences_chunk_loaded = pyqtSignal(list)  # List[SequenceData] chunk
    loading_progress = pyqtSignal(int, int)  # current, total
    loading_completed = pyqtSignal(list)  # List[SequenceData] final_result
    loading_cancelled = pyqtSignal()

    def __init__(self, dictionary_manager: ModernDictionaryDataManager):
        super().__init__()
        self.dictionary_manager = dictionary_manager
        self._loading_timer = QTimer()
        self._loading_timer.timeout.connect(self._process_next_chunk)

        # Loading state
        self._is_loading = False
        self._pending_records: List[SequenceRecord] = []
        self._processed_sequences: List[SequenceData] = []
        self._chunk_size = 10  # Process 10 sequences at a time
        self._sequence_id_mapping = {}  # For ID mapping
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
        self._sequence_id_mapping.clear()
        self._current_chunk_index = 0

        # Get filtered records (this is still fast since records are cached)
        self._pending_records = self._get_filtered_records(filter_type, filter_value)

        total_count = len(self._pending_records)

        # Emit started signal
        self.loading_started.emit(total_count)

        if total_count == 0:
            self.loading_completed.emit([])
            return

        # Start processing timer
        self._loading_timer.start(50)  # Process chunk every 50ms

    def cancel_loading(self) -> None:
        """Cancel the current loading operation."""
        if self._is_loading:
            self._loading_timer.stop()
            self._is_loading = False
            self._pending_records.clear()
            print("❌ Progressive loading cancelled")
            self.loading_cancelled.emit()

    def _process_next_chunk(self) -> None:
        """Process the next chunk of sequences."""
        if not self._is_loading or not self._pending_records:
            self._finish_loading()
            return

        # Calculate chunk boundaries
        start_idx = self._current_chunk_index * self._chunk_size
        end_idx = min(start_idx + self._chunk_size, len(self._pending_records))

        if start_idx >= len(self._pending_records):
            self._finish_loading()
            return

        # Process current chunk
        chunk_records = self._pending_records[start_idx:end_idx]
        chunk_sequences = []

        for record in chunk_records:
            # Convert record to SequenceData
            sequence_data = self._convert_record_to_sequence_data(record)
            chunk_sequences.append(sequence_data)
            self._processed_sequences.append(sequence_data)

        # Emit chunk loaded
        self.sequences_chunk_loaded.emit(chunk_sequences)

        # Update progress
        current_progress = end_idx
        total_progress = len(self._pending_records)
        self.loading_progress.emit(current_progress, total_progress)

        # Allow UI to update
        QApplication.processEvents()

        # Move to next chunk
        self._current_chunk_index += 1

        # Check if we're done
        if end_idx >= len(self._pending_records):
            self._finish_loading()

    def _finish_loading(self) -> None:
        """Finish the loading process."""
        self._loading_timer.stop()
        self._is_loading = False

        total_loaded = len(self._processed_sequences)

        # Emit completion signal
        self.loading_completed.emit(self._processed_sequences.copy())

    def _get_filtered_records(
        self, filter_type: FilterType, filter_value: Any
    ) -> List[SequenceRecord]:
        """Get filtered records from dictionary manager."""
        # This uses the existing dictionary manager filtering logic
        if filter_type == FilterType.STARTING_LETTER:
            if isinstance(filter_value, str):
                if "-" in filter_value and len(filter_value) == 3:
                    start_letter, end_letter = filter_value.split("-")
                    letters = [
                        chr(i) for i in range(ord(start_letter), ord(end_letter) + 1)
                    ]
                    return self.dictionary_manager.get_records_by_starting_letters(
                        letters
                    )
                elif filter_value == "All Letters":
                    return self.dictionary_manager.get_all_records()
                else:
                    return self.dictionary_manager.get_records_by_starting_letter(
                        filter_value
                    )
            elif isinstance(filter_value, list):
                return self.dictionary_manager.get_records_by_starting_letters(
                    filter_value
                )

        elif filter_type == FilterType.LENGTH:
            if isinstance(filter_value, int):
                return self.dictionary_manager.get_records_by_length(filter_value)
            elif filter_value == "All":
                return self.dictionary_manager.get_all_records()

        elif filter_type == FilterType.DIFFICULTY:
            if filter_value == "All":
                return self.dictionary_manager.get_all_records()
            else:
                return self.dictionary_manager.get_records_by_difficulty(filter_value)

        elif filter_type == FilterType.AUTHOR:
            if filter_value == "All Authors":
                return self.dictionary_manager.get_all_records()
            else:
                return self.dictionary_manager.get_records_by_author(filter_value)

        elif filter_type == FilterType.GRID_MODE:
            if filter_value == "All":
                return self.dictionary_manager.get_all_records()
            else:
                return self.dictionary_manager.get_records_by_grid_mode(filter_value)

        elif filter_type == FilterType.FAVORITES:
            return self.dictionary_manager.get_favorite_records()

        elif filter_type == FilterType.RECENT:
            return self.dictionary_manager.get_recent_records()

        else:
            return self.dictionary_manager.get_all_records()

    def _convert_record_to_sequence_data(self, record: SequenceRecord) -> SequenceData:
        """Convert SequenceRecord to SequenceData."""
        from desktop.modern.domain.models.sequence_data import SequenceData

        sequence_data = SequenceData(
            word=record.word,
            thumbnails=record.thumbnails,
            author=record.author,
            level=record.level,
            sequence_length=record.sequence_length,
            date_added=record.date_added,
            grid_mode=record.grid_mode,
            prop_type=record.prop_type,
            is_favorite=record.is_favorite,
            is_circular=record.is_circular,
            starting_position=record.starting_position,
            difficulty_level=record.difficulty_level,
            tags=record.tags,
        )

        # Store mapping for quick lookup
        self._sequence_id_mapping[sequence_data.id] = record.word

        return sequence_data

    def get_sequence_id_mapping(self) -> dict:
        """Get the current sequence ID to word mapping."""
        return self._sequence_id_mapping.copy()

    def is_loading(self) -> bool:
        """Check if currently loading."""
        return self._is_loading
