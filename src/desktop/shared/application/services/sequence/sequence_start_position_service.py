"""
Pure Sequence Start Position Management Service - Platform Agnostic

This service handles start position operations without any Qt dependencies.
Qt-specific signal coordination is handled by adapters in the presentation layer.
"""

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING

from desktop.modern.core.interfaces.sequence_data_services import (
    ISequenceStartPositionManager,
)
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData
from shared.application.services.data.modern_to_legacy_converter import (
    ModernToLegacyConverter,
)
from shared.application.services.sequence.beat_factory import BeatFactory
from shared.application.services.sequence.sequence_persister import SequencePersister

if TYPE_CHECKING:
    from desktop.modern.presentation.components.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )

logger = logging.getLogger(__name__)


class SequenceStartPositionService(ISequenceStartPositionManager):
    """
    Pure service for managing start positions in sequences.

    This service is platform-agnostic and does not depend on Qt.
    Signal coordination is handled by Qt adapters in the presentation layer.

    Responsibilities:
    - Setting start positions
    - Converting start position data to legacy format
    - Managing start position persistence
    - Coordinating start position with workbench
    """

    def __init__(
        self,
        workbench_getter: Callable[[], "SequenceWorkbench"] | None = None,
        modern_to_legacy_converter: ModernToLegacyConverter | None = None,
        beat_factory: BeatFactory | None = None,
        persistence_service: SequencePersister | None = None,
    ):
        self.workbench_getter = workbench_getter
        self.modern_to_legacy_converter = (
            modern_to_legacy_converter or ModernToLegacyConverter()
        )
        self.beat_factory = beat_factory or BeatFactory()
        self.persistence_service = persistence_service or SequencePersister()

        # Platform-agnostic event callbacks
        self._start_position_set_callbacks: list[Callable[[BeatData], None]] = []
        self._start_position_updated_callbacks: list[Callable[[BeatData], None]] = []

    def add_start_position_set_callback(self, callback: Callable[[BeatData], None]):
        """Add callback for when start position is set."""
        self._start_position_set_callbacks.append(callback)

    def add_start_position_updated_callback(self, callback: Callable[[BeatData], None]):
        """Add callback for when start position is updated."""
        self._start_position_updated_callbacks.append(callback)

    def set_start_position(
        self,
        pictograph_data: PictographData,
        sequence_data: SequenceData | None = None,
        persist: bool = True,
    ):
        """
        Set the start position for the sequence.

        Args:
            pictograph_data: The pictograph data for the start position
            sequence_data: Current sequence data (if available)
            persist: Whether to persist the change
        """
        try:
            # Create beat data from pictograph data
            start_position_beat = self.beat_factory.create_beat_from_pictograph(
                pictograph_data, beat_number=0
            )

            # Get current sequence or create new one
            if sequence_data is None and self.workbench_getter:
                try:
                    workbench = self.workbench_getter()
                    if workbench and hasattr(workbench, "get_sequence"):
                        sequence_data = workbench.get_sequence()
                except Exception as e:
                    logger.warning(f"Could not get sequence from workbench: {e}")

            # Update sequence with new start position
            if sequence_data:
                updated_sequence = sequence_data.update_start_position(
                    start_position_beat
                )

                # Update workbench if available
                if self.workbench_getter:
                    try:
                        workbench = self.workbench_getter()
                        if workbench and hasattr(workbench, "set_sequence"):
                            workbench.set_sequence(updated_sequence)
                    except Exception as e:
                        logger.warning(f"Could not update workbench: {e}")

            # Persist if requested
            if persist:
                self._persist_start_position(start_position_beat, sequence_data)

            # Notify callbacks instead of emitting Qt signals
            for callback in self._start_position_set_callbacks:
                callback(start_position_beat)

            logger.info(f"Start position set: {pictograph_data.letter}")

        except Exception as e:
            logger.error(f"Failed to set start position: {e}")
            raise

    def update_start_position(
        self,
        pictograph_data: PictographData,
        sequence_data: SequenceData | None = None,
        persist: bool = True,
    ):
        """
        Update the existing start position.

        Args:
            pictograph_data: The new pictograph data for the start position
            sequence_data: Current sequence data (if available)
            persist: Whether to persist the change
        """
        try:
            # Create beat data from pictograph data
            start_position_beat = self.beat_factory.create_beat_from_pictograph(
                pictograph_data, beat_number=0
            )

            # Get current sequence or create new one
            if sequence_data is None and self.workbench_getter:
                try:
                    workbench = self.workbench_getter()
                    if workbench and hasattr(workbench, "get_sequence"):
                        sequence_data = workbench.get_sequence()
                except Exception as e:
                    logger.warning(f"Could not get sequence from workbench: {e}")

            # Update sequence with new start position
            if sequence_data:
                updated_sequence = sequence_data.update_start_position(
                    start_position_beat
                )

                # Update workbench if available
                if self.workbench_getter:
                    try:
                        workbench = self.workbench_getter()
                        if workbench and hasattr(workbench, "set_sequence"):
                            workbench.set_sequence(updated_sequence)
                    except Exception as e:
                        logger.warning(f"Could not update workbench: {e}")

            # Persist if requested
            if persist:
                self._persist_start_position(start_position_beat, sequence_data)

            # Notify callbacks instead of emitting Qt signals
            for callback in self._start_position_updated_callbacks:
                callback(start_position_beat)

            logger.info(f"Start position updated: {pictograph_data.letter}")

        except Exception as e:
            logger.error(f"Failed to update start position: {e}")
            raise

    def get_start_position(
        self, sequence_data: SequenceData | None = None
    ) -> BeatData | None:
        """
        Get the current start position.

        Args:
            sequence_data: Current sequence data (if available)

        Returns:
            The start position beat data, or None if not available
        """
        try:
            # Get current sequence if not provided
            if sequence_data is None and self.workbench_getter:
                try:
                    workbench = self.workbench_getter()
                    if workbench and hasattr(workbench, "get_sequence"):
                        sequence_data = workbench.get_sequence()
                except Exception as e:
                    logger.warning(f"Could not get sequence from workbench: {e}")

            if sequence_data and hasattr(sequence_data, "start_position"):
                return sequence_data.start_position

            return None

        except Exception as e:
            logger.error(f"Failed to get start position: {e}")
            return None

    def _persist_start_position(
        self, start_position_beat: BeatData, sequence_data: SequenceData | None
    ):
        """
        Persist the start position to storage.

        Args:
            start_position_beat: The start position beat data
            sequence_data: Current sequence data (if available)
        """
        try:
            # Convert to legacy format and persist
            legacy_data = self.modern_to_legacy_converter.convert_beat_to_legacy(
                start_position_beat
            )

            # Use persistence service to save
            if sequence_data:
                self.persistence_service.save_sequence(sequence_data)
            else:
                # Save just the start position
                self.persistence_service.save_start_position(legacy_data)

        except Exception as e:
            logger.error(f"Failed to persist start position: {e}")

    def clear_start_position(
        self, sequence_data: SequenceData | None = None, persist: bool = True
    ):
        """
        Clear the start position.

        Args:
            sequence_data: Current sequence data (if available)
            persist: Whether to persist the change
        """
        try:
            # Get current sequence if not provided
            if sequence_data is None and self.workbench_getter:
                try:
                    workbench = self.workbench_getter()
                    if workbench and hasattr(workbench, "get_sequence"):
                        sequence_data = workbench.get_sequence()
                except Exception as e:
                    logger.warning(f"Could not get sequence from workbench: {e}")

            # Clear start position in sequence
            if sequence_data:
                updated_sequence = sequence_data.clear_start_position()

                # Update workbench if available
                if self.workbench_getter:
                    try:
                        workbench = self.workbench_getter()
                        if workbench and hasattr(workbench, "set_sequence"):
                            workbench.set_sequence(updated_sequence)
                    except Exception as e:
                        logger.warning(f"Could not update workbench: {e}")

            # Persist if requested
            if persist and sequence_data:
                self.persistence_service.save_sequence(sequence_data)

            logger.info("Start position cleared")

        except Exception as e:
            logger.error(f"Failed to clear start position: {e}")
            raise
