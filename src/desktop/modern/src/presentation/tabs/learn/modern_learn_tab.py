"""
Modern Learn Tab Implementation

Main coordinator for the learn tab following the browse tab architecture pattern.
Uses QStackedWidget for navigation between lesson selector, lesson widget, and results.
"""

import logging
from typing import Optional

from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, QTimer

from core.interfaces.learn_services import (
    ILessonConfigurationService, IQuizSessionService, IQuestionGenerationService,
    IAnswerValidationService, ILessonProgressService, ILearnUIService, 
    ILearnNavigationService, ILearnDataService
)
from domain.models.learn import LessonType, QuizMode
from .components import LessonSelectorPanel, LessonWidgetPanel, LessonResultsPanel

logger = logging.getLogger(__name__)


class ModernLearnTab(QWidget):
    """
    Modern Learn Tab coordinator following browse tab architecture.
    
    Uses QStackedWidget for navigation between:
    - Index 0: Lesson selector
    - Index 1: Lesson widget  
    - Index 2: Results display
    
    Provides complete functional parity with legacy learn tab while
    following modern service-based architecture patterns.
    """
    
    # External signals for main app integration
    navigation_requested = pyqtSignal(str)  # For main app navigation
    tab_state_changed = pyqtSignal(str)     # For state tracking
    
    def __init__(
        self,
        lesson_config_service: ILessonConfigurationService,
        session_service: IQuizSessionService,
        question_service: IQuestionGenerationService,
        validation_service: IAnswerValidationService,
        progress_service: ILessonProgressService,
        ui_service: ILearnUIService,
        navigation_service: ILearnNavigationService,
        data_service: ILearnDataService,
        parent: Optional[QWidget] = None
    ):
        """
        Initialize modern learn tab.
        
        Args:
            lesson_config_service: Service for lesson configurations
            session_service: Service for session management
            question_service: Service for question generation
            validation_service: Service for answer validation
            progress_service: Service for progress tracking
            ui_service: Service for UI calculations
            navigation_service: Service for navigation management
            data_service: Service for data persistence
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Inject all services
        self.lesson_config_service = lesson_config_service
        self.session_service = session_service
        self.question_service = question_service
        self.validation_service = validation_service
        self.progress_service = progress_service
        self.ui_service = ui_service
        self.navigation_service = navigation_service
        self.data_service = data_service
        
        # Current state
        self.current_session_id: Optional[str] = None
        
        self._setup_ui()
        self._setup_connections()
        
        # Initialize to lesson selector
        QTimer.singleShot(100, self._show_lesson_selector)
        
        logger.info("Modern learn tab initialized")
    
    def _setup_ui(self) -> None:
        """Setup main learn tab UI."""
        try:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            
            # Stack widget for navigation (matching browse tab pattern)
            self.stack = QStackedWidget()
            
            # Create components with service injection
            self.lesson_selector = LessonSelectorPanel(
                self.lesson_config_service,
                self.ui_service,
                self
            )
            
            self.lesson_widget = LessonWidgetPanel(
                self.session_service,
                self.question_service,
                self.validation_service,
                self.progress_service,
                self.lesson_config_service,
                self.ui_service,
                self
            )
            
            self.results_panel = LessonResultsPanel(
                self.progress_service,
                self.ui_service,
                self
            )
            
            # Add to stack (matching legacy indexes)
            self.stack.addWidget(self.lesson_selector)  # Index 0
            self.stack.addWidget(self.lesson_widget)    # Index 1  
            self.stack.addWidget(self.results_panel)    # Index 2
            
            layout.addWidget(self.stack)
            
        except Exception as e:
            logger.error(f"Failed to setup learn tab UI: {e}")
    
    def _setup_connections(self) -> None:
        """Setup component signal connections."""
        try:
            # Lesson selector signals
            self.lesson_selector.lesson_selected.connect(self._on_lesson_selected)
            
            # Lesson widget signals
            self.lesson_widget.lesson_completed.connect(self._on_lesson_completed)
            self.lesson_widget.back_to_selector.connect(self._show_lesson_selector)
            self.lesson_widget.answer_feedback.connect(self._on_answer_feedback)
            
            # Results panel signals
            self.results_panel.restart_lesson.connect(self._on_restart_lesson)
            self.results_panel.back_to_selector.connect(self._show_lesson_selector)
            
        except Exception as e:
            logger.error(f"Failed to setup learn tab connections: {e}")
    
    def _on_lesson_selected(self, lesson_type_str: str, mode_str: str) -> None:
        """
        Handle lesson selection from selector.
        
        Args:
            lesson_type_str: Lesson type identifier
            mode_str: Quiz mode identifier
        """
        try:
            lesson_type = LessonType(lesson_type_str)
            quiz_mode = QuizMode(mode_str)
            
            # Create new session
            session_id = self.session_service.create_session(lesson_type, quiz_mode)
            self.current_session_id = session_id
            
            # Update navigation service
            self.navigation_service.navigate_to_lesson(session_id)
            
            # Navigate to lesson view
            self._show_lesson_widget()
            
            # Start lesson
            self.lesson_widget.start_lesson(session_id)
            
            # Emit state change signal
            self.tab_state_changed.emit("lesson_active")
            
            logger.info(f"Started lesson: {lesson_type.value} in {quiz_mode.value} mode")
            
        except Exception as e:
            logger.error(f"Failed to start lesson: {e}")
            # Stay on selector on error
            self._show_lesson_selector()
    
    def _on_lesson_completed(self, session_id: str) -> None:
        """
        Handle lesson completion.
        
        Args:
            session_id: Completed session identifier
        """
        try:
            self.current_session_id = session_id
            
            # Calculate and save results
            results = self.progress_service.calculate_results(session_id)
            save_success = self.data_service.save_lesson_results(results)
            
            if not save_success:
                logger.warning(f"Failed to save results for session {session_id}")
            
            # Update navigation service
            self.navigation_service.navigate_to_results(session_id)
            
            # Navigate to results view
            self._show_results()
            
            # Show results
            self.results_panel.show_results(session_id)
            
            # Emit state change signal
            self.tab_state_changed.emit("lesson_completed")
            
            logger.info(f"Lesson completed: {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to handle lesson completion: {e}")
    
    def _on_answer_feedback(self, is_correct: bool) -> None:
        """
        Handle answer feedback from lesson widget.
        
        Args:
            is_correct: Whether the answer was correct
        """
        # This could be used for additional feedback or analytics
        logger.debug(f"Answer feedback: {'correct' if is_correct else 'incorrect'}")
    
    def _on_restart_lesson(self, lesson_type_str: str) -> None:
        """
        Handle lesson restart request.
        
        Args:
            lesson_type_str: Lesson type to restart
        """
        try:
            # Get the current mode from lesson selector
            current_mode = self.lesson_selector.get_selected_mode()
            
            # Start new lesson with same type and mode
            self._on_lesson_selected(lesson_type_str, current_mode.value)
            
            logger.info(f"Restarted lesson: {lesson_type_str}")
            
        except Exception as e:
            logger.error(f"Failed to restart lesson: {e}")
            # Fallback to selector
            self._show_lesson_selector()
    
    def _show_lesson_selector(self) -> None:
        """Navigate to lesson selector view."""
        try:
            self.stack.setCurrentIndex(0)
            self.navigation_service.navigate_to_lesson_selector()
            
            # Reset lesson widget
            self.lesson_widget.reset_lesson()
            
            # Clear results
            self.results_panel.clear_results()
            
            # Clear current session
            self.current_session_id = None
            
            # Emit state change signal
            self.tab_state_changed.emit("selector_active")
            
            logger.debug("Navigated to lesson selector")
            
        except Exception as e:
            logger.error(f"Failed to show lesson selector: {e}")
    
    def _show_lesson_widget(self) -> None:
        """Navigate to lesson widget view."""
        try:
            self.stack.setCurrentIndex(1)
            
            # Emit state change signal
            self.tab_state_changed.emit("lesson_widget_active")
            
            logger.debug("Navigated to lesson widget")
            
        except Exception as e:
            logger.error(f"Failed to show lesson widget: {e}")
    
    def _show_results(self) -> None:
        """Navigate to results view."""
        try:
            self.stack.setCurrentIndex(2)
            
            # Emit state change signal
            self.tab_state_changed.emit("results_active")
            
            logger.debug("Navigated to results view")
            
        except Exception as e:
            logger.error(f"Failed to show results: {e}")
    
    def get_current_view(self) -> str:
        """
        Get current view identifier.
        
        Returns:
            Current view identifier
        """
        try:
            return self.navigation_service.get_current_view()
        except Exception as e:
            logger.error(f"Failed to get current view: {e}")
            return "unknown"
    
    def get_current_session_id(self) -> Optional[str]:
        """
        Get current session ID if any.
        
        Returns:
            Current session ID or None
        """
        return self.current_session_id
    
    def cleanup(self) -> None:
        """Cleanup learn tab resources."""
        try:
            # Stop any active timers
            if hasattr(self.lesson_widget, 'timer'):
                self.lesson_widget.timer.stop_timer()
            
            # End current session if active
            if self.current_session_id:
                self.session_service.end_session(self.current_session_id)
            
            # Cleanup old session data
            self.session_service.cleanup_old_sessions()
            
            # Cleanup old data files
            self.data_service.cleanup_old_data()
            
            logger.info("Learn tab cleanup completed")
            
        except Exception as e:
            logger.error(f"Failed to cleanup learn tab: {e}")
    
    def save_state(self) -> dict:
        """
        Save current learn tab state.
        
        Returns:
            Dictionary with current state
        """
        try:
            state = {
                "current_view": self.get_current_view(),
                "current_session_id": self.current_session_id,
                "selected_mode": self.lesson_selector.get_selected_mode().value,
                "navigation_state": self.navigation_service.get_navigation_state(),
            }
            
            return state
            
        except Exception as e:
            logger.error(f"Failed to save learn tab state: {e}")
            return {}
    
    def restore_state(self, state: dict) -> bool:
        """
        Restore learn tab state.
        
        Args:
            state: State dictionary to restore
            
        Returns:
            True if restore successful, False otherwise
        """
        try:
            if not state:
                return False
            
            # Restore selected mode
            selected_mode = state.get("selected_mode")
            if selected_mode:
                try:
                    mode = QuizMode(selected_mode)
                    self.lesson_selector.set_mode(mode)
                except ValueError:
                    pass
            
            # Restore view (but don't restore active lessons for safety)
            current_view = state.get("current_view", "lesson_selector")
            if current_view == "lesson_selector":
                self._show_lesson_selector()
            
            logger.info("Learn tab state restored")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore learn tab state: {e}")
            return False
    
    def get_statistics(self) -> dict:
        """
        Get learn tab usage statistics.
        
        Returns:
            Dictionary with usage statistics
        """
        try:
            session_stats = self.session_service.get_session_statistics()
            validation_stats = self.validation_service.get_statistics()
            data_stats = self.data_service.get_data_statistics()
            
            return {
                "sessions": session_stats,
                "validation": validation_stats,
                "data": data_stats,
                "current_session": self.current_session_id,
                "current_view": self.get_current_view(),
            }
            
        except Exception as e:
            logger.error(f"Failed to get learn tab statistics: {e}")
            return {}
    
    def resizeEvent(self, event) -> None:
        """Handle resize events for responsive design."""
        try:
            # Update responsive styling for all components
            width = self.width()
            height = self.height()
            
            # Update components if they have responsive styling methods
            for component in [self.lesson_selector, self.lesson_widget, self.results_panel]:
                if hasattr(component, 'update_responsive_styling'):
                    component.update_responsive_styling(width, height)
            
            super().resizeEvent(event)
            
        except Exception as e:
            logger.error(f"Failed to handle resize event: {e}")
