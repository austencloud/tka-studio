"""
Sequence Repository - CRUD Operations and Data Access

Handles all sequence data access operations and repository patterns.
Extracted from the monolithic sequence management service to focus
solely on data access and storage operations.
"""

import logging
from abc import ABC, abstractmethod

from desktop.modern.domain.models.sequence_data import SequenceData

logger = logging.getLogger(__name__)


class RepositoryError(Exception):
    """Custom exception for repository errors."""


class ISequenceRepository(ABC):
    """Interface for sequence data access operations."""

    @abstractmethod
    def save(self, sequence: SequenceData) -> SequenceData:
        """Save a sequence to storage."""

    @abstractmethod
    def get_by_id(self, sequence_id: str) -> SequenceData | None:
        """Retrieve a sequence by its ID."""

    @abstractmethod
    def get_all(self) -> list[SequenceData]:
        """Retrieve all sequences."""

    @abstractmethod
    def delete(self, sequence_id: str) -> bool:
        """Delete a sequence by ID."""

    @abstractmethod
    def exists(self, sequence_id: str) -> bool:
        """Check if a sequence exists."""

    @abstractmethod
    def get_current_sequence(self) -> SequenceData | None:
        """Get the current active sequence."""

    @abstractmethod
    def set_current_sequence(self, sequence: SequenceData) -> None:
        """Set the current active sequence."""

    @abstractmethod
    def clear_current_sequence(self) -> None:
        """Clear the current active sequence."""


