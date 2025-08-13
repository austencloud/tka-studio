"""
Pure Sequence Beat Operations Service - Platform Agnostic

This service handles beat operations without any Qt dependencies.
Qt-specific signal coordination is handled by adapters in the presentation layer.
"""

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING

from desktop.modern.application.services.sequence.beat_factory import BeatFactory
from desktop.modern.application.services.sequence.sequence_persister import (
    SequencePersister,
)
from desktop.modern.core.interfaces.workbench_services import IWorkbenchStateManager
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class SequenceBeatOperationsService:
    """
    Pure service for managing beat operations in sequences.

    This service is platform-agnostic and does not depend on Qt.
    Signal coordination is handled by Qt adapters in the presentation layer.

    Responsibilities:
    - Adding beats to sequences
    - Removing beats from sequences
    - Updating beats in sequences
    - Managing beat persistence
    """

    def __init__(
        self,
        workbench_state_manager: IWorkbenchStateManager | None = None,
        beat_factory: BeatFactory | None = None,
        persistence_service: SequencePersister | None = None,
    ):
        self.workbench_state_manager = workbench_state_manager
        self.beat_factory = beat_factory or BeatFactory()
        self.persistence_service = persistence_service or SequencePersister()

        # Platform-agnostic event callbacks
        self._beat_added_callbacks: list[
            Callable[[BeatData, int, SequenceData], None]
        ] = []
        self._beat_removed_callbacks: list[Callable[[int], None]] = []
        self._beat_updated_callbacks: list[Callable[[BeatData, int], None]] = []

    def add_beat_added_callback(
        self, callback: Callable[[BeatData, int, SequenceData], None]
    ):
        """Add callback for when a beat is added."""
        self._beat_added_callbacks.append(callback)

    def add_beat_removed_callback(self, callback: Callable[[int], None]):
        """Add callback for when a beat is removed."""
        self._beat_removed_callbacks.append(callback)

    def add_beat_updated_callback(self, callback: Callable[[BeatData, int], None]):
        """Add callback for when a beat is updated."""
        self._beat_updated_callbacks.append(callback)

    def add_beat(
        self,
        pictograph_data: PictographData,
        position: int,
        sequence_data: SequenceData | None = None,
        persist: bool = True,
    ) -> SequenceData:
        """
        Add a beat to the sequence at the specified position.

        Args:
            pictograph_data: The pictograph data for the new beat
            position: The position to insert the beat
            sequence_data: Current sequence data (if available)
            persist: Whether to persist the change

        Returns:
            Updated sequence data
        """
        try:
            # Get current sequence if not provided
            if sequence_data is None and self.workbench_state_manager:
                try:
                    sequence_data = self.workbench_state_manager.get_current_sequence()
                except Exception as e:
                    logger.warning(f"Could not get sequence from workbench: {e}")

            # Create beat data from pictograph data
            # Convert position (0-indexed) to beat_number (1-indexed)
            beat_data = self.beat_factory.create_from_pictograph(
                pictograph_data, beat_number=position + 1
            )

            # Add beat to sequence
            if sequence_data:
                updated_sequence = sequence_data.add_beat(beat_data)
            else:
                # Create new sequence with this beat
                updated_sequence = SequenceData(name="New Sequence", beats=[beat_data])

            # Update workbench if available
            if self.workbench_state_manager:
                try:
                    self.workbench_state_manager.set_sequence(updated_sequence)
                except Exception as e:
                    logger.warning(f"Could not update workbench: {e}")

            # Persist if requested
            if persist:
                try:
                    # Convert SequenceData to the format expected by persistence service
                    sequence_dict = (
                        updated_sequence.to_dict()
                        if hasattr(updated_sequence, "to_dict")
                        else []
                    )
                    self.persistence_service.save_current_sequence(sequence_dict)
                except Exception as e:
                    # Log the error but don't fail the operation
                    logger.warning(f"Failed to persist sequence: {e}")
                    # Continue without persistence - the in-memory sequence is still valid

            # Notify callbacks instead of emitting Qt signals
            for callback in self._beat_added_callbacks:
                callback(beat_data, position, updated_sequence)

            logger.info(f"Beat added at position {position}: {pictograph_data.letter}")
            return updated_sequence

        except Exception as e:
            logger.error(f"Failed to add beat: {e}")
            raise

    def remove_beat(
        self,
        position: int,
        sequence_data: SequenceData | None = None,
        persist: bool = True,
    ) -> SequenceData:
        """
        Remove a beat from the sequence at the specified position.

        Args:
            position: The position of the beat to remove
            sequence_data: Current sequence data (if available)
            persist: Whether to persist the change

        Returns:
            Updated sequence data
        """
        try:
            # Get current sequence if not provided
            if sequence_data is None and self.workbench_state_manager:
                try:
                    sequence_data = self.workbench_state_manager.get_current_sequence()
                except Exception as e:
                    logger.warning(f"Could not get sequence from workbench: {e}")

            if not sequence_data:
                raise ValueError("No sequence data available")

            # Remove beat from sequence
            updated_sequence = sequence_data.remove_beat(position)

            # Update workbench if available
            if self.workbench_state_manager:
                try:
                    self.workbench_state_manager.set_current_sequence(updated_sequence)
                except Exception as e:
                    logger.warning(f"Could not update workbench: {e}")

            # Persist if requested
            if persist:
                self.persistence_service.save_sequence(updated_sequence)

            # Notify callbacks instead of emitting Qt signals
            for callback in self._beat_removed_callbacks:
                callback(position)

            logger.info(f"Beat removed from position {position}")
            return updated_sequence

        except Exception as e:
            logger.error(f"Failed to remove beat: {e}")
            raise

    def update_beat(
        self,
        position: int,
        pictograph_data: PictographData,
        sequence_data: SequenceData | None = None,
        persist: bool = True,
    ) -> SequenceData:
        """
        Update a beat in the sequence at the specified position.

        Args:
            position: The position of the beat to update
            pictograph_data: The new pictograph data for the beat
            sequence_data: Current sequence data (if available)
            persist: Whether to persist the change

        Returns:
            Updated sequence data
        """
        try:
            # Get current sequence if not provided
            if sequence_data is None and self.workbench_state_manager:
                try:
                    sequence_data = self.workbench_state_manager.get_current_sequence()
                except Exception as e:
                    logger.warning(f"Could not get sequence from workbench: {e}")

            if not sequence_data:
                raise ValueError("No sequence data available")

            # Create updated beat data from pictograph data
            beat_data = self.beat_factory.create_beat_from_pictograph(
                pictograph_data, beat_number=position
            )

            # Update beat in sequence
            updated_sequence = sequence_data.update_beat(position, beat_data)

            # Update workbench if available
            if self.workbench_state_manager:
                try:
                    self.workbench_state_manager.set_current_sequence(updated_sequence)
                except Exception as e:
                    logger.warning(f"Could not update workbench: {e}")

            # Persist if requested
            if persist:
                self.persistence_service.save_sequence(updated_sequence)

            # Notify callbacks instead of emitting Qt signals
            for callback in self._beat_updated_callbacks:
                callback(beat_data, position)

            logger.info(
                f"Beat updated at position {position}: {pictograph_data.letter}"
            )
            return updated_sequence

        except Exception as e:
            logger.error(f"Failed to update beat: {e}")
            raise

    def get_beat(
        self,
        position: int,
        sequence_data: SequenceData | None = None,
    ) -> BeatData | None:
        """
        Get a beat from the sequence at the specified position.

        Args:
            position: The position of the beat to get
            sequence_data: Current sequence data (if available)

        Returns:
            The beat data at the specified position, or None if not found
        """
        try:
            # Get current sequence if not provided
            if sequence_data is None and self.workbench_state_manager:
                try:
                    sequence_data = self.workbench_state_manager.get_current_sequence()
                except Exception as e:
                    logger.warning(f"Could not get sequence from workbench: {e}")

            if not sequence_data:
                return None

            # Get beat from sequence
            return sequence_data.get_beat(position)

        except Exception as e:
            logger.error(f"Failed to get beat: {e}")
            return None

    def get_beat_count(self, sequence_data: SequenceData | None = None) -> int:
        """
        Get the number of beats in the sequence.

        Args:
            sequence_data: Current sequence data (if available)

        Returns:
            The number of beats in the sequence
        """
        try:
            # Get current sequence if not provided
            if sequence_data is None and self.workbench_state_manager:
                try:
                    sequence_data = self.workbench_state_manager.get_current_sequence()
                except Exception as e:
                    logger.warning(f"Could not get sequence from workbench: {e}")

            if not sequence_data:
                return 0

            return len(sequence_data.beats)

        except Exception as e:
            logger.error(f"Failed to get beat count: {e}")
            return 0
