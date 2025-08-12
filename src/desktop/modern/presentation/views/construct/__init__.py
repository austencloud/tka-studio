"""
Construct Tab Components

This package contains the UI components of the ConstructTabWidget,
following proper separation of concerns between presentation and business logic.

Presentation Components (in this package):
- ConstructTabLayoutManager: Handles UI layout and panel creation
- ConstructTabServiceOrchestrator: Lightweight coordinator for existing services
- StartPositionHandler: Manages start position UI interactions
- OptionPickerManager: Handles option picker UI management
- SignalCoordinator: Coordinates signals between UI components

Business Logic Services (moved to application layer):
- SequenceLoadingService: Handles sequence loading from persistence
- SequenceBeatOperations: Manages beat-level operations
- SequenceStartPositionManager: Manages start position operations
- SequenceDataConverter: Handles data conversion between formats (enhanced with caching)

Architecture Notes:
- Replaced ConstructTabController god class with direct service delegation
- Uses existing SignalCoordinator and service architecture
- Maintains same public API for backward compatibility
- No unnecessary orchestration layer
"""

from __future__ import annotations

from desktop.modern.application.services.sequence.sequence_beat_operations import (
    SequenceBeatOperations,
)
from desktop.modern.application.services.sequence.sequence_start_position_manager import (
    SequenceStartPositionManager,
)

# Services moved to application layer
from desktop.modern.presentation.adapters.qt.sequence_loader_adapter import (
    QtSequenceLoaderAdapter,
)
from desktop.modern.presentation.components.option_picker.option_picker_manager import (
    OptionPickerManager,
)
from desktop.modern.presentation.components.start_position_picker.start_position_selection_handler import (
    StartPositionSelectionHandler,
)
from desktop.modern.presentation.controllers.construct.signal_coordinator import (
    SignalCoordinator,
)
from desktop.modern.presentation.managers.construct.layout_manager import (
    ConstructTabLayoutManager,
)
from desktop.modern.presentation.views.construct.construct_tab import ConstructTab


# Create alias for backward compatibility
ModernConstructTab = ConstructTab

__all__ = [
    "ConstructTab",
    # Presentation components (local)
    "ConstructTabLayoutManager",
    "ModernConstructTab",  # Alias for backward compatibility
    "OptionPickerManager",
    # Business services (re-exported from application layer)
    "QtSequenceLoaderAdapter",
    "SequenceBeatOperations",
    "SequenceStartPositionManager",
    "SignalCoordinator",
    "StartPositionSelectionHandler",
]
