"""
Test script to verify letter I prop positioning behavior.

This test uses real letter I pictograph data from the actual dataset
to identify positioning differences between legacy and modern implementations.
"""

import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src" / "desktop" / "modern" / "src"))

try:
    from application.services.data.dataset_query import DatasetQuery
    from application.services.learn.real_pictograph_data_service import (
        RealPictographDataService,
    )
    from application.services.pictograph.pictograph_csv_manager import (
        PictographCSVManager,
    )
    from application.services.positioning.props.calculation.direction_calculation_service import (
        DirectionCalculationService,
    )
    from application.services.positioning.props.orchestration.prop_orchestrator import (
        PropOrchestrator,
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
        # Initialize the real data service
        csv_manager = PictographCSVManager()
        dataset_query = DatasetQuery(csv_manager)
        data_service = RealPictographDataService(dataset_query)

        # Get letter I pictographs
        letter_i_data = data_service.get_pictographs_by_letter("I")

        print(f"📊 Found {len(letter_i_data)} real letter I pictographs")

        # Convert to BeatData for testing
        test_beats = []
        for i, pictograph_entry in enumerate(letter_i_data[:5]):  # Test first 5
            if "beat_data" in pictograph_entry:
                beat_data = pictograph_entry["beat_data"]
                if beat_data.has_pictograph:
                    test_beats.append(beat_data)
                    print(
                        f"  📌 I_{i}: {beat_data.pictograph_data.letter} with motions: red={beat_data.red_motion.motion_type.value if beat_data.red_motion else 'None'}, blue={beat_data.blue_motion.motion_type.value if beat_data.blue_motion else 'None'}"
                    )

        return test_beats

    except Exception as e:
        print(f"❌ Failed to load real letter I data: {e}")
        return []


def test_real_letter_I_pro_anti_positioning():
    """Test real letter I pictographs for PRO/ANTI positioning."""
    print("\n🔬 Testing Real Letter I PRO/ANTI positioning...")

    real_beats = get_real_letter_I_pictographs()
    if not real_beats:
        print("❌ No real letter I data available for testing")
        return False

    orchestrator = PropOrchestrator()
    direction_service = DirectionCalculationService()

    issues_found = []

    for i, beat_data in enumerate(real_beats):
        print(f"\n  Testing real I pictograph #{i}:")
        print(
            f"    Red motion: {beat_data.red_motion.motion_type.value} ending at {beat_data.red_motion.end_loc.value}"
        )
        print(
            f"    Blue motion: {beat_data.blue_motion.motion_type.value} ending at {beat_data.blue_motion.end_loc.value}"
        )

        # Test beta positioning should be applied
        should_apply = orchestrator.should_apply_beta_positioning(beat_data)
        if not should_apply:
            issues_found.append(f"I_{i}: Beta positioning not applied")
            continue

        # Calculate separation directions
        red_direction = direction_service.calculate_separation_direction(
            beat_data.red_motion, beat_data, "red"
        )
        blue_direction = direction_service.calculate_separation_direction(
            beat_data.blue_motion, beat_data, "blue"
        )

        print(f"    Red prop direction: {red_direction.value}")
        print(f"    Blue prop direction: {blue_direction.value}")

        # For letter I, PRO and ANTI props should move in opposite directions
        # Check which motion is PRO and which is ANTI
        if (
            beat_data.red_motion.motion_type == MotionType.PRO
            and beat_data.blue_motion.motion_type == MotionType.ANTI
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
            beat_data.blue_motion.motion_type == MotionType.PRO
            and beat_data.red_motion.motion_type == MotionType.ANTI
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
                f"    ⚠️  Skipping: Not a PRO/ANTI combination (red={beat_data.red_motion.motion_type.value}, blue={beat_data.blue_motion.motion_type.value})"
            )

    if issues_found:
        print(f"\n❌ Found {len(issues_found)} positioning issues in real data:")
        for issue in issues_found:
            print(f"   - {issue}")
        return False
    else:
        print(f"\n✅ All real letter I tests passed")
        return True


def test_real_letter_I_grid_mode_analysis():
    """Analyze real letter I pictographs by grid mode to understand the pattern."""
    print("\n🔬 Analyzing Real Letter I by Grid Mode...")

    real_beats = get_real_letter_I_pictographs()
    if not real_beats:
        print("❌ No real letter I data available for analysis")
        return False

    direction_service = DirectionCalculationService()

    diamond_issues = []
    box_issues = []

    for i, beat_data in enumerate(real_beats):
        # Determine grid mode from locations
        red_loc = beat_data.red_motion.end_loc
        blue_loc = beat_data.blue_motion.end_loc

        red_grid_mode = direction_service.detect_grid_mode(red_loc)
        blue_grid_mode = direction_service.detect_grid_mode(blue_loc)

        print(
            f"\n  I_{i}: Red {red_loc.value} ({red_grid_mode}), Blue {blue_loc.value} ({blue_grid_mode})"
        )
        print(
            f"    Motion types: Red {beat_data.red_motion.motion_type.value}, Blue {beat_data.blue_motion.motion_type.value}"
        )

        # Calculate directions
        red_direction = direction_service.calculate_separation_direction(
            beat_data.red_motion, beat_data, "red"
        )
        blue_direction = direction_service.calculate_separation_direction(
            beat_data.blue_motion, beat_data, "blue"
        )

        print(f"    Directions: Red {red_direction.value}, Blue {blue_direction.value}")

        # Check if they're opposite (the key test for letter I)
        opposite_red = direction_service.get_opposite_direction(red_direction)
        opposite_blue = direction_service.get_opposite_direction(blue_direction)

        if red_direction == opposite_blue and blue_direction == opposite_red:
            print(f"    ✅ Props move in opposite directions")
        else:
            issue = f"I_{i}: Red {red_direction.value} vs Blue {blue_direction.value} (not opposite)"
            if red_grid_mode == "diamond" or blue_grid_mode == "diamond":
                diamond_issues.append(issue)
            else:
                box_issues.append(issue)
            print(f"    ❌ {issue}")

    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"Diamond grid issues: {len(diamond_issues)}")
    print(f"Box grid issues: {len(box_issues)}")

    if diamond_issues:
        print(f"\n❌ Diamond grid issues:")
        for issue in diamond_issues:
            print(f"   - {issue}")

    if box_issues:
        print(f"\n❌ Box grid issues:")
        for issue in box_issues:
            print(f"   - {issue}")

    return len(diamond_issues) == 0 and len(box_issues) == 0


