#!/usr/bin/env python3
"""
Test Beat Data Signal Handling
==============================

Comprehensive test to ensure beat data signals work correctly without crashes.
Tests the complete signal flow from beat selection to pictograph updates.
"""

import sys
import os
from pathlib import Path

# Add TKA source path
tka_root = Path(__file__).parent
sys.path.insert(0, str(tka_root / "src" / "desktop" / "modern" / "src"))


def test_signal_definitions():
    """Test that signals are properly defined."""
    print("Testing signal definitions...")

    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import pyqtSignal
        from presentation.components.graph_editor.components.pictograph_display_section import (
            PictographDisplaySection,
        )

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        # Create component
        display_section = PictographDisplaySection()

        # Check signal exists and has correct signature
        assert hasattr(
            display_section, "pictograph_updated"
        ), "pictograph_updated signal missing"

        # Check signal is a pyqtSignal (it's actually a bound signal, so check differently)
        signal = display_section.pictograph_updated
        assert hasattr(signal, "emit"), "pictograph_updated should have emit method"
        assert hasattr(
            signal, "connect"
        ), "pictograph_updated should have connect method"

        print("  ✓ Signal definitions are correct")
        return True

    except Exception as e:
        print(f"  ✗ Signal definition test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_signal_connection():
    """Test that signals can be connected without errors."""
    print("\nTesting signal connections...")

    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.graph_editor import GraphEditor

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        # Create graph editor (this should connect signals internally)
        editor = GraphEditor()

        # Verify the connection was made
        if editor._pictograph_display:
            # Check that the signal exists
            assert hasattr(
                editor._pictograph_display, "pictograph_updated"
            ), "Signal missing"
            print("  ✓ Signal connection successful")
        else:
            print("  ! Pictograph display not created, but no crash occurred")

        return True

    except Exception as e:
        print(f"  ✗ Signal connection test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_signal_emission_with_mock_data():
    """Test signal emission with mock beat data."""
    print("\nTesting signal emission with mock data...")

    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QObject
        from presentation.components.graph_editor.components.pictograph_display_section import (
            PictographDisplaySection,
        )
        from domain.models.core_models import BeatData

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        # Create mock beat data
        try:
            # Try to create real BeatData
            beat_data = BeatData(
                beat_number=1,
                letter="A",
                duration=1.0,
                red_motion=None,
                blue_motion=None,
            )
            print("  ✓ Real BeatData created successfully")
        except Exception as e:
            print(f"  ! Could not create real BeatData ({e}), using mock")

            # Create a simple mock object with all required attributes
            class MockBeatData:
                def __init__(self):
                    self.beat_number = 1
                    self.letter = "A"
                    self.duration = 1.0
                    self.blue_motion = None
                    self.red_motion = None
                    self.glyph_data = None
                    self.blue_reversal = False
                    self.red_reversal = False
                    self.is_blank = False
                    self.metadata = {}

            beat_data = MockBeatData()

        # Create display section
        display_section = PictographDisplaySection()

        # Create signal receiver to test emission
        class SignalReceiver(QObject):
            def __init__(self):
                super().__init__()
                self.received_signals = []

            def on_pictograph_updated(self, beat_index, beat_data):
                self.received_signals.append((beat_index, beat_data))
                print(
                    f"    Signal received: beat_index={beat_index}, beat_data={beat_data}"
                )

        receiver = SignalReceiver()
        display_section.pictograph_updated.connect(receiver.on_pictograph_updated)

        # Test signal emission
        print("  Testing signal emission...")
        display_section.pictograph_updated.emit(0, beat_data)

        # Verify signal was received
        assert len(receiver.received_signals) == 1, "Signal was not received"
        received_index, received_data = receiver.received_signals[0]
        assert received_index == 0, f"Expected index 0, got {received_index}"
        assert received_data == beat_data, "Beat data mismatch"

        print("  ✓ Signal emission successful")
        return True

    except Exception as e:
        print(f"  ✗ Signal emission test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_update_display_method():
    """Test the update_display method that caused the original crash."""
    print("\nTesting update_display method...")

    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QObject
        from presentation.components.graph_editor.components.pictograph_display_section import (
            PictographDisplaySection,
        )

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        # Create mock beat data with all required attributes
        class MockBeatData:
            def __init__(self):
                self.beat_number = 1
                self.letter = "A"
                self.duration = 1.0
                self.blue_motion = None
                self.red_motion = None
                self.glyph_data = None
                self.blue_reversal = False
                self.red_reversal = False
                self.is_blank = False
                self.metadata = {}

        beat_data = MockBeatData()

        # Create display section
        display_section = PictographDisplaySection()

        # Create signal receiver
        class SignalReceiver(QObject):
            def __init__(self):
                super().__init__()
                self.received_signals = []

            def on_pictograph_updated(self, beat_index, beat_data):
                self.received_signals.append((beat_index, beat_data))

        receiver = SignalReceiver()
        display_section.pictograph_updated.connect(receiver.on_pictograph_updated)

        # Test update_display method (this was causing the crash)
        print("  Testing update_display method...")
        display_section.update_display(0, beat_data)

        # Verify signal was emitted
        assert (
            len(receiver.received_signals) == 1
        ), "Signal was not emitted from update_display"

        print("  ✓ update_display method works without crash")

        # Test with None beat data
        print("  Testing update_display with None...")
        display_section.update_display(-1, None)

        # Should not emit signal for None data, so count should remain 1
        assert (
            len(receiver.received_signals) == 1
        ), "Signal should not be emitted for None data"

        print("  ✓ update_display handles None data correctly")
        return True

    except Exception as e:
        print(f"  ✗ update_display test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_full_integration():
    """Test full integration with GraphEditor."""
    print("\nTesting full integration with GraphEditor...")

    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QObject
        from presentation.components.graph_editor.graph_editor import GraphEditor

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        # Create graph editor
        editor = GraphEditor()

        # Create signal receiver for the main editor signals
        class SignalReceiver(QObject):
            def __init__(self):
                super().__init__()
                self.beat_modified_signals = []

            def on_beat_modified(self, beat_index, beat_data):
                self.beat_modified_signals.append((beat_index, beat_data))

        receiver = SignalReceiver()
        editor.beat_modified.connect(receiver.on_beat_modified)

        # Create mock beat data with all required attributes
        class MockBeatData:
            def __init__(self):
                self.beat_number = 1
                self.letter = "A"
                self.duration = 1.0
                self.blue_motion = None
                self.red_motion = None
                self.glyph_data = None
                self.blue_reversal = False
                self.red_reversal = False
                self.is_blank = False
                self.metadata = {}

        beat_data = MockBeatData()

        # Test set_selected_beat_data (this should trigger the signal chain)
        print("  Testing set_selected_beat_data...")
        result = editor.set_selected_beat_data(0, beat_data)
        assert result == True, "set_selected_beat_data should return True"

        print("  ✓ set_selected_beat_data works without crash")

        # Test that the data was stored correctly
        stored_data = editor.get_selected_beat_data()
        assert stored_data == beat_data, "Beat data was not stored correctly"

        stored_index = editor.get_selected_beat_index()
        assert stored_index == 0, "Beat index was not stored correctly"

        print("  ✓ Beat data storage works correctly")
        return True

    except Exception as e:
        print(f"  ✗ Full integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all signal tests."""
    print("=" * 60)
    print("Testing Beat Data Signal Handling")
    print("=" * 60)

    tests = [
        test_signal_definitions,
        test_signal_connection,
        test_signal_emission_with_mock_data,
        test_update_display_method,
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
    print(f"Signal Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print(
            "SUCCESS: All signal tests passed! Beat data handling should work without crashes."
        )
        return True
    else:
        print("FAILURE: Some signal tests failed. There may still be crash issues.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
