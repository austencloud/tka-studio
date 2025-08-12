"""
Pure Sequence Loading Service - Platform Agnostic

This service handles sequence loading without any Qt dependencies.
Qt-specific signal coordination is handled by adapters in the presentation layer.
"""

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING

from desktop.modern.core.interfaces.sequence_data_services import ISequenceLoader
from desktop.modern.core.interfaces.workbench_services import IWorkbenchStateManager
from desktop.modern.domain.models.sequence_data import SequenceData
from shared.application.services.data.legacy_to_modern_converter import (
    LegacyToModernConverter,
)
from shared.application.services.sequence.sequence_persister import SequencePersister

if TYPE_CHECKING:
    from desktop.modern.domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)


class SequenceLoaderService(ISequenceLoader):
    """
    Pure service for loading sequences from persistence and handling startup restoration.

    This service is platform-agnostic and does not depend on Qt.
    Signal coordination is handled by Qt adapters in the presentation layer.

    Responsibilities:
    - Loading sequences from current_sequence.json
    - Converting legacy format to modern SequenceData
    - Managing startup sequence restoration
    - Providing data to presentation layer adapters
    """

    def __init__(
        self,
        workbench_state_manager: IWorkbenchStateManager | None = None,
        legacy_to_modern_converter: LegacyToModernConverter | None = None,
    ):
        self.workbench_state_manager = workbench_state_manager
        self.legacy_to_modern_converter = (
            legacy_to_modern_converter or LegacyToModernConverter()
        )
        self.persistence_service = SequencePersister()

        # Platform-agnostic event callbacks
        self._sequence_loaded_callbacks: list[Callable[[SequenceData], None]] = []
        self._start_position_loaded_callbacks: list[Callable[[object, str], None]] = []

    def add_sequence_loaded_callback(self, callback: Callable[[SequenceData], None]):
        """Add callback for when sequence is loaded."""
        self._sequence_loaded_callbacks.append(callback)

    def add_start_position_loaded_callback(
        self, callback: Callable[[object, str], None]
    ):
        """Add callback for when start position is loaded."""
        self._start_position_loaded_callbacks.append(callback)

    def load_sequence_on_startup(self):
        """Load sequence from current_sequence.json on startup - exactly like legacy"""
        try:
            # Load sequence from persistence
            sequence_data = self.persistence_service.load_current_sequence()

            if len(sequence_data) <= 1:
                # CRITICAL FIX: Always initialize start position component for empty sequences
                # This ensures the "START" text overlay is visible even when no sequence exists
                self._initialize_empty_sequence_start_position()
                return

            # Extract metadata and beats
            metadata = sequence_data[0]
            sequence_word = metadata.get("word", "")

            # Find start position (beat 0) and actual beats (beat 1+)
            start_position_data = None
            beats_data = []

            for item in sequence_data[1:]:
                if item.get("beat") == 0:
                    start_position_data = item
                elif "letter" in item and not item.get("is_placeholder", False):
                    beats_data.append(item)

            # Convert beats to modern format with full pictograph data
            beat_objects = []
            for i, beat_dict in enumerate(beats_data):
                try:
                    # Convert legacy format back to modern BeatData with full data
                    beat_obj = (
                        self.legacy_to_modern_converter.convert_legacy_to_beat_data(
                            beat_dict, i + 1
                        )
                    )
                    beat_objects.append(beat_obj)
                except Exception as e:
                    logger.error(
                        f"Failed to convert beat {beat_dict.get('letter', '?')}: {e}"
                    )

            # CRITICAL FIX: Handle start position loading INDEPENDENTLY of beats
            # This ensures start positions are visible even when there are no beats
            if start_position_data:
                try:
                    # Extract the position key from the start position data
                    end_position = start_position_data.get("end_pos", "alpha1")
                    position_key = f"{end_position}_{end_position}"

                    # Create start position data in both formats
                    # Create BeatData for workbench - direct return
                    try:
                        start_position_beat = self.legacy_to_modern_converter.convert_legacy_start_position_to_beat_data(
                            start_position_data
                        )

                        # Set start position in workbench via state manager
                        if self.workbench_state_manager:
                            self.workbench_state_manager.set_start_position(
                                start_position_beat
                            )

                        # Notify callbacks instead of emitting Qt signals
                        for callback in self._start_position_loaded_callbacks:
                            callback(start_position_beat, position_key)

                    except Exception as e:
                        logger.error(f"Failed to convert start position: {e}")
                        return  # Skip start position loading if conversion fails
                except Exception as e:
                    logger.error(f"Failed to load start position: {e}")

            # Create and set the sequence (even if empty, to maintain state) using direct constructor
            loaded_sequence = SequenceData(
                name=sequence_word or "Loaded Sequence", beats=beat_objects
            )

            # Set sequence in workbench
            if self.workbench_state_manager:
                self.workbench_state_manager.set_sequence(loaded_sequence)

            # Notify callbacks instead of emitting Qt signals
            for callback in self._sequence_loaded_callbacks:
                callback(loaded_sequence)

        except Exception as e:
            logger.error(f"Failed to load sequence on startup: {e}")
            import traceback

            traceback.print_exc()

    def _create_start_position_pictograph_data(
        self, position_key: str, end_pos: str
    ) -> "PictographData":
        """Create PictographData for start position using dataset service."""
        try:
            # Use dependency injection to get shared services
            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
            )
            from desktop.modern.domain.models.grid_data import GridData
            from desktop.modern.domain.models.pictograph_data import PictographData
            from shared.application.services.data.dataset_query import IDatasetQuery

            container = get_container()
            dataset_service = container.resolve(IDatasetQuery)
            # Get real start position data from dataset as PictographData
            real_start_position_pictograph = (
                dataset_service.get_start_position_pictograph_data(
                    position_key, "diamond"
                )
            )

            if real_start_position_pictograph:
                # Update the pictograph data with correct position information
                pictograph_data = real_start_position_pictograph.update(
                    start_position=position_key,
                    end_position=end_pos,
                    metadata={"source": "sequence_loading"},
                )
                return pictograph_data
            else:
                logger.warning(
                    f"No real data found for position {position_key}, using fallback"
                )
                # Fallback PictographData
                return PictographData(
                    letter=position_key,
                    start_position=position_key,
                    end_position=end_pos,
                    grid_data=GridData(),
                    arrows={},
                    props={},
                    is_blank=False,
                    metadata={"source": "fallback_sequence_loading"},
                )
        except Exception as e:
            logger.error(f"Error creating PictographData: {e}")
            # Last resort fallback
            from desktop.modern.domain.models.grid_data import GridData
            from desktop.modern.domain.models.pictograph_data import PictographData

            return PictographData(
                letter=position_key,
                start_position=position_key,
                end_position=end_pos,
                grid_data=GridData(),
                arrows={},
                props={},
                is_blank=False,
                metadata={"source": "error_fallback"},
            )

    def _initialize_empty_sequence_start_position(self):
        """Initialize start position component for empty sequences"""
        try:
            # Clear start position through state manager
            if self.workbench_state_manager:
                # Setting None will properly clear the start position
                # and trigger appropriate UI updates through the state manager
                self.workbench_state_manager.set_start_position(None)
                logger.info("Initialized empty sequence start position")
            else:
                logger.warning(
                    "No workbench state manager available for start position initialization"
                )
        except Exception as e:
            logger.error(f"Failed to initialize empty sequence start position: {e}")

    def get_current_sequence_from_workbench(self) -> SequenceData | None:
        """Get the current sequence from workbench via state manager"""
        if self.workbench_state_manager:
            try:
                return self.workbench_state_manager.get_current_sequence()
            except Exception as e:
                logger.error(f"Error getting current sequence: {e}")
        return None

    def load_sequence_from_file(self, filepath: str) -> SequenceData | None:
        """
        Load sequence from file.

        Args:
            filepath: Path to sequence file

        Returns:
            Loaded sequence data, or None if failed
        """
        try:
            return self.persistence_service.load_sequence_from_file(filepath)
        except Exception as e:
            logger.error(f"Failed to load sequence from file {filepath}: {e}")
            return None

    def load_current_sequence(self) -> SequenceData | None:
        """
        Load the current sequence from default location.

        Returns:
            Current sequence data, or None if not found
        """
        try:
            # Use the existing startup loading logic
            sequence_data = self.persistence_service.load_current_sequence()
            if sequence_data and len(sequence_data) > 1:
                # Convert to modern format
                metadata = sequence_data[0]
                beats_data = [
                    item for item in sequence_data[1:] if item.get("beat", 0) > 0
                ]

                # Create SequenceData object - simplified version
                # For full implementation, would need to properly convert all data
                return SequenceData(
                    name=metadata.get("word", ""),
                    beats=[],  # Would need proper conversion
                )
        except Exception as e:
            logger.error(f"Failed to load current sequence: {e}")

        return None
