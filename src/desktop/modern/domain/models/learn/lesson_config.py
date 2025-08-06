"""
Lesson Configuration Domain Models

Defines lesson types, quiz modes, and configuration data structures
for the learning module.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class LessonType(Enum):
    """Types of lessons available in the learning module."""

    PICTOGRAPH_TO_LETTER = "pictograph_to_letter"
    LETTER_TO_PICTOGRAPH = "letter_to_pictograph"
    VALID_NEXT_PICTOGRAPH = "valid_next_pictograph"


class QuizMode(Enum):
    """Quiz modes for lesson execution."""

    FIXED_QUESTION = "fixed_question"
    COUNTDOWN = "countdown"


@dataclass
class LessonConfig:
    """
    Configuration data for a lesson type.

    Contains all static configuration needed to set up and run a lesson,
    including display formats, prompts, and quiz parameters.
    """

    lesson_type: LessonType
    question_format: str
    answer_format: str
    quiz_description: str
    question_prompt: str

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize configuration to dictionary for session state.

        Returns:
            Dictionary representation with enum values serialized as strings
        """
        return {
            "lesson_type": self.lesson_type.value,
            "question_format": self.question_format,
            "answer_format": self.answer_format,
            "quiz_description": self.quiz_description,
            "question_prompt": self.question_prompt,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LessonConfig:
        """
        Deserialize configuration from dictionary.

        Args:
            data: Dictionary containing configuration data

        Returns:
            LessonConfig instance
        """
        return cls(
            lesson_type=LessonType(data["lesson_type"]),
            question_format=data["question_format"],
            answer_format=data["answer_format"],
            quiz_description=data["quiz_description"],
            question_prompt=data["question_prompt"],
        )
