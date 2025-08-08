"""
Answer Options Component

Focused component for displaying answer options in different formats.
Handles buttons, pictographs, and other option types with clean interfaces.
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QGridLayout, QPushButton, QVBoxLayout, QWidget

from desktop.modern.domain.models.learn import QuestionData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.components.pictograph.views import create_learn_view


logger = logging.getLogger(__name__)


class AnswerOptionFactory:
    """Factory for creating answer option widgets."""

    @staticmethod
    def create_button_option(option: Any, parent: QWidget) -> QPushButton:
        """Create button-style answer option."""
        button = QPushButton(str(option))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(70, 130, 180, 0.8);
                border: 2px solid rgba(70, 130, 180, 1.0);
                border-radius: 12px;
                color: white;
                font-family: Georgia;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 30px;
                min-width: 150px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: rgba(100, 149, 237, 0.9);
                border: 2px solid rgba(100, 149, 237, 1.0);
            }
            QPushButton:pressed {
                background-color: rgba(65, 105, 225, 1.0);
                border: 2px solid rgba(65, 105, 225, 1.0);
            }
            QPushButton:disabled {
                background-color: rgba(255, 0, 0, 0.2);
                border: 2px solid rgba(255, 0, 0, 0.3);
                color: rgba(255, 255, 255, 0.5);
            }
        """
        )
        return button

    @staticmethod
    def create_pictograph_option(option: Any, parent: QWidget) -> QWidget:
        """Create pictograph-style answer option."""
        try:
            # Extract pictograph data
            pictograph_data = None
            if isinstance(option, dict) and "data" in option:
                pictograph_data = option["data"]
            elif isinstance(option, PictographData):
                pictograph_data = option

            if not pictograph_data:
                # Fallback to button if pictograph data is invalid
                return AnswerOptionFactory.create_button_option(str(option), parent)

            # Create pictograph widget
            pictograph_widget = create_learn_view(
                parent=parent, context="answer_option"
            )

            # Configure size and properties for better visibility
            pictograph_widget.setFixedSize(200, 200)  # Larger for better visibility
            pictograph_widget.setCursor(Qt.CursorShape.PointingHandCursor)

            # Add hover styling
            pictograph_widget.setStyleSheet(
                """
                QWidget {
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 8px;
                    background-color: rgba(255, 255, 255, 0.1);
                }
                QWidget:hover {
                    border: 2px solid rgba(255, 255, 255, 0.5);
                    background-color: rgba(255, 255, 255, 0.2);
                }
            """
            )

            # Render pictograph
            pictograph_widget.update_from_pictograph_data(pictograph_data)

            return pictograph_widget

        except Exception as e:
            logger.error(f"Failed to create pictograph option: {e}")
            # Fallback to button
            return AnswerOptionFactory.create_button_option(str(option), parent)


