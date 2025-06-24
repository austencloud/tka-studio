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
    BeatData,
)
from domain.models.pictograph_models import PictographData, ArrowData, GridData
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

    def test_dash_arrow_location_with_pictograph_data(self):
        """Test dash arrow location calculation with full pictograph context."""
        # Create dash motion
        dash_motion = MotionData(
            motion_type=MotionType.DASH,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            turns=0.0,
        )

        # Create shift motion for Type 3 scenario
        shift_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            turns=1.0,
        )

        # Create pictograph data with both arrows
        pictograph_data = PictographData(
            grid_data=GridData(),
            arrows={
                "blue": ArrowData(color="blue", motion_data=dash_motion),
                "red": ArrowData(color="red", motion_data=shift_motion),
            },
            metadata={"letter": "A", "created_from_beat": 1},
        )

        # Test dash location calculation with pictograph context
        result = self.calculator.calculate_location(dash_motion, pictograph_data)

        # Should return a valid location (not None)
        assert isinstance(result, Location)
        # For this Type 3 scenario with NORTH->SOUTH dash and EAST->WEST shift,
        # the diamond map doesn't have (NORTH, EAST) so it falls back to start_loc
        assert result == Location.NORTH

    def test_dash_arrow_location_without_pictograph_data(self):
        """Test dash arrow location calculation without pictograph context."""
        dash_motion = MotionData(
            motion_type=MotionType.DASH,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            turns=0.0,
        )

        # Test without pictograph data - should still work but with limited context
        result = self.calculator.calculate_location(dash_motion, None)

        # Should return a valid location
        assert isinstance(result, Location)
        # Should return EAST for NORTH->SOUTH dash motion
        assert result == Location.EAST

    def test_extract_beat_data_from_pictograph(self):
        """Test extraction of beat data from pictograph."""
        # Create test motions
        blue_motion = MotionData(
            motion_type=MotionType.DASH,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
        )

        red_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            prop_rot_dir=RotationDirection.CLOCKWISE,
        )

        # Create pictograph data
        pictograph_data = PictographData(
            arrows={
                "blue": ArrowData(color="blue", motion_data=blue_motion),
                "red": ArrowData(color="red", motion_data=red_motion),
            },
            metadata={"letter": "A", "created_from_beat": 1},
        )

        # Test extraction
        beat_data = self.calculator._extract_beat_data_from_pictograph(pictograph_data)

        assert beat_data is not None
        assert beat_data.blue_motion == blue_motion
        assert beat_data.red_motion == red_motion
        assert beat_data.letter == "A"
        assert beat_data.beat_number == 1

    def test_is_blue_arrow_motion(self):
        """Test determination of arrow color from motion."""
        blue_motion = MotionData(
            motion_type=MotionType.DASH,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
        )

        red_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            prop_rot_dir=RotationDirection.CLOCKWISE,
        )

        beat_data = BeatData(
            blue_motion=blue_motion,
            red_motion=red_motion,
            letter="A",
        )

        # Test blue motion identification
        assert self.calculator._is_blue_arrow_motion(blue_motion, beat_data) is True

        # Test red motion identification
        assert self.calculator._is_blue_arrow_motion(red_motion, beat_data) is False

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
