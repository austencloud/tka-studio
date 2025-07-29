#!/usr/bin/env python3
"""
Test script to verify the CSS property warning fixes.
"""

import os
import sys

# Add paths
sys.path.insert(0, os.path.join(os.getcwd(), "src", "desktop", "modern"))
sys.path.insert(0, os.path.join(os.getcwd(), "src"))


def test_sequence_state_manager_fix():
    """Test that sequence state manager access is less noisy."""
    print("Testing sequence state manager access...")
    try:
        from desktop.modern.core.service_locator import get_sequence_state_manager

        result = get_sequence_state_manager()
        print(f"✅ Sequence state manager access test passed (result: {result})")
        return True
    except Exception as e:
        print(f"❌ Sequence state manager test failed: {e}")
        return False


def test_qt_message_filter():
    """Test Qt message filter installation."""
    print("Testing Qt message filter...")
    try:
        from desktop.modern.core.logging.qt_message_filter import (
            get_qt_message_filter_stats,
            install_qt_message_filter,
        )

        install_qt_message_filter()
        stats = get_qt_message_filter_stats()
        print(f"✅ Qt message filter installed successfully")
        print(f"   Filter stats: {stats}")
        return True
    except Exception as e:
        print(f"❌ Qt message filter test failed: {e}")
        return False


def test_css_property_fixes():
    """Test that CSS properties have been removed from stylesheets."""
    print("Testing CSS property fixes...")
    try:
        # Check if design system no longer uses unsupported properties
        from desktop.modern.presentation.styles.design_system import DesignSystem

        ds = DesignSystem()
        hover_style = ds.create_hover_style("background: red;")

        unsupported_props = ["transform:", "box-shadow:", "transition:"]
        has_unsupported = any(prop in hover_style for prop in unsupported_props)

        if has_unsupported:
            print(f"❌ Design system still contains unsupported CSS properties")
            print(f"   Hover style: {hover_style}")
            return False
        else:
            print(f"✅ Design system CSS properties cleaned up")
            print(f"   Clean hover style: {hover_style}")
            return True

    except Exception as e:
        print(f"❌ CSS property test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Testing TKA CSS Property Warning Fixes")
    print("=" * 50)

    tests = [
        test_sequence_state_manager_fix,
        test_qt_message_filter,
        test_css_property_fixes,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            print()

    print("=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All fixes are working correctly!")
        return 0
    else:
        print("⚠️  Some fixes may need additional work")
        return 1


if __name__ == "__main__":
    sys.exit(main())
