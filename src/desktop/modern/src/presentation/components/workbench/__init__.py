"""
Sequence Workbench Components

Modern sequence workbench with modern architecture.
"""

from presentation.components.workbench.sequence_beat_frame import (
    SequenceBeatFrame,
    BeatView,
    StartPositionView,
    BeatSelectionManager,
)

from .workbench import (
    SequenceWorkbench,
)

from .indicator_section import WorkbenchIndicatorSection
from .beat_frame_section import WorkbenchBeatFrameSection
from .event_controller import WorkbenchEventController
from .button_interface import (
    WorkbenchButtonInterfaceAdapter,
    IWorkbenchButtonInterface,
    WorkbenchButtonSignals,
    ButtonOperationResult,
)

# Legacy compatibility
from .button_interface import (
    WorkbenchButtonInterfaceAdapter as ButtonInterface,
)

__all__ = [
    "SequenceWorkbench",
    "SequenceBeatFrame",
    "BeatView",
    "StartPositionView",
    "BeatSelectionManager",
    # Core components
    "WorkbenchIndicatorSection",
    "WorkbenchBeatFrameSection",
    "WorkbenchEventController",
    # Interface adapters
    "WorkbenchButtonInterfaceAdapter",
    "IWorkbenchButtonInterface",
    "WorkbenchButtonSignals",
    "ButtonOperationResult",
    "ButtonInterface",  # Legacy alias
]
