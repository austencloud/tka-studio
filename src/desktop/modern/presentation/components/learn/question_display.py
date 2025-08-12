"""
Question Display Component

Focused component for displaying quiz questions in different formats.
Handles pictographs, letters, and text with appropriate rendering.
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget

from desktop.modern.domain.models.learn import QuestionData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.components.pictograph.views import create_learn_view


logger = logging.getLogger(__name__)


class QuestionRenderer:
    """Base class for question renderers."""

    def render(self, question_content: Any, parent: QWidget) -> QWidget:
        """Render question content and return widget."""
        raise NotImplementedError


class PictographQuestionRenderer(QuestionRenderer):
    """Renderer for pictograph questions."""

    def render(self, question_content: Any, parent: QWidget) -> QWidget:
        """Render pictograph question."""
        try:
            # Extract PictographData from question content
            pictograph_data = self._extract_pictograph_data(question_content)

            if not pictograph_data:
                return self._create_error_widget("Invalid pictograph data", parent)

            # Create pictograph view
            pictograph_widget = create_learn_view(parent=parent, context="question")

            # Configure size policy and constraints for better visibility
            pictograph_widget.setSizePolicy(
                QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
            )
            pictograph_widget.setFixedSize(
                500, 500
            )  # Larger square container for better visibility

            # Render the pictograph
            pictograph_widget.update_from_pictograph_data(pictograph_data)

            logger.debug("Rendered pictograph question successfully")
            return pictograph_widget

        except Exception as e:
            logger.exception(f"Failed to render pictograph: {e}")
            return self._create_error_widget(f"Rendering error: {e}", parent)

    def _extract_pictograph_data(self, question_content: Any) -> PictographData | None:
        """Extract PictographData from question content."""
        if isinstance(question_content, dict) and "data" in question_content:
            return question_content["data"]
        if isinstance(question_content, PictographData):
            return question_content
        logger.warning(f"Unexpected pictograph data format: {type(question_content)}")
        return None

    def _create_error_widget(self, message: str, parent: QWidget) -> QWidget:
        """Create error display widget."""
        error_label = QLabel(message)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 0, 0, 0.8);
                font-family: Georgia;
                border: 2px solid rgba(255, 0, 0, 0.3);
                border-radius: 8px;
                padding: 20px;
                background-color: rgba(255, 0, 0, 0.1);
                min-width: 200px;
                min-height: 150px;
            }
        """
        )
        return error_label


class LetterQuestionRenderer(QuestionRenderer):
    """Renderer for letter questions."""

    def render(self, question_content: Any, parent: QWidget) -> QWidget:
        """Render letter question."""
        letter_label = QLabel(str(question_content))
        letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        letter_label.setStyleSheet(
            """
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
        """
        )
        return letter_label


class TextQuestionRenderer(QuestionRenderer):
    """Renderer for generic text questions."""

    def render(self, question_content: Any, parent: QWidget) -> QWidget:
        """Render text question."""
        text_label = QLabel(str(question_content))
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setWordWrap(True)
        text_label.setStyleSheet(
            """
            QLabel {
                color: white;
                font-family: Georgia;
                font-size: 18px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 20px;
                background-color: rgba(255, 255, 255, 0.1);
            }
        """
        )
        return text_label


class QuestionDisplay(QWidget):
    """
    Focused component for displaying quiz questions.

    Handles different question formats using appropriate renderers
    with clean separation of concerns.
    """

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.current_question: QuestionData | None = None
        self.current_format: str = ""
        self.content_widget: QWidget | None = None

        # Renderer registry
        self._renderers = {
            "pictograph": PictographQuestionRenderer(),
            "letter": LetterQuestionRenderer(),
            "text": TextQuestionRenderer(),
        }

        self._setup_ui()

        logger.debug("Question display component initialized")

    def _setup_ui(self) -> None:
        """Setup question display UI."""
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def show_question(self, question: QuestionData, format_type: str) -> None:
        """
        Display a question with the specified format.

        Args:
            question: Question data to display
            format_type: Format type ("pictograph", "letter", "text")
        """
        try:
            if not question:
                logger.warning("Cannot display empty question")
                return

            self.current_question = question
            self.current_format = format_type

            # Clear existing content
            self._clear_content()

            # Get appropriate renderer
            renderer = self._get_renderer(format_type)

            # Render question content
            self.content_widget = renderer.render(question.question_content, self)

            # Add to layout
            self.layout.addWidget(self.content_widget)

            # Ensure visibility
            self.setVisible(True)

            logger.debug(f"Displayed {format_type} question: {question.question_id}")

        except Exception as e:
            logger.exception(f"Failed to show question: {e}")
            self._show_error_message(f"Failed to display question: {e}")

    def _get_renderer(self, format_type: str) -> QuestionRenderer:
        """Get appropriate renderer for format type."""
        return self._renderers.get(format_type, self._renderers["text"])

    def _clear_content(self) -> None:
        """Clear existing question content."""
        if self.content_widget:
            self.layout.removeWidget(self.content_widget)
            self.content_widget.deleteLater()
            self.content_widget = None

    def _show_error_message(self, message: str) -> None:
        """Show error message in place of question."""
        error_renderer = TextQuestionRenderer()
        self.content_widget = error_renderer.render(message, self)
        self.layout.addWidget(self.content_widget)

    def update_responsive_styling(self, parent_width: int, parent_height: int) -> None:
        """Update styling based on parent widget size."""
        if not self.content_widget:
            return

        try:
            # Calculate responsive sizes
            display_size = min(parent_width // 3, parent_height // 3, 500)
            display_size = max(display_size, 200)  # Minimum size

            # Update content widget size if it's a pictograph
            if self.current_format == "pictograph":
                self.content_widget.setFixedSize(display_size, display_size)

            # Update font size for letter display
            elif self.current_format == "letter":
                font_size = max(24, min(72, parent_width // 15))
                font = self.content_widget.font()
                font.setPointSize(font_size)
                self.content_widget.setFont(font)

            # Update font size for text display
            elif self.current_format == "text":
                font_size = max(12, min(24, parent_width // 40))
                font = self.content_widget.font()
                font.setPointSize(font_size)
                self.content_widget.setFont(font)

        except Exception as e:
            logger.exception(f"Failed to update responsive styling: {e}")

    def get_current_format(self) -> str:
        """Get current display format."""
        return self.current_format
