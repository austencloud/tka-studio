"""
Qt Sequence Loader Adapter

This adapter wraps the pure SequenceLoaderService and provides Qt signal coordination.
This maintains the separation between platform-agnostic services and Qt-specific presentation logic.
"""

from typing import Callable, Optional

from application.services.data.legacy_to_modern_converter import LegacyToModernConverter
from application.services.sequence.sequence_loader_service import SequenceLoaderService
from domain.models.sequence_data import SequenceData
from PyQt6.QtCore import QObject, pyqtSignal


class QtSequenceLoaderAdapter(QObject):
    """
    Qt adapter for the SequenceLoaderService that provides signal coordination.

    This class handles Qt-specific signal emissions while delegating actual
    sequence loading logic to the platform-agnostic service.
    """

    # Qt signals for UI coordination
    sequence_loaded = pyqtSignal(object)  # SequenceData object
    start_position_loaded = pyqtSignal(object, str)  # BeatData object, position_key

    def __init__(
        self,
        workbench_getter: Optional[Callable[[], object]] = None,
        workbench_setter: Optional[Callable[[SequenceData], None]] = None,
        legacy_to_modern_converter: Optional[LegacyToModernConverter] = None,
    ):
        super().__init__()

        # Create the pure service
        self._service = SequenceLoaderService(
            workbench_getter=workbench_getter,
            workbench_setter=workbench_setter,
            legacy_to_modern_converter=legacy_to_modern_converter,
        )

        # Connect service callbacks to Qt signals
        self._service.add_sequence_loaded_callback(self._on_sequence_loaded)
        self._service.add_start_position_loaded_callback(self._on_start_position_loaded)

    def _on_sequence_loaded(self, sequence_data: SequenceData):
        """Convert service callback to Qt signal."""
        self.sequence_loaded.emit(sequence_data)

    def _on_start_position_loaded(self, beat_data: object, position_key: str):
        """Convert service callback to Qt signal."""
        self.start_position_loaded.emit(beat_data, position_key)

    # Delegate all service methods to the pure service
    def load_sequence_on_startup(self):
        """Load sequence from current_sequence.json on startup."""
        return self._service.load_sequence_on_startup()

    def get_current_sequence_from_workbench(self) -> Optional[SequenceData]:
        """Get the current sequence from workbench."""
        return self._service.get_current_sequence_from_workbench()

    def load_sequence_from_file(self, filepath: str) -> Optional[SequenceData]:
        """Load sequence from file."""
        return self._service.load_sequence_from_file(filepath)

    def load_current_sequence(self) -> Optional[SequenceData]:
        """Load the current sequence from default location."""
        return self._service.load_current_sequence()
