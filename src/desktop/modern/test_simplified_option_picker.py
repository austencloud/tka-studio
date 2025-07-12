#!/usr/bin/env python3
"""
Test Script for Simplified Option Picker

This script tests the simplified option picker to ensure it:
1. Can be instantiated without errors
2. Displays 36 options correctly distributed across 6 sections
3. Handles section toggling properly
4. Maintains proper layout behavior like the Legacy version

Run this script to validate the simplified option picker implementation.
"""

import os
import sys

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


def test_simplified_option_picker():
    """Test the simplified option picker implementation."""

    print("🧪 Testing Simplified Option Picker...")

    # Create QApplication
    app = QApplication(sys.argv)

    try:
        # Import our simplified components directly to avoid package import issues
        from presentation.components.option_picker.core.option_factory import (
            OptionFactory,
        )
        from presentation.components.option_picker.core.simplified_option_picker_widget import (
            SimplifiedOptionPickerWidget,
        )

        print("✅ Successfully imported simplified components")

        # Create a test window
        window = QMainWindow()
        window.setWindowTitle("Simplified Option Picker Test")
        window.setGeometry(100, 100, 1000, 800)

        # Create central widget
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create size provider that simulates main window size
        def size_provider():
            # Simulate a realistic main window size (1200x800)
            return QSize(1200, 800)

        # Create simplified option picker widget
        print("🏗️ Creating OptionPickerWidget...")
        option_picker_widget = SimplifiedOptionPickerWidget(
            parent=central_widget, mw_size_provider=size_provider
        )

        print("✅ Successfully created OptionPickerWidget")

        # Create factory
        print("🏗️ Creating SimplifiedOptionFactory...")
        factory = OptionFactory(
            parent_widget=central_widget, mw_size_provider=size_provider
        )

        print("✅ Successfully created SimplifiedOptionFactory")

        # Initialize widget with factory
        print("🔗 Initializing widget with factory...")
        option_picker_widget.initialize_with_factory(factory)

        print("✅ Successfully initialized widget with factory")

        # Add to layout
        layout.addWidget(option_picker_widget)

        # Test section count
        sections = option_picker_widget.sections
        print(f"📊 Created {len(sections)} sections")

        if len(sections) == 6:
            print("✅ Correct number of sections (6)")
        else:
            print(f"❌ Expected 6 sections, got {len(sections)}")

        # Test factory and frames
        print(f"📦 Factory created {len(factory.option_pool)} frames")

        if len(factory.option_pool) == 36:
            print("✅ Correct number of frames (36)")
        else:
            print(f"❌ Expected 36 frames, got {len(factory.option_pool)}")

        # Test section types and sizing
        from presentation.components.option_picker.types.letter_types import LetterType

        groupable_count = 0
        individual_count = 0

        # Test sizing
        main_window_size = size_provider()
        expected_option_picker_width = main_window_size.width() // 2
        actual_option_picker_width = option_picker_widget.width()

        print(
            f"📐 Main window size: {main_window_size.width()}x{main_window_size.height()}"
        )
        print(f"📐 Expected option picker width: {expected_option_picker_width}")
        print(f"📐 Actual option picker width: {actual_option_picker_width}")

        for letter_type, section in sections.items():
            section_width = section.width()
            if section.is_groupable:
                groupable_count += 1
                expected_width = expected_option_picker_width // 3
                print(
                    f"📋 {letter_type}: Groupable section (width: {section_width}, expected: ~{expected_width})"
                )
            else:
                individual_count += 1
                expected_width = expected_option_picker_width
                print(
                    f"📋 {letter_type}: Individual section (width: {section_width}, expected: {expected_width})"
                )

        if individual_count == 3 and groupable_count == 3:
            print("✅ Correct section distribution (3 individual, 3 groupable)")
        else:
            print(
                f"❌ Expected 3 individual + 3 groupable, got {individual_count} + {groupable_count}"
            )

        # Show the window
        window.show()
        print("🖼️ Test window displayed")
        print(
            "👀 Visual inspection: Check that sections are visible and properly laid out"
        )
        print("🔄 Try clicking section headers to toggle visibility")
        print("❌ Close the window to complete the test")

        # Run the application
        return app.exec()

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = test_simplified_option_picker()
    sys.exit(exit_code)
