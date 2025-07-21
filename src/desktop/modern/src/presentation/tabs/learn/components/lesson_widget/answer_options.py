"""
Answer Options Component

Displays answer options in different formats (buttons, pictographs)
and handles user selection with proper feedback.
"""

import logging
from typing import Optional, List, Any, Dict

from PyQt6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

from core.interfaces.learn_services import ILearnUIService
from domain.models.learn import QuestionData

logger = logging.getLogger(__name__)


class AnswerOptions(QWidget):
    """
    Component for displaying and managing answer options.

    Supports different answer formats including buttons and pictographs
    with selection handling and visual feedback.
    """

    # Signals
    answer_selected = pyqtSignal(object)  # selected answer

    def __init__(self, ui_service: ILearnUIService, parent: Optional[QWidget] = None):
        """
        Initialize answer options component.

        Args:
            ui_service: Service for UI calculations
            parent: Parent widget
        """
        super().__init__(parent)

        self.ui_service = ui_service
        self.current_question: Optional[QuestionData] = None
        self.current_format: str = ""
        self.answer_widgets: Dict[Any, QWidget] = {}

        self._setup_ui()

        logger.debug("Answer options component initialized")

    def _setup_ui(self) -> None:
        """Setup answer options UI."""
        try:
            # Use grid layout to accommodate different arrangements
            self.layout = QGridLayout(self)
            self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Placeholder label
            self.placeholder_label = QPushButton("Answer options will appear here")
            self.placeholder_label.setEnabled(False)
            self.placeholder_label.setStyleSheet(
                """
                QPushButton {
                    color: rgba(255, 255, 255, 0.6);
                    font-family: Georgia;
                    font-style: italic;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 8px;
                    background-color: rgba(255, 255, 255, 0.05);
                    padding: 10px;
                }
            """
            )

            self.layout.addWidget(self.placeholder_label, 0, 0)

        except Exception as e:
            logger.error(f"Failed to setup answer options UI: {e}")

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

            # Display based on format
            if format_type == "button":
                self._display_button_options(
                    question.answer_options, question.correct_answer
                )
            elif format_type == "pictograph":
                self._display_pictograph_options(
                    question.answer_options, question.correct_answer
                )
            else:
                logger.warning(f"Unknown answer format: {format_type}")
                self._display_button_options(
                    question.answer_options, question.correct_answer
                )

            logger.debug(
                f"Displayed {len(question.answer_options)} {format_type} options"
            )

        except Exception as e:
            logger.error(f"Failed to show answer options: {e}")

    def _display_button_options(self, options: List[Any], correct_answer: Any) -> None:
        """
        Display answer options as buttons.

        Args:
            options: List of answer options
            correct_answer: The correct answer
        """
        try:
            # Use horizontal layout for buttons
            button_layout = QHBoxLayout()
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            for i, option in enumerate(options):
                button = self._create_answer_button(option, correct_answer)
                button_layout.addWidget(button)
                self.answer_widgets[option] = button

            # Add layout to main grid
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
            self.layout.addWidget(button_widget, 0, 0)

        except Exception as e:
            logger.error(f"Failed to display button options: {e}")

    def _display_pictograph_options(
        self, options: List[Any], correct_answer: Any
    ) -> None:
        """
        Display answer options as pictographs.

        Args:
            options: List of pictograph options
            correct_answer: The correct pictograph
        """
        try:
            # Use 2x2 grid for pictographs
            columns = 2

            for i, option in enumerate(options):
                row = i // columns
                col = i % columns

                pictograph_widget = self._create_pictograph_option(
                    option, correct_answer
                )
                self.layout.addWidget(pictograph_widget, row, col)

                # Use option ID as key instead of the dict itself (which is not hashable)
                option_id = (
                    option.get("id", f"option_{i}")
                    if isinstance(option, dict)
                    else str(option)
                )
                self.answer_widgets[option_id] = pictograph_widget

        except Exception as e:
            logger.error(f"Failed to display pictograph options: {e}")

    def _create_answer_button(self, option: Any, correct_answer: Any) -> QPushButton:
        """
        Create an answer button for an option.

        Args:
            option: Answer option
            correct_answer: The correct answer

        Returns:
            Configured answer button
        """
        try:
            button = QPushButton(str(option))
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 12px;
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    padding: 12px 20px;
                    min-width: 80px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.3);
                    border: 2px solid rgba(255, 255, 255, 0.5);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.4);
                }
                QPushButton:disabled {
                    background-color: rgba(255, 0, 0, 0.3);
                    border: 2px solid rgba(255, 0, 0, 0.5);
                    color: rgba(255, 255, 255, 0.7);
                }
            """
            )

            button.clicked.connect(lambda: self._on_answer_selected(option))
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            return button

        except Exception as e:
            logger.error(f"Failed to create answer button: {e}")
            return QPushButton("Error")

    def _create_pictograph_option(self, option: Any, correct_answer: Any) -> QWidget:
        """
        Create a pictograph option widget using actual pictograph rendering.

        Args:
            option: Pictograph option data
            correct_answer: The correct pictograph

        Returns:
            Configured pictograph widget
        """
        try:
            # Import required components
            from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
            from presentation.components.pictograph.views import create_learn_view
            from domain.models.pictograph_data import PictographData

            # Extract PictographData from the option data structure
            actual_pictograph_data = None
            if isinstance(option, dict) and "data" in option:
                actual_pictograph_data = option["data"]
            elif isinstance(option, PictographData):
                actual_pictograph_data = option

            if actual_pictograph_data and isinstance(
                actual_pictograph_data, PictographData
            ):
                # Create a clickable frame container
                option_frame = QFrame()
                option_frame.setFrameStyle(QFrame.Shape.Box)
                option_frame.setStyleSheet(
                    """
                    QFrame {
                        background-color: rgba(255, 255, 255, 0.15);
                        border: 2px solid rgba(255, 255, 255, 0.3);
                        border-radius: 8px;
                    }
                    QFrame:hover {
                        background-color: rgba(255, 255, 255, 0.25);
                        border: 2px solid rgba(255, 255, 255, 0.5);
                    }
                    QFrame:pressed {
                        background-color: rgba(255, 255, 255, 0.35);
                    }
                """
                )

                # Set up layout for the frame
                layout = QVBoxLayout(option_frame)
                layout.setContentsMargins(4, 4, 4, 4)
                layout.setSpacing(0)

                # Create direct pictograph view for answer options (no widget wrapper)
                pictograph_widget = create_learn_view(
                    parent=option_frame, context="answer"
                )
                pictograph_widget.setSizePolicy(
                    QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
                )

                # Set size constraints for answer options
                pictograph_widget.setMinimumSize(100, 100)
                pictograph_widget.setMaximumSize(200, 200)

                # Fit to container as a square for consistent answer option display
                pictograph_widget.fit_to_container(200, 200, maintain_square=True)

                # Direct view handles its own scaling - no scaling context needed

                # Render the pictograph
                pictograph_widget.update_from_pictograph_data(actual_pictograph_data)

                # Add to layout
                layout.addWidget(pictograph_widget)

                # Make the frame clickable
                option_frame.mousePressEvent = lambda event: self._on_answer_selected(
                    option
                )
                option_frame.setCursor(Qt.CursorShape.PointingHandCursor)

                logger.info(f"✅ Created real pictograph option widget")
                return option_frame

            else:
                # Fallback to placeholder if no valid pictograph data
                return self._create_pictograph_placeholder(
                    f"Invalid option: {type(option)}"
                )

        except Exception as e:
            logger.error(f"Failed to create pictograph option: {e}")
            return self._create_pictograph_placeholder(f"Error: {e}")

    def _create_pictograph_placeholder(self, message: str) -> QWidget:
        """Create a placeholder widget for pictograph options."""
        from PyQt6.QtWidgets import QPushButton

        pictograph_button = QPushButton(message)
        pictograph_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                color: white;
                font-family: Georgia;
                min-width: 120px;
                min-height: 120px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.35);
            }
        """
        )

        pictograph_button.clicked.connect(
            lambda: self._on_answer_selected("placeholder")
        )
        pictograph_button.setCursor(Qt.CursorShape.PointingHandCursor)

        return pictograph_button

    def _on_answer_selected(self, selected_option: Any) -> None:
        """
        Handle answer selection.

        Args:
            selected_option: The selected answer option
        """
        try:
            self.answer_selected.emit(selected_option)
            logger.debug(f"Answer selected: {selected_option}")
        except Exception as e:
            logger.error(f"Failed to handle answer selection: {e}")

    def disable_option(self, option: Any) -> None:
        """
        Disable a specific answer option (for incorrect answers).

        Args:
            option: Option to disable
        """
        try:
            widget = self.answer_widgets.get(option)
            if widget and hasattr(widget, "setEnabled"):
                widget.setEnabled(False)
                logger.debug(f"Disabled answer option: {option}")
        except Exception as e:
            logger.error(f"Failed to disable option: {e}")

    def enable_all_options(self) -> None:
        """Enable all answer options."""
        try:
            for widget in self.answer_widgets.values():
                if hasattr(widget, "setEnabled"):
                    widget.setEnabled(True)
            logger.debug("Enabled all answer options")
        except Exception as e:
            logger.error(f"Failed to enable all options: {e}")

    def _clear_options(self) -> None:
        """Clear existing answer options."""
        try:
            # Remove all widgets from layout
            while self.layout.count():
                child = self.layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Clear tracking dictionaries
            self.answer_widgets.clear()

            logger.debug("Cleared answer options")

        except Exception as e:
            logger.error(f"Failed to clear answer options: {e}")

    def clear_all(self) -> None:
        """Clear all options and show placeholder."""
        try:
            self._clear_options()

            # Re-add placeholder
            self.layout.addWidget(self.placeholder_label, 0, 0)

            self.current_question = None
            self.current_format = ""

        except Exception as e:
            logger.error(f"Failed to clear all options: {e}")

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
            component_sizes = self.ui_service.get_component_sizes(
                parent_width, parent_height
            )
            spacing = self.ui_service.get_layout_spacing(parent_width, parent_height)

            # Update layout spacing
            answer_spacing = spacing.get("answer_options", 15)
            self.layout.setSpacing(answer_spacing)

            # Update button sizes and fonts
            if self.current_format == "button":
                button_size = component_sizes.get("answer_button", (150, 50))
                button_font_size = font_sizes.get("answer_button", 12)

                for widget in self.answer_widgets.values():
                    if isinstance(widget, QPushButton):
                        widget.setMinimumSize(*button_size)
                        font = widget.font()
                        font.setPointSize(button_font_size)
                        widget.setFont(font)

            elif self.current_format == "pictograph":
                pictograph_size = component_sizes.get("pictograph_view", (150, 150))

                for widget in self.answer_widgets.values():
                    if hasattr(widget, "setMinimumSize"):
                        widget.setMinimumSize(*pictograph_size)

        except Exception as e:
            logger.error(f"Failed to update responsive styling: {e}")
