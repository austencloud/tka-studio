"""
Lesson Results View

Pure UI component for displaying lesson completion results.
Handles only UI rendering and event emission - no business logic.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.domain.models.learn import LessonResults


logger = logging.getLogger(__name__)


class ResultsStatsWidget(QWidget):
    """Widget for displaying lesson statistics."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup statistics display."""
        self.layout = QGridLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(15)

        # Create stat labels (will be populated later)
        self.stat_labels = {}

        # Apply container styling
        self.setStyleSheet(
            """
            QWidget {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 20px;
            }
        """
        )

    def add_stat(
        self, row: int, col: int, label: str, value: str, value_color: str = "white"
    ) -> None:
        """Add a statistic to the grid."""
        # Create label
        stat_label = QLabel(label)
        stat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stat_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-family: Georgia;
                font-size: 12px;
                font-weight: normal;
            }
        """
        )

        # Create value
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(
            f"""
            QLabel {{
                color: {value_color};
                font-family: Georgia;
                font-size: 18px;
                font-weight: bold;
            }}
        """
        )

        # Add to grid
        self.layout.addWidget(stat_label, row * 2, col)
        self.layout.addWidget(value_label, row * 2 + 1, col)

        # Store references
        self.stat_labels[label] = (stat_label, value_label)


class LessonResultsView(QWidget):
    """
    Pure UI component for lesson results display.

    Shows comprehensive results and provides navigation options.
    Emits events for user interactions - no business logic.
    """

    # Events emitted to controllers
    restart_lesson_requested = pyqtSignal(object)  # LessonType
    back_to_selector_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        # Set object name for test compatibility
        self.setObjectName("results_panel")

        self._current_results: LessonResults | None = None

        self._setup_ui()
        self._connect_signals()

        logger.debug("Lesson results view initialized")

    def _setup_ui(self) -> None:
        """Setup results display UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title
        self.title_label = QLabel("Lesson Complete!")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._apply_title_styling()

        # Performance summary
        self.performance_label = QLabel()
        self.performance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._apply_performance_styling()

        # Statistics container
        self.stats_widget = ResultsStatsWidget(self)

        # Action buttons container
        self.buttons_container = QWidget()
        self._setup_action_buttons()

        # Add to main layout
        main_layout.addStretch(1)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.performance_label)
        main_layout.addStretch(1)
        main_layout.addWidget(self.stats_widget)
        main_layout.addStretch(1)
        main_layout.addWidget(self.buttons_container)
        main_layout.addStretch(1)

    def _apply_title_styling(self) -> None:
        """Apply styling to title label."""
        self.title_label.setStyleSheet(
            """
            QLabel {
                color: white;
                font-family: Georgia;
                font-weight: bold;
                font-size: 28px;
                background-color: rgba(0, 255, 0, 0.2);
                border: 2px solid rgba(0, 255, 0, 0.4);
                border-radius: 12px;
                padding: 15px 30px;
            }
        """
        )

    def _apply_performance_styling(self) -> None:
        """Apply styling to performance label."""
        self.performance_label.setStyleSheet(
            """
            QLabel {
                color: white;
                font-family: Georgia;
                font-weight: bold;
                font-size: 20px;
                padding: 10px;
            }
        """
        )

    def _setup_action_buttons(self) -> None:
        """Setup action buttons."""
        layout = QHBoxLayout(self.buttons_container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Restart lesson button
        self.restart_button = QPushButton("Restart Lesson")
        self.restart_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.restart_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(62, 99, 221, 0.8);
                border: 2px solid rgba(62, 99, 221, 1.0);
                border-radius: 12px;
                color: white;
                font-family: Georgia;
                font-weight: bold;
                font-size: 14px;
                padding: 12px 24px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: rgba(62, 99, 221, 1.0);
                border: 2px solid rgba(82, 119, 241, 1.0);
            }
            QPushButton:pressed {
                background-color: rgba(42, 79, 201, 1.0);
            }
        """
        )

        # Back to selector button
        self.back_button = QPushButton("Choose Another Lesson")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                color: white;
                font-family: Georgia;
                font-weight: bold;
                font-size: 14px;
                padding: 12px 24px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.4);
            }
        """
        )

        layout.addWidget(self.restart_button)
        layout.addWidget(self.back_button)

    def _connect_signals(self) -> None:
        """Connect button signals."""
        self.restart_button.clicked.connect(self._on_restart_clicked)
        self.back_button.clicked.connect(self.back_to_selector_requested.emit)

    def _on_restart_clicked(self) -> None:
        """Handle restart button click."""
        if self._current_results:
            self.restart_lesson_requested.emit(self._current_results.lesson_type)

    # Public interface for external state updates
    def display_results(self, results: LessonResults) -> None:
        """Display lesson results."""
        self._current_results = results

        # Update performance summary
        grade = results.grade_letter
        performance = results.performance_level
        self.performance_label.setText(f"Grade: {grade} - {performance}")

        # Update performance label color based on grade
        if grade in ["A", "A+"]:
            color = "rgba(0, 255, 0, 1.0)"  # Green
        elif grade in ["B", "B+"]:
            color = "rgba(255, 255, 0, 1.0)"  # Yellow
        elif grade in ["C", "C+"]:
            color = "rgba(255, 165, 0, 1.0)"  # Orange
        else:
            color = "rgba(255, 0, 0, 1.0)"  # Red

        current_style = self.performance_label.styleSheet()
        import re

        new_style = re.sub(r"color:\s*[^;]+;", f"color: {color};", current_style)
        self.performance_label.setStyleSheet(new_style)

        # Clear existing stats
        self.stats_widget = ResultsStatsWidget(self)
        # Replace in layout
        main_layout = self.layout()
        main_layout.replaceWidget(main_layout.itemAt(3).widget(), self.stats_widget)

        # Add statistics
        self._populate_statistics(results)

    def _populate_statistics(self, results: LessonResults) -> None:
        """Populate statistics display."""
        # Row 0: Accuracy and Questions
        self.stats_widget.add_stat(
            0, 0, "Accuracy", f"{results.accuracy_percentage:.1f}%"
        )
        self.stats_widget.add_stat(
            0,
            1,
            "Questions Answered",
            f"{results.questions_answered}/{results.total_questions}",
        )

        # Row 1: Correct and Incorrect
        self.stats_widget.add_stat(
            1,
            0,
            "Correct Answers",
            str(results.correct_answers),
            "rgba(0, 255, 0, 1.0)",
        )
        self.stats_widget.add_stat(
            1,
            1,
            "Incorrect Attempts",
            str(results.incorrect_guesses),
            "rgba(255, 0, 0, 1.0)",
        )

        # Row 2: Time and Performance
        time_text = f"{results.completion_time_seconds:.1f}s"
        self.stats_widget.add_stat(2, 0, "Completion Time", time_text)

        if results.average_time_per_question:
            avg_time_text = f"{results.average_time_per_question:.1f}s"
            self.stats_widget.add_stat(2, 1, "Avg Time/Question", avg_time_text)

    def set_loading_state(self, is_loading: bool) -> None:
        """Set loading state."""
        self.restart_button.setEnabled(not is_loading)
        self.back_button.setEnabled(not is_loading)

    def update_responsive_styling(self, parent_width: int, parent_height: int) -> None:
        """Update styling based on parent size."""
        # Calculate responsive font sizes
        title_font_size = max(20, min(36, parent_width // 20))
        performance_font_size = max(16, min(24, parent_width // 30))
        button_font_size = max(12, min(16, parent_width // 50))

        # Update title font
        current_style = self.title_label.styleSheet()
        import re

        new_style = re.sub(
            r"font-size:\s*\d+px;", f"font-size: {title_font_size}px;", current_style
        )
        self.title_label.setStyleSheet(new_style)

        # Update performance font
        current_style = self.performance_label.styleSheet()
        new_style = re.sub(
            r"font-size:\s*\d+px;",
            f"font-size: {performance_font_size}px;",
            current_style,
        )
        self.performance_label.setStyleSheet(new_style)

        # Update button fonts
        for button in [self.restart_button, self.back_button]:
            font = button.font()
            font.setPointSize(button_font_size)
            button.setFont(font)
