"""
Progress Controls Component

Focused component for displaying lesson progress including progress bar,
question counter, and accuracy tracking with clean visual design.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QVBoxLayout, QWidget


logger = logging.getLogger(__name__)


class ProgressInfo:
    """Data class for progress information."""

    def __init__(
        self,
        current_question: int = 1,
        total_questions: int = 20,
        correct_answers: int = 0,
        questions_answered: int = 0,
        accuracy_percentage: float = 0.0,
    ):
        self.current_question = current_question
        self.total_questions = total_questions
        self.correct_answers = correct_answers
        self.questions_answered = questions_answered
        self.accuracy_percentage = accuracy_percentage


class ProgressControls(QWidget):
    """
    Focused component for lesson progress display.

    Shows progress bar, question counter, and accuracy metrics
    with responsive design and clear visual hierarchy.
    """

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self._current_progress: ProgressInfo | None = None
        self._is_timer_mode: bool = False

        self._setup_ui()

        logger.debug("Progress controls component initialized")

    def _setup_ui(self) -> None:
        """Setup progress controls UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(10, 5, 10, 5)
        main_layout.setSpacing(8)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(12)
        self._apply_progress_bar_styling()

        # Info container
        info_container = QWidget()
        info_layout = QHBoxLayout(info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(20)

        # Question counter
        self.question_label = QLabel("Question 1 of 20")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._apply_info_label_styling(self.question_label)

        # Accuracy display
        self.accuracy_label = QLabel("Accuracy: 0%")
        self.accuracy_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self._apply_info_label_styling(self.accuracy_label)

        # Add to info layout
        info_layout.addWidget(self.question_label)
        info_layout.addStretch()
        info_layout.addWidget(self.accuracy_label)

        # Add to main layout
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(info_container)

    def _apply_progress_bar_styling(self) -> None:
        """Apply styling to progress bar."""
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                background-color: rgba(255, 255, 255, 0.1);
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(62, 99, 221, 0.8),
                    stop: 1 rgba(82, 119, 241, 0.9)
                );
                border-radius: 5px;
            }
        """)

    def _apply_info_label_styling(self, label: QLabel) -> None:
        """Apply styling to info labels."""
        label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-family: Georgia;
                font-size: 12px;
                font-weight: 500;
            }
        """)

    def update_progress(self, progress_info: ProgressInfo) -> None:
        """
        Update progress display with new information.

        Args:
            progress_info: Progress information to display
        """
        try:
            self._current_progress = progress_info

            if self._is_timer_mode:
                self._update_timer_mode_display(progress_info)
            else:
                self._update_question_mode_display(progress_info)

            logger.debug(
                f"Updated progress: {progress_info.current_question}/{progress_info.total_questions}"
            )

        except Exception as e:
            logger.exception(f"Failed to update progress: {e}")

    def _update_question_mode_display(self, progress_info: ProgressInfo) -> None:
        """Update display for question-based mode."""
        # Update progress bar
        if progress_info.total_questions > 0:
            progress_percentage = (
                progress_info.questions_answered / progress_info.total_questions
            ) * 100
            self.progress_bar.setValue(int(progress_percentage))

        # Update question counter
        self.question_label.setText(
            f"Question {progress_info.current_question} of {progress_info.total_questions}"
        )

        # Update accuracy
        self.accuracy_label.setText(
            f"Accuracy: {progress_info.accuracy_percentage:.0f}%"
        )

        # Update accuracy color based on percentage
        self._update_accuracy_color(progress_info.accuracy_percentage)

    def _update_timer_mode_display(self, progress_info: ProgressInfo) -> None:
        """Update display for timer-based mode."""
        # In timer mode, show questions answered instead of progress
        self.progress_bar.setValue(0)  # Timer handles its own progress

        # Update question counter to show answered count
        self.question_label.setText(
            f"Questions Answered: {progress_info.questions_answered}"
        )

        # Update accuracy
        self.accuracy_label.setText(
            f"Accuracy: {progress_info.accuracy_percentage:.0f}%"
        )

        # Update accuracy color
        self._update_accuracy_color(progress_info.accuracy_percentage)

    def _update_accuracy_color(self, accuracy: float) -> None:
        """Update accuracy label color based on percentage."""
        if accuracy >= 90:
            color = "rgba(0, 255, 0, 0.9)"  # Green
        elif accuracy >= 70:
            color = "rgba(255, 255, 0, 0.9)"  # Yellow
        elif accuracy >= 50:
            color = "rgba(255, 165, 0, 0.9)"  # Orange
        else:
            color = "rgba(255, 0, 0, 0.9)"  # Red

        self.accuracy_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-family: Georgia;
                font-size: 12px;
                font-weight: bold;
            }}
        """)

    def set_question_mode(self, total_questions: int) -> None:
        """Set progress display to question-based mode."""
        self._is_timer_mode = False
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        # Initialize display
        initial_progress = ProgressInfo(
            current_question=1,
            total_questions=total_questions,
            correct_answers=0,
            questions_answered=0,
            accuracy_percentage=0.0,
        )
        self.update_progress(initial_progress)

        logger.debug(f"Set question mode with {total_questions} questions")

    def set_timer_mode(self) -> None:
        """Set progress display to timer-based mode."""
        self._is_timer_mode = True
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        # Initialize display
        initial_progress = ProgressInfo(
            current_question=1,
            total_questions=0,  # Not relevant in timer mode
            correct_answers=0,
            questions_answered=0,
            accuracy_percentage=0.0,
        )
        self.update_progress(initial_progress)

        logger.debug("Set timer mode")

    def show_completion(self) -> None:
        """Show completion state."""
        if self._current_progress:
            if not self._is_timer_mode:
                self.progress_bar.setValue(100)

            self.question_label.setText("Lesson Complete!")

            # Show final accuracy with appropriate color
            final_accuracy = self._current_progress.accuracy_percentage
            self.accuracy_label.setText(f"Final Accuracy: {final_accuracy:.0f}%")
            self._update_accuracy_color(final_accuracy)

        logger.debug("Showing completion state")

    def reset(self) -> None:
        """Reset progress display to initial state."""
        self._current_progress = None
        self._is_timer_mode = False

        self.progress_bar.setValue(0)
        self.question_label.setText("Question 1 of 20")
        self.accuracy_label.setText("Accuracy: 0%")

        # Reset accuracy color
        self._apply_info_label_styling(self.accuracy_label)

        logger.debug("Progress controls reset")

    def update_responsive_styling(self, parent_width: int, parent_height: int) -> None:
        """Update styling based on parent widget size."""
        try:
            # Calculate responsive font size
            font_size = max(10, min(14, parent_width // 60))

            # Update label fonts
            for label in [self.question_label, self.accuracy_label]:
                current_style = label.styleSheet()
                # Replace font-size in current style
                import re

                new_style = re.sub(
                    r"font-size:\s*\d+px;", f"font-size: {font_size}px;", current_style
                )
                label.setStyleSheet(new_style)

            # Update progress bar height based on screen size
            bar_height = max(8, min(16, parent_height // 50))
            self.progress_bar.setFixedHeight(bar_height)

        except Exception as e:
            logger.exception(f"Failed to update responsive styling: {e}")

    def get_current_progress(self) -> ProgressInfo | None:
        """Get current progress information."""
        return self._current_progress

    def is_timer_mode(self) -> bool:
        """Check if in timer mode."""
        return self._is_timer_mode
