"""
Lesson Progress Service Implementation

Tracks lesson progress, completion status, and calculates results
for quiz sessions.
"""

import logging
from typing import Any

from desktop.modern.core.interfaces.learn_services import (
    IAnswerValidationService,
    ILessonProgressService,
    IQuizSessionService,
)
from desktop.modern.domain.models.learn import LessonResults, QuizMode

logger = logging.getLogger(__name__)


class LessonProgressService(ILessonProgressService):
    """
    Production implementation of lesson progress tracking.

    Monitors session progress, determines completion status,
    and calculates comprehensive lesson results.
    """

    def __init__(
        self,
        session_service: IQuizSessionService,
        validation_service: IAnswerValidationService,
    ):
        """
        Initialize lesson progress service.

        Args:
            session_service: Service for session management
            validation_service: Service for answer validation and history
        """
        self.session_service = session_service
        self.validation_service = validation_service

        logger.info("Lesson progress service initialized")

    def get_progress_info(self, session_id: str) -> dict[str, Any]:
        """
        Get current progress information for display.

        Args:
            session_id: Session to get progress for

        Returns:
            Dictionary containing progress information
        """
        try:
            session = self.session_service.get_session(session_id)
            if not session:
                logger.warning(f"Session not found for progress info: {session_id}")
                return {}

            # Get answer history for additional metrics
            answer_history = self.validation_service.get_answer_history(session_id)
            current_streak = self.validation_service.get_correct_streak(session_id)
            accuracy = self.validation_service.get_session_accuracy(session_id)

            progress_info = {
                # Basic progress
                "current_question": session.current_question,
                "total_questions": session.total_questions,
                "questions_answered": session.questions_answered,
                "correct_answers": session.correct_answers,
                "incorrect_guesses": session.incorrect_guesses,
                # Time tracking
                "quiz_time_remaining": session.quiz_time,
                "elapsed_time_seconds": session.elapsed_time_seconds,
                # Performance metrics
                "accuracy_percentage": accuracy,
                "current_streak": current_streak,
                "longest_streak": self.validation_service.get_longest_streak(
                    session_id
                ),
                # Session state
                "quiz_mode": session.quiz_mode.value if session.quiz_mode else None,
                "lesson_type": session.lesson_type.value
                if session.lesson_type
                else None,
                "is_active": session.is_active,
                "is_completed": session.is_completed,
                # Display formatting
                "progress_text": self._format_progress_text(session),
                "time_display": self._format_time_display(session),
            }

            logger.debug(f"Progress info for session {session_id}: {progress_info}")
            return progress_info

        except Exception as e:
            logger.error(f"Failed to get progress info for session {session_id}: {e}")
            return {}

    def is_lesson_complete(self, session_id: str) -> bool:
        """
        Check if lesson should be completed.

        Args:
            session_id: Session to check

        Returns:
            True if lesson is complete, False otherwise
        """
        try:
            session = self.session_service.get_session(session_id)
            if not session:
                logger.warning(f"Session not found for completion check: {session_id}")
                return False

            # Check if already marked as completed
            if session.is_completed:
                return True

            # Check completion criteria based on quiz mode
            if session.quiz_mode == QuizMode.FIXED_QUESTION:
                # Fixed question mode: complete when all questions answered
                is_complete = session.current_question > session.total_questions
            elif session.quiz_mode == QuizMode.COUNTDOWN:
                # Countdown mode: complete when time expires
                is_complete = session.quiz_time <= 0
            else:
                logger.warning(
                    f"Unknown quiz mode for session {session_id}: {session.quiz_mode}"
                )
                return False

            if is_complete:
                logger.info(f"Lesson complete for session {session_id}")

            return is_complete

        except Exception as e:
            logger.error(
                f"Failed to check lesson completion for session {session_id}: {e}"
            )
            return False

    def calculate_results(self, session_id: str) -> LessonResults:
        """
        Calculate final lesson results.

        Args:
            session_id: Session to calculate results for

        Returns:
            Complete lesson results with statistics

        Raises:
            ValueError: If session not found or not completed
        """
        try:
            session = self.session_service.get_session(session_id)
            if not session:
                raise ValueError(f"Session not found: {session_id}")

            # Calculate metrics
            accuracy = self.validation_service.get_session_accuracy(session_id)
            longest_streak = self.validation_service.get_longest_streak(session_id)
            completion_time = session.elapsed_time_seconds

            # Calculate average time per question
            avg_time_per_question = None
            if session.questions_answered > 0:
                avg_time_per_question = completion_time / session.questions_answered

            # Create results object
            results = LessonResults(
                session_id=session_id,
                lesson_type=session.lesson_type,
                quiz_mode=session.quiz_mode,
                total_questions=session.total_questions,
                correct_answers=session.correct_answers,
                incorrect_guesses=session.incorrect_guesses,
                questions_answered=session.questions_answered,
                accuracy_percentage=accuracy,
                completion_time_seconds=completion_time,
                average_time_per_question=avg_time_per_question,
                streak_longest_correct=longest_streak,
            )

            logger.info(
                f"Calculated results for session {session_id}: "
                f"{results.correct_answers}/{results.questions_answered} correct "
                f"({results.accuracy_percentage:.1f}%) in {results.minutes_taken:.1f} minutes"
            )

            return results

        except Exception as e:
            logger.error(f"Failed to calculate results for session {session_id}: {e}")
            raise

    def should_advance_to_next_question(self, session_id: str) -> bool:
        """
        Check if session should advance to next question.

        Args:
            session_id: Session to check

        Returns:
            True if should advance, False otherwise
        """
        try:
            session = self.session_service.get_session(session_id)
            if not session:
                return False

            # Don't advance if lesson is complete
            if self.is_lesson_complete(session_id):
                return False

            # Don't advance if session is not active
            if not session.is_active:
                return False

            # For countdown mode, always advance if time remaining
            if session.quiz_mode == QuizMode.COUNTDOWN:
                return session.quiz_time > 0

            # For fixed question mode, advance if more questions remain
            if session.quiz_mode == QuizMode.FIXED_QUESTION:
                return session.current_question <= session.total_questions

            return False

        except Exception as e:
            logger.error(
                f"Failed to check if should advance for session {session_id}: {e}"
            )
            return False

    def _format_progress_text(self, session) -> str:
        """Format progress text for display."""
        try:
            if session.quiz_mode == QuizMode.COUNTDOWN:
                minutes, seconds = divmod(session.quiz_time, 60)
                return f"Time Remaining: {minutes}:{seconds:02d}"
            else:
                return f"{session.current_question}/{session.total_questions}"
        except Exception as e:
            logger.error(f"Failed to format progress text: {e}")
            return "Progress: N/A"

    def _format_time_display(self, session) -> str:
        """Format time display for UI."""
        try:
            if session.quiz_mode == QuizMode.COUNTDOWN:
                minutes, seconds = divmod(max(0, session.quiz_time), 60)
                return f"{minutes}:{seconds:02d}"
            else:
                elapsed_minutes = int(session.elapsed_time_seconds // 60)
                elapsed_seconds = int(session.elapsed_time_seconds % 60)
                return f"{elapsed_minutes}:{elapsed_seconds:02d}"
        except Exception as e:
            logger.error(f"Failed to format time display: {e}")
            return "0:00"

    def get_performance_summary(self, session_id: str) -> dict[str, Any]:
        """
        Get performance summary for a completed session.

        Args:
            session_id: Session to get summary for

        Returns:
            Dictionary with performance summary
        """
        try:
            session = self.session_service.get_session(session_id)
            if not session:
                return {}

            accuracy = self.validation_service.get_session_accuracy(session_id)
            longest_streak = self.validation_service.get_longest_streak(session_id)

            # Determine performance level
            if accuracy >= 95:
                performance_level = "Excellent"
                performance_color = "green"
            elif accuracy >= 85:
                performance_level = "Good"
                performance_color = "blue"
            elif accuracy >= 70:
                performance_level = "Fair"
                performance_color = "orange"
            elif accuracy >= 50:
                performance_level = "Needs Improvement"
                performance_color = "yellow"
            else:
                performance_level = "Poor"
                performance_color = "red"

            return {
                "accuracy_percentage": accuracy,
                "correct_answers": session.correct_answers,
                "total_questions": session.questions_answered,
                "incorrect_guesses": session.incorrect_guesses,
                "longest_streak": longest_streak,
                "completion_time_minutes": session.elapsed_time_seconds / 60.0,
                "performance_level": performance_level,
                "performance_color": performance_color,
                "quiz_mode": session.quiz_mode.value if session.quiz_mode else None,
                "lesson_type": session.lesson_type.value
                if session.lesson_type
                else None,
            }

        except Exception as e:
            logger.error(
                f"Failed to get performance summary for session {session_id}: {e}"
            )
            return {}
