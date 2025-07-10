"""
Construct Tab Components

This package contains the UI components of the ConstructTabWidget,
following proper separation of concerns between presentation and business logic.

Presentation Components (in this package):
- ConstructTabLayoutManager: Handles UI layout and panel creation
- StartPositionHandler: Manages start position UI interactions
- OptionPickerManager: Handles option picker UI management
- SignalCoordinator: Coordinates signals between UI components

Business Logic Services (moved to application layer):
- SequenceLoadingService: Handles sequence loading from persistence
- SequenceBeatOperations: Manages beat-level operations
- SequenceStartPositionManager: Manages start position operations
- SequenceDataConverter: Handles data conversion between formats (enhanced with caching)
"""

from application.services.data.sequence_data_converter import SequenceDataConverter
from application.services.sequence.sequence_beat_operations import (
    SequenceBeatOperations,
)

# Services moved to application layer
from application.services.sequence.loader import SequenceLoader
from application.services.sequence.sequence_start_position_manager import (
    SequenceStartPositionManager,
)

from .layout_manager import ConstructTabLayoutManager
from .option_picker_manager import OptionPickerManager
from .signal_coordinator import SignalCoordinator
from .start_position_handler import StartPositionHandler

__all__ = [
    # Presentation components (local)
    "ConstructTabLayoutManager",
    "StartPositionHandler",
    "OptionPickerManager",
    "SignalCoordinator",
    # Business services (re-exported from application layer)
    "SequenceLoader",
    "SequenceBeatOperations",
    "SequenceStartPositionManager",
    "SequenceDataConverter",
]
