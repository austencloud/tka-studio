"""
Question Data Domain Model

Represents quiz questions with content, options, and metadata
for the learning module.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import uuid


@dataclass
class QuestionData:
    """
    Represents a quiz question with content and answer options.

    Supports different question types (pictograph, letter, etc.) with
    flexible content and answer structures.
    """

    # Question identification
    question_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # Question content (pictograph dict, letter string, etc.)
    question_content: Any = None

    # Answer options (list of letters, pictographs, etc.)
    answer_options: list[Any] = field(default_factory=list)

    # Correct answer (matches one of the options)
    correct_answer: Any = None

    # Question metadata
    question_type: str = ""
    lesson_type: str = ""

    # Additional metadata
    generation_timestamp: str | None = None
    difficulty_level: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize question to dictionary.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            "question_id": self.question_id,
            "question_content": self.question_content,
            "answer_options": self.answer_options,
            "correct_answer": self.correct_answer,
            "question_type": self.question_type,
            "lesson_type": self.lesson_type,
            "generation_timestamp": self.generation_timestamp,
            "difficulty_level": self.difficulty_level,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> QuestionData:
        """
        Deserialize question from dictionary.

        Args:
            data: Dictionary containing question data

        Returns:
            QuestionData instance
        """
        return cls(
            question_id=data["question_id"],
            question_content=data["question_content"],
            answer_options=data["answer_options"],
            correct_answer=data["correct_answer"],
            question_type=data["question_type"],
            lesson_type=data["lesson_type"],
            generation_timestamp=data.get("generation_timestamp"),
            difficulty_level=data.get("difficulty_level"),
        )

    def is_valid(self) -> bool:
        """
        Validate question data integrity.

        Returns:
            True if question has valid content and correct answer is in options
        """
        if not self.question_content or not self.answer_options:
            return False

        if not self.correct_answer:
            return False

        # Check if correct answer is in the options
        return self.correct_answer in self.answer_options

    def get_incorrect_options(self) -> list[Any]:
        """
        Get list of incorrect answer options.

        Returns:
            List of options that are not the correct answer
        """
        return [
            option for option in self.answer_options if option != self.correct_answer
        ]
