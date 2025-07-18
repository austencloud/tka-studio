#!/usr/bin/env python3
"""
Test script to verify component-specific view sizes
"""
import os
import sys

# Add the modern desktop source to Python path
modern_src = os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
if modern_src not in sys.path:
    sys.path.insert(0, modern_src)

from PyQt6.QtWidgets import QApplication


def ensure_qt_app():
    """Ensure QApplication is initialized."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_view_sizes():
    """Test that component-specific views are correctly sized"""
    print("🔍 Testing component-specific view sizes...")

    ensure_qt_app()

    try:
        from presentation.components.pictograph.component_specific_view_pools import (
            get_beat_frame_view_pool,
            get_option_picker_view_pool,
            get_start_position_picker_view_pool,
            initialize_component_view_pools,
        )

        # Initialize pools
        initialize_component_view_pools()

        # Test option picker view size (120x120)
        option_pool = get_option_picker_view_pool()
        option_view = option_pool.checkout_view()
        option_size = option_view.size()
        print(f"Option picker view size: {option_size.width()}x{option_size.height()}")
        print(f"Expected: 120x120")
        option_pass = option_size.width() == 120 and option_size.height() == 120
        print(f'Option picker size test: {"PASS" if option_pass else "FAIL"}')
        option_pool.checkin_view(option_view)

        # Test beat frame view size (150x150)
        beat_pool = get_beat_frame_view_pool()
        beat_view = beat_pool.checkout_view()
        beat_size = beat_view.size()
        print(f"Beat frame view size: {beat_size.width()}x{beat_size.height()}")
        print(f"Expected: 150x150")
        beat_pass = beat_size.width() == 150 and beat_size.height() == 150
        print(f'Beat frame size test: {"PASS" if beat_pass else "FAIL"}')
        beat_pool.checkin_view(beat_view)

        # Test start position view size (100x100)
        start_pool = get_start_position_picker_view_pool()
        start_view = start_pool.checkout_view()
        start_size = start_view.size()
        print(f"Start position view size: {start_size.width()}x{start_size.height()}")
        print(f"Expected: 100x100")
        start_pass = start_size.width() == 100 and start_size.height() == 100
        print(f'Start position size test: {"PASS" if start_pass else "FAIL"}')
        start_pool.checkin_view(start_view)

        all_pass = option_pass and beat_pass and start_pass
        print(f'\n🎯 ALL SIZE TESTS: {"PASS" if all_pass else "FAIL"}')

        return all_pass

    except Exception as e:
        print(f"❌ Size test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_view_sizes()
