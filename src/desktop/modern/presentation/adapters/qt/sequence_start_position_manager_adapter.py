"""
Qt Sequence Start Position Manager Adapter

This adapter wraps the pure SequenceStartPositionService and provides Qt signal coordination.
This maintains the separation between platform-agnostic services and Qt-specific presentation logic.
"""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.application.services.data.modern_to_legacy_converter import (
    ModernToLegacyConverter,
)
from desktop.modern.application.services.sequence.beat_factory import BeatFactory
from desktop.modern.application.services.sequence.sequence_persister import (
    SequencePersister,
)
from desktop.modern.application.services.sequence.sequence_start_position_service import (
    SequenceStartPositionService,
)
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData


class QtSequenceStartPositionManagerAdapter(QObject):
    """
    Qt adapter for the SequenceStartPositionService that provides signal coordination.

    This class handles Qt-specific signal emissions while delegating actual
    start position management logic to the platform-agnostic service.
    """

    # Qt signals for UI coordination
    start_position_set = pyqtSignal(object)  # BeatData object
    start_position_updated = pyqtSignal(object)  # BeatData object

    def __init__(
        self,
        workbench_getter: Callable[[], object] | None = None,
        modern_to_legacy_converter: ModernToLegacyConverter | None = None,
        beat_factory: BeatFactory | None = None,
        persistence_service: SequencePersister | None = None,
    ):
        super().__init__()

        # Create the pure service
        self._service = SequenceStartPositionService(
            workbench_getter=workbench_getter,
            modern_to_legacy_converter=modern_to_legacy_converter,
            beat_factory=beat_factory,
            persistence_service=persistence_service,
        )

        # Connect service callbacks to Qt signals
        self._service.add_start_position_set_callback(self._on_start_position_set)
        self._service.add_start_position_updated_callback(
            self._on_start_position_updated
        )

    def _on_start_position_set(self, beat_data: BeatData):
        """Convert service callback to Qt signal."""
        self.start_position_set.emit(beat_data)

    def _on_start_position_updated(self, beat_data: BeatData):
        """Convert service callback to Qt signal."""
        self.start_position_updated.emit(beat_data)

    # Delegate all service methods to the pure service
    def set_start_position(
        self,
        pictograph_data: PictographData,
        sequence_data: SequenceData | None = None,
        persist: bool = True,
    ):
        """Set the start position for the sequence."""
        return self._service.set_start_position(pictograph_data, sequence_data, persist)

    def update_start_position(
        self,
        pictograph_data: PictographData,
        sequence_data: SequenceData | None = None,
        persist: bool = True,
    ):
        """Update the existing start position."""
        return self._service.update_start_position(
            pictograph_data, sequence_data, persist
        )

    def get_start_position(
        self, sequence_data: SequenceData | None = None
    ) -> BeatData | None:
        """Get the current start position."""
        return self._service.get_start_position(sequence_data)

    def clear_start_position(
        self, sequence_data: SequenceData | None = None, persist: bool = True
    ):
        """Clear the start position."""
        return self._service.clear_start_position(sequence_data, persist)
