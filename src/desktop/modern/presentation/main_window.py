"""
TKA Main Window - Simple window container

This module contains the main window class that simply holds the UI.
Focused on window lifecycle only - no business logic.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QMainWindow


class TKAMainWindow(QMainWindow):
    """
    Main application window for TKA.

    Simple window container that delegates all business logic to the orchestrator.
    """

    _instance_count = 0

    def __init__(self, container=None):
        super().__init__()

        TKAMainWindow._instance_count += 1
        print(
            f"[MAIN_WINDOW] Creating TKAMainWindow instance #{TKAMainWindow._instance_count}"
        )

        self.container = container

        if self.container:
            # Initialize the main UI
            self._initialize_ui()

    def _initialize_ui(self) -> None:
        """Initialize the main UI components."""
        from desktop.modern.application.services.core.application_orchestrator import (
            ApplicationOrchestrator,
        )

        # Create orchestrator and initialize application
        self.orchestrator = ApplicationOrchestrator()
        self.tab_widget = self.orchestrator.initialize_application(self)

    def show(self):
        """Override show to ensure tab widget is properly displayed."""
        super().show()

        # Ensure tab widget is shown when main window is shown
        if hasattr(self, "tab_widget") and self.tab_widget:
            self.tab_widget.show()
            self.tab_widget.setVisible(True)
            # Also show the current tab
            current_tab = self.tab_widget.currentWidget()
            if current_tab:
                current_tab.show()
                current_tab.setVisible(True)

    def resizeEvent(self, a0):
        """Handle window resize events."""
        super().resizeEvent(a0)

        if hasattr(self, "orchestrator"):
            self.orchestrator.handle_window_resize(self)
