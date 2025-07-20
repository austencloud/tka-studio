"""
Lesson Mode Toggle Component

Provides radio button interface for selecting between fixed question
and countdown quiz modes.
"""

import logging
from typing import Optional

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QRadioButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

from core.interfaces.learn_services import ILearnUIService
from domain.models.learn import QuizMode

logger = logging.getLogger(__name__)


class LessonModeToggle(QWidget):
    """
    Widget for toggling between quiz modes.
    
    Provides radio button interface for selecting fixed question mode
    or countdown mode with descriptive labels.
    """
    
    # Signals
    mode_changed = pyqtSignal(str)  # mode value
    
    def __init__(
        self, 
        ui_service: ILearnUIService,
        parent: Optional[QWidget] = None
    ):
        """
        Initialize lesson mode toggle.
        
        Args:
            ui_service: Service for UI calculations
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.ui_service = ui_service
        
        self._setup_ui()
        self._setup_connections()
        
        logger.debug("Lesson mode toggle initialized")
    
    def _setup_ui(self) -> None:
        """Setup mode toggle UI."""
        try:
            layout = QHBoxLayout(self)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Fixed question mode
            self.fixed_question_radio = QRadioButton("Fixed Questions (20)")
            self.fixed_question_radio.setChecked(True)  # Default selection
            self.fixed_question_label = QLabel("Answer 20 questions")
            
            # Countdown mode
            self.countdown_radio = QRadioButton("Countdown (2 min)")
            self.countdown_label = QLabel("Answer as many as possible in 2 minutes")
            
            # Apply styling
            self._apply_styling()
            
            # Add to layout
            layout.addWidget(self.fixed_question_radio)
            layout.addWidget(self.fixed_question_label)
            layout.addStretch()
            layout.addWidget(self.countdown_radio)
            layout.addWidget(self.countdown_label)
            
        except Exception as e:
            logger.error(f"Failed to setup mode toggle UI: {e}")
    
    def _setup_connections(self) -> None:
        """Setup signal connections."""
        try:
            self.fixed_question_radio.toggled.connect(self._on_mode_changed)
            self.countdown_radio.toggled.connect(self._on_mode_changed)
        except Exception as e:
            logger.error(f"Failed to setup mode toggle connections: {e}")
    
    def _apply_styling(self) -> None:
        """Apply styling to mode toggle components."""
        try:
            # Radio button styling
            radio_style = """
                QRadioButton {
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                    border-radius: 8px;
                    border: 2px solid rgba(255, 255, 255, 0.5);
                    background-color: transparent;
                }
                QRadioButton::indicator:checked {
                    background-color: rgba(255, 255, 255, 0.8);
                    border: 2px solid white;
                }
                QRadioButton::indicator:hover {
                    border: 2px solid rgba(255, 255, 255, 0.7);
                }
            """
            
            # Label styling
            label_style = """
                QLabel {
                    color: rgba(255, 255, 255, 0.8);
                    font-family: Georgia;
                    margin-left: 5px;
                }
            """
            
            self.fixed_question_radio.setStyleSheet(radio_style)
            self.countdown_radio.setStyleSheet(radio_style)
            self.fixed_question_label.setStyleSheet(label_style)
            self.countdown_label.setStyleSheet(label_style)
            
        except Exception as e:
            logger.error(f"Failed to apply mode toggle styling: {e}")
    
    def _on_mode_changed(self) -> None:
        """Handle mode selection change."""
        try:
            selected_mode = self.get_selected_mode()
            self.mode_changed.emit(selected_mode.value)
            logger.debug(f"Mode changed to: {selected_mode.value}")
        except Exception as e:
            logger.error(f"Failed to handle mode change: {e}")
    
    def get_selected_mode(self) -> QuizMode:
        """
        Get currently selected quiz mode.
        
        Returns:
            Selected quiz mode
        """
        try:
            if self.fixed_question_radio.isChecked():
                return QuizMode.FIXED_QUESTION
            else:
                return QuizMode.COUNTDOWN
        except Exception as e:
            logger.error(f"Failed to get selected mode: {e}")
            return QuizMode.FIXED_QUESTION  # Default fallback
    
    def set_selected_mode(self, mode: QuizMode) -> None:
        """
        Set the selected quiz mode.
        
        Args:
            mode: Quiz mode to select
        """
        try:
            if mode == QuizMode.FIXED_QUESTION:
                self.fixed_question_radio.setChecked(True)
            elif mode == QuizMode.COUNTDOWN:
                self.countdown_radio.setChecked(True)
            else:
                logger.warning(f"Unknown quiz mode: {mode}")
        except Exception as e:
            logger.error(f"Failed to set selected mode: {e}")
    
    def update_responsive_styling(self, parent_width: int, parent_height: int) -> None:
        """
        Update styling based on parent widget size.
        
        Args:
            parent_width: Parent widget width
            parent_height: Parent widget height
        """
        try:
            # Get responsive font sizes
            font_sizes = self.ui_service.get_font_sizes(parent_width, parent_height)
            
            # Update radio button fonts
            radio_font_size = font_sizes.get("mode_label", 12)
            for radio in [self.fixed_question_radio, self.countdown_radio]:
                font = radio.font()
                font.setFamily("Georgia")
                font.setPointSize(radio_font_size)
                radio.setFont(font)
            
            # Update label fonts
            label_font_size = font_sizes.get("mode_description", 10)
            for label in [self.fixed_question_label, self.countdown_label]:
                font = label.font()
                font.setFamily("Georgia")
                font.setPointSize(label_font_size)
                label.setFont(font)
            
        except Exception as e:
            logger.error(f"Failed to update responsive styling: {e}")
