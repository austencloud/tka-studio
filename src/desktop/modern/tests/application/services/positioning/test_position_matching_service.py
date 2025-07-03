"""
Tests for Position Matching Service

This module tests the extracted position matching business logic service
to ensure it correctly handles position calculations and end position extraction.
"""

import pytest
from unittest.mock import Mock

from application.services.positioning.position_matching_service import (
    PositionMatchingService,
)
from domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)


class TestPositionMatchingService:
    """Test cases for PositionMatchingService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = PositionMatchingService()

    def test_initialization(self):
        """Test service initialization."""
        assert self.service is not None
        assert hasattr(self.service, "_location_to_position_map")
        assert len(self.service._location_to_position_map) > 0

    def test_positions_map_contains_expected_mappings(self):
        """Test that the positions map contains expected mappings."""
        # Test alpha positions
        assert self.service._location_to_position_map[("s", "n")] == "alpha1"
        assert self.service._location_to_position_map[("sw", "ne")] == "alpha2"
        assert self.service._location_to_position_map[("w", "e")] == "alpha3"

        # Test beta positions
        assert self.service._location_to_position_map[("n", "n")] == "beta1"
        assert self.service._location_to_position_map[("s", "s")] == "beta5"

        # Test gamma positions
        assert self.service._location_to_position_map[("w", "n")] == "gamma1"
        assert self.service._location_to_position_map[("s", "e")] == "gamma11"

    def test_extract_end_position_direct_field(self):
        """Test extracting end position from direct end_pos field."""
        beat_data = {"end_pos": "alpha1"}
        result = self.service.extract_end_position(beat_data)
        assert result == "alpha1"

    def test_extract_end_position_metadata(self):
        """Test extracting end position from metadata."""
        beat_data = {"metadata": {"end_pos": "beta5"}}
        result = self.service.extract_end_position(beat_data)
        assert result == "beta5"

    def test_extract_end_position_from_motions(self):
        """Test extracting end position from motion attributes."""
        beat_data = {
            "blue_attributes": {"end_loc": "s"},
            "red_attributes": {"end_loc": "n"},
        }
        result = self.service.extract_end_position(beat_data)
        assert result == "alpha1"  # (s, n) -> alpha1

    def test_extract_end_position_fallback(self):
        """Test fallback when no position data is available."""
        beat_data = {}
        result = self.service.extract_end_position(beat_data)
        assert result == "alpha1"  # Default fallback

    def test_calculate_end_position_from_motions_valid(self):
        """Test calculating end position from valid motion data."""
        beat_data = {
            "blue_attributes": {"end_loc": "w"},
            "red_attributes": {"end_loc": "e"},
        }
        result = self.service.calculate_end_position_from_motions(beat_data)
        assert result == "alpha3"  # (w, e) -> alpha3

    def test_calculate_end_position_from_motions_invalid(self):
        """Test calculating end position with invalid motion data."""
        beat_data = {
            "blue_attributes": {"end_loc": "invalid"},
            "red_attributes": {"end_loc": "also_invalid"},
        }
        result = self.service.calculate_end_position_from_motions(beat_data)
        assert result is None

    def test_calculate_end_position_from_motions_missing_data(self):
        """Test calculating end position with missing motion data."""
        beat_data = {"blue_attributes": {}}
        result = self.service.calculate_end_position_from_motions(beat_data)
        assert result is None

    def test_get_position_from_locations_valid(self):
        """Test getting position from valid locations."""
        result = self.service.get_position_from_locations("n", "s")
        assert result == "alpha5"

    def test_get_position_from_locations_invalid(self):
        """Test getting position from invalid locations."""
        result = self.service.get_position_from_locations("invalid", "also_invalid")
        assert result is None

    def test_has_motion_attributes_true(self):
        """Test checking motion attributes when they exist."""
        beat_data = {
            "blue_attributes": {"end_loc": "s"},
            "red_attributes": {"end_loc": "n"},
        }
        result = self.service.has_motion_attributes(beat_data)
        assert result is True

    def test_has_motion_attributes_false_missing_blue(self):
        """Test checking motion attributes when blue attributes are missing."""
        beat_data = {"red_attributes": {"end_loc": "n"}}
        result = self.service.has_motion_attributes(beat_data)
        assert result is False

    def test_has_motion_attributes_false_missing_red(self):
        """Test checking motion attributes when red attributes are missing."""
        beat_data = {"blue_attributes": {"end_loc": "s"}}
        result = self.service.has_motion_attributes(beat_data)
        assert result is False

    def test_has_motion_attributes_false_missing_end_loc(self):
        """Test checking motion attributes when end_loc is missing."""
        beat_data = {"blue_attributes": {}, "red_attributes": {"end_loc": "n"}}
        result = self.service.has_motion_attributes(beat_data)
        assert result is False

    def test_extract_modern_end_position_from_metadata(self):
        """Test extracting end position from modern BeatData metadata."""
        beat_data = BeatData(letter="A", metadata={"end_pos": "gamma5"})
        result = self.service.extract_modern_end_position(beat_data)
        assert result == "gamma5"

    def test_extract_modern_end_position_from_motions(self):
        """Test extracting end position from modern BeatData motions."""
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
            start_ori="in",
            end_ori="out",
        )
        red_motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.SOUTH,
            end_loc=Location.NORTH,
            turns=1.0,
            start_ori="in",
            end_ori="out",
        )
        beat_data = BeatData(letter="A", blue_motion=blue_motion, red_motion=red_motion)
        result = self.service.extract_modern_end_position(beat_data)
        assert result == "alpha1"  # (s, n) -> alpha1

    def test_extract_modern_end_position_fallback(self):
        """Test extracting end position from modern BeatData with fallback."""
        beat_data = BeatData(letter="A")
        result = self.service.extract_modern_end_position(beat_data)
        assert result == "beta5"  # Default fallback

    def test_error_handling_in_extract_end_position(self):
        """Test error handling in extract_end_position method."""
        # Test with None input
        result = self.service.extract_end_position(None)
        assert result is None  # Should handle gracefully and return None on error

    def test_error_handling_in_has_motion_attributes(self):
        """Test error handling in has_motion_attributes method."""
        # Test with None input
        result = self.service.has_motion_attributes(None)
        assert result is False  # Should handle gracefully

    def test_error_handling_in_get_position_from_locations(self):
        """Test error handling in get_position_from_locations method."""
        # Test with None inputs
        result = self.service.get_position_from_locations(None, None)
        assert result is None  # Should handle gracefully


if __name__ == "__main__":
    pytest.main([__file__])
