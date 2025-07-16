#!/usr/bin/env python3
"""
Direct test of delete beat functionality without UI dependencies.
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from application.services.sequence.sequence_beat_operations import (
    SequenceBeatOperations,
)
from application.services.workbench.workbench_operation_coordinator import (
    WorkbenchOperationCoordinator,
)
from application.services.workbench.workbench_state_manager import WorkbenchStateManager
from domain.models.beat_data import BeatData
from domain.models.sequence_data import SequenceData


def test_delete_beat_service_directly():
    """Test the delete beat service directly."""
    print("🧪 [DIRECT_TEST] Testing delete beat service directly...")

    try:
        # Create test sequence
        beats = [
            BeatData(beat_number=1, metadata={"letter": "J"}),
            BeatData(beat_number=2, metadata={"letter": "θ"}),
            BeatData(beat_number=3, metadata={"letter": "X"}),
            BeatData(beat_number=4, metadata={"letter": "Σ"}),
            BeatData(beat_number=5, metadata={"letter": "W"}),
        ]

        test_sequence = SequenceData(
            id="delete_test", beats=beats, start_position="beta3"
        )

        print(
            f"📝 [DIRECT_TEST] Original sequence: {[beat.letter for beat in test_sequence.beats]}"
        )

        # Create beat operations service
        beat_operations = SequenceBeatOperations()

        # Test delete beat at index 2 (X) and all following
        print("🗑️ [DIRECT_TEST] Deleting beat at index 2 and all following...")
        updated_sequence = beat_operations.delete_beat(test_sequence, 2)

        remaining_letters = [beat.letter for beat in updated_sequence.beats]
        print(f"✅ [DIRECT_TEST] Result: {remaining_letters}")

        # Should have 2 beats remaining (J, θ)
        expected = ["J", "θ"]
        if remaining_letters == expected:
            print("✅ [DIRECT_TEST] Delete beat service working correctly!")
            return True
        else:
            print(f"❌ [DIRECT_TEST] Expected {expected}, got {remaining_letters}")
            return False

    except Exception as e:
        print(f"❌ [DIRECT_TEST] Service test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_operation_coordinator_directly():
    """Test the operation coordinator directly."""
    print("🧪 [DIRECT_TEST] Testing operation coordinator directly...")

    try:
        # Create test sequence
        beats = [
            BeatData(beat_number=1, metadata={"letter": "J"}),
            BeatData(beat_number=2, metadata={"letter": "θ"}),
            BeatData(beat_number=3, metadata={"letter": "X"}),
            BeatData(beat_number=4, metadata={"letter": "Σ"}),
            BeatData(beat_number=5, metadata={"letter": "W"}),
        ]

        test_sequence = SequenceData(
            id="coordinator_test", beats=beats, start_position="beta3"
        )

        print(
            f"📝 [DIRECT_TEST] Original sequence: {[beat.letter for beat in test_sequence.beats]}"
        )

        # Create state manager and set sequence
        state_manager = WorkbenchStateManager()
        state_manager.set_sequence(test_sequence)

        # Create beat operations service
        beat_operations = SequenceBeatOperations()

        # Create operation coordinator
        coordinator = WorkbenchOperationCoordinator(
            workbench_state_manager=state_manager, beat_operations=beat_operations
        )

        # Test delete beat operation
        print("🗑️ [DIRECT_TEST] Executing delete beat operation via coordinator...")
        result = coordinator.delete_beat(2)  # Delete beat at index 2

        if not result.success:
            print(f"❌ [DIRECT_TEST] Operation failed: {result.message}")
            return False

        print(f"✅ [DIRECT_TEST] Operation successful: {result.message}")

        # Check the updated sequence
        if result.updated_sequence:
            remaining_letters = [beat.letter for beat in result.updated_sequence.beats]
            print(f"📊 [DIRECT_TEST] Result: {remaining_letters}")

            # Should have 2 beats remaining (J, θ)
            expected = ["J", "θ"]
            if remaining_letters == expected:
                print("✅ [DIRECT_TEST] Operation coordinator working correctly!")
                return True
            else:
                print(f"❌ [DIRECT_TEST] Expected {expected}, got {remaining_letters}")
                return False
        else:
            print("❌ [DIRECT_TEST] No updated sequence in result")
            return False

    except Exception as e:
        print(f"❌ [DIRECT_TEST] Coordinator test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_start_position_deletion_directly():
    """Test start position deletion directly."""
    print("🧪 [DIRECT_TEST] Testing start position deletion directly...")

    try:
        # Create test sequence
        beats = [
            BeatData(beat_number=1, metadata={"letter": "J"}),
            BeatData(beat_number=2, metadata={"letter": "θ"}),
        ]

        test_sequence = SequenceData(
            id="start_pos_test", beats=beats, start_position="beta3"
        )

        print(
            f"📝 [DIRECT_TEST] Original sequence: {[beat.letter for beat in test_sequence.beats]}"
        )

        # Create state manager and set sequence
        state_manager = WorkbenchStateManager()
        state_manager.set_sequence(test_sequence)

        # Create beat operations service
        beat_operations = SequenceBeatOperations()

        # Create operation coordinator
        coordinator = WorkbenchOperationCoordinator(
            workbench_state_manager=state_manager, beat_operations=beat_operations
        )

        # Test start position deletion (beat_index = -1)
        print("🗑️ [DIRECT_TEST] Executing start position deletion...")
        result = coordinator.delete_beat(-1)  # Start position deletion

        if not result.success:
            print(f"❌ [DIRECT_TEST] Start position deletion failed: {result.message}")
            return False

        print(f"✅ [DIRECT_TEST] Start position deletion successful: {result.message}")

        # Check that all beats were deleted
        if result.updated_sequence:
            remaining_count = len(result.updated_sequence.beats)
            print(f"📊 [DIRECT_TEST] Remaining beats: {remaining_count}")

            if remaining_count == 0:
                print("✅ [DIRECT_TEST] Start position deletion working correctly!")
                return True
            else:
                print(f"❌ [DIRECT_TEST] Expected 0 beats, got {remaining_count}")
                return False
        else:
            print("❌ [DIRECT_TEST] No updated sequence in result")
            return False

    except Exception as e:
        print(f"❌ [DIRECT_TEST] Start position deletion test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def run_all_direct_tests():
    """Run all direct tests."""
    print("🚀 [DIRECT_TEST] Running all direct delete beat tests...")

    tests = [
        ("Delete Beat Service", test_delete_beat_service_directly),
        ("Operation Coordinator", test_operation_coordinator_directly),
        ("Start Position Deletion", test_start_position_deletion_directly),
    ]

    results = {}
    all_passed = True

    for test_name, test_func in tests:
        print(f"\n🧪 [DIRECT_TEST] Running: {test_name}")
        try:
            result = test_func()
            results[test_name] = result
            if result:
                print(f"✅ [DIRECT_TEST] {test_name} PASSED")
            else:
                print(f"❌ [DIRECT_TEST] {test_name} FAILED")
                all_passed = False
        except Exception as e:
            print(f"❌ [DIRECT_TEST] {test_name} ERROR: {e}")
            results[test_name] = False
            all_passed = False

    # Print summary
    print(f"\n📊 [DIRECT_TEST] Test Summary:")
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")

    if all_passed:
        print("\n🎉 All direct delete beat tests PASSED!")
    else:
        print("\n❌ Some direct delete beat tests FAILED!")

    return all_passed


if __name__ == "__main__":
    run_all_direct_tests()
