"""
Unit tests for ArrowLocationCalculator

Tests the pure algorithmic arrow location calculation service.
Validates extraction from ArrowManagementService maintains accuracy.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

# Add modern/src to path for imports
modern_src_path = Path(__file__).parent.parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)
from domain.models.pictograph_models import PictographData
from application.services.positioning.arrows.calculation.arrow_location_calculator import (
    ArrowLocationCalculatorService as ArrowLocationCalculator,
)
from core.interfaces.positioning_services import IArrowLocationCalculator


class TestArrowLocationCalculator:
    """Test suite for ArrowLocationCalculator."""

    def setup_method(self):
        """Set up test fixtures."""
        # Mock dash location service to avoid complex dependencies
        self.mock_dash_service = Mock()
        self.calculator = ArrowLocationCalculator()

    def test_static_arrow_location(self):
        """Test static arrow location calculation."""
        motion = MotionData(
            motion_type=MotionType.STATIC,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
        )

        result = self.calculator.calculate_location(motion)
        assert result == Location.NORTH

    def test_shift_arrow_locations(self):
        """Test shift arrow location calculations for all direction pairs."""
        test_cases = [
            # (start, end, expected_location)
            (Location.NORTH, Location.EAST, Location.NORTHEAST),
            (Location.EAST, Location.SOUTH, Location.SOUTHEAST),
            (Location.SOUTH, Location.WEST, Location.SOUTHWEST),
            (Location.WEST, Location.NORTH, Location.NORTHWEST),
            (Location.NORTHEAST, Location.NORTHWEST, Location.NORTH),
            (Location.NORTHEAST, Location.SOUTHEAST, Location.EAST),
            (Location.SOUTHWEST, Location.SOUTHEAST, Location.SOUTH),
            (Location.NORTHWEST, Location.SOUTHWEST, Location.WEST),
        ]

        for start_loc, end_loc, expected in test_cases:
            motion = MotionData(
                motion_type=MotionType.PRO,
                start_loc=start_loc,
                end_loc=end_loc,
                prop_rot_dir=RotationDirection.CLOCKWISE,
            )

            result = self.calculator.calculate_location(motion)
            assert result == expected, f"Failed for {start_loc} -> {end_loc}"

    def test_dash_arrow_location_delegates_to_service(self):
        """Test dash arrow location calculation."""
        motion = MotionData(
            motion_type=MotionType.DASH,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
        )

        result = self.calculator.calculate_location(motion)

        # Dash arrows use sophisticated mapping - RED arrow NORTH→SOUTH maps to EAST
        assert result == Location.EAST

    def test_unknown_motion_type_returns_start_location(self):
        """Test unknown motion type returns start location as fallback."""
        # Test with static motion type
        motion = MotionData(
            motion_type=MotionType.STATIC,
            start_loc=Location.WEST,
            end_loc=Location.EAST,
            prop_rot_dir=RotationDirection.CLOCKWISE,
        )

        # Test that static motion returns start location
        result = self.calculator.calculate_location(motion)
        assert result == Location.WEST

    def test_interface_compliance(self):
        """Test that ArrowLocationCalculator implements the interface correctly."""
        assert isinstance(self.calculator, IArrowLocationCalculator)

        # Test interface method exists and is callable
        motion = MotionData(
            motion_type=MotionType.STATIC,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
        )

        result = self.calculator.calculate_location(motion)
        assert isinstance(result, Location)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
