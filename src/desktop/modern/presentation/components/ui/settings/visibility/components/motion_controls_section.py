"""
Motion Controls Section for Visibility Settings.

Focused component handling motion visibility controls with validation and glassmorphism styling.
Extracted from the monolithic visibility tab following TKA clean architecture principles.
"""

import logging

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from desktop.modern.core.interfaces.tab_settings_interfaces import (
    IVisibilitySettingsManager,
)
from desktop.modern.presentation.components.ui.settings.components.motion_toggle import (
    MotionToggle,
)

logger = logging.getLogger(__name__)


class MotionControlsSection(QFrame):
    """
    Motion controls section with validation and glassmorphism styling.

    Handles motion visibility toggles, validation logic, and user feedback.
    Follows TKA single-responsibility principle and dependency injection patterns.
    """

    motion_visibility_changed = pyqtSignal(str, bool)

    def __init__(
        self,
        visibility_service: IVisibilitySettingsManager,
        simple_visibility_service,
        parent=None,
    ):
        """
        Initialize motion controls section.

        Args:
            visibility_service: Service for visibility state management (legacy interface)
            simple_visibility_service: Simple visibility service for state management
            parent: Parent widget
        """
        super().__init__(parent)

        # Service dependencies
        self.visibility_service = visibility_service
        self.simple_visibility_service = simple_visibility_service

        # UI components
        self.motion_toggles: dict[str, MotionToggle] = {}

        self._setup_ui()
        self._setup_connections()
        self._load_initial_settings()

    def _setup_ui(self):
        """Setup the motion controls UI with glassmorphism styling."""
        self.setObjectName("motion_section")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Section title
        title = QLabel("Motion Controls")
        title.setObjectName("subsection_title")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        # Motion toggle buttons in horizontal layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        for color in ["blue", "red"]:
            toggle = MotionToggle(color)
            self.motion_toggles[color] = toggle
            button_layout.addWidget(toggle)

        layout.addLayout(button_layout)

        # Note about motion visibility
        note = QLabel("Note: At least one motion type must remain visible")
        note.setObjectName("note")
        note.setWordWrap(True)
        layout.addWidget(note)

        self._apply_styling()

    def _setup_connections(self):
        """Setup signal connections for motion toggles."""
        for color, toggle in self.motion_toggles.items():
            toggle.toggled.connect(
                lambda checked, c=color: self._on_motion_visibility_changed(c, checked)
            )

    def _load_initial_settings(self):
        """Load initial motion visibility settings."""
        for color, toggle in self.motion_toggles.items():
            visible = self.simple_visibility_service.get_motion_visibility(color)
            toggle.set_active(visible)

    def _on_motion_visibility_changed(self, color: str, visible: bool):
        """
        Handle motion visibility changes with validation.

        Args:
            color: Motion color ("blue" or "red")
            visible: Whether the motion should be visible
        """
        try:
            # Use simple visibility service for validation and updates
            self.simple_visibility_service.set_motion_visibility(color, visible)

            # Emit signal for parent coordination
            self.motion_visibility_changed.emit(color, visible)

            logger.debug(f"Motion visibility changed: {color} = {visible}")

        except Exception as e:
            logger.error(f"Error changing motion visibility: {e}")
            # Revert toggle state on error
            toggle = self.motion_toggles.get(color)
            if toggle:
                toggle.set_active(not visible)

    def update_motion_toggles(self):
        """Update motion toggle states from simple visibility service."""
        for color, toggle in self.motion_toggles.items():
            visible = self.simple_visibility_service.get_motion_visibility(color)
            if toggle.get_is_active() != visible:
                toggle.set_active(visible)

    def get_motion_states(self) -> dict[str, bool]:
        """
        Get current motion visibility states.

        Returns:
            Dictionary mapping motion colors to visibility states
        """
        return {
            color: toggle.get_is_active()
            for color, toggle in self.motion_toggles.items()
        }

    def _apply_styling(self):
        """Apply glassmorphism styling to the section."""
        self.setStyleSheet(
            """
            QFrame#motion_section {
                background: rgba(59, 130, 246, 0.1);
                border: 2px solid rgba(59, 130, 246, 0.2);
                border-radius: 12px;
                padding: 20px;
                margin: 5px;
            }

            QLabel#subsection_title {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 15px;
            }

            QLabel#note {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                font-style: italic;
                margin-top: 15px;
                padding: 10px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 6px;
                border-left: 3px solid rgba(255, 193, 7, 0.8);
            }
        """
        )
