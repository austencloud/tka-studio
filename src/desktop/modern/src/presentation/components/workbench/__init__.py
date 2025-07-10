"""
Sequence Workbench Components

Modern sequence workbench with modern architecture.
"""

from presentation.components.workbench.sequence_beat_frame import (
    BeatSelector,
    BeatView,
    SequenceBeatFrame,
    StartPositionView,
)

from .beat_frame_section import WorkbenchBeatFrameSection

# Legacy compatibility
from .button_interface import ButtonOperationResult, IWorkbenchButtonInterface
from .button_interface import WorkbenchButtonInterfaceAdapter
from .button_interface import WorkbenchButtonInterfaceAdapter as ButtonInterface
from .button_interface import WorkbenchButtonSignals
from .event_controller import WorkbenchEventController
from .indicator_section import WorkbenchIndicatorSection
from .workbench import SequenceWorkbench

__all__ = [
    "SequenceWorkbench",
    "SequenceBeatFrame",
    "BeatView",
    "StartPositionView",
    "BeatSelector",
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
