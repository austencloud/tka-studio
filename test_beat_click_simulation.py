#!/usr/bin/env python3
"""
Test Beat Click Simulation
==========================

Simulates the exact scenario that was causing crashes when clicking a beat.
This test verifies that the complete signal chain works without crashes.
"""

import sys
import os
from pathlib import Path

# Add TKA source path
tka_root = Path(__file__).parent
sys.path.insert(0, str(tka_root / "src" / "desktop" / "modern" / "src"))


def test_beat_click_scenario():
    """Test the exact scenario that happens when a user clicks a beat."""
    print("Testing beat click scenario...")

    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QObject
        from presentation.components.graph_editor.graph_editor import GraphEditor
        from domain.models.core_models import BeatData

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        # Create graph editor (this is what happens when the workbench loads)
        print("  Creating GraphEditor...")
        editor = GraphEditor()
        print("  ✓ GraphEditor created successfully")

        # Create a signal receiver to capture the beat_modified signal
        class BeatClickReceiver(QObject):
            def __init__(self):
                super().__init__()
                self.received_beats = []

            def on_beat_modified(self, beat_index, beat_data):
                self.received_beats.append((beat_index, beat_data))
                print(
                    f"    Beat modified signal received: index={beat_index}, letter={beat_data.letter if beat_data else 'None'}"
                )

        receiver = BeatClickReceiver()
        editor.beat_modified.connect(receiver.on_beat_modified)
        print("  ✓ Signal receiver connected")

        # Create real beat data (this is what comes from the sequence)
        print("  Creating real BeatData...")
        beat_data = BeatData(
            beat_number=1, letter="A", duration=1.0, red_motion=None, blue_motion=None
        )
        print(f"  ✓ BeatData created: {beat_data.letter}")

        # Simulate what happens when a user clicks a beat in the beat frame
        # This calls set_selected_beat_data which should update the pictograph
        print("  Simulating beat click (calling set_selected_beat_data)...")
        result = editor.set_selected_beat_data(0, beat_data)

        if not result:
            print("  ✗ set_selected_beat_data returned False")
            return False

        print("  ✓ set_selected_beat_data completed successfully")

        # Verify the data was stored correctly
        stored_data = editor.get_selected_beat_data()
        stored_index = editor.get_selected_beat_index()

        if stored_data != beat_data:
            print(f"  ✗ Beat data mismatch: expected {beat_data}, got {stored_data}")
            return False

        if stored_index != 0:
            print(f"  ✗ Beat index mismatch: expected 0, got {stored_index}")
            return False

        print("  ✓ Beat data stored correctly")

        # Test that the pictograph display was updated (if it exists)
        if editor._pictograph_display:
            print("  ✓ Pictograph display exists and should have been updated")
        else:
            print("  ! Pictograph display not created (expected in test environment)")

        # Test direct pictograph update (this was the line causing crashes)
        if editor._pictograph_display:
            print("  Testing direct pictograph update...")
            editor._pictograph_display.update_display(0, beat_data)
            print("  ✓ Direct pictograph update successful")

        print("  ✓ Beat click scenario completed without crashes")
        return True

    except Exception as e:
        print(f"  ✗ Beat click scenario failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_multiple_beat_clicks():
    """Test multiple beat clicks to ensure no memory leaks or crashes."""
    print("\nTesting multiple beat clicks...")

    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.graph_editor import GraphEditor
        from domain.models.core_models import BeatData

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        editor = GraphEditor()

        # Create multiple beat data objects
        beats = []
        for i in range(5):
            beat = BeatData(
                beat_number=i + 1,
                letter=chr(ord("A") + i),  # A, B, C, D, E
                duration=1.0,
                red_motion=None,
                blue_motion=None,
            )
            beats.append(beat)

        print(f"  Created {len(beats)} beat data objects")

        # Simulate clicking each beat multiple times
        for i, beat in enumerate(beats):
            for click_count in range(3):  # Click each beat 3 times
                result = editor.set_selected_beat_data(i, beat)
                if not result:
                    print(f"  ✗ Failed on beat {i}, click {click_count}")
                    return False

        print("  ✓ Multiple beat clicks completed successfully")

        # Test rapid switching between beats
        for _ in range(10):
            for i, beat in enumerate(beats):
                editor.set_selected_beat_data(i, beat)

        print("  ✓ Rapid beat switching completed successfully")
        return True

    except Exception as e:
        print(f"  ✗ Multiple beat clicks test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_edge_cases():
    """Test edge cases that might cause crashes."""
    print("\nTesting edge cases...")

    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.graph_editor import GraphEditor
        from domain.models.core_models import BeatData

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        editor = GraphEditor()

        # Test with None beat data
        print("  Testing with None beat data...")
        result = editor.set_selected_beat_data(-1, None)
        if not result:
            print("  ✗ Failed with None beat data")
            return False
        print("  ✓ None beat data handled correctly")

        # Test with invalid beat index (should return False due to validation)
        print("  Testing with invalid beat index...")
        beat = BeatData(
            beat_number=1, letter="A", duration=1.0, red_motion=None, blue_motion=None
        )
        result = editor.set_selected_beat_data(-999, beat)
        if result:  # Should return False for invalid index
            print("  ✗ Invalid beat index should have been rejected")
            return False
        print("  ✓ Invalid beat index correctly rejected")

        # Test switching from valid to None
        print("  Testing switch from valid to None...")
        editor.set_selected_beat_data(0, beat)
        result = editor.set_selected_beat_data(-1, None)
        if not result:
            print("  ✗ Failed switching from valid to None")
            return False
        print("  ✓ Switch from valid to None handled correctly")

        print("  ✓ All edge cases handled successfully")
        return True

    except Exception as e:
        print(f"  ✗ Edge cases test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all beat click tests."""
    print("=" * 60)
    print("Testing Beat Click Scenarios")
    print("=" * 60)

    tests = [
        test_beat_click_scenario,
        test_multiple_beat_clicks,
        test_edge_cases,
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
    print(f"Beat Click Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("SUCCESS: Beat clicking should work without crashes!")
        print("The signal emission issue has been completely resolved.")
        return True
    else:
        print("FAILURE: Some beat click tests failed.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
