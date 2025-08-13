"""
Qt Sequence Beat Operations Adapter

This adapter wraps the pure SequenceBeatOperationsService and provides Qt signal coordination.
This maintains the separation between platform-agnostic services and Qt-specific presentation logic.
"""

from __future__ import annotations

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.application.services.sequence.beat_factory import BeatFactory
from desktop.modern.application.services.sequence.sequence_beat_operations_service import (
    SequenceBeatOperationsService,
)
from desktop.modern.application.services.sequence.sequence_persister import (
    SequencePersister,
)
from desktop.modern.core.interfaces.workbench_services import IWorkbenchStateManager
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData


class QtSequenceBeatOperationsAdapter(QObject):
    """
    Improved Qt adapter for the SequenceBeatOperationsService.

    Uses WorkbenchStateService for clean dependency injection instead of
    passing workbench_getter callable around.

    Benefits:
    - Type-safe dependencies
    - Better error handling
    - Easier testing
    - Clear interface contracts
    - Loose coupling
    """

    # Qt signals for UI coordination
    beat_added = pyqtSignal(object, int, object)  # BeatData, position, SequenceData
    beat_removed = pyqtSignal(int)  # position
    beat_updated = pyqtSignal(object, int)  # BeatData, position

    def __init__(
        self,
        workbench_state_manager: IWorkbenchStateManager,
        beat_factory: BeatFactory | None = None,
        persistence_service: SequencePersister | None = None,
    ):
        super().__init__()

        self._workbench_state_manager = workbench_state_manager

        # Create the pure service
        self._service = SequenceBeatOperationsService(
            workbench_state_manager=workbench_state_manager,
            beat_factory=beat_factory,
            persistence_service=persistence_service,
        )

        # Connect service callbacks to Qt signals
        self._service.add_beat_added_callback(self._on_beat_added)
        self._service.add_beat_removed_callback(self._on_beat_removed)
        self._service.add_beat_updated_callback(self._on_beat_updated)

    def _on_beat_added(
        self, beat_data: BeatData, position: int, sequence_data: SequenceData
    ):
        """Convert service callback to Qt signal."""
        self.beat_added.emit(beat_data, position, sequence_data)

    def _on_beat_removed(self, position: int):
        """Convert service callback to Qt signal."""
        self.beat_removed.emit(position)

    def _on_beat_updated(self, beat_data: BeatData, position: int):
        """Convert service callback to Qt signal."""
        self.beat_updated.emit(beat_data, position)

    # Delegate all service methods to the pure service
    def add_beat(
        self,
        pictograph_data: PictographData,
        position: int,
        sequence_data: SequenceData | None = None,
        persist: bool = True,
    ) -> SequenceData:
        """Add a beat to the sequence at the specified position."""
        return self._service.add_beat(pictograph_data, position, sequence_data, persist)

    def remove_beat(
        self,
        position: int,
        sequence_data: SequenceData | None = None,
        persist: bool = True,
    ) -> SequenceData:
        """Remove a beat from the sequence at the specified position."""
        return self._service.remove_beat(position, sequence_data, persist)

    def update_beat(
        self,
        position: int,
        pictograph_data: PictographData,
        sequence_data: SequenceData | None = None,
        persist: bool = True,
    ) -> SequenceData:
        """Update a beat in the sequence at the specified position."""
        return self._service.update_beat(
            position, pictograph_data, sequence_data, persist
        )

    def get_beat(
        self,
        position: int,
        sequence_data: SequenceData | None = None,
    ) -> BeatData | None:
        """Get a beat from the sequence at the specified position."""
        return self._service.get_beat(position, sequence_data)

    def get_beat_count(self, sequence_data: SequenceData | None = None) -> int:
        """Get the number of beats in the sequence."""
        return self._service.get_beat_count(sequence_data)

    def add_pictograph_to_sequence(self, pictograph_data: PictographData) -> None:
        """Add pictograph to sequence (compatibility method for signal connections)."""
        try:
            print("🔍 [BEAT_OPERATIONS] add_pictograph_to_sequence called")
            print(f"🔍 [BEAT_OPERATIONS] Pictograph: {pictograph_data.letter}")

            # Get current sequence from workbench state manager
            current_sequence = self._workbench_state_manager.get_current_sequence()
            print(
                f"🔍 [BEAT_OPERATIONS] Current sequence: {current_sequence.length if current_sequence else 0} beats"
            )

            if current_sequence and current_sequence.beats:
                for i, beat in enumerate(current_sequence.beats):
                    print(
                        f"🔍 [BEAT_OPERATIONS] Existing Beat {i}: beat_number={beat.beat_number}, is_blank={beat.is_blank}"
                    )
                    if hasattr(beat, "pictograph_data") and beat.pictograph_data:
                        print(
                            f"🔍 [BEAT_OPERATIONS] Existing Beat {i} pictograph: letter={beat.pictograph_data.letter}"
                        )

            # Calculate next position
            position = len(current_sequence.beats) if current_sequence else 0
            print(f"🔍 [BEAT_OPERATIONS] Adding at position: {position}")

            # Use the add_beat method
            self.add_beat(pictograph_data, position, current_sequence, persist=True)

        except Exception as e:
            print(f"❌ Error adding pictograph to sequence: {e}")
            import traceback

            traceback.print_exc()
