"""
UI Automation Framework for TKA Modern Testing
==============================================

Provides automated UI interaction and validation capabilities for testing
the Modern image export system's user interface components.

Components:
- PickerNavigator: Automate StartPositionPicker and OptionPicker interactions
- BeatFrameValidator: Validate BeatFrame state and pictograph rendering
- WorkbenchController: Orchestrate complete workflow automation
"""

from .beat_frame_validator import BeatFrameValidator
from .picker_navigator import PickerNavigator
from .workbench_controller import SequenceSpec, WorkbenchController

__all__ = [
    "PickerNavigator",
    "BeatFrameValidator",
    "WorkbenchController",
    "SequenceSpec",
]
