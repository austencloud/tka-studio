"""
Comprehensive Tests for PropOverlapDetector

Tests the prop overlap detection service in isolation.
"""

import pytest

from domain.models import BeatData, MotionData, MotionType, Orientation
from domain.models.enums import Location
from domain.models.pictograph_data import PictographData

from application.services.positioning.props.detection.prop_overlap_detector import (
    PropOverlapDetector,
)


class TestPropOverlapDetector:
    """Comprehensive test suite for PropOverlapDetector."""

    @pytest.fixture
    def detector(self):
        """Create detector instance for testing."""
        return PropOverlapDetector()

    @pytest.fixture
    def sample_motion_data(self):
        """Create sample motion data for testing."""
        return MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            turns=1.0,
        )

    def test_initialization(self, detector):
        """Test that detector initializes correctly."""
        assert detector is not None

    def test_switch_orientation(self, detector):
        """Test orientation switching functionality."""
        assert detector.switch_orientation(Orientation.IN) == Orientation.OUT
        assert detector.switch_orientation(Orientation.OUT) == Orientation.IN

    @pytest.mark.parametrize("motion_type,turns,start_ori,expected_ori", [
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
    ])
    def test_calculate_end_orientation(self, detector, motion_type, turns, start_ori, expected_ori):
        """Test end orientation calculation for various motion types and turns."""
        motion = MotionData(
            motion_type=motion_type,
            turns=turns,
            start_ori=start_ori,
            end_ori=start_ori,  # Will be calculated
        )
        
        result = detector.calculate_end_orientation(motion, start_ori)
        assert result == expected_ori

    def test_calculate_end_orientation_with_float_turns(self, detector):
        """Test end orientation calculation with float turns (should convert to int)."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            turns=1.5,  # Should be treated as 1
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )
        
        result = detector.calculate_end_orientation(motion, Orientation.IN)
        assert result == Orientation.OUT

    def test_calculate_end_orientation_with_invalid_turns(self, detector):
        """Test end orientation calculation with invalid turns (outside 0-3)."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            turns=5,  # Invalid
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )
        
        result = detector.calculate_end_orientation(motion, Orientation.IN)
        assert result == Orientation.IN  # Should return start orientation

    def test_detect_overlap_same_location_same_orientation(self, detector):
        """Test overlap detection when props end at same location with same orientation."""
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=0.0,
        )
        red_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.EAST,
            end_loc=Location.SOUTH,  # Same end location
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=0.0,
        )
        
        pictograph_data = PictographData(
            letter="G",
            motions={"blue": blue_motion, "red": red_motion}
        )
        beat_data = BeatData(pictograph_data=pictograph_data)
        
        result = detector.detect_prop_overlap(beat_data)
        assert result is True

    def test_detect_overlap_same_location_different_orientation(self, detector):
        """Test no overlap when props end at same location but different orientations."""
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=0.0,
        )
        red_motion = MotionData(
            motion_type=MotionType.ANTI,
            start_loc=Location.EAST,
            end_loc=Location.SOUTH,  # Same end location
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,  # Different calculated end orientation
            turns=0.0,
        )
        
        pictograph_data = PictographData(
            letter="G",
            motions={"blue": blue_motion, "red": red_motion}
        )
        beat_data = BeatData(pictograph_data=pictograph_data)
        
        result = detector.detect_prop_overlap(beat_data)
        assert result is False

    def test_detect_overlap_different_locations(self, detector):
        """Test no overlap when props end at different locations."""
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=0.0,
        )
        red_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.EAST,
            end_loc=Location.WEST,  # Different end location
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=0.0,
        )
        
        pictograph_data = PictographData(
            letter="G",
            motions={"blue": blue_motion, "red": red_motion}
        )
        beat_data = BeatData(pictograph_data=pictograph_data)
        
        result = detector.detect_prop_overlap(beat_data)
        assert result is False

    def test_detect_overlap_missing_motion_data(self, detector):
        """Test no overlap when motion data is missing."""
        # Test with no pictograph data
        beat_data = BeatData()
        assert detector.detect_prop_overlap(beat_data) is False
        
        # Test with pictograph data but no motions
        pictograph_data = PictographData(letter="G")
        beat_data = BeatData(pictograph_data=pictograph_data)
        assert detector.detect_prop_overlap(beat_data) is False
        
        # Test with only blue motion
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=0.0,
        )
        pictograph_data = PictographData(
            letter="G",
            motions={"blue": blue_motion}
        )
        beat_data = BeatData(pictograph_data=pictograph_data)
        assert detector.detect_prop_overlap(beat_data) is False

    def test_detect_overlap_complex_motion_calculation(self, detector):
        """Test overlap detection with complex motion calculations."""
        # Both motions should end with same calculated orientation
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            turns=1.0,  # PRO with 1 turn: IN -> OUT
        )
        red_motion = MotionData(
            motion_type=MotionType.ANTI,
            start_loc=Location.EAST,
            end_loc=Location.SOUTH,  # Same end location
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=1.0,  # ANTI with 1 turn: IN -> IN
        )
        
        pictograph_data = PictographData(
            letter="G",
            motions={"blue": blue_motion, "red": red_motion}
        )
        beat_data = BeatData(pictograph_data=pictograph_data)
        
        result = detector.detect_prop_overlap(beat_data)
        assert result is False  # Different calculated orientations

    def test_performance_with_many_calls(self, detector, sample_motion_data):
        """Test performance with many repeated calls."""
        import time
        
        pictograph_data = PictographData(
            letter="G",
            motions={"blue": sample_motion_data, "red": sample_motion_data}
        )
        beat_data = BeatData(pictograph_data=pictograph_data)
        
        start_time = time.time()
        for _ in range(1000):
            detector.detect_prop_overlap(beat_data)
        end_time = time.time()
        
        # Should complete 1,000 calls in under 1 second
        assert (end_time - start_time) < 1.0

    def test_edge_case_orientations(self, detector):
        """Test edge cases with different orientation combinations."""
        orientations = [Orientation.IN, Orientation.OUT, Orientation.CLOCK, Orientation.COUNTER]
        
        for start_ori in orientations:
            motion = MotionData(
                motion_type=MotionType.PRO,
                turns=0.0,
                start_ori=start_ori,
                end_ori=start_ori,
            )
            
            result = detector.calculate_end_orientation(motion, start_ori)
            # With 0 turns and PRO motion, should return start orientation
            assert result == start_ori
