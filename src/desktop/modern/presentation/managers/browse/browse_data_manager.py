"""
Browse Data Manager - Simplified Data Operations for Browse Tab

This class is responsible for:
- Applying filters using the dictionary data manager
- Providing data access methods for the browse tab
- Managing sequence ID to word mappings

Simplified: No more conversion between data formats since dictionary manager
returns SequenceData directly.
"""

from __future__ import annotations

import logging
from pathlib import Path

from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.views.browse.errors import DataLoadError, FilterError
from desktop.modern.presentation.views.browse.models import FilterType


logger = logging.getLogger(__name__)


class BrowseDataManager:
    """
    Simplified data manager for the Browse tab.

    No longer does data conversion - dictionary manager returns SequenceData directly.
    Focuses on filtering operations and ID mappings.
    """

    def __init__(self, data_dir: Path, dictionary_manager=None):
        """
        Initialize the browse data manager.

        Args:
            data_dir: Directory containing dictionary data
            dictionary_manager: Optional injected dictionary manager
        """
        if dictionary_manager:
            self.dictionary_manager = dictionary_manager
        else:
            # Fallback to direct instantiation if not injected
            from desktop.modern.application.services.browse.dictionary_data_manager import (
                DictionaryDataManager,
            )

            self.dictionary_manager = DictionaryDataManager(data_dir)

        # Mapping from sequence UUID to word (for quick lookup)
        self.sequence_id_to_word: dict[str, str] = {}

        # Connect to dictionary manager signals
        self.dictionary_manager.data_loaded.connect(self._on_data_loaded)
        self.dictionary_manager.loading_progress.connect(self._on_loading_progress)

    def load_all_sequences(self) -> None:
        """Load all sequences from the dictionary."""
        try:
            self.dictionary_manager.load_all_sequences()
        except Exception as e:
            raise DataLoadError(f"Failed to load sequences: {e}") from e

    def refresh_data(self) -> None:
        """Refresh sequence data from disk."""
        try:
            self.dictionary_manager.refresh_data()
            self.sequence_id_to_word.clear()
        except Exception as e:
            raise DataLoadError(f"Failed to refresh data: {e}") from e

    def apply_filter(self, filter_type: FilterType, filter_value) -> list[SequenceData]:
        """
        Apply filter using the dictionary data manager.

        Args:
            filter_type: Type of filter to apply
            filter_value: Value to filter by

        Returns:
            List of filtered SequenceData objects
        """
        logger.info(
            f"🔍 [DATA_MANAGER] Applying filter: {filter_type.value} = {filter_value} (type: {type(filter_value)})"
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
                logger.info("⭐ Getting favorite sequences")
                sequences = self.dictionary_manager.get_favorite_sequences()
            elif filter_type == FilterType.RECENT:
                logger.info("🔥 Getting recent sequences")
                sequences = self.dictionary_manager.get_recent_sequences()
            else:
                logger.info("📊 Getting all sequences (default)")
                sequences = self.dictionary_manager.get_all_sequences()

            # Update ID mappings for the returned sequences
            self._update_id_mappings(sequences)

            logger.info(f"📊 [DATA_MANAGER] Filter returned {len(sequences)} sequences")

            # Debug: Log first few sequence words to verify real data
            if sequences:
                sample_words = [seq.word for seq in sequences[:3] if seq.word]
                logger.info(f"📊 [DATA_MANAGER] Sample sequences: {sample_words}")
            else:
                logger.warning("📊 [DATA_MANAGER] No sequences returned!")

            return sequences

        except Exception as e:
            raise FilterError(f"Failed to apply filter {filter_type.value}: {e}") from e

    def _apply_starting_letter_filter(self, filter_value) -> list[SequenceData]:
        """Apply starting letter filter logic."""
        if isinstance(filter_value, str):
            # Handle letter ranges like "A-D"
            if "-" in filter_value and len(filter_value) == 3:
                start_letter, end_letter = filter_value.split("-")
                letters = [
                    chr(i) for i in range(ord(start_letter), ord(end_letter) + 1)
                ]
                logger.info(f"📝 Letter range {filter_value} -> {letters}")
                return self.dictionary_manager.get_sequences_by_starting_letters(
                    letters
                )
            if filter_value == "All Letters":
                return self.dictionary_manager.get_all_sequences()
            # Single letter
            return self.dictionary_manager.get_sequences_by_starting_letter(
                filter_value
            )
        if isinstance(filter_value, list):
            return self.dictionary_manager.get_sequences_by_starting_letters(
                filter_value
            )
        return self.dictionary_manager.get_all_sequences()

    def _apply_length_filter(self, filter_value) -> list[SequenceData]:
        """Apply length filter logic."""
        if isinstance(filter_value, str):
            if filter_value == "All":
                return self.dictionary_manager.get_all_sequences()
            try:
                length_value = int(filter_value)
                logger.info(f"📏 Converting length '{filter_value}' to {length_value}")
                return self.dictionary_manager.get_sequences_by_length(length_value)
            except ValueError:
                logger.warning(f"⚠️ Invalid length value: {filter_value}")
                return []
        elif isinstance(filter_value, int):
            return self.dictionary_manager.get_sequences_by_length(filter_value)
        else:
            return self.dictionary_manager.get_all_sequences()

    def _apply_difficulty_filter(self, filter_value) -> list[SequenceData]:
        """Apply difficulty filter logic."""
        if filter_value in {"All", "All Levels"}:
            return self.dictionary_manager.get_all_sequences()
        logger.info(f"📊 Filtering by difficulty: {filter_value}")
        return self.dictionary_manager.get_sequences_by_difficulty(filter_value)

    def _apply_author_filter(self, filter_value) -> list[SequenceData]:
        """Apply author filter logic."""
        if filter_value == "All Authors":
            return self.dictionary_manager.get_all_sequences()
        return self.dictionary_manager.get_sequences_by_author(filter_value)

    def _apply_grid_mode_filter(self, filter_value) -> list[SequenceData]:
        """Apply grid mode filter logic."""
        if filter_value in {"All", "All Styles"}:
            return self.dictionary_manager.get_all_sequences()
        return self.dictionary_manager.get_sequences_by_grid_mode(filter_value)

    def _update_id_mappings(self, sequences: list[SequenceData]) -> None:
        """Update ID to word mappings for given sequences."""
        for sequence in sequences:
            if sequence.word:
                self.sequence_id_to_word[sequence.id] = sequence.word

    def get_sequence_data(self, sequence_id: str) -> SequenceData | None:
        """
        Get sequence data by ID.

        Args:
            sequence_id: Deterministic ID of the sequence

        Returns:
            SequenceData object if found, None otherwise
        """
        logger.info(f"🔍 [DATA_MANAGER] Looking for sequence with ID: {sequence_id}")

        # Since we now use deterministic IDs, we can search directly by ID
        # Get all sequences from dictionary manager
        all_sequences = self.dictionary_manager.get_all_sequences()

        logger.info(
            f"🔍 [DATA_MANAGER] Searching through {len(all_sequences)} sequences"
        )

        # DEBUG: Log the first few sequence IDs for comparison
        logger.info("🔍 [DATA_MANAGER] First 3 sequence IDs in data:")
        for i, sequence in enumerate(all_sequences[:3]):
            logger.info(f"   {i}: {sequence.id}")
        logger.info(f"🔍 [DATA_MANAGER] Requested ID: {sequence_id}")
        logger.info(f"🔍 [DATA_MANAGER] ID length: {len(sequence_id)} vs expected ~64")

        # Find the sequence by ID directly
        for i, sequence in enumerate(all_sequences):
            logger.debug(
                f"🔍 [DATA_MANAGER] Sequence {i}: id={sequence.id[:16]}..., word={sequence.word}"
            )
            if sequence.id == sequence_id:
                logger.info(
                    f"✅ [DATA_MANAGER] Found matching sequence: {sequence.word}"
                )
                return sequence

        logger.error(
            f"❌ [DATA_MANAGER] No sequence found for sequence_id: {sequence_id}"
        )
        logger.info("🔍 [DATA_MANAGER] Available sequence IDs:")
        for i, sequence in enumerate(all_sequences[:5]):  # Show first 5 for debugging
            logger.info(f"🔍 [DATA_MANAGER]   {i}: {sequence.id} -> {sequence.word}")

        return None

    def get_loading_errors(self) -> list[str]:
        """Get any loading errors from the dictionary manager."""
        return self.dictionary_manager.get_loading_errors()

    def get_all_sequences(self) -> list[SequenceData]:
        """
        Get all sequences as SequenceData objects.

        Returns:
            List of SequenceData objects directly from dictionary manager
        """
        sequences = self.dictionary_manager.get_all_sequences()
        self._update_id_mappings(sequences)
        return sequences

    def _on_data_loaded(self, count: int) -> None:
        """Handle data loading completion."""
        # Check for loading errors
        errors = self.dictionary_manager.get_loading_errors()
        if errors:
            logger.warning(f"⚠️  {len(errors)} loading errors occurred")
            for error in errors[:5]:  # Show first 5 errors
                logger.warning(f"   - {error}")

    def _on_loading_progress(self, message: str, current: int, total: int) -> None:
        """Handle loading progress updates."""
        if current == total:
            pass  # Loading complete
