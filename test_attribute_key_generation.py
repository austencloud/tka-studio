"""
Test Attribute Key Generation Service

Automated tests to ensure the attribute key generation works correctly.
"""

import sys
import os

sys.path.append(
    os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
)

from application.services.positioning.attribute_key_generation_service import (
    AttributeKeyGenerationService,
)
from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)
from domain.models.pictograph_models import ArrowData, PictographData, ArrowType


def test_attribute_key_generation_service():
    """Test the attribute key generation service."""

    service = AttributeKeyGenerationService()

    print("=== Testing Attribute Key Generation Service ===")

    # Test Case 1: Basic pro motion
    print("\nTest Case 1: Basic pro motion")

    blue_motion_pro = MotionData(
        motion_type=MotionType.PRO,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        turns=1.0,
        start_ori="in",
        end_ori="out",
    )

    blue_arrow_pro = ArrowData(
        arrow_type=ArrowType.BLUE, motion_data=blue_motion_pro, color="blue"
    )

    pictograph_pro = PictographData(letter="D", arrows={"blue": blue_arrow_pro})

    attr_key_pro = service.generate_attribute_key(blue_arrow_pro, pictograph_pro)
    print(f"Pro motion attribute key: '{attr_key_pro}'")

    # Test Case 2: Anti motion with different orientations
    print("\nTest Case 2: Anti motion")

    red_motion_anti = MotionData(
        motion_type=MotionType.ANTI,
        start_loc=Location.WEST,
        end_loc=Location.EAST,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        turns=0.0,
        start_ori="clock",
        end_ori="counter",
    )

    red_arrow_anti = ArrowData(
        arrow_type=ArrowType.RED, motion_data=red_motion_anti, color="red"
    )

    pictograph_anti = PictographData(letter="W", arrows={"red": red_arrow_anti})

    attr_key_anti = service.generate_attribute_key(red_arrow_anti, pictograph_anti)
    print(f"Anti motion attribute key: '{attr_key_anti}'")

    # Test Case 3: Dash motion
    print("\nTest Case 3: Dash motion")

    dash_motion = MotionData(
        motion_type=MotionType.DASH,
        start_loc=Location.NORTHEAST,
        end_loc=Location.SOUTHWEST,
        prop_rot_dir=RotationDirection.NO_ROTATION,
        turns=0.0,
        start_ori="in",
        end_ori="in",
    )

    dash_arrow = ArrowData(
        arrow_type=ArrowType.BLUE, motion_data=dash_motion, color="blue"
    )

    pictograph_dash = PictographData(letter="Δ-", arrows={"blue": dash_arrow})

    attr_key_dash = service.generate_attribute_key(dash_arrow, pictograph_dash)
    print(f"Dash motion attribute key: '{attr_key_dash}'")

    # Test Case 4: Static motion
    print("\nTest Case 4: Static motion")

    static_motion = MotionData(
        motion_type=MotionType.STATIC,
        start_loc=Location.EAST,
        end_loc=Location.EAST,
        prop_rot_dir=RotationDirection.NO_ROTATION,
        turns=0.0,
        start_ori="out",
        end_ori="out",
    )

    static_arrow = ArrowData(
        arrow_type=ArrowType.RED, motion_data=static_motion, color="red"
    )

    pictograph_static = PictographData(letter="β", arrows={"red": static_arrow})

    attr_key_static = service.generate_attribute_key(static_arrow, pictograph_static)
    print(f"Static motion attribute key: '{attr_key_static}'")

    # Test Case 5: Fractional turns
    print("\nTest Case 5: Fractional turns")

    frac_motion = MotionData(
        motion_type=MotionType.PRO,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        turns=1.5,
        start_ori="in",
        end_ori="out",
    )

    frac_arrow = ArrowData(
        arrow_type=ArrowType.BLUE, motion_data=frac_motion, color="blue"
    )

    pictograph_frac = PictographData(letter="A", arrows={"blue": frac_arrow})

    attr_key_frac = service.generate_attribute_key(frac_arrow, pictograph_frac)
    print(f"Fractional turns attribute key: '{attr_key_frac}'")

    # Test Case 6: Simple attribute key
    print("\nTest Case 6: Simple attribute key")

    simple_key = service.generate_simple_attribute_key(MotionType.PRO, "blue")
    print(f"Simple attribute key: '{simple_key}' (expected: 'pro_blue')")

    # Test Case 7: Position-based key
    print("\nTest Case 7: Position-based key")

    pos_key = service.generate_position_based_key(blue_arrow_pro, pictograph_pro)
    print(f"Position-based key: '{pos_key}'")

    print("\n=== All tests completed ===")


if __name__ == "__main__":
    test_attribute_key_generation_service()
