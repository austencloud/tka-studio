"""
Test for Faithful Attribute Key Generation Service

Tests only the methods that actually exist in the legacy AttrKeyGenerator.
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


def test_faithful_attribute_key_generation():
    """Test the faithful port of legacy AttrKeyGenerator methods only."""

    service = AttributeKeyGenerationService()

    print("=== Testing Faithful Legacy AttrKeyGenerator Port ===\n")

    # Test Case 1: Standard orientation, non-hybrid motion, Type1 letter
    print("Test Case 1: Standard orientation, non-hybrid, Type1 letter")
    motion_data = MotionData(
        motion_type=MotionType.PRO,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        turns=1.0,
        start_ori="in",
        end_ori="out",
    )

    arrow_data = ArrowData(
        arrow_type=ArrowType.BLUE, motion_data=motion_data, color="blue"
    )

    pictograph_data = PictographData(
        letter="D", arrows={"blue": arrow_data}  # Type1 letter
    )

    result = service.get_key_from_arrow(arrow_data, pictograph_data)
    print(
        f"Result: '{result}' (expected: color = 'blue' for standard orientation + non-hybrid)"
    )

    # Test Case 2: Mixed orientation with hybrid motions, radial start
    print("\nTest Case 2: Mixed orientation with hybrid motions, radial start")
    blue_motion = MotionData(
        motion_type=MotionType.PRO,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        turns=1.0,
        start_ori="in",  # Radial
        end_ori="out",
    )

    red_motion = MotionData(
        motion_type=MotionType.ANTI,  # Different motion type = hybrid
        start_loc=Location.EAST,
        end_loc=Location.WEST,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        turns=0.5,
        start_ori="clock",  # Different start orientation = mixed
        end_ori="counter",
    )

    blue_arrow = ArrowData(
        arrow_type=ArrowType.BLUE, motion_data=blue_motion, color="blue"
    )

    red_arrow = ArrowData(arrow_type=ArrowType.RED, motion_data=red_motion, color="red")

    pictograph_mixed = PictographData(
        letter="W", arrows={"blue": blue_arrow, "red": red_arrow}  # Type2 letter
    )

    result = service.get_key_from_arrow(blue_arrow, pictograph_mixed)
    print(
        f"Result: '{result}' (expected: 'pro_from_layer1' for mixed + hybrid + radial start)"
    )

    # Test Case 3: S/T letter with standard orientation
    print("\nTest Case 3: S/T letter with standard orientation")
    pictograph_s = PictographData(
        letter="S", arrows={"blue": arrow_data}  # Special S letter
    )

    result = service.get_key_from_arrow(arrow_data, pictograph_s)
    print(
        f"Result: '{result}' (expected: 'blue_blue' for S letter + standard orientation)"
    )

    # Test Case 4: Core generate_key method
    print("\nTest Case 4: Core generate_key method")
    result = service.generate_key(
        motion_type="pro",
        letter="D",
        start_ori="in",
        color="blue",
        lead_state="blue",
        has_hybrid_motions=False,
        starts_from_mixed_orientation=False,
        starts_from_standard_orientation=True,
    )
    print(f"Result: '{result}' (expected: 'blue' for standard + non-hybrid)")

    print("\n=== Faithful Legacy Tests Completed ===")


if __name__ == "__main__":
    test_faithful_attribute_key_generation()
