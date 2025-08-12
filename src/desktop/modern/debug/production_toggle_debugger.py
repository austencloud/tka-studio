"""
Production Toggle Debugger
==========================

Real-time debugging tool that runs within the actual TKA application
to monitor toggle functionality and identify production-specific failures.
"""

from __future__ import annotations

import time
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget


# Use simple print statements for production debugging to avoid logging format issues
def production_log(message: str) -> None:
    """Simple production logging function"""

    timestamp = time.strftime("%H:%M:%S")
    print(f"🔍 [PROD-DEBUG] {timestamp} - {message}")


class ProductionToggleDebugger(QObject):
    """
    Production-context debugger that monitors toggle functionality
    in the actual running TKA application.
    """

    debug_event = pyqtSignal(str, dict)  # event_type, data

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._monitoring_active = False
        self._graph_editor: QWidget | None = None
        self._toggle_tab: QWidget | None = None
        self._animation_controller: QObject | None = None
        self._layout_manager: QObject | None = None
        self._workbench: QWidget | None = None

        # State tracking
        self._event_sequence: list[dict[str, Any]] = []
        self._last_click_time: float | None = None

        production_log("Production Toggle Debugger initialized")

    def attach_to_application(self, main_window: QWidget) -> bool:
        """
        Attach debugger to the running TKA application.

        Args:
            main_window: The main TKA application window

        Returns:
            bool: True if successfully attached, False otherwise
        """
        try:
            production_log("🔗 Attaching to TKA application...")

            # Navigate to workbench
            self._workbench = self._find_workbench(main_window)
            if not self._workbench:
                production_log("❌ Could not find workbench in application")
                return False

            production_log(f"✅ Found workbench: {type(self._workbench).__name__}")

            # Navigate to graph section
            graph_section = self._find_graph_section(self._workbench)
            if not graph_section:
                production_log("❌ Could not find graph section")
                return False

            production_log(f"✅ Found graph section: {type(graph_section).__name__}")

            # Navigate to graph editor
            self._graph_editor = self._find_graph_editor(graph_section)
            if not self._graph_editor:
                production_log("❌ Could not find graph editor")
                return False

            production_log(
                f"✅ Found graph editor: {type(self._graph_editor).__name__}"
            )

            # Get layout manager
            self._layout_manager = getattr(self._graph_editor, "_layout_manager", None)
            if not self._layout_manager:
                production_log("❌ Could not find layout manager")
                return False

            production_log(
                f"✅ Found layout manager: {type(self._layout_manager).__name__}"
            )

            # Get toggle tab
            self._toggle_tab = getattr(self._layout_manager, "_toggle_tab", None)
            if not self._toggle_tab:
                production_log("❌ Could not find toggle tab")
                return False

            production_log(f"✅ Found toggle tab: {type(self._toggle_tab).__name__}")

            # Get animation controller
            self._animation_controller = getattr(
                self._graph_editor, "_animation_controller", None
            )
            if not self._animation_controller:
                production_log("❌ Could not find animation controller")
                return False

            production_log(
                f"✅ Found animation controller: {type(self._animation_controller).__name__}"
            )

            # Hook into components
            self._install_debug_hooks()

            production_log("🎯 Successfully attached to TKA application!")
            return True

        except Exception as e:
            production_log(f"❌ Failed to attach to application: {e}")
            import traceback

            production_log(f"   Traceback: {traceback.format_exc()}")
            return False

    def _find_workbench(self, main_window: QWidget) -> QWidget | None:
        """Find the workbench widget in the main window"""
        # Look for workbench in main window children
        for child in main_window.findChildren(QWidget):
            if (
                hasattr(child, "_graph_section")
                or "workbench" in type(child).__name__.lower()
            ):
                return child
        return None

    def _find_graph_section(self, workbench: QWidget) -> QWidget | None:
        """Find the graph section in the workbench"""
        if hasattr(workbench, "_graph_section"):
            return workbench._graph_section

        # Search children
        for child in workbench.findChildren(QWidget):
            if (
                "graph" in type(child).__name__.lower()
                and "section" in type(child).__name__.lower()
            ):
                return child
        return None

    def _find_graph_editor(self, graph_section: QWidget) -> QWidget | None:
        """Find the graph editor in the graph section"""
        if hasattr(graph_section, "_graph_editor"):
            return graph_section._graph_editor

        # Search children
        for child in graph_section.findChildren(QWidget):
            if "grapheditor" in type(child).__name__.lower().replace("_", ""):
                return child
        return None

    def _install_debug_hooks(self) -> None:
        """Install debug hooks into the components"""
        production_log("🔧 Installing debug hooks...")

        # Hook toggle tab click
        if self._toggle_tab and hasattr(self._toggle_tab, "toggle_requested"):
            self._toggle_tab.toggle_requested.connect(self._on_toggle_requested)
            production_log("✅ Hooked toggle_requested signal")

        # Hook animation controller signals
        if self._animation_controller:
            if hasattr(self._animation_controller, "animation_started"):
                self._animation_controller.animation_started.connect(
                    self._on_animation_started
                )
                production_log("✅ Hooked animation_started signal")

            if hasattr(self._animation_controller, "animation_finished"):
                self._animation_controller.animation_finished.connect(
                    self._on_animation_finished
                )
                production_log("✅ Hooked animation_finished signal")

        # Hook graph editor toggle method
        if self._graph_editor and hasattr(self._graph_editor, "toggle_visibility"):
            self._graph_editor.toggle_visibility = debug_toggle_visibility
