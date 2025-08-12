"""
Answer Validation Service Implementation

Validates quiz answers and tracks answer history for scoring
and progress tracking.
"""

from __future__ import annotations

import logging
from typing import Any

from desktop.modern.core.interfaces.learn_services import (
    IAnswerValidationService,
    IQuizSessionService,
)
from desktop.modern.domain.models.learn import QuestionData


logger = logging.getLogger(__name__)


class AnswerValidationService(IAnswerValidationService):
    """
    Production implementation of answer validation for quiz lessons.

    Handles answer checking, score tracking, and answer history
    with proper error handling and logging.
    """

    def __init__(self, session_service: IQuizSessionService):
        """
        Initialize answer validation service.

        Args:
            session_service: Service for session management
        """
        self.session_service = session_service

        # Track answer history per session
        self._answer_history: dict[str, list[tuple[str, bool]]] = {}

        logger.info("Answer validation service initialized")

    def check_answer(self, question: QuestionData, selected_answer: Any) -> bool:
        """
        Check if selected answer is correct.

        Args:
            question: The question being answered
            selected_answer: Answer selected by user

        Returns:
            True if answer is correct, False otherwise
        """
        try:
            if not question or question.correct_answer is None:
                logger.warning("Cannot check answer for invalid question")
                return False

            # Handle different answer types
            is_correct = self._compare_answers(question.correct_answer, selected_answer)

            logger.debug(
                f"Answer check for question {question.question_id}: "
                f"selected={selected_answer}, correct={question.correct_answer}, "
                f"result={is_correct}"
            )

            return is_correct

        except Exception as e:
            logger.error(
                f"Failed to check answer for question {question.question_id}: {e}"
            )
            return False

    def _compare_answers(self, correct_answer: Any, selected_answer: Any) -> bool:
        """
        Compare answers handling different data types.

        Args:
            correct_answer: The correct answer
            selected_answer: The selected answer

        Returns:
            True if answers match, False otherwise
        """
        try:
            # Direct comparison for simple types
            if correct_answer == selected_answer:
                return True

            # String comparison (case-insensitive)
            if isinstance(correct_answer, str) and isinstance(selected_answer, str):
                return correct_answer.lower() == selected_answer.lower()

            # Dictionary comparison for pictographs
            if isinstance(correct_answer, dict) and isinstance(selected_answer, dict):
                return self._compare_pictographs(correct_answer, selected_answer)

            # Type conversion attempts
            try:
                if str(correct_answer) == str(selected_answer):
                    return True
            except:
                pass

            return False

        except Exception as e:
            logger.error(f"Failed to compare answers: {e}")
            return False

    def _compare_pictographs(self, correct: dict, selected: dict) -> bool:
        """
        Compare pictograph dictionaries for equality.

        Args:
            correct: Correct pictograph data
            selected: Selected pictograph data

        Returns:
            True if pictographs are equivalent, False otherwise
        """
        try:
            # Import constants safely
            try:
                from data.constants import END_POS, LETTER, START_POS

                key_fields = [LETTER, START_POS, END_POS]
            except ImportError:
                # Fallback to string keys
                key_fields = ["letter", "start_pos", "end_pos"]

            # Compare key fields
            for field in key_fields:
                if correct.get(field) != selected.get(field):
                    return False

            return True

        except Exception as e:
            logger.error(f"Failed to compare pictographs: {e}")
            return False

    def record_answer(self, session_id: str, question_id: str, correct: bool) -> None:
        """
        Record answer result for session tracking.

        Args:
            session_id: Session the answer belongs to
            question_id: Question that was answered
            correct: Whether the answer was correct
        """
        try:
            # Initialize history for session if needed
            if session_id not in self._answer_history:
                self._answer_history[session_id] = []

            # Record answer
            self._answer_history[session_id].append((question_id, correct))

            # Update session statistics
            session = self.session_service.get_session(session_id)
            if session:
                updates = {"questions_answered": len(self._answer_history[session_id])}

                if correct:
                    updates["correct_answers"] = session.correct_answers + 1
                else:
                    updates["incorrect_guesses"] = session.incorrect_guesses + 1

                success = self.session_service.update_session_progress(
                    session_id, **updates
                )
                if not success:
                    logger.warning(
                        f"Failed to update session progress for {session_id}"
                    )

            logger.debug(
                f"Recorded answer for session {session_id}, question {question_id}: "
                f"correct={correct}"
            )

        except Exception as e:
            logger.error(f"Failed to record answer for session {session_id}: {e}")

    def get_answer_history(self, session_id: str) -> list[tuple[str, bool]]:
        """
        Get answer history for a session.

        Args:
            session_id: Session to get history for

        Returns:
            List of tuples containing (question_id, correct)
        """
        try:
            return self._answer_history.get(session_id, [])
        except Exception as e:
            logger.error(f"Failed to get answer history for session {session_id}: {e}")
            return []

    def get_session_accuracy(self, session_id: str) -> float:
        """
        Calculate current accuracy percentage for a session.

        Args:
            session_id: Session to calculate accuracy for

        Returns:
            Accuracy percentage (0.0 to 100.0)
        """
        try:
            history = self.get_answer_history(session_id)
            if not history:
                return 0.0

            correct_count = sum(1 for _, correct in history if correct)
            return (correct_count / len(history)) * 100.0

        except Exception as e:
            logger.error(f"Failed to calculate accuracy for session {session_id}: {e}")
            return 0.0

    def get_correct_streak(self, session_id: str) -> int:
        """
        Get current streak of consecutive correct answers.

        Args:
            session_id: Session to check streak for

        Returns:
            Number of consecutive correct answers from the end
        """
        try:
            history = self.get_answer_history(session_id)
            if not history:
                return 0

            streak = 0
            for _, correct in reversed(history):
                if correct:
                    streak += 1
                else:
                    break

            return streak

        except Exception as e:
            logger.error(
                f"Failed to calculate correct streak for session {session_id}: {e}"
            )
            return 0

    def get_longest_streak(self, session_id: str) -> int:
        """
        Get longest streak of consecutive correct answers in session.

        Args:
            session_id: Session to check longest streak for

        Returns:
            Longest consecutive correct answer streak
        """
        try:
            history = self.get_answer_history(session_id)
            if not history:
                return 0

            max_streak = 0
            current_streak = 0

            for _, correct in history:
                if correct:
                    current_streak += 1
                    max_streak = max(max_streak, current_streak)
                else:
                    current_streak = 0

            return max_streak

        except Exception as e:
            logger.error(
                f"Failed to calculate longest streak for session {session_id}: {e}"
            )
            return 0

    def clear_session_history(self, session_id: str) -> bool:
        """
        Clear answer history for a session.

        Args:
            session_id: Session to clear history for

        Returns:
            True if history cleared successfully, False otherwise
        """
        try:
            if session_id in self._answer_history:
                del self._answer_history[session_id]
                logger.info(f"Cleared answer history for session {session_id}")

            return True

        except Exception as e:
            logger.error(f"Failed to clear history for session {session_id}: {e}")
            return False

    def get_statistics(self) -> dict[str, Any]:
        """
        Get service statistics for monitoring.

        Returns:
            Dictionary with service statistics
        """
        try:
            total_sessions = len(self._answer_history)
            total_answers = sum(
                len(history) for history in self._answer_history.values()
            )

            return {
                "tracked_sessions": total_sessions,
                "total_answers_recorded": total_answers,
                "average_answers_per_session": (
                    total_answers / total_sessions if total_sessions > 0 else 0
                ),
            }

        except Exception as e:
            logger.error(f"Failed to get validation service statistics: {e}")
            return {
                "tracked_sessions": 0,
                "total_answers_recorded": 0,
                "average_answers_per_session": 0,
            }
