"""
Option Picker Data Service

Pure service for handling option picker data management.
Extracted from OptionPicker to follow single responsibility principle.

This service handles:
- Beat data loading and caching
- Option refresh logic
- Data format conversions (legacy/modern)
- Beat data lookup by option ID

No UI dependencies, completely testable in isolation.
"""

import logging
from typing import List, Dict, Any, Optional

from core.interfaces.option_picker_services import (
    IOptionPickerDataService,
)
from domain.models.core_models import BeatData, SequenceData

logger = logging.getLogger(__name__)


class OptionPickerDataService(IOptionPickerDataService):
    """
    Pure service for option picker data management.

    Handles all data operations without any UI concerns.
    Provides clean interface for beat data operations.
    """

    def __init__(self, beat_loader: Any):
        """
        Initialize the data service.

        Args:
            beat_loader: Beat data loader instance
        """
        self.beat_loader = beat_loader
        self._cached_options: List[BeatData] = []

    def load_beat_options(self) -> List[BeatData]:
        """
        Load initial beat options.

        Returns:
            List of available beat data options
        """
        try:
            if not self.beat_loader:
                logger.warning("Beat loader not available")
                return []

            options = self.beat_loader.refresh_options()
            self._cached_options = options

            logger.debug(f"Loaded {len(options)} beat options")
            return options

        except Exception as e:
            logger.error(f"Error loading beat options: {e}")
            return []

    def refresh_options(self) -> List[BeatData]:
        """
        Refresh beat options.

        Returns:
            Updated list of beat data options
        """
        try:
            if not self.beat_loader:
                logger.warning("Beat loader not available")
                return self._cached_options

            options = self.beat_loader.refresh_options()
            self._cached_options = options

            logger.debug(f"Refreshed {len(options)} beat options")
            return options

        except Exception as e:
            logger.error(f"Error refreshing beat options: {e}")
            return self._cached_options

    def refresh_from_sequence_data(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[BeatData]:
        """
        Refresh options based on legacy sequence data.

        Args:
            sequence_data: Legacy sequence data format

        Returns:
            Updated list of beat data options
        """
        try:
            if not self.beat_loader:
                logger.warning("Beat loader not available")
                return self._cached_options

            # Use beat loader's method for handling legacy sequence data
            if hasattr(self.beat_loader, "load_motion_combinations"):
                options = self.beat_loader.load_motion_combinations(sequence_data)
            elif hasattr(self.beat_loader, "refresh_options_from_sequence"):
                options = self.beat_loader.refresh_options_from_sequence(sequence_data)
            else:
                logger.warning("Beat loader doesn't support sequence data refresh")
                options = self.refresh_options()

            self._cached_options = options

            logger.debug(f"Refreshed {len(options)} beat options from sequence data")
            return options

        except Exception as e:
            logger.error(f"Error refreshing from sequence data: {e}")
            return self._cached_options

    def refresh_from_sequence(self, sequence: SequenceData) -> List[BeatData]:
        """
        Refresh options based on modern sequence data.

        Args:
            sequence: Modern sequence data

        Returns:
            Updated list of beat data options
        """
        try:
            if not self.beat_loader:
                logger.warning("Beat loader not available")
                return self._cached_options

            # Use beat loader's method for handling modern sequence data
            if hasattr(self.beat_loader, "refresh_options_from_modern_sequence"):
                options = self.beat_loader.refresh_options_from_modern_sequence(
                    sequence
                )
            else:
                logger.warning("Beat loader doesn't support modern sequence refresh")
                options = self.refresh_options()

            self._cached_options = options

            logger.debug(f"Refreshed {len(options)} beat options from modern sequence")
            return options

        except Exception as e:
            logger.error(f"Error refreshing from modern sequence: {e}")
            return self._cached_options

    def get_beat_data_for_option(self, option_id: str) -> Optional[BeatData]:
        """
        Get beat data for a specific option ID.

        Args:
            option_id: Option identifier (e.g., 'beat_J')

        Returns:
            BeatData if found, None otherwise
        """
        try:
            if not option_id:
                logger.warning("Empty option ID provided")
                return None

            # Extract letter from option_id (e.g., "beat_J" -> "J")
            if option_id.startswith("beat_"):
                target_letter = option_id[5:]  # Remove "beat_" prefix

                # Search through current beat options for matching letter
                current_options = self.get_current_options()
                for beat_data in current_options:
                    if beat_data.letter == target_letter:
                        logger.debug(
                            f"Found beat data for option {option_id}: {beat_data.letter}"
                        )
                        return beat_data

                logger.debug(
                    f"No beat data found for option {option_id} (letter: {target_letter})"
                )
                return None
            else:
                logger.warning(f"Invalid option ID format: {option_id}")
                return None

        except Exception as e:
            logger.error(f"Error getting beat data for option {option_id}: {e}")
            return None

    def get_current_options(self) -> List[BeatData]:
        """
        Get currently loaded beat options.

        Returns:
            Current list of beat data options
        """
        try:
            # Try to get fresh options from beat loader
            if self.beat_loader and hasattr(self.beat_loader, "get_beat_options"):
                fresh_options = self.beat_loader.get_beat_options()
                if fresh_options:
                    self._cached_options = fresh_options
                    return fresh_options

            # Fall back to cached options
            return self._cached_options

        except Exception as e:
            logger.error(f"Error getting current options: {e}")
            return self._cached_options

    def search_options(self, search_term: str) -> List[BeatData]:
        """
        Search beat options by letter or other criteria.

        Args:
            search_term: Term to search for

        Returns:
            Filtered list of beat data options
        """
        try:
            if not search_term:
                return self.get_current_options()

            current_options = self.get_current_options()
            search_term_lower = search_term.lower()

            filtered_options = []
            for beat_data in current_options:
                # Search by letter
                if beat_data.letter and beat_data.letter.lower().startswith(
                    search_term_lower
                ):
                    filtered_options.append(beat_data)
                # Could add more search criteria here (e.g., by motion type)

            logger.debug(
                f"Found {len(filtered_options)} options matching '{search_term}'"
            )
            return filtered_options

        except Exception as e:
            logger.error(f"Error searching options: {e}")
            return self.get_current_options()

    def get_options_by_letter(self, letter: str) -> Optional[BeatData]:
        """
        Get beat data by letter.

        Args:
            letter: Letter to search for

        Returns:
            BeatData if found, None otherwise
        """
        try:
            current_options = self.get_current_options()
            for beat_data in current_options:
                if beat_data.letter == letter:
                    return beat_data
            return None

        except Exception as e:
            logger.error(f"Error getting options by letter {letter}: {e}")
            return None

    def get_data_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about current data.

        Returns:
            Dictionary with data statistics
        """
        try:
            current_options = self.get_current_options()

            letters = [opt.letter for opt in current_options if opt.letter]
            unique_letters = set(letters)

            return {
                "total_options": len(current_options),
                "unique_letters": len(unique_letters),
                "letters": sorted(unique_letters),
                "has_beat_loader": self.beat_loader is not None,
                "cached_options_count": len(self._cached_options),
            }

        except Exception as e:
            logger.error(f"Error getting data statistics: {e}")
            return {
                "total_options": 0,
                "unique_letters": 0,
                "letters": [],
                "has_beat_loader": False,
                "cached_options_count": 0,
                "error": str(e),
            }

    def clear_cache(self) -> None:
        """Clear cached options."""
        self._cached_options = []
        logger.debug("Cleared cached options")

    def validate_beat_loader(self) -> bool:
        """
        Validate that beat loader is properly configured.

        Returns:
            True if beat loader is valid
        """
        if not self.beat_loader:
            return False

        # Check for required methods
        required_methods = ["refresh_options"]
        for method_name in required_methods:
            if not hasattr(self.beat_loader, method_name):
                logger.warning(f"Beat loader missing required method: {method_name}")
                return False

        return True
