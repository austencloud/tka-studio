"""
Generate Tab

Modern Generate Tab implementation wrapping the existing GeneratePanel
and GenerateTabController in a tab-compatible interface.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.presentation.components.generate_tab.generate_panel import (
    GeneratePanel,
)
from desktop.modern.presentation.components.generate_tab.generate_tab_controller import (
    GenerateTabController,
)


logger = logging.getLogger(__name__)


class GenerateTab(QWidget):
    """
    Main generate tab following the tab system pattern.

    Provides the external interface expected by the tab system while
    delegating all functionality to the existing GeneratePanel and
    GenerateTabController architecture.
    """

    # Signals for main application
    error_occurred = pyqtSignal(str)
    sequence_generated = pyqtSignal(object)  # Generated sequence data

    def __init__(self, container: DIContainer | None = None, parent: QWidget = None):
        """
        Initialize the generate tab.

        Args:
            container: DI container for service resolution
            parent: Parent widget
        """
        super().__init__(parent)

        self.container = container
        self._generate_panel: GeneratePanel | None = None
        self._controller: GenerateTabController | None = None

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup the UI with the existing GeneratePanel."""
        try:
            # Create main layout
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            # Create and add the generate panel
            self._generate_panel = GeneratePanel(container=self.container, parent=self)
            layout.addWidget(self._generate_panel)

            # Set background style to match other tabs
            self.setStyleSheet("""
                GenerateTab {
                    background: transparent;
                }
            """)

        except Exception as e:
            logger.exception(f"Failed to setup Generate Tab UI: {e}")
            self.error_occurred.emit(f"Failed to setup Generate Tab: {e}")
            self._create_error_fallback()

    def _create_error_fallback(self) -> None:
        """Create a fallback UI when the main UI fails."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont
        from PyQt6.QtWidgets import QLabel

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        error_label = QLabel(
            "⚠️ Generate Tab Error\n\nFailed to initialize generate panel"
        )
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        error_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                background: rgba(40, 40, 40, 0.3);
                border: 2px dashed rgba(255, 100, 100, 0.5);
                border-radius: 10px;
                padding: 30px;
                margin: 20px;
            }
        """)

        layout.addWidget(error_label)

    def _connect_signals(self) -> None:
        """Connect signals from the generate panel."""
        if self._generate_panel:
            # Forward controller signals if available
            controller = self._generate_panel.get_controller()
            if controller:
                self._controller = controller
                controller.generation_completed.connect(self._on_generation_completed)
                controller.error_occurred.connect(self.error_occurred.emit)

    def _on_generation_completed(self, result) -> None:
        """Handle generation completion."""
        if result.success and result.sequence_data:
            self.sequence_generated.emit(result.sequence_data)
            logger.info(
                f"Generate Tab: Successfully generated sequence with {len(result.sequence_data)} beats"
            )
        else:
            error_msg = result.error_message or "Unknown generation error"
            logger.warning(f"Generate Tab: Generation failed - {error_msg}")
            self.error_occurred.emit(error_msg)

    def get_generate_panel(self) -> GeneratePanel | None:
        """Get the underlying generate panel for direct access."""
        return self._generate_panel

    def get_controller(self) -> GenerateTabController | None:
        """Get the generation controller for direct access."""
        return self._controller

    def refresh(self) -> None:
        """Refresh the tab content."""
        if self._generate_panel:
            # Reset panel to initial state if needed
            pass

    def cleanup(self) -> None:
        """Cleanup resources when tab is closed."""
        if self._controller:
            # Cleanup controller resources if needed
            pass
        logger.debug("Generate Tab cleanup completed")

    def __del__(self):
        """Cleanup when tab is destroyed."""
        self.cleanup()
