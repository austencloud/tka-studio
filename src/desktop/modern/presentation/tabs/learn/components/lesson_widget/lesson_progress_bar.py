"""
Lesson Progress Bar Component

Displays lesson progress for both fixed question and countdown modes
with appropriate formatting and visual feedback.
"""

import logging
from typing import Optional, Dict, Any

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt

from desktop.modern.core.interfaces.learn_services import ILearnUIService

logger = logging.getLogger(__name__)


class LessonProgressBar(QWidget):
    """
    Component for displaying lesson progress.
    
    Shows progress information appropriate for the quiz mode:
    - Fixed question mode: X/Y questions
    - Countdown mode: Time remaining
    """
    
    def __init__(
        self,
        ui_service: ILearnUIService,
        parent: Optional[QWidget] = None
    ):
        """
        Initialize lesson progress bar.
        
        Args:
            ui_service: Service for UI calculations
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.ui_service = ui_service
        self.current_mode: str = "fixed_question"
        
        self._setup_ui()
        
        logger.debug("Lesson progress bar initialized")
    
    def _setup_ui(self) -> None:
        """Setup progress bar UI."""
        try:
            layout = QHBoxLayout(self)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Progress label
            self.progress_label = QLabel("Progress: 0/20")
            self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._apply_label_styling()
            
            # Progress bar (optional visual indicator)
            self.progress_bar = QProgressBar()
            self.progress_bar.setVisible(False)  # Hidden by default
            self._apply_progress_bar_styling()
            
            layout.addWidget(self.progress_label)
            layout.addWidget(self.progress_bar)
            
        except Exception as e:
            logger.error(f"Failed to setup progress bar UI: {e}")
    
    def _apply_label_styling(self) -> None:
        """Apply styling to progress label."""
        try:
            self.progress_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 6px;
                    padding: 8px 16px;
                }
            """)
        except Exception as e:
            logger.error(f"Failed to apply label styling: {e}")
    
    def _apply_progress_bar_styling(self) -> None:
        """Apply styling to progress bar."""
        try:
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 8px;
                    background-color: rgba(255, 255, 255, 0.1);
                    text-align: center;
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                }
                QProgressBar::chunk {
                    background-color: rgba(0, 255, 0, 0.7);
                    border-radius: 6px;
                }
            """)
        except Exception as e:
            logger.error(f"Failed to apply progress bar styling: {e}")
    
    def set_question_mode(self, total_questions: int = 20) -> None:
        """
        Set progress bar to question mode.
        
        Args:
            total_questions: Total number of questions
        """
        try:
            self.current_mode = "fixed_question"
            
            # Configure for question counting
            self.progress_bar.setRange(0, total_questions)
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)
            
            # Update label
            self.progress_label.setText(f"Progress: 0/{total_questions}")
            
            logger.debug(f"Set question mode with {total_questions} total questions")
            
        except Exception as e:
            logger.error(f"Failed to set question mode: {e}")
    
    def set_timer_mode(self) -> None:
        """Set progress bar to timer mode."""
        try:
            self.current_mode = "countdown"
            
            # Hide progress bar for timer mode
            self.progress_bar.setVisible(False)
            
            # Update label
            self.progress_label.setText("Time Remaining: 2:00")
            
            logger.debug("Set timer mode")
            
        except Exception as e:
            logger.error(f"Failed to set timer mode: {e}")
    
    def update_progress(self, progress_info: Dict[str, Any]) -> None:
        """
        Update progress display with new information.
        
        Args:
            progress_info: Dictionary containing progress information
        """
        try:
            if not progress_info:
                return
            
            if self.current_mode == "fixed_question":
                self._update_question_progress(progress_info)
            elif self.current_mode == "countdown":
                self._update_timer_progress(progress_info)
                
        except Exception as e:
            logger.error(f"Failed to update progress: {e}")
    
    def _update_question_progress(self, progress_info: Dict[str, Any]) -> None:
        """Update progress for question mode."""
        try:
            current = progress_info.get("current_question", 0)
            total = progress_info.get("total_questions", 20)
            
            # Update progress bar
            self.progress_bar.setValue(current - 1)  # 0-based for progress bar
            
            # Update label
            self.progress_label.setText(f"Progress: {current}/{total}")
            
            logger.debug(f"Updated question progress: {current}/{total}")
            
        except Exception as e:
            logger.error(f"Failed to update question progress: {e}")
    
    def _update_timer_progress(self, progress_info: Dict[str, Any]) -> None:
        """Update progress for timer mode."""
        try:
            time_remaining = progress_info.get("quiz_time_remaining", 120)
            
            # Format time display
            minutes, seconds = divmod(max(0, time_remaining), 60)
            time_text = f"Time Remaining: {minutes}:{seconds:02d}"
            
            self.progress_label.setText(time_text)
            
            logger.debug(f"Updated timer progress: {time_text}")
            
        except Exception as e:
            logger.error(f"Failed to update timer progress: {e}")
    
    def show_completion(self) -> None:
        """Show completion state."""
        try:
            if self.current_mode == "fixed_question":
                self.progress_label.setText("Lesson Complete!")
                self.progress_bar.setValue(self.progress_bar.maximum())
            else:
                self.progress_label.setText("Time's Up!")
            
            # Change styling to indicate completion
            self.progress_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    background-color: rgba(0, 255, 0, 0.3);
                    border: 1px solid rgba(0, 255, 0, 0.5);
                    border-radius: 6px;
                    padding: 8px 16px;
                }
            """)
            
            logger.debug("Showing completion state")
            
        except Exception as e:
            logger.error(f"Failed to show completion: {e}")
    
    def reset(self) -> None:
        """Reset progress display to initial state."""
        try:
            self.progress_label.setText("Progress: 0/20")
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(False)
            
            # Reset styling
            self._apply_label_styling()
            
            logger.debug("Progress bar reset")
            
        except Exception as e:
            logger.error(f"Failed to reset progress bar: {e}")
    
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
            
            # Update label font
            progress_font_size = font_sizes.get("progress", 13)
            font = self.progress_label.font()
            font.setFamily("Georgia")
            font.setPointSize(progress_font_size)
            font.setBold(True)
            self.progress_label.setFont(font)
            
            # Update progress bar size
            progress_bar_size = component_sizes.get("progress_bar", (250, 25))
            self.progress_bar.setMinimumSize(*progress_bar_size)
            
        except Exception as e:
            logger.error(f"Failed to update responsive styling: {e}")
