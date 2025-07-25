"""
Simple test for letter I positioning fix.

Tests the letter I special case handling without complex data dependencies.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src" / "desktop" / "modern" / "src"))

try:
    from application.services.positioning.props.calculation.direction_calculation_service import (
        DirectionCalculationService,
    )
    from domain.models import BeatData, MotionData, PictographData
    from domain.models.enums import Location, MotionType, Orientation

    print("✅ Successfully imported modern components")
except ImportError as e:
    print(f"❌ Failed to import modern components: {e}")
    sys.exit(1)


def create_letter_I_beat(red_motion_type, blue_motion_type, red_end_loc, blue_end_loc):
    """Create a letter I beat for testing."""
    red_motion = MotionData(
        motion_type=red_motion_type,
        start_loc=Location.NORTH,
        end_loc=red_end_loc,
        start_ori=Orientation.IN,
        end_ori=Orientation.IN,
        turns=0.0,
        prop_rot_dir=None,
    )

    blue_motion = MotionData(
        motion_type=blue_motion_type,
        start_loc=Location.SOUTH,
        end_loc=blue_end_loc,
        start_ori=Orientation.IN,
        end_ori=Orientation.IN,
        turns=0.0,
        prop_rot_dir=None,
    )

    pictograph_data = PictographData(
        letter="I", motions={"red": red_motion, "blue": blue_motion}
    )

    beat_data = BeatData(beat_number=1, pictograph_data=pictograph_data, is_blank=False)

    # Add convenience properties for easier access
    beat_data.red_motion = red_motion
    beat_data.blue_motion = blue_motion
    beat_data.letter = "I"

    return beat_data


def test_letter_I_fix():
    """Test the letter I positioning fix."""
    print("\n🔧 Testing Letter I Fix...")

    direction_service = DirectionCalculationService()

    test_cases = [
        # (red_motion, blue_motion, red_end_loc, blue_end_loc, case_name)
        (
            MotionType.PRO,
            MotionType.ANTI,
            Location.NORTH,
            Location.SOUTH,
            "PRO-red/ANTI-blue N-S",
        ),
        (
            MotionType.ANTI,
            MotionType.PRO,
            Location.NORTH,
            Location.SOUTH,
            "ANTI-red/PRO-blue N-S",
        ),
        (
            MotionType.PRO,
            MotionType.ANTI,
            Location.EAST,
            Location.WEST,
            "PRO-red/ANTI-blue E-W",
        ),
        (
            MotionType.PRO,
            MotionType.ANTI,
            Location.NORTHEAST,
            Location.SOUTHWEST,
            "PRO-red/ANTI-blue NE-SW",
        ),
    ]

    all_passed = True

    for red_type, blue_type, red_loc, blue_loc, case_name in test_cases:
        print(f"\n  Testing: {case_name}")

        beat_data = create_letter_I_beat(red_type, blue_type, red_loc, blue_loc)

        red_direction = direction_service.calculate_separation_direction(
            beat_data.red_motion, beat_data, "red"
        )
        blue_direction = direction_service.calculate_separation_direction(
            beat_data.blue_motion, beat_data, "blue"
        )

        print(f"    Red {red_type.value} direction: {red_direction.value}")
        print(f"    Blue {blue_type.value} direction: {blue_direction.value}")

        # Check if they are opposite
        expected_opposite = direction_service.get_opposite_direction(red_direction)

        if blue_direction == expected_opposite:
            print(f"    ✅ PASS: Props move in opposite directions")
        else:
            print(
                f"    ❌ FAIL: Expected blue to be {expected_opposite.value}, got {blue_direction.value}"
            )
            all_passed = False

    return all_passed


def test_letter_I_vs_beta():
    """Test that letter I behaves differently from letter β."""
    print("\n🔧 Testing Letter I vs β difference...")

    direction_service = DirectionCalculationService()

    # Create identical beats except for letter
    red_motion = MotionData(
        motion_type=MotionType.PRO,
        start_loc=Location.NORTH,
        end_loc=Location.NORTH,
        start_ori=Orientation.IN,
        end_ori=Orientation.IN,
        turns=0.0,
        prop_rot_dir=None,
    )

    blue_motion = MotionData(
        motion_type=MotionType.ANTI,
        start_loc=Location.SOUTH,
        end_loc=Location.SOUTH,
        start_ori=Orientation.IN,
        end_ori=Orientation.IN,
        turns=0.0,
        prop_rot_dir=None,
    )

    # Letter I beat
    i_data = PictographData(
        letter="I", motions={"red": red_motion, "blue": blue_motion}
    )
    i_beat = BeatData(beat_number=1, pictograph_data=i_data, is_blank=False)
    i_beat.red_motion = red_motion
    i_beat.blue_motion = blue_motion
    i_beat.letter = "I"

    # Letter β beat
    beta_data = PictographData(
        letter="β", motions={"red": red_motion, "blue": blue_motion}
    )
    beta_beat = BeatData(beat_number=1, pictograph_data=beta_data, is_blank=False)
    beta_beat.red_motion = red_motion
    beta_beat.blue_motion = blue_motion
    beta_beat.letter = "β"

    # Calculate directions
    i_red_dir = direction_service.calculate_separation_direction(
        red_motion, i_beat, "red"
    )
    i_blue_dir = direction_service.calculate_separation_direction(
        blue_motion, i_beat, "blue"
    )

    beta_red_dir = direction_service.calculate_separation_direction(
        red_motion, beta_beat, "red"
    )
    beta_blue_dir = direction_service.calculate_separation_direction(
        blue_motion, beta_beat, "blue"
    )

    print(f"  Letter I:  Red {i_red_dir.value}, Blue {i_blue_dir.value}")
    print(f"  Letter β:  Red {beta_red_dir.value}, Blue {beta_blue_dir.value}")

    # They should be different
    if i_red_dir != beta_red_dir or i_blue_dir != beta_blue_dir:
        print(f"  ✅ PASS: Letter I has different positioning than β")
        return True
    else:
        print(f"  ❌ FAIL: Letter I and β have identical positioning")
        return False


def main():
    """Run all tests."""
    print("🚀 Testing Letter I Positioning Fix...")
    print("=" * 50)

    tests = [
        test_letter_I_fix,
        test_letter_I_vs_beta,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed with error: {e}")
            import traceback

            traceback.print_exc()
            results.append(False)

    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    print(f"✅ Passed: {sum(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}")

    if all(results):
        print("🎉 All tests passed! Letter I fix is working correctly.")
    else:
        print("❌ Some tests failed. Letter I fix needs more work.")

    return all(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
