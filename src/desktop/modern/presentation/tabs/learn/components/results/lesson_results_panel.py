"""
Lesson Results Panel Component

Displays lesson completion results including scores, statistics,
and navigation options for restarting or returning to selector.
"""

import logging
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal

from desktop.modern.core.interfaces.learn_services import ILessonProgressService, ILearnUIService
from desktop.modern.domain.models.learn import LessonResults

logger = logging.getLogger(__name__)


class LessonResultsPanel(QWidget):
    """
    Component for displaying lesson completion results.
    
    Shows comprehensive results including accuracy, timing, performance level,
    and options for restarting or returning to lesson selector.
    """
    
    # Signals
    restart_lesson = pyqtSignal(str)  # lesson_type
    back_to_selector = pyqtSignal()
    
    def __init__(
        self,
        progress_service: ILessonProgressService,
        ui_service: ILearnUIService,
        parent: Optional[QWidget] = None
    ):
        """
        Initialize lesson results panel.
        
        Args:
            progress_service: Service for progress and results calculation
            ui_service: Service for UI calculations
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.progress_service = progress_service
        self.ui_service = ui_service
        self.current_results: Optional[LessonResults] = None
        
        self._setup_ui()
        self._setup_connections()
        
        logger.debug("Lesson results panel initialized")
    
    def _setup_ui(self) -> None:
        """Setup results panel UI."""
        try:
            main_layout = QVBoxLayout(self)
            main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Title
            self.title_label = QLabel("Lesson Complete!")
            self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._apply_title_styling()
            
            # Results container
            self.results_container = QWidget()
            self.results_layout = QGridLayout(self.results_container)
            self._setup_results_layout()
            
            # Action buttons
            self.buttons_container = QWidget()
            self._setup_action_buttons()
            
            # Add to main layout
            main_layout.addStretch(1)
            main_layout.addWidget(self.title_label)
            main_layout.addStretch(1)
            main_layout.addWidget(self.results_container)
            main_layout.addStretch(1)
            main_layout.addWidget(self.buttons_container)
            main_layout.addStretch(1)
            
        except Exception as e:
            logger.error(f"Failed to setup results panel UI: {e}")
    
    def _apply_title_styling(self) -> None:
        """Apply styling to title label."""
        try:
            self.title_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    font-size: 28px;
                    background-color: rgba(0, 255, 0, 0.2);
                    border: 2px solid rgba(0, 255, 0, 0.4);
                    border-radius: 12px;
                    padding: 16px 32px;
                }
            """)
        except Exception as e:
            logger.error(f"Failed to apply title styling: {e}")
    
    def _setup_results_layout(self) -> None:
        """Setup the results display layout."""
        try:
            # Create result statistic labels
            self.accuracy_label = self._create_stat_label("Accuracy", "0%")
            self.score_label = self._create_stat_label("Score", "0/0")
            self.time_label = self._create_stat_label("Time", "0:00")
            self.performance_label = self._create_stat_label("Performance", "")
            
            # Additional statistics
            self.streak_label = self._create_stat_label("Best Streak", "0")
            self.grade_label = self._create_stat_label("Grade", "")
            
            # Arrange in grid (2 columns)
            self.results_layout.addWidget(self.accuracy_label, 0, 0)
            self.results_layout.addWidget(self.score_label, 0, 1)
            self.results_layout.addWidget(self.time_label, 1, 0)
            self.results_layout.addWidget(self.performance_label, 1, 1)
            self.results_layout.addWidget(self.streak_label, 2, 0)
            self.results_layout.addWidget(self.grade_label, 2, 1)
            
            # Set spacing
            self.results_layout.setSpacing(20)
            
        except Exception as e:
            logger.error(f"Failed to setup results layout: {e}")
    
    def _create_stat_label(self, stat_name: str, stat_value: str) -> QLabel:
        """
        Create a statistic display label.
        
        Args:
            stat_name: Name of the statistic
            stat_value: Value of the statistic
            
        Returns:
            Configured statistic label
        """
        try:
            label = QLabel(f"{stat_name}\n{stat_value}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    background-color: rgba(255, 255, 255, 0.15);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 10px;
                    padding: 16px;
                    min-width: 120px;
                    min-height: 80px;
                }
            """)
            return label
        except Exception as e:
            logger.error(f"Failed to create stat label: {e}")
            return QLabel("Error")
    
    def _setup_action_buttons(self) -> None:
        """Setup action buttons layout."""
        try:
            buttons_layout = QHBoxLayout(self.buttons_container)
            buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Back to selector button
            self.back_button = self._create_action_button(
                "← Back to Lessons", "back"
            )
            
            # Restart lesson button
            self.restart_button = self._create_action_button(
                "↻ Try Again", "restart"
            )
            
            # Add buttons to layout
            buttons_layout.addWidget(self.back_button)
            buttons_layout.addStretch()
            buttons_layout.addWidget(self.restart_button)
            
        except Exception as e:
            logger.error(f"Failed to setup action buttons: {e}")
    
    def _create_action_button(self, text: str, button_type: str) -> QPushButton:
        """
        Create an action button with appropriate styling.
        
        Args:
            text: Button text
            button_type: Type of button for styling
            
        Returns:
            Configured action button
        """
        try:
            button = QPushButton(text)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            
            if button_type == "back":
                button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(255, 255, 255, 0.2);
                        border: 2px solid rgba(255, 255, 255, 0.3);
                        border-radius: 12px;
                        color: white;
                        font-family: Georgia;
                        font-weight: bold;
                        padding: 12px 24px;
                        min-width: 140px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 0.3);
                        border: 2px solid rgba(255, 255, 255, 0.5);
                    }
                    QPushButton:pressed {
                        background-color: rgba(255, 255, 255, 0.4);
                    }
                """)
            elif button_type == "restart":
                button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(0, 255, 0, 0.2);
                        border: 2px solid rgba(0, 255, 0, 0.3);
                        border-radius: 12px;
                        color: white;
                        font-family: Georgia;
                        font-weight: bold;
                        padding: 12px 24px;
                        min-width: 140px;
                    }
                    QPushButton:hover {
                        background-color: rgba(0, 255, 0, 0.3);
                        border: 2px solid rgba(0, 255, 0, 0.5);
                    }
                    QPushButton:pressed {
                        background-color: rgba(0, 255, 0, 0.4);
                    }
                """)
            
            return button
            
        except Exception as e:
            logger.error(f"Failed to create action button: {e}")
            return QPushButton("Error")
    
    def _setup_connections(self) -> None:
        """Setup button signal connections."""
        try:
            self.back_button.clicked.connect(self.back_to_selector.emit)
            self.restart_button.clicked.connect(self._on_restart_clicked)
        except Exception as e:
            logger.error(f"Failed to setup results connections: {e}")
    
    def show_results(self, session_id: str) -> None:
        """
        Show results for a completed session.
        
        Args:
            session_id: Completed session identifier
        """
        try:
            # Calculate results
            results = self.progress_service.calculate_results(session_id)
            self.current_results = results
            
            # Update display
            self._update_results_display(results)
            
            logger.info(
                f"Showing results for session {session_id}: "
                f"{results.correct_answers}/{results.questions_answered} correct "
                f"({results.accuracy_percentage:.1f}%)"
            )
            
        except Exception as e:
            logger.error(f"Failed to show results for session {session_id}: {e}")
    
    def _update_results_display(self, results: LessonResults) -> None:
        """
        Update the results display with calculated results.
        
        Args:
            results: Calculated lesson results
        """
        try:
            # Update accuracy
            self.accuracy_label.setText(f"Accuracy\n{results.accuracy_percentage:.1f}%")
            
            # Update score
            self.score_label.setText(f"Score\n{results.correct_answers}/{results.questions_answered}")
            
            # Update time
            time_text = f"Time\n{results.minutes_taken:.1f} min"
            self.time_label.setText(time_text)
            
            # Update performance level
            self.performance_label.setText(f"Performance\n{results.performance_level}")
            
            # Update best streak
            streak_text = f"Best Streak\n{results.streak_longest_correct or 0}"
            self.streak_label.setText(streak_text)
            
            # Update grade
            self.grade_label.setText(f"Grade\n{results.grade_letter}")
            
            # Update performance label color based on level
            self._update_performance_styling(results.performance_level)
            
            # Update title based on performance
            self._update_title_based_on_performance(results.accuracy_percentage)
            
        except Exception as e:
            logger.error(f"Failed to update results display: {e}")
    
    def _update_performance_styling(self, performance_level: str) -> None:
        """
        Update performance label styling based on performance level.
        
        Args:
            performance_level: Performance level string
        """
        try:
            color_map = {
                "Excellent": "rgba(0, 255, 0, 0.3)",
                "Good": "rgba(0, 150, 255, 0.3)",
                "Fair": "rgba(255, 165, 0, 0.3)",
                "Needs Improvement": "rgba(255, 255, 0, 0.3)",
                "Poor": "rgba(255, 0, 0, 0.3)"
            }
            
            background_color = color_map.get(performance_level, "rgba(255, 255, 255, 0.15)")
            
            self.performance_label.setStyleSheet(f"""
                QLabel {{
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    background-color: {background_color};
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 10px;
                    padding: 16px;
                    min-width: 120px;
                    min-height: 80px;
                }}
            """)
            
        except Exception as e:
            logger.error(f"Failed to update performance styling: {e}")
    
    def _update_title_based_on_performance(self, accuracy: float) -> None:
        """
        Update title text and styling based on performance.
        
        Args:
            accuracy: Accuracy percentage
        """
        try:
            if accuracy >= 95:
                title_text = "Outstanding!"
                title_color = "rgba(0, 255, 0, 0.3)"
            elif accuracy >= 80:
                title_text = "Great Job!"
                title_color = "rgba(0, 150, 255, 0.3)"
            elif accuracy >= 60:
                title_text = "Good Effort!"
                title_color = "rgba(255, 165, 0, 0.3)"
            else:
                title_text = "Keep Practicing!"
                title_color = "rgba(255, 255, 0, 0.3)"
            
            self.title_label.setText(title_text)
            self.title_label.setStyleSheet(f"""
                QLabel {{
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    font-size: 28px;
                    background-color: {title_color};
                    border: 2px solid rgba(255, 255, 255, 0.4);
                    border-radius: 12px;
                    padding: 16px 32px;
                }}
            """)
            
        except Exception as e:
            logger.error(f"Failed to update title based on performance: {e}")
    
    def _on_restart_clicked(self) -> None:
        """Handle restart button click."""
        try:
            if self.current_results:
                lesson_type = self.current_results.lesson_type.value
                self.restart_lesson.emit(lesson_type)
                logger.debug(f"Restart requested for lesson type: {lesson_type}")
        except Exception as e:
            logger.error(f"Failed to handle restart click: {e}")
    
    def clear_results(self) -> None:
        """Clear current results display."""
        try:
            self.current_results = None
            
            # Reset title
            self.title_label.setText("Lesson Complete!")
            self._apply_title_styling()
            
            # Reset statistics
            self.accuracy_label.setText("Accuracy\n0%")
            self.score_label.setText("Score\n0/0")
            self.time_label.setText("Time\n0:00")
            self.performance_label.setText("Performance\n")
            self.streak_label.setText("Best Streak\n0")
            self.grade_label.setText("Grade\n")
            
            logger.debug("Results display cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear results: {e}")
    
    def update_responsive_styling(self, parent_width: int, parent_height: int) -> None:
        """
        Update styling based on parent widget size.
        
        Args:
            parent_width: Parent widget width
            parent_height: Parent widget height
        """
        try:
            # Get responsive sizes
            font_sizes = self.ui_service.get_font_sizes(parent_width, parent_height)
            component_sizes = self.ui_service.get_component_sizes(parent_width, parent_height)
            
            # Update title font
            title_font_size = font_sizes.get("results_title", 22)
            font = self.title_label.font()
            font.setFamily("Georgia")
            font.setPointSize(title_font_size)
            font.setBold(True)
            self.title_label.setFont(font)
            
            # Update statistic labels
            stat_font_size = font_sizes.get("results_stat", 14)
            stat_size = component_sizes.get("results_stat", (200, 30))
            
            for label in [self.accuracy_label, self.score_label, self.time_label,
                         self.performance_label, self.streak_label, self.grade_label]:
                font = label.font()
                font.setFamily("Georgia")
                font.setPointSize(stat_font_size)
                font.setBold(True)
                label.setFont(font)
                label.setMinimumSize(*stat_size)
            
            # Update button fonts
            button_font_size = font_sizes.get("button", 14)
            for button in [self.back_button, self.restart_button]:
                font = button.font()
                font.setFamily("Georgia")
                font.setPointSize(button_font_size)
                font.setBold(True)
                button.setFont(font)
            
        except Exception as e:
            logger.error(f"Failed to update responsive styling: {e}")
