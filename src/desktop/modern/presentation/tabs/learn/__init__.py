"""
Learn Tab Package

Modern learn tab implementation following clean architecture principles.
Provides a complete learning system with state management, controllers, and views.
"""

# Specialized components
from .components import (
    AnswerLayoutManager,
    AnswerOptionFactory,
    AnswerOptions,
    LessonControls,
    LessonTimer,
    LetterQuestionRenderer,
    PictographQuestionRenderer,
    ProgressControls,
    ProgressInfo,
    QuestionDisplay,
    QuestionRenderer,
    TextQuestionRenderer,
)

# Controllers
from .controllers import (
    LessonResultsController,
    LessonSelectorController,
    LessonWorkspaceController,
)
from .learn_tab import LearnTab
from .learn_tab_coordinator import LearnTabCoordinator

# State management
from .state import (
    AnswerValidationError,
    ConfigurationError,
    DataCorruptionError,
    ErrorRecoveryStrategy,
    ErrorState,
    ErrorType,
    InvalidStateTransition,
    LayoutMode,
    LearnError,
    LearnState,
    LearnStateManager,
    LearnView,
    LessonNotAvailable,
    NetworkError,
    ProgressCalculationError,
    ProgressState,
    QuestionGenerationError,
    SessionCreationError,
    UIRenderingError,
    UIState,
)

# Views
from .views import (
    LessonButton,
    LessonModeToggle,
    LessonResultsView,
    LessonSelectorView,
    LessonWorkspaceView,
    ResultsStatsWidget,
)

__all__ = [
    # Main classes
    "LearnTab",
    "LearnTabCoordinator",
    # State management
    "LearnState",
    "LearnStateManager",
    "LearnView",
    "LayoutMode",
    "ErrorType",
    "ErrorState",
    "UIState",
    "ProgressState",
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
    # Views
    "LessonSelectorView",
    "LessonWorkspaceView",
    "LessonResultsView",
    "LessonModeToggle",
    "LessonButton",
    "ResultsStatsWidget",
    # Controllers
    "LessonSelectorController",
    "LessonWorkspaceController",
    "LessonResultsController",
    # Specialized components
    "QuestionDisplay",
    "AnswerOptions",
    "ProgressControls",
    "LessonTimer",
    "LessonControls",
    "QuestionRenderer",
    "PictographQuestionRenderer",
    "LetterQuestionRenderer",
    "TextQuestionRenderer",
    "AnswerOptionFactory",
    "AnswerLayoutManager",
    "ProgressInfo",
]
