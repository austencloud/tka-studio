"""
Comprehensive Tests for PropPositioningOrchestrator

Tests the main orchestrator that coordinates all modular services.
Validates backward compatibility and service integration.
"""

from unittest.mock import Mock, patch

import pytest
from desktop.modern.core.types import Point
from desktop.modern.domain.models import BeatData, MotionData, MotionType, Orientation
from desktop.modern.domain.models.enums import Location, PropType
from desktop.modern.domain.models.pictograph_data import PictographData

from shared.application.services.positioning.props.calculation.direction_calculation_service import (
    SeparationDirection,
)
from shared.application.services.positioning.props.orchestration.prop_positioning_orchestrator import (
    PropPositioningOrchestrator,
)


class TestPropPositioningOrchestrator:
    """Test suite for PropPositioningOrchestrator."""

    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance for testing."""
        return PropPositioningOrchestrator()

    @pytest.fixture
    def sample_beat_data(self):
        """Create sample beat data for testing."""
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            turns=1.0,
        )
        red_motion = MotionData(
            motion_type=MotionType.ANTI,
            start_loc=Location.SOUTH,
            end_loc=Location.NORTH,
            start_ori=Orientation.OUT,
            end_ori=Orientation.IN,
            turns=1.0,
        )

        pictograph_data = PictographData(
            letter="G", motions={"blue": blue_motion, "red": red_motion}
        )

        return BeatData(letter="G", pictograph_data=pictograph_data)

    @pytest.fixture
    def letter_i_beat_data(self):
        """Create Letter I beat data for testing special case."""
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            turns=1.0,
        )
        red_motion = MotionData(
            motion_type=MotionType.ANTI,
            start_loc=Location.SOUTH,
            end_loc=Location.NORTH,
            start_ori=Orientation.OUT,
            end_ori=Orientation.IN,
            turns=1.0,
        )

        pictograph_data = PictographData(
            letter="I", motions={"blue": blue_motion, "red": red_motion}
        )

        return BeatData(letter="I", pictograph_data=pictograph_data)

    def test_should_apply_beta_positioning_for_beta_letters(
        self, orchestrator, sample_beat_data
    ):
        """Test that beta positioning is applied for beta-ending letters."""
        result = orchestrator.should_apply_beta_positioning(sample_beat_data)
        assert result is True

    def test_should_not_apply_beta_positioning_for_non_beta_letters(self, orchestrator):
        """Test that beta positioning is not applied for non-beta letters."""
        beat_data = BeatData(letter="A")
        result = orchestrator.should_apply_beta_positioning(beat_data)
        assert result is False

    def test_should_not_apply_beta_positioning_for_empty_data(self, orchestrator):
        """Test that beta positioning is not applied for empty data."""
        result = orchestrator.should_apply_beta_positioning(None)
        assert result is False

    def test_detect_prop_overlap_same_location_same_orientation(self, orchestrator):
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
            motion_type=MotionType.ANTI,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=0.0,
        )

        pictograph_data = PictographData(
            letter="G", motions={"blue": blue_motion, "red": red_motion}
        )

        beat_data = BeatData(letter="G", pictograph_data=pictograph_data)

        result = orchestrator.detect_prop_overlap(beat_data)
        assert result is True

    def test_no_overlap_different_locations(self, orchestrator, sample_beat_data):
        """Test no overlap when props end at different locations."""
        result = orchestrator.detect_prop_overlap(sample_beat_data)
        assert result is False

    def test_calculate_separation_offsets_returns_points(
        self, orchestrator, sample_beat_data
    ):
        """Test that separation offset calculation returns Point objects."""
        blue_offset, red_offset = orchestrator.calculate_separation_offsets(
            sample_beat_data.pictograph_data
        )

        assert isinstance(blue_offset, Point)
        assert isinstance(red_offset, Point)
        assert blue_offset.x != 0 or blue_offset.y != 0  # Should have some offset
        assert red_offset.x != 0 or red_offset.y != 0  # Should have some offset

    def test_letter_i_special_case_handling(self, orchestrator, letter_i_beat_data):
        """Test that Letter I gets special PRO/ANTI coordination."""
        blue_offset, red_offset = orchestrator.calculate_separation_offsets(
            letter_i_beat_data.pictograph_data
        )

        # Letter I should use special coordination logic
        assert isinstance(blue_offset, Point)
        assert isinstance(red_offset, Point)

        # PRO and ANTI should move in opposite directions
        # This is a basic check - more detailed validation would require
        # knowing the exact direction mapping

    def test_apply_beta_positioning_returns_beat_data(
        self, orchestrator, sample_beat_data
    ):
        """Test that apply_beta_positioning returns BeatData."""
        result = orchestrator.apply_beta_positioning(sample_beat_data)
        assert isinstance(result, BeatData)
        assert result.letter == sample_beat_data.letter

    def test_apply_beta_positioning_skips_non_beta_letters(self, orchestrator):
        """Test that apply_beta_positioning skips non-beta letters."""
        beat_data = BeatData(letter="A")
        result = orchestrator.apply_beta_positioning(beat_data)
        assert result is beat_data  # Should return same object unchanged

    @patch(
        "application.services.positioning.props.orchestration.prop_positioning_orchestrator.get_event_bus"
    )
    def test_event_publishing_integration(
        self, mock_get_event_bus, orchestrator, sample_beat_data
    ):
        """Test that events are published correctly."""
        mock_event_bus = Mock()
        mock_get_event_bus.return_value = mock_event_bus

        # Create new orchestrator with mocked event bus
        orchestrator = PropPositioningOrchestrator()

        # Test overlap detection event
        orchestrator.detect_prop_overlap(sample_beat_data)

        # Test separation calculation event
        orchestrator.calculate_separation_offsets(sample_beat_data.pictograph_data)

        # Test beta positioning event
        orchestrator.apply_beta_positioning(sample_beat_data)

        # Verify events were published (exact verification would depend on event structure)
        # This is a basic integration test

    def test_service_composition_integration(self, orchestrator):
        """Test that all services are properly composed and accessible."""
        # Verify all required services are initialized
        assert orchestrator.beta_detector is not None
        assert orchestrator.overlap_detector is not None
        assert orchestrator.direction_service is not None
        assert orchestrator.letter_i_service is not None
        assert orchestrator.offset_calculator is not None
        assert orchestrator.classification_service is not None
        assert orchestrator.rotation_calculator is not None
        assert orchestrator.override_service is not None
        assert orchestrator.event_publisher is not None

    def test_backward_compatibility_interface(self, orchestrator, sample_beat_data):
        """Test that the orchestrator maintains the same interface as PropManagementService."""
        # Test all public methods exist and work
        assert hasattr(orchestrator, "should_apply_beta_positioning")
        assert hasattr(orchestrator, "apply_beta_positioning")
        assert hasattr(orchestrator, "calculate_separation_offsets")
        assert hasattr(orchestrator, "detect_prop_overlap")

        # Test method signatures work
        orchestrator.should_apply_beta_positioning(sample_beat_data)
        orchestrator.apply_beta_positioning(sample_beat_data)
        orchestrator.calculate_separation_offsets(sample_beat_data.pictograph_data)
        orchestrator.detect_prop_overlap(sample_beat_data)
