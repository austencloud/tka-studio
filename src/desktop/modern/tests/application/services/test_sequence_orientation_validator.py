"""
Test Suite for Sequence Orientation Validator

Tests the critical bug fix for orientation service that affects option picker's display logic.
Verifies that the sequence orientation validator correctly:
1. Extracts actual end orientations from sequence context
2. Validates orientation continuity between pictographs
3. Provides accurate starting orientations for new pictograph options
4. Fixes orientation discontinuities in sequences
"""

from unittest.mock import Mock, patch

import pytest
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.enums import (
    GridPosition,
    Location,
    MotionType,
    Orientation,
    RotationDirection,
)
from desktop.modern.domain.models.grid_data import GridData
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.prop_data import PropData, PropType
from desktop.modern.domain.models.sequence_data import SequenceData

from shared.application.services.sequence.sequence_orientation_validator import (
    SequenceOrientationValidator,
)


class TestSequenceOrientationValidator:
    """Test suite for the sequence orientation validator service."""

    @pytest.fixture
    def validator(self):
        """Create a sequence orientation validator instance."""
        return SequenceOrientationValidator()

    @pytest.fixture
    def sample_motion_blue_in_to_out(self):
        """Create a sample blue motion from IN to OUT orientation."""
        return MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )

    @pytest.fixture
    def sample_motion_red_out_to_clock(self):
        """Create a sample red motion from OUT to CLOCK orientation."""
        return MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.SOUTH,
            end_loc=Location.EAST,
            turns=0.5,
            start_ori=Orientation.OUT,
            end_ori=Orientation.CLOCK,
        )

    @pytest.fixture
    def sample_pictograph_data(
        self, sample_motion_blue_in_to_out, sample_motion_red_out_to_clock
    ):
        """Create sample pictograph data with motions."""
        return PictographData(
            grid_data=GridData(),
            start_position=GridPosition.ALPHA1,
            end_position=GridPosition.BETA2,
            motions={
                "blue": sample_motion_blue_in_to_out,
                "red": sample_motion_red_out_to_clock,
            },
            props={
                "blue": PropData(prop_type=PropType.STAFF, orientation=Orientation.IN),
                "red": PropData(prop_type=PropType.STAFF, orientation=Orientation.OUT),
            },
        )

    @pytest.fixture
    def sample_beat_data(self, sample_pictograph_data):
        """Create sample beat data."""
        return BeatData(
            beat_number=1,
            pictograph_data=sample_pictograph_data,
            is_blank=False,
        )

    @pytest.fixture
    def sample_sequence_data(self, sample_beat_data):
        """Create sample sequence data with one beat."""
        return SequenceData(
            name="test_sequence",
            beats=[sample_beat_data],
        )

    def test_get_sequence_end_orientations_empty_sequence(self, validator):
        """Test getting end orientations from empty sequence returns defaults."""
        empty_sequence = SequenceData(name="empty", beats=[])

        end_orientations = validator.get_sequence_end_orientations(empty_sequence)

        assert end_orientations["blue"] == Orientation.IN
        assert end_orientations["red"] == Orientation.OUT

    def test_get_sequence_end_orientations_valid_sequence(
        self, validator, sample_sequence_data
    ):
        """Test getting end orientations from valid sequence."""
        end_orientations = validator.get_sequence_end_orientations(sample_sequence_data)

        # Should extract actual end orientations from the last beat
        assert end_orientations["blue"] == Orientation.OUT
        assert end_orientations["red"] == Orientation.CLOCK

    def test_validate_sequence_orientation_continuity_single_beat(
        self, validator, sample_sequence_data
    ):
        """Test validation with single beat (should pass)."""
        is_valid, errors = validator.validate_sequence_orientation_continuity(
            sample_sequence_data
        )

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_sequence_orientation_continuity_valid_sequence(self, validator):
        """Test validation with valid orientation continuity."""
        # Create two beats with proper orientation continuity
        beat1_motions = {
            "blue": MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=1.0,
                start_ori=Orientation.IN,
                end_ori=Orientation.OUT,
            ),
            "red": MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.EAST,
                turns=0.5,
                start_ori=Orientation.OUT,
                end_ori=Orientation.CLOCK,
            ),
        }

        beat2_motions = {
            "blue": MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.SOUTH,
                end_loc=Location.SOUTH,
                turns=0.0,
                start_ori=Orientation.OUT,  # Matches beat1 blue end_ori
                end_ori=Orientation.OUT,
            ),
            "red": MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.EAST,
                end_loc=Location.EAST,
                turns=0.0,
                start_ori=Orientation.CLOCK,  # Matches beat1 red end_ori
                end_ori=Orientation.CLOCK,
            ),
        }

        beat1 = BeatData(
            beat_number=1,
            pictograph_data=PictographData(
                grid_data=GridData(),
                start_position=GridPosition.ALPHA1,
                end_position=GridPosition.BETA2,
                motions=beat1_motions,
            ),
            is_blank=False,
        )

        beat2 = BeatData(
            beat_number=2,
            pictograph_data=PictographData(
                grid_data=GridData(),
                start_position=GridPosition.BETA2,
                end_position=GridPosition.GAMMA3,
                motions=beat2_motions,
            ),
            is_blank=False,
        )

        sequence = SequenceData(name="valid_sequence", beats=[beat1, beat2])

        is_valid, errors = validator.validate_sequence_orientation_continuity(sequence)

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_sequence_orientation_continuity_invalid_sequence(self, validator):
        """Test validation with invalid orientation continuity."""
        # Create two beats with orientation discontinuity
        beat1_motions = {
            "blue": MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=1.0,
                start_ori=Orientation.IN,
                end_ori=Orientation.OUT,
            ),
        }

        beat2_motions = {
            "blue": MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.SOUTH,
                end_loc=Location.SOUTH,
                turns=0.0,
                start_ori=Orientation.IN,  # WRONG! Should be OUT to match beat1 end_ori
                end_ori=Orientation.IN,
            ),
        }

        beat1 = BeatData(
            beat_number=1,
            pictograph_data=PictographData(
                grid_data=GridData(),
                start_position=GridPosition.ALPHA1,
                end_position=GridPosition.BETA2,
                motions=beat1_motions,
            ),
            is_blank=False,
        )

        beat2 = BeatData(
            beat_number=2,
            pictograph_data=PictographData(
                grid_data=GridData(),
                start_position=GridPosition.BETA2,
                end_position=GridPosition.GAMMA3,
                motions=beat2_motions,
            ),
            is_blank=False,
        )

        sequence = SequenceData(name="invalid_sequence", beats=[beat1, beat2])

        is_valid, errors = validator.validate_sequence_orientation_continuity(sequence)

        assert is_valid is False
        assert len(errors) > 0
        assert "Orientation discontinuity in blue" in errors[0]

    def test_calculate_option_start_orientations(self, validator, sample_sequence_data):
        """Test calculating correct start orientations for options."""
        # Create sample options with default orientations
        option1 = PictographData(
            grid_data=GridData(),
            start_position=GridPosition.BETA2,
            end_position=GridPosition.GAMMA3,
            motions={
                "blue": MotionData(
                    motion_type=MotionType.STATIC,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.SOUTH,
                    end_loc=Location.SOUTH,
                    turns=0.0,
                    start_ori=Orientation.IN,  # Default - should be updated
                    end_ori=Orientation.IN,
                ),
                "red": MotionData(
                    motion_type=MotionType.STATIC,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.SOUTH,
                    end_loc=Location.SOUTH,
                    turns=0.0,
                    start_ori=Orientation.OUT,  # Default - should be updated
                    end_ori=Orientation.OUT,
                ),
            },
            props={
                "blue": PropData(prop_type=PropType.STAFF, orientation=Orientation.IN),
                "red": PropData(prop_type=PropType.STAFF, orientation=Orientation.OUT),
            },
        )

        options = [option1]

        with patch(
            "application.services.positioning.arrows.calculation.orientation_calculator.OrientationCalculator"
        ) as mock_calc_class:
            mock_calc = Mock()
            mock_calc_class.return_value = mock_calc
            # Mock the end orientation calculation
            mock_calc.calculate_end_orientation.return_value = Orientation.OUT

            updated_options = validator.calculate_option_start_orientations(
                sample_sequence_data, options
            )

        assert len(updated_options) == 1
        updated_option = updated_options[0]

        # Verify that start orientations were updated to match sequence end orientations
        assert (
            updated_option.motions["blue"].start_ori == Orientation.OUT
        )  # From sequence
        assert (
            updated_option.motions["red"].start_ori == Orientation.CLOCK
        )  # From sequence

        # Verify that props were also updated
        assert updated_option.props["blue"].orientation == Orientation.OUT
        assert updated_option.props["red"].orientation == Orientation.CLOCK
