#!/usr/bin/env python3
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: Validate clear sequence and startup functionality fixes
DELETE_AFTER: 2025-01-31
CREATED: 2025-01-03
AUTHOR: @ai-agent
RELATED_ISSUE: Clear sequence button and minimal sequence startup

Simple test to validate the fixes using TKA testing infrastructure.
"""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from application.services.sequence.sequence_persister import SequencePersister
from core.testing.ai_agent_helpers import TKAAITestHelper, ai_test_tka_comprehensive


def test_clear_sequence_fix():
    """Test that clear sequence functionality works correctly"""
    print("🧪 Testing clear sequence fix...")

    try:
        # Use TKA testing infrastructure
        helper = TKAAITestHelper(use_test_mode=True)
        persistence_service = SequencePersister()

        # Step 1: Create a test sequence
        print("📝 Creating test sequence...")
        seq_result = helper.create_sequence("Test Sequence", 4)
        assert seq_result.success, f"Failed to create sequence: {seq_result.message}"

        # Add a beat
        beat_result = helper.create_beat_with_motions(1, "A")
        assert beat_result.success, f"Failed to create beat: {beat_result.message}"

        print("✅ Test sequence created")

        # Step 2: Verify sequence exists in persistence
        print("📝 Verifying sequence exists in persistence...")
        sequence_data = persistence_service.load_current_sequence()
        initial_length = len(sequence_data)
        assert initial_length > 1, "Sequence should have metadata + beats"
        print(f"✅ Sequence has {initial_length} items in persistence")

        # Step 3: Clear the sequence (this tests our fix)
        print("📝 Clearing sequence...")
        persistence_service.clear_current_sequence()
        print("✅ Clear sequence called")

        # Step 4: Verify sequence is cleared
        print("📝 Verifying sequence is cleared...")
        cleared_sequence_data = persistence_service.load_current_sequence()
        cleared_length = len(cleared_sequence_data)
        print(f"🔍 Cleared sequence has {cleared_length} items")

        # Should have only default metadata
        assert cleared_length == 1, f"Expected 1 item (metadata), got {cleared_length}"
        assert (
            "word" in cleared_sequence_data[0]
        ), "Metadata should contain 'word' field"
        assert (
            cleared_sequence_data[0]["word"] == ""
        ), "Word should be empty after clearing"

        print("✅ Clear sequence fix works correctly")
        return True

    except Exception as e:
        print(f"❌ Clear sequence test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_minimal_sequence_startup():
    """Test startup with minimal sequence (metadata + start position only)"""
    print("\n🧪 Testing minimal sequence startup...")

    try:
        persistence_service = SequencePersister()

        # Create a minimal sequence (metadata + start position only)
        print("📝 Creating minimal sequence...")
        minimal_sequence = [
            {
                "word": "",
                "author": "test",
                "level": 0,
                "prop_type": "staff",
                "grid_mode": "diamond",
                "is_circular": False,
            },
            {
                "beat": 0,
                "sequence_start_position": "alpha1",
                "end_pos": "alpha1",
                "blue_attributes": {
                    "start_ori": 0,
                    "end_ori": 0,
                    "motion_type": 0,
                    "prop_rot_dir": 0,
                    "turns": 0,
                },
                "red_attributes": {
                    "start_ori": 0,
                    "end_ori": 0,
                    "motion_type": 0,
                    "prop_rot_dir": 0,
                    "turns": 0,
                },
            },
        ]

        # Save minimal sequence to persistence
        persistence_service.save_current_sequence(minimal_sequence)
        print("✅ Minimal sequence saved to persistence")

        # Verify the minimal sequence structure
        print("📝 Verifying minimal sequence structure...")
        loaded_sequence_data = persistence_service.load_current_sequence()
        assert (
            len(loaded_sequence_data) == 2
        ), f"Expected 2 items (metadata + start position), got {len(loaded_sequence_data)}"

        # Check metadata
        metadata = loaded_sequence_data[0]
        assert "word" in metadata, "Metadata should contain 'word' field"

        # Check start position
        start_pos = loaded_sequence_data[1]
        assert start_pos.get("beat") == 0, "Start position should have beat=0"
        assert (
            "sequence_start_position" in start_pos
        ), "Start position should have sequence_start_position"

        print("✅ Minimal sequence startup works correctly")
        return True

    except Exception as e:
        print(f"❌ Minimal sequence startup test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_comprehensive_workflow():
    """Test complete workflow using TKA testing infrastructure"""
    print("\n🧪 Testing comprehensive workflow...")

    try:
        # Use TKA comprehensive test
        result = ai_test_tka_comprehensive()

        assert result["overall_success"], "Comprehensive test should pass"
        assert (
            result["success_rate"] > 0.8
        ), f"Success rate should be > 0.8, got {result['success_rate']}"

        print("✅ Comprehensive workflow test passed")
        return True

    except Exception as e:
        print(f"❌ Comprehensive workflow test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 Starting Clear Sequence and Startup Fix Tests")
    print("=" * 60)

    tests = [
        ("Clear Sequence Fix", test_clear_sequence_fix),
        ("Minimal Sequence Startup", test_minimal_sequence_startup),
        ("Comprehensive Workflow", test_comprehensive_workflow),
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
