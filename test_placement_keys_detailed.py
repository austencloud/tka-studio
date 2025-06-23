"""
Test Placement Key Generation vs Special Placement Paths

This test helps us understand the discrepancy between what keys we generate
and what paths the special placement system expects.
"""

import sys
import os

sys.path.append(
    os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
)

from application.services.positioning.placement_key_generation_service import (
    PlacementKeyGenerationService,
)
from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)
from domain.models.pictograph_models import ArrowData, PictographData, ArrowType


def test_placement_keys_for_dash_letters():
    """Test placement key generation for dash letters (TYPE3/TYPE5)."""

    service = PlacementKeyGenerationService()

    # Test letters that are failing in the logs
    test_letters = ["Δ-", "Φ", "Ψ-", "β"]

    for letter in test_letters:
        print(f"\n=== Testing letter: {letter} ===")

        # Create test motion data (similar to what might cause the issues)
        motion_data = MotionData(
            motion_type=MotionType.ANTI,  # From the logs
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            turns=0.0,
            start_ori="in",
            end_ori="out",
        )

        arrow_data = ArrowData(
            arrow_type=ArrowType.BLUE, motion_data=motion_data, color="blue"
        )

        pictograph_data = PictographData(letter=letter, arrows={"blue": arrow_data})

        # Test with empty default placements (should fall back to motion type)
        default_placements = {}

        # Generate placement key
        placement_key = service.generate_key(
            arrow_data, pictograph_data, default_placements
        )
        print(f"Placement key: '{placement_key}'")

        # Test individual components that make up the key
        motion_end_ori_key = service._get_motion_end_ori_key(
            False, "out"
        )  # Not hybrid, end_ori="out"
        print(f"Motion end ori key: '{motion_end_ori_key}'")

        letter_suffix = service._get_letter_suffix(letter)
        print(f"Letter suffix: '{letter_suffix}'")

        # Test with different hybrid scenarios
        key_middle_radial = service._get_key_middle(
            True, False, False, False, False, False
        )
        print(f"Key middle (radial props): '{key_middle_radial}'")

        key_middle_nonradial = service._get_key_middle(
            False, True, False, False, False, False
        )
        print(f"Key middle (non-radial props): '{key_middle_nonradial}'")

        key_middle_hybrid = service._get_key_middle(
            False, False, True, False, False, False
        )
        print(f"Key middle (hybrid orientation): '{key_middle_hybrid}'")


if __name__ == "__main__":
    test_placement_keys_for_dash_letters()
