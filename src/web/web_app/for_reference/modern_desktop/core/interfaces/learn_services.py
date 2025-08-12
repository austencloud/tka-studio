"""
Learn Services Interfaces

Defines all service interfaces for the learning module including
lesson management, quiz sessions, question generation, and UI services.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from desktop.modern.domain.models.learn import (
    LessonConfig,
    LessonResults,
    LessonType,
    QuestionData,
    QuizMode,
    QuizSession,
)


class ILessonConfigurationService(ABC):
    """Service for managing lesson configurations and types."""

    @abstractmethod
    def get_all_lesson_configs(self) -> dict[str, LessonConfig]:
        """
        Get all available lesson configurations.

        Returns:
            Dictionary mapping lesson identifiers to configurations
        """

    @abstractmethod
    def get_lesson_config(self, lesson_type: LessonType) -> Optional[LessonConfig]:
        """
        Get configuration for specific lesson type.

        Args:
            lesson_type: Type of lesson to get configuration for

        Returns:
            Lesson configuration or None if not found
        """

    @abstractmethod
    def get_lesson_names(self) -> list[str]:
        """
        Get list of all lesson display names.

        Returns:
            List of human-readable lesson names
        """


class IQuizSessionService(ABC):
    """Service for managing quiz sessions and state."""

    @abstractmethod
    def create_session(self, lesson_type: LessonType, quiz_mode: QuizMode) -> str:
        """
        Create new quiz session and return session ID.

        Args:
            lesson_type: Type of lesson for this session
            quiz_mode: Quiz mode (fixed questions or countdown)

        Returns:
            Unique session identifier
        """

    @abstractmethod
    def get_session(self, session_id: str) -> Optional[QuizSession]:
        """
        Get quiz session by ID.

        Args:
            session_id: Unique session identifier

        Returns:
            Quiz session or None if not found
        """

    @abstractmethod
    def update_session_progress(self, session_id: str, **updates) -> bool:
        """
        Update session progress data.

        Args:
            session_id: Session to update
            **updates: Key-value pairs of fields to update

        Returns:
            True if update successful, False otherwise
        """

    @abstractmethod
    def end_session(self, session_id: str) -> bool:
        """
        Mark session as completed.

        Args:
            session_id: Session to end

        Returns:
            True if session ended successfully, False otherwise
        """

    @abstractmethod
    def get_active_sessions(self) -> list[QuizSession]:
        """
        Get all currently active sessions.

        Returns:
            List of active quiz sessions
        """


class IQuestionGenerationService(ABC):
    """Service for generating quiz questions."""

    @abstractmethod
    def generate_question(
        self, session_id: str, lesson_config: LessonConfig
    ) -> QuestionData:
        """
        Generate next question for the session.

        Args:
            session_id: Session to generate question for
            lesson_config: Configuration for the lesson type

        Returns:
            Generated question data
        """

    @abstractmethod
    def get_pictograph_dataset(self) -> dict[Any, list[dict]]:
        """
        Get pictograph dataset for question generation.

        Returns:
            Dictionary mapping letters to pictograph data lists
        """

    @abstractmethod
    def validate_question(self, question: QuestionData) -> bool:
        """
        Validate that a question is properly formed.

        Args:
            question: Question to validate

        Returns:
            True if question is valid, False otherwise
        """


class IAnswerValidationService(ABC):
    """Service for validating answers and tracking progress."""

    @abstractmethod
    def check_answer(self, question: QuestionData, selected_answer: Any) -> bool:
        """
        Check if selected answer is correct.

        Args:
            question: The question being answered
            selected_answer: Answer selected by user

        Returns:
            True if answer is correct, False otherwise
        """

    @abstractmethod
    def record_answer(self, session_id: str, question_id: str, correct: bool) -> None:
        """
        Record answer result for session tracking.

        Args:
            session_id: Session the answer belongs to
            question_id: Question that was answered
            correct: Whether the answer was correct
        """

    @abstractmethod
    def get_answer_history(self, session_id: str) -> list[tuple[str, bool]]:
        """
        Get answer history for a session.

        Args:
            session_id: Session to get history for

        Returns:
            List of tuples containing (question_id, correct)
        """


class ILessonProgressService(ABC):
    """Service for tracking lesson progress and completion."""

    @abstractmethod
    def get_progress_info(self, session_id: str) -> dict[str, Any]:
        """
        Get current progress information for display.

        Args:
            session_id: Session to get progress for

        Returns:
            Dictionary containing progress information
        """

    @abstractmethod
    def is_lesson_complete(self, session_id: str) -> bool:
        """
        Check if lesson should be completed.

        Args:
            session_id: Session to check

        Returns:
            True if lesson is complete, False otherwise
        """

    @abstractmethod
    def calculate_results(self, session_id: str) -> LessonResults:
        """
        Calculate final lesson results.

        Args:
            session_id: Session to calculate results for

        Returns:
            Complete lesson results with statistics
        """

    @abstractmethod
    def should_advance_to_next_question(self, session_id: str) -> bool:
        """
        Check if session should advance to next question.

        Args:
            session_id: Session to check

        Returns:
            True if should advance, False otherwise
        """


class ILearnUIService(ABC):
    """Service for learn tab UI state management."""

    @abstractmethod
    def get_font_sizes(self, widget_width: int, widget_height: int) -> dict[str, int]:
        """
        Calculate responsive font sizes.

        Args:
            widget_width: Current widget width
            widget_height: Current widget height

        Returns:
            Dictionary mapping font type to size
        """

    @abstractmethod
    def get_component_sizes(
        self, widget_width: int, widget_height: int
    ) -> dict[str, tuple[int, int]]:
        """
        Calculate responsive component sizes.

        Args:
            widget_width: Current widget width
            widget_height: Current widget height

        Returns:
            Dictionary mapping component type to (width, height) tuple
        """

    @abstractmethod
    def get_layout_spacing(
        self, widget_width: int, widget_height: int
    ) -> dict[str, int]:
        """
        Calculate responsive layout spacing.

        Args:
            widget_width: Current widget width
            widget_height: Current widget height

        Returns:
            Dictionary mapping spacing type to pixel value
        """


class ILearnNavigationService(ABC):
    """Service for learn tab navigation management."""

    @abstractmethod
    def navigate_to_lesson_selector(self) -> None:
        """Navigate to lesson selector view."""

    @abstractmethod
    def navigate_to_lesson(self, session_id: str) -> None:
        """
        Navigate to lesson view.

        Args:
            session_id: Session to navigate to
        """

    @abstractmethod
    def navigate_to_results(self, session_id: str) -> None:
        """
        Navigate to results view.

        Args:
            session_id: Session to show results for
        """

    @abstractmethod
    def get_current_view(self) -> str:
        """
        Get current view identifier.

        Returns:
            String identifier for current view
        """

    @abstractmethod
    def can_navigate_back(self) -> bool:
        """
        Check if back navigation is possible.

        Returns:
            True if can navigate back, False otherwise
        """


class ILearnDataService(ABC):
    """Service for learn tab data persistence and retrieval."""

    @abstractmethod
    def save_lesson_progress(
        self, session_id: str, progress_data: dict[str, Any]
    ) -> bool:
        """
        Save lesson progress to persistent storage.

        Args:
            session_id: Session to save progress for
            progress_data: Progress data to save

        Returns:
            True if save successful, False otherwise
        """

    @abstractmethod
    def load_lesson_progress(self, session_id: str) -> Optional[dict[str, Any]]:
        """
        Load lesson progress from persistent storage.

        Args:
            session_id: Session to load progress for

        Returns:
            Progress data or None if not found
        """

    @abstractmethod
    def save_lesson_results(self, results: LessonResults) -> bool:
        """
        Save lesson results to persistent storage.

        Args:
            results: Results to save

        Returns:
            True if save successful, False otherwise
        """

    @abstractmethod
    def get_lesson_history(
        self, lesson_type: LessonType, limit: int = 10
    ) -> list[LessonResults]:
        """
        Get lesson history for a specific lesson type.

        Args:
            lesson_type: Type of lesson to get history for
            limit: Maximum number of results to return

        Returns:
            List of lesson results ordered by completion date
        """
