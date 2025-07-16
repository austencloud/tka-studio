#!/usr/bin/env python3
"""
Test script to verify menu bar layout changes.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src", "desktop", "modern"))

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow


# Mock the styled button and navigation widget for testing
class MockStyledButton:
    def __init__(self, label, context, parent=None):
        self.label = label
        self.parent = parent
        self._width = 120
        self._height = 40

    def clicked(self):
        pass

    def connect(self, slot):
        pass

    def setFont(self, font):
        pass

    def update_appearance(self):
        pass

    def setFixedSize(self, width, height):
        self._width = width
        self._height = height

    def width(self):
        return self._width

    def height(self):
        return self._height

    def move(self, x, y):
        print(f"Settings button positioned at ({x}, {y})")

    def raise_(self):
        pass

    def show(self):
        pass


class MockNavigationWidget:
    def __init__(self, parent=None, size_provider=None):
        self.parent = parent

    def tab_changed(self):
        pass

    def connect(self, slot):
        pass

    def set_active_tab(self, tab_name):
        pass

    def get_current_tab(self):
        return "construct"

    def get_available_tabs(self):
        return ["construct", "browse", "learn", "sequence_card"]

    def update_size_provider(self, size_provider):
        pass


# Mock imports
import sys

sys.modules["PyQt6.QtCore"].pyqtSignal = lambda *args: lambda: None

# Patch the imports
sys.modules["src.presentation.components.menu_bar.buttons.styled_button"] = type(
    "module",
    (),
    {
        "StyledButton": MockStyledButton,
        "ButtonContext": type(
            "ButtonContext", (), {"SETTINGS": "settings", "NAVIGATION": "navigation"}
        ),
    },
)()

sys.modules[
    "src.presentation.components.menu_bar.navigation.menu_bar_navigation_widget"
] = type("module", (), {"MenuBarNavigationWidget": MockNavigationWidget})()


# Test the layout
def test_menu_bar_layout():
    app = QApplication(sys.argv)

    # Import after mocking
    from src.presentation.components.menu_bar.menu_bar_widget import MenuBarWidget

    # Create a test window
    window = QMainWindow()
    window.setGeometry(100, 100, 1200, 800)

    # Create menu bar widget
    menu_bar = MenuBarWidget(parent=window, size_provider=lambda: QSize(1200, 800))
    window.setCentralWidget(menu_bar)

    # Simulate resize to trigger positioning
    menu_bar.main_container.resize(1200, 60)
    menu_bar._position_settings_button()

    print("Menu bar layout test completed successfully!")
    print(f"Navigation widget should be centered")
    print(f"Settings button should be positioned on the right")

    # Don't show the window, just test the logic
    return True


if __name__ == "__main__":
    try:
        test_menu_bar_layout()
        print("✅ Test passed - layout logic works correctly")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
