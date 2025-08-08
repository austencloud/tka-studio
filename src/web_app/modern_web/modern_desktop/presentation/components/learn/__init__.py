"""
Learn Tab Specialized Components Package

Focused, single-responsibility components for the lesson workspace.
Each component handles one specific aspect of the lesson interface.
"""

from __future__ import annotations

from .answer_options import AnswerLayoutManager, AnswerOptionFactory, AnswerOptions
from .lesson_controls import LessonControls
from .lesson_timer import LessonTimer
from .progress_controls import ProgressControls, ProgressInfo
from .question_display import (
    LetterQuestionRenderer,
    PictographQuestionRenderer,
    QuestionDisplay,
    QuestionRenderer,
    TextQuestionRenderer,
)


__all__ = [
    # Main components
    "QuestionDisplay",
    "AnswerOptions",
    "ProgressControls",
    "LessonTimer",
    "LessonControls",
    # Supporting classes
    "QuestionRenderer",
    "PictographQuestionRenderer",
    "LetterQuestionRenderer",
    "TextQuestionRenderer",
    "AnswerOptionFactory",
    "AnswerLayoutManager",
    "ProgressInfo",
]
