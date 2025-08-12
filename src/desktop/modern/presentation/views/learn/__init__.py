"""
Learn Tab Views Package

Pure UI components for the learn tab with no business logic.
These components handle only UI rendering and event emission.
"""

from __future__ import annotations

from .learn_tab import LearnTab
from .lesson_results_view import LessonResultsView, ResultsStatsWidget
from .lesson_selector_view import LessonButton, LessonModeToggle, LessonSelectorView
from .lesson_workspace_view import LessonWorkspaceView


__all__ = [
    # Main tab
    "LearnTab",
    "LessonButton",
    # Sub-components
    "LessonModeToggle",
    "LessonResultsView",
    # Main views
    "LessonSelectorView",
    "LessonWorkspaceView",
    "ResultsStatsWidget",
]
