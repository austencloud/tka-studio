"""
Graph Editor Hotkey Service Usage Example

This example demonstrates how to use the refactored hotkey service
with proper service separation using the Adapter Pattern.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.interfaces.workbench_services import IGraphEditorService


# Example 1: Using the Qt Adapter (recommended for Qt components)
def create_hotkey_service_with_qt_signals(graph_service: "IGraphEditorService"):
    """Create hotkey service with Qt signal support"""
    from .graph_editor_hotkey_adapter import GraphEditorHotkeyAdapter

    # Create the adapter (handles Qt signals)
    hotkey_adapter = GraphEditorHotkeyAdapter(graph_service)

    # Connect to Qt signals
    hotkey_adapter.arrow_moved.connect(handle_arrow_moved)
    hotkey_adapter.rotation_override_requested.connect(handle_rotation_override)

    return hotkey_adapter


# Example 2: Using the Pure Service (recommended for non-Qt components)
def create_hotkey_service_with_callbacks(graph_service: "IGraphEditorService"):
    """Create hotkey service with callback-based communication"""
    from .graph_editor_hotkey_service import GraphEditorHotkeyService

    # Create callback handler
    class MyCallbackHandler:
        def on_arrow_moved(self, arrow_id: str, delta_x: int, delta_y: int) -> None:
            print(f"Arrow {arrow_id} moved by ({delta_x}, {delta_y})")

        def on_rotation_override_requested(self, arrow_id: str) -> None:
            print(f"Rotation override requested for arrow {arrow_id}")

        def on_special_placement_removal_requested(self, arrow_id: str) -> None:
            print(f"Special placement removal requested for arrow {arrow_id}")

        def on_prop_placement_override_requested(self, arrow_id: str) -> None:
            print(f"Prop placement override requested for arrow {arrow_id}")

    # Create the pure service
    callback_handler = MyCallbackHandler()
    hotkey_service = GraphEditorHotkeyService(graph_service, callback_handler)

    return hotkey_service


# Example signal handlers
def handle_arrow_moved(arrow_id: str, delta_x: int, delta_y: int):
    """Handle arrow movement signal"""
    print(f"Qt Signal: Arrow {arrow_id} moved by ({delta_x}, {delta_y})")


def handle_rotation_override(arrow_id: str):
    """Handle rotation override signal"""
    print(f"Qt Signal: Rotation override for arrow {arrow_id}")


# Example usage in a Qt component
def example_integration():
    """Example of integrating the hotkey service in a Qt component"""
    from PyQt6.QtWidgets import QWidget
    from PyQt6.QtCore import pyqtSignal

    class GraphEditorWidget(QWidget):
        # This widget can use the adapter for Qt signal integration

        def __init__(self, graph_service):
            super().__init__()

            # Use the adapter for Qt signal support
            self.hotkey_adapter = create_hotkey_service_with_qt_signals(graph_service)

            # Connect to our own handlers
            self.hotkey_adapter.arrow_moved.connect(self.on_arrow_moved)

        def keyPressEvent(self, event):
            """Handle key press events"""
            if self.hotkey_adapter.handle_key_event(event):
                return  # Event was handled by hotkey service
            super().keyPressEvent(event)

        def on_arrow_moved(self, arrow_id: str, delta_x: int, delta_y: int):
            """Handle arrow movement in this widget"""
            # Update the visual representation
            pass
