"""
Debug test for letter I positioning to see what's actually happening.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src" / "desktop" / "modern" / "src"))

try:
    from application.services.data.dataset_query import DatasetQuery
    from application.services.positioning.props.orchestration.prop_management_service import (
        PropManagementService,
    )

    print("✅ Successfully imported modern components")
except ImportError as e:
    print(f"❌ Failed to import modern components: {e}")
    sys.exit(1)


def debug_letter_I_positioning():
    """Debug letter I positioning step by step using REAL letter I data."""
    print("\n🔬 DEBUG: Letter I Positioning with REAL data...")

    # Get real letter I data from dataset
    dataset_query = DatasetQuery()

    try:
        # Get actual letter I pictographs from CSV
        letter_I_beats = dataset_query.find_pictographs_by_letter("I")

        if not letter_I_beats:
            print("❌ No letter I data found in dataset!")
            return False

        print(f"📊 Found {len(letter_I_beats)} letter I pictographs in dataset")

        # Use the first letter I pictograph
        first_beat = letter_I_beats[0]

        if not first_beat.has_pictograph:
            print("❌ First beat has no pictograph data!")
            return False

        pictograph_data = first_beat.pictograph_data

        print(f"\n🎯 Using real letter I data (first):")
        print(f"  Letter: {pictograph_data.letter}")
        print(f"  Start position: {pictograph_data.start_position}")
        print(f"  End position: {pictograph_data.end_position}")

        # Get the actual motions
        red_motion = pictograph_data.motions.get("red")
        blue_motion = pictograph_data.motions.get("blue")

        if not red_motion or not blue_motion:
            print("❌ Missing motion data!")
            return False

        print(
            f"  Red motion: {red_motion.motion_type.value} from {red_motion.start_loc.value} to {red_motion.end_loc.value}"
        )
        print(
            f"  Blue motion: {blue_motion.motion_type.value} from {blue_motion.start_loc.value} to {blue_motion.end_loc.value}"
        )

        # Test PropManagementService
        prop_service = PropManagementService()

        # Debug: Test the NEW _calculate_letter_I_directions method directly
        print(f"\n🔍 Testing _calculate_letter_I_directions method (first):")

        # Test the coordinated method
        blue_result, red_result = prop_service._calculate_letter_I_directions(
            blue_motion, red_motion
        )

        print(
            f"Blue {blue_motion.motion_type.value.upper()} direction: {blue_result.value}"
        )
        print(
            f"Red {red_motion.motion_type.value.upper()} direction: {red_result.value}"
        )

        # Check if they're opposite
        print(f"\n📊 Analysis (first):")
        print(f"  Blue direction: {blue_result.value}")
        print(f"  Red direction: {red_result.value}")

        # Manual check for opposites
        opposite_pairs = [
            ("right", "left"),
            ("left", "right"),
            ("up", "down"),
            ("down", "up"),
            ("upright", "downleft"),
            ("downleft", "upright"),
            ("upleft", "downright"),
            ("downright", "upleft"),
        ]

        is_opposite_first = (blue_result.value, red_result.value) in opposite_pairs or (
            red_result.value,
            blue_result.value,
        ) in opposite_pairs
        print(f"  Are opposite: {is_opposite_first}")

        # Now test second pictograph
        if len(letter_I_beats) > 1:
            second_beat = letter_I_beats[1]
            if second_beat.has_pictograph:
                pictograph_data_2 = second_beat.pictograph_data
                print(f"\n🎯 Using real letter I data (second):")
                print(f"  Letter: {pictograph_data_2.letter}")
                print(f"  Start position: {pictograph_data_2.start_position}")
                print(f"  End position: {pictograph_data_2.end_position}")

                red_motion_2 = pictograph_data_2.motions.get("red")
                blue_motion_2 = pictograph_data_2.motions.get("blue")

                if red_motion_2 and blue_motion_2:
                    print(
                        f"  Red motion: {red_motion_2.motion_type.value} from {red_motion_2.start_loc.value} to {red_motion_2.end_loc.value}"
                    )
                    print(
                        f"  Blue motion: {blue_motion_2.motion_type.value} from {blue_motion_2.start_loc.value} to {blue_motion_2.end_loc.value}"
                    )

                    print(
                        f"\n🔍 Testing _calculate_letter_I_directions method (second):"
                    )
                    blue_result_2, red_result_2 = (
                        prop_service._calculate_letter_I_directions(
                            blue_motion_2, red_motion_2
                        )
                    )

                    print(
                        f"Blue {blue_motion_2.motion_type.value.upper()} direction: {blue_result_2.value}"
                    )
                    print(
                        f"Red {red_motion_2.motion_type.value.upper()} direction: {red_result_2.value}"
                    )

                    is_opposite_second = (
                        blue_result_2.value,
                        red_result_2.value,
                    ) in opposite_pairs or (
                        red_result_2.value,
                        blue_result_2.value,
                    ) in opposite_pairs
                    print(f"  Are opposite: {is_opposite_second}")

                    if is_opposite_first and is_opposite_second:
                        print(
                            "✅ SUCCESS: Letter I positioning is working correctly for both cases!"
                        )
                        return True
                    elif is_opposite_first:
                        print("⚠️ PARTIAL: First case works, second case doesn't")
                        return False
                    else:
                        print("❌ FAILURE: Letter I positioning is NOT working!")
                        return False

        if is_opposite_first:
            print("✅ SUCCESS: Letter I positioning is working correctly!")
            return True
        else:
            print("❌ FAILURE: Letter I positioning is NOT working!")
            return False

    except Exception as e:
        print(f"❌ Error loading real data: {e}")
        return False


if __name__ == "__main__":
    success = debug_letter_I_positioning()
    sys.exit(0 if success else 1)
