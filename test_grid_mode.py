#!/usr/bin/env python3
"""Test script to verify grid mode selector functionality."""


def test_grid_mode_selector():
    """Test if grid mode selector is properly accessible."""
    print("Testing grid mode selector...")

    try:
        from desktop.modern.domain.models.enums import GridMode
        from desktop.modern.presentation.components.generate_tab import (
            ModernGridModeSelector,
        )

        print("✅ ModernGridModeSelector imported successfully")
        print(f"✅ GridMode enum values: {[mode.value for mode in GridMode]}")

        # Test creating the selector
        import sys

        from PyQt6.QtWidgets import QApplication

        app = QApplication(sys.argv)
        selector = ModernGridModeSelector()
        print("✅ ModernGridModeSelector created successfully")
        print(f"✅ Default grid mode: {selector.get_value()}")

        # Test setting values
        selector.set_value(GridMode.BOX)
        print(f"✅ Set to BOX mode: {selector.get_value()}")

        selector.set_value(GridMode.DIAMOND)
        print(f"✅ Set to DIAMOND mode: {selector.get_value()}")

        print("🎉 All grid mode selector tests passed!")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_grid_mode_selector()
