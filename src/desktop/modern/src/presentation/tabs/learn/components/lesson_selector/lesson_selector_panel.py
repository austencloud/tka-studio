"""
Lesson Selector Panel Component

Main panel for lesson selection with mode toggle and lesson buttons.
Follows the modern component architecture pattern.
"""

import logging
from functools import partial
from typing import Optional, Dict

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

from core.interfaces.learn_services import ILessonConfigurationService, ILearnUIService
from domain.models.learn import LessonType, QuizMode
from .lesson_mode_toggle import LessonModeToggle
from .lesson_button import LessonButton

logger = logging.getLogger(__name__)


class LessonSelectorPanel(QWidget):
    """
    Modern lesson selector panel following component architecture.
    
    Provides lesson selection interface with mode toggle and 
    responsive design matching legacy behavior.
    """
    
    # Signals for communication
    lesson_selected = pyqtSignal(str, str)  # (lesson_type, mode)
    
    def __init__(
        self,
        lesson_config_service: ILessonConfigurationService,
        ui_service: ILearnUIService,
        parent: Optional[QWidget] = None
    ):
        """
        Initialize lesson selector panel.
        
        Args:
            lesson_config_service: Service for lesson configurations
            ui_service: Service for UI calculations
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.lesson_config_service = lesson_config_service
        self.ui_service = ui_service
        
        # UI components
        self.lesson_buttons: Dict[str, LessonButton] = {}
        self.description_labels: Dict[str, QLabel] = {}
        
        self._setup_ui()
        self._setup_connections()
        
        logger.info("Lesson selector panel initialized")
    
    def _setup_ui(self) -> None:
        """Setup the lesson selector UI."""
        try:
            # Main layout
            self.layout = QVBoxLayout(self)
            self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Title label
            self.title_label = QLabel("Select a Lesson:")
            self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._apply_title_styling()
            
            # Mode toggle widget
            self.mode_toggle = LessonModeToggle(self.ui_service, self)
            
            # Add to layout
            self.layout.addStretch(2)
            self.layout.addWidget(self.title_label)
            self.layout.addStretch(1)
            self.layout.addWidget(self.mode_toggle)
            self.layout.addStretch(1)
            
            # Create lesson buttons
            self._create_lesson_buttons()
            
            self.layout.addStretch(2)
            
        except Exception as e:
            logger.error(f"Failed to setup lesson selector UI: {e}")
    
    def _apply_title_styling(self) -> None:
        """Apply styling to title label."""
        try:
            self.title_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                }
            """)
        except Exception as e:
            logger.error(f"Failed to apply title styling: {e}")
    
    def _create_lesson_buttons(self) -> None:
        """Create buttons for each lesson type."""
        try:
            lesson_configs = self.lesson_config_service.get_all_lesson_configs()
            
            # Define lesson information matching legacy order
            lesson_info = [
                ("Lesson 1", "Match the correct letter to the given pictograph", LessonType.PICTOGRAPH_TO_LETTER),
                ("Lesson 2", "Identify the correct pictograph for the displayed letter", LessonType.LETTER_TO_PICTOGRAPH),
                ("Lesson 3", "Choose the pictograph that logically follows", LessonType.VALID_NEXT_PICTOGRAPH),
            ]
            
            for lesson_name, description, lesson_type in lesson_info:
                self._add_lesson_button(lesson_name, description, lesson_type)
                
        except Exception as e:
            logger.error(f"Failed to create lesson buttons: {e}")
    
    def _add_lesson_button(self, button_text: str, description_text: str, lesson_type: LessonType) -> None:
        """
        Create and add a lesson button with description.
        
        Args:
            button_text: Text for the button
            description_text: Description text below button
            lesson_type: Associated lesson type
        """
        try:
            # Create vertical layout for button + description
            lesson_layout = QVBoxLayout()
            lesson_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Create button
            button = LessonButton(button_text, self)
            button.set_lesson_description(description_text)
            button.clicked.connect(partial(self._on_lesson_selected, lesson_type))
            self.lesson_buttons[button_text] = button
            
            # Create description label
            description_label = QLabel(description_text)
            description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            description_label.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.8);
                    font-family: Georgia;
                }
            """)
            self.description_labels[button_text] = description_label
            
            # Add to layout
            lesson_layout.addWidget(button)
            lesson_layout.addWidget(description_label)
            
            self.layout.addLayout(lesson_layout)
            self.layout.addStretch(1)
            
        except Exception as e:
            logger.error(f"Failed to add lesson button {button_text}: {e}")
    
    def _setup_connections(self) -> None:
        """Setup signal connections."""
        try:
            # Mode toggle signals
            self.mode_toggle.mode_changed.connect(self._on_mode_changed)
        except Exception as e:
            logger.error(f"Failed to setup lesson selector connections: {e}")
    
    def _on_lesson_selected(self, lesson_type: LessonType) -> None:
        """
        Handle lesson selection.
        
        Args:
            lesson_type: Selected lesson type
        """
        try:
            mode = self.mode_toggle.get_selected_mode()
            self.lesson_selected.emit(lesson_type.value, mode.value)
            logger.info(f"Lesson selected: {lesson_type.value} in {mode.value} mode")
        except Exception as e:
            logger.error(f"Failed to handle lesson selection: {e}")
    
    def _on_mode_changed(self, mode_value: str) -> None:
        """
        Handle mode change.
        
        Args:
            mode_value: New mode value
        """
        logger.debug(f"Quiz mode changed to: {mode_value}")
    
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
            
            # Get responsive sizes from UI service
            font_sizes = self.ui_service.get_font_sizes(parent_width, parent_height)
            component_sizes = self.ui_service.get_component_sizes(parent_width, parent_height)
            
            # Update title font
            title_font_size = font_sizes.get("title", 24)
            font = self.title_label.font()
            font.setFamily("Georgia")
            font.setPointSize(title_font_size)
            font.setBold(True)
            self.title_label.setFont(font)
            
            # Update button sizes and fonts
            button_size = component_sizes.get("lesson_button", (200, 50))
            button_font_size = font_sizes.get("lesson_button", 14)
            
            for button in self.lesson_buttons.values():
                button.update_size(*button_size)
                button.update_font_size(button_font_size)
            
            # Update description fonts
            description_font_size = font_sizes.get("description", 12)
            for label in self.description_labels.values():
                font = label.font()
                font.setFamily("Georgia")
                font.setPointSize(description_font_size)
                label.setFont(font)
            
            # Update mode toggle
            self.mode_toggle.update_responsive_styling(parent_width, parent_height)
            
        except Exception as e:
            logger.error(f"Failed to update responsive styling: {e}")
    
    def get_selected_mode(self) -> QuizMode:
        """
        Get currently selected quiz mode.
        
        Returns:
            Selected quiz mode
        """
        try:
            return self.mode_toggle.get_selected_mode()
        except Exception as e:
            logger.error(f"Failed to get selected mode: {e}")
            return QuizMode.FIXED_QUESTION
    
    def set_mode(self, mode: QuizMode) -> None:
        """
        Set the selected quiz mode.
        
        Args:
            mode: Quiz mode to select
        """
        try:
            self.mode_toggle.set_selected_mode(mode)
        except Exception as e:
            logger.error(f"Failed to set mode: {e}")
