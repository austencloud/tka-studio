"""
Lesson Timer Component

Focused component for countdown timer display with visual progress
and time remaining indicators for timed quiz modes.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QVBoxLayout, QWidget


logger = logging.getLogger(__name__)


class LessonTimer(QWidget):
    """
    Focused component for lesson countdown timer.

    Provides visual countdown with progress bar and time display
    for timed quiz modes with clear visual feedback.
    """

    # Signals
    time_updated = pyqtSignal(int)  # remaining seconds
    time_expired = pyqtSignal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self._total_time: int = 0
        self._remaining_time: int = 0
        self._is_running: bool = False
        self._is_paused: bool = False

        # Internal timer
        self._timer = QTimer()
        self._timer.timeout.connect(self._on_timer_tick)
        self._timer.setInterval(1000)  # 1 second intervals

        self._setup_ui()

        # Start hidden (shown only for timed modes)
        self.hide()

        logger.debug("Lesson timer component initialized")

    def _setup_ui(self) -> None:
        """Setup timer UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(10, 5, 10, 5)
        main_layout.setSpacing(8)

        # Timer label
        self.time_label = QLabel("Time Remaining: 2:00")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._apply_time_label_styling()

        # Progress bar (shows time remaining)
        self.time_progress = QProgressBar()
        self.time_progress.setTextVisible(False)
        self.time_progress.setFixedHeight(8)
        self._apply_progress_bar_styling()

        # Status container
        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(10)

        # Status label (paused, running, etc.)
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._apply_status_label_styling()

        status_layout.addWidget(self.status_label)

        # Add to main layout
        main_layout.addWidget(self.time_label)
        main_layout.addWidget(self.time_progress)
        main_layout.addWidget(status_container)

    def _apply_time_label_styling(self) -> None:
        """Apply styling to time label."""
        self.time_label.setStyleSheet("""
            QLabel {
                color: white;
                font-family: Georgia;
                font-size: 16px;
                font-weight: bold;
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 8px 16px;
            }
        """)

    def _apply_progress_bar_styling(self) -> None:
        """Apply styling to progress bar."""
        self.time_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                background-color: rgba(255, 255, 255, 0.1);
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(255, 165, 0, 0.8),
                    stop: 0.5 rgba(255, 255, 0, 0.8),
                    stop: 1 rgba(255, 0, 0, 0.8)
                );
                border-radius: 3px;
            }
        """)

    def _apply_status_label_styling(self) -> None:
        """Apply styling to status label."""
        self.status_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-family: Georgia;
                font-size: 12px;
                font-style: italic;
            }
        """)

    def start_countdown(self, total_seconds: int) -> None:
        """
        Start countdown timer.

        Args:
            total_seconds: Total time for countdown in seconds
        """
        try:
            self._total_time = total_seconds
            self._remaining_time = total_seconds
            self._is_running = True
            self._is_paused = False

            # Setup progress bar
            self.time_progress.setMaximum(total_seconds)
            self.time_progress.setValue(total_seconds)

            # Update display
            self._update_display()

            # Start timer
            self._timer.start()

            # Show timer
            self.show()

            logger.info(f"Started countdown timer: {total_seconds} seconds")

        except Exception as e:
            logger.error(f"Failed to start countdown: {e}")

    def pause_timer(self) -> None:
        """Pause the countdown timer."""
        if self._is_running and not self._is_paused:
            self._timer.stop()
            self._is_paused = True
            self.status_label.setText("PAUSED")
            logger.debug("Timer paused")

    def resume_timer(self) -> None:
        """Resume the countdown timer."""
        if self._is_running and self._is_paused:
            self._timer.start()
            self._is_paused = False
            self.status_label.setText("")
            logger.debug("Timer resumed")

    def stop_timer(self) -> None:
        """Stop the countdown timer."""
        self._timer.stop()
        self._is_running = False
        self._is_paused = False
        self.status_label.setText("")
        logger.debug("Timer stopped")

    def hide_timer(self) -> None:
        """Hide the timer (for non-timed modes)."""
        self.stop_timer()
        self.hide()
        logger.debug("Timer hidden")

    def reset(self) -> None:
        """Reset timer to initial state."""
        self.stop_timer()
        self._total_time = 0
        self._remaining_time = 0
        self.time_progress.setValue(0)
        self.time_label.setText("Time Remaining: 0:00")
        self.status_label.setText("")
        self.hide()
        logger.debug("Timer reset")

    def _on_timer_tick(self) -> None:
        """Handle timer tick (every second)."""
        try:
            if not self._is_running or self._is_paused:
                return

            self._remaining_time -= 1

            # Update display
            self._update_display()

            # Emit time update signal
            self.time_updated.emit(self._remaining_time)

            # Check if time expired
            if self._remaining_time <= 0:
                self._on_time_expired()

        except Exception as e:
            logger.error(f"Timer tick error: {e}")

    def _update_display(self) -> None:
        """Update timer display."""
        try:
            # Format time as MM:SS
            minutes = self._remaining_time // 60
            seconds = self._remaining_time % 60
            time_text = f"{minutes}:{seconds:02d}"

            # Update label
            self.time_label.setText(f"Time Remaining: {time_text}")

            # Update progress bar
            self.time_progress.setValue(self._remaining_time)

            # Update styling based on remaining time
            self._update_urgency_styling()

        except Exception as e:
            logger.error(f"Failed to update timer display: {e}")

    def _update_urgency_styling(self) -> None:
        """Update styling based on time urgency."""
        if self._total_time == 0:
            return

        time_percentage = (self._remaining_time / self._total_time) * 100

        if time_percentage <= 10:  # Last 10% - urgent red
            color = "rgba(255, 0, 0, 0.9)"
            bg_color = "rgba(255, 0, 0, 0.2)"
            border_color = "rgba(255, 0, 0, 0.5)"
        elif time_percentage <= 25:  # Last 25% - warning orange
            color = "rgba(255, 165, 0, 0.9)"
            bg_color = "rgba(255, 165, 0, 0.2)"
            border_color = "rgba(255, 165, 0, 0.5)"
        elif time_percentage <= 50:  # Half time - caution yellow
            color = "rgba(255, 255, 0, 0.9)"
            bg_color = "rgba(255, 255, 0, 0.1)"
            border_color = "rgba(255, 255, 0, 0.3)"
        else:  # Plenty of time - normal white
            color = "white"
            bg_color = "rgba(255, 255, 255, 0.1)"
            border_color = "rgba(255, 255, 255, 0.2)"

        self.time_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-family: Georgia;
                font-size: 16px;
                font-weight: bold;
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 6px;
                padding: 8px 16px;
            }}
        """)

    def _on_time_expired(self) -> None:
        """Handle time expiration."""
        self.stop_timer()
        self.time_label.setText("Time's Up!")
        self.status_label.setText("TIME EXPIRED")

        # Set final styling
        self.time_label.setStyleSheet("""
            QLabel {
                color: white;
                font-family: Georgia;
                font-size: 16px;
                font-weight: bold;
                background-color: rgba(255, 0, 0, 0.3);
                border: 2px solid rgba(255, 0, 0, 0.6);
                border-radius: 6px;
                padding: 8px 16px;
            }
        """)

        # Emit expiration signal
        self.time_expired.emit()

        logger.info("Timer expired")

    def get_remaining_time(self) -> int:
        """Get remaining time in seconds."""
        return self._remaining_time

    def get_elapsed_time(self) -> int:
        """Get elapsed time in seconds."""
        return self._total_time - self._remaining_time

    def is_timer_running(self) -> bool:
        """Check if timer is running."""
        return self._is_running and not self._is_paused

    def is_timer_paused(self) -> bool:
        """Check if timer is paused."""
        return self._is_paused

    def update_responsive_styling(self, parent_width: int, parent_height: int) -> None:
        """Update styling based on parent widget size."""
        try:
            # Calculate responsive font size
            font_size = max(12, min(20, parent_width // 40))
            status_font_size = max(10, min(14, parent_width // 60))

            # Update time label font size
            current_style = self.time_label.styleSheet()
            import re

            new_style = re.sub(
                r"font-size:\s*\d+px;", f"font-size: {font_size}px;", current_style
            )
            self.time_label.setStyleSheet(new_style)

            # Update status label font size
            current_style = self.status_label.styleSheet()
            new_style = re.sub(
                r"font-size:\s*\d+px;",
                f"font-size: {status_font_size}px;",
                current_style,
            )
            self.status_label.setStyleSheet(new_style)

            # Update progress bar height
            bar_height = max(6, min(12, parent_height // 60))
            self.time_progress.setFixedHeight(bar_height)

        except Exception as e:
            logger.error(f"Failed to update responsive styling: {e}")
