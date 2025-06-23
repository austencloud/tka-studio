"""
Test Turns Tuple Generation Service

Automated tests to ensure the turns tuple generation works correctly.
"""

import sys
import os

sys.path.append(
    os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
)

from application.services.positioning.turns_tuple_generation_service import (
    TurnsTupleGenerationService,
)
from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)
from domain.models.pictograph_models import ArrowData, PictographData, ArrowType


def test_turns_tuple_generation_service():
    """Test the turns tuple generation service."""

    service = TurnsTupleGenerationService()

    print("=== Testing Turns Tuple Generation Service ===")

    # Test Case 1: Non-hybrid letter (Type1)
    print("\nTest Case 1: Non-hybrid letter (Type1)")

    blue_motion = MotionData(
        motion_type=MotionType.PRO,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        turns=1.0,
        start_ori="in",
        end_ori="out",
    )

    red_motion = MotionData(
        motion_type=MotionType.ANTI,
        start_loc=Location.WEST,
        end_loc=Location.EAST,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        turns=0.0,
        start_ori="out",
        end_ori="in",
    )

    blue_arrow = ArrowData(
        arrow_type=ArrowType.BLUE, motion_data=blue_motion, color="blue"
    )

    red_arrow = ArrowData(arrow_type=ArrowType.RED, motion_data=red_motion, color="red")

    pictograph_type1 = PictographData(
        letter="D", arrows={"blue": blue_arrow, "red": red_arrow}  # Type1 letter
    )

    tuple_type1 = service.generate_turns_tuple(pictograph_type1)
    print(f"Type1 letter 'D' turns tuple: '{tuple_type1}' (expected: '(1, 0)')")

    # Test Case 2: Type3 dash letter (hybrid)
    print("\nTest Case 2: Type3 dash letter (hybrid)")

    blue_motion_dash = MotionData(
        motion_type=MotionType.DASH,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        turns=0.0,
        start_ori="in",
        end_ori="out",
    )

    red_motion_dash = MotionData(
        motion_type=MotionType.DASH,
        start_loc=Location.WEST,
        end_loc=Location.EAST,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        turns=0.0,
        start_ori="clock",
        end_ori="counter",
    )

    blue_arrow_dash = ArrowData(
        arrow_type=ArrowType.BLUE, motion_data=blue_motion_dash, color="blue"
    )

    red_arrow_dash = ArrowData(
        arrow_type=ArrowType.RED, motion_data=red_motion_dash, color="red"
    )

    pictograph_type3 = PictographData(
        letter="Δ-",  # Type3 letter
        arrows={"blue": blue_arrow_dash, "red": red_arrow_dash},
    )

    tuple_type3 = service.generate_turns_tuple(pictograph_type3)
    print(f"Type3 letter 'Δ-' turns tuple: '{tuple_type3}' (expected: '(0, 0)')")

    # Test Case 3: Fractional turns
    print("\nTest Case 3: Fractional turns")

    blue_motion_frac = MotionData(
        motion_type=MotionType.PRO,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        turns=1.5,
        start_ori="in",
        end_ori="out",
    )

    red_motion_frac = MotionData(
        motion_type=MotionType.ANTI,
        start_loc=Location.WEST,
        end_loc=Location.EAST,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        turns=0.5,
        start_ori="out",
        end_ori="in",
    )

    blue_arrow_frac = ArrowData(
        arrow_type=ArrowType.BLUE, motion_data=blue_motion_frac, color="blue"
    )

    red_arrow_frac = ArrowData(
        arrow_type=ArrowType.RED, motion_data=red_motion_frac, color="red"
    )

    pictograph_frac = PictographData(
        letter="A",  # Type1 letter
        arrows={"blue": blue_arrow_frac, "red": red_arrow_frac},
    )

    tuple_frac = service.generate_turns_tuple(pictograph_frac)
    print(f"Fractional turns tuple: '{tuple_frac}' (expected: '(1.5, 0.5)')")

    # Test Case 4: Type6 letter (Greek letters)
    print("\nTest Case 4: Type6 letter (Greek letters)")

    pictograph_type6 = PictographData(
        letter="β", arrows={"blue": blue_arrow, "red": red_arrow}  # Type6 letter
    )

    tuple_type6 = service.generate_turns_tuple(pictograph_type6)
    print(f"Type6 letter 'β' turns tuple: '{tuple_type6}' (expected: '(1, 0)')")

    print("\n=== All tests completed ===")


if __name__ == "__main__":
    test_turns_tuple_generation_service()
