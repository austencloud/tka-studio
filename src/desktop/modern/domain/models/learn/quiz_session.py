"""
Quiz Session Domain Model

Represents the state and progress of an active quiz session,
including timing, scoring, and progression data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid

from .lesson_config import LessonType, QuizMode


@dataclass
class QuizSession:
    """
    Represents an active quiz session with state and progress tracking.

    Maintains all data needed for lesson execution including timing,
    scoring, and current position within the quiz.
    """

    # Session identification
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # Lesson configuration
    lesson_type: LessonType | None = None
    quiz_mode: QuizMode | None = None

    # Progress tracking
    current_question: int = 1
    total_questions: int = 20
    questions_answered: int = 0
    correct_answers: int = 0
    incorrect_guesses: int = 0

    # Timing
    quiz_time: int = 120  # seconds remaining for countdown mode
    start_time: datetime = field(default_factory=datetime.now)
    last_interaction: datetime = field(default_factory=datetime.now)

    # State management
    is_active: bool = True
    is_completed: bool = False

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize session to dictionary with proper enum handling.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            "session_id": self.session_id,
            "lesson_type": self.lesson_type.value if self.lesson_type else None,
            "quiz_mode": self.quiz_mode.value if self.quiz_mode else None,
            "current_question": self.current_question,
            "total_questions": self.total_questions,
            "questions_answered": self.questions_answered,
            "correct_answers": self.correct_answers,
            "incorrect_guesses": self.incorrect_guesses,
            "quiz_time": self.quiz_time,
            "start_time": self.start_time.isoformat(),
            "last_interaction": self.last_interaction.isoformat(),
            "is_active": self.is_active,
            "is_completed": self.is_completed,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> QuizSession:
        """
        Deserialize session from dictionary.

        Args:
            data: Dictionary containing session data

        Returns:
            QuizSession instance
        """
        return cls(
            session_id=data["session_id"],
            lesson_type=LessonType(data["lesson_type"])
            if data.get("lesson_type")
            else None,
            quiz_mode=QuizMode(data["quiz_mode"]) if data.get("quiz_mode") else None,
            current_question=data["current_question"],
            total_questions=data["total_questions"],
            questions_answered=data["questions_answered"],
            correct_answers=data["correct_answers"],
            incorrect_guesses=data["incorrect_guesses"],
            quiz_time=data["quiz_time"],
            start_time=datetime.fromisoformat(data["start_time"]),
            last_interaction=datetime.fromisoformat(data["last_interaction"]),
            is_active=data["is_active"],
            is_completed=data["is_completed"],
        )

    @property
    def accuracy_percentage(self) -> float:
        """Calculate current accuracy percentage."""
        if self.questions_answered == 0:
            return 0.0
        return (self.correct_answers / self.questions_answered) * 100.0

    @property
    def elapsed_time_seconds(self) -> float:
        """Calculate elapsed time since session start."""
        return (datetime.now() - self.start_time).total_seconds()

    def mark_interaction(self) -> None:
        """Mark user interaction timestamp."""
        self.last_interaction = datetime.now()

    def complete_session(self) -> None:
        """Mark session as completed."""
        self.is_active = False
        self.is_completed = True
        self.mark_interaction()
