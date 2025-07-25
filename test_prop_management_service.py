"""
Focused test for PropManagementService letter I fix.
Tests the actual service that handles prop positioning in the renderer.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src" / "desktop" / "modern" / "src"))

try:
    from domain.models import BeatData, MotionData, PictographData
    from domain.models.enums import Location, MotionType, Orientation
    from application.services.positioning.props.orchestration.prop_management_service import PropManagementService
    
    print("✅ Successfully imported modern components")
except ImportError as e:
    print(f"❌ Failed to import modern components: {e}")
    sys.exit(1)


def create_letter_I_pictograph_data(red_motion_type, blue_motion_type, end_location):
    """Create a letter I pictograph data with both motions ending at same location."""
    
    red_motion = MotionData(
        motion_type=red_motion_type,
        start_loc=Location.NORTH,
        end_loc=end_location,  # Same end location for letter I
        start_ori=Orientation.IN,
        end_ori=Orientation.IN,
        turns=0.0,
        prop_rot_dir=None
    )
    
    blue_motion = MotionData(
        motion_type=blue_motion_type,
        start_loc=Location.SOUTH,
        end_loc=end_location,  # Same end location for letter I
        start_ori=Orientation.IN,
        end_ori=Orientation.IN,
        turns=0.0,
        prop_rot_dir=None
    )
    
    pictograph_data = PictographData(
        letter="I",
        motions={
            "red": red_motion,
            "blue": blue_motion
        }
    )
    
    return pictograph_data


def test_prop_management_service_letter_I():
    """Test PropManagementService letter I positioning directly."""
    print("\n🔬 Testing PropManagementService Letter I Fix...")
    
    # Create test case: PRO red, ANTI blue, both at NORTH (diamond grid)
    pictograph_data = create_letter_I_pictograph_data(
        red_motion_type=MotionType.PRO,
        blue_motion_type=MotionType.ANTI,
        end_location=Location.NORTH
    )
    
    print(f"Test case: Red {pictograph_data.motions['red'].motion_type.value} at {pictograph_data.motions['red'].end_loc.value}")
    print(f"           Blue {pictograph_data.motions['blue'].motion_type.value} at {pictograph_data.motions['blue'].end_loc.value}")
    print(f"           Letter: {pictograph_data.letter}")
    
    # Create PropManagementService and test
    prop_service = PropManagementService()
    
    # Test the separation direction calculation
    red_direction = prop_service._calculate_separation_direction(
        pictograph_data.motions["red"], "red", pictograph_data.letter
    )
    blue_direction = prop_service._calculate_separation_direction(
        pictograph_data.motions["blue"], "blue", pictograph_data.letter
    )
    
    print(f"Calculated directions: Red {red_direction.value}, Blue {blue_direction.value}")
    
    # For letter I, PRO and ANTI should be opposite
    if red_direction.value == "right" and blue_direction.value == "left":
        print("✅ Correct: Red PRO goes right, Blue ANTI goes left (opposite directions)")
        return True
    elif red_direction.value == "left" and blue_direction.value == "right":
        print("✅ Correct: Red PRO goes left, Blue ANTI goes right (opposite directions)")
        return True
    else:
        print(f"❌ Wrong: Red PRO goes {red_direction.value}, Blue ANTI goes {blue_direction.value}")
        print(f"   Expected: Opposite directions for PRO and ANTI in letter I")
        return False


def test_letter_I_vs_beta_comparison():
    """Compare letter I positioning with generic beta positioning."""
    print("\n🔬 Comparing Letter I vs Beta Positioning...")
    
    prop_service = PropManagementService()
    
    # Test letter I
    i_pictograph = create_letter_I_pictograph_data(
        MotionType.PRO, MotionType.ANTI, Location.NORTH
    )
    
    i_red_dir = prop_service._calculate_separation_direction(
        i_pictograph.motions["red"], "red", "I"
    )
    i_blue_dir = prop_service._calculate_separation_direction(
        i_pictograph.motions["blue"], "blue", "I"
    )
    
    # Test generic beta letter (β)
    beta_pictograph = create_letter_I_pictograph_data(
        MotionType.PRO, MotionType.ANTI, Location.NORTH
    )
    beta_pictograph.letter = "β"
    
    beta_red_dir = prop_service._calculate_separation_direction(
        beta_pictograph.motions["red"], "red", "β"
    )
    beta_blue_dir = prop_service._calculate_separation_direction(
        beta_pictograph.motions["blue"], "blue", "β"
    )
    
    print(f"Letter I:  Red {i_red_dir.value}, Blue {i_blue_dir.value}")
    print(f"Letter β:  Red {beta_red_dir.value}, Blue {beta_blue_dir.value}")
    
    # They should be different if letter I special case is working
    if (i_red_dir != beta_red_dir) or (i_blue_dir != beta_blue_dir):
        print("✅ Letter I has different positioning than β (special case working)")
        return True
    else:
        print("❌ Letter I and β have identical positioning (special case not working)")
        return False


def test_various_letter_I_positions():
    """Test letter I at various end positions."""
    print("\n🔬 Testing Letter I at Various Positions...")
    
    prop_service = PropManagementService()
    test_locations = [Location.NORTH, Location.EAST, Location.NORTHEAST, Location.SOUTHEAST]
    
    issues = []
    
    for location in test_locations:
        print(f"\n  Testing at {location.value}:")
        
        pictograph_data = create_letter_I_pictograph_data(
            MotionType.PRO, MotionType.ANTI, location
        )
        
        red_direction = prop_service._calculate_separation_direction(
            pictograph_data.motions["red"], "red", "I"
        )
        blue_direction = prop_service._calculate_separation_direction(
            pictograph_data.motions["blue"], "blue", "I"
        )
        
        print(f"    Red PRO: {red_direction.value}, Blue ANTI: {blue_direction.value}")
        
        # Check if they're opposite
        opposite_pairs = [
            ("right", "left"), ("left", "right"),
            ("up", "down"), ("down", "up"),
            ("upright", "downleft"), ("downleft", "upright"),
            ("upleft", "downright"), ("downright", "upleft")
        ]
        
        is_opposite = (red_direction.value, blue_direction.value) in opposite_pairs
        
        if is_opposite:
            print(f"    ✅ Opposite directions (correct for letter I)")
        else:
            issue = f"{location.value}: Red {red_direction.value} vs Blue {blue_direction.value} (not opposite)"
            issues.append(issue)
            print(f"    ❌ {issue}")
    
    if issues:
        print(f"\n❌ Found {len(issues)} positioning issues:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print(f"\n✅ All positions work correctly")
        return True


def run_prop_management_test():
    """Run PropManagementService-focused tests."""
    print("🚀 Testing PropManagementService Letter I Fix")
    print("=" * 50)
    
    tests = [
        test_prop_management_service_letter_I,
        test_letter_I_vs_beta_comparison,
        test_various_letter_I_positions,
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
    
    if all(results):
        print("\n🎉 All tests passed! Letter I positioning fix is working correctly.")
    else:
        print("\n🔧 Some tests failed. The letter I positioning fix needs more work.")
    
    return all(results)


if __name__ == "__main__":
    success = run_prop_management_test()
    sys.exit(0 if success else 1)
