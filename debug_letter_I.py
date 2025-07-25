"""
Debug test for letter I positioning to trace what's happening.
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


def create_debug_letter_I_beat():
    """Create a simple letter I beat for debugging."""

    # Create motions with clear PRO/ANTI at diamond locations
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

    # Create pictograph data
    pictograph_data = PictographData(
        letter="I", motions={"red": red_motion, "blue": blue_motion}
    )

    # Create beat data
    beat_data = BeatData(beat_number=1, pictograph_data=pictograph_data, is_blank=False)

    return beat_data


def debug_letter_I_positioning():
    """Debug letter I positioning step by step."""
    print("\n🔍 DEBUG: Letter I Positioning Step by Step")
    print("=" * 60)

    beat_data = create_debug_letter_I_beat()

    print(f"Beat letter: {beat_data.letter}")
    print(
        f"Red motion: {beat_data.red_motion.motion_type.value} at {beat_data.red_motion.end_loc.value}"
    )
    print(
        f"Blue motion: {beat_data.blue_motion.motion_type.value} at {beat_data.blue_motion.end_loc.value}"
    )

    direction_service = DirectionCalculationService()

    print("\n🔍 Calculating red direction...")
    red_direction = direction_service.calculate_separation_direction(
        beat_data.red_motion, beat_data, "red"
    )
    print(f"Red direction result: {red_direction.value}")

    print("\n🔍 Calculating blue direction...")
    blue_direction = direction_service.calculate_separation_direction(
        beat_data.blue_motion, beat_data, "blue"
    )
    print(f"Blue direction result: {blue_direction.value}")

    # Check if they're opposite
    opposite_red = direction_service.get_opposite_direction(red_direction)
    print(f"\n🔍 Analysis:")
    print(f"Red direction: {red_direction.value}")
    print(f"Blue direction: {blue_direction.value}")
    print(f"Opposite of red: {opposite_red.value}")

    if blue_direction == opposite_red:
        print("✅ SUCCESS: Props move in opposite directions")
        return True
    else:
        print("❌ FAILURE: Props don't move in opposite directions")
        print("This means the letter I special case is NOT working")
        return False


def test_without_letter_I():
    """Test the same positions with a different letter to see the difference."""
    print("\n🔍 DEBUG: Same positions with letter β (generic beta)")
    print("=" * 60)

    # Create a new beat with β letter instead of modifying frozen dataclass
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

    pictograph_data = PictographData(
        letter="β", motions={"red": red_motion, "blue": blue_motion}  # Different letter
    )

    beat_data = BeatData(beat_number=1, pictograph_data=pictograph_data, is_blank=False)

    print(f"Beat letter: {beat_data.letter}")
    print(
        f"Red motion: {beat_data.red_motion.motion_type.value} at {beat_data.red_motion.end_loc.value}"
    )
    print(
        f"Blue motion: {beat_data.blue_motion.motion_type.value} at {beat_data.blue_motion.end_loc.value}"
    )

    direction_service = DirectionCalculationService()

    red_direction = direction_service.calculate_separation_direction(
        beat_data.red_motion, beat_data, "red"
    )
    blue_direction = direction_service.calculate_separation_direction(
        beat_data.blue_motion, beat_data, "blue"
    )

    print(f"β Red direction: {red_direction.value}")
    print(f"β Blue direction: {blue_direction.value}")

    opposite_red = direction_service.get_opposite_direction(red_direction)

    if blue_direction == opposite_red:
        print("✅ β props move in opposite directions")
    else:
        print("❌ β props don't move in opposite directions")
        print("This shows the standard behavior vs letter I behavior")


def run_debug_tests():
    """Run debug tests."""
    print("🔍 DEBUG: Letter I Positioning Analysis")
    print("=" * 70)

    result1 = debug_letter_I_positioning()
    test_without_letter_I()

    print("\n" + "=" * 70)
    print("🔍 DEBUG SUMMARY:")
    if result1:
        print("Letter I positioning appears to be working correctly")
        print("The issue might be elsewhere in the pipeline")
    else:
        print("Letter I special case is NOT working")
        print("Need to investigate why the fix isn't being applied")


if __name__ == "__main__":
    run_debug_tests()
