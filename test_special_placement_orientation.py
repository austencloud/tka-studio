"""
Test Special Placement Orientation Service

Automated tests to ensure the orientation key generation works correctly.
"""

import sys
import os

sys.path.append(
    os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
)

from application.services.positioning.special_placement_orientation_service import (
    SpecialPlacementOrientationService,
)
from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)
from domain.models.pictograph_models import ArrowData, PictographData, ArrowType


def test_special_placement_orientation_service():
    """Test the special placement orientation service."""

    service = SpecialPlacementOrientationService()

    print("=== Testing Special Placement Orientation Service ===")

    # Test Case 1: Pure radial orientations (should generate "from_layer1")
    print("\nTest Case 1: Pure radial orientations")

    blue_motion_radial = MotionData(
        motion_type=MotionType.PRO,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        turns=1.0,
        start_ori="in",
        end_ori="out",  # Radial
    )

    red_motion_radial = MotionData(
        motion_type=MotionType.ANTI,
        start_loc=Location.WEST,
        end_loc=Location.EAST,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        turns=0.0,
        start_ori="out",
        end_ori="in",  # Radial
    )

    blue_arrow_radial = ArrowData(
        arrow_type=ArrowType.BLUE, motion_data=blue_motion_radial, color="blue"
    )

    red_arrow_radial = ArrowData(
        arrow_type=ArrowType.RED, motion_data=red_motion_radial, color="red"
    )

    pictograph_radial = PictographData(
        letter="D", arrows={"blue": blue_arrow_radial, "red": red_arrow_radial}
    )

    ori_key_radial = service.generate_orientation_key(
        blue_motion_radial, pictograph_radial
    )
    print(f"Radial orientation key: '{ori_key_radial}' (expected: 'from_layer1')")

    # Test Case 2: Pure non-radial orientations (should generate "from_layer2")
    print("\nTest Case 2: Pure non-radial orientations")

    blue_motion_nonradial = MotionData(
        motion_type=MotionType.PRO,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        turns=1.0,
        start_ori="clock",
        end_ori="counter",  # Non-radial
    )

    red_motion_nonradial = MotionData(
        motion_type=MotionType.ANTI,
        start_loc=Location.WEST,
        end_loc=Location.EAST,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        turns=0.0,
        start_ori="counter",
        end_ori="clock",  # Non-radial
    )

    blue_arrow_nonradial = ArrowData(
        arrow_type=ArrowType.BLUE, motion_data=blue_motion_nonradial, color="blue"
    )

    red_arrow_nonradial = ArrowData(
        arrow_type=ArrowType.RED, motion_data=red_motion_nonradial, color="red"
    )

    pictograph_nonradial = PictographData(
        letter="W",  # Type2 letter (hybrid)
        arrows={"blue": blue_arrow_nonradial, "red": red_arrow_nonradial},
    )

    ori_key_nonradial = service.generate_orientation_key(
        blue_motion_nonradial, pictograph_nonradial
    )
    print(
        f"Non-radial orientation key: '{ori_key_nonradial}' (expected: 'from_layer2' or 'from_layer3')"
    )

    # Test Case 3: Mixed orientations (should generate layer3 key)
    print("\nTest Case 3: Mixed orientations (layer 3)")

    blue_motion_mixed = MotionData(
        motion_type=MotionType.PRO,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        turns=1.0,
        start_ori="in",
        end_ori="out",  # Radial (layer 1)
    )

    red_motion_mixed = MotionData(
        motion_type=MotionType.ANTI,
        start_loc=Location.WEST,
        end_loc=Location.EAST,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        turns=0.0,
        start_ori="clock",
        end_ori="counter",  # Non-radial (layer 2)
    )

    blue_arrow_mixed = ArrowData(
        arrow_type=ArrowType.BLUE, motion_data=blue_motion_mixed, color="blue"
    )

    red_arrow_mixed = ArrowData(
        arrow_type=ArrowType.RED, motion_data=red_motion_mixed, color="red"
    )

    pictograph_mixed = PictographData(
        letter="Δ-",  # Type3 letter (hybrid)
        arrows={"blue": blue_arrow_mixed, "red": red_arrow_mixed},
    )

    ori_key_mixed = service.generate_orientation_key(
        blue_motion_mixed, pictograph_mixed
    )
    print(
        f"Mixed orientation key: '{ori_key_mixed}' (expected: 'from_layer3_blue1_red2')"
    )

    print("\n=== All tests completed ===")


if __name__ == "__main__":
    test_special_placement_orientation_service()
