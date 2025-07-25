"""
Comprehensive Tests for OffsetCalculationService

Tests the offset calculation service in isolation.
"""

import pytest
import math

from core.types import Point
from domain.models.enums import PropType

from application.services.positioning.props.calculation.offset_calculation_service import (
    OffsetCalculationService,
)
from application.services.positioning.props.calculation.direction_calculation_service import (
    SeparationDirection,
)


class TestOffsetCalculationService:
    """Comprehensive test suite for OffsetCalculationService."""

    @pytest.fixture
    def calculator(self):
        """Create calculator instance for testing."""
        return OffsetCalculationService()

    def test_initialization(self, calculator):
        """Test that calculator initializes correctly."""
        assert calculator is not None
        assert calculator._scene_reference_size == 950
        assert calculator._large_offset_divisor == 60
        assert calculator._medium_offset_divisor == 50
        assert calculator._small_offset_divisor == 45

    def test_prop_offset_divisor_mapping(self, calculator):
        """Test that prop types are mapped to correct offset divisors."""
        # Large props
        assert calculator.get_prop_offset_divisor(PropType.CLUB) == 60
        assert calculator.get_prop_offset_divisor(PropType.EIGHTRINGS) == 60
        assert calculator.get_prop_offset_divisor(PropType.BIGHOOP) == 60
        
        # Medium props
        assert calculator.get_prop_offset_divisor(PropType.DOUBLESTAR) == 50
        assert calculator.get_prop_offset_divisor(PropType.BIGDOUBLESTAR) == 50
        assert calculator.get_prop_offset_divisor(PropType.BIGBUUGENG) == 50
        
        # Small props
        assert calculator.get_prop_offset_divisor(PropType.HAND) == 45
        assert calculator.get_prop_offset_divisor(PropType.BUUGENG) == 45
        assert calculator.get_prop_offset_divisor(PropType.TRIAD) == 45

    def test_calculate_base_offset(self, calculator):
        """Test base offset calculation."""
        # Large prop: 950 / 60 = 15.833...
        base_offset = calculator.calculate_base_offset(PropType.CLUB)
        assert abs(base_offset - (950 / 60)) < 0.001
        
        # Medium prop: 950 / 50 = 19.0
        base_offset = calculator.calculate_base_offset(PropType.DOUBLESTAR)
        assert abs(base_offset - 19.0) < 0.001
        
        # Small prop: 950 / 45 = 21.111...
        base_offset = calculator.calculate_base_offset(PropType.HAND)
        assert abs(base_offset - (950 / 45)) < 0.001

    def test_calculate_diagonal_offset(self, calculator):
        """Test diagonal offset calculation."""
        base_offset = calculator.calculate_base_offset(PropType.HAND)
        diagonal_offset = calculator.calculate_diagonal_offset(PropType.HAND)
        
        expected_diagonal = base_offset / math.sqrt(2)
        assert abs(diagonal_offset - expected_diagonal) < 0.001

    @pytest.mark.parametrize("direction,expected_x,expected_y", [
        (SeparationDirection.LEFT, -1, 0),
        (SeparationDirection.RIGHT, 1, 0),
        (SeparationDirection.UP, 0, -1),
        (SeparationDirection.DOWN, 0, 1),
    ])
    def test_calculate_directional_offset_cardinal_directions(self, calculator, direction, expected_x, expected_y):
        """Test directional offset calculation for cardinal directions."""
        offset = calculator.calculate_directional_offset(direction, PropType.HAND)
        
        base_offset = calculator.calculate_base_offset(PropType.HAND)
        expected_offset = Point(expected_x * base_offset, expected_y * base_offset)
        
        assert isinstance(offset, Point)
        assert abs(offset.x - expected_offset.x) < 0.001
        assert abs(offset.y - expected_offset.y) < 0.001

    @pytest.mark.parametrize("direction", [
        SeparationDirection.DOWNRIGHT,
        SeparationDirection.UPLEFT,
        SeparationDirection.DOWNLEFT,
        SeparationDirection.UPRIGHT,
    ])
    def test_calculate_directional_offset_diagonal_directions(self, calculator, direction):
        """Test directional offset calculation for diagonal directions."""
        offset = calculator.calculate_directional_offset(direction, PropType.HAND)
        
        diagonal_offset = calculator.calculate_diagonal_offset(PropType.HAND)
        
        assert isinstance(offset, Point)
        # All diagonal offsets should have the same magnitude
        magnitude = math.sqrt(offset.x**2 + offset.y**2)
        assert abs(magnitude - diagonal_offset) < 0.001

    def test_calculate_directional_offset_diagonal_coordinates(self, calculator):
        """Test specific diagonal direction coordinates."""
        diagonal_offset = calculator.calculate_diagonal_offset(PropType.HAND)
        
        # Test each diagonal direction
        downright = calculator.calculate_directional_offset(SeparationDirection.DOWNRIGHT, PropType.HAND)
        assert abs(downright.x - diagonal_offset) < 0.001
        assert abs(downright.y - diagonal_offset) < 0.001
        
        upleft = calculator.calculate_directional_offset(SeparationDirection.UPLEFT, PropType.HAND)
        assert abs(upleft.x - (-diagonal_offset)) < 0.001
        assert abs(upleft.y - (-diagonal_offset)) < 0.001
        
        downleft = calculator.calculate_directional_offset(SeparationDirection.DOWNLEFT, PropType.HAND)
        assert abs(downleft.x - (-diagonal_offset)) < 0.001
        assert abs(downleft.y - diagonal_offset) < 0.001
        
        upright = calculator.calculate_directional_offset(SeparationDirection.UPRIGHT, PropType.HAND)
        assert abs(upright.x - diagonal_offset) < 0.001
        assert abs(upright.y - (-diagonal_offset)) < 0.001

    def test_calculate_separation_offsets(self, calculator):
        """Test calculation of separation offsets for both props."""
        blue_offset, red_offset = calculator.calculate_separation_offsets(
            SeparationDirection.LEFT,
            SeparationDirection.RIGHT,
            PropType.HAND
        )
        
        assert isinstance(blue_offset, Point)
        assert isinstance(red_offset, Point)
        
        # Should be opposite directions
        base_offset = calculator.calculate_base_offset(PropType.HAND)
        assert abs(blue_offset.x - (-base_offset)) < 0.001
        assert abs(red_offset.x - base_offset) < 0.001
        assert blue_offset.y == 0
        assert red_offset.y == 0

    def test_different_prop_types_different_offsets(self, calculator):
        """Test that different prop types produce different offset magnitudes."""
        hand_offset = calculator.calculate_directional_offset(SeparationDirection.RIGHT, PropType.HAND)
        club_offset = calculator.calculate_directional_offset(SeparationDirection.RIGHT, PropType.CLUB)
        
        # Club should have smaller offset than hand (larger divisor = smaller offset)
        assert club_offset.x < hand_offset.x

    def test_unknown_prop_type_uses_default(self, calculator):
        """Test that unknown prop types use the default small offset divisor."""
        # Create a mock prop type that's not in the mapping
        class UnknownPropType:
            pass
        
        unknown_prop = UnknownPropType()
        divisor = calculator.get_prop_offset_divisor(unknown_prop)
        assert divisor == calculator._small_offset_divisor

    def test_zero_offset_for_invalid_direction(self, calculator):
        """Test that invalid directions return zero offset."""
        # Create a mock direction that's not in the mapping
        class InvalidDirection:
            pass
        
        invalid_direction = InvalidDirection()
        offset = calculator.calculate_directional_offset(invalid_direction, PropType.HAND)
        
        assert isinstance(offset, Point)
        assert offset.x == 0
        assert offset.y == 0

    def test_offset_scaling_with_scene_size(self, calculator):
        """Test that offsets scale correctly with scene reference size."""
        original_size = calculator._scene_reference_size
        
        # Double the scene size
        calculator._scene_reference_size = 1900
        
        large_scene_offset = calculator.calculate_directional_offset(SeparationDirection.RIGHT, PropType.HAND)
        
        # Reset to original
        calculator._scene_reference_size = original_size
        
        normal_scene_offset = calculator.calculate_directional_offset(SeparationDirection.RIGHT, PropType.HAND)
        
        # Large scene should produce double the offset
        assert abs(large_scene_offset.x - (2 * normal_scene_offset.x)) < 0.001

    def test_performance_with_many_calculations(self, calculator):
        """Test performance with many repeated calculations."""
        import time
        
        start_time = time.time()
        for _ in range(10000):
            calculator.calculate_directional_offset(SeparationDirection.RIGHT, PropType.HAND)
        end_time = time.time()
        
        # Should complete 10,000 calculations in under 1 second
        assert (end_time - start_time) < 1.0

    def test_offset_consistency(self, calculator):
        """Test that repeated calculations return consistent results."""
        direction = SeparationDirection.DOWNRIGHT
        prop_type = PropType.CLUB
        
        offset1 = calculator.calculate_directional_offset(direction, prop_type)
        offset2 = calculator.calculate_directional_offset(direction, prop_type)
        
        assert offset1.x == offset2.x
        assert offset1.y == offset2.y

    def test_all_separation_directions_covered(self, calculator):
        """Test that all separation directions are handled."""
        all_directions = [
            SeparationDirection.LEFT,
            SeparationDirection.RIGHT,
            SeparationDirection.UP,
            SeparationDirection.DOWN,
            SeparationDirection.DOWNRIGHT,
            SeparationDirection.UPLEFT,
            SeparationDirection.DOWNLEFT,
            SeparationDirection.UPRIGHT,
        ]
        
        for direction in all_directions:
            offset = calculator.calculate_directional_offset(direction, PropType.HAND)
            assert isinstance(offset, Point)
            # None of the valid directions should return zero offset
            assert offset.x != 0 or offset.y != 0

    def test_mathematical_correctness_of_diagonal_offsets(self, calculator):
        """Test that diagonal offsets maintain correct mathematical relationships."""
        base_offset = calculator.calculate_base_offset(PropType.HAND)
        diagonal_offset = calculator.calculate_diagonal_offset(PropType.HAND)
        
        # Diagonal offset should be base_offset / sqrt(2)
        expected_diagonal = base_offset / math.sqrt(2)
        assert abs(diagonal_offset - expected_diagonal) < 0.001
        
        # Test that diagonal direction magnitudes are correct
        downright = calculator.calculate_directional_offset(SeparationDirection.DOWNRIGHT, PropType.HAND)
        magnitude = math.sqrt(downright.x**2 + downright.y**2)
        assert abs(magnitude - diagonal_offset) < 0.001
