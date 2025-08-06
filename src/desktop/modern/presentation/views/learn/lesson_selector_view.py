"""
Lesson Selector View

Pure UI component for lesson selection with no business logic.
Emits events for user interactions and updates UI based on external state.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from desktop.modern.domain.models.learn import LessonType, QuizMode


logger = logging.getLogger(__name__)


class LessonModeToggle(QWidget):
    """Pure UI component for quiz mode selection."""

    mode_changed = pyqtSignal(str)  # QuizMode.value

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup mode toggle UI."""
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        # Container for toggle group
        self.toggle_container = QWidget()
        toggle_layout = QHBoxLayout(self.toggle_container)
        toggle_layout.setContentsMargins(4, 4, 4, 4)
        toggle_layout.setSpacing(0)

        # Create toggle buttons
        self.fixed_question_btn = QPushButton("Fixed Questions")
        self.countdown_btn = QPushButton("Countdown")

        # Set button properties
        self.fixed_question_btn.setCheckable(True)
        self.countdown_btn.setCheckable(True)
        self.fixed_question_btn.setChecked(True)  # Default selection

        # Set fixed sizes
        button_width = 120
        button_height = 36
        self.fixed_question_btn.setFixedSize(button_width, button_height)
        self.countdown_btn.setFixedSize(button_width, button_height)

        # Add to layout
        toggle_layout.addWidget(self.fixed_question_btn)
        toggle_layout.addWidget(self.countdown_btn)

        # Apply styling
        self._apply_styling()

        layout.addWidget(self.toggle_container)

    def _apply_styling(self) -> None:
        """Apply styling to toggle components."""
        container_style = """
            QWidget {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
            }
        """

        button_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                color: rgba(255, 255, 255, 0.8);
                font-family: Georgia;
                font-size: 12px;
                font-weight: 500;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.9);
            }
            QPushButton:checked {
                background-color: rgba(62, 99, 221, 0.8);
                color: white;
                font-weight: bold;
            }
            QPushButton:checked:hover {
                background-color: rgba(62, 99, 221, 0.9);
            }
        """

        self.toggle_container.setStyleSheet(container_style)
        self.fixed_question_btn.setStyleSheet(button_style)
        self.countdown_btn.setStyleSheet(button_style)

    def _connect_signals(self) -> None:
        """Connect button signals."""
        self.fixed_question_btn.clicked.connect(self._on_fixed_question_clicked)
        self.countdown_btn.clicked.connect(self._on_countdown_clicked)

    def _on_fixed_question_clicked(self) -> None:
        """Handle fixed question button click."""
        self.fixed_question_btn.setChecked(True)
        self.countdown_btn.setChecked(False)
        self.mode_changed.emit(QuizMode.FIXED_QUESTION.value)

    def _on_countdown_clicked(self) -> None:
        """Handle countdown button click."""
        self.countdown_btn.setChecked(True)
        self.fixed_question_btn.setChecked(False)
        self.mode_changed.emit(QuizMode.COUNTDOWN.value)

    def get_selected_mode(self) -> QuizMode:
        """Get currently selected mode."""
        return (
            QuizMode.FIXED_QUESTION
            if self.fixed_question_btn.isChecked()
            else QuizMode.COUNTDOWN
        )

    def set_selected_mode(self, mode: QuizMode) -> None:
        """Set selected mode."""
        if mode == QuizMode.FIXED_QUESTION:
            self.fixed_question_btn.setChecked(True)
            self.countdown_btn.setChecked(False)
        else:
            self.countdown_btn.setChecked(True)
            self.fixed_question_btn.setChecked(False)


class LessonButton(QPushButton):
    """Styled lesson selection button."""

    def __init__(
        self, text: str, lesson_type: LessonType, parent: QWidget | None = None
    ):
        super().__init__(text, parent)
        self.lesson_type = lesson_type
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._setup_styling()

    def _setup_styling(self) -> None:
        """Setup button styling."""
        self.setStyleSheet(
            """
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
        """
        )


class LessonSelectorView(QWidget):
    """
    Pure UI component for lesson selection.

    Handles only UI rendering and event emission - no business logic.
    """

    # Events emitted to controllers
    lesson_requested = pyqtSignal(object, object)  # LessonType, QuizMode

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        # Set object name for test compatibility
        self.setObjectName("lesson_selector")

        # UI components
        self.lesson_buttons: dict[LessonType, LessonButton] = {}
        self.description_labels: dict[LessonType, QLabel] = {}

        self._setup_ui()
        self._connect_signals()

        logger.debug("Lesson selector view initialized")

    def _setup_ui(self) -> None:
        """Setup the lesson selector UI."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        self.title_label = QLabel("Select a Lesson:")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._apply_title_styling()

        # Mode toggle
        self.mode_toggle = LessonModeToggle(self)

        # Add to layout
        layout.addStretch(2)
        layout.addWidget(self.title_label)
        layout.addStretch(1)
        layout.addWidget(self.mode_toggle)
        layout.addStretch(1)

        # Create lesson buttons
        self._create_lesson_buttons(layout)

        layout.addStretch(2)

    def _apply_title_styling(self) -> None:
        """Apply styling to title label."""
        self.title_label.setStyleSheet(
            """
            QLabel {
                color: white;
                font-family: Georgia;
                font-weight: bold;
                font-size: 24px;
            }
        """
        )

    def _create_lesson_buttons(self, layout: QVBoxLayout) -> None:
        """Create lesson selection buttons."""
        # Lesson information
        lesson_info = [
            (
                "Lesson 1",
                "Match the correct letter to the given pictograph",
                LessonType.PICTOGRAPH_TO_LETTER,
            ),
            (
                "Lesson 2",
                "Identify the correct pictograph for the displayed letter",
                LessonType.LETTER_TO_PICTOGRAPH,
            ),
            (
                "Lesson 3",
                "Choose the pictograph that logically follows",
                LessonType.VALID_NEXT_PICTOGRAPH,
            ),
        ]

        for lesson_name, description, lesson_type in lesson_info:
            self._add_lesson_button(layout, lesson_name, description, lesson_type)

    def _add_lesson_button(
        self,
        layout: QVBoxLayout,
        button_text: str,
        description_text: str,
        lesson_type: LessonType,
    ) -> None:
        """Create and add a lesson button with description."""
        # Create vertical layout for button + description
        lesson_layout = QVBoxLayout()
        lesson_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create button
        button = LessonButton(button_text, lesson_type, self)
        button.setToolTip(description_text)
        self.lesson_buttons[lesson_type] = button

        # Create description label
        description_label = QLabel(description_text)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-family: Georgia;
                font-size: 12px;
            }
        """
        )
        self.description_labels[lesson_type] = description_label

        # Add to layout
        lesson_layout.addWidget(button)
        lesson_layout.addWidget(description_label)

        layout.addLayout(lesson_layout)
        layout.addStretch(1)

    def _connect_signals(self) -> None:
        """Connect UI signals."""
        # Connect lesson buttons
        for lesson_type, button in self.lesson_buttons.items():
            button.clicked.connect(
                lambda checked, lt=lesson_type: self._on_lesson_clicked(lt)
            )

    def _on_lesson_clicked(self, lesson_type: LessonType) -> None:
        """Handle lesson button click."""
        selected_mode = self.mode_toggle.get_selected_mode()
        self.lesson_requested.emit(lesson_type, selected_mode)

    # Public interface for external state updates
    def update_lesson_availability(self, available_lessons: list[LessonType]) -> None:
        """Update which lessons are available."""
        for lesson_type, button in self.lesson_buttons.items():
            button.setEnabled(lesson_type in available_lessons)

    def set_loading_state(self, is_loading: bool) -> None:
        """Set loading state."""
        for button in self.lesson_buttons.values():
            button.setEnabled(not is_loading)
        self.mode_toggle.setEnabled(not is_loading)

    def set_selected_mode(self, mode: QuizMode) -> None:
        """Set the selected quiz mode."""
        self.mode_toggle.set_selected_mode(mode)

    def update_responsive_styling(self, parent_width: int, parent_height: int) -> None:
        """Update styling based on parent size."""
        # Calculate responsive font sizes
        title_font_size = max(16, min(32, parent_width // 25))
        button_font_size = max(12, min(18, parent_width // 40))
        description_font_size = max(10, min(14, parent_width // 50))

        # Update title font
        self.title_label.setStyleSheet(
            f"""
            QLabel {{
                color: white;
                font-family: Georgia;
                font-weight: bold;
                font-size: {title_font_size}px;
            }}
        """
        )

        # Update button sizes
        button_width = max(150, min(250, parent_width // 4))
        button_height = max(40, min(60, parent_height // 12))

        for button in self.lesson_buttons.values():
            button.setFixedSize(button_width, button_height)
            font = button.font()
            font.setPointSize(button_font_size)
            button.setFont(font)

        # Update description fonts
        for label in self.description_labels.values():
            font = label.font()
            font.setPointSize(description_font_size)
            label.setFont(font)
