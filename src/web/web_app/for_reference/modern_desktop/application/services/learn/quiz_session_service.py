"""
Quiz Session Service Implementation

Manages quiz sessions, state tracking, and session lifecycle
for the learning module.
"""

from __future__ import annotations

from datetime import datetime
import logging

from desktop.modern.core.interfaces.learn_services import IQuizSessionService
from desktop.modern.domain.models.learn import LessonType, QuizMode, QuizSession


logger = logging.getLogger(__name__)


class QuizSessionService(IQuizSessionService):
    """
    Production implementation of quiz session management.

    Handles session creation, state updates, and lifecycle management
    with proper error handling and logging.
    """

    def __init__(self):
        """Initialize quiz session service."""
        self._active_sessions: dict[str, QuizSession] = {}
        self._completed_sessions: dict[str, QuizSession] = {}

        logger.info("Quiz session service initialized")

    def create_session(self, lesson_type: LessonType, quiz_mode: QuizMode) -> str:
        """
        Create new quiz session and return session ID.

        Args:
            lesson_type: Type of lesson for this session
            quiz_mode: Quiz mode (fixed questions or countdown)

        Returns:
            Unique session identifier

        Raises:
            ValueError: If invalid lesson type or quiz mode provided
        """
        try:
            # Validate inputs
            if not isinstance(lesson_type, LessonType):
                raise ValueError(f"Invalid lesson type: {lesson_type}")

            if not isinstance(quiz_mode, QuizMode):
                raise ValueError(f"Invalid quiz mode: {quiz_mode}")

            # Create session with appropriate configuration
            session = QuizSession(
                lesson_type=lesson_type,
                quiz_mode=quiz_mode,
                total_questions=20 if quiz_mode == QuizMode.FIXED_QUESTION else 0,
                quiz_time=120 if quiz_mode == QuizMode.COUNTDOWN else 0,
            )

            # Store in active sessions
            self._active_sessions[session.session_id] = session

            logger.info(
                f"Created quiz session {session.session_id} for {lesson_type.value} "
                f"in {quiz_mode.value} mode"
            )

            return session.session_id

        except Exception as e:
            logger.error(f"Failed to create quiz session: {e}")
            raise

    def get_session(self, session_id: str) -> QuizSession | None:
        """
        Get quiz session by ID.

        Args:
            session_id: Unique session identifier

        Returns:
            Quiz session or None if not found
        """
        if not session_id:
            return None

        # Check active sessions first
        session = self._active_sessions.get(session_id)
        if session:
            return session

        # Check completed sessions
        session = self._completed_sessions.get(session_id)
        if session:
            return session

        logger.warning(f"Session not found: {session_id}")
        return None

    def update_session_progress(self, session_id: str, **updates) -> bool:
        """
        Update session progress data.

        Args:
            session_id: Session to update
            **updates: Key-value pairs of fields to update

        Returns:
            True if update successful, False otherwise
        """
        try:
            session = self._active_sessions.get(session_id)
            if not session:
                logger.warning(
                    f"Cannot update inactive or non-existent session: {session_id}"
                )
                return False

            # Validate and apply updates
            valid_fields = {
                "current_question",
                "questions_answered",
                "correct_answers",
                "incorrect_guesses",
                "quiz_time",
                "is_active",
                "is_completed",
            }

            applied_updates = []
            for key, value in updates.items():
                if key in valid_fields and hasattr(session, key):
                    old_value = getattr(session, key)
                    setattr(session, key, value)
                    applied_updates.append(f"{key}: {old_value} → {value}")
                else:
                    logger.warning(
                        f"Invalid update field for session {session_id}: {key}"
                    )

            # Always update interaction timestamp
            session.mark_interaction()

            if applied_updates:
                logger.debug(
                    f"Updated session {session_id}: {', '.join(applied_updates)}"
                )

            return True

        except Exception as e:
            logger.error(f"Failed to update session {session_id}: {e}")
            return False

    def end_session(self, session_id: str) -> bool:
        """
        Mark session as completed and move to completed sessions.

        Args:
            session_id: Session to end

        Returns:
            True if session ended successfully, False otherwise
        """
        try:
            session = self._active_sessions.get(session_id)
            if not session:
                logger.warning(
                    f"Cannot end inactive or non-existent session: {session_id}"
                )
                return False

            # Mark session as completed
            session.complete_session()

            # Move from active to completed
            self._completed_sessions[session_id] = session
            del self._active_sessions[session_id]

            logger.info(
                f"Ended session {session_id}: {session.correct_answers}/{session.questions_answered} "
                f"correct ({session.accuracy_percentage:.1f}%)"
            )

            return True

        except Exception as e:
            logger.error(f"Failed to end session {session_id}: {e}")
            return False

    def get_active_sessions(self) -> list[QuizSession]:
        """
        Get all currently active sessions.

        Returns:
            List of active quiz sessions
        """
        try:
            return list(self._active_sessions.values())
        except Exception as e:
            logger.error(f"Failed to get active sessions: {e}")
            return []

    def get_completed_sessions(self) -> list[QuizSession]:
        """
        Get all completed sessions.

        Returns:
            List of completed quiz sessions
        """
        try:
            return list(self._completed_sessions.values())
        except Exception as e:
            logger.error(f"Failed to get completed sessions: {e}")
            return []

    def cleanup_old_sessions(self, max_age_hours: int = 24) -> int:
        """
        Clean up old inactive sessions to prevent memory leaks.

        Args:
            max_age_hours: Maximum age in hours before cleanup

        Returns:
            Number of sessions cleaned up
        """
        try:
            from datetime import timedelta

            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            cleaned_count = 0

            # Clean up old active sessions (shouldn't happen normally)
            active_to_remove = []
            for session_id, session in self._active_sessions.items():
                if session.last_interaction < cutoff_time:
                    active_to_remove.append(session_id)

            for session_id in active_to_remove:
                del self._active_sessions[session_id]
                cleaned_count += 1
                logger.info(f"Cleaned up old active session: {session_id}")

            # Clean up old completed sessions
            completed_to_remove = []
            for session_id, session in self._completed_sessions.items():
                if session.last_interaction < cutoff_time:
                    completed_to_remove.append(session_id)

            for session_id in completed_to_remove:
                del self._completed_sessions[session_id]
                cleaned_count += 1
                logger.debug(f"Cleaned up old completed session: {session_id}")

            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} old sessions")

            return cleaned_count

        except Exception as e:
            logger.error(f"Failed to cleanup old sessions: {e}")
            return 0

    def get_session_statistics(self) -> dict[str, int]:
        """
        Get session statistics for monitoring.

        Returns:
            Dictionary with session counts and statistics
        """
        try:
            return {
                "active_sessions": len(self._active_sessions),
                "completed_sessions": len(self._completed_sessions),
                "total_sessions": len(self._active_sessions)
                + len(self._completed_sessions),
            }
        except Exception as e:
            logger.error(f"Failed to get session statistics: {e}")
            return {"active_sessions": 0, "completed_sessions": 0, "total_sessions": 0}
