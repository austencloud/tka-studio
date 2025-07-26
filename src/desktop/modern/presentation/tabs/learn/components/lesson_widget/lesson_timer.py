"""
Lesson Timer Component

Manages countdown timer for quiz sessions with visual display
and time expiration handling.
"""

import logging
from typing import Optional

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

from desktop.modern.core.interfaces.learn_services import ILearnUIService

logger = logging.getLogger(__name__)


class LessonTimer(QWidget):
    """
    Component for managing and displaying lesson timer.
    
    Provides countdown functionality for timed quiz modes
    with visual feedback and expiration signals.
    """
    
    # Signals
    time_expired = pyqtSignal()
    time_updated = pyqtSignal(int)  # remaining seconds
    
    def __init__(
        self,
        ui_service: ILearnUIService,
        parent: Optional[QWidget] = None
    ):
        """
        Initialize lesson timer.
        
        Args:
            ui_service: Service for UI calculations
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.ui_service = ui_service
        self.remaining_time: int = 0
        self.is_running: bool = False
        
        # Qt timer for countdown
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_timer_tick)
        
        self._setup_ui()
        
        logger.debug("Lesson timer initialized")
    
    def _setup_ui(self) -> None:
        """Setup timer UI."""
        try:
            layout = QHBoxLayout(self)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Timer display label
            self.time_label = QLabel("2:00")
            self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._apply_styling()
            
            layout.addWidget(self.time_label)
            
            # Initially hidden
            self.setVisible(False)
            
        except Exception as e:
            logger.error(f"Failed to setup timer UI: {e}")
    
    def _apply_styling(self) -> None:
        """Apply styling to timer label."""
        try:
            self.time_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    font-size: 18px;
                    background-color: rgba(255, 255, 255, 0.15);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 8px;
                    padding: 10px 20px;
                    min-width: 80px;
                }
            """)
        except Exception as e:
            logger.error(f"Failed to apply timer styling: {e}")
    
    def start_countdown(self, duration_seconds: int) -> None:
        """
        Start countdown timer.
        
        Args:
            duration_seconds: Duration in seconds
        """
        try:
            self.remaining_time = duration_seconds
            self.is_running = True
            
            # Update display immediately
            self._update_display()
            
            # Start Qt timer (1 second intervals)
            self.timer.start(1000)
            
            # Show timer
            self.setVisible(True)
            
            logger.info(f"Started countdown timer: {duration_seconds} seconds")
            
        except Exception as e:
            logger.error(f"Failed to start countdown: {e}")
    
    def stop_timer(self) -> None:
        """Stop the countdown timer."""
        try:
            self.is_running = False
            self.timer.stop()
            
            logger.debug("Timer stopped")
            
        except Exception as e:
            logger.error(f"Failed to stop timer: {e}")
    
    def pause_timer(self) -> None:
        """Pause the countdown timer."""
        try:
            if self.is_running:
                self.timer.stop()
                logger.debug("Timer paused")
        except Exception as e:
            logger.error(f"Failed to pause timer: {e}")
    
    def resume_timer(self) -> None:
        """Resume the countdown timer."""
        try:
            if self.is_running and not self.timer.isActive():
                self.timer.start(1000)
                logger.debug("Timer resumed")
        except Exception as e:
            logger.error(f"Failed to resume timer: {e}")
    
    def update_time_remaining(self, seconds: int) -> None:
        """
        Update remaining time without affecting timer state.
        
        Args:
            seconds: Remaining seconds
        """
        try:
            self.remaining_time = seconds
            self._update_display()
        except Exception as e:
            logger.error(f"Failed to update time remaining: {e}")
    
    def _on_timer_tick(self) -> None:
        """Handle timer tick (called every second)."""
        try:
            if not self.is_running:
                return
            
            self.remaining_time -= 1
            self._update_display()
            
            # Emit time update signal
            self.time_updated.emit(self.remaining_time)
            
            # Check if time expired
            if self.remaining_time <= 0:
                self._on_time_expired()
                
        except Exception as e:
            logger.error(f"Failed to handle timer tick: {e}")
    
    def _on_time_expired(self) -> None:
        """Handle time expiration."""
        try:
            self.stop_timer()
            self.remaining_time = 0
            self._update_display()
            
            # Change styling to indicate expiration
            self.time_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    font-size: 18px;
                    background-color: rgba(255, 0, 0, 0.3);
                    border: 2px solid rgba(255, 0, 0, 0.5);
                    border-radius: 8px;
                    padding: 10px 20px;
                    min-width: 80px;
                }
            """)
            
            # Emit expiration signal
            self.time_expired.emit()
            
            logger.info("Timer expired")
            
        except Exception as e:
            logger.error(f"Failed to handle time expiration: {e}")
    
    def _update_display(self) -> None:
        """Update timer display with current remaining time."""
        try:
            minutes, seconds = divmod(max(0, self.remaining_time), 60)
            time_text = f"{minutes}:{seconds:02d}"
            
            self.time_label.setText(time_text)
            
            # Change color as time runs low
            if self.remaining_time <= 30 and self.remaining_time > 10:
                # Warning - yellow/orange
                self.time_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-family: Georgia;
                        font-weight: bold;
                        font-size: 18px;
                        background-color: rgba(255, 165, 0, 0.3);
                        border: 2px solid rgba(255, 165, 0, 0.5);
                        border-radius: 8px;
                        padding: 10px 20px;
                        min-width: 80px;
                    }
                """)
            elif self.remaining_time <= 10 and self.remaining_time > 0:
                # Critical - red
                self.time_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-family: Georgia;
                        font-weight: bold;
                        font-size: 18px;
                        background-color: rgba(255, 0, 0, 0.3);
                        border: 2px solid rgba(255, 0, 0, 0.5);
                        border-radius: 8px;
                        padding: 10px 20px;
                        min-width: 80px;
                    }
                """)
            elif self.remaining_time > 30:
                # Normal - default styling
                self._apply_styling()
            
        except Exception as e:
            logger.error(f"Failed to update timer display: {e}")
    
    def hide_timer(self) -> None:
        """Hide the timer display."""
        try:
            self.setVisible(False)
            logger.debug("Timer hidden")
        except Exception as e:
            logger.error(f"Failed to hide timer: {e}")
    
    def show_timer(self) -> None:
        """Show the timer display."""
        try:
            self.setVisible(True)
            logger.debug("Timer shown")
        except Exception as e:
            logger.error(f"Failed to show timer: {e}")
    
    def reset(self) -> None:
        """Reset timer to initial state."""
        try:
            self.stop_timer()
            self.remaining_time = 0
            self.time_label.setText("2:00")
            self._apply_styling()
            self.setVisible(False)
            
            logger.debug("Timer reset")
            
        except Exception as e:
            logger.error(f"Failed to reset timer: {e}")
    
    def get_remaining_time(self) -> int:
        """
        Get remaining time in seconds.
        
        Returns:
            Remaining time in seconds
        """
        return self.remaining_time
    
    def is_timer_running(self) -> bool:
        """
        Check if timer is currently running.
        
        Returns:
            True if timer is running, False otherwise
        """
        return self.is_running and self.timer.isActive()
    
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
            
            # Update timer font size
            timer_font_size = font_sizes.get("timer", 16)
            font = self.time_label.font()
            font.setFamily("Georgia")
            font.setPointSize(timer_font_size)
            font.setBold(True)
            self.time_label.setFont(font)
            
            # Update timer size
            timer_size = component_sizes.get("timer_display", (150, 40))
            self.time_label.setMinimumSize(*timer_size)
            
        except Exception as e:
            logger.error(f"Failed to update responsive styling: {e}")
