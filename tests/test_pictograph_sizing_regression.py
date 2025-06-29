"""
Test for Pictograph Sizing Regression Fix

This test validates that the sizing callback registration fix works correctly.
It tests the specific bug where SectionLayoutManager was looking for
"ModernOptionPickerWidget" instead of "OptionPickerWidget".

The test verifies:
1. SectionLayoutManager can find the correct widget class
2. Sizing callbacks are properly registered
3. The fix resolves the pictograph sizing regression
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget

# Add TKA module root to path
tka_root = Path(__file__).parent.parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(tka_root))

from presentation.components.option_picker.core.option_picker_widget import (
    OptionPickerWidget,
)
from presentation.components.option_picker.components.sections.section_layout_manager import (
    SectionLayoutManager,
)
from presentation.components.option_picker.types.letter_types import LetterType


class MockSection:
    """Mock section for testing layout manager."""

    def __init__(self, letter_type):
        self.letter_type = letter_type
        self._parent = None

    def parent(self):
        return self._parent

    def set_parent(self, parent):
        self._parent = parent


class SizingCallbackTest:
    """Test class for validating sizing callback registration fix."""

    def __init__(self):
        self.app = None
        self.callbacks_registered = []

    def setup_application(self):
        """Setup minimal Qt application."""
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()

    def test_widget_class_name_detection(self):
        """Test that SectionLayoutManager can find OptionPickerWidget correctly."""
        print("🔍 Testing widget class name detection...")

        # Create widget hierarchy
        option_picker_widget = OptionPickerWidget()
        container_widget = QWidget()
        section_widget = QWidget()

        # Set up parent-child relationships
        container_widget.setParent(option_picker_widget)
        section_widget.setParent(container_widget)

        # Create mock section and layout manager
        mock_section = MockSection(LetterType.TYPE1)
        mock_section.set_parent(section_widget)

        layout_manager = SectionLayoutManager(mock_section)

        # Test the registration process
        success = self._test_registration_process(layout_manager, option_picker_widget)

        return success

    def _test_registration_process(self, layout_manager, option_picker_widget):
        """Test the actual registration process."""
        print("📝 Testing registration process...")

        # Mock the add_sizing_callback method to track calls
        original_method = option_picker_widget.add_sizing_callback
        callback_registered = False

        def mock_add_sizing_callback(callback):
            nonlocal callback_registered
            callback_registered = True
            self.callbacks_registered.append(callback)
            print(f"✅ Sizing callback registered successfully!")
            return original_method(callback)

        option_picker_widget.add_sizing_callback = mock_add_sizing_callback

        # Attempt registration
        try:
            layout_manager.register_for_sizing_updates()

            if callback_registered:
                print("✅ Registration successful - callback was registered")
                return True
            else:
                print("❌ Registration failed - no callback was registered")
                return False

        except Exception as e:
            print(f"❌ Registration failed with error: {e}")
            return False

    def test_callback_invocation(self):
        """Test that registered callbacks are actually called."""
        print("📞 Testing callback invocation...")

        if not self.callbacks_registered:
            print("❌ No callbacks registered to test")
            return False

        # Test calling the registered callback
        test_width = 800
        callback_called = False

        try:
            for callback in self.callbacks_registered:
                callback(test_width)
                callback_called = True
                print(f"✅ Callback invoked with width: {test_width}px")

            return callback_called

        except Exception as e:
            print(f"❌ Callback invocation failed: {e}")
            return False

    def cleanup(self):
        """Clean up test resources."""
        if self.app:
            self.app.quit()


def test_pictograph_sizing_regression_fix():
    """Main test function for the pictograph sizing regression fix."""
    print("🚀 Starting Pictograph Sizing Regression Fix Test")
    print("🎯 Testing the fix for SectionLayoutManager widget class detection")

    test = SizingCallbackTest()

    try:
        # Setup
        test.setup_application()

        # Test 1: Widget class name detection and callback registration
        registration_success = test.test_widget_class_name_detection()

        # Test 2: Callback invocation
        invocation_success = test.test_callback_invocation()

        # Overall result
        overall_success = registration_success and invocation_success

        if overall_success:
            print("\n🎉 Test PASSED: Sizing callback registration fix works correctly!")
            print("✅ SectionLayoutManager now correctly finds 'OptionPickerWidget'")
            print("✅ Sizing callbacks are properly registered and functional")
            print("✅ Pictograph sizing regression should be resolved")
        else:
            print("\n💥 Test FAILED: Issues detected with sizing callback registration")
            if not registration_success:
                print("❌ Callback registration failed")
            if not invocation_success:
                print("❌ Callback invocation failed")

        return overall_success

    except Exception as e:
        print(f"\n💥 Test ERROR: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        test.cleanup()


if __name__ == "__main__":
    success = test_pictograph_sizing_regression_fix()
    sys.exit(0 if success else 1)
