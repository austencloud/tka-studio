"""
Learn Tab State Management Package

Provides immutable state models and reactive state management for the learn tab.
This package implements modern state management patterns with clear separation
of concerns and predictable state transitions.
"""

from __future__ import annotations

from desktop.modern.presentation.managers.learn.learn_state_manager import (
    LearnStateManager,
)

from .learn_exceptions import (
    AnswerValidationError,
    ConfigurationError,
    DataCorruptionError,
    ErrorRecoveryStrategy,
    InvalidStateTransition,
    LearnError,
    LessonNotAvailable,
    NetworkError,
    ProgressCalculationError,
    QuestionGenerationError,
    SessionCreationError,
    UIRenderingError,
)
from .learn_state import (
    ErrorState,
    ErrorType,
    LayoutMode,
    LearnState,
    LearnView,
    ProgressState,
    UIState,
)


__all__ = [
    # State models
    "LearnState",
    "LearnView",
    "LayoutMode",
    "ErrorType",
    "ErrorState",
    "UIState",
    "ProgressState",
    # State manager
    "LearnStateManager",
    # Exceptions
    "LearnError",
    "InvalidStateTransition",
    "LessonNotAvailable",
    "SessionCreationError",
    "QuestionGenerationError",
    "AnswerValidationError",
    "ProgressCalculationError",
    "UIRenderingError",
    "DataCorruptionError",
    "NetworkError",
    "ConfigurationError",
    "ErrorRecoveryStrategy",
]
