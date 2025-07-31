#!/usr/bin/env python3
"""
Debug script for start position selection issue.
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication


def debug_start_position_selection():
    """Debug the start position selection issue."""
    print("🔍 DEBUG: Starting start position selection debug...")

    try:
        # Create application using our simplified main.py
        from desktop.modern.core.application.application_factory import (
            ApplicationFactory,
        )
        from desktop.modern.presentation.main_window import TKAMainWindow

        # Create Qt app
        app = QApplication.instance() or QApplication([])

        # Create container
        container = ApplicationFactory.create_app("production")

        # Create main window
        window = TKAMainWindow(container)
        window.show()

        print("✅ DEBUG: Application created and shown")

        # Wait for initialization
        QTest.qWait(3000)
        print("✅ DEBUG: Initialization wait completed")

        # Find the construct tab and start position picker
        tab_widget = window.tab_widget
        if not tab_widget:
            print("❌ DEBUG: No tab widget found!")
            return False

        print(f"✅ DEBUG: Found tab widget with {tab_widget.count()} tabs")

        # Navigate to construct tab (should be index 0)
        tab_widget.setCurrentIndex(0)
        QTest.qWait(1000)
        print("✅ DEBUG: Navigated to construct tab")

        # Get the construct tab widget
        construct_tab = tab_widget.currentWidget()
        if not construct_tab:
            print("❌ DEBUG: No construct tab widget found!")
            return False

        print("✅ DEBUG: Found construct tab widget")

        # Find start position picker
        from desktop.modern.presentation.components.start_position_picker.start_position_picker import (
            StartPositionPicker,
        )

        start_position_picker = construct_tab.findChild(StartPositionPicker)
        if not start_position_picker:
            print("❌ DEBUG: No start position picker found!")
            # Try to find it by searching all children
            all_children = construct_tab.findChildren(StartPositionPicker)
            print(f"🔍 DEBUG: Found {len(all_children)} StartPositionPicker children")
            return False

        print("✅ DEBUG: Found start position picker")

        # Get available start positions
        positions = start_position_picker.get_available_positions()
        if not positions:
            print("❌ DEBUG: No start positions available!")
            return False

        print(f"✅ DEBUG: Found {len(positions)} start positions: {positions[:5]}...")

        # Try to select the first position
        test_position = positions[0]
        print(f"🎯 DEBUG: Attempting to select position: {test_position}")

        # Simulate clicking the position
        success = start_position_picker.select_position(test_position)
        if not success:
            print(f"❌ DEBUG: Failed to select position: {test_position}")
            return False

        print(f"✅ DEBUG: Successfully selected position: {test_position}")

        # Wait for UI updates
        QTest.qWait(2000)

        # Check if the beat frame was updated
        workbench = construct_tab.findChild(
            object, "workbench"
        )  # Try to find workbench
        if workbench:
            print("✅ DEBUG: Found workbench")
            # Check if start position is set
            start_pos = getattr(workbench, "get_start_position", lambda: None)()
            if start_pos:
                print(f"✅ DEBUG: Start position is set in workbench: {start_pos}")
            else:
                print("❌ DEBUG: Start position is NOT set in workbench!")
        else:
            print("❌ DEBUG: Could not find workbench")

        return True

    except Exception as e:
        print(f"❌ DEBUG: Error during debug: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = debug_start_position_selection()
    if success:
        print("✅ DEBUG: Debug completed successfully")
    else:
        print("❌ DEBUG: Debug failed")
        sys.exit(1)
