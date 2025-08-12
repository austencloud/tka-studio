#!/usr/bin/env python3
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: Debug clear sequence transition issue
DELETE_AFTER: 2025-01-31
CREATED: 2025-01-03
AUTHOR: @ai-agent

Test to debug why clear sequence is not transitioning to start position picker.
"""
from __future__ import annotations

from pathlib import Path
import sys


# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_clear_sequence_logic():
    """Test the clear sequence logic step by step"""
    print("🧪 Testing clear sequence transition logic...")

    try:
        from domain.models import SequenceData

        # Step 1: Test empty sequence detection
        print("\n📝 Step 1: Testing empty sequence detection")
        empty_sequence = SequenceData.empty()
        print(
            f"Empty sequence: length={empty_sequence.length}, beats={len(empty_sequence.beats)}"
        )

        # Step 2: Test the has_beats logic from signal coordinator
        print("\n📝 Step 2: Testing has_beats logic")
        has_beats = (
            empty_sequence is not None
            and empty_sequence.length > 0
            and not (
                empty_sequence.length == 1 and empty_sequence.beats[0].is_blank
                if empty_sequence.beats
                else False
            )
            and empty_sequence.metadata.get("cleared") is not True
        )
        print(f"has_beats result: {has_beats}")

        # Step 3: Test start position state (simulating cleared state)
        print("\n📝 Step 3: Testing start position state")
        start_position_set = False  # This should be False after clearing
        print(f"start_position_set: {start_position_set}")

        # Step 4: Test the transition logic
        print("\n📝 Step 4: Testing transition logic")
        if start_position_set or has_beats:
            print("🎯 Result: Would transition to OPTION PICKER")
            print("❌ This is WRONG for a cleared sequence!")
        else:
            print("🎯 Result: Would transition to START POSITION PICKER")
            print("✅ This is CORRECT for a cleared sequence!")

        # Step 5: Test with a sequence that has beats
        print("\n📝 Step 5: Testing with sequence that has beats")
        from domain.models import BeatData

        beat = BeatData(beat_number=1, letter="A")
        sequence_with_beats = SequenceData(name="Test", beats=[beat])

        has_beats_with_content = (
            sequence_with_beats is not None
            and sequence_with_beats.length > 0
            and not (
                sequence_with_beats.length == 1
                and sequence_with_beats.beats[0].is_blank
                if sequence_with_beats.beats
                else False
            )
            and sequence_with_beats.metadata.get("cleared") is not True
        )
        print(
            f"Sequence with beats: length={sequence_with_beats.length}, has_beats={has_beats_with_content}"
        )

        if False or has_beats_with_content:  # start_position_set = False for this test
            print("🎯 Result: Would transition to OPTION PICKER")
            print("✅ This is CORRECT for a sequence with beats!")
        else:
            print("🎯 Result: Would transition to START POSITION PICKER")
            print("❌ This is WRONG for a sequence with beats!")

        print("\n✅ Clear sequence logic test completed")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_persistence_consistency():
    """Test that startup and clear produce consistent default sequences"""
    print("\n🧪 Testing persistence consistency...")

    try:
        from application.services.sequences.persister import SequencePersister

        service = SequencePersister()

        # Get default sequence
        default_seq = service.get_default_sequence()
        print(f"Default sequence: {default_seq}")

        # Clear sequence and check result
        service.clear_current_sequence()
        cleared_seq = service.load_current_sequence()
        print(f"Cleared sequence: {cleared_seq}")

        # Compare
        if default_seq == cleared_seq:
            print("✅ Default and cleared sequences match!")
        else:
            print("❌ Default and cleared sequences don't match!")
            print("Differences:")
            for i, (default_item, cleared_item) in enumerate(
                zip(default_seq, cleared_seq)
            ):
                if default_item != cleared_item:
                    print(f"  Item {i}: default={default_item}, cleared={cleared_item}")

        return default_seq == cleared_seq

    except Exception as e:
        print(f"❌ Persistence test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 Starting Clear Sequence Transition Debug Tests")
    print("=" * 60)

    tests = [
        ("Clear Sequence Logic", test_clear_sequence_logic),
        ("Persistence Consistency", test_persistence_consistency),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        return True

    print("⚠️ Some tests failed!")
    return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
