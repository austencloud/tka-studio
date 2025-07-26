"""
Browse Data Manager - Handles data conversion and sequence operations for Browse Tab

This class is responsible for:
- Converting between SequenceRecord and SequenceData formats
- Managing sequence ID to word mappings
- Applying filters using the dictionary data manager
- Providing data access methods for the browse tab
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.tabs.browse.models import FilterType
from desktop.modern.presentation.tabs.browse.services.modern_dictionary_data_manager import (
    ModernDictionaryDataManager,
)

logger = logging.getLogger(__name__)


class BrowseDataManager:
    """
    Manages data operations for the Browse tab.
    
    Handles conversion between data formats, filtering operations,
    and maintains sequence mappings for efficient lookups.
    """

    def __init__(self, data_dir: Path):
        """
        Initialize the browse data manager.
        
        Args:
            data_dir: Directory containing dictionary data
        """
        self.dictionary_manager = ModernDictionaryDataManager(data_dir)
        
        # Mapping from sequence UUID to word (for quick lookup)
        self.sequence_id_to_word: Dict[str, str] = {}
        
        # Connect to dictionary manager signals
        self.dictionary_manager.data_loaded.connect(self._on_data_loaded)
        self.dictionary_manager.loading_progress.connect(self._on_loading_progress)

    def load_all_sequences(self) -> None:
        """Load all sequences from the dictionary."""
        self.dictionary_manager.load_all_sequences()

    def refresh_data(self) -> None:
        """Refresh sequence data from disk."""
        self.dictionary_manager.refresh_data()
        self.sequence_id_to_word.clear()

    def apply_filter(self, filter_type: FilterType, filter_value) -> List[SequenceData]:
        """
        Apply filter using the dictionary data manager.
        
        Args:
            filter_type: Type of filter to apply
            filter_value: Value to filter by
            
        Returns:
            List of filtered SequenceData objects
        """
        records = []

        if filter_type == FilterType.STARTING_LETTER:
            if isinstance(filter_value, str):
                # Handle letter ranges like "A-D"
                if "-" in filter_value and len(filter_value) == 3:
                    start_letter, end_letter = filter_value.split("-")
                    letters = [
                        chr(i) for i in range(ord(start_letter), ord(end_letter) + 1)
                    ]
                    records = self.dictionary_manager.get_records_by_starting_letters(
                        letters
                    )
                elif filter_value == "All Letters":
                    records = self.dictionary_manager.get_all_records()
                else:
                    # Single letter
                    records = self.dictionary_manager.get_records_by_starting_letter(
                        filter_value
                    )
            elif isinstance(filter_value, list):
                records = self.dictionary_manager.get_records_by_starting_letters(
                    filter_value
                )

        elif filter_type == FilterType.LENGTH:
            if isinstance(filter_value, int):
                records = self.dictionary_manager.get_records_by_length(filter_value)
            elif filter_value == "All":
                records = self.dictionary_manager.get_all_records()

        elif filter_type == FilterType.DIFFICULTY:
            if filter_value == "All":
                records = self.dictionary_manager.get_all_records()
            else:
                records = self.dictionary_manager.get_records_by_difficulty(
                    filter_value
                )

        elif filter_type == FilterType.AUTHOR:
            if filter_value == "All Authors":
                records = self.dictionary_manager.get_all_records()
            else:
                records = self.dictionary_manager.get_records_by_author(filter_value)

        elif filter_type == FilterType.GRID_MODE:
            if filter_value == "All":
                records = self.dictionary_manager.get_all_records()
            else:
                records = self.dictionary_manager.get_records_by_grid_mode(filter_value)

        elif filter_type == FilterType.FAVORITES:
            records = self.dictionary_manager.get_favorite_records()

        elif filter_type == FilterType.RECENT:
            records = self.dictionary_manager.get_recent_records()

        else:
            records = self.dictionary_manager.get_all_records()

        # Convert SequenceRecord to SequenceData format for compatibility
        return self._convert_records_to_sequence_data(records)

    def get_sequence_data(self, sequence_id: str) -> Optional[SequenceData]:
        """
        Get sequence data by ID.
        
        Args:
            sequence_id: UUID of the sequence
            
        Returns:
            SequenceData object if found, None otherwise
        """
        # Get the word from the mapping
        word = self.sequence_id_to_word.get(sequence_id)
        if not word:
            logger.error(f"❌ No word mapping found for sequence_id: {sequence_id}")
            return None

        # Get all records from dictionary manager
        all_records = self.dictionary_manager.get_all_records()

        # Find the record by word
        target_record = None
        for record in all_records:
            if record.word == word:
                target_record = record
                break

        if not target_record:
            logger.error(f"❌ No record found for word: {word}")
            return None

        # Convert SequenceRecord to SequenceData
        sequence_data = SequenceData(
            id=sequence_id,  # Use the original UUID
            word=target_record.word,
            thumbnails=target_record.thumbnails,
            author=target_record.author,
            level=target_record.level,
            sequence_length=target_record.sequence_length,
            date_added=target_record.date_added,
            grid_mode=target_record.grid_mode,
            prop_type=target_record.prop_type,
            is_favorite=target_record.is_favorite,
            is_circular=target_record.is_circular,
            starting_position=target_record.starting_position,
            difficulty_level=target_record.difficulty_level,
            tags=target_record.tags,
        )

        return sequence_data

    def get_loading_errors(self) -> List[str]:
        """Get any loading errors from the dictionary manager."""
        return self.dictionary_manager.get_loading_errors()

    def _convert_records_to_sequence_data(self, records) -> List[SequenceData]:
        """Convert SequenceRecord objects to SequenceData format."""
        sequence_data_list = []
        for record in records:
            # Create SequenceData object
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

            # Store mapping from UUID to word for quick lookup
            self.sequence_id_to_word[sequence_data.id] = record.word

            sequence_data_list.append(sequence_data)

        return sequence_data_list

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
