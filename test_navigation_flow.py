#!/usr/bin/env python3
"""
Test Navigation Flow

This script tests the start position picker navigation flow to see if the
transition to option picker is working correctly.
"""

import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configure logging to see debug output
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_navigation_flow():
    """Test the navigation flow from start position picker to option picker."""
    print("🚀 TESTING NAVIGATION FLOW")
    print("=" * 50)

    try:
        from PyQt6.QtCore import QTimer
        from PyQt6.QtWidgets import QApplication

        # Ensure QApplication exists
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        # Import the main window from main.py
        from desktop.modern.core.dependency_injection.di_container import get_container
        from desktop.modern.main import TKAMainWindow

        print("✅ Creating main window...")
        container = get_container()
        main_window = TKAMainWindow(container=container)
        main_window.show()

        print("✅ Main window created and shown")

        # Get the construct tab
        construct_tab = main_window.tab_widget.construct_tab
        print(f"✅ Got construct tab: {type(construct_tab)}")

        # Get the start position picker
        start_pos_picker = construct_tab.layout_manager.start_position_picker
        print(f"✅ Got start position picker: {type(start_pos_picker)}")

        # Get the signal coordinator
        signal_coordinator = construct_tab.signal_coordinator
        print(f"✅ Got signal coordinator: {type(signal_coordinator)}")

        # Test signal emission
        def test_position_selection():
            print("🔧 Testing position selection...")
            test_position = "alpha1_alpha1"

            # Emit the signal
            print(f"📡 Emitting start_position_selected signal: {test_position}")
            start_pos_picker.start_position_selected.emit(test_position)

            # Check if we're on the option picker after a delay
            QTimer.singleShot(2000, check_navigation_result)

        def check_navigation_result():
            print("🔍 Checking navigation result...")

            # Check current stack index
            current_index = construct_tab.layout_manager.picker_stack.currentIndex()
            print(f"📊 Current stack index: {current_index}")

            if current_index == 1:  # Option picker index
                print("✅ SUCCESS: Navigation to option picker worked!")
            else:
                print("❌ FAILED: Still on start position picker")

            # Exit the application
            app.quit()

        # Start the test after a short delay
        QTimer.singleShot(1000, test_position_selection)

        # Run the application
        print("🏃 Running application...")
        app.exec()

        return True

    except Exception as e:
        print(f"❌ Navigation flow test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_navigation_flow()
    sys.exit(0 if success else 1)
