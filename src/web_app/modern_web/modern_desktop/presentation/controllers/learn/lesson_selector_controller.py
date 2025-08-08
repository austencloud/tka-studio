"""
Lesson Selector Controller

Handles business logic for lesson selection including validation,
session creation, and state management. Coordinates between view and services.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QObject

from desktop.modern.core.interfaces.learn_services import (
    ILessonConfigurationService,
    IQuizSessionService,
)
from desktop.modern.domain.models.learn import LessonType, QuizMode
from desktop.modern.presentation.controllers.learn.state import (
    LearnStateManager,
    LessonNotAvailable,
    SessionCreationError,
)
from desktop.modern.presentation.views.learn.lesson_selector_view import (
    LessonSelectorView,
)


logger = logging.getLogger(__name__)


class LessonSelectorController(QObject):
    """
    Handles lesson selection business logic.

    Coordinates between the lesson selector view and services to handle
    lesson availability, validation, and session creation.
    """

    def __init__(
        self,
        view: LessonSelectorView,
        config_service: ILessonConfigurationService,
        session_service: IQuizSessionService,
        state_manager: LearnStateManager,
    ):
        super().__init__()

        self.view = view
        self.config_service = config_service
        self.session_service = session_service
        self.state_manager = state_manager

        self._connect_signals()
        self._initialize_view()

        logger.debug("Lesson selector controller initialized")

    def _connect_signals(self) -> None:
        """Connect view events to business logic handlers."""
        self.view.lesson_requested.connect(self._handle_lesson_request)

        # Connect state manager signals
        self.state_manager.state_changed.connect(self._on_state_changed)
        self.state_manager.error_occurred.connect(self._on_error_occurred)
        self.state_manager.loading_changed.connect(self._on_loading_changed)

    def _initialize_view(self) -> None:
        """Initialize view with available lessons."""
        try:
            # Get available lessons from configuration service
            available_lessons = self._get_available_lessons()
            self.view.update_lesson_availability(available_lessons)

            # Set default mode from current state
            current_state = self.state_manager.get_state()
            if current_state.current_session:
                self.view.set_selected_mode(current_state.current_session.quiz_mode)

            logger.info(
                f"Initialized lesson selector with {len(available_lessons)} available lessons"
            )

        except Exception as e:
            logger.error(f"Failed to initialize lesson selector: {e}")
            self.state_manager.set_error(LessonNotAvailable("initialization", str(e)))

    def _get_available_lessons(self) -> list[LessonType]:
        """Get list of available lesson types."""
        try:
            configs = self.config_service.get_all_lesson_configs()
            available_lessons = []

            for config in configs.values():
                if self._is_lesson_available(config.lesson_type):
                    available_lessons.append(config.lesson_type)

            return available_lessons

        except Exception as e:
            logger.error(f"Failed to get available lessons: {e}")
            return []  # Return empty list on error

    def _is_lesson_available(self, lesson_type: LessonType) -> bool:
        """Check if a specific lesson type is available."""
        try:
            # Get lesson configuration
            config = self.config_service.get_lesson_config(lesson_type)
            if not config:
                return False

            # Validate configuration
            if not config.question_format or not config.answer_format:
                return False

            # Additional availability checks could go here
            # (e.g., data availability, feature flags, etc.)

            return True

        except Exception as e:
            logger.warning(f"Error checking lesson availability for {lesson_type}: {e}")
            return False

    def _handle_lesson_request(
        self, lesson_type: LessonType, quiz_mode: QuizMode
    ) -> None:
        """
        Handle lesson selection request with validation and session creation.

        Args:
            lesson_type: Selected lesson type
            quiz_mode: Selected quiz mode
        """
        try:
            logger.info(
                f"Processing lesson request: {lesson_type.value} in {quiz_mode.value} mode"
            )

            # Clear any existing error state before attempting new lesson
            self.state_manager.clear_error()

            # Set loading state
            self.state_manager.update_ui_state(is_loading=True)

            # Validate lesson availability
            if not self._is_lesson_available(lesson_type):
                raise LessonNotAvailable(
                    lesson_type.value, "Lesson configuration is invalid or missing"
                )

            # Get lesson configuration
            config = self.config_service.get_lesson_config(lesson_type)
            if not config:
                raise LessonNotAvailable(
                    lesson_type.value, "Lesson configuration not found"
                )

            # Validate quiz mode compatibility
            if not self._is_quiz_mode_compatible(lesson_type, quiz_mode):
                raise SessionCreationError(
                    lesson_type.value,
                    quiz_mode.value,
                    "Quiz mode not compatible with lesson type",
                )

            # Create quiz session
            session_id = self.session_service.create_session(lesson_type, quiz_mode)
            if not session_id:
                raise SessionCreationError(
                    lesson_type.value, quiz_mode.value, "Failed to create session"
                )

            # Get created session
            session = self.session_service.get_session(session_id)
            if not session:
                raise SessionCreationError(
                    lesson_type.value, quiz_mode.value, "Created session not found"
                )

            # Clear loading state before transition
            self.state_manager.update_ui_state(is_loading=False)

            # Transition to lesson workspace
            self.state_manager.transition_to_lesson_workspace(session)

            logger.info(
                f"Successfully created session {session_id} for {lesson_type.value}"
            )

        except (LessonNotAvailable, SessionCreationError) as e:
            logger.error(f"Lesson request failed: {e}")
            self.state_manager.set_error(e)

        except Exception as e:
            logger.error(f"Unexpected error in lesson request: {e}")
            self.state_manager.set_error(
                SessionCreationError(
                    lesson_type.value if "lesson_type" in locals() else "unknown",
                    quiz_mode.value if "quiz_mode" in locals() else "unknown",
                    f"Unexpected error: {e!s}",
                )
            )

        finally:
            # Clear loading state
            self.state_manager.update_ui_state(is_loading=False)

    def _is_quiz_mode_compatible(
        self, lesson_type: LessonType, quiz_mode: QuizMode
    ) -> bool:
        """Check if quiz mode is compatible with lesson type."""
        # All current lesson types support both quiz modes
        # This method allows for future restrictions if needed
        return True

    def _on_state_changed(self, state) -> None:
        """Handle state changes."""
        # Update view based on new state
        if state.error_state:
            self.view.set_loading_state(False)
        else:
            self.view.set_loading_state(state.ui_state.is_loading)

    def _on_error_occurred(self, error_state) -> None:
        """Handle error state."""
        logger.warning(f"Error occurred in lesson selector: {error_state.message}")

        # Update view to show error state
        self.view.set_loading_state(False)

        # Could show error message in view if needed
        # For now, errors are handled at the tab level

    def _on_loading_changed(self, is_loading: bool) -> None:
        """Handle loading state changes."""
        self.view.set_loading_state(is_loading)

    def refresh_available_lessons(self) -> None:
        """Refresh the list of available lessons."""
        try:
            available_lessons = self._get_available_lessons()
            self.view.update_lesson_availability(available_lessons)
            logger.debug("Refreshed available lessons")

        except Exception as e:
            logger.error(f"Failed to refresh available lessons: {e}")

    def activate(self) -> None:
        """Activate the controller (called when view becomes active)."""
        # Refresh available lessons when activated
        self.refresh_available_lessons()

        # Clear any previous errors
        self.state_manager.clear_error()

        logger.debug("Lesson selector controller activated")

    def deactivate(self) -> None:
        """Deactivate the controller (called when view becomes inactive)."""
        # Clear loading state
        self.state_manager.update_ui_state(is_loading=False)

        logger.debug("Lesson selector controller deactivated")
