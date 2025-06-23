"""
Test for Placement Key Generation Service

Simple test to verify the faithfully ported placement key generation logic.
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
    Orientation,
    Location,
    RotationDirection,
)
from domain.models.pictograph_models import ArrowData, PictographData, ArrowType


def test_placement_key_generation():
    """Test basic placement key generation functionality."""

    # Create service
    service = PlacementKeyGenerationService()

    # Create test data using correct enum values
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

    pictograph_data = PictographData(letter="D", arrows={"blue": arrow_data})

    # Test placement key generation
    default_placements = {"pro": True, "pro_to_layer1": True, "pro_to_layer1_D": True}

    result = service.generate_key(arrow_data, pictograph_data, default_placements)
    print(f"Generated placement key: {result}")

    # Test letter suffix generation
    suffix = service._get_letter_suffix("D")
    print(f"Letter suffix for 'D': {suffix}")

    # Test TYPE3 letter suffix
    suffix_type3 = service._get_letter_suffix("W-")
    print(f"Letter suffix for 'W-': {suffix_type3}")

    # Test TYPE5 letter suffix
    suffix_type5 = service._get_letter_suffix("Φ-")
    print(f"Letter suffix for 'Φ-': {suffix_type5}")


if __name__ == "__main__":
    test_placement_key_generation()
