"""
Write Tab UI Components

UI components for write tab functionality including act browsing,
editing interface, and music player controls.
"""

from __future__ import annotations

from .act_browser_component import ActBrowserComponent, ActThumbnailWidget
from .act_sheet_component import (
    ActHeaderComponent,
    ActSheetComponent,
    SequenceGridComponent,
    SequenceThumbnailWidget,
)
from .music_player_component import MusicPlayerComponent


__all__ = [
    "ActBrowserComponent",
    "ActHeaderComponent",
    "ActSheetComponent",
    "ActThumbnailWidget",
    "MusicPlayerComponent",
    "SequenceGridComponent",
    "SequenceThumbnailWidget",
]
