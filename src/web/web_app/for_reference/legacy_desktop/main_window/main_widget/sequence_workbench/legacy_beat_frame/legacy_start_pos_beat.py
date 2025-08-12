from __future__ import annotations

from typing import TYPE_CHECKING

from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import Beat

if TYPE_CHECKING:
    from base_widgets.base_beat_frame import BaseBeatFrame


class LegacyStartPositionBeat(Beat):
    def __init__(self, beat_frame: "BaseBeatFrame") -> None:
        super().__init__(beat_frame)
        self.beat_frame = beat_frame
