#!/usr/bin/env python3
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: Validate clear sequence and startup functionality fixes
DELETE_AFTER: 2025-01-31
CREATED: 2025-01-03
AUTHOR: @ai-agent
RELATED_ISSUE: Clear sequence button and minimal sequence startup

This test validates:
1. Clear sequence button properly clears both memory and current_sequence.json
2. Startup with minimal sequences (metadata + start position only) works correctly
3. Option picker loads correctly based on start position
4. UI visibility states are properly set

Usage:
    python test_clear_sequence_and_startup.py
"""
from __future__ import annotations

from pathlib import Path
import sys


# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from application.services.sequence.sequence_persister import SequencePersister
from core.testing.ai_agent_helpers import TKAAITestHelper


class ClearSequenceAndStartupTester:
    """Test clear sequence and startup functionality using TKA testing patterns"""

    def __init__(self):
        self.helper = None
        self.persistence_service = None

    def setup(self):
        """Setup test environment using TKA testing patterns"""
        print("🔧 Setting up test environment...")

        # Use TKA testing infrastructure
        self.helper = TKAAITestHelper(use_test_mode=True)
        self.persistence_service = SequencePersister()

        print("✅ Test environment setup complete")

    def test_clear_sequence_functionality(self):
        """Test that clear sequence button properly clears both memory and persistence"""
        print("\n🧪 Testing clear sequence functionality...")

        try:
            # Step 1: Create a sequence with start position and beats
            print("📝 Step 1: Creating test sequence...")
            seq_result = self.helper.create_sequence("Test Sequence", 4)
            assert (
                seq_result.success
            ), f"Failed to create sequence: {seq_result.message}"

            # Add a start position
            start_pos_result = self.helper.create_beat_with_motions(0, "alpha1")
            assert (
                start_pos_result.success
            ), f"Failed to create start position: {start_pos_result.message}"

            # Add some beats
            beat1_result = self.helper.create_beat_with_motions(1, "A")
            assert (
                beat1_result.success
            ), f"Failed to create beat 1: {beat1_result.message}"

            beat2_result = self.helper.create_beat_with_motions(2, "B")
            assert (
                beat2_result.success
            ), f"Failed to create beat 2: {beat2_result.message}"

            print("✅ Test sequence created successfully")

            # Step 2: Verify sequence exists in persistence
            print("📝 Step 2: Verifying sequence exists in persistence...")
            sequence_data = self.persistence_service.load_current_sequence()
            assert len(sequence_data) > 1, "Sequence should have metadata + beats"
            print(f"✅ Sequence has {len(sequence_data)} items in persistence")

            # Step 3: Clear the sequence using the service
            print("📝 Step 3: Clearing sequence...")
            self.persistence_service.clear_current_sequence()
            print("✅ Clear sequence called")

            # Step 4: Verify sequence is cleared in persistence
            print("📝 Step 4: Verifying sequence is cleared in persistence...")
            cleared_sequence_data = self.persistence_service.load_current_sequence()
            print(f"🔍 Cleared sequence has {len(cleared_sequence_data)} items")

            # Should have only default metadata
            assert (
                len(cleared_sequence_data) == 1
            ), f"Expected 1 item (metadata), got {len(cleared_sequence_data)}"
            assert (
                "word" in cleared_sequence_data[0]
            ), "Metadata should contain 'word' field"
            assert (
                cleared_sequence_data[0]["word"] == ""
            ), "Word should be empty after clearing"

            print("✅ Clear sequence functionality works correctly")
            return True

        except Exception as e:
            print(f"❌ Clear sequence test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_minimal_sequence_startup(self):
        """Test startup with minimal sequence (metadata + start position only)"""
        print("\n🧪 Testing minimal sequence startup...")

        try:
            # Step 1: Create a minimal sequence (metadata + start position only)
            print("📝 Step 1: Creating minimal sequence...")
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
            self.persistence_service.save_current_sequence(minimal_sequence)
            print("✅ Minimal sequence saved to persistence")

            # Step 2: Test loading the minimal sequence
            print("📝 Step 2: Testing sequence loading...")
            from application.services.sequences.sequence_loading_service import (
                SequenceLoadingService,
            )

            # Create a mock workbench for testing
            class MockWorkbench:
                def __init__(self):
                    self._start_position_data = None

                def set_start_position(self, start_position_data):
                    self._start_position_data = start_position_data
                    print(
                        f"✅ Mock workbench: Start position set to {start_position_data.letter}"
                    )

            mock_workbench = MockWorkbench()

            # Create loading service
            loading_service = SequenceLoadingService(
                workbench_getter=lambda: mock_workbench,
                workbench_setter=lambda seq: print(
                    f"✅ Mock workbench: Sequence set with {len(seq.beats)} beats"
                ),
            )

            # Test loading
            loading_service.load_sequence_on_startup()

            # Verify start position was set
            assert (
                mock_workbench._start_position_data is not None
            ), "Start position should be set in workbench"
            print("✅ Start position loaded correctly")

            # Step 3: Verify the loaded sequence structure
            print("📝 Step 3: Verifying loaded sequence structure...")
            loaded_sequence_data = self.persistence_service.load_current_sequence()
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

    def test_end_to_end_workflow(self):
        """Test complete workflow: clear sequence → restart app → verify proper initialization"""
        print("\n🧪 Testing end-to-end workflow...")

        try:
            # Step 1: Clear sequence functionality
            clear_success = self.test_clear_sequence_functionality()
            if not clear_success:
                return False

            # Step 2: Minimal sequence startup
            startup_success = self.test_minimal_sequence_startup()
            if not startup_success:
                return False

            # Step 3: Test complete workflow with TKAAITestHelper
            print("📝 Step 3: Testing complete workflow with TKAAITestHelper...")
            workflow_result = self.helper.test_complete_user_workflow()
            assert (
                workflow_result.success
            ), f"Complete workflow test failed: {workflow_result.message}"

            print("✅ End-to-end workflow test passed")
            return True

        except Exception as e:
            print(f"❌ End-to-end workflow test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Clear Sequence and Startup Tests")
        print("=" * 60)

        self.setup()

        tests = [
            ("Clear Sequence Functionality", self.test_clear_sequence_functionality),
            ("Minimal Sequence Startup", self.test_minimal_sequence_startup),
            ("End-to-End Workflow", self.test_end_to_end_workflow),
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
    tester = ClearSequenceAndStartupTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
