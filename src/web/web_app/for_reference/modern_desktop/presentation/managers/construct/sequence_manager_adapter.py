"""
Direct Microservices Access - Clean Dependency Injection

Components that need sequence operations should directly inject and use
the specific microservices they need instead of going through adapters.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.application.services.sequence.sequence_beat_operations import (
    SequenceBeatOperations,
)
from desktop.modern.application.services.sequence.sequence_start_position_manager import (
    SequenceStartPositionManager,
)
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.adapters.qt.sequence_loader_adapter import (
    QtSequenceLoaderAdapter,
)


logger = logging.getLogger(__name__)


class SequenceSignalEmitter(QObject):
    """
    Simple Qt signal emitter for sequence events.

    Components that need sequence operations should inject the specific
    microservices they need and use this for signal emission only.
    """

    sequence_modified = pyqtSignal(object)  # SequenceData object
    sequence_cleared = pyqtSignal()
    beat_added = pyqtSignal(object, int)  # BeatData, position
    beat_removed = pyqtSignal(int)  # position
    beat_updated = pyqtSignal(object, int)  # BeatData, position
    start_position_set = pyqtSignal(object)  # BeatData
    sequence_loaded = pyqtSignal(object)  # SequenceData

    def __init__(self):
        """Initialize the signal emitter."""
        super().__init__()


# Example of how components should use microservices directly:
class ExampleSequenceComponent:
    """
    Example showing how components should directly use microservices.

    Instead of adapters, components should:
    1. Inject only the microservices they actually need
    2. Use them directly without wrapper methods
    3. Emit signals through a simple signal emitter
    """

    def __init__(
        self,
        beat_operations: SequenceBeatOperations,
        start_position_manager: SequenceStartPositionManager | None = None,
        sequence_loader: QtSequenceLoaderAdapter | None = None,
        signal_emitter: SequenceSignalEmitter | None = None,
    ):
        """
        Initialize with only the microservices this component actually needs.

        Args:
            beat_operations: Required for beat operations
            start_position_manager: Optional, only if component needs start position ops
            sequence_loader: Optional, only if component needs loading ops
            signal_emitter: Optional signal emitter
        """
        self.beat_operations = beat_operations
        self.start_position_manager = start_position_manager
        self.sequence_loader = sequence_loader
        self.signal_emitter = signal_emitter

    def add_pictograph(self, pictograph_data: PictographData):
        """Example: Add pictograph directly using microservice."""
        self.beat_operations.add_pictograph_to_sequence(pictograph_data)
        # Signal emission is handled by the microservice itself

    def set_start_position(self, beat_data: BeatData):
        """Example: Set start position if this component needs that functionality."""
        if self.start_position_manager:
            self.start_position_manager.set_start_position(beat_data)
        else:
            logger.warning("Start position manager not available")
