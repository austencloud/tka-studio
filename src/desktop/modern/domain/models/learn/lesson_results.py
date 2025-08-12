"""
Lesson Results Domain Model

Represents completion results and statistics for a finished lesson,
including scoring, timing, and performance metrics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .lesson_config import LessonType, QuizMode


@dataclass
class LessonResults:
    """
    Represents the final results and statistics for a completed lesson.

    Contains comprehensive performance data including accuracy, timing,
    and detailed scoring information.
    """

    # Session identification
    session_id: str

    # Lesson configuration
    lesson_type: LessonType
    quiz_mode: QuizMode

    # Core metrics
    total_questions: int
    correct_answers: int
    incorrect_guesses: int
    questions_answered: int

    # Performance metrics
    accuracy_percentage: float
    completion_time_seconds: float

    # Timing data
    completed_at: datetime = field(default_factory=datetime.now)

    # Additional statistics
    average_time_per_question: float | None = None
    streak_longest_correct: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize results to dictionary with proper enum handling.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            "session_id": self.session_id,
            "lesson_type": self.lesson_type.value,
            "quiz_mode": self.quiz_mode.value,
            "total_questions": self.total_questions,
            "correct_answers": self.correct_answers,
            "incorrect_guesses": self.incorrect_guesses,
            "questions_answered": self.questions_answered,
            "accuracy_percentage": self.accuracy_percentage,
            "completion_time_seconds": self.completion_time_seconds,
            "completed_at": self.completed_at.isoformat(),
            "average_time_per_question": self.average_time_per_question,
            "streak_longest_correct": self.streak_longest_correct,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LessonResults:
        """
        Deserialize results from dictionary.

        Args:
            data: Dictionary containing results data

        Returns:
            LessonResults instance
        """
        return cls(
            session_id=data["session_id"],
            lesson_type=LessonType(data["lesson_type"]),
            quiz_mode=QuizMode(data["quiz_mode"]),
            total_questions=data["total_questions"],
            correct_answers=data["correct_answers"],
            incorrect_guesses=data["incorrect_guesses"],
            questions_answered=data["questions_answered"],
            accuracy_percentage=data["accuracy_percentage"],
            completion_time_seconds=data["completion_time_seconds"],
            completed_at=datetime.fromisoformat(data["completed_at"]),
            average_time_per_question=data.get("average_time_per_question"),
            streak_longest_correct=data.get("streak_longest_correct"),
        )

    @property
    def grade_letter(self) -> str:
        """Calculate letter grade based on accuracy percentage."""
        if self.accuracy_percentage >= 90:
            return "A"
        if self.accuracy_percentage >= 80:
            return "B"
        if self.accuracy_percentage >= 70:
            return "C"
        if self.accuracy_percentage >= 60:
            return "D"
        return "F"

    @property
    def performance_level(self) -> str:
        """Get performance level description."""
        if self.accuracy_percentage >= 95:
            return "Excellent"
        if self.accuracy_percentage >= 85:
            return "Good"
        if self.accuracy_percentage >= 70:
            return "Fair"
        if self.accuracy_percentage >= 50:
            return "Needs Improvement"
        return "Poor"

    @property
    def minutes_taken(self) -> float:
        """Get completion time in minutes."""
        return self.completion_time_seconds / 60.0

    def calculate_score(self, max_points: int = 100) -> int:
        """
        Calculate numeric score out of maximum points.

        Args:
            max_points: Maximum possible score

        Returns:
            Calculated score based on accuracy percentage
        """
        return int((self.accuracy_percentage / 100.0) * max_points)
