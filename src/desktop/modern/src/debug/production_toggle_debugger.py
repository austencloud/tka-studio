"""
Production Toggle Debugger
==========================

Real-time debugging tool that runs within the actual TKA application
to monitor toggle functionality and identify production-specific failures.
"""
from __future__ import annotations

import time
from typing import Any

from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtWidgets import QWidget


# Use simple print statements for production debugging to avoid logging format issues
def production_log(message: str) -> None:
    """Simple production logging function"""
    import time

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
            original_toggle = self._graph_editor.toggle_visibility

            def debug_toggle_visibility():
                self._log_event(
                    "toggle_visibility_called",
                    {
                        "timestamp": time.time(),
                        "graph_editor_height": self._graph_editor.height(),
                        "graph_editor_visible": self._graph_editor.isVisible(),
                        "toggle_tab_visible": (
                            self._toggle_tab.isVisible() if self._toggle_tab else None
                        ),
                    },
                )
                result = original_toggle()
                self._log_event(
                    "toggle_visibility_returned",
                    {
                        "result": result,
                        "graph_editor_height": self._graph_editor.height(),
                        "graph_editor_visible": self._graph_editor.isVisible(),
                    },
                )
                return result

            self._graph_editor.toggle_visibility = debug_toggle_visibility
            production_log("✅ Hooked toggle_visibility method")

        # Start monitoring timer
        self._start_monitoring()

    def _start_monitoring(self) -> None:
        """Start continuous monitoring of component states"""
        self._monitoring_active = True

        # Create monitoring timer
        self._monitor_timer = QTimer(self)
        self._monitor_timer.timeout.connect(self._monitor_states)
        self._monitor_timer.start(100)  # Monitor every 100ms

        production_log("🔄 Started continuous state monitoring")

    def _monitor_states(self) -> None:
        """Monitor component states continuously"""
        if not self._monitoring_active:
            return

        # Only log significant state changes, not every tick
        current_state = self._get_current_state()

        # Check for significant changes
        if hasattr(self, "_last_state"):
            if self._state_changed(self._last_state, current_state):
                self._log_event("state_change", current_state)

        self._last_state = current_state

    def _get_current_state(self) -> dict[str, Any]:
        """Get current state of all monitored components"""
        state = {
            "timestamp": time.time(),
            "graph_editor": {
                "height": self._graph_editor.height() if self._graph_editor else None,
                "width": self._graph_editor.width() if self._graph_editor else None,
                "visible": (
                    self._graph_editor.isVisible() if self._graph_editor else None
                ),
                "min_height": (
                    self._graph_editor.minimumHeight() if self._graph_editor else None
                ),
                "max_height": (
                    self._graph_editor.maximumHeight() if self._graph_editor else None
                ),
            },
            "toggle_tab": {
                "visible": self._toggle_tab.isVisible() if self._toggle_tab else None,
                "position": str(self._toggle_tab.pos()) if self._toggle_tab else None,
                "size": str(self._toggle_tab.size()) if self._toggle_tab else None,
            },
            "animation": {
                "is_animating": (
                    self._animation_controller.is_animating()
                    if self._animation_controller
                    else None
                ),
                "internal_visible": (
                    getattr(self._animation_controller, "_is_visible", None)
                    if self._animation_controller
                    else None
                ),
            },
        }
        return state

    def _state_changed(
        self, old_state: dict[str, Any], new_state: dict[str, Any]
    ) -> bool:
        """Check if state has changed significantly"""
        # Check for visibility changes
        if old_state["graph_editor"]["visible"] != new_state["graph_editor"]["visible"]:
            return True
        if old_state["toggle_tab"]["visible"] != new_state["toggle_tab"]["visible"]:
            return True

        # Check for height changes
        if old_state["graph_editor"]["height"] != new_state["graph_editor"]["height"]:
            return True

        # Check for animation state changes
        return old_state["animation"]["is_animating"] != new_state["animation"]["is_animating"]

    def _log_event(self, event_type: str, data: dict[str, Any]) -> None:
        """Log a debug event"""
        event = {"type": event_type, "timestamp": time.time(), "data": data}
        self._event_sequence.append(event)

        # Emit signal for external listeners
        self.debug_event.emit(event_type, data)

        # Log to console
        production_log(f"📋 {event_type}: {data}")

    # Signal handlers
    def _on_toggle_requested(self) -> None:
        """Handle toggle requested signal"""
        self._last_click_time = time.time()
        self._log_event(
            "toggle_requested",
            {
                "click_time": self._last_click_time,
                "current_state": self._get_current_state(),
            },
        )

    def _on_animation_started(self, is_showing: bool) -> None:
        """Handle animation started signal"""
        self._log_event(
            "animation_started",
            {"is_showing": is_showing, "current_state": self._get_current_state()},
        )

    def _on_animation_finished(self, is_visible: bool) -> None:
        """Handle animation finished signal"""
        self._log_event(
            "animation_finished",
            {"is_visible": is_visible, "current_state": self._get_current_state()},
        )

    def get_event_sequence(self) -> list[dict[str, Any]]:
        """Get the complete event sequence"""
        return self._event_sequence.copy()

    def clear_events(self) -> None:
        """Clear the event sequence"""
        self._event_sequence.clear()
        production_log("🗑️ Cleared event sequence")

    def stop_monitoring(self) -> None:
        """Stop monitoring"""
        self._monitoring_active = False
        if hasattr(self, "_monitor_timer"):
            self._monitor_timer.stop()
        production_log("⏹️ Stopped monitoring")

    def run_production_test(self) -> None:
        """Run production toggle test to identify issues"""
        production_log("🧪 STARTING PRODUCTION TOGGLE TEST")
        production_log("=" * 50)

        if not self._graph_editor:
            production_log("❌ Graph editor not available")
            return

        # Clear previous events
        self.clear_events()
        production_log("🗑️ Cleared previous debug events")

        # Get initial state
        production_log("📊 INITIAL STATE:")
        initial_state = self._get_current_state()
        production_log(
            f"   Graph editor height: {initial_state['graph_editor']['height']}"
        )
        production_log(
            f"   Graph editor visible: {initial_state['graph_editor']['visible']}"
        )
        production_log(
            f"   Toggle tab visible: {initial_state['toggle_tab']['visible']}"
        )
        production_log(
            f"   Animation running: {initial_state['animation']['is_animating']}"
        )

        # Test 1: Direct toggle_visibility call
        production_log("🧪 TEST 1: Direct toggle_visibility() call")
        try:
            production_log("   Calling graph_editor.toggle_visibility()...")
            self._graph_editor.toggle_visibility()

            # Use QTimer to check state after animation
            from PyQt6.QtCore import QTimer

            QTimer.singleShot(500, self._check_test_results)

        except Exception as e:
            production_log(f"   ❌ Error in direct toggle: {e}")
            import traceback

            production_log(f"   Traceback: {traceback.format_exc()}")

    def _check_test_results(self) -> None:
        """Check test results after animation"""
        production_log("📊 RESULTS AFTER TOGGLE:")
        after_state = self._get_current_state()
        production_log(
            f"   Graph editor height: {after_state['graph_editor']['height']}"
        )
        production_log(
            f"   Graph editor visible: {after_state['graph_editor']['visible']}"
        )
        production_log(f"   Toggle tab visible: {after_state['toggle_tab']['visible']}")
        production_log(
            f"   Animation running: {after_state['animation']['is_animating']}"
        )

        # Show captured events
        production_log("📋 CAPTURED DEBUG EVENTS:")
        events = self.get_event_sequence()
        if events:
            for i, event in enumerate(events):
                production_log(f"   {i+1}. {event['type']} at {event['timestamp']:.3f}")
        else:
            production_log("   No events captured")

        production_log("🏁 Production toggle test completed")
        production_log("=" * 50)


# Global debugger instance
_production_debugger: ProductionToggleDebugger | None = None


def get_production_debugger() -> ProductionToggleDebugger:
    """Get or create the global production debugger instance"""
    global _production_debugger
    if _production_debugger is None:
        _production_debugger = ProductionToggleDebugger()
    return _production_debugger


def attach_to_application(main_window: QWidget) -> bool:
    """
    Attach the production debugger to the running TKA application.

    Args:
        main_window: The main TKA application window

    Returns:
        bool: True if successfully attached, False otherwise
    """
    debugger = get_production_debugger()
    return debugger.attach_to_application(main_window)


def get_debug_events() -> list[dict[str, Any]]:
    """Get all debug events from the production debugger"""
    debugger = get_production_debugger()
    return debugger.get_event_sequence()


def clear_debug_events() -> None:
    """Clear all debug events"""
    debugger = get_production_debugger()
    debugger.clear_events()
