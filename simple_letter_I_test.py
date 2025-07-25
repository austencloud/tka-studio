"""
Simple test for letter I prop positioning with manually created valid data.
This tests the fix without needing the complex data service.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src" / "desktop" / "modern" / "src"))

try:
    from application.services.data.dataset_query import DatasetQuery
    from application.services.pictograph.pictograph_csv_manager import (
        PictographCSVManager,
    )
    from application.services.positioning.props.calculation.direction_calculation_service import (
        DirectionCalculationService,
    )
    from domain.models import BeatData, MotionData, PictographData
    from domain.models.enums import Location, MotionType, Orientation

    print("✅ Successfully imported modern components")
except ImportError as e:
    print(f"❌ Failed to import modern components: {e}")
    sys.exit(1)


def get_real_letter_I_pictographs():
    """Get real letter I pictographs from the actual dataset."""
    try:
        # Initialize the CSV manager and dataset query
        csv_manager = PictographCSVManager()
        dataset_query = DatasetQuery(csv_manager)

        # Get letter I pictographs using the correct API
        letter_i_beats = dataset_query.find_pictographs_by_letter("I")

        print(f"📊 Found {len(letter_i_beats)} real letter I pictographs")

        # Show details of first few
        for i, beat_data in enumerate(letter_i_beats[:5]):  # Show first 5
            try:
                if beat_data and beat_data.has_pictograph:
                    red_motion = beat_data.red_motion
                    blue_motion = beat_data.blue_motion
                    print(
                        f"  📌 I_{i}: Red {red_motion.motion_type.value if red_motion else 'None'} at {red_motion.end_loc.value if red_motion else 'None'}, Blue {blue_motion.motion_type.value if blue_motion else 'None'} at {blue_motion.end_loc.value if blue_motion else 'None'}"
                    )
            except Exception as e:
                print(f"  ⚠️  Skipping pictograph {i}: {e}")

        return letter_i_beats[:10]  # Return first 10 for testing

    except Exception as e:
        print(f"❌ Failed to load real letter I data: {e}")
        return []


def create_letter_I_beat(red_motion_type, blue_motion_type, end_location):
    """Create a valid letter I BeatData with proper structure.

    Letter I always has:
    - One PRO motion and one ANTI motion
    - Both motions END AT THE SAME LOCATION
    - Props move in opposite directions regardless of location
    """

    # Create motions - BOTH END AT THE SAME LOCATION for letter I
    red_motion = MotionData(
        motion_type=red_motion_type,
        start_loc=Location.NORTH,  # Start position doesn't matter for prop positioning
        end_loc=end_location,  # SAME end location for letter I
        start_ori=Orientation.IN,
        end_ori=Orientation.IN,
        turns=0.0,
        prop_rot_dir=None,
    )

    blue_motion = MotionData(
        motion_type=blue_motion_type,
        start_loc=Location.SOUTH,  # Start position doesn't matter for prop positioning
        end_loc=end_location,  # SAME end location for letter I
        start_ori=Orientation.IN,
        end_ori=Orientation.IN,
        turns=0.0,
        prop_rot_dir=None,
    )

    # Create pictograph data with motions dict
    pictograph_data = PictographData(
        letter="I", motions={"red": red_motion, "blue": blue_motion}
    )

    # Create beat data
    beat_data = BeatData(beat_number=1, pictograph_data=pictograph_data, is_blank=False)

    return beat_data


def test_real_letter_I_positioning():
    """Test real letter I pictographs for PRO/ANTI positioning."""
    print("\n🔬 Testing Real Letter I PRO/ANTI positioning...")

    real_beats = get_real_letter_I_pictographs()
    if not real_beats:
        print("❌ No real letter I data available for testing")
        return False

    direction_service = DirectionCalculationService()
    issues_found = []

    for i, beat_data in enumerate(real_beats):
        print(f"\n  Testing real I pictograph #{i}:")
        red_motion = beat_data.red_motion
        blue_motion = beat_data.blue_motion

        if not red_motion or not blue_motion:
            print(f"    ⚠️  Skipping: Missing motion data")
            continue

        print(
            f"    Red motion: {red_motion.motion_type.value} ending at {red_motion.end_loc.value}"
        )
        print(
            f"    Blue motion: {blue_motion.motion_type.value} ending at {blue_motion.end_loc.value}"
        )

        # Calculate separation directions
        red_direction = direction_service.calculate_separation_direction(
            red_motion, beat_data, "red"
        )
        blue_direction = direction_service.calculate_separation_direction(
            blue_motion, beat_data, "blue"
        )

        print(f"    Red prop direction: {red_direction.value}")
        print(f"    Blue prop direction: {blue_direction.value}")

        # For letter I, PRO and ANTI props should move in opposite directions
        # Check which motion is PRO and which is ANTI
        if (
            red_motion.motion_type == MotionType.PRO
            and blue_motion.motion_type == MotionType.ANTI
        ):
            # Red is PRO, blue is ANTI - they should be opposite
            expected_blue_direction = direction_service.get_opposite_direction(
                red_direction
            )
            if blue_direction != expected_blue_direction:
                issue = f"I_{i}: Red PRO goes {red_direction.value}, Blue ANTI goes {blue_direction.value} (expected {expected_blue_direction.value})"
                issues_found.append(issue)
                print(f"    ❌ {issue}")
            else:
                print(f"    ✅ Correct: PRO and ANTI move in opposite directions")

        elif (
            blue_motion.motion_type == MotionType.PRO
            and red_motion.motion_type == MotionType.ANTI
        ):
            # Blue is PRO, red is ANTI - they should be opposite
            expected_red_direction = direction_service.get_opposite_direction(
                blue_direction
            )
            if red_direction != expected_red_direction:
                issue = f"I_{i}: Blue PRO goes {blue_direction.value}, Red ANTI goes {red_direction.value} (expected {expected_red_direction.value})"
                issues_found.append(issue)
                print(f"    ❌ {issue}")
            else:
                print(f"    ✅ Correct: PRO and ANTI move in opposite directions")
        else:
            print(
                f"    ⚠️  Skipping: Not a PRO/ANTI combination (red={red_motion.motion_type.value}, blue={blue_motion.motion_type.value})"
            )

    if issues_found:
        print(f"\n❌ Found {len(issues_found)} positioning issues in real data:")
        for issue in issues_found:
            print(f"   - {issue}")
        return False
    else:
        print(f"\n✅ All real letter I tests passed")
        return True


def test_letter_I_diamond_grid_issue():
    """Test the specific diamond grid issue where both props get same direction."""
    print("\n🔬 Testing Letter I Diamond Grid Issue...")

    # Use real letter I data instead of fake data
    real_beats = get_real_letter_I_pictographs()
    if not real_beats:
        print("❌ No real letter I data available for testing")
        return False

    # Test the first real letter I pictograph
    beat_data = real_beats[0]
    red_motion = beat_data.red_motion
    blue_motion = beat_data.blue_motion

    if not red_motion or not blue_motion:
        print("❌ Missing motion data in real pictograph")
        return False

    print(f"Testing: Red {red_motion.motion_type.value} at {red_motion.end_loc.value}")
    print(
        f"         Blue {blue_motion.motion_type.value} at {blue_motion.end_loc.value}"
    )

    direction_service = DirectionCalculationService()

    # Calculate directions with current system
    red_direction = direction_service.calculate_separation_direction(
        red_motion, beat_data, "red"
    )
    blue_direction = direction_service.calculate_separation_direction(
        blue_motion, beat_data, "blue"
    )

    print(f"Current directions: Red {red_direction.value}, Blue {blue_direction.value}")

    # Check if they're opposite (what letter I needs)
    opposite_red = direction_service.get_opposite_direction(red_direction)

    if blue_direction == opposite_red:
        print("✅ Props move in opposite directions (CORRECT for letter I)")
        return True
    else:
        print(f"❌ Props don't move in opposite directions!")
        print(f"   Red {red_motion.motion_type.value} goes {red_direction.value}")
        print(f"   Blue {blue_motion.motion_type.value} goes {blue_direction.value}")
        print(f"   Expected blue to go {opposite_red.value}")
        print(f"   💡 This is the letter I positioning bug!")
        return False


def test_letter_I_various_combinations():
    """Test letter I with various real pictographs."""
    print("\n🔬 Testing Letter I Various Real Pictographs...")

    real_beats = get_real_letter_I_pictographs()
    if not real_beats:
        print("❌ No real letter I data available for testing")
        return False

    direction_service = DirectionCalculationService()
    issues = []

    for i, beat_data in enumerate(real_beats):
        red_motion = beat_data.red_motion
        blue_motion = beat_data.blue_motion

        if not red_motion or not blue_motion:
            continue

        print(
            f"\n  Testing real pictograph {i}: Red {red_motion.motion_type.value} at {red_motion.end_loc.value}, Blue {blue_motion.motion_type.value} at {blue_motion.end_loc.value}"
        )

        red_direction = direction_service.calculate_separation_direction(
            red_motion, beat_data, "red"
        )
        blue_direction = direction_service.calculate_separation_direction(
            blue_motion, beat_data, "blue"
        )

        print(f"    Directions: Red {red_direction.value}, Blue {blue_direction.value}")

        # For letter I, PRO and ANTI should be opposite regardless of which color they are
        if (
            red_motion.motion_type == MotionType.PRO
            and blue_motion.motion_type == MotionType.ANTI
        ):
            expected_blue = direction_service.get_opposite_direction(red_direction)
            if blue_direction != expected_blue:
                issue = f"I_{i}: Red PRO {red_direction.value} vs Blue ANTI {blue_direction.value} (expected {expected_blue.value})"
                issues.append(issue)
                print(f"    ❌ {issue}")
            else:
                print(f"    ✅ Correct: PRO and ANTI are opposite")

        elif (
            red_motion.motion_type == MotionType.ANTI
            and blue_motion.motion_type == MotionType.PRO
        ):
            expected_red = direction_service.get_opposite_direction(blue_direction)
            if red_direction != expected_red:
                issue = f"I_{i}: Blue PRO {blue_direction.value} vs Red ANTI {red_direction.value} (expected {expected_red.value})"
                issues.append(issue)
                print(f"    ❌ {issue}")
            else:
                print(f"    ✅ Correct: PRO and ANTI are opposite")
        else:
            print(f"    ⚠️  Skipping: Not a PRO/ANTI combination")

    if issues:
        print(f"\n❌ Found {len(issues)} issues:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print(f"\n✅ All combinations work correctly")
        return True


def run_simple_letter_I_test():
    """Run simple letter I test with manual data."""
    print("🚀 Testing Letter I Positioning (Simple Test)")
    print("=" * 50)

    tests = [
        test_real_letter_I_positioning,
        test_letter_I_diamond_grid_issue,
        test_letter_I_various_combinations,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed: {e}")
            results.append(False)

    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    print(f"✅ Passed: {sum(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}")

    if not all(results):
        print("\n🔧 The issue is confirmed:")
        print("Letter I props don't move in opposite directions for PRO/ANTI motions")
        print(
            "The modern system needs the fix I implemented in DirectionCalculationService"
        )

    return all(results)


if __name__ == "__main__":
    success = run_simple_letter_I_test()
    sys.exit(0 if success else 1)
