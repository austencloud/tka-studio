"""
Tests for Individual Modular Services

Tests to validate each extracted service works correctly in isolation.
"""

import pytest

from desktop.modern.core.types import Point
from desktop.modern.domain.models import BeatData, MotionData, MotionType, Orientation
from desktop.modern.domain.models.enums import Location, PropType

from shared.application.services.positioning.props.detection.beta_positioning_detector import (
    BetaPositioningDetector,
)
from shared.application.services.positioning.props.detection.prop_overlap_detector import (
    PropOverlapDetector,
)
from shared.application.services.positioning.props.calculation.offset_calculation_service import (
    OffsetCalculationService,
)
from shared.application.services.positioning.props.calculation.direction_calculation_service import (
    DirectionCalculationService,
    SeparationDirection,
)
from shared.application.services.positioning.props.calculation.prop_rotation_calculator import (
    PropRotationCalculator,
)
from shared.application.services.positioning.props.specialization.letter_i_positioning_service import (
    LetterIPositioningService,
)


class TestBetaPositioningDetector:
    """Test suite for BetaPositioningDetector."""

    @pytest.fixture
    def detector(self):
        return BetaPositioningDetector()

    def test_detects_beta_ending_letters(self, detector):
        """Test detection of beta-ending letters."""
        beta_letters = ["G", "H", "I", "J", "K", "L", "Y", "Z", "Y-", "Z-", "Ψ", "Ψ-", "β"]
        
        for letter in beta_letters:
            beat_data = BeatData(letter=letter)
            assert detector.should_apply_beta_positioning(beat_data) is True

    def test_rejects_non_beta_letters(self, detector):
        """Test rejection of non-beta letters."""
        non_beta_letters = ["A", "B", "C", "D", "E", "F"]
        
        for letter in non_beta_letters:
            beat_data = BeatData(letter=letter)
            assert detector.should_apply_beta_positioning(beat_data) is False

    def test_handles_empty_data(self, detector):
        """Test handling of empty or invalid data."""
        assert detector.should_apply_beta_positioning(None) is False
        assert detector.should_apply_beta_positioning(BeatData()) is False


class TestPropOverlapDetector:
    """Test suite for PropOverlapDetector."""

    @pytest.fixture
    def detector(self):
        return PropOverlapDetector()

    def test_calculates_end_orientation_pro_motion(self, detector):
        """Test end orientation calculation for PRO motion."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            turns=1.0,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )
        
        result = detector.calculate_end_orientation(motion, Orientation.IN)
        assert result == Orientation.OUT

    def test_calculates_end_orientation_anti_motion(self, detector):
        """Test end orientation calculation for ANTI motion."""
        motion = MotionData(
            motion_type=MotionType.ANTI,
            turns=1.0,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )
        
        result = detector.calculate_end_orientation(motion, Orientation.IN)
        assert result == Orientation.IN

    def test_switches_orientation(self, detector):
        """Test orientation switching."""
        assert detector.switch_orientation(Orientation.IN) == Orientation.OUT
        assert detector.switch_orientation(Orientation.OUT) == Orientation.IN


class TestOffsetCalculationService:
    """Test suite for OffsetCalculationService."""

    @pytest.fixture
    def calculator(self):
        return OffsetCalculationService()

    def test_calculates_directional_offset(self, calculator):
        """Test directional offset calculation."""
        offset = calculator.calculate_directional_offset(
            SeparationDirection.RIGHT, PropType.HAND
        )
        
        assert isinstance(offset, Point)
        assert offset.x > 0  # Should move right
        assert offset.y == 0  # No vertical movement

    def test_calculates_diagonal_offset(self, calculator):
        """Test diagonal offset calculation."""
        offset = calculator.calculate_directional_offset(
            SeparationDirection.DOWNRIGHT, PropType.HAND
        )
        
        assert isinstance(offset, Point)
        assert offset.x > 0  # Should move right
        assert offset.y > 0  # Should move down

    def test_different_prop_types_different_offsets(self, calculator):
        """Test that different prop types produce different offsets."""
        hand_offset = calculator.calculate_directional_offset(
            SeparationDirection.RIGHT, PropType.HAND
        )
        club_offset = calculator.calculate_directional_offset(
            SeparationDirection.RIGHT, PropType.CLUB
        )
        
        # Club should have larger offset than hand
        assert club_offset.x > hand_offset.x


class TestDirectionCalculationService:
    """Test suite for DirectionCalculationService."""

    @pytest.fixture
    def calculator(self):
        return DirectionCalculationService()

    def test_detects_grid_mode(self, calculator):
        """Test grid mode detection."""
        assert calculator.detect_grid_mode(Location.NORTH) == "diamond"
        assert calculator.detect_grid_mode(Location.NORTHEAST) == "box"

    def test_determines_radial_orientation(self, calculator):
        """Test radial orientation determination."""
        assert calculator.is_radial_orientation(Orientation.IN) is True
        assert calculator.is_radial_orientation(Orientation.OUT) is True
        assert calculator.is_radial_orientation(Orientation.CLOCK) is False
        assert calculator.is_radial_orientation(Orientation.COUNTER) is False


class TestPropRotationCalculator:
    """Test suite for PropRotationCalculator."""

    @pytest.fixture
    def calculator(self):
        return PropRotationCalculator()

    def test_calculates_rotation_angle(self, calculator):
        """Test rotation angle calculation."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            end_loc=Location.NORTH,
            turns=0.0,
        )
        
        angle = calculator.calculate_prop_rotation_angle(motion, Orientation.IN)
        assert isinstance(angle, float)
        assert 0 <= angle < 360

    def test_different_locations_different_angles(self, calculator):
        """Test that different locations produce different angles."""
        motion_north = MotionData(motion_type=MotionType.PRO, end_loc=Location.NORTH, turns=0.0)
        motion_south = MotionData(motion_type=MotionType.PRO, end_loc=Location.SOUTH, turns=0.0)
        
        angle_north = calculator.calculate_prop_rotation_angle(motion_north)
        angle_south = calculator.calculate_prop_rotation_angle(motion_south)
        
        assert angle_north != angle_south


class TestLetterIPositioningService:
    """Test suite for LetterIPositioningService."""

    @pytest.fixture
    def service(self):
        return LetterIPositioningService()

    def test_calculates_opposite_directions(self, service):
        """Test opposite direction calculation."""
        assert service.get_opposite_direction(SeparationDirection.LEFT) == SeparationDirection.RIGHT
        assert service.get_opposite_direction(SeparationDirection.UP) == SeparationDirection.DOWN
        assert service.get_opposite_direction(SeparationDirection.UPLEFT) == SeparationDirection.DOWNRIGHT

    def test_letter_i_pro_anti_coordination(self, service):
        """Test Letter I PRO/ANTI coordination."""
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            end_loc=Location.NORTH,
            end_ori=Orientation.IN,
        )
        red_motion = MotionData(
            motion_type=MotionType.ANTI,
            end_loc=Location.SOUTH,
            end_ori=Orientation.OUT,
        )
        
        blue_dir, red_dir = service.calculate_letter_i_directions(blue_motion, red_motion)
        
        # PRO and ANTI should get opposite directions
        assert blue_dir != red_dir
        assert service.get_opposite_direction(blue_dir) == red_dir
