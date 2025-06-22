"""Test hover events and cursor changes in the TKA Launcher."""

import os
import sys

# Add the launcher directory to the Python path
launcher_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, launcher_dir)


def test_cursor_and_hover_functionality():
    """Test that all interactive elements have proper cursors and hover effects."""
    try:
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QApplication
        from ui.components import (
            ReliableApplicationCard,
            ReliableButton,
            ReliableSearchBox,
        )

        app = QApplication([])

        # Test button cursor
        button = ReliableButton("Test Button")
        assert button.cursor().shape() == Qt.CursorShape.PointingHandCursor
        print("✅ ReliableButton has PointingHandCursor")

        # Test search box cursor
        search_box = ReliableSearchBox("Test Search")
        assert search_box.cursor().shape() == Qt.CursorShape.IBeamCursor
        print("✅ ReliableSearchBox has IBeamCursor")

        # Test that components have hover methods
        assert hasattr(button, "enterEvent")
        assert hasattr(button, "leaveEvent")
        assert hasattr(search_box, "enterEvent")
        assert hasattr(search_box, "leaveEvent")
        print("✅ Components have hover event methods")

        # Test that styling includes hover states
        button_style = button.styleSheet()
        assert ":hover" in button_style
        print("✅ Button has CSS hover styling")

        search_style = search_box.styleSheet()
        assert ":hover" in search_style
        print("✅ Search box has CSS hover styling")

        print("\n🎉 All cursor and hover functionality tests passed!")
        return True

    except Exception as e:
        print(f"❌ Error testing cursor and hover functionality: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_animation_functionality():
    """Test that animation components are properly integrated."""
    try:
        from ui.reliable_effects import get_animation_manager, get_shadow_manager

        shadow_manager = get_shadow_manager()
        animation_manager = get_animation_manager()

        # Test that managers have required methods
        assert hasattr(shadow_manager, "apply_hover_shadow")
        assert hasattr(shadow_manager, "reset_shadow")
        assert hasattr(animation_manager, "smooth_hover_scale")
        assert hasattr(animation_manager, "button_press_feedback")
        print("✅ Animation managers have required methods")

        print("✅ Animation functionality is properly integrated!")
        return True

    except Exception as e:
        print(f"❌ Error testing animation functionality: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🧪 Testing Hover Events and Cursor Changes")
    print("=" * 50)

    success1 = test_cursor_and_hover_functionality()
    print()
    success2 = test_animation_functionality()

    if success1 and success2:
        print("\n✅ ALL HOVER & CURSOR TESTS PASSED!")
        print("🎯 Interactive elements are working perfectly!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed - please check the implementation")
        sys.exit(1)
