"""
Learn State Manager

Manages state transitions and validation for the learn tab following reactive patterns.
Provides a single source of truth for state with proper validation and event emission.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
import logging

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.domain.models.learn import LessonResults, QuestionData, QuizSession
from desktop.modern.presentation.controllers.learn.state.learn_exceptions import (
    ErrorRecoveryStrategy,
    InvalidStateTransition,
    LearnError,
)
from desktop.modern.presentation.controllers.learn.state.learn_state import (
    ErrorState,
    ErrorType,
    LayoutMode,
    LearnState,
    LearnView,
    ProgressState,
)


logger = logging.getLogger(__name__)


class LearnStateManager(QObject):
    """
    Manages state transitions with validation and events.

    Provides a reactive state management system where all state changes
    go through validation and emit events for UI updates.
    """

    # Signals for reactive updates
    state_changed = pyqtSignal(object)  # LearnState
    view_changed = pyqtSignal(str)  # LearnView.value
    error_occurred = pyqtSignal(object)  # ErrorState
    error_cleared = pyqtSignal()
    loading_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._state = LearnState()
        self._state_history = [self._state]  # For debugging and potential undo
        self._max_history = 10

        logger.debug("Learn state manager initialized")

    def get_state(self) -> LearnState:
        """Get current immutable state."""
        return self._state

    def transition_to_lesson_selector(self) -> None:
        """Transition to lesson selector view."""
        try:
            if self._state.current_view == LearnView.LESSON_SELECTOR:
                logger.debug("Already in lesson selector view")
                return

            # Clear any active session and errors
            new_state = replace(
                self._state,
                current_view=LearnView.LESSON_SELECTOR,
                current_session=None,
                current_question=None,
                lesson_results=None,
                error_state=None,
                ui_state=replace(
                    self._state.ui_state,
                    is_loading=False,
                    is_paused=False,
                    show_feedback=False,
                ),
                progress_state=ProgressState(),  # Reset progress
                last_updated=datetime.now(),
            )

            self._update_state(new_state)
            logger.info("Transitioned to lesson selector")

        except Exception as e:
            logger.exception(f"Failed to transition to lesson selector: {e}")
            self._handle_error(
                InvalidStateTransition(
                    self._state.current_view.value,
                    LearnView.LESSON_SELECTOR.value,
                    str(e),
                )
            )

    def transition_to_lesson_workspace(self, session: QuizSession) -> None:
        """Transition to lesson workspace with validation."""
        try:
            logger.debug(
                f"Transitioning to lesson workspace for {session.lesson_type.value if session else 'unknown'}"
            )

            if not session or not session.is_active:
                raise InvalidStateTransition(
                    self._state.current_view.value,
                    LearnView.LESSON_WORKSPACE.value,
                    "Session is not active",
                )

            if not self._state.can_transition_to_lesson():
                raise InvalidStateTransition(
                    self._state.current_view.value,
                    LearnView.LESSON_WORKSPACE.value,
                    "Current state does not allow lesson transition",
                )

            # Determine layout mode based on lesson type
            required_layout = (
                LayoutMode.HORIZONTAL
                if session.lesson_type.value == "valid_next_pictograph"
                else LayoutMode.VERTICAL
            )

            # Initialize progress state from session
            progress_state = ProgressState(
                current_question_number=session.current_question,
                total_questions=session.total_questions,
                correct_answers=session.correct_answers,
                incorrect_attempts=session.incorrect_guesses,
                questions_answered=session.questions_answered,
                session_start_time=session.start_time,
                time_remaining=(
                    session.quiz_time
                    if session.quiz_mode.value == "countdown"
                    else None
                ),
            )

            # Update UI state for lesson workspace
            ui_state = replace(
                self._state.ui_state,
                layout_mode=required_layout,
                show_timer=session.quiz_mode.value == "countdown",
                show_progress=True,
                show_controls=True,
                is_loading=False,
                is_paused=False,
            )

            new_state = replace(
                self._state,
                current_view=LearnView.LESSON_WORKSPACE,
                current_session=session,
                current_question=None,  # Will be set when question is generated
                lesson_results=None,
                error_state=None,
                ui_state=ui_state,
                progress_state=progress_state,
                last_updated=datetime.now(),
            )

            self._update_state(new_state)
            logger.info(
                f"Transitioned to lesson workspace for {session.lesson_type.value}"
            )

        except Exception as e:
            logger.exception(f"Failed to transition to lesson workspace: {e}")
            self._handle_error(
                e
                if isinstance(e, LearnError)
                else InvalidStateTransition(
                    self._state.current_view.value,
                    LearnView.LESSON_WORKSPACE.value,
                    str(e),
                )
            )

    def transition_to_results(self, results: LessonResults) -> None:
        """Transition to results view."""
        try:
            if not self._state.can_transition_to_results():
                raise InvalidStateTransition(
                    self._state.current_view.value,
                    LearnView.LESSON_RESULTS.value,
                    "Cannot transition to results from current state",
                )

            new_state = replace(
                self._state,
                current_view=LearnView.LESSON_RESULTS,
                lesson_results=results,
                current_question=None,
                ui_state=replace(
                    self._state.ui_state,
                    is_loading=False,
                    is_paused=False,
                    show_feedback=False,
                    show_timer=False,
                ),
                last_updated=datetime.now(),
            )

            self._update_state(new_state)
            logger.info("Transitioned to results view")

        except Exception as e:
            logger.exception(f"Failed to transition to results: {e}")
            self._handle_error(
                e
                if isinstance(e, LearnError)
                else InvalidStateTransition(
                    self._state.current_view.value,
                    LearnView.LESSON_RESULTS.value,
                    str(e),
                )
            )

    def update_current_question(self, question: QuestionData) -> None:
        """Update current question with validation."""
        try:
            if self._state.current_view != LearnView.LESSON_WORKSPACE:
                raise InvalidStateTransition(
                    self._state.current_view.value,
                    "question_update",
                    "Cannot update question outside lesson workspace",
                )

            new_state = replace(
                self._state,
                current_question=question,
                ui_state=replace(
                    self._state.ui_state, show_feedback=False, feedback_message=""
                ),
                last_updated=datetime.now(),
            )

            self._update_state(new_state)
            logger.debug(f"Updated current question: {question.question_id}")

        except Exception as e:
            logger.exception(f"Failed to update question: {e}")
            self._handle_error(e if isinstance(e, LearnError) else LearnError(str(e)))

    def update_progress(self, **kwargs) -> None:
        """Update progress state with given parameters."""
        try:
            current_progress = self._state.progress_state

            # Update only provided fields
            updated_progress = replace(current_progress, **kwargs)

            new_state = replace(
                self._state,
                progress_state=updated_progress,
                last_updated=datetime.now(),
            )

            self._update_state(new_state)
            logger.debug(f"Updated progress: {kwargs}")

        except Exception as e:
            logger.exception(f"Failed to update progress: {e}")
            self._handle_error(LearnError(f"Progress update failed: {e}"))

    def update_ui_state(self, **kwargs) -> None:
        """Update UI state with given parameters."""
        try:
            current_ui = self._state.ui_state
            updated_ui = replace(current_ui, **kwargs)

            new_state = replace(
                self._state, ui_state=updated_ui, last_updated=datetime.now()
            )

            self._update_state(new_state)

            # Emit specific signals for common UI changes
            if "is_loading" in kwargs:
                self.loading_changed.emit(kwargs["is_loading"])

            logger.debug(f"Updated UI state: {kwargs}")

        except Exception as e:
            logger.exception(f"Failed to update UI state: {e}")
            self._handle_error(LearnError(f"UI state update failed: {e}"))

    def set_error(self, error: LearnError) -> None:
        """Set error state."""
        try:
            error_state = ErrorState(
                error_type=self._get_error_type(error),
                message=str(error),
                recoverable=ErrorRecoveryStrategy.can_recover(error),
                context=getattr(error, "context", None),
            )

            new_state = replace(
                self._state,
                error_state=error_state,
                ui_state=replace(self._state.ui_state, is_loading=False),
                last_updated=datetime.now(),
            )

            self._update_state(new_state)
            self.error_occurred.emit(error_state)
            logger.error(f"Error set: {error}")

        except Exception as e:
            logger.critical(f"Failed to set error state: {e}")

    def clear_error(self) -> None:
        """Clear current error state."""
        if self._state.error_state is None:
            return

        new_state = replace(self._state, error_state=None, last_updated=datetime.now())

        self._update_state(new_state)
        self.error_cleared.emit()
        logger.info("Error state cleared")

    def _update_state(self, new_state: LearnState) -> None:
        """Update state and emit signals."""
        old_view = self._state.current_view
        self._state = new_state

        # Add to history
        self._state_history.append(new_state)
        if len(self._state_history) > self._max_history:
            self._state_history.pop(0)

        # Emit signals
        self.state_changed.emit(new_state)

        if old_view != new_state.current_view:
            self.view_changed.emit(new_state.current_view.value)

    def _handle_error(self, error: Exception) -> None:
        """Handle error by converting to LearnError if needed."""
        if isinstance(error, LearnError):
            self.set_error(error)
        else:
            self.set_error(LearnError(str(error)))

    def _get_error_type(self, error: LearnError) -> ErrorType:
        """Get error type from exception."""
        from .learn_exceptions import (
            AnswerValidationError,
            DataCorruptionError,
            LessonNotAvailable,
            NetworkError,
            ProgressCalculationError,
            QuestionGenerationError,
            SessionCreationError,
            UIRenderingError,
        )

        if isinstance(error, LessonNotAvailable):
            return ErrorType.LESSON_UNAVAILABLE
        if isinstance(error, SessionCreationError):
            return ErrorType.SESSION_CREATION_FAILED
        if isinstance(error, QuestionGenerationError):
            return ErrorType.QUESTION_GENERATION_FAILED
        if isinstance(error, AnswerValidationError):
            return ErrorType.ANSWER_VALIDATION_FAILED
        if isinstance(error, ProgressCalculationError):
            return ErrorType.PROGRESS_CALCULATION_FAILED
        if isinstance(error, UIRenderingError):
            return ErrorType.UI_RENDERING_FAILED
        if isinstance(error, NetworkError):
            return ErrorType.NETWORK_ERROR
        if isinstance(error, DataCorruptionError):
            return ErrorType.DATA_CORRUPTION
        return ErrorType.UI_RENDERING_FAILED  # Default fallback
