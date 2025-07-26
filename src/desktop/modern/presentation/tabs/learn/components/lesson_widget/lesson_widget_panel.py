"""
Lesson Widget Panel Component

Main coordinator for the lesson interface including question display,
answer options, progress tracking, and controls.
"""

import logging
from typing import Optional

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

from desktop.modern.core.interfaces.learn_services import (
    IQuizSessionService, IQuestionGenerationService, 
    IAnswerValidationService, ILessonProgressService,
    ILessonConfigurationService, ILearnUIService
)
from desktop.modern.domain.models.learn import QuestionData
from .question_display import QuestionDisplay
from .answer_options import AnswerOptions
from .lesson_progress_bar import LessonProgressBar
from .lesson_timer import LessonTimer
from .lesson_controls import LessonControls

logger = logging.getLogger(__name__)


class LessonWidgetPanel(QWidget):
    """
    Main lesson widget panel coordinator.
    
    Orchestrates all lesson components including question display,
    answer options, progress tracking, timer, and controls.
    """
    
    # Signals
    lesson_completed = pyqtSignal(str)  # session_id
    back_to_selector = pyqtSignal()
    answer_feedback = pyqtSignal(bool)  # correct/incorrect
    
    def __init__(
        self,
        session_service: IQuizSessionService,
        question_service: IQuestionGenerationService,
        validation_service: IAnswerValidationService,
        progress_service: ILessonProgressService,
        config_service: ILessonConfigurationService,
        ui_service: ILearnUIService,
        parent: Optional[QWidget] = None
    ):
        """
        Initialize lesson widget panel.
        
        Args:
            session_service: Service for session management
            question_service: Service for question generation
            validation_service: Service for answer validation
            progress_service: Service for progress tracking
            config_service: Service for lesson configurations
            ui_service: Service for UI calculations
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Inject services
        self.session_service = session_service
        self.question_service = question_service
        self.validation_service = validation_service
        self.progress_service = progress_service
        self.config_service = config_service
        self.ui_service = ui_service
        
        # Current state
        self.current_session_id: Optional[str] = None
        self.current_question: Optional[QuestionData] = None
        self.is_lesson_active: bool = False
        
        self._setup_ui()
        self._setup_connections()
        
        logger.info("Lesson widget panel initialized")
    
    def _setup_ui(self) -> None:
        """Setup lesson widget UI."""
        try:
            layout = QVBoxLayout(self)
            layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            
            # Controls at top
            self.controls = LessonControls(self.ui_service, self)
            layout.addWidget(self.controls)
            
            # Add stretch before main content
            layout.addStretch(1)
            
            # Question prompt
            self.question_prompt = QLabel()
            self.question_prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._apply_question_prompt_styling()
            layout.addWidget(self.question_prompt)
            
            # Question display
            self.question_display = QuestionDisplay(self.ui_service, self)
            layout.addWidget(self.question_display)
            
            # Answer options
            self.answer_options = AnswerOptions(self.ui_service, self)
            layout.addWidget(self.answer_options)
            
            # Add stretch before bottom elements
            layout.addStretch(1)
            
            # Progress and timer at bottom
            self.progress_bar = LessonProgressBar(self.ui_service, self)
            layout.addWidget(self.progress_bar)
            
            self.timer = LessonTimer(self.ui_service, self)
            layout.addWidget(self.timer)
            
        except Exception as e:
            logger.error(f"Failed to setup lesson widget UI: {e}")
    
    def _apply_question_prompt_styling(self) -> None:
        """Apply styling to question prompt label."""
        try:
            self.question_prompt.setStyleSheet("""
                QLabel {
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 8px;
                    padding: 12px 20px;
                    margin: 10px;
                }
            """)
        except Exception as e:
            logger.error(f"Failed to apply question prompt styling: {e}")
    
    def _setup_connections(self) -> None:
        """Setup component connections."""
        try:
            # Answer selection
            self.answer_options.answer_selected.connect(self._on_answer_selected)
            
            # Timer signals
            self.timer.time_expired.connect(self._on_timer_expired)
            self.timer.time_updated.connect(self._on_timer_updated)
            
            # Control signals
            self.controls.back_clicked.connect(self.back_to_selector.emit)
            self.controls.pause_clicked.connect(self._on_pause_clicked)
            self.controls.restart_clicked.connect(self._on_restart_clicked)
            
        except Exception as e:
            logger.error(f"Failed to setup lesson widget connections: {e}")
    
    def start_lesson(self, session_id: str) -> None:
        """
        Start lesson with given session.
        
        Args:
            session_id: Session identifier
        """
        try:
            self.current_session_id = session_id
            session = self.session_service.get_session(session_id)
            
            if not session:
                logger.error(f"Session not found: {session_id}")
                return
            
            self.is_lesson_active = True
            
            # Setup based on quiz mode
            if session.quiz_mode.value == "countdown":
                self.timer.start_countdown(session.quiz_time)
                self.progress_bar.set_timer_mode()
                self.controls.show_pause_button(True)  # Show pause for timed mode
            else:
                self.progress_bar.set_question_mode(session.total_questions)
                self.timer.hide_timer()
                self.controls.show_pause_button(False)
            
            # Generate first question
            self._generate_next_question()
            
            logger.info(f"Started lesson for session {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to start lesson: {e}")
    
    def _generate_next_question(self) -> None:
        """Generate and display next question."""
        try:
            if not self.current_session_id or not self.is_lesson_active:
                return
                
            session = self.session_service.get_session(self.current_session_id)
            if not session:
                logger.error(f"Session not found: {self.current_session_id}")
                return
                
            lesson_config = self.config_service.get_lesson_config(session.lesson_type)
            if not lesson_config:
                logger.error(f"Lesson config not found for {session.lesson_type}")
                return
            
            # Update question prompt
            self.question_prompt.setText(lesson_config.question_prompt)
            
            # Generate question
            question = self.question_service.generate_question(
                self.current_session_id, lesson_config
            )
            self.current_question = question
            
            # Update displays
            self.question_display.show_question(question, lesson_config.question_format)
            self.answer_options.show_options(question, lesson_config.answer_format)
            
            # Update progress
            self._update_progress_display()
            
            logger.debug(f"Generated question for session {self.current_session_id}")
            
        except Exception as e:
            logger.error(f"Failed to generate next question: {e}")
    
    def _on_answer_selected(self, selected_answer) -> None:
        """
        Handle answer selection.
        
        Args:
            selected_answer: The selected answer
        """
        try:
            if not self.current_question or not self.is_lesson_active:
                return
            
            # Check if answer is correct
            is_correct = self.validation_service.check_answer(
                self.current_question, selected_answer
            )
            
            # Record answer
            self.validation_service.record_answer(
                self.current_session_id, 
                self.current_question.question_id, 
                is_correct
            )
            
            # Emit feedback signal
            self.answer_feedback.emit(is_correct)
            
            # Show visual feedback
            self._show_answer_feedback(is_correct)
            
            if is_correct:
                # Update session progress
                session = self.session_service.get_session(self.current_session_id)
                if session:
                    self.session_service.update_session_progress(
                        self.current_session_id,
                        current_question=session.current_question + 1
                    )
                
                # Check if lesson complete
                if self.progress_service.is_lesson_complete(self.current_session_id):
                    self._complete_lesson()
                else:
                    # Generate next question after delay
                    QTimer.singleShot(1500, self._generate_next_question)
            else:
                # Show incorrect feedback, disable this answer option
                self.answer_options.disable_option(selected_answer)
            
            logger.debug(f"Answer selected: {selected_answer}, correct: {is_correct}")
            
        except Exception as e:
            logger.error(f"Failed to handle answer selection: {e}")
    
    def _show_answer_feedback(self, is_correct: bool) -> None:
        """
        Show visual feedback for answer selection.
        
        Args:
            is_correct: Whether the answer was correct
        """
        try:
            if is_correct:
                # Show correct feedback
                feedback_text = "Correct! Well done."
                feedback_color = "rgba(0, 255, 0, 0.3)"
                border_color = "rgba(0, 255, 0, 0.5)"
            else:
                # Show incorrect feedback
                feedback_text = "Wrong! Try again."
                feedback_color = "rgba(255, 0, 0, 0.3)"
                border_color = "rgba(255, 0, 0, 0.5)"
            
            # Update question prompt with feedback
            self.question_prompt.setText(feedback_text)
            self.question_prompt.setStyleSheet(f"""
                QLabel {{
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    background-color: {feedback_color};
                    border: 2px solid {border_color};
                    border-radius: 8px;
                    padding: 12px 20px;
                    margin: 10px;
                }}
            """)
            
            # Reset styling after delay if answer was correct
            if is_correct:
                QTimer.singleShot(1500, self._reset_question_prompt_styling)
            
        except Exception as e:
            logger.error(f"Failed to show answer feedback: {e}")
    
    def _reset_question_prompt_styling(self) -> None:
        """Reset question prompt to normal styling."""
        try:
            self._apply_question_prompt_styling()
        except Exception as e:
            logger.error(f"Failed to reset question prompt styling: {e}")
    
    def _on_timer_expired(self) -> None:
        """Handle timer expiration."""
        try:
            logger.info("Timer expired - completing lesson")
            self._complete_lesson()
        except Exception as e:
            logger.error(f"Failed to handle timer expiration: {e}")
    
    def _on_timer_updated(self, remaining_seconds: int) -> None:
        """
        Handle timer update.
        
        Args:
            remaining_seconds: Remaining time in seconds
        """
        try:
            # Update session with remaining time
            if self.current_session_id:
                self.session_service.update_session_progress(
                    self.current_session_id,
                    quiz_time=remaining_seconds
                )
        except Exception as e:
            logger.error(f"Failed to handle timer update: {e}")
    
    def _on_pause_clicked(self) -> None:
        """Handle pause button click."""
        try:
            if self.timer.is_timer_running():
                self.timer.pause_timer()
                self.controls.set_pause_state(True)
                logger.debug("Lesson paused")
            else:
                self.timer.resume_timer()
                self.controls.set_pause_state(False)
                logger.debug("Lesson resumed")
        except Exception as e:
            logger.error(f"Failed to handle pause click: {e}")
    
    def _on_restart_clicked(self) -> None:
        """Handle restart button click."""
        try:
            if self.current_session_id:
                # Reset session and restart
                session = self.session_service.get_session(self.current_session_id)
                if session:
                    # Reset session state
                    self.session_service.update_session_progress(
                        self.current_session_id,
                        current_question=1,
                        questions_answered=0,
                        correct_answers=0,
                        incorrect_guesses=0,
                        quiz_time=120 if session.quiz_mode.value == "countdown" else 0
                    )
                    
                    # Restart lesson
                    self.start_lesson(self.current_session_id)
                    
                    logger.info("Lesson restarted")
        except Exception as e:
            logger.error(f"Failed to handle restart click: {e}")
    
    def _complete_lesson(self) -> None:
        """Complete the current lesson."""
        try:
            if not self.current_session_id:
                return
            
            self.is_lesson_active = False
            
            # Stop timer if running
            self.timer.stop_timer()
            
            # Mark session as completed
            self.session_service.end_session(self.current_session_id)
            
            # Show completion state
            self.progress_bar.show_completion()
            self.question_prompt.setText("Lesson Complete!")
            
            # Disable controls
            self.controls.enable_controls(False)
            
            # Emit completion signal
            self.lesson_completed.emit(self.current_session_id)
            
            logger.info(f"Lesson completed for session {self.current_session_id}")
            
        except Exception as e:
            logger.error(f"Failed to complete lesson: {e}")
    
    def _update_progress_display(self) -> None:
        """Update progress display."""
        try:
            if not self.current_session_id:
                return
                
            progress_info = self.progress_service.get_progress_info(self.current_session_id)
            self.progress_bar.update_progress(progress_info)
            
        except Exception as e:
            logger.error(f"Failed to update progress display: {e}")
    
    def reset_lesson(self) -> None:
        """Reset lesson widget to initial state."""
        try:
            self.is_lesson_active = False
            self.current_session_id = None
            self.current_question = None
            
            # Reset components
            self.question_display.clear_question()
            self.answer_options.clear_all()
            self.progress_bar.reset()
            self.timer.reset()
            self.controls.reset_controls()
            
            # Reset question prompt
            self.question_prompt.setText("")
            self._apply_question_prompt_styling()
            
            logger.debug("Lesson widget reset")
            
        except Exception as e:
            logger.error(f"Failed to reset lesson widget: {e}")
    
    def resizeEvent(self, event) -> None:
        """Handle resize events for responsive design."""
        try:
            self._update_responsive_styling()
            super().resizeEvent(event)
        except Exception as e:
            logger.error(f"Failed to handle resize event: {e}")
    
    def _update_responsive_styling(self) -> None:
        """Update styling based on current size."""
        try:
            if not self.parent():
                return
                
            parent_width = self.parent().width()
            parent_height = self.parent().height()
            
            # Get responsive sizes
            font_sizes = self.ui_service.get_font_sizes(parent_width, parent_height)
            
            # Update question prompt font
            prompt_font_size = font_sizes.get("question_prompt", 16)
            font = self.question_prompt.font()
            font.setFamily("Georgia")
            font.setPointSize(prompt_font_size)
            font.setBold(True)
            self.question_prompt.setFont(font)
            
            # Update component styling
            self.question_display.update_responsive_styling(parent_width, parent_height)
            self.answer_options.update_responsive_styling(parent_width, parent_height)
            self.progress_bar.update_responsive_styling(parent_width, parent_height)
            self.timer.update_responsive_styling(parent_width, parent_height)
            self.controls.update_responsive_styling(parent_width, parent_height)
            
        except Exception as e:
            logger.error(f"Failed to update responsive styling: {e}")
