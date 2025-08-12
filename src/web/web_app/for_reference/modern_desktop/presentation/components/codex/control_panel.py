"""
Codex Control Panel

Control panel for codex operations including rotate, mirror, color swap
and orientation selector.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class CodexControlButton(QPushButton):
    """Specialized button for codex operations."""

    def __init__(self, icon_name: str, tooltip: str, callback: Callable, parent=None):
        super().__init__(parent)

        self.callback = callback

        # Set button properties
        self.setFixedSize(40, 40)
        self.setToolTip(tooltip)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Load icon if available
        self._load_icon(icon_name)

        # Connect click event
        self.clicked.connect(self.callback)

        # Apply styling
        self.setStyleSheet("""
            QPushButton {
                border: 2px solid #ccc;
                border-radius: 5px;
                background-color: #f0f0f0;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-color: #999;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
                border-color: #666;
            }
        """)

    def _load_icon(self, icon_name: str) -> None:
        """Load icon for the button."""
        try:
            # Try to load icon from resources
            # For now, just set text as fallback
            if icon_name == "rotate.png":
                self.setText("↻")
            elif icon_name == "mirror.png":
                self.setText("⟷")
            elif icon_name == "yinyang1.png":
                self.setText("⚊⚋")
            else:
                self.setText("?")
        except Exception as e:
            logger.debug(f"Could not load icon {icon_name}: {e}")
            self.setText("?")


class CodexOrientationSelector(QComboBox):
    """Orientation selector for codex display."""

    orientation_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Add orientation options
        self.addItems(["Diamond", "Box", "Skewed"])

        # Set default
        self.setCurrentText("Diamond")

        # Connect signal
        self.currentTextChanged.connect(self.orientation_changed.emit)

        # Apply styling
        self.setStyleSheet("""
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
                min-width: 80px;
            }
            QComboBox:hover {
                border-color: #999;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """)


class CodexControlPanel(QWidget):
    """
    Control panel for codex operations.

    Provides buttons for rotate, mirror, color swap operations
    and orientation selector.
    """

    # Signals for operations
    rotate_requested = pyqtSignal()
    mirror_requested = pyqtSignal()
    color_swap_requested = pyqtSignal()
    orientation_changed = pyqtSignal(str)

    def __init__(self, container: DIContainer, parent=None):
        super().__init__(parent)

        self.container = container

        # Set object name for styling
        self.setObjectName("codex_control_panel")

        # Setup UI
        self._setup_ui()

        logger.debug("CodexControlPanel initialized")

    def _setup_ui(self) -> None:
        """Setup the control panel UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Orientation selector section
        orientation_layout = QHBoxLayout()
        orientation_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        orientation_label = QLabel("Orientation:")
        orientation_label.setStyleSheet("font-weight: bold;")

        self.orientation_selector = CodexOrientationSelector(self)
        self.orientation_selector.orientation_changed.connect(
            self.orientation_changed.emit
        )

        orientation_layout.addWidget(orientation_label)
        orientation_layout.addWidget(self.orientation_selector)

        # Control buttons section
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.setSpacing(10)

        # Create control buttons
        self.rotate_button = CodexControlButton(
            "rotate.png",
            "Rotate all pictographs 90° clockwise",
            self._on_rotate_clicked,
            self,
        )

        self.mirror_button = CodexControlButton(
            "mirror.png",
            "Mirror all pictographs vertically",
            self._on_mirror_clicked,
            self,
        )

        self.color_swap_button = CodexControlButton(
            "yinyang1.png",
            "Swap red and blue colors",
            self._on_color_swap_clicked,
            self,
        )

        # Add buttons to layout
        buttons_layout.addWidget(self.rotate_button)
        buttons_layout.addWidget(self.mirror_button)
        buttons_layout.addWidget(self.color_swap_button)

        # Add sections to main layout
        main_layout.addLayout(orientation_layout)
        main_layout.addLayout(buttons_layout)

        # Apply panel styling
        self.setStyleSheet("""
            CodexControlPanel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
        """)

    def _on_rotate_clicked(self) -> None:
        """Handle rotate button click."""
        logger.debug("Rotate button clicked")
        self.rotate_requested.emit()

    def _on_mirror_clicked(self) -> None:
        """Handle mirror button click."""
        logger.debug("Mirror button clicked")
        self.mirror_requested.emit()

    def _on_color_swap_clicked(self) -> None:
        """Handle color swap button click."""
        logger.debug("Color swap button clicked")
        self.color_swap_requested.emit()

    def get_current_orientation(self) -> str:
        """Get the currently selected orientation."""
        return self.orientation_selector.currentText()

    def set_orientation(self, orientation: str) -> None:
        """Set the orientation selector value."""
        self.orientation_selector.setCurrentText(orientation)
