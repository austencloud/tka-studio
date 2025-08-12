#!/usr/bin/env python3
"""
SIMPLIFIED END-TO-END TEST: Clear Sequence Functionality
MANDATORY: Tests the REAL clear sequence workflow with REAL data

This test validates:
1. Creates REAL test sequence with actual data
2. Executes clear sequence operation
3. Validates persistence layer changes
4. Confirms expected default state
"""
from __future__ import annotations

from pathlib import Path
import sys


# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from application.services.sequence.sequence_persister import SequencePersister


class SimpleClearSequenceTest:
    """Simplified test for clear sequence functionality using REAL data"""

    def __init__(self):
        self.persistence_service = SequencePersister()

    def create_real_test_sequence(self) -> bool:
        """Create test sequence with REAL data that will actually be used"""
        print("📝 [SIMPLE_TEST] Creating REAL test sequence...")

        try:
            # REAL sequence data - exactly as provided by user
            real_sequence = [
                {
                    "word": "test",
                    "author": "e2e_test",
                    "level": 1,
                    "prop_type": "staff",
                    "grid_mode": "diamond",
                    "is_circular": False,
                },
                {
                    "beat": 0,
                    "sequence_start_position": "alpha1",
                    "end_pos": "alpha1",
                    "blue_attributes": {"start_ori": 0, "end_ori": 0, "motion_type": 0},
                    "red_attributes": {"start_ori": 0, "end_ori": 0, "motion_type": 0},
                },
                {
                    "beat": 1,
                    "letter": "A",
                    "blue_attributes": {
                        "start_ori": 0,
                        "end_ori": 90,
                        "motion_type": 1,
                    },
                    "red_attributes": {"start_ori": 0, "end_ori": 90, "motion_type": 1},
                },
            ]

            # Save REAL sequence
            self.persistence_service.save_current_sequence(real_sequence)

            # Verify it was saved correctly
            loaded = self.persistence_service.load_current_sequence()
            if len(loaded) >= 3:
                print(f"✅ [SIMPLE_TEST] REAL sequence created: {len(loaded)} items")
                print(
                    f"📝 [SIMPLE_TEST] Word: '{loaded[0].get('word')}', Author: '{loaded[0].get('author')}'"
                )
                print(
                    f"📝 [SIMPLE_TEST] Start pos: {loaded[1].get('sequence_start_position')}"
                )
                print(f"📝 [SIMPLE_TEST] Beat 1: {loaded[2].get('letter')}")
                return True
            print(
                f"❌ [SIMPLE_TEST] Failed to create sequence: {len(loaded)} items"
            )
            return False

        except Exception as e:
            print(f"❌ [SIMPLE_TEST] Error creating sequence: {e}")
            return False

    def execute_clear_sequence(self) -> bool:
        """Execute the clear sequence operation"""
        print("🧹 [SIMPLE_TEST] Executing clear sequence...")

        try:
            # Record state before clearing
            before_clear = self.persistence_service.load_current_sequence()
            print(f"📝 [SIMPLE_TEST] Before clear: {len(before_clear)} items")

            # Execute clear sequence operation
            self.persistence_service.clear_current_sequence()
            print("✅ [SIMPLE_TEST] Clear sequence operation executed")

            # Record state after clearing
            after_clear = self.persistence_service.load_current_sequence()
            print(f"📝 [SIMPLE_TEST] After clear: {len(after_clear)} items")

            return True

        except Exception as e:
            print(f"❌ [SIMPLE_TEST] Error during clear: {e}")
            return False

    def validate_clear_results(self) -> bool:
        """Validate the results of clear sequence operation"""
        print("✅ [SIMPLE_TEST] Validating clear results...")

        try:
            # Load current sequence
            current_sequence = self.persistence_service.load_current_sequence()

            # Should have exactly 1 item (metadata only)
            if len(current_sequence) != 1:
                print(
                    f"❌ [SIMPLE_TEST] Wrong sequence length: expected 1, got {len(current_sequence)}"
                )
                return False

            # Check metadata content
            metadata = current_sequence[0]

            # Word should be empty
            if metadata.get("word") != "":
                print(
                    f"❌ [SIMPLE_TEST] Word not cleared: expected '', got '{metadata.get('word')}'"
                )
                return False

            # Should have required fields
            required_fields = ["word", "author", "level", "prop_type", "grid_mode"]
            for field in required_fields:
                if field not in metadata:
                    print(f"❌ [SIMPLE_TEST] Missing required field: {field}")
                    return False

            print("✅ [SIMPLE_TEST] Clear sequence results validated successfully")
            print(f"📝 [SIMPLE_TEST] Final metadata: {metadata}")
            return True

        except Exception as e:
            print(f"❌ [SIMPLE_TEST] Error validating results: {e}")
            return False

    def test_sequence_consistency(self) -> bool:
        """Test that default sequence is consistent"""
        print("🔍 [SIMPLE_TEST] Testing sequence consistency...")

        try:
            # Get default sequence
            default_seq = self.persistence_service.get_default_sequence()

            # Clear and get cleared sequence
            self.persistence_service.clear_current_sequence()
            cleared_seq = self.persistence_service.load_current_sequence()

            # They should be identical
            if default_seq == cleared_seq:
                print("✅ [SIMPLE_TEST] Default and cleared sequences are consistent")
                return True
            print("❌ [SIMPLE_TEST] Default and cleared sequences differ")
            print(f"📝 [SIMPLE_TEST] Default: {default_seq}")
            print(f"📝 [SIMPLE_TEST] Cleared: {cleared_seq}")
            return False

        except Exception as e:
            print(f"❌ [SIMPLE_TEST] Error testing consistency: {e}")
            return False

    def run_complete_test(self) -> bool:
        """Run the complete simplified test"""
        print("🚀 SIMPLIFIED CLEAR SEQUENCE TEST")
        print("=" * 50)

        test_steps = [
            ("Create REAL Test Sequence", self.create_real_test_sequence),
            ("Execute Clear Sequence", self.execute_clear_sequence),
            ("Validate Clear Results", self.validate_clear_results),
            ("Test Sequence Consistency", self.test_sequence_consistency),
        ]

        for step_name, step_func in test_steps:
            print(f"\n🧪 {step_name}")
            print("-" * 30)

            try:
                success = step_func()
                if success:
                    print(f"✅ {step_name}: PASSED")
                else:
                    print(f"❌ {step_name}: FAILED")
                    return False
            except Exception as e:
                print(f"❌ {step_name}: ERROR - {e}")
                return False

        print("\n" + "=" * 50)
        print("🎉 ALL SIMPLIFIED TESTS PASSED!")
        print("✅ Clear sequence functionality works correctly")
        print("=" * 50)

        return True


def main():
    """Main test execution"""
    test = SimpleClearSequenceTest()
    success = test.run_complete_test()

    if success:
        print("\n🎉 SIMPLIFIED E2E TEST: SUCCESS")
        print("✅ Clear sequence persistence layer works correctly")
        print("✅ REAL data is handled properly")
        print("✅ Default sequence consistency maintained")
        return 0
    print("\n❌ SIMPLIFIED E2E TEST: FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
