"""
Improved Qt Sequence Loader Adapter

This adapter wraps the pure SequenceLoaderService and provides Qt signal coordination.
Now uses proper dependency injection with IWorkbenchStateManager instead of clumsy getter/setter functions.

Benefits:
- Clean, typed dependencies
- Better testability
- Loose coupling
- Proper dependency injection patterns
"""

from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal
from shared.application.services.data.legacy_to_modern_converter import (
    LegacyToModernConverter,
)
from shared.application.services.sequence.sequence_loader_service import (
    SequenceLoaderService,
)

from desktop.modern.core.interfaces.workbench_services import IWorkbenchStateManager
from desktop.modern.domain.models.sequence_data import SequenceData


class QtSequenceLoaderAdapter(QObject):
    """
    Improved Qt adapter for the SequenceLoaderService.

    Uses proper dependency injection with IWorkbenchStateManager instead of
    passing getter/setter functions around.

    Benefits:
    - Type-safe dependencies
    - Better error handling
    - Easier testing
    - Clear interface contracts
    - Loose coupling
    """

    # Qt signals for UI coordination
    sequence_loaded = pyqtSignal(object)  # SequenceData object
    start_position_loaded = pyqtSignal(object, str)  # BeatData object, position_key

    def __init__(
        self,
        workbench_state_manager: IWorkbenchStateManager,
        legacy_to_modern_converter: Optional[LegacyToModernConverter] = None,
    ):
        super().__init__()

        self._workbench_state_manager = workbench_state_manager

        # Create the pure service
        self._service = SequenceLoaderService(
            workbench_state_manager=workbench_state_manager,
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

    def is_workbench_ready(self) -> bool:
        """Check if workbench is available for operations."""
        return self._workbench_state_manager is not None
