"""
Sequence Repository for TKA Modern API
Provides in-memory storage for sequences with CRUD operations.
"""

from __future__ import annotations

import logging

from desktop.modern.domain.models.sequence_data import SequenceData


logger = logging.getLogger(__name__)


class SequenceRepository:
    """
    In-memory repository for sequence storage.

    This provides the storage layer for the API, allowing sequences to be
    persisted, retrieved, updated, and deleted. In a production system,
    this would be backed by a database, but for now we use in-memory storage.
    """

    def __init__(self):
        """Initialize the repository with empty storage."""
        self._sequences: dict[str, SequenceData] = {}
        self._current_sequence_id: str | None = None
        logger.info("SequenceRepository initialized")

    def save(self, sequence: SequenceData) -> None:
        """
        Save a sequence to the repository.

        Args:
            sequence: The sequence to save
        """
        self._sequences[sequence.id] = sequence
        logger.debug(f"Saved sequence {sequence.id}: {sequence.name}")

    def get_by_id(self, sequence_id: str) -> SequenceData | None:
        """
        Retrieve a sequence by its ID.

        Args:
            sequence_id: The ID of the sequence to retrieve

        Returns:
            The sequence if found, None otherwise
        """
        sequence = self._sequences.get(sequence_id)
        if sequence:
            logger.debug(f"Retrieved sequence {sequence_id}: {sequence.name}")
        else:
            logger.debug(f"Sequence {sequence_id} not found")
        return sequence

    def get_all(self) -> list[SequenceData]:
        """
        Get all sequences in the repository.

        Returns:
            List of all sequences
        """
        sequences = list(self._sequences.values())
        logger.debug(f"Retrieved {len(sequences)} sequences")
        return sequences

    def update(self, sequence: SequenceData) -> bool:
        """
        Update an existing sequence.

        Args:
            sequence: The updated sequence data

        Returns:
            True if the sequence was updated, False if it doesn't exist
        """
        if sequence.id in self._sequences:
            self._sequences[sequence.id] = sequence
            logger.debug(f"Updated sequence {sequence.id}: {sequence.name}")
            return True
        logger.warning(f"Attempted to update non-existent sequence {sequence.id}")
        return False

    def delete(self, sequence_id: str) -> bool:
        """
        Delete a sequence from the repository.

        Args:
            sequence_id: The ID of the sequence to delete

        Returns:
            True if the sequence was deleted, False if it doesn't exist
        """
        if sequence_id in self._sequences:
            deleted_sequence = self._sequences.pop(sequence_id)
            logger.debug(f"Deleted sequence {sequence_id}: {deleted_sequence.name}")

            # Clear current sequence if it was deleted
            if self._current_sequence_id == sequence_id:
                self._current_sequence_id = None
                logger.debug("Cleared current sequence (was deleted)")

            return True
        logger.warning(f"Attempted to delete non-existent sequence {sequence_id}")
        return False

    def set_current_sequence(self, sequence_id: str) -> bool:
        """
        Set the current active sequence.

        Args:
            sequence_id: The ID of the sequence to set as current

        Returns:
            True if the sequence exists and was set as current, False otherwise
        """
        if sequence_id in self._sequences:
            self._current_sequence_id = sequence_id
            logger.debug(f"Set current sequence to {sequence_id}")
            return True
        logger.warning(
            f"Attempted to set non-existent sequence {sequence_id} as current"
        )
        return False

    def get_current_sequence(self) -> SequenceData | None:
        """
        Get the currently active sequence.

        Returns:
            The current sequence if one is set, None otherwise
        """
        if self._current_sequence_id:
            return self.get_by_id(self._current_sequence_id)
        return None

    def get_current_sequence_id(self) -> str | None:
        """
        Get the ID of the currently active sequence.

        Returns:
            The current sequence ID if one is set, None otherwise
        """
        return self._current_sequence_id

    def clear_current_sequence(self) -> None:
        """Clear the current sequence selection."""
        self._current_sequence_id = None
        logger.debug("Cleared current sequence")

    def count(self) -> int:
        """
        Get the total number of sequences in the repository.

        Returns:
            The number of sequences
        """
        return len(self._sequences)

    def exists(self, sequence_id: str) -> bool:
        """
        Check if a sequence exists in the repository.

        Args:
            sequence_id: The ID to check

        Returns:
            True if the sequence exists, False otherwise
        """
        return sequence_id in self._sequences
