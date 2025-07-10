"""
Element Visibility Section for Visibility Settings.

Focused component handling element visibility controls with dependency management.
Extracted from the monolithic visibility tab following TKA clean architecture principles.
"""

import logging
from typing import Dict

from application.services.pictograph.visibility_state_manager import (
    VisibilityStateManager,
)
from core.interfaces.tab_settings_interfaces import IVisibilitySettingsManager
from presentation.components.ui.settings.components.element_toggle import ElementToggle
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout

logger = logging.getLogger(__name__)


class ElementVisibilitySection(QFrame):
    """
    Element visibility controls section with dependency management.

    Handles element visibility toggles, motion dependency logic, and organized grid layout.
    Follows TKA single-responsibility principle and dependency injection patterns.
    """

    element_visibility_changed = pyqtSignal(str, bool)

    def __init__(
        self,
        visibility_service: IVisibilitySettingsManager,
        state_manager: VisibilityStateManager,
        parent=None,
    ):
        """
        Initialize element visibility section.

        Args:
            visibility_service: Service for visibility state management
            state_manager: State manager for validation and updates
            parent: Parent widget
        """
        super().__init__(parent)

        # Service dependencies
        self.visibility_service = visibility_service
        self.state_manager = state_manager

        # UI components
        self.element_toggles: Dict[str, ElementToggle] = {}

        self._setup_ui()
        self._setup_connections()
        self._load_initial_settings()

    def _setup_ui(self):
        """Setup the element visibility controls UI with organized grid layout."""
        self.setObjectName("element_section")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Section title
        title = QLabel("Element Visibility Controls")
        title.setObjectName("subsection_title")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        # Element controls in organized grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(6)

        # Define element groups with their properties
        element_groups = [
            ("TKA", "Show TKA (The Kinetic Alphabet) symbols", True, 0, 0),
            ("Reversals", "Show reversal indicators", False, 0, 1),
            ("VTG", "Show VTG (Vertical/Twist/Gyre) symbols", True, 1, 0),
            ("Elemental", "Show elemental symbols", True, 1, 1),
            ("Positions", "Show position indicators", True, 2, 0),
            ("Non-radial_points", "Show non-radial point indicators", False, 2, 1),
        ]

        for name, tooltip, is_dependent, row, col in element_groups:
            toggle = ElementToggle(name.replace("_", " ").replace("-", " "), tooltip)
            toggle.set_dependent(is_dependent)
            self.element_toggles[name] = toggle
            grid_layout.addWidget(toggle, row, col)

        layout.addLayout(grid_layout)
        self._apply_styling()

    def _setup_connections(self):
        """Setup signal connections for element toggles."""
        for name, toggle in self.element_toggles.items():
            toggle.toggled.connect(
                lambda checked, n=name: self._on_element_visibility_changed(n, checked)
            )

    def _load_initial_settings(self):
        """Load initial element visibility settings."""
        for name, toggle in self.element_toggles.items():
            visible = self.state_manager.get_glyph_visibility(name)
            toggle.setChecked(visible)

    def _on_element_visibility_changed(self, name: str, visible: bool):
        """
        Handle element visibility changes.

        Args:
            name: Element name
            visible: Whether the element should be visible
        """
        try:
            # Use state manager for updates
            self.state_manager.set_glyph_visibility(name, visible)

            # Emit signal for parent coordination
            self.element_visibility_changed.emit(name, visible)

            logger.debug(f"Element visibility changed: {name} = {visible}")

        except Exception as e:
            logger.error(f"Error changing element visibility: {e}")
            # Revert toggle state on error
            toggle = self.element_toggles.get(name)
            if toggle:
                toggle.setChecked(not visible)

    def update_motion_dependency(self, all_motions_visible: bool):
        """
        Update element toggles based on motion dependency states.

        Args:
            all_motions_visible: Whether all motions are currently visible
        """
        for _, toggle in self.element_toggles.items():
            if toggle.get_is_dependent():
                toggle.set_motions_visible(all_motions_visible)

    def get_element_states(self) -> Dict[str, bool]:
        """
        Get current element visibility states.

        Returns:
            Dictionary mapping element names to visibility states
        """
        return {
            name: toggle.isChecked() for name, toggle in self.element_toggles.items()
        }

    def get_dependent_elements(self) -> Dict[str, bool]:
        """
        Get elements that depend on motion visibility.

        Returns:
            Dictionary mapping dependent element names to their dependency status
        """
        return {
            name: toggle.get_is_dependent()
            for name, toggle in self.element_toggles.items()
        }

    def _apply_styling(self):
        """Apply glassmorphism styling to the section."""
        self.setStyleSheet(
            """
            QFrame#element_section {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
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
        """
        )
