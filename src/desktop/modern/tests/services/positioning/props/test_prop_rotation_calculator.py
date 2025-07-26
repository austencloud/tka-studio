"""
Comprehensive Tests for PropRotationCalculator

Tests the prop rotation calculation service in isolation.
"""

import pytest
from desktop.modern.domain.models import MotionData, MotionType, Orientation
from desktop.modern.domain.models.enums import Location, RotationDirection

from shared.application.services.positioning.props.calculation.prop_rotation_calculator import (
    PropRotationCalculator,
)


class TestPropRotationCalculator:
    """Comprehensive test suite for PropRotationCalculator."""

    @pytest.fixture
    def calculator(self):
        """Create calculator instance for testing."""
        return PropRotationCalculator()

    @pytest.fixture
    def sample_motion(self):
        """Create sample motion data for testing."""
        return MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            turns=1.0,
        )

    def test_initialization(self, calculator):
        """Test that calculator initializes correctly."""
        assert calculator is not None
        angle_map = calculator.get_rotation_angle_map()
        assert Orientation.IN in angle_map
        assert Orientation.OUT in angle_map

    def test_rotation_angle_map_structure(self, calculator):
        """Test that rotation angle map has correct structure."""
        angle_map = calculator.get_rotation_angle_map()

        # Should have entries for IN and OUT orientations
        assert Orientation.IN in angle_map
        assert Orientation.OUT in angle_map

        # Each orientation should have entries for diamond grid locations
        for orientation in [Orientation.IN, Orientation.OUT]:
            orientation_map = angle_map[orientation]
            assert Location.NORTH in orientation_map
            assert Location.SOUTH in orientation_map
            assert Location.EAST in orientation_map
            assert Location.WEST in orientation_map

    @pytest.mark.parametrize(
        "location,expected_angle",
        [
            (Location.NORTH, 90),
            (Location.SOUTH, 270),
            (Location.WEST, 0),
            (Location.EAST, 180),
        ],
    )
    def test_rotation_angles_for_in_orientation(
        self, calculator, location, expected_angle
    ):
        """Test rotation angles for IN orientation at diamond grid locations."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=location,
            end_loc=location,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=0.0,  # No turns to maintain IN orientation
        )

        angle = calculator.calculate_prop_rotation_angle(motion, Orientation.IN)
        assert angle == expected_angle

    @pytest.mark.parametrize(
        "location,expected_angle",
        [
            (Location.NORTH, 270),
            (Location.SOUTH, 90),
            (Location.WEST, 180),
            (Location.EAST, 0),
        ],
    )
    def test_rotation_angles_for_out_orientation(
        self, calculator, location, expected_angle
    ):
        """Test rotation angles for OUT orientation at diamond grid locations."""
        motion = MotionData(
            motion_type=MotionType.ANTI,
            start_loc=location,
            end_loc=location,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            turns=0.0,  # ANTI with 0 turns: IN -> OUT
        )

        angle = calculator.calculate_prop_rotation_angle(motion, Orientation.IN)
        assert angle == expected_angle

    def test_calculate_prop_rotation_angle_returns_float(
        self, calculator, sample_motion
    ):
        """Test that rotation angle calculation returns a float."""
        angle = calculator.calculate_prop_rotation_angle(sample_motion)
        assert isinstance(angle, float)

    @pytest.mark.parametrize(
        "motion_type,turns,start_ori,expected_end_ori",
        [
            (MotionType.PRO, 0, Orientation.IN, Orientation.IN),
            (MotionType.PRO, 1, Orientation.IN, Orientation.OUT),
            (MotionType.PRO, 2, Orientation.IN, Orientation.IN),
            (MotionType.PRO, 3, Orientation.IN, Orientation.OUT),
            (MotionType.ANTI, 0, Orientation.IN, Orientation.OUT),
            (MotionType.ANTI, 1, Orientation.IN, Orientation.IN),
            (MotionType.ANTI, 2, Orientation.IN, Orientation.OUT),
            (MotionType.ANTI, 3, Orientation.IN, Orientation.IN),
            (MotionType.STATIC, 0, Orientation.IN, Orientation.IN),
            (MotionType.STATIC, 1, Orientation.IN, Orientation.OUT),
            (MotionType.DASH, 0, Orientation.IN, Orientation.OUT),
            (MotionType.DASH, 1, Orientation.IN, Orientation.IN),
        ],
    )
    def test_end_orientation_calculation(
        self, calculator, motion_type, turns, start_ori, expected_end_ori
    ):
        """Test end orientation calculation for various motion types and turns."""
        motion = MotionData(
            motion_type=motion_type,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            start_ori=start_ori,
            end_ori=start_ori,  # Will be calculated
            turns=turns,
        )

        # Calculate rotation angle (which internally calculates end orientation)
        angle = calculator.calculate_prop_rotation_angle(motion, start_ori)

        # Verify the angle corresponds to the expected end orientation
        angle_map = calculator.get_rotation_angle_map()
        expected_angle = angle_map[expected_end_ori][Location.NORTH]
        assert angle == expected_angle

    def test_half_turn_orientation_calculation(self, calculator):
        """Test that half turns (1.5) are handled correctly, not truncated."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=1.5,  # Half turn - should switch orientation
        )

        angle = calculator.calculate_prop_rotation_angle(motion, Orientation.IN)

        # With 1.5 turns (half turn): IN -> OUT (orientation switches)
        angle_map = calculator.get_rotation_angle_map()
        expected_angle = angle_map[Orientation.OUT][Location.NORTH]
        assert angle == expected_angle

    @pytest.mark.parametrize(
        "turns,expected_switches",
        [
            (0.5, True),  # Half turn - should switch
            (1.0, True),  # Whole turn (odd) - should switch for PRO
            (1.5, True),  # Half turn - should switch
            (2.0, False),  # Whole turn (even) - should preserve for PRO
            (2.5, True),  # Half turn - should switch
            (3.0, True),  # Whole turn (odd) - should switch for PRO
        ],
    )
    def test_legacy_orientation_logic_pro_motion(
        self, calculator, turns, expected_switches
    ):
        """Test that orientation calculation follows legacy logic for PRO motions."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=turns,
        )

        angle = calculator.calculate_prop_rotation_angle(motion, Orientation.IN)
        angle_map = calculator.get_rotation_angle_map()

        if expected_switches:
            expected_angle = angle_map[Orientation.OUT][Location.NORTH]
        else:
            expected_angle = angle_map[Orientation.IN][Location.NORTH]

        assert (
            angle == expected_angle
        ), f"Failed for {turns} turns: expected {'OUT' if expected_switches else 'IN'}"

    def test_invalid_turns_returns_start_orientation(self, calculator):
        """Test that invalid turns (outside 0-3) return start orientation angle."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=5,  # Invalid
        )

        angle = calculator.calculate_prop_rotation_angle(motion, Orientation.IN)

        # Should return angle for start orientation
        angle_map = calculator.get_rotation_angle_map()
        expected_angle = angle_map[Orientation.IN][Location.NORTH]
        assert angle == expected_angle

    def test_unknown_location_returns_default_angle(self, calculator):
        """Test that unknown locations return default angle (0)."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTHEAST,  # Not in diamond grid
            end_loc=Location.NORTHEAST,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=0.0,
        )

        angle = calculator.calculate_prop_rotation_angle(motion, Orientation.IN)
        assert angle == 0.0

    def test_get_rotation_angle_map_returns_copy(self, calculator):
        """Test that get_rotation_angle_map returns a copy, not the original."""
        map1 = calculator.get_rotation_angle_map()
        map2 = calculator.get_rotation_angle_map()

        # Should be equal but not the same object
        assert map1 == map2
        assert map1 is not map2

        # Modifying one should not affect the other
        map1[Orientation.IN][Location.NORTH] = 999
        assert map2[Orientation.IN][Location.NORTH] != 999

    def test_angle_values_are_valid_degrees(self, calculator):
        """Test that all angle values are valid degrees (0-359)."""
        angle_map = calculator.get_rotation_angle_map()

        for orientation_map in angle_map.values():
            for angle in orientation_map.values():
                assert 0 <= angle < 360
                assert isinstance(angle, (int, float))

    def test_in_out_orientation_symmetry(self, calculator):
        """Test that IN and OUT orientations have symmetric angle relationships."""
        angle_map = calculator.get_rotation_angle_map()

        in_map = angle_map[Orientation.IN]
        out_map = angle_map[Orientation.OUT]

        # For each location, OUT should be 180 degrees different from IN
        for location in [Location.NORTH, Location.SOUTH, Location.EAST, Location.WEST]:
            in_angle = in_map[location]
            out_angle = out_map[location]

            # Calculate the difference, accounting for 360-degree wrap-around
            diff = abs(in_angle - out_angle)
            if diff > 180:
                diff = 360 - diff

            assert (
                diff == 180
            ), f"Location {location}: IN={in_angle}, OUT={out_angle}, diff={diff}"

    def test_performance_with_many_calculations(self, calculator, sample_motion):
        """Test performance with many repeated calculations."""
        import time

        start_time = time.time()
        for _ in range(10000):
            calculator.calculate_prop_rotation_angle(sample_motion)
        end_time = time.time()

        # Should complete 10,000 calculations in under 1 second
        assert (end_time - start_time) < 1.0

    def test_consistency_across_multiple_calls(self, calculator, sample_motion):
        """Test that repeated calculations return consistent results."""
        angle1 = calculator.calculate_prop_rotation_angle(sample_motion)
        angle2 = calculator.calculate_prop_rotation_angle(sample_motion)
        angle3 = calculator.calculate_prop_rotation_angle(sample_motion)

        assert angle1 == angle2 == angle3

    def test_all_motion_types_supported(self, calculator):
        """Test that all motion types are supported."""
        motion_types = [
            MotionType.PRO,
            MotionType.ANTI,
            MotionType.STATIC,
            MotionType.DASH,
        ]

        for motion_type in motion_types:
            motion = MotionData(
                motion_type=motion_type,
                start_loc=Location.NORTH,
                end_loc=Location.NORTH,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
                turns=0.0,
            )

            angle = calculator.calculate_prop_rotation_angle(motion)
            assert isinstance(angle, float)
            assert 0 <= angle < 360

    def test_default_start_orientation(self, calculator):
        """Test that default start orientation is IN."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=0.0,
        )

        # Call without specifying start orientation (should default to IN)
        angle_default = calculator.calculate_prop_rotation_angle(motion)
        angle_explicit = calculator.calculate_prop_rotation_angle(
            motion, Orientation.IN
        )

        assert angle_default == angle_explicit
