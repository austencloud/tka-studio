"""
Modern Learn Tab Package

Complete implementation of the learn tab for the modern architecture
including domain models, services, and UI components.
"""

from .learn_tab import LearnTab
from .components import (
    LessonSelectorPanel,
    LessonWidgetPanel,
    LessonResultsPanel,
    QuestionDisplay,
    AnswerOptions,
    LessonProgressBar,
    LessonTimer,
    LessonControls,
    LessonModeToggle,
    LessonButton,
)

__all__ = [
    # Main Learn Tab
    "LearnTab",
    # Main Panels
    "LessonSelectorPanel",
    "LessonWidgetPanel",
    "LessonResultsPanel",
    # Individual Components
    "QuestionDisplay",
    "AnswerOptions",
    "LessonProgressBar",
    "LessonTimer",
    "LessonControls",
    "LessonModeToggle",
    "LessonButton",
]