def compare_legacy_vs_modern_letter_I():
    """Document the difference between legacy and modern letter I logic."""
    print("\n🔬 Comparing Legacy vs Modern Letter I Logic...")

    print("LEGACY LOGIC (from reposition_I method):")
    print("1. Identify which prop has PRO motion and which has ANTI motion")
    print("2. Calculate direction for PRO motion using get_dir(pro_motion)")
    print("3. Move PRO prop in that direction")
    print("4. Move ANTI prop in opposite direction")
    print("=> PRO and ANTI always move in opposite directions regardless of location")

    print("\nMODERN LOGIC (current DirectionCalculationService):")
    print("1. Use location-based direction mapping")
    print("2. For diamond grid: (NORTH,red)→RIGHT, (SOUTH,blue)→RIGHT")
    print("3. For box grid: (NORTHEAST,red)→DOWNRIGHT, (SOUTHWEST,blue)→UPLEFT")
    print("=> Direction depends on location+color, ignoring motion type")

    print("\n💡 THE KEY DIFFERENCE:")
    print("Legacy: Motion type (PRO/ANTI) determines direction relationship")
    print("Modern: Location + color determines direction (motion type ignored)")

    print("\n🔧 REQUIRED FIX:")
    print("Modern system needs letter-specific logic that:")
    print("1. Detects letter I")
    print("2. Identifies PRO and ANTI motions")
    print("3. Ensures PRO and ANTI props move in opposite directions")


def run_comprehensive_letter_I_test():
    """Run comprehensive test suite for real letter I positioning."""
    print("🚀 Running comprehensive Letter I positioning tests with REAL data...")
    print("=" * 70)

    tests = [
        test_real_letter_I_pro_anti_positioning,
        test_real_letter_I_grid_mode_analysis,
        compare_legacy_vs_modern_letter_I,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            # compare_legacy_vs_modern_letter_I doesn't return boolean
            if result is None:
                result = True
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed with error: {e}")
            results.append(False)

    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY:")
    print(f"✅ Passed: {sum(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}")
    print(f"📈 Success rate: {sum(results)/len(results)*100:.1f}%")

    if not all(results):
        print("\n🔧 ISSUES IDENTIFIED:")
        print("1. Modern system lacks PRO/ANTI-specific positioning for letter I")
        print(
            "2. Direction calculation uses location/color mapping instead of motion type"
        )
        print("3. Missing letter-specific handling in prop orchestrator")

        print("\n💡 RECOMMENDED FIXES:")
        print(
            "1. Add letter-specific direction calculation in DirectionCalculationService"
        )
        print("2. Implement PRO/ANTI motion identification in prop orchestrator")
        print("3. Add letter I special case handling similar to legacy implementation")

    return all(results)


if __name__ == "__main__":
    success = run_comprehensive_letter_I_test()
    sys.exit(0 if success else 1)