class AnswerLayoutManager:
    """Manages layout of answer options."""

    @staticmethod
    def arrange_options(
        widgets: list[QWidget], container: QWidget, format_type: str
    ) -> None:
        """Arrange option widgets in appropriate layout."""
        # Clear existing layout
        if container.layout():
            AnswerLayoutManager._clear_layout(container.layout())
            # Delete the old layout
            old_layout = container.layout()
            if old_layout:
                old_layout.setParent(None)

        if format_type == "pictograph":
            AnswerLayoutManager._arrange_pictograph_grid(widgets, container)
        else:
            AnswerLayoutManager._arrange_button_list(widgets, container)

    @staticmethod
    def _arrange_button_list(widgets: list[QWidget], container: QWidget) -> None:
        """Arrange buttons in vertical list."""
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        for widget in widgets:
            layout.addWidget(widget)

    @staticmethod
    def _arrange_pictograph_grid(widgets: list[QWidget], container: QWidget) -> None:
        """Arrange pictographs in grid layout."""
        layout = QGridLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        # Arrange in 2x2 grid for up to 4 options
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

        for i, widget in enumerate(widgets):
            if i < len(positions):
                row, col = positions[i]
                layout.addWidget(widget, row, col)

    @staticmethod
    def _clear_layout(layout) -> None:
        """Clear all widgets from layout."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class AnswerOptions(QWidget):
    """
    Focused component for displaying answer options.

    Handles different option formats with appropriate layouts
    and provides clean event interfaces.
    """

    # Signals
    answer_selected = pyqtSignal(object)  # Selected answer

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.current_question: QuestionData | None = None
        self.current_format: str = ""
        self.option_widgets: list[QWidget] = []
        self.option_to_widget: dict[Any, QWidget] = {}

        self._setup_ui()

        logger.debug("Answer options component initialized")

    def _setup_ui(self) -> None:
        """Setup answer options UI."""
        # Main layout will be set dynamically based on format
        self.setContentsMargins(0, 0, 0, 0)

    def show_options(self, question: QuestionData, format_type: str) -> None:
        """
        Display answer options for a question.

        Args:
            question: Question with answer options
            format_type: Format type ("button", "pictograph")
        """
        try:
            if not question or not question.answer_options:
                logger.warning("Cannot display options for invalid question")
                return

            self.current_question = question
            self.current_format = format_type

            # Clear existing options
            self._clear_options()

            # Create option widgets
            self._create_option_widgets(question.answer_options, format_type)

            # Arrange in appropriate layout
            AnswerLayoutManager.arrange_options(self.option_widgets, self, format_type)

            # Connect signals
            self._connect_option_signals()

            logger.debug(
                f"Displayed {len(question.answer_options)} {format_type} options"
            )

        except Exception as e:
            logger.error(f"Failed to show options: {e}")
            self._show_error_message(f"Failed to display options: {e}")

    def _create_option_widgets(self, options: list[Any], format_type: str) -> None:
        """Create widgets for answer options."""
        self.option_widgets = []
        self.option_to_widget = {}

        for i, option in enumerate(options):
            if format_type == "pictograph":
                widget = AnswerOptionFactory.create_pictograph_option(option, self)
            else:
                widget = AnswerOptionFactory.create_button_option(option, self)

            self.option_widgets.append(widget)
            # Use index as key since options might be unhashable dicts
            self.option_to_widget[i] = widget

    def _connect_option_signals(self) -> None:
        """Connect option widget signals."""
        for i, widget in enumerate(self.option_widgets):
            option = self.current_question.answer_options[i]

            if isinstance(widget, QPushButton):
                widget.clicked.connect(
                    lambda checked, opt=option: self.answer_selected.emit(opt)
                )
            else:
                # For pictograph widgets, we need to handle mouse events
                widget.mousePressEvent = (
                    lambda event, opt=option: self.answer_selected.emit(opt)
                )

    def _clear_options(self) -> None:
        """Clear existing option widgets."""
        if self.layout():
            AnswerLayoutManager._clear_layout(self.layout())
            self.layout().deleteLater()

        self.option_widgets.clear()
        self.option_to_widget.clear()

    def _show_error_message(self, message: str) -> None:
        """Show error message in place of options."""
        layout = QVBoxLayout(self)
        error_label = QPushButton(message)
        error_label.setEnabled(False)
        error_label.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255, 0, 0, 0.2);
                border: 2px solid rgba(255, 0, 0, 0.3);
                color: rgba(255, 255, 255, 0.8);
                font-family: Georgia;
                padding: 20px;
            }
        """
        )
        layout.addWidget(error_label)

    def show_placeholder(
        self, message: str = "Select a question to see answer options"
    ) -> None:
        """Show placeholder message."""
        layout = QVBoxLayout(self)
        placeholder_label = QPushButton(message)
        placeholder_label.setEnabled(False)
        placeholder_label.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px dashed rgba(255, 255, 255, 0.3);
                color: rgba(255, 255, 255, 0.6);
                font-family: Georgia;
                font-style: italic;
                padding: 30px;
            }
        """
        )
        layout.addWidget(placeholder_label)

    def update_responsive_styling(self, parent_width: int, parent_height: int) -> None:
        """Update styling based on parent widget size."""
        if not self.option_widgets:
            return

        try:
            if self.current_format == "pictograph":
                # Update pictograph sizes
                size = max(100, min(200, parent_width // 6))
                for widget in self.option_widgets:
                    widget.setFixedSize(size, size)

            else:
                # Update button sizes and fonts
                button_width = max(100, min(200, parent_width // 5))
                button_height = max(35, min(60, parent_height // 15))
                font_size = max(10, min(16, parent_width // 60))

                for widget in self.option_widgets:
                    if isinstance(widget, QPushButton):
                        widget.setMinimumSize(button_width, button_height)
                        font = widget.font()
                        font.setPointSize(font_size)
                        widget.setFont(font)

        except Exception as e:
            logger.error(f"Failed to update responsive styling: {e}")
