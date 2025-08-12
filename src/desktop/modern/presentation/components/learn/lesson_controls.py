"""
Lesson Controls Component

Focused component for lesson navigation and control buttons including
back, pause/resume, and restart functionality with consistent styling.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget


logger = logging.getLogger(__name__)


class LessonControls(QWidget):
    """
    Focused component for lesson navigation and control buttons.

    Provides consistent control interface with proper state management
    and responsive design for lesson navigation.
    """

    # Signals
    back_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    restart_clicked = pyqtSignal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self._is_paused: bool = False
        self._show_pause_button: bool = False

        self._setup_ui()
        self._connect_signals()

        logger.debug("Lesson controls component initialized")

    def _setup_ui(self) -> None:
        """Setup controls UI."""
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Note: Back button is handled by the workspace view to avoid duplication

        # Add stretch to push other controls to the right
        layout.addStretch()

        # Pause/Resume button (conditional visibility)
        self.pause_button = self._create_control_button("⏸ Pause", "pause")
        self.pause_button.setVisible(False)
        layout.addWidget(self.pause_button)

        # Restart button (conditional visibility)
        self.restart_button = self._create_control_button("↻ Restart", "restart")
        self.restart_button.setVisible(False)
        layout.addWidget(self.restart_button)

    def _create_control_button(self, text: str, button_type: str) -> QPushButton:
        """
        Create a control button with consistent styling.

        Args:
            text: Button text
            button_type: Type of button for styling

        Returns:
            Configured control button
        """
        button = QPushButton(text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Apply styling based on button type
        if button_type == "back":
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.2);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 12px;
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 8px 16px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.3);
                    border: 2px solid rgba(255, 255, 255, 0.5);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.4);
                }
                QPushButton:disabled {
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    color: rgba(255, 255, 255, 0.5);
                }
            """
            )

        elif button_type == "pause":
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(255, 165, 0, 0.7);
                    border: 2px solid rgba(255, 165, 0, 0.9);
                    border-radius: 12px;
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 8px 16px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 165, 0, 0.8);
                    border: 2px solid rgba(255, 185, 20, 1.0);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 165, 0, 0.9);
                }
                QPushButton:disabled {
                    background-color: rgba(255, 165, 0, 0.3);
                    border: 2px solid rgba(255, 165, 0, 0.4);
                    color: rgba(255, 255, 255, 0.5);
                }
            """
            )

        elif button_type == "restart":
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(62, 99, 221, 0.7);
                    border: 2px solid rgba(62, 99, 221, 0.9);
                    border-radius: 12px;
                    color: white;
                    font-family: Georgia;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 8px 16px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: rgba(62, 99, 221, 0.8);
                    border: 2px solid rgba(82, 119, 241, 1.0);
                }
                QPushButton:pressed {
                    background-color: rgba(62, 99, 221, 0.9);
                }
                QPushButton:disabled {
                    background-color: rgba(62, 99, 221, 0.3);
                    border: 2px solid rgba(62, 99, 221, 0.4);
                    color: rgba(255, 255, 255, 0.5);
                }
            """
            )

        return button

    def _connect_signals(self) -> None:
        """Connect button signals."""
        # Note: Back button is handled by the workspace view
        self.pause_button.clicked.connect(self.pause_clicked.emit)
        self.restart_button.clicked.connect(self.restart_clicked.emit)

    def enable_controls(self, enabled: bool) -> None:
        """
        Enable or disable all controls.

        Args:
            enabled: Whether controls should be enabled
        """
        # Note: Back button is handled by the workspace view
        self.pause_button.setEnabled(enabled)
        self.restart_button.setEnabled(enabled)
        logger.debug(f"Controls enabled: {enabled}")

    def update_responsive_styling(self, parent_width: int, parent_height: int) -> None:
        """Update styling based on parent widget size."""
        try:
            # Calculate responsive sizes
            font_size = max(10, min(14, parent_width // 60))
            button_height = max(30, min(45, parent_height // 20))
            button_width = max(70, min(100, parent_width // 12))

            # Update all buttons (back button is handled by workspace view)
            for button in [self.pause_button, self.restart_button]:
                # Update size
                button.setMinimumSize(button_width, button_height)

                # Update font
                font = button.font()
                font.setPointSize(font_size)
                button.setFont(font)

        except Exception as e:
            logger.exception(f"Failed to update responsive styling: {e}")

    def is_restart_button_visible(self) -> bool:
        """Check if restart button is visible."""
        return self.restart_button.isVisible()
