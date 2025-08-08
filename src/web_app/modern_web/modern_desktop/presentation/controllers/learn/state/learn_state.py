"""
Learn Tab State Models

Immutable state models for the learn tab following modern reactive patterns.
These models represent the complete state of the learn tab at any point in time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from desktop.modern.domain.models.learn import LessonResults, QuestionData, QuizSession


class LearnView(Enum):
    """Available views in the learn tab."""

    LESSON_SELECTOR = "lesson_selector"
    LESSON_WORKSPACE = "lesson_workspace"
    LESSON_RESULTS = "lesson_results"


class LayoutMode(Enum):
    """Layout modes for lesson workspace."""

    VERTICAL = "vertical"  # Question top, answers bottom
    HORIZONTAL = "horizontal"  # Question left, answers right


class ErrorType(Enum):
    """Types of errors that can occur in the learn tab."""

    LESSON_UNAVAILABLE = "lesson_unavailable"
    SESSION_CREATION_FAILED = "session_creation_failed"
    QUESTION_GENERATION_FAILED = "question_generation_failed"
    ANSWER_VALIDATION_FAILED = "answer_validation_failed"
    PROGRESS_CALCULATION_FAILED = "progress_calculation_failed"
    UI_RENDERING_FAILED = "ui_rendering_failed"
    NETWORK_ERROR = "network_error"
    DATA_CORRUPTION = "data_corruption"


@dataclass(frozen=True)
class ErrorState:
    """Immutable error state information."""

    error_type: ErrorType
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    recoverable: bool = True
    context: dict | None = None


@dataclass(frozen=True)
class UIState:
    """Immutable UI state information."""

    layout_mode: LayoutMode = LayoutMode.VERTICAL
    is_loading: bool = False
    is_paused: bool = False
    show_feedback: bool = False
    feedback_message: str = ""
    feedback_type: str = "info"  # "info", "success", "error", "warning"

    # Responsive sizing state
    parent_width: int = 800
    parent_height: int = 600

    # Component visibility
    show_timer: bool = False
    show_progress: bool = True
    show_controls: bool = True


@dataclass(frozen=True)
class ProgressState:
    """Immutable progress tracking state."""

    current_question_number: int = 1
    total_questions: int = 20
    correct_answers: int = 0
    incorrect_attempts: int = 0
    questions_answered: int = 0

    # Timing information
    session_start_time: datetime | None = None
    current_question_start_time: datetime | None = None
    time_remaining: int | None = None  # seconds for countdown mode

    # Performance metrics
    average_time_per_question: float = 0.0
    accuracy_percentage: float = 0.0
    current_streak: int = 0
    longest_streak: int = 0


@dataclass(frozen=True)
class LearnState:
    """
    Immutable state container for the entire learn tab.

    This represents the complete state at any point in time and enables
    predictable state management with clear transitions.
    """

    # Navigation state
    current_view: LearnView = LearnView.LESSON_SELECTOR

    # Core lesson data
    current_session: QuizSession | None = None
    current_question: QuestionData | None = None
    lesson_results: LessonResults | None = None

    # State tracking
    ui_state: UIState = field(default_factory=UIState)
    progress_state: ProgressState = field(default_factory=ProgressState)
    error_state: ErrorState | None = None

    # Metadata
    last_updated: datetime = field(default_factory=datetime.now)
    state_version: int = 1

    def is_lesson_active(self) -> bool:
        """Check if a lesson is currently active."""
        return (
            self.current_view == LearnView.LESSON_WORKSPACE
            and self.current_session is not None
            and self.current_session.is_active
        )

    def is_in_error_state(self) -> bool:
        """Check if the tab is in an error state."""
        return self.error_state is not None

    def can_transition_to_lesson(self) -> bool:
        """Check if we can transition to lesson workspace."""
        return (
            self.current_view == LearnView.LESSON_SELECTOR
            and not self.is_in_error_state()
            and not self.ui_state.is_loading
        )

    def can_transition_to_results(self) -> bool:
        """Check if we can transition to results view."""
        return (
            self.current_view == LearnView.LESSON_WORKSPACE
            and self.current_session is not None
            and (
                self.current_session.is_completed
                or self.progress_state.questions_answered
                >= self.progress_state.total_questions
            )
        )

    def can_answer_question(self) -> bool:
        """Check if user can answer the current question."""
        return (
            self.is_lesson_active()
            and self.current_question is not None
            and not self.ui_state.is_paused
            and not self.ui_state.show_feedback
        )

    def needs_horizontal_layout(self) -> bool:
        """Check if current lesson needs horizontal layout."""
        if not self.current_session:
            return False

        from desktop.modern.domain.models.learn import LessonType

        return self.current_session.lesson_type == LessonType.VALID_NEXT_PICTOGRAPH

    def get_required_layout_mode(self) -> LayoutMode:
        """Get the required layout mode for current lesson."""
        return (
            LayoutMode.HORIZONTAL
            if self.needs_horizontal_layout()
            else LayoutMode.VERTICAL
        )
