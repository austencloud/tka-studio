"""
Lesson Mode Toggle Component

Provides radio button interface for selecting between fixed question
and countdown quiz modes.
"""

import logging
from typing import Optional

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

from core.interfaces.learn_services import ILearnUIService
from domain.models.learn import QuizMode

logger = logging.getLogger(__name__)


class LessonModeToggle(QWidget):
    """
    Widget for toggling between quiz modes.

    Provides radio button interface for selecting fixed question mode
    or countdown mode with descriptive labels.
    """

    # Signals
    mode_changed = pyqtSignal(str)  # mode value

    def __init__(self, ui_service: ILearnUIService, parent: Optional[QWidget] = None):
        """
        Initialize lesson mode toggle.

        Args:
            ui_service: Service for UI calculations
            parent: Parent widget
        """
        super().__init__(parent)

        self.ui_service = ui_service

        self._setup_ui()
        self._setup_connections()

        logger.debug("Lesson mode toggle initialized")

    def _setup_ui(self) -> None:
        """Setup mode toggle UI."""
        try:
            # Main layout
            main_layout = QHBoxLayout(self)
            main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.setContentsMargins(0, 0, 0, 0)

            # Container for the toggle group
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

            # Set fixed sizes for consistent appearance
            button_width = 120
            button_height = 36
            self.fixed_question_btn.setFixedSize(button_width, button_height)
            self.countdown_btn.setFixedSize(button_width, button_height)

            # Add buttons to toggle layout
            toggle_layout.addWidget(self.fixed_question_btn)
            toggle_layout.addWidget(self.countdown_btn)

            # Apply styling
            self._apply_styling()

            # Add toggle container to main layout
            main_layout.addWidget(self.toggle_container)

        except Exception as e:
            logger.error(f"Failed to setup mode toggle UI: {e}")

    def _setup_connections(self) -> None:
        """Setup signal connections."""
        try:
            self.fixed_question_btn.clicked.connect(self._on_fixed_question_clicked)
            self.countdown_btn.clicked.connect(self._on_countdown_clicked)
        except Exception as e:
            logger.error(f"Failed to setup mode toggle connections: {e}")

    def _apply_styling(self) -> None:
        """Apply styling to mode toggle components."""
        try:
            # Container styling (creates the border around the toggle group)
            container_style = """
                QWidget {
                    background-color: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 6px;
                }
            """

            # Button styling for modern toggle appearance
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

            # Apply styles
            self.toggle_container.setStyleSheet(container_style)
            self.fixed_question_btn.setStyleSheet(button_style)
            self.countdown_btn.setStyleSheet(button_style)

        except Exception as e:
            logger.error(f"Failed to apply mode toggle styling: {e}")

    def _on_fixed_question_clicked(self) -> None:
        """Handle fixed question button click."""
        try:
            self.fixed_question_btn.setChecked(True)
            self.countdown_btn.setChecked(False)
            self.mode_changed.emit(QuizMode.FIXED_QUESTION.value)
            logger.debug("Mode changed to: fixed_question")
        except Exception as e:
            logger.error(f"Failed to handle fixed question click: {e}")

    def _on_countdown_clicked(self) -> None:
        """Handle countdown button click."""
        try:
            self.countdown_btn.setChecked(True)
            self.fixed_question_btn.setChecked(False)
            self.mode_changed.emit(QuizMode.COUNTDOWN.value)
            logger.debug("Mode changed to: countdown")
        except Exception as e:
            logger.error(f"Failed to handle countdown click: {e}")

    def get_selected_mode(self) -> QuizMode:
        """
        Get currently selected quiz mode.

        Returns:
            Selected quiz mode
        """
        try:
            if self.fixed_question_btn.isChecked():
                return QuizMode.FIXED_QUESTION
            else:
                return QuizMode.COUNTDOWN
        except Exception as e:
            logger.error(f"Failed to get selected mode: {e}")
            return QuizMode.FIXED_QUESTION  # Default fallback

    def set_selected_mode(self, mode: QuizMode) -> None:
        """
        Set the selected quiz mode.

        Args:
            mode: Quiz mode to select
        """
        try:
            if mode == QuizMode.FIXED_QUESTION:
                self.fixed_question_btn.setChecked(True)
                self.countdown_btn.setChecked(False)
            elif mode == QuizMode.COUNTDOWN:
                self.countdown_btn.setChecked(True)
                self.fixed_question_btn.setChecked(False)
            else:
                logger.warning(f"Unknown quiz mode: {mode}")
        except Exception as e:
            logger.error(f"Failed to set selected mode: {e}")

    def update_responsive_styling(self, parent_width: int, parent_height: int) -> None:
        """
        Update styling based on parent widget size.

        Args:
            parent_width: Parent widget width
            parent_height: Parent widget height
        """
        try:
            # Get responsive font sizes
            font_sizes = self.ui_service.get_font_sizes(parent_width, parent_height)

            # Update button fonts
            button_font_size = font_sizes.get("mode_label", 12)
            for button in [self.fixed_question_btn, self.countdown_btn]:
                font = button.font()
                font.setFamily("Georgia")
                font.setPointSize(button_font_size)
                button.setFont(font)

        except Exception as e:
            logger.error(f"Failed to update responsive styling: {e}")
