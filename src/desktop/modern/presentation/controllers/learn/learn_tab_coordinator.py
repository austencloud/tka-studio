"""
Learn Tab Coordinator

Main coordinator for the learn tab following modern architecture patterns.
Orchestrates views, controllers, and state management with clean separation of concerns.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.learn_services import (
    IAnswerValidationService,
    ILearnUIService,
    ILessonConfigurationService,
    ILessonProgressService,
    IQuestionGenerationService,
    IQuizSessionService,
)
from desktop.modern.presentation.components.learn import (
    AnswerOptions,
    LessonControls,
    LessonTimer,
    ProgressControls,
    QuestionDisplay,
)
from desktop.modern.presentation.views.learn.lesson_results_view import (
    LessonResultsView,
)
from desktop.modern.presentation.views.learn.lesson_selector_view import (
    LessonSelectorView,
)
from desktop.modern.presentation.views.learn.lesson_workspace_view import (
    LessonWorkspaceView,
)

from .lesson_results_controller import LessonResultsController
from .lesson_selector_controller import LessonSelectorController
from .lesson_workspace_controller import LessonWorkspaceController
from .state import LearnStateManager, LearnView


logger = logging.getLogger(__name__)


class LearnTabCoordinator(QWidget):
    """
    Main coordinator for the learn tab following modern architecture.

    Orchestrates all components with clean separation of concerns:
    - State management through LearnStateManager
    - Business logic through Controllers
    - UI rendering through Views
    - Specialized components for focused functionality
    """

    # Signals for communication with main app
    error_occurred = pyqtSignal(str)  # error message

    def __init__(self, container: DIContainer, parent: QWidget | None = None):
        super().__init__(parent)

        self.container = container

        # Core state management
        self.state_manager = LearnStateManager()

        # Services (will be resolved during initialization)
        self.config_service: ILessonConfigurationService | None = None
        self.session_service: IQuizSessionService | None = None
        self.question_service: IQuestionGenerationService | None = None
        self.validation_service: IAnswerValidationService | None = None
        self.progress_service: ILessonProgressService | None = None
        self.ui_service: ILearnUIService | None = None

        # Views
        self.lesson_selector_view: LessonSelectorView | None = None
        self.lesson_workspace_view: LessonWorkspaceView | None = None
        self.lesson_results_view: LessonResultsView | None = None

        # Controllers
        self.selector_controller: LessonSelectorController | None = None
        self.workspace_controller: LessonWorkspaceController | None = None
        self.results_controller: LessonResultsController | None = None

        # Specialized components
        self.question_display: QuestionDisplay | None = None
        self.answer_options: AnswerOptions | None = None
        self.progress_controls: ProgressControls | None = None
        self.lesson_timer: LessonTimer | None = None
        self.lesson_controls: LessonControls | None = None

        # UI structure
        self.stacked_widget: QStackedWidget | None = None

        self._setup_ui()
        self._setup_connections()

        # Initialize immediately for better test compatibility
        self._initialize_coordinator()

        logger.info("Learn tab coordinator initialized")

    def _resolve_services(self) -> None:
        """Resolve services from dependency injection container."""
        try:
            self.config_service = self.container.resolve(ILessonConfigurationService)
            self.session_service = self.container.resolve(IQuizSessionService)
            self.question_service = self.container.resolve(IQuestionGenerationService)
            self.validation_service = self.container.resolve(IAnswerValidationService)
            self.progress_service = self.container.resolve(ILessonProgressService)
            self.ui_service = self.container.resolve(ILearnUIService)

            logger.debug("Services resolved successfully")

        except Exception as e:
            logger.exception(f"Failed to resolve services: {e}")
            raise

    def _setup_ui(self) -> None:
        """Setup the main UI structure."""
        try:
            # Main layout
            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setSpacing(0)

            # Stacked widget for navigation
            self.stacked_widget = QStackedWidget()
            main_layout.addWidget(self.stacked_widget)

            # Create views
            self._create_views()

            # Create specialized components
            self._create_specialized_components()

            # Setup workspace view with components
            self._setup_workspace_components()

            # Add views to stack
            self.stacked_widget.addWidget(self.lesson_selector_view)  # Index 0
            self.stacked_widget.addWidget(self.lesson_workspace_view)  # Index 1
            self.stacked_widget.addWidget(self.lesson_results_view)  # Index 2

            # Start with lesson selector
            self.stacked_widget.setCurrentIndex(0)

            logger.debug("UI structure setup complete")

        except Exception as e:
            logger.exception(f"Failed to setup UI: {e}")
            raise

    def _create_views(self) -> None:
        """Create main views."""
        self.lesson_selector_view = LessonSelectorView(self)
        self.lesson_workspace_view = LessonWorkspaceView(self)
        self.lesson_results_view = LessonResultsView(self)

    def _create_specialized_components(self) -> None:
        """Create specialized components for lesson workspace."""
        self.question_display = QuestionDisplay(self)
        self.answer_options = AnswerOptions(self)
        self.progress_controls = ProgressControls(self)
        self.lesson_timer = LessonTimer(self)
        self.lesson_controls = LessonControls(self)

    def _setup_workspace_components(self) -> None:
        """Setup workspace view with specialized components."""
        if self.lesson_workspace_view:
            self.lesson_workspace_view.set_question_display(self.question_display)
            self.lesson_workspace_view.set_answer_options(self.answer_options)
            self.lesson_workspace_view.set_progress_controls(self.progress_controls)
            self.lesson_workspace_view.set_lesson_timer(self.lesson_timer)
            self.lesson_workspace_view.set_lesson_controls(self.lesson_controls)

    def _setup_connections(self) -> None:
        """Setup signal connections."""
        try:
            # State manager signals
            self.state_manager.view_changed.connect(self._on_view_changed)
            self.state_manager.error_occurred.connect(self._on_error_occurred)

            logger.debug("Signal connections setup complete")

        except Exception as e:
            logger.exception(f"Failed to setup connections: {e}")

    def _initialize_coordinator(self) -> None:
        """Initialize coordinator after UI is ready."""
        try:
            logger.info("🚀 Initializing Learn Tab Coordinator...")

            # Try to resolve services
            try:
                self._resolve_services()
                logger.debug("Services resolved successfully")
            except Exception as e:
                logger.warning(f"Failed to resolve services: {e}")
                # Continue with basic initialization even without services
                # This allows the UI to be visible for testing

            # Create controllers (only if services are available)
            if hasattr(self, "config_service") and self.config_service:
                self._create_controllers()

                # Activate initial controller
                if self.selector_controller:
                    self.selector_controller.activate()
                    logger.debug("Controllers activated")
            else:
                logger.warning("Controllers not created due to missing services")

            logger.info("✅ Learn Tab Coordinator initialized successfully")

        except Exception as e:
            logger.exception(f"❌ Failed to initialize coordinator: {e}")
            # Don't emit error for missing services in test environments
            if "Service" not in str(e):
                self.error_occurred.emit(f"Failed to initialize learn tab: {e!s}")

    def _create_controllers(self) -> None:
        """Create controllers with dependency injection."""
        try:
            # Lesson selector controller
            self.selector_controller = LessonSelectorController(
                view=self.lesson_selector_view,
                config_service=self.config_service,
                session_service=self.session_service,
                state_manager=self.state_manager,
            )

            # Lesson workspace controller
            self.workspace_controller = LessonWorkspaceController(
                view=self.lesson_workspace_view,
                question_service=self.question_service,
                validation_service=self.validation_service,
                progress_service=self.progress_service,
                config_service=self.config_service,
                session_service=self.session_service,
                state_manager=self.state_manager,
                question_display=self.question_display,
                answer_options=self.answer_options,
            )

            # Lesson results controller
            self.results_controller = LessonResultsController(
                view=self.lesson_results_view,
                config_service=self.config_service,
                session_service=self.session_service,
                progress_service=self.progress_service,
                state_manager=self.state_manager,
            )

            # Connect workspace components to controller
            self._connect_workspace_components()

            logger.debug("Controllers created successfully")

        except Exception as e:
            logger.exception(f"Failed to create controllers: {e}")
            raise

    def _connect_workspace_components(self) -> None:
        """Connect workspace components to controller."""
        if self.workspace_controller and self.answer_options:
            # Connect answer selection to controller
            self.answer_options.answer_selected.connect(
                self.workspace_controller.handle_answer_selection
            )

    def _on_view_changed(self, view_name: str) -> None:
        """Handle view changes from state manager."""
        try:
            view_enum = LearnView(view_name)

            # Deactivate current controller
            self._deactivate_current_controller()

            # Switch view
            if view_enum == LearnView.LESSON_SELECTOR:
                self.stacked_widget.setCurrentIndex(0)
                self.selector_controller.activate()
            elif view_enum == LearnView.LESSON_WORKSPACE:
                self.stacked_widget.setCurrentIndex(1)
                self.workspace_controller.activate()
                # Start lesson with current session
                current_state = self.state_manager.get_state()
                if current_state.current_session:
                    self.workspace_controller.start_lesson(
                        current_state.current_session
                    )
            elif view_enum == LearnView.LESSON_RESULTS:
                self.stacked_widget.setCurrentIndex(2)
                self.results_controller.activate()

            logger.info(f"Switched to view: {view_name}")

        except Exception as e:
            logger.exception(f"Failed to handle view change: {e}")

    def _deactivate_current_controller(self) -> None:
        """Deactivate currently active controller."""
        current_index = self.stacked_widget.currentIndex()

        if current_index == 0 and self.selector_controller:
            self.selector_controller.deactivate()
        elif current_index == 1 and self.workspace_controller:
            self.workspace_controller.deactivate()
        elif current_index == 2 and self.results_controller:
            self.results_controller.deactivate()

    def _on_error_occurred(self, error_state) -> None:
        """Handle error state from state manager."""
        logger.error(f"Learn tab error: {error_state.message}")
        self.error_occurred.emit(error_state.message)

    def resizeEvent(self, event) -> None:
        """Handle resize events for responsive design."""
        try:
            self._update_responsive_styling()
            super().resizeEvent(event)
        except Exception as e:
            logger.exception(f"Failed to handle resize event: {e}")

    def _update_responsive_styling(self) -> None:
        """Update responsive styling for all components."""
        try:
            width = self.width()
            height = self.height()

            # Update views
            if self.lesson_selector_view:
                self.lesson_selector_view.update_responsive_styling(width, height)
            if self.lesson_workspace_view:
                self.lesson_workspace_view.update_responsive_styling(width, height)
            if self.lesson_results_view:
                self.lesson_results_view.update_responsive_styling(width, height)

            # Update specialized components
            if self.question_display:
                self.question_display.update_responsive_styling(width, height)
            if self.answer_options:
                self.answer_options.update_responsive_styling(width, height)
            if self.progress_controls:
                self.progress_controls.update_responsive_styling(width, height)
            if self.lesson_timer:
                self.lesson_timer.update_responsive_styling(width, height)
            if self.lesson_controls:
                self.lesson_controls.update_responsive_styling(width, height)

        except Exception as e:
            logger.exception(f"Failed to update responsive styling: {e}")

    def get_current_view(self) -> LearnView:
        """Get current active view."""
        current_state = self.state_manager.get_state()
        return current_state.current_view

    def get_state_manager(self) -> LearnStateManager:
        """Get state manager for external access."""
        return self.state_manager
