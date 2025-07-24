"""
Image Export Drawers
===================

This module contains drawer classes for rendering different components of exported images,
following the Legacy system's drawer pattern but using Modern dependency injection.

Each drawer is responsible for a specific aspect of image rendering:
- WordDrawer: Renders word text with legacy-compatible font scaling
- UserInfoDrawer: Renders user information (name, date, notes)
- DifficultyLevelDrawer: Renders difficulty level indicators
- BeatDrawer: Renders sequence beats and pictographs
- FontMarginHelper: Provides font and margin calculations using exact legacy logic
"""

from .word_drawer import WordDrawer
from .user_info_drawer import UserInfoDrawer
from .difficulty_level_drawer import DifficultyLevelDrawer
from .beat_drawer import BeatDrawer
from .font_margin_helper import FontMarginHelper

__all__ = [
    "WordDrawer",
    "UserInfoDrawer", 
    "DifficultyLevelDrawer",
    "BeatDrawer",
    "FontMarginHelper",
]
