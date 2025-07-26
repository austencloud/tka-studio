"""
Lesson Controls Component

Provides navigation and control buttons for the lesson widget
including go back button and other lesson controls.
"""

import logging
from typing import Optional

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

from desktop.modern.core.interfaces.learn_services import ILearnUIService

logger = logging.getLogger(__name__)


class LessonControls(QWidget):
    """
    Component for lesson navigation and control buttons.
    
    Provides buttons for going back, pausing, and other lesson controls
    with consistent styling and responsive behavior.
    """
    
    # Signals
    back_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    restart_clicked = pyqtSignal()
    
    def __init__(
        self,
        ui_service: ILearnUIService,
        parent: Optional[QWidget] = None
    ):
        """
        Initialize lesson controls.
        
        Args:
            ui_service: Service for UI calculations
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.ui_service = ui_service
        
        self._setup_ui()
        self._setup_connections()
        
        logger.debug("Lesson controls initialized")
    
    def _setup_ui(self) -> None:
        """Setup controls UI."""
        try:
            layout = QHBoxLayout(self)
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            
            # Go back button (primary control)
            self.go_back_button = self._create_control_button("← Back", "go_back")
            layout.addWidget(self.go_back_button)
            
            # Add stretch to push other controls to the right if needed
            layout.addStretch()
            
            # Additional controls (initially hidden)
            self.pause_button = self._create_control_button("⏸ Pause", "pause")
            self.pause_button.setVisible(False)
            layout.addWidget(self.pause_button)
            
            self.restart_button = self._create_control_button("↻ Restart", "restart") 
            self.restart_button.setVisible(False)
            layout.addWidget(self.restart_button)
            
        except Exception as e:
            logger.error(f"Failed to setup controls UI: {e}")
    
    def _create_control_button(self, text: str, button_type: str) -> QPushButton:
        """
        Create a control button with consistent styling.
        
        Args:
            text: Button text
            button_type: Type of button for styling
            
        Returns:
            Configured control button
        """
        try:
            button = QPushButton(text)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # Apply styling based on button type
            if button_type == "go_back":
                button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(255, 255, 255, 0.2);
                        border: 2px solid rgba(255, 255, 255, 0.3);
                        border-radius: 12px;
                        color: white;
                        font-family: Georgia;
                        font-weight: bold;
                        padding: 8px 16px;
                        min-width: 80px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 0.3);
                        border: 2px solid rgba(255, 255, 255, 0.5);
                    }
                    QPushButton:pressed {
                        background-color: rgba(255, 255, 255, 0.4);
                    }
                """)
            else:
                # Secondary buttons with subtle styling
                button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(255, 255, 255, 0.1);
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        border-radius: 8px;
                        color: rgba(255, 255, 255, 0.8);
                        font-family: Georgia;
                        padding: 6px 12px;
                        min-width: 60px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 0.2);
                        border: 1px solid rgba(255, 255, 255, 0.4);
                        color: white;
                    }
                    QPushButton:pressed {
                        background-color: rgba(255, 255, 255, 0.3);
                    }
                """)
            
            return button
            
        except Exception as e:
            logger.error(f"Failed to create control button: {e}")
            return QPushButton("Error")
    
    def _setup_connections(self) -> None:
        """Setup button signal connections."""
        try:
            self.go_back_button.clicked.connect(self.back_clicked.emit)
            self.pause_button.clicked.connect(self.pause_clicked.emit)
            self.restart_button.clicked.connect(self.restart_clicked.emit)
        except Exception as e:
            logger.error(f"Failed to setup control connections: {e}")
    
    def show_pause_button(self, show: bool = True) -> None:
        """
        Show or hide the pause button.
        
        Args:
            show: Whether to show the pause button
        """
        try:
            self.pause_button.setVisible(show)
            logger.debug(f"Pause button {'shown' if show else 'hidden'}")
        except Exception as e:
            logger.error(f"Failed to show/hide pause button: {e}")
    
    def show_restart_button(self, show: bool = True) -> None:
        """
        Show or hide the restart button.
        
        Args:
            show: Whether to show the restart button
        """
        try:
            self.restart_button.setVisible(show)
            logger.debug(f"Restart button {'shown' if show else 'hidden'}")
        except Exception as e:
            logger.error(f"Failed to show/hide restart button: {e}")
    
    def set_pause_state(self, is_paused: bool) -> None:
        """
        Update pause button to reflect current state.
        
        Args:
            is_paused: Whether lesson is currently paused
        """
        try:
            if is_paused:
                self.pause_button.setText("▶ Resume")
            else:
                self.pause_button.setText("⏸ Pause")
            
            logger.debug(f"Pause button set to {'resume' if is_paused else 'pause'} state")
            
        except Exception as e:
            logger.error(f"Failed to set pause state: {e}")
    
    def enable_controls(self, enabled: bool = True) -> None:
        """
        Enable or disable all control buttons.
        
        Args:
            enabled: Whether to enable controls
        """
        try:
            self.go_back_button.setEnabled(enabled)
            self.pause_button.setEnabled(enabled)
            self.restart_button.setEnabled(enabled)
            
            logger.debug(f"Controls {'enabled' if enabled else 'disabled'}")
            
        except Exception as e:
            logger.error(f"Failed to enable/disable controls: {e}")
    
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
            
            # Update go back button size (primary control)
            go_back_size = component_sizes.get("go_back_button", (100, 40))
            go_back_font_size = font_sizes.get("control_button", 14)
            
            self.go_back_button.setMinimumSize(*go_back_size)
            font = self.go_back_button.font()
            font.setFamily("Georgia")
            font.setPointSize(go_back_font_size)
            font.setBold(True)
            self.go_back_button.setFont(font)
            
            # Update secondary button sizes
            control_size = component_sizes.get("control_button", (120, 45))
            control_font_size = font_sizes.get("button", 12)
            
            for button in [self.pause_button, self.restart_button]:
                button.setMinimumSize(*control_size)
                font = button.font()
                font.setFamily("Georgia")
                font.setPointSize(control_font_size)
                button.setFont(font)
            
        except Exception as e:
            logger.error(f"Failed to update responsive styling: {e}")
    
    def reset_controls(self) -> None:
        """Reset controls to initial state."""
        try:
            # Show only go back button
            self.show_pause_button(False)
            self.show_restart_button(False)
            
            # Reset pause button text
            self.set_pause_state(False)
            
            # Enable all controls
            self.enable_controls(True)
            
            logger.debug("Controls reset to initial state")
            
        except Exception as e:
            logger.error(f"Failed to reset controls: {e}")
