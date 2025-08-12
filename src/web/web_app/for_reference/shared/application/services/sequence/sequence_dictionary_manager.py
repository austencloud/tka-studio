"""
Sequence Dictionary Service - Simple Dictionary Operations

Provides basic dictionary functionality for sequences including word calculation
and difficulty assessment without unnecessary interface abstractions.
"""

import logging
from typing import Optional

from desktop.modern.core.interfaces.sequence_data_services import (
    ISequenceDictionaryManager,
)
from desktop.modern.domain.models.sequence_data import SequenceData

logger = logging.getLogger(__name__)


class SequenceDictionaryManager(ISequenceDictionaryManager):
    """
    Simple dictionary service for sequence operations.

    Provides basic functionality for calculating words from sequences
    and assessing difficulty levels.
    """

    def __init__(self):
        """Initialize the dictionary service."""

    def get_word_for_sequence(self, sequence: SequenceData) -> Optional[str]:
        """Get word associated with sequence."""
        try:
            logger.debug("Calculating word from sequence beats")

            # Calculate word from beat letters (excluding start position)
            if not sequence.beats:
                return ""

            word = "".join(
                beat.letter for beat in sequence.beats if beat.beat_number > 0
            )

            logger.debug(f"Calculated word: '{word}'")
            return word

        except Exception as e:
            logger.error(f"Error getting word for sequence: {e}")
            return None

    def calculate_difficulty(self, sequence: SequenceData) -> int:
        """Calculate sequence difficulty level."""
        try:
            logger.debug("Calculating sequence difficulty")

            # Simple difficulty calculation based on sequence length
            # This could be enhanced with more sophisticated algorithms
            length = len([beat for beat in sequence.beats if beat.beat_number > 0])

            if length <= 3:
                difficulty = 1
            elif length <= 6:
                difficulty = 2
            elif length <= 10:
                difficulty = 3
            else:
                difficulty = 4

            logger.debug(f"Calculated difficulty: {difficulty} (length: {length})")
            return difficulty

        except Exception as e:
            logger.error(f"Error calculating difficulty: {e}")
            return 1  # Default to easiest difficulty on error

    def add_sequence_to_dictionary(self, sequence: SequenceData, word: str) -> bool:
        """Add sequence to dictionary."""
        try:
            logger.debug(f"Adding sequence to dictionary: {word}")

            # TODO: Integrate with actual dictionary service when available
            # For now, this is a placeholder implementation
            logger.warning("Dictionary service integration not yet implemented")

            # Simulate successful addition
            logger.info(f"Sequence '{word}' added to dictionary (placeholder)")
            return True

        except Exception as e:
            logger.error(f"Error adding sequence to dictionary: {e}")
            return False
