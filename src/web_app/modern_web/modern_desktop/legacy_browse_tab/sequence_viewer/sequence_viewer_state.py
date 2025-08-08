from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.thumbnail_box.thumbnail_box_favorites_manager import (
        ThumbnailBox,
    )


class SequenceViewerState:
    def __init__(self):
        self.sequence_json: dict | None = None
        self.matching_thumbnail_box: ThumbnailBox | None = None
