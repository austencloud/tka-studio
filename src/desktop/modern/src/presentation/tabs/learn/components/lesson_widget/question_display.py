"""
Question Display Component

Displays quiz questions in different formats (pictographs, letters)
based on the lesson type and question configuration.
"""

import logging
from typing import Optional, Any

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from core.interfaces.learn_services import ILearnUIService
from domain.models.learn import QuestionData

logger = logging.getLogger(__name__)


class QuestionDisplay(QWidget):
    """
    Component for displaying quiz questions.
    
    Handles different question formats including pictographs and letters
    with appropriate rendering and styling.
    """
    
    def __init__(
        self,
        ui_service: ILearnUIService,
        parent: Optional[QWidget] = None
    ):
        """
        Initialize question display.
        
        Args:
            ui_service: Service for UI calculations
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.ui_service = ui_service
        self.current_question: Optional[QuestionData] = None
        self.current_format: str = ""
        
        self._setup_ui()
        
        logger.debug("Question display component initialized")
    
    def _setup_ui(self) -> None:
        """Setup question display UI."""
        try:
            self.layout = QVBoxLayout(self)
            self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Question content widget (will be replaced based on format)
            self.content_widget: Optional[QWidget] = None
            
            # Placeholder label
            self.placeholder_label = QLabel("Question will appear here")
            self.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.placeholder_label.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.6);
                    font-family: Georgia;
                    font-style: italic;
                }
            """)
            
            self.layout.addWidget(self.placeholder_label)
            
        except Exception as e:
            logger.error(f"Failed to setup question display UI: {e}")
    
    def show_question(self, question: QuestionData, format_type: str) -> None:
        """
        Display a question with the specified format.
        
        Args:
            question: Question data to display
            format_type: Format type ("pictograph", "letter", etc.)
        """
        try:
            if not question:
                logger.warning("Cannot display empty question")
                return
            
            self.current_question = question
            self.current_format = format_type
            
            # Clear existing content
            self._clear_content()
            
            # Display based on format
            if format_type == "pictograph":
                self._display_pictograph(question.question_content)
            elif format_type == "letter":
                self._display_letter(question.question_content)
            else:
                logger.warning(f"Unknown question format: {format_type}")
                self._display_text(str(question.question_content))
            
            logger.debug(f"Displayed {format_type} question: {question.question_id}")
            
        except Exception as e:
            logger.error(f"Failed to show question: {e}")
    
    def _display_pictograph(self, pictograph_data: Any) -> None:
        """
        Display a pictograph question.
        
        Args:
            pictograph_data: Pictograph data to display
        """
        try:
            # For now, display a placeholder for pictograph
            # In a full implementation, this would use the pictograph rendering system
            pictograph_label = QLabel("Pictograph Display\n(Implementation Pending)")
            pictograph_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pictograph_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-family: Georgia;
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 8px;
                    padding: 20px;
                    background-color: rgba(255, 255, 255, 0.1);
                    min-width: 200px;
                    min-height: 150px;
                }
            """)
            
            self.content_widget = pictograph_label
            self.layout.addWidget(self.content_widget)
            
            logger.debug("Displayed pictograph (placeholder)")
            
        except Exception as e:
            logger.error(f"Failed to display pictograph: {e}")
    
    def _display_letter(self, letter_content: Any) -> None:
        """
        Display a letter question.
        
        Args:
            letter_content: Letter content to display
        """
        try:
            letter_label = QLabel(str(letter_content))
            letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            letter_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-family: Georgia;
                    font-size: 48px;
                    font-weight: bold;
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 8px;
                    padding: 30px;
                    background-color: rgba(255, 255, 255, 0.1);
                    min-width: 100px;
                    min-height: 100px;
                }
            """)
            
            self.content_widget = letter_label
            self.layout.addWidget(self.content_widget)
            
            logger.debug(f"Displayed letter: {letter_content}")
            
        except Exception as e:
            logger.error(f"Failed to display letter: {e}")
    
    def _display_text(self, text_content: str) -> None:
        """
        Display generic text content.
        
        Args:
            text_content: Text content to display
        """
        try:
            text_label = QLabel(text_content)
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            text_label.setWordWrap(True)
            text_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-family: Georgia;
                    font-size: 18px;
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 8px;
                    padding: 20px;
                    background-color: rgba(255, 255, 255, 0.1);
                }
            """)
            
            self.content_widget = text_label
            self.layout.addWidget(self.content_widget)
            
            logger.debug(f"Displayed text: {text_content[:50]}...")
            
        except Exception as e:
            logger.error(f"Failed to display text: {e}")
    
    def _clear_content(self) -> None:
        """Clear existing question content."""
        try:
            # Remove current content widget
            if self.content_widget:
                self.layout.removeWidget(self.content_widget)
                self.content_widget.deleteLater()
                self.content_widget = None
            
            # Remove placeholder if present
            if self.placeholder_label:
                self.layout.removeWidget(self.placeholder_label)
                
        except Exception as e:
            logger.error(f"Failed to clear question content: {e}")
    
    def clear_question(self) -> None:
        """Clear the current question and show placeholder."""
        try:
            self._clear_content()
            
            # Re-add placeholder
            self.layout.addWidget(self.placeholder_label)
            
            self.current_question = None
            self.current_format = ""
            
            logger.debug("Question display cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear question: {e}")
    
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
            
            # Update content widget size if it exists
            if self.content_widget:
                display_size = component_sizes.get("question_display", (300, 200))
                self.content_widget.setMinimumSize(*display_size)
                
                # Update font size based on content type
                if self.current_format == "letter":
                    # Larger font for letters
                    letter_font_size = max(font_sizes.get("title", 24) * 2, 36)
                    font = self.content_widget.font()
                    font.setPointSize(letter_font_size)
                    self.content_widget.setFont(font)
            
            # Update placeholder font
            placeholder_font_size = font_sizes.get("subtitle", 16)
            font = self.placeholder_label.font()
            font.setPointSize(placeholder_font_size)
            self.placeholder_label.setFont(font)
            
        except Exception as e:
            logger.error(f"Failed to update responsive styling: {e}")
