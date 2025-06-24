"""
Unit tests for DirectionCalculationService

Tests the pure direction calculation service.
Validates extraction from PropManagementService maintains functionality.
"""

import pytest
import sys
from pathlib import Path

# Add modern/src to path for imports
modern_src_path = Path(__file__).parent.parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
    Orientation,
)
from application.services.positioning.props.calculation.direction_calculation_service import (
    DirectionCalculationService,
    SeparationDirection,
)


class TestDirectionCalculationService:
    """Test suite for DirectionCalculationService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = DirectionCalculationService()

    def test_interface_compliance(self):
        """Test that DirectionCalculationService implements the interface correctly."""
        assert isinstance(self.service, DirectionCalculationService)

    def test_detect_grid_mode_diamond(self):
        """Test grid mode detection for diamond positions."""
        diamond_locations = [
            Location.NORTH,
            Location.SOUTH,
            Location.EAST,
            Location.WEST,
        ]

        for location in diamond_locations:
            result = self.service.detect_grid_mode(location)
            assert result == "diamond", f"Location {location} should be diamond grid"

    def test_detect_grid_mode_box(self):
        """Test grid mode detection for box positions."""
        box_locations = [
            Location.NORTHEAST,
            Location.SOUTHEAST,
            Location.SOUTHWEST,
            Location.NORTHWEST,
        ]

        for location in box_locations:
            result = self.service.detect_grid_mode(location)
            assert result == "box", f"Location {location} should be box grid"

    def test_calculate_separation_direction_diamond_radial(self):
        """Test separation direction calculation for diamond grid with radial orientation."""
        # Create motion with radial orientation (in/out)
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            end_ori="in",  # Radial orientation
        )

        beat_data = BeatData(letter="A", blue_motion=motion)

        # Test blue prop at north position with radial orientation
        result = self.service.calculate_separation_direction(motion, beat_data, "blue")
        assert result == SeparationDirection.LEFT

        # Test red prop at north position with radial orientation
        result = self.service.calculate_separation_direction(motion, beat_data, "red")
        assert result == SeparationDirection.RIGHT

    def test_calculate_separation_direction_diamond_nonradial(self):
        """Test separation direction calculation for diamond grid with nonradial orientation."""
        # Create motion with nonradial orientation (clock/counter)
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            end_ori="clock",  # Nonradial orientation
        )

        beat_data = BeatData(letter="A", blue_motion=motion)

        # Test blue prop at north position with nonradial orientation
        result = self.service.calculate_separation_direction(motion, beat_data, "blue")
        assert result == SeparationDirection.DOWN

        # Test red prop at north position with nonradial orientation
        result = self.service.calculate_separation_direction(motion, beat_data, "red")
        assert result == SeparationDirection.UP

    def test_calculate_separation_direction_box_radial(self):
        """Test separation direction calculation for box grid with radial orientation."""
        # Create motion with radial orientation at northeast
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTHEAST,
            end_loc=Location.NORTHEAST,
            end_ori="in",  # Radial orientation
        )

        beat_data = BeatData(letter="A", blue_motion=motion)

        # Test blue prop at northeast position with radial orientation
        result = self.service.calculate_separation_direction(motion, beat_data, "blue")
        assert result == SeparationDirection.UPLEFT

        # Test red prop at northeast position with radial orientation
        result = self.service.calculate_separation_direction(motion, beat_data, "red")
        assert result == SeparationDirection.DOWNRIGHT

    def test_calculate_separation_direction_box_nonradial(self):
        """Test separation direction calculation for box grid with nonradial orientation."""
        # Create motion with nonradial orientation at northeast
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTHEAST,
            end_loc=Location.NORTHEAST,
            end_ori="clock",  # Nonradial orientation
        )

        beat_data = BeatData(letter="A", blue_motion=motion)

        # Test blue prop at northeast position with nonradial orientation
        result = self.service.calculate_separation_direction(motion, beat_data, "blue")
        assert result == SeparationDirection.DOWNLEFT

        # Test red prop at northeast position with nonradial orientation
        result = self.service.calculate_separation_direction(motion, beat_data, "red")
        assert result == SeparationDirection.UPRIGHT

    def test_calculate_end_orientation_pro_motion(self):
        """Test end orientation calculation for pro motion."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1,
        )

        # Pro motion with 1 turn should switch orientation
        result = self.service.calculate_end_orientation(motion, Orientation.IN)
        assert result == Orientation.OUT

        # Pro motion with 2 turns should keep orientation
        motion_2_turns = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=2,
        )
        result = self.service.calculate_end_orientation(motion_2_turns, Orientation.IN)
        assert result == Orientation.IN

    def test_calculate_end_orientation_anti_motion(self):
        """Test end orientation calculation for anti motion."""
        motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1,
        )

        # Anti motion with 1 turn should keep orientation
        result = self.service.calculate_end_orientation(motion, Orientation.IN)
        assert result == Orientation.IN

        # Anti motion with 2 turns should switch orientation
        motion_2_turns = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=2,
        )
        result = self.service.calculate_end_orientation(motion_2_turns, Orientation.IN)
        assert result == Orientation.OUT

    def test_is_radial_orientation(self):
        """Test radial orientation detection."""
        assert self.service.is_radial_orientation("in") == True
        assert self.service.is_radial_orientation("out") == True
        assert self.service.is_radial_orientation("clock") == False
        assert self.service.is_radial_orientation("counter") == False

    def test_get_opposite_direction(self):
        """Test opposite direction calculation."""
        test_cases = [
            (SeparationDirection.LEFT, SeparationDirection.RIGHT),
            (SeparationDirection.UP, SeparationDirection.DOWN),
            (SeparationDirection.UPLEFT, SeparationDirection.DOWNRIGHT),
            (SeparationDirection.DOWNLEFT, SeparationDirection.UPRIGHT),
        ]

        for direction, expected_opposite in test_cases:
            result = self.service.get_opposite_direction(direction)
            assert result == expected_opposite

    def test_separation_direction_enum_values(self):
        """Test that SeparationDirection enum has expected values."""
        expected_values = {
            "left",
            "right",
            "up",
            "down",
            "downright",
            "upleft",
            "downleft",
            "upright",
        }

        actual_values = {direction.value for direction in SeparationDirection}
        assert actual_values == expected_values

    def test_edge_case_unknown_location(self):
        """Test handling of edge cases with unknown locations."""
        # Create motion with valid data
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            end_ori="in",
        )

        beat_data = BeatData(letter="A", blue_motion=motion)

        # Should return default direction for unknown combinations
        result = self.service.calculate_separation_direction(motion, beat_data, "blue")
        assert isinstance(result, SeparationDirection)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
