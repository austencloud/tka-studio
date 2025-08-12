"""
Sequence Workbench Components

Modern sequence workbench with modern architecture.
"""

from __future__ import annotations

from desktop.modern.presentation.components.sequence_workbench.sequence_beat_frame import (
    BeatSelector,
    BeatView,
    SequenceBeatFrame,
    StartPositionView,
)

from .beat_frame_section import WorkbenchBeatFrameSection

# Legacy compatibility
from .button_interface import (
    ButtonOperationResult,
    IWorkbenchButtonInterface,
    WorkbenchButtonInterfaceAdapter,
    WorkbenchButtonInterfaceAdapter as ButtonInterface,
    WorkbenchButtonSignals,
)
from .indicator_section import WorkbenchIndicatorSection
from .sequence_workbench import SequenceWorkbench


__all__ = [
    "SequenceWorkbench",
    "SequenceBeatFrame",
    "BeatView",
    "StartPositionView",
    "BeatSelector",
    # Core components
    "WorkbenchIndicatorSection",
    "WorkbenchBeatFrameSection",
    # Interface adapters
    "WorkbenchButtonInterfaceAdapter",
    "IWorkbenchButtonInterface",
    "WorkbenchButtonSignals",
    "ButtonOperationResult",
    "ButtonInterface",  # Legacy alias
]
