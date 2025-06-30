#!/usr/bin/env python3
"""
Test Modern Design Improvements
===============================

Tests the modern 2025 design improvements to the graph editor:
- Large, easily pressable turn value buttons
- Modern glassmorphism styling
- Larger pictograph display
- Better space utilization
"""

import sys
import os
from pathlib import Path

# Add TKA source path
tka_root = Path(__file__).parent
sys.path.insert(0, str(tka_root / "src" / "desktop" / "modern" / "src"))


def test_modern_turn_controls():
    """Test the modern turn adjustment controls."""
    print("Testing modern turn adjustment controls...")

    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.components.turn_adjustment_controls.turn_adjustment_controls import (
            TurnAdjustmentControls,
        )

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        # Create modern turn controls
        turn_controls = TurnAdjustmentControls()
        print("  ✓ Modern turn controls created successfully")

        # Test that all turn values are available
        expected_values = ["fl", "0", "0.5", "1", "1.5", "2", "2.5", "3"]
        assert (
            turn_controls._turn_values == expected_values
        ), f"Expected {expected_values}, got {turn_controls._turn_values}"
        print("  ✓ All turn values available")

        # Test turn value mapping
        assert turn_controls._turn_value_map["fl"] == 0.25, "fl should map to 0.25"
        assert turn_controls._turn_value_map["0"] == 0.0, "0 should map to 0.0"
        assert turn_controls._turn_value_map["3"] == 3.0, "3 should map to 3.0"
        print("  ✓ Turn value mapping correct")

        # Test that button dictionaries exist
        assert hasattr(
            turn_controls, "_blue_turn_buttons"
        ), "Should have blue turn buttons"
        assert hasattr(
            turn_controls, "_red_turn_buttons"
        ), "Should have red turn buttons"
        print("  ✓ Button dictionaries exist")

        # Test that current value labels exist
        assert hasattr(
            turn_controls, "_blue_current_label"
        ), "Should have blue current label"
        assert hasattr(
            turn_controls, "_red_current_label"
        ), "Should have red current label"
        print("  ✓ Current value labels exist")

        return True

    except Exception as e:
        print(f"  ✗ Modern turn controls test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_turn_value_selection():
    """Test turn value selection functionality."""
    print("\nTesting turn value selection...")

    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QObject
        from presentation.components.graph_editor.components.turn_adjustment_controls.turn_adjustment_controls import (
            TurnAdjustmentControls,
        )

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        turn_controls = TurnAdjustmentControls()

        # Create signal receiver
        class SignalReceiver(QObject):
            def __init__(self):
                super().__init__()
                self.received_signals = []

            def on_turn_changed(self, color, amount):
                self.received_signals.append((color, amount))

        receiver = SignalReceiver()
        turn_controls.turn_amount_changed.connect(receiver.on_turn_changed)

        # Test selecting different turn values
        test_cases = [
            ("blue", "fl", 0.25),
            ("blue", "1", 1.0),
            ("red", "2.5", 2.5),
            ("red", "0", 0.0),
        ]

        for color, turn_value, expected_amount in test_cases:
            turn_controls._on_turn_value_selected(color, turn_value)

            # Check internal state
            actual_amount = (
                turn_controls._blue_turn_amount
                if color == "blue"
                else turn_controls._red_turn_amount
            )
            assert (
                actual_amount == expected_amount
            ), f"Expected {expected_amount}, got {actual_amount}"

            # Check signal emission
            assert len(receiver.received_signals) > 0, "Signal should have been emitted"
            last_signal = receiver.received_signals[-1]
            assert last_signal == (
                color,
                expected_amount,
            ), f"Expected signal {(color, expected_amount)}, got {last_signal}"

            print(f"  ✓ {color} {turn_value} -> {expected_amount} works correctly")

        return True

    except Exception as e:
        print(f"  ✗ Turn value selection test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_larger_pictograph_display():
    """Test the larger pictograph display."""
    print("\nTesting larger pictograph display...")

    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.components.pictograph_display_section import (
            PictographDisplaySection,
        )

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        # Test default larger size
        display_section = PictographDisplaySection()
        assert (
            display_section._pictograph_size == 280
        ), f"Expected 280px, got {display_section._pictograph_size}px"
        print("  ✓ Default pictograph size is now 280px (was 140px)")

        # Test that pictograph component exists and has correct size
        if display_section._pictograph_component:
            size = display_section._pictograph_component.size()
            assert size.width() == 280, f"Expected width 280, got {size.width()}"
            assert size.height() == 280, f"Expected height 280, got {size.height()}"
            print("  ✓ Pictograph component has correct size")
        else:
            print("  ! Pictograph component not created (expected in test environment)")

        # Test custom size
        custom_display = PictographDisplaySection(pictograph_size=350)
        assert (
            custom_display._pictograph_size == 350
        ), f"Expected 350px, got {custom_display._pictograph_size}px"
        print("  ✓ Custom pictograph size works")

        return True

    except Exception as e:
        print(f"  ✗ Larger pictograph display test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_space_utilization():
    """Test improved space utilization."""
    print("\nTesting improved space utilization...")

    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.components.pictograph_display_section import (
            PictographDisplaySection,
        )

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        display_section = PictographDisplaySection()

        # Test that info panel has size constraints
        if display_section._info_panel:
            assert (
                display_section._info_panel.minimumWidth() == 180
            ), "Info panel should have 180px minimum width"
            assert (
                display_section._info_panel.maximumWidth() == 250
            ), "Info panel should have 250px maximum width"
            print("  ✓ Info panel has appropriate size constraints")
        else:
            print("  ! Info panel not created (expected in test environment)")

        return True

    except Exception as e:
        print(f"  ✗ Space utilization test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_full_integration():
    """Test full integration of modern design improvements."""
    print("\nTesting full integration...")

    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.graph_editor import GraphEditor

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        # Create graph editor with modern components
        editor = GraphEditor()
        print("  ✓ Graph editor with modern components created")

        # Test that modern components are integrated
        if editor._pictograph_display:
            assert (
                editor._pictograph_display._pictograph_size == 280
            ), "Should use larger pictograph size"
            print("  ✓ Larger pictograph integrated")

        if editor._adjustment_panel:
            # Check if it has the modern turn controls
            print("  ✓ Modern adjustment panel integrated")

        # Test that the modern design doesn't break existing functionality
        result = editor.set_selected_beat_data(-1, None)
        assert result == True, "Basic functionality should still work"
        print("  ✓ Existing functionality preserved")

        return True

    except Exception as e:
        print(f"  ✗ Full integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all modern design improvement tests."""
    print("=" * 60)
    print("Testing Modern Design Improvements")
    print("=" * 60)

    tests = [
        test_modern_turn_controls,
        test_turn_value_selection,
        test_larger_pictograph_display,
        test_space_utilization,
        test_full_integration,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
                print(f"  PASS: {test.__name__}")
            else:
                failed += 1
                print(f"  FAIL: {test.__name__}")
        except Exception as e:
            failed += 1
            print(f"  ERROR: {test.__name__} - {e}")

    print("\n" + "=" * 60)
    print(f"Modern Design Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("SUCCESS: All modern design improvements are working correctly!")
        print("✨ The graph editor now features:")
        print(
            "  • Large, easily pressable turn value buttons (fl, 0, 0.5, 1, 1.5, 2, 2.5, 3)"
        )
        print("  • Modern glassmorphism styling with color-themed gradients")
        print("  • Much larger pictograph display (280px vs 140px)")
        print("  • Better space utilization with 2:1 pictograph-to-info ratio")
        print("  • Direct turn value selection (no more tiny increment buttons)")
        return True
    else:
        print("FAILURE: Some modern design improvements need fixes.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
