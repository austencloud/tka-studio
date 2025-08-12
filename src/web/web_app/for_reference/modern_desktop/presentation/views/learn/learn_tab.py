"""
Learn Tab

Main learn tab implementation following the browse tab pattern.
Integrates with the existing tab system while using modern architecture internally.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.presentation.controllers.learn.learn_tab_coordinator import (
    LearnTabCoordinator,
)


# Import codex component


logger = logging.getLogger(__name__)


class LearnTab(QWidget):
    """
    Main learn tab following the browse tab pattern.

    Provides the external interface expected by the tab system while
    delegating all functionality to the modern coordinator architecture.
    """

    # Signals for main application
    error_occurred = pyqtSignal(str)

    def __init__(self, container: DIContainer, parent: QWidget | None = None):
        super().__init__(parent)

        # Set object name for test compatibility
        self.setObjectName("learn_tab")

        self.container = container
        self.coordinator: LearnTabCoordinator | None = None
        self.codex_component: CodexComponent | None = None
        self.splitter = None
        self.codex_visible = True

        self._setup_ui()

        logger.info("Learn tab initialized")

    def _setup_ui(self) -> None:
        """Setup the learn tab UI with codex on the left side."""
        try:
            # Import here to avoid circular imports
            from PyQt6.QtCore import Qt
            from PyQt6.QtWidgets import QSplitter

            from desktop.modern.presentation.components.codex import CodexComponent

            # Main layout
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            # Create splitter for codex + coordinator layout
            self.splitter = QSplitter(Qt.Orientation.Horizontal)

            # Create codex component (left side)
            self.codex_component = CodexComponent(self.container, self)
            self.codex_component.setMinimumWidth(250)
            self.splitter.addWidget(self.codex_component)

            # Create coordinator (right side)
            self.coordinator = LearnTabCoordinator(self.container, self)
            self.splitter.addWidget(self.coordinator)

            # Set initial splitter sizes (codex smaller than coordinator)
            self.splitter.setSizes([300, 700])

            # Add splitter to main layout
            layout.addWidget(self.splitter)

            # Connect signals
            self.coordinator.error_occurred.connect(self.error_occurred.emit)
            self.codex_component.error_occurred.connect(self.error_occurred.emit)

            logger.debug("Learn tab UI setup complete with codex")

        except Exception as e:
            logger.error(f"Failed to setup learn tab UI: {e}")
            self.error_occurred.emit(f"Failed to initialize learn tab: {e!s}")

    def resizeEvent(self, event) -> None:
        """Handle resize events."""
        try:
            super().resizeEvent(event)
            # Coordinator handles its own responsive updates
        except Exception as e:
            logger.error(f"Failed to handle resize event: {e}")

    def showEvent(self, event) -> None:
        """Handle show events (tab activation)."""
        try:
            super().showEvent(event)
            logger.debug("Learn tab shown")
        except Exception as e:
            logger.error(f"Failed to handle show event: {e}")

    def hideEvent(self, event) -> None:
        """Handle hide events (tab deactivation)."""
        try:
            super().hideEvent(event)
            logger.debug("Learn tab hidden")
        except Exception as e:
            logger.error(f"Failed to handle hide event: {e}")

    # Public interface methods (if needed by main application)

    def get_current_view(self) -> str:
        """Get current active view name."""
        if self.coordinator:
            return self.coordinator.get_current_view().value
        return "lesson_selector"

    def is_lesson_active(self) -> bool:
        """Check if a lesson is currently active."""
        if self.coordinator:
            state = self.coordinator.get_state_manager().get_state()
            return state.is_lesson_active()
        return False

    def toggle_codex(self) -> None:
        """Toggle the visibility of the codex."""
        if self.splitter and self.codex_component:
            if self.codex_visible:
                # Hide codex
                self.splitter.setSizes([0, 1000])
                self.codex_component.hide()
                self.codex_visible = False
                logger.debug("Codex hidden")
            else:
                # Show codex
                self.codex_component.show()
                self.splitter.setSizes([300, 700])
                self.codex_visible = True
                logger.debug("Codex shown")

    def is_codex_visible(self) -> bool:
        """Check if the codex is currently visible."""
        return self.codex_visible

    def get_codex_component(self) -> CodexComponent | None:
        """Get the codex component."""
        return self.codex_component
