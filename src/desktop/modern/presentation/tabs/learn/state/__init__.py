"""
Learn Tab State Management Package

Provides immutable state models and reactive state management for the learn tab.
This package implements modern state management patterns with clear separation
of concerns and predictable state transitions.
"""

from .learn_state import (
    LearnState,
    LearnView,
    LayoutMode,
    ErrorType,
    ErrorState,
    UIState,
    ProgressState
)

from .learn_state_manager import LearnStateManager

from .learn_exceptions import (
    LearnError,
    InvalidStateTransition,
    LessonNotAvailable,
    SessionCreationError,
    QuestionGenerationError,
    AnswerValidationError,
    ProgressCalculationError,
    UIRenderingError,
    DataCorruptionError,
    NetworkError,
    ConfigurationError,
    ErrorRecoveryStrategy
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
    "ErrorRecoveryStrategy"
]
