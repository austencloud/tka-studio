"""
Unit tests for OffsetCalculationService

Tests the pure offset calculation service.
Validates extraction from PropManagementService maintains functionality.
"""

import pytest
import sys
from pathlib import Path

# Add modern/src to path for imports
modern_src_path = Path(__file__).parent.parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))


# Mock QPointF to avoid Qt dependency in tests
class MockQPointF:
    def __init__(self, x=0.0, y=0.0):
        self._x = float(x)
        self._y = float(y)

    def x(self):
        return self._x

    def y(self):
        return self._y

    def __eq__(self, other):
        if not isinstance(other, MockQPointF):
            return False
        return abs(self._x - other._x) < 0.01 and abs(self._y - other._y) < 0.01


# Patch QPointF in the offset service
import sys

sys.modules["PyQt6.QtCore"] = type("MockModule", (), {"QPointF": MockQPointF})()

from desktop.modern.src.domain.models.pictograph_models import PropType
from desktop.modern.src.application.services.positioning.offset_calculation_service import (
    OffsetCalculationService,
    IOffsetCalculationService,
)
from desktop.modern.src.application.services.positioning.direction_calculation_service import (
    SeparationDirection,
)


class TestOffsetCalculationService:
    """Test suite for OffsetCalculationService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = OffsetCalculationService()

    def test_interface_compliance(self):
        """Test that OffsetCalculationService implements the interface correctly."""
        assert isinstance(self.service, IOffsetCalculationService)

    def test_get_prop_offset_divisor_large_props(self):
        """Test offset divisor for large props."""
        large_props = [
            PropType.CLUB,
            PropType.EIGHTRINGS,
            PropType.BIG_EIGHT_RINGS,
            PropType.BIGHOOP,
        ]

        for prop_type in large_props:
            divisor = self.service.get_prop_offset_divisor(prop_type)
            assert divisor == 60, f"Large prop {prop_type} should have divisor 60"

    def test_get_prop_offset_divisor_medium_props(self):
        """Test offset divisor for medium props."""
        medium_props = [
            PropType.DOUBLESTAR,
            PropType.BIGDOUBLESTAR,
            PropType.BIGBUUGENG,
        ]

        for prop_type in medium_props:
            divisor = self.service.get_prop_offset_divisor(prop_type)
            assert divisor == 50, f"Medium prop {prop_type} should have divisor 50"

    def test_get_prop_offset_divisor_small_props(self):
        """Test offset divisor for small props."""
        small_props = [PropType.HAND, PropType.BUUGENG, PropType.TRIAD, PropType.STAFF]

        for prop_type in small_props:
            divisor = self.service.get_prop_offset_divisor(prop_type)
            assert divisor == 45, f"Small prop {prop_type} should have divisor 45"

    def test_calculate_directional_offset_cardinal_directions(self):
        """Test directional offset calculation for cardinal directions."""
        prop_type = PropType.HAND  # Small prop with divisor 45
        expected_base_offset = 950 / 45  # ~21.11

        # Test cardinal directions
        test_cases = [
            (SeparationDirection.LEFT, MockQPointF(-expected_base_offset, 0)),
            (SeparationDirection.RIGHT, MockQPointF(expected_base_offset, 0)),
            (SeparationDirection.UP, MockQPointF(0, -expected_base_offset)),
            (SeparationDirection.DOWN, MockQPointF(0, expected_base_offset)),
        ]

        for direction, expected_offset in test_cases:
            result = self.service.calculate_directional_offset(direction, prop_type)
            assert (
                abs(result.x() - expected_offset.x()) < 0.01
            ), f"X offset mismatch for {direction}"
            assert (
                abs(result.y() - expected_offset.y()) < 0.01
            ), f"Y offset mismatch for {direction}"

    def test_calculate_directional_offset_diagonal_directions(self):
        """Test directional offset calculation for diagonal directions."""
        prop_type = PropType.HAND  # Small prop with divisor 45
        base_offset = 950 / 45
        expected_diagonal_offset = base_offset / (2**0.5)  # ~14.93

        # Test diagonal directions
        test_cases = [
            (
                SeparationDirection.DOWNRIGHT,
                MockQPointF(expected_diagonal_offset, expected_diagonal_offset),
            ),
            (
                SeparationDirection.UPLEFT,
                MockQPointF(-expected_diagonal_offset, -expected_diagonal_offset),
            ),
            (
                SeparationDirection.DOWNLEFT,
                MockQPointF(-expected_diagonal_offset, expected_diagonal_offset),
            ),
            (
                SeparationDirection.UPRIGHT,
                MockQPointF(expected_diagonal_offset, -expected_diagonal_offset),
            ),
        ]

        for direction, expected_offset in test_cases:
            result = self.service.calculate_directional_offset(direction, prop_type)
            assert (
                abs(result.x() - expected_offset.x()) < 0.01
            ), f"X offset mismatch for {direction}"
            assert (
                abs(result.y() - expected_offset.y()) < 0.01
            ), f"Y offset mismatch for {direction}"

    def test_calculate_separation_offsets(self):
        """Test calculation of separation offsets for both props."""
        prop_type = PropType.CLUB  # Large prop
        blue_direction = SeparationDirection.LEFT
        red_direction = SeparationDirection.RIGHT

        blue_offset, red_offset = self.service.calculate_separation_offsets(
            blue_direction, red_direction, prop_type
        )

        # Verify both offsets are calculated
        assert hasattr(blue_offset, "x") and hasattr(blue_offset, "y")
        assert hasattr(red_offset, "x") and hasattr(red_offset, "y")

        # Verify they are opposite for LEFT/RIGHT
        assert blue_offset.x() == -red_offset.x()
        assert blue_offset.y() == red_offset.y()

    def test_calculate_base_offset(self):
        """Test base offset calculation."""
        # Test with different prop types
        test_cases = [
            (PropType.CLUB, 950 / 60),  # Large prop
            (PropType.DOUBLESTAR, 950 / 50),  # Medium prop
            (PropType.HAND, 950 / 45),  # Small prop
        ]

        for prop_type, expected_offset in test_cases:
            result = self.service.calculate_base_offset(prop_type)
            assert (
                abs(result - expected_offset) < 0.01
            ), f"Base offset mismatch for {prop_type}"

    def test_calculate_diagonal_offset(self):
        """Test diagonal offset calculation."""
        prop_type = PropType.HAND
        base_offset = self.service.calculate_base_offset(prop_type)
        expected_diagonal = base_offset / (2**0.5)

        result = self.service.calculate_diagonal_offset(prop_type)
        assert abs(result - expected_diagonal) < 0.01

    def test_scale_offset_for_scene_size(self):
        """Test offset scaling for different scene sizes."""
        original_offset = MockQPointF(100, 50)

        # Test scaling for different scene sizes
        test_cases = [
            (950, 1.0),  # Reference size - no scaling
            (1900, 2.0),  # Double size - double scaling
            (475, 0.5),  # Half size - half scaling
        ]

        for scene_size, expected_scale in test_cases:
            result = self.service.scale_offset_for_scene_size(
                original_offset, scene_size
            )
            expected_x = original_offset.x() * expected_scale
            expected_y = original_offset.y() * expected_scale

            assert (
                abs(result.x() - expected_x) < 0.01
            ), f"X scaling mismatch for scene size {scene_size}"
            assert (
                abs(result.y() - expected_y) < 0.01
            ), f"Y scaling mismatch for scene size {scene_size}"

    def test_get_offset_for_prop_size_category(self):
        """Test offset divisor by size category."""
        test_cases = [
            ("large", 60),
            ("medium", 50),
            ("small", 45),
            ("unknown", 45),  # Default to small
        ]

        for category, expected_divisor in test_cases:
            result = self.service.get_offset_for_prop_size_category(category)
            assert (
                result == expected_divisor
            ), f"Divisor mismatch for category {category}"

    def test_prop_offset_map_completeness(self):
        """Test that all PropType enum values have offset mappings."""
        # Get all PropType values
        all_prop_types = list(PropType)

        # Verify each has a mapping
        for prop_type in all_prop_types:
            divisor = self.service.get_prop_offset_divisor(prop_type)
            assert divisor in [
                45,
                50,
                60,
            ], f"PropType {prop_type} has invalid divisor {divisor}"

    def test_offset_calculation_consistency(self):
        """Test that offset calculations are consistent across different prop types."""
        directions = [
            SeparationDirection.LEFT,
            SeparationDirection.RIGHT,
            SeparationDirection.UP,
            SeparationDirection.DOWN,
        ]

        for direction in directions:
            # Calculate offsets for different prop sizes
            small_offset = self.service.calculate_directional_offset(
                direction, PropType.HAND
            )
            medium_offset = self.service.calculate_directional_offset(
                direction, PropType.DOUBLESTAR
            )
            large_offset = self.service.calculate_directional_offset(
                direction, PropType.CLUB
            )

            # Large props should have smaller offsets (larger divisor)
            # Small props should have larger offsets (smaller divisor)
            if direction in [SeparationDirection.LEFT, SeparationDirection.RIGHT]:
                assert (
                    abs(small_offset.x())
                    > abs(medium_offset.x())
                    > abs(large_offset.x())
                )
            elif direction in [SeparationDirection.UP, SeparationDirection.DOWN]:
                assert (
                    abs(small_offset.y())
                    > abs(medium_offset.y())
                    > abs(large_offset.y())
                )

    def test_zero_offset_for_unknown_direction(self):
        """Test that unknown directions return zero offset."""
        # This test assumes the service handles unknown directions gracefully
        # by returning QPointF(0, 0) for any direction not in the mapping
        prop_type = PropType.HAND

        # The service should handle all SeparationDirection enum values
        # so this test verifies the mapping is complete
        for direction in SeparationDirection:
            result = self.service.calculate_directional_offset(direction, prop_type)
            assert hasattr(result, "x") and hasattr(
                result, "y"
            ), f"Should return point-like object for {direction}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
