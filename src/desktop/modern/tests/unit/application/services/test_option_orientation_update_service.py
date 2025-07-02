"""
TEST LIFECYCLE: UNIT
PURPOSE: Test OptionOrientationUpdateService orientation calculation functionality
AUTHOR: @ai-agent
"""

import pytest
from unittest.mock import Mock, patch

from domain.models.core_models import (
    BeatData,
    SequenceData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
    Orientation,
)
from application.services.option_picker.orientation_update_service import (
    OptionOrientationUpdateService,
)


@pytest.mark.unit
class TestOptionOrientationUpdateService:
    """Test suite for OptionOrientationUpdateService"""

    @pytest.fixture
    def orientation_calculator_mock(self):
        """Mock orientation calculator"""
        mock = Mock()
        mock.calculate_end_orientation.return_value = Orientation.OUT
        return mock

    @pytest.fixture
    def service(self, orientation_calculator_mock):
        """Create service instance with mocked calculator"""
        return OptionOrientationUpdateService(orientation_calculator_mock)

    @pytest.fixture
    def sample_motion_data(self):
        """Create sample motion data"""
        return MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
            start_ori="in",
            end_ori="out",
        )

    @pytest.fixture
    def sample_beat_data(self, sample_motion_data):
        """Create sample beat data with motion"""
        return BeatData(
            letter="A",
            blue_motion=sample_motion_data,
            red_motion=sample_motion_data,
        )

    @pytest.fixture
    def sample_sequence(self, sample_beat_data):
        """Create sample sequence with one beat"""
        return SequenceData(
            name="Test Sequence",
            beats=[sample_beat_data],
        )

    @pytest.fixture
    def sample_options(self):
        """Create sample option beats"""
        option1 = BeatData(
            letter="B",
            blue_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.NORTH,
                turns=2.0,
                start_ori="in",  # Default orientation
                end_ori="in",  # Default orientation
            ),
            red_motion=MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.SOUTH,
                end_loc=Location.SOUTH,
                turns=0.0,
                start_ori="in",  # Default orientation
                end_ori="in",  # Default orientation
            ),
        )

        option2 = BeatData(
            letter="C",
            blue_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.EAST,
                turns=1.5,
                start_ori="in",  # Default orientation
                end_ori="in",  # Default orientation
            ),
            red_motion=MotionData(
                motion_type=MotionType.DASH,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.WEST,
                turns=0.5,
                start_ori="in",  # Default orientation
                end_ori="in",  # Default orientation
            ),
        )

        return [option1, option2]

    def test_update_option_orientations_basic(
        self, service, sample_sequence, sample_options
    ):
        """Test basic orientation update functionality"""
        # Act
        updated_options = service.update_option_orientations(
            sample_sequence, sample_options
        )

        # Assert
        assert len(updated_options) == 2

        # Check that start orientations were updated from sequence context
        assert (
            updated_options[0].blue_motion.start_ori == "out"
        )  # From last beat's end_ori
        assert (
            updated_options[0].red_motion.start_ori == "out"
        )  # From last beat's end_ori
        assert (
            updated_options[1].blue_motion.start_ori == "out"
        )  # From last beat's end_ori
        assert (
            updated_options[1].red_motion.start_ori == "out"
        )  # From last beat's end_ori

        # Check that end orientations were calculated (mocked to return OUT)
        assert updated_options[0].blue_motion.end_ori == "out"
        assert updated_options[0].red_motion.end_ori == "out"
        assert updated_options[1].blue_motion.end_ori == "out"
        assert updated_options[1].red_motion.end_ori == "out"

    def test_update_option_orientations_empty_sequence(self, service, sample_options):
        """Test handling of empty sequence"""
        empty_sequence = SequenceData(name="Empty", beats=[])

        # Act
        updated_options = service.update_option_orientations(
            empty_sequence, sample_options
        )

        # Assert - should return original options unchanged
        assert updated_options == sample_options

    def test_update_option_orientations_blank_last_beat(self, service, sample_options):
        """Test handling of sequence with blank last beat"""
        # Create sequence with blank last beat
        blank_beat = BeatData(letter="BLANK", beat_number=2, is_blank=True)
        valid_beat = BeatData(
            letter="A",
            beat_number=1,
            blue_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=1.0,
                start_ori="clock",
                end_ori="counter",
            ),
            red_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.EAST,
                end_loc=Location.WEST,
                turns=2.0,
                start_ori="out",
                end_ori="in",
            ),
        )

        sequence = SequenceData(name="Test", beats=[valid_beat, blank_beat])

        # Act
        updated_options = service.update_option_orientations(sequence, sample_options)

        # Assert - should use second-to-last beat's orientations
        assert (
            updated_options[0].blue_motion.start_ori == "counter"
        )  # From valid beat's blue end_ori
        assert (
            updated_options[0].red_motion.start_ori == "in"
        )  # From valid beat's red end_ori

    def test_orientation_calculator_called_correctly(
        self, service, sample_sequence, sample_options
    ):
        """Test that orientation calculator is called with correct parameters"""
        # Act
        service.update_option_orientations(sample_sequence, sample_options)

        # Assert - calculator should be called for each motion
        assert (
            service.orientation_calculator.calculate_end_orientation.call_count == 4
        )  # 2 options × 2 motions each

    def test_string_to_orientation_conversion(self, service):
        """Test orientation string conversion"""
        assert service._string_to_orientation("in") == Orientation.IN
        assert service._string_to_orientation("out") == Orientation.OUT
        assert service._string_to_orientation("clock") == Orientation.CLOCK
        assert service._string_to_orientation("counter") == Orientation.COUNTER
        assert (
            service._string_to_orientation("invalid") == Orientation.IN
        )  # Default fallback
