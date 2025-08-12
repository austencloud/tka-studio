"""
Lesson Workspace Controller

Orchestrates lesson execution including question generation, answer validation,
progress tracking, and state management. Coordinates between view and services.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, QTimer

from desktop.modern.core.interfaces.learn_services import (
    IAnswerValidationService,
    ILessonConfigurationService,
    ILessonProgressService,
    IQuestionGenerationService,
    IQuizSessionService,
)
from desktop.modern.domain.models.learn import QuestionData, QuizSession
from desktop.modern.presentation.controllers.learn.state import (
    AnswerValidationError,
    LayoutMode,
    LearnStateManager,
    ProgressCalculationError,
    QuestionGenerationError,
)


if TYPE_CHECKING:
    from desktop.modern.presentation.views.learn.lesson_workspace_view import (
        LessonWorkspaceView,
    )

logger = logging.getLogger(__name__)


class LessonWorkspaceController(QObject):
    """
    Orchestrates lesson execution without UI coupling.

    Handles the complete lesson flow including question generation,
    answer validation, progress tracking, and state transitions.
    """

    def __init__(
        self,
        view: LessonWorkspaceView,
        question_service: IQuestionGenerationService,
        validation_service: IAnswerValidationService,
        progress_service: ILessonProgressService,
        config_service: ILessonConfigurationService,
        session_service: IQuizSessionService,
        state_manager: LearnStateManager,
        question_display=None,
        answer_options=None,
    ):
        super().__init__()

        self.view = view
        self.question_service = question_service
        self.validation_service = validation_service
        self.progress_service = progress_service
        self.config_service = config_service
        self.session_service = session_service
        self.state_manager = state_manager

        # UI components for displaying content
        self.question_display = question_display
        self.answer_options = answer_options

        # Timers for feedback and transitions
        self.feedback_timer = QTimer()
        self.feedback_timer.setSingleShot(True)
        self.feedback_timer.timeout.connect(self._clear_feedback)

        self.transition_timer = QTimer()
        self.transition_timer.setSingleShot(True)
        self.transition_timer.timeout.connect(self._generate_next_question)

        self._connect_signals()

        logger.debug("Lesson workspace controller initialized")

    def _connect_signals(self) -> None:
        """Connect view events and state changes to handlers."""
        # View events
        self.view.back_requested.connect(self._handle_back_request)
        self.view.pause_requested.connect(self._handle_pause_request)
        self.view.restart_requested.connect(self._handle_restart_request)

        # State manager signals
        self.state_manager.state_changed.connect(self._on_state_changed)
        self.state_manager.error_occurred.connect(self._on_error_occurred)

    def start_lesson(self, session: QuizSession) -> None:
        """
        Start lesson execution for the given session.

        Args:
            session: Quiz session to start
        """
        try:
            logger.info(f"Starting lesson for session {session.session_id}")

            # Set loading state
            self.state_manager.update_ui_state(is_loading=True)

            # Configure view layout based on lesson type
            layout_mode = self._determine_layout_mode(session.lesson_type)
            self.view.set_layout_mode(layout_mode)

            # Get lesson configuration
            config = self.config_service.get_lesson_config(session.lesson_type)
            if not config:
                raise QuestionGenerationError(
                    session.session_id,
                    session.lesson_type.value,
                    "Lesson configuration not found",
                )

            # Set question prompt
            self.view.set_question_prompt(config.question_prompt)

            # Generate first question
            self._generate_first_question(session, config)

            logger.info(f"Lesson started successfully for {session.lesson_type.value}")

        except Exception as e:
            logger.exception(f"Failed to start lesson: {e}")
            if isinstance(e, QuestionGenerationError):
                self.state_manager.set_error(e)
            else:
                self.state_manager.set_error(
                    QuestionGenerationError(
                        session.session_id, session.lesson_type.value, str(e)
                    )
                )

        finally:
            self.state_manager.update_ui_state(is_loading=False)

    def _display_question_and_answers(self, question: QuestionData, config) -> None:
        """Display question and answer options in UI components."""
        try:
            # Display question if component is available
            if self.question_display and question:
                question_format = getattr(config, "question_format", "pictograph")
                self.question_display.show_question(question, question_format)
                logger.debug(f"Displayed question in {question_format} format")

            # Display answer options if component is available
            if self.answer_options and question and question.answer_options:
                answer_format = getattr(config, "answer_format", "button")
                self.answer_options.show_options(question, answer_format)
                logger.debug(
                    f"Displayed {len(question.answer_options)} answer options in {answer_format} format"
                )

        except Exception as e:
            logger.exception(f"Failed to display question and answers: {e}")

    def _determine_layout_mode(self, lesson_type) -> LayoutMode:
        """Determine layout mode based on lesson type."""
        from desktop.modern.domain.models.learn import LessonType

        if lesson_type == LessonType.VALID_NEXT_PICTOGRAPH:
            return LayoutMode.HORIZONTAL
        return LayoutMode.VERTICAL

    def _generate_first_question(self, session: QuizSession, config) -> None:
        """Generate the first question for the lesson."""
        try:
            question = self.question_service.generate_question(
                session.session_id, config
            )
            if not question:
                raise QuestionGenerationError(
                    session.session_id,
                    session.lesson_type.value,
                    "Question generation returned None",
                )

            # Update state with new question
            self.state_manager.update_current_question(question)

            # Update progress (convert timestamp if needed)
            from datetime import datetime

            start_time = datetime.now()
            if (
                hasattr(question, "generation_timestamp")
                and question.generation_timestamp
            ):
                if isinstance(question.generation_timestamp, str):
                    start_time = datetime.fromisoformat(question.generation_timestamp)
                elif isinstance(question.generation_timestamp, datetime):
                    start_time = question.generation_timestamp

            self.state_manager.update_progress(current_question_start_time=start_time)

            # Display the question and answers in UI components
            self._display_question_and_answers(question, config)

            logger.debug(f"Generated first question: {question.question_id}")

        except Exception as e:
            logger.exception(f"Failed to generate first question: {e}")
            raise QuestionGenerationError(
                session.session_id,
                session.lesson_type.value,
                f"First question generation failed: {e!s}",
            )

    def _generate_next_question(self) -> None:
        """Generate the next question in the sequence."""
        try:
            current_state = self.state_manager.get_state()

            if not current_state.current_session:
                logger.warning("No active session for next question generation")
                return

            # Check if lesson should be completed
            if self.progress_service.is_lesson_complete(
                current_state.current_session.session_id
            ):
                self._complete_lesson()
                return

            # Get lesson configuration
            config = self.config_service.get_lesson_config(
                current_state.current_session.lesson_type
            )
            if not config:
                raise QuestionGenerationError(
                    current_state.current_session.session_id,
                    current_state.current_session.lesson_type.value,
                    "Lesson configuration not found",
                )

            # Generate next question
            question = self.question_service.generate_question(
                current_state.current_session.session_id, config
            )

            if not question:
                raise QuestionGenerationError(
                    current_state.current_session.session_id,
                    current_state.current_session.lesson_type.value,
                    "Question generation returned None",
                )

            # Update state with new question
            self.state_manager.update_current_question(question)

            # Update progress (convert timestamp if needed)
            from datetime import datetime

            start_time = datetime.now()
            if (
                hasattr(question, "generation_timestamp")
                and question.generation_timestamp
            ):
                if isinstance(question.generation_timestamp, str):
                    start_time = datetime.fromisoformat(question.generation_timestamp)
                elif isinstance(question.generation_timestamp, datetime):
                    start_time = question.generation_timestamp

            self.state_manager.update_progress(current_question_start_time=start_time)

            logger.debug(f"Generated next question: {question.question_id}")

        except Exception as e:
            logger.exception(f"Failed to generate next question: {e}")
            self.state_manager.set_error(
                QuestionGenerationError(
                    (
                        current_state.current_session.session_id
                        if current_state.current_session
                        else "unknown"
                    ),
                    (
                        current_state.current_session.lesson_type.value
                        if current_state.current_session
                        else "unknown"
                    ),
                    str(e),
                )
            )

    def handle_answer_selection(self, answer) -> None:
        """
        Handle answer selection with validation and progression.

        Args:
            answer: Selected answer from user
        """
        try:
            current_state = self.state_manager.get_state()

            if not current_state.can_answer_question():
                logger.warning("Cannot answer question in current state")
                return

            if not current_state.current_question:
                logger.warning("No current question for answer validation")
                return

            # Validate answer
            is_correct = self.validation_service.check_answer(
                current_state.current_question, answer
            )

            # Record answer
            self.validation_service.record_answer(
                current_state.current_session.session_id,
                current_state.current_question.question_id,
                is_correct,
            )

            # Update session progress
            self._update_session_progress(is_correct)

            # Show feedback
            self._show_answer_feedback(is_correct)

            # Handle progression based on correctness
            if is_correct:
                self._handle_correct_answer()
            else:
                self._handle_incorrect_answer(answer)

            logger.debug(f"Answer processed: {answer}, correct: {is_correct}")

        except Exception as e:
            logger.exception(f"Failed to handle answer selection: {e}")
            self.state_manager.set_error(
                AnswerValidationError(
                    (
                        current_state.current_question.question_id
                        if current_state.current_question
                        else "unknown"
                    ),
                    answer,
                    str(e),
                )
            )

    def _update_session_progress(self, is_correct: bool) -> None:
        """Update session progress based on answer result."""
        try:
            current_state = self.state_manager.get_state()
            session = current_state.current_session

            if not session:
                return

            # Calculate new progress values
            new_questions_answered = session.questions_answered + (
                1 if is_correct else 0
            )
            new_correct_answers = session.correct_answers + (1 if is_correct else 0)
            new_incorrect_guesses = session.incorrect_guesses + (0 if is_correct else 1)
            new_current_question = session.current_question + (1 if is_correct else 0)

            # Update session via service
            self.session_service.update_session_progress(
                session.session_id,
                current_question=new_current_question,
                questions_answered=new_questions_answered,
                correct_answers=new_correct_answers,
                incorrect_guesses=new_incorrect_guesses,
            )

            # Update local progress state
            self.state_manager.update_progress(
                current_question_number=new_current_question,
                questions_answered=new_questions_answered,
                correct_answers=new_correct_answers,
                incorrect_attempts=new_incorrect_guesses,
                accuracy_percentage=(
                    new_correct_answers / max(new_questions_answered, 1)
                )
                * 100,
            )

        except Exception as e:
            logger.exception(f"Failed to update session progress: {e}")
            raise ProgressCalculationError(
                (
                    current_state.current_session.session_id
                    if current_state.current_session
                    else "unknown"
                ),
                str(e),
            )

    def _show_answer_feedback(self, is_correct: bool) -> None:
        """Show visual feedback for answer selection."""
        if is_correct:
            self.view.show_feedback("Correct! Well done.", "success")
        else:
            self.view.show_feedback("Incorrect. Try again.", "error")

        # Set timer to clear feedback
        self.feedback_timer.start(1500)  # 1.5 seconds

    def _clear_feedback(self) -> None:
        """Clear answer feedback."""
        self.view.clear_feedback()

        # Restore question prompt
        current_state = self.state_manager.get_state()
        if current_state.current_session:
            config = self.config_service.get_lesson_config(
                current_state.current_session.lesson_type
            )
            if config:
                self.view.set_question_prompt(config.question_prompt)

    def _handle_correct_answer(self) -> None:
        """Handle correct answer progression."""
        # Start timer for next question generation
        self.transition_timer.start(1500)  # 1.5 seconds delay

    def _handle_incorrect_answer(self, answer) -> None:
        """Handle incorrect answer (allow retry)."""
        # Disable the incorrect option in the view
        # This will be handled by the answer options component

    def _complete_lesson(self) -> None:
        """Complete the current lesson."""
        try:
            current_state = self.state_manager.get_state()

            if not current_state.current_session:
                logger.warning("No active session to complete")
                return

            # Calculate final results
            results = self.progress_service.calculate_results(
                current_state.current_session.session_id
            )

            # End session
            self.session_service.end_session(current_state.current_session.session_id)

            # Transition to results
            self.state_manager.transition_to_results(results)

            logger.info(
                f"Lesson completed for session {current_state.current_session.session_id}"
            )

        except Exception as e:
            logger.exception(f"Failed to complete lesson: {e}")
            self.state_manager.set_error(
                ProgressCalculationError(
                    (
                        current_state.current_session.session_id
                        if current_state.current_session
                        else "unknown"
                    ),
                    str(e),
                )
            )

    def _handle_back_request(self) -> None:
        """Handle back to selector request."""
        self.state_manager.transition_to_lesson_selector()

    def _handle_pause_request(self) -> None:
        """Handle pause/resume request."""
        current_state = self.state_manager.get_state()
        new_paused_state = not current_state.ui_state.is_paused
        self.state_manager.update_ui_state(is_paused=new_paused_state)

    def _handle_restart_request(self) -> None:
        """Handle lesson restart request."""
        current_state = self.state_manager.get_state()
        if current_state.current_session:
            # Reset session and restart
            session = current_state.current_session
            new_session_id = self.session_service.create_session(
                session.lesson_type, session.quiz_mode
            )
            new_session = self.session_service.get_session(new_session_id)
            if new_session:
                self.state_manager.transition_to_lesson_workspace(new_session)

    def _on_state_changed(self, state) -> None:
        """Handle state changes."""
        # Update view based on state
        self.view.set_loading_state(state.ui_state.is_loading)

        # Handle layout changes
        if state.current_session:
            required_layout = state.get_required_layout_mode()
            self.view.set_layout_mode(required_layout)

    def _on_error_occurred(self, error_state) -> None:
        """Handle error state."""
        logger.warning(f"Error occurred in lesson workspace: {error_state.message}")
        self.view.set_loading_state(False)

    def activate(self) -> None:
        """Activate the controller."""
        logger.debug("Lesson workspace controller activated")

    def deactivate(self) -> None:
        """Deactivate the controller."""
        # Stop any running timers
        self.feedback_timer.stop()
        self.transition_timer.stop()

        logger.debug("Lesson workspace controller deactivated")
