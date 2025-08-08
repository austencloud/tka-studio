"""
Lesson Workspace View

Pure UI component for lesson workspace with dynamic layout support.
Handles only UI rendering and layout - no business logic.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from desktop.modern.presentation.controllers.learn.state import LayoutMode


logger = logging.getLogger(__name__)


class LessonWorkspaceView(QWidget):
    """
    Pure UI component for lesson workspace.

    Provides dynamic layout switching and component hosting.
    Emits events for user interactions - no business logic.
    """

    # Events emitted to controllers
    back_requested = pyqtSignal()
    pause_requested = pyqtSignal()
    restart_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        # Set object name for test compatibility
        self.setObjectName("lesson_widget")

        # Layout state
        self._current_layout_mode: LayoutMode | None = None

        # Component placeholders (will be set by controller)
        self.question_display: QWidget | None = None
        self.answer_options: QWidget | None = None
        self.progress_controls: QWidget | None = None
        self.lesson_timer: QWidget | None = None
        self.lesson_controls: QWidget | None = None

        self._setup_ui()

        logger.debug("Lesson workspace view initialized")

    def _setup_ui(self) -> None:
        """Setup workspace UI structure."""
        # Main vertical layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # Controls container (top)
        self.controls_container = QWidget()
        self.controls_layout = QHBoxLayout(self.controls_container)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)

        # Back button
        self.back_button = QPushButton("← Back")
        self.back_button.setObjectName("back_button")
        self.back_button.clicked.connect(self.back_requested.emit)
        self.back_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4a5568;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2d3748;
            }
        """
        )
        self.controls_layout.addWidget(self.back_button)
        self.controls_layout.addStretch()  # Push back button to left

        self.main_layout.addWidget(self.controls_container)

        # Question prompt label
        self.question_prompt = QLabel()
        self.question_prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._apply_question_prompt_styling()
        self.main_layout.addWidget(self.question_prompt)

        # Content container (dynamic layout)
        self.content_container = QWidget()
        self.main_layout.addWidget(self.content_container)

        # Bottom container for progress and timer
        self.bottom_container = QWidget()
        self.bottom_layout = QVBoxLayout(self.bottom_container)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.bottom_container)

        # Set initial layout mode
        self.set_layout_mode(LayoutMode.VERTICAL)

    def _apply_question_prompt_styling(self) -> None:
        """Apply styling to question prompt."""
        self.question_prompt.setStyleSheet(
            """
            QLabel {
                color: white;
                font-family: Georgia;
                font-weight: bold;
                font-size: 16px;
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 12px 20px;
                margin: 10px;
            }
        """
        )

    def set_layout_mode(self, mode: LayoutMode) -> None:
        """Set layout mode for content area."""
        if self._current_layout_mode == mode:
            return

        self._current_layout_mode = mode

        # Clear existing layout
        if self.content_container.layout():
            self._clear_content_layout()

        # Create new layout based on mode
        if mode == LayoutMode.VERTICAL:
            self._setup_vertical_layout()
        elif mode == LayoutMode.HORIZONTAL:
            self._setup_horizontal_layout()

        logger.debug(f"Set layout mode to {mode.value}")

    def _setup_vertical_layout(self) -> None:
        """Setup vertical layout (question top, answers bottom)."""
        layout = QVBoxLayout(self.content_container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Add components if they exist
        if self.question_display:
            layout.addWidget(self.question_display)
        if self.answer_options:
            layout.addWidget(self.answer_options)

    def _setup_horizontal_layout(self) -> None:
        """Setup horizontal layout (question left, answers right)."""
        layout = QHBoxLayout(self.content_container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        # Add components if they exist
        if self.question_display:
            layout.addWidget(self.question_display, 2)  # 40% width
        if self.answer_options:
            layout.addWidget(self.answer_options, 3)  # 60% width

    def _clear_content_layout(self) -> None:
        """Clear existing content layout."""
        layout = self.content_container.layout()
        if layout:
            # Remove widgets from layout but don't delete them
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().setParent(None)

            # Delete the layout
            layout.deleteLater()

    def set_question_display(self, widget: QWidget) -> None:
        """Set the question display component."""
        if self.question_display:
            self.question_display.setParent(None)

        self.question_display = widget
        widget.setParent(self.content_container)

        # Re-setup layout to include new component
        self.set_layout_mode(self._current_layout_mode)

    def set_answer_options(self, widget: QWidget) -> None:
        """Set the answer options component."""
        if self.answer_options:
            self.answer_options.setParent(None)

        self.answer_options = widget
        widget.setParent(self.content_container)

        # Re-setup layout to include new component
        self.set_layout_mode(self._current_layout_mode)

    def set_lesson_controls(self, widget: QWidget) -> None:
        """Set the lesson controls component."""
        if self.lesson_controls:
            self.lesson_controls.setParent(None)

        self.lesson_controls = widget
        self.controls_layout.addWidget(widget)

    def set_progress_controls(self, widget: QWidget) -> None:
        """Set the progress controls component."""
        if self.progress_controls:
            self.progress_controls.setParent(None)

        self.progress_controls = widget
        self.bottom_layout.addWidget(widget)

    def set_lesson_timer(self, widget: QWidget) -> None:
        """Set the lesson timer component."""
        if self.lesson_timer:
            self.lesson_timer.setParent(None)

        self.lesson_timer = widget
        self.bottom_layout.addWidget(widget)

    # Public interface for external state updates
    def set_question_prompt(self, text: str) -> None:
        """Set question prompt text."""
        self.question_prompt.setText(text)

    def show_feedback(self, message: str, feedback_type: str = "info") -> None:
        """Show feedback message with styling."""
        self.question_prompt.setText(message)

        # Apply feedback styling
        if feedback_type == "success":
            color = "rgba(0, 255, 0, 0.3)"
            border_color = "rgba(0, 255, 0, 0.5)"
        elif feedback_type == "error":
            color = "rgba(255, 0, 0, 0.3)"
            border_color = "rgba(255, 0, 0, 0.5)"
        elif feedback_type == "warning":
            color = "rgba(255, 255, 0, 0.3)"
            border_color = "rgba(255, 255, 0, 0.5)"
        else:
            color = "rgba(255, 255, 255, 0.1)"
            border_color = "rgba(255, 255, 255, 0.2)"

        self.question_prompt.setStyleSheet(
            f"""
            QLabel {{
                color: white;
                font-family: Georgia;
                font-weight: bold;
                font-size: 16px;
                background-color: {color};
                border: 2px solid {border_color};
                border-radius: 8px;
                padding: 12px 20px;
                margin: 10px;
            }}
        """
        )

    def clear_feedback(self) -> None:
        """Clear feedback and restore normal styling."""
        self._apply_question_prompt_styling()

    def set_loading_state(self, is_loading: bool) -> None:
        """Set loading state for the workspace."""
        # Disable/enable all interactive components
        if self.question_display:
            self.question_display.setEnabled(not is_loading)
        if self.answer_options:
            self.answer_options.setEnabled(not is_loading)
        if self.lesson_controls:
            self.lesson_controls.setEnabled(not is_loading)

    def update_responsive_styling(self, parent_width: int, parent_height: int) -> None:
        """Update styling based on parent size."""
        # Calculate responsive font size for question prompt
        prompt_font_size = max(12, min(20, parent_width // 40))

        # Update question prompt styling
        current_style = self.question_prompt.styleSheet()
        # Replace font-size in current style
        import re

        new_style = re.sub(
            r"font-size:\s*\d+px;", f"font-size: {prompt_font_size}px;", current_style
        )
        self.question_prompt.setStyleSheet(new_style)

        # Update component spacing based on size
        if parent_width < 800:
            self.main_layout.setSpacing(5)
            self.main_layout.setContentsMargins(5, 5, 5, 5)
        else:
            self.main_layout.setSpacing(10)
            self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Update content layout spacing
        if self.content_container.layout():
            if self._current_layout_mode == LayoutMode.HORIZONTAL:
                spacing = max(15, min(40, parent_width // 25))
            else:
                spacing = max(10, min(30, parent_height // 25))
            self.content_container.layout().setSpacing(spacing)
