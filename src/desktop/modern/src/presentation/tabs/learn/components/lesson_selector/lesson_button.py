"""
Lesson Button Component

Styled button for lesson selection with responsive design and
hover effects matching the legacy implementation.
"""

import logging
from typing import Optional

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)


class LessonButton(QPushButton):
    """
    Styled lesson selection button.
    
    Provides consistent styling and responsive behavior
    for lesson selection buttons.
    """
    
    def __init__(
        self, 
        text: str, 
        parent: Optional[object] = None
    ):
        """
        Initialize lesson button.
        
        Args:
            text: Button text
            parent: Parent widget
        """
        super().__init__(text, parent)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._setup_styling()
        
        logger.debug(f"Lesson button initialized: {text}")
    
    def _setup_styling(self) -> None:
        """Setup button styling matching legacy implementation."""
        try:
            self.setStyleSheet("""
                LessonButton {
                    background-color: rgba(255, 255, 255, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 14px;
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    padding: 8px 16px;
                }
                LessonButton:hover {
                    background-color: rgba(255, 255, 255, 0.3);
                    border: 2px solid rgba(255, 255, 255, 0.5);
                }
                LessonButton:pressed {
                    background-color: rgba(255, 255, 255, 0.4);
                    border: 2px solid rgba(255, 255, 255, 0.6);
                }
                LessonButton:disabled {
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    color: rgba(255, 255, 255, 0.5);
                }
            """)
        except Exception as e:
            logger.error(f"Failed to setup button styling: {e}")
    
    def update_font_size(self, size: int) -> None:
        """
        Update button font size for responsive design.
        
        Args:
            size: Font size in points
        """
        try:
            font = self.font()
            font.setFamily("Georgia")
            font.setPointSize(max(size, 8))  # Minimum size
            font.setBold(True)
            self.setFont(font)
        except Exception as e:
            logger.error(f"Failed to update font size: {e}")
    
    def update_size(self, width: int, height: int) -> None:
        """
        Update button size for responsive design.
        
        Args:
            width: Button width
            height: Button height
        """
        try:
            # Ensure minimum size
            final_width = max(width, 120)
            final_height = max(height, 40)
            
            self.setFixedSize(final_width, final_height)
        except Exception as e:
            logger.error(f"Failed to update button size: {e}")
    
    def set_lesson_description(self, description: str) -> None:
        """
        Set tooltip with lesson description.
        
        Args:
            description: Lesson description text
        """
        try:
            self.setToolTip(description)
        except Exception as e:
            logger.error(f"Failed to set lesson description: {e}")
