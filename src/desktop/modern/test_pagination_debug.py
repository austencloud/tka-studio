"""
Simple test to trigger the pagination debugging and see the output.
This script will manually trigger the option loading process to observe the debugging output.
"""

import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_option_loading():
    """Test the option loading process with debugging."""
    try:
        print("🚀 [PAGINATION_DEBUG_TEST] Starting option loading test...")

        # Import the services we added debugging to
        from application.services.option_picker.sequence_option_service import (
            SequenceOptionService,
        )
        from application.services.positioning.arrows.utilities.pictograph_position_matcher import (
            PictographPositionMatcher,
        )
        from domain.models.beat_data import BeatData
        from domain.models.pictograph_data import PictographData
        from domain.models.sequence_data import SequenceData

        print("✅ [PAGINATION_DEBUG_TEST] Imports successful")

        # Create position matcher
        position_matcher = PictographPositionMatcher()
        print("✅ [PAGINATION_DEBUG_TEST] Position matcher created")

        # Create sequence option service
        sequence_option_service = SequenceOptionService(position_matcher)
        print("✅ [PAGINATION_DEBUG_TEST] Sequence option service created")

        # Create a test sequence with alpha1 start position
        print("\n🔄 [PAGINATION_DEBUG_TEST] Creating test sequence...")

        # Create a simple beat with alpha1 end position
        test_beat = BeatData(
            pictograph_data=PictographData(
                letter="A", start_position="alpha1", end_position="alpha1"
            )
        )

        # Create sequence with beats
        test_sequence = SequenceData(beats=[test_beat])

        print("✅ [PAGINATION_DEBUG_TEST] Test sequence created")

        # Test multiple consecutive calls to simulate the pagination issue
        print("\n🔍 [PAGINATION_DEBUG_TEST] Testing consecutive option loads...")

        for i in range(1, 5):
            print(f"\n{'='*50}")
            print(f"🔄 [PAGINATION_DEBUG_TEST] LOAD #{i}")
            print(f"{'='*50}")

            # Call get_options_for_sequence (this should trigger our debugging)
            options_by_type = sequence_option_service.get_options_for_sequence(
                test_sequence
            )

            # Count total options
            total_options = sum(len(options) for options in options_by_type.values())
            print(
                f"📊 [PAGINATION_DEBUG_TEST] Load #{i} result: {total_options} total options"
            )

            for letter_type, options in options_by_type.items():
                if options:
                    print(f"   {letter_type}: {len(options)} options")

        print(f"\n✅ [PAGINATION_DEBUG_TEST] Test completed successfully")

    except Exception as e:
        print(f"❌ [PAGINATION_DEBUG_TEST] Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_option_loading()
