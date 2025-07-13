"""
Modern Visibility Tab - Refactored Component Coordinator.

Streamlined coordinator that manages decomposed visibility components following
TKA clean architecture principles. Reduced from 631 lines to focused coordination.
"""

import logging
from typing import Any, Dict, Optional

from application.services.pictograph.global_visibility_service import (
    PictographVisibilityManager,
)
from application.services.pictograph.visibility_state_manager import (
    VisibilityStateManager,
)
from core.interfaces.tab_settings_interfaces import IVisibilitySettingsManager
from presentation.components.ui.settings.visibility.components import (
    DependencyWarning,
    ElementVisibilitySection,
    MotionControlsSection,
    VisibilityPreviewSection,
)
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

logger = logging.getLogger(__name__)


class VisibilityTab(QWidget):
    """
    Modern Visibility Tab - Component Coordinator.

    Streamlined coordinator managing decomposed visibility components while maintaining
    all existing functionality. Follows TKA clean architecture and single-responsibility principles.

    Features:
    - Component-based architecture with focused responsibilities
    - Real pictograph preview using PictographScene
    - Motion controls with dependency validation
    - Organized element control management
    - Global visibility application
    """

    visibility_changed = pyqtSignal(str, bool)

    def __init__(
        self,
        visibility_service: IVisibilitySettingsManager,
        global_visibility_service: PictographVisibilityManager,
        parent=None,
    ):
        """
        Initialize visibility tab coordinator.

        Args:
            visibility_service: Service for visibility state management
            global_visibility_service: Service for global visibility updates
            parent: Parent widget
        """
        super().__init__(parent)

        # Services
        self.visibility_service = visibility_service
        self.state_manager = VisibilityStateManager(visibility_service)
        self.global_visibility_service = global_visibility_service

        # Component sections
        self.motion_section: Optional[MotionControlsSection] = None
        self.element_section: Optional[ElementVisibilitySection] = None
        self.preview_section: Optional[VisibilityPreviewSection] = None
        self.dependency_warning: Optional[DependencyWarning] = None

        # Update timer for batching rapid changes
        self._update_timer = QTimer()
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._apply_global_updates)

        self._setup_ui()
        self._setup_connections()
        self._load_initial_settings()
        self._register_observers()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        title = QLabel("Visibility Settings")
        title.setObjectName("section_title")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        main_layout.addWidget(title)

        description = QLabel("Control which elements are visible in pictographs")
        description.setObjectName("description")
        description.setFont(QFont("Arial", 10))
        main_layout.addWidget(description)

        # Fixed 50/50 horizontal layout
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        controls_widget = self._create_controls_widget()
        preview_widget = self._create_preview_widget()

        controls_widget.setSizePolicy(
            controls_widget.sizePolicy().horizontalPolicy(),
            controls_widget.sizePolicy().verticalPolicy(),
        )
        preview_widget.setSizePolicy(
            preview_widget.sizePolicy().horizontalPolicy(),
            preview_widget.sizePolicy().verticalPolicy(),
        )

        content_layout.addWidget(controls_widget, 1)
        content_layout.addWidget(preview_widget, 1)

        main_layout.addLayout(content_layout)
        self._apply_styling()

    def _create_controls_widget(self) -> QWidget:
        """Create the controls section with component coordination."""
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(12)

        # Motion controls section
        self.motion_section = MotionControlsSection(
            self.visibility_service, self.state_manager
        )
        controls_layout.addWidget(self.motion_section)

        # Dependency warning (initially hidden)
        self.dependency_warning = DependencyWarning()
        controls_layout.addWidget(self.dependency_warning)

        # Element controls section
        self.element_section = ElementVisibilitySection(
            self.visibility_service, self.state_manager
        )
        controls_layout.addWidget(self.element_section)

        controls_layout.addStretch()
        return controls_widget

    def _create_preview_widget(self) -> QWidget:
        """Create the preview section with component coordination."""
        self.preview_section = VisibilityPreviewSection()
        return self.preview_section

    def _setup_connections(self):
        """Setup signal connections between components."""
        # Connect motion section signals
        if self.motion_section:
            self.motion_section.motion_visibility_changed.connect(
                self._on_motion_visibility_changed
            )

        # Connect element section signals
        if self.element_section:
            self.element_section.element_visibility_changed.connect(
                self._on_element_visibility_changed
            )

        # Connect preview section signals
        if self.preview_section:
            self.preview_section.preview_updated.connect(self._on_preview_updated)

    def _register_observers(self):
        """Register with state manager for updates."""
        self.state_manager.register_observer(
            self._on_state_changed, ["motion", "glyph", "buttons"]
        )

    def _load_initial_settings(self):
        """Load initial settings and update components."""
        # Components handle their own initial loading
        self._update_dependency_states()

    def _on_motion_visibility_changed(self, color: str, visible: bool):
        """
            Handle motion visibility changes with coordination.

            Args:
                color: Motion color ("blue" or "red")def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        title = QLabel("Visibility Settings")
        title.setObjectName("section_title")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        main_layout.addWidget(title)

        description = QLabel("Control which elements are visible in pictographs")
        description.setObjectName("description")
        description.setFont(QFont("Arial", 10))
        main_layout.addWidget(description)

        # Fixed 50/50 horizontal layout
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        controls_widget = self._create_controls_widget()
        preview_widget = self._create_preview_widget()

        controls_widget.setSizePolicy(
            controls_widget.sizePolicy().horizontalPolicy(),
            controls_widget.sizePolicy().verticalPolicy()
        )
        preview_widget.setSizePolicy(
            preview_widget.sizePolicy().horizontalPolicy(),
            preview_widget.sizePolicy().verticalPolicy()
        )

        content_layout.addWidget(controls_widget, 1)
        content_layout.addWidget(preview_widget, 1)

        main_layout.addLayout(content_layout)
        self._apply_styling()

                visible: Whether the motion should be visible
        """
        try:
            # Update preview
            if self.preview_section:
                self.preview_section.update_visibility(f"{color}_motion", visible)

            # Update dependency states
            self._update_dependency_states()

            # Schedule global update
            self._schedule_global_update()

            # Emit signal
            self.visibility_changed.emit(f"motion_{color}", visible)

            logger.debug(f"Motion visibility changed: {color} = {visible}")

        except Exception as e:
            logger.error(f"Error handling motion visibility change: {e}")

    def _on_element_visibility_changed(self, name: str, visible: bool):
        """
        Handle element visibility changes with coordination.

        Args:
            name: Element name
            visible: Whether the element should be visible
        """
        try:
            # Update preview
            if self.preview_section:
                self.preview_section.update_visibility(name, visible)

            # Schedule global update
            self._schedule_global_update()

            # Emit signal
            self.visibility_changed.emit(f"element_{name}", visible)

            logger.debug(f"Element visibility changed: {name} = {visible}")

        except Exception as e:
            logger.error(f"Error handling element visibility change: {e}")

    def _on_state_changed(self):
        """Handle state manager notifications."""
        self._update_dependency_states()
        if self.motion_section:
            self.motion_section.update_motion_toggles()

    def _update_dependency_states(self):
        """Update UI based on motion dependency states."""
        all_motions_visible = self.state_manager.are_all_motions_visible()

        # Update element section dependency state
        if self.element_section:
            self.element_section.update_motion_dependency(all_motions_visible)

        # Update dependency warning
        if self.dependency_warning:
            self.dependency_warning.update_warning_state(all_motions_visible)

    def _schedule_global_update(self):
        """Schedule a global update with debouncing."""
        self._update_timer.stop()
        self._update_timer.start(200)  # 200ms delay for batching

    def _apply_global_updates(self):
        """Apply visibility changes to all pictographs globally."""
        try:
            # Get current visibility states
            motion_states = {}
            element_states = {}

            if self.motion_section:
                motion_states = self.motion_section.get_motion_states()

            if self.element_section:
                element_states = self.element_section.get_element_states()

            # Apply motion visibility changes
            for color, visible in motion_states.items():
                result = self.global_visibility_service.apply_visibility_change(
                    element_type="motion",
                    element_name=f"{color}_motion",
                    visible=visible,
                )
                logger.debug(
                    f"Applied motion visibility {color}={visible}: {result['success_count']} updated"
                )

            # Apply element visibility changes
            for element_name, visible in element_states.items():
                # Determine appropriate element type
                if element_name == "Non-radial_points":
                    element_type = "grid"
                else:
                    element_type = "glyph"

                result = self.global_visibility_service.apply_visibility_change(
                    element_type=element_type,
                    element_name=element_name,
                    visible=visible,
                )
                logger.debug(
                    f"Applied element visibility {element_name}={visible}: {result['success_count']} updated"
                )

            logger.info("Successfully applied global visibility updates")

        except Exception as e:
            logger.error(f"Error applying global updates: {e}")

    def _on_preview_updated(self):
        """Handle preview update notifications."""
        logger.debug("Preview updated")

    def refresh_all_settings(self):
        """Force refresh all settings from the service."""
        self._load_initial_settings()
        if self.preview_section:
            self.preview_section.refresh_preview()

    def cleanup(self):
        """Clean up resources when tab is destroyed."""
        try:
            # Stop timers
            self._update_timer.stop()

            # Clean up preview section
            if self.preview_section:
                self.preview_section.cleanup()

            logger.debug("Visibility tab cleaned up")

        except Exception as e:
            logger.error(f"Error during visibility tab cleanup: {e}")

    def _apply_styling(self):
        """Apply modern glassmorphism styling to the entire tab."""
        self.setStyleSheet(
            """
            QWidget {
                background: transparent;
                color: white;
            }

            QLabel#section_title {
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }

            QLabel#description {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                margin-bottom: 20px;
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

            QLabel#dependency_warning {
                color: rgba(255, 193, 7, 1.0);
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
                background: rgba(255, 193, 7, 0.1);
                border: 2px solid rgba(255, 193, 7, 0.3);
                border-radius: 8px;
                margin: 10px 0;
            }

            QFrame#motion_section {
                background: rgba(59, 130, 246, 0.1);
                border: 2px solid rgba(59, 130, 246, 0.2);
                border-radius: 12px;
                padding: 20px;
                margin: 5px;
            }

            QFrame#element_section {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 20px;
                margin: 5px;
            }

            QSplitter::handle {
                background: rgba(255, 255, 255, 0.2);
                width: 2px;
            }

            QSplitter::handle:hover {
                background: rgba(255, 255, 255, 0.4);
            }
        """
        )
