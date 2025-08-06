from __future__ import annotations

from typing import TYPE_CHECKING

from base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat_grabber import (
    BeatGrabber,
)
from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat_start_text_manager import (
    BeatStartTextItem,
)

from .beat_number_item import BeatNumberItem

if TYPE_CHECKING:
    from base_widgets.base_beat_frame import BaseBeatFrame
    from base_widgets.pictograph.elements.views.beat_view import LegacyBeatView


class Beat(LegacyPictograph):
    view: "LegacyBeatView" = None
    is_placeholder = False
    parent_beat = None
    beat_number = 0

    def __init__(self, beat_frame: "BaseBeatFrame", duration: int | float = 1):
        super().__init__()
        self.beat_number_item = BeatNumberItem(self)
        self.grabber = BeatGrabber(self)
        self.duration = duration
        self.start_text_item = BeatStartTextItem(self)
