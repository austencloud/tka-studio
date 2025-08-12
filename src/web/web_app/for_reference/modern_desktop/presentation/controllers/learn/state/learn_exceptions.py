"""
Learn Tab Exception Types

Specific exception types for the learn tab that enable proper error handling
and recovery strategies. Each exception type has a clear meaning and context.
"""

from __future__ import annotations

from typing import Any


class LearnError(Exception):
    """Base exception for all learn tab related errors."""

    def __init__(self, message: str, context: dict | None = None):
        super().__init__(message)
        self.context = context or {}


class InvalidStateTransition(LearnError):
    """Raised when an invalid state transition is attempted."""

    def __init__(self, from_state: str, to_state: str, reason: str = ""):
        message = f"Cannot transition from {from_state} to {to_state}"
        if reason:
            message += f": {reason}"
        super().__init__(message, {"from_state": from_state, "to_state": to_state})


class LessonNotAvailable(LearnError):
    """Raised when a requested lesson is not available."""

    def __init__(self, lesson_type: str, reason: str = ""):
        message = f"Lesson '{lesson_type}' is not available"
        if reason:
            message += f": {reason}"
        super().__init__(message, {"lesson_type": lesson_type})


class SessionCreationError(LearnError):
    """Raised when session creation fails."""

    def __init__(self, lesson_type: str, quiz_mode: str, reason: str = ""):
        message = f"Failed to create session for {lesson_type} in {quiz_mode} mode"
        if reason:
            message += f": {reason}"
        super().__init__(message, {"lesson_type": lesson_type, "quiz_mode": quiz_mode})


class QuestionGenerationError(LearnError):
    """Raised when question generation fails."""

    def __init__(self, session_id: str, lesson_type: str, reason: str = ""):
        message = f"Failed to generate question for session {session_id}"
        if reason:
            message += f": {reason}"
        super().__init__(
            message, {"session_id": session_id, "lesson_type": lesson_type}
        )


class AnswerValidationError(LearnError):
    """Raised when answer validation fails."""

    def __init__(self, question_id: str, answer: Any, reason: str = ""):
        message = f"Failed to validate answer for question {question_id}"
        if reason:
            message += f": {reason}"
        super().__init__(message, {"question_id": question_id, "answer": str(answer)})


class ProgressCalculationError(LearnError):
    """Raised when progress calculation fails."""

    def __init__(self, session_id: str, reason: str = ""):
        message = f"Failed to calculate progress for session {session_id}"
        if reason:
            message += f": {reason}"
        super().__init__(message, {"session_id": session_id})


class UIRenderingError(LearnError):
    """Raised when UI rendering fails."""

    def __init__(self, component: str, reason: str = ""):
        message = f"Failed to render UI component '{component}'"
        if reason:
            message += f": {reason}"
        super().__init__(message, {"component": component})


class DataCorruptionError(LearnError):
    """Raised when data corruption is detected."""

    def __init__(self, data_type: str, identifier: str, reason: str = ""):
        message = f"Data corruption detected in {data_type} '{identifier}'"
        if reason:
            message += f": {reason}"
        super().__init__(message, {"data_type": data_type, "identifier": identifier})


class NetworkError(LearnError):
    """Raised when network operations fail."""

    def __init__(self, operation: str, reason: str = ""):
        message = f"Network operation '{operation}' failed"
        if reason:
            message += f": {reason}"
        super().__init__(message, {"operation": operation})


class ConfigurationError(LearnError):
    """Raised when configuration is invalid or missing."""

    def __init__(self, config_type: str, reason: str = ""):
        message = f"Configuration error in '{config_type}'"
        if reason:
            message += f": {reason}"
        super().__init__(message, {"config_type": config_type})


# Error recovery strategies
class ErrorRecoveryStrategy:
    """Defines how to recover from specific error types."""

    @staticmethod
    def can_recover(error: LearnError) -> bool:
        """Check if an error is recoverable."""
        recoverable_types = (
            LessonNotAvailable,
            QuestionGenerationError,
            AnswerValidationError,
            UIRenderingError,
            NetworkError,
        )
        return isinstance(error, recoverable_types)

    @staticmethod
    def get_recovery_action(error: LearnError) -> str:
        """Get the recommended recovery action for an error."""
        if isinstance(error, LessonNotAvailable):
            return "return_to_selector"
        if isinstance(error, QuestionGenerationError):
            return "retry_question_generation"
        if isinstance(error, AnswerValidationError):
            return "retry_validation"
        if isinstance(error, UIRenderingError):
            return "refresh_component"
        if isinstance(error, NetworkError):
            return "retry_operation"
        if isinstance(error, InvalidStateTransition):
            return "reset_to_safe_state"
        return "show_error_message"

    @staticmethod
    def get_user_message(error: LearnError) -> str:
        """Get a user-friendly error message."""
        if isinstance(error, LessonNotAvailable):
            return "This lesson is currently unavailable. Please try another lesson."
        if isinstance(error, QuestionGenerationError):
            return "Unable to generate the next question. Please try again."
        if isinstance(error, AnswerValidationError):
            return "There was an issue processing your answer. Please try again."
        if isinstance(error, UIRenderingError):
            return "Display issue encountered. Refreshing the interface..."
        if isinstance(error, NetworkError):
            return (
                "Network connection issue. Please check your connection and try again."
            )
        if isinstance(error, DataCorruptionError):
            return "Data integrity issue detected. Please restart the lesson."
        return "An unexpected error occurred. Please try again."