class SequenceRepository(ISequenceRepository):
    """
    Repository for sequence data access operations.

    Responsibilities:
    - CRUD operations for sequences
    - Data persistence coordination
    - Storage abstraction
    - Query operations
    - Current sequence management
    """

    def __init__(self, storage_adapter=None):
        """
        Initialize repository with optional storage adapter.

        Args:
            storage_adapter: Optional storage implementation (file, database, etc.)
        """
        self._storage_adapter = storage_adapter
        self._sequences_cache = {}
        self._current_sequence_id = None
        logger.info("SequenceRepository initialized")

    def save(self, sequence: SequenceData) -> SequenceData:
        """
        Save a sequence to storage.

        Args:
            sequence: The sequence to save

        Returns:
            The saved sequence

        Raises:
            RepositoryError: If save operation fails
        """
        if not sequence:
            raise ValueError("Cannot save None sequence")

        logger.debug(f"Saving sequence: {sequence.name} (ID: {sequence.id})")

        try:
            # Update cache
            self._sequences_cache[sequence.id] = sequence

            # Persist to storage if adapter available
            if self._storage_adapter:
                self._storage_adapter.save_sequence(sequence)

            logger.info(f"Sequence '{sequence.name}' saved successfully")
            return sequence

        except Exception as e:
            logger.error(f"Failed to save sequence {sequence.name}: {e}")
            raise RepositoryError(f"Failed to save sequence: {e}") from e

    def get_by_id(self, sequence_id: str) -> SequenceData | None:
        """
        Retrieve a sequence by its ID.

        Args:
            sequence_id: The sequence ID to retrieve

        Returns:
            The sequence if found, None otherwise
        """
        if not sequence_id:
            return None

        logger.debug(f"Retrieving sequence by ID: {sequence_id}")

        # Check cache first
        if sequence_id in self._sequences_cache:
            logger.debug(f"Sequence {sequence_id} found in cache")
            return self._sequences_cache[sequence_id]

        # Try storage adapter
        if self._storage_adapter:
            try:
                sequence = self._storage_adapter.load_sequence(sequence_id)
                if sequence:
                    # Cache the result
                    self._sequences_cache[sequence_id] = sequence
                    logger.debug(f"Sequence {sequence_id} loaded from storage")
                    return sequence
            except Exception as e:
                logger.error(f"Failed to load sequence {sequence_id} from storage: {e}")

        logger.debug(f"Sequence {sequence_id} not found")
        return None

    def update(self, sequence: SequenceData) -> SequenceData:
        """
        Update an existing sequence.

        Args:
            sequence: The sequence to update

        Returns:
            The updated sequence

        Raises:
            RepositoryError: If sequence doesn't exist or update fails
        """
        if not sequence:
            raise ValueError("Cannot update None sequence")

        if not self.exists(sequence.id):
            raise RepositoryError(f"Sequence {sequence.id} does not exist")

        logger.debug(f"Updating sequence: {sequence.name} (ID: {sequence.id})")

        try:
            # Update cache
            self._sequences_cache[sequence.id] = sequence

            # Persist to storage if adapter available
            if self._storage_adapter:
                self._storage_adapter.save_sequence(sequence)

            logger.info(f"Sequence '{sequence.name}' updated successfully")
            return sequence

        except Exception as e:
            logger.error(f"Failed to update sequence {sequence.name}: {e}")
            raise RepositoryError(f"Failed to update sequence: {e}") from e

    def delete(self, sequence_id: str) -> bool:
        """
        Delete a sequence by ID.

        Args:
            sequence_id: The sequence ID to delete

        Returns:
            True if deleted, False if not found

        Raises:
            RepositoryError: If delete operation fails
        """
        if not sequence_id:
            return False

        logger.debug(f"Deleting sequence: {sequence_id}")

        try:
            # Remove from cache
            if sequence_id in self._sequences_cache:
                del self._sequences_cache[sequence_id]

            # Remove from storage if adapter available
            if self._storage_adapter:
                success = self._storage_adapter.delete_sequence(sequence_id)
                if not success:
                    logger.warning(
                        f"Storage adapter reported failure deleting {sequence_id}"
                    )

            # Clear current sequence if it was deleted
            if self._current_sequence_id == sequence_id:
                self._current_sequence_id = None

            logger.info(f"Sequence {sequence_id} deleted successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to delete sequence {sequence_id}: {e}")
            raise RepositoryError(f"Failed to delete sequence: {e}") from e

    def exists(self, sequence_id: str) -> bool:
        """
        Check if a sequence exists.

        Args:
            sequence_id: The sequence ID to check

        Returns:
            True if sequence exists, False otherwise
        """
        if not sequence_id:
            return False

        # Check cache first
        if sequence_id in self._sequences_cache:
            return True

        # Check storage adapter
        if self._storage_adapter:
            try:
                return self._storage_adapter.sequence_exists(sequence_id)
            except Exception as e:
                logger.error(f"Error checking sequence existence {sequence_id}: {e}")

        return False

    def get_all(self) -> list[SequenceData]:
        """
        Get all sequences.

        Returns:
            List of all sequences
        """
        logger.debug("Retrieving all sequences")

        sequences = []

        # Add cached sequences
        sequences.extend(self._sequences_cache.values())

        # Add sequences from storage (if not already cached)
        if self._storage_adapter:
            try:
                storage_sequences = self._storage_adapter.get_all_sequences()
                for seq in storage_sequences:
                    if seq.id not in self._sequences_cache:
                        sequences.append(seq)
                        # Cache it for future use
                        self._sequences_cache[seq.id] = seq
            except Exception as e:
                logger.error(f"Failed to retrieve sequences from storage: {e}")

        logger.info(f"Retrieved {len(sequences)} sequences")
        return sequences

    def find_by_name(self, name: str) -> list[SequenceData]:
        """
        Find sequences by name (partial match).

        Args:
            name: The name to search for

        Returns:
            List of matching sequences
        """
        if not name:
            return []

        logger.debug(f"Finding sequences by name: '{name}'")

        all_sequences = self.get_all()
        matching_sequences = [
            seq for seq in all_sequences if name.lower() in seq.name.lower()
        ]

        logger.debug(f"Found {len(matching_sequences)} sequences matching '{name}'")
        return matching_sequences

    def get_current_sequence(self) -> SequenceData | None:
        """
        Get the current active sequence.

        Returns:
            The current sequence if set, None otherwise
        """
        if not self._current_sequence_id:
            logger.debug("No current sequence set")
            return None

        sequence = self.get_by_id(self._current_sequence_id)
        if not sequence:
            logger.warning(f"Current sequence ID {self._current_sequence_id} not found")
            self._current_sequence_id = None

        return sequence

    def set_current_sequence(self, sequence_id: str) -> bool:
        """
        Set the current active sequence.

        Args:
            sequence_id: The sequence ID to set as current

        Returns:
            True if set successfully, False otherwise
        """
        if not sequence_id:
            self._current_sequence_id = None
            logger.info("Current sequence cleared")
            return True

        if not self.exists(sequence_id):
            logger.warning(f"Cannot set current sequence: {sequence_id} does not exist")
            return False

        self._current_sequence_id = sequence_id
        logger.info(f"Current sequence set to: {sequence_id}")
        return True

    def get_sequences_by_length(self, length: int) -> list[SequenceData]:
        """
        Get sequences by their length.

        Args:
            length: The sequence length to filter by

        Returns:
            List of sequences with the specified length
        """
        all_sequences = self.get_all()
        matching_sequences = [seq for seq in all_sequences if len(seq.beats) == length]

        logger.debug(f"Found {len(matching_sequences)} sequences with length {length}")
        return matching_sequences

    def clear_cache(self) -> None:
        """Clear the internal cache."""
        self._sequences_cache.clear()
        logger.info("Repository cache cleared")

    def get_cache_size(self) -> int:
        """Get the number of sequences in cache."""
        return len(self._sequences_cache)

    def set_storage_adapter(self, adapter) -> None:
        """Set the storage adapter."""
        self._storage_adapter = adapter
        logger.info(f"Storage adapter set: {type(adapter).__name__}")
