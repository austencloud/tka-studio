"""
Lesson Results Controller

Handles business logic for lesson results display including result calculation,
performance analysis, and navigation. Coordinates between view and services.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QObject

from desktop.modern.core.interfaces.learn_services import (
    ILessonConfigurationService,
    ILessonProgressService,
    IQuizSessionService,
)
from desktop.modern.domain.models.learn import LessonResults, LessonType
from desktop.modern.presentation.controllers.learn.state import (
    LearnStateManager,
    SessionCreationError,
)
from desktop.modern.presentation.views.learn.lesson_results_view import (
    LessonResultsView,
)


logger = logging.getLogger(__name__)


class LessonResultsController(QObject):
    """
    Handles lesson results business logic.

    Coordinates between the results view and services to display
    comprehensive lesson results and handle navigation.
    """

    def __init__(
        self,
        view: LessonResultsView,
        config_service: ILessonConfigurationService,
        session_service: IQuizSessionService,
        progress_service: ILessonProgressService,
        state_manager: LearnStateManager,
    ):
        super().__init__()

        self.view = view
        self.config_service = config_service
        self.session_service = session_service
        self.progress_service = progress_service
        self.state_manager = state_manager

        self._connect_signals()

        logger.debug("Lesson results controller initialized")

    def _connect_signals(self) -> None:
        """Connect view events to business logic handlers."""
        self.view.restart_lesson_requested.connect(self._handle_restart_lesson)
        self.view.back_to_selector_requested.connect(self._handle_back_to_selector)

        # Connect state manager signals
        self.state_manager.state_changed.connect(self._on_state_changed)
        self.state_manager.error_occurred.connect(self._on_error_occurred)
        self.state_manager.loading_changed.connect(self._on_loading_changed)

    def display_results(self, results: LessonResults) -> None:
        """
        Display lesson results with analysis and recommendations.

        Args:
            results: Lesson results to display
        """
        try:
            logger.info(
                f"Displaying results for {results.lesson_type.value}: {results.accuracy_percentage:.1f}%"
            )

            # Display results in view
            self.view.display_results(results)

            # Log performance summary
            self._log_performance_summary(results)

        except Exception as e:
            logger.error(f"Failed to display results: {e}")
            # Don't set error state here as results are already calculated
            # Just log the error and show what we can

    def _log_performance_summary(self, results: LessonResults) -> None:
        """Log performance summary for analytics."""
        logger.info("Lesson Performance Summary:")
        logger.info(f"  Lesson: {results.lesson_type.value}")
        logger.info(f"  Mode: {results.quiz_mode.value}")
        logger.info(f"  Accuracy: {results.accuracy_percentage:.1f}%")
        logger.info(
            f"  Questions: {results.questions_answered}/{results.total_questions}"
        )
        logger.info(f"  Time: {results.completion_time_seconds:.1f}s")
        logger.info(f"  Grade: {results.grade_letter}")
        logger.info(f"  Performance: {results.performance_level}")

    def _handle_restart_lesson(self, lesson_type: LessonType) -> None:
        """
        Handle lesson restart request.

        Args:
            lesson_type: Type of lesson to restart
        """
        try:
            logger.info(f"Restarting lesson: {lesson_type.value}")

            # Set loading state
            self.state_manager.update_ui_state(is_loading=True)

            # Get current state to determine quiz mode
            current_state = self.state_manager.get_state()
            quiz_mode = None

            # Try to get quiz mode from current results
            if current_state.lesson_results:
                quiz_mode = current_state.lesson_results.quiz_mode

            # If no quiz mode available, default to fixed question
            if not quiz_mode:
                from desktop.modern.domain.models.learn import QuizMode

                quiz_mode = QuizMode.FIXED_QUESTION
                logger.warning(
                    "No quiz mode found in results, defaulting to fixed question mode"
                )

            # Validate lesson availability
            config = self.config_service.get_lesson_config(lesson_type)
            if not config:
                raise SessionCreationError(
                    lesson_type.value, quiz_mode.value, "Lesson configuration not found"
                )

            # Create new session
            session_id = self.session_service.create_session(lesson_type, quiz_mode)
            if not session_id:
                raise SessionCreationError(
                    lesson_type.value, quiz_mode.value, "Failed to create new session"
                )

            # Get created session
            session = self.session_service.get_session(session_id)
            if not session:
                raise SessionCreationError(
                    lesson_type.value, quiz_mode.value, "Created session not found"
                )

            # Transition to lesson workspace
            self.state_manager.transition_to_lesson_workspace(session)

            logger.info(f"Successfully restarted lesson {lesson_type.value}")

        except SessionCreationError as e:
            logger.error(f"Failed to restart lesson: {e}")
            self.state_manager.set_error(e)

        except Exception as e:
            logger.error(f"Unexpected error restarting lesson: {e}")
            self.state_manager.set_error(
                SessionCreationError(
                    lesson_type.value, "unknown", f"Unexpected error: {e!s}"
                )
            )

        finally:
            # Clear loading state
            self.state_manager.update_ui_state(is_loading=False)

    def _handle_back_to_selector(self) -> None:
        """Handle back to lesson selector request."""
        try:
            logger.info("Returning to lesson selector")
            self.state_manager.transition_to_lesson_selector()

        except Exception as e:
            logger.error(f"Failed to return to lesson selector: {e}")
            # Force transition even if there's an error
            self.state_manager.transition_to_lesson_selector()

    def _on_state_changed(self, state) -> None:
        """Handle state changes."""
        # Update view based on new state
        self.view.set_loading_state(state.ui_state.is_loading)

        # If we have new results, display them
        if state.lesson_results and state.current_view.value == "lesson_results":
            self.view.display_results(state.lesson_results)

    def _on_error_occurred(self, error_state) -> None:
        """Handle error state."""
        logger.warning(f"Error occurred in lesson results: {error_state.message}")

        # Update view to show error state
        self.view.set_loading_state(False)

        # Could show error message in view if needed
        # For now, errors are handled at the tab level

    def _on_loading_changed(self, is_loading: bool) -> None:
        """Handle loading state changes."""
        self.view.set_loading_state(is_loading)

    def activate(self) -> None:
        """Activate the controller (called when view becomes active)."""
        # Display current results if available
        current_state = self.state_manager.get_state()
        if current_state.lesson_results:
            self.display_results(current_state.lesson_results)

        logger.debug("Lesson results controller activated")

    def deactivate(self) -> None:
        """Deactivate the controller (called when view becomes inactive)."""
        # Clear loading state
        self.state_manager.update_ui_state(is_loading=False)

        logger.debug("Lesson results controller deactivated")
