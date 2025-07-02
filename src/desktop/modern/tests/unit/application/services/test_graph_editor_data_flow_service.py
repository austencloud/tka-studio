"""
TEST LIFECYCLE: UNIT
PURPOSE: Test GraphEditorDataFlowService core functionality
AUTHOR: @ai-agent
"""

import pytest
from unittest.mock import Mock, MagicMock
from PyQt6.QtCore import QObject

from application.services.graph_editor_data_flow_service import (
    GraphEditorDataFlowService,
)
from domain.models.core_models import (
    BeatData,
    SequenceData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)


@pytest.mark.unit
class TestGraphEditorDataFlowService:
    """Test the graph editor data flow service"""

    @pytest.fixture
    def data_flow_service(self):
        """Create a data flow service for testing"""
        return GraphEditorDataFlowService()

    @pytest.fixture
    def sample_beat_data(self):
        """Create sample beat data for testing"""
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
        )
        red_motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            turns=0.5,
        )
        return BeatData(beat_number=1, blue_motion=blue_motion, red_motion=red_motion)

    @pytest.fixture
    def sample_sequence_data(self, sample_beat_data):
        """Create sample sequence data for testing"""
        return SequenceData(name="Test Sequence", beats=[sample_beat_data])

    def test_service_initialization(self, data_flow_service):
        """Test that the service initializes correctly"""
        assert isinstance(data_flow_service, QObject)
        assert data_flow_service._current_sequence is None
        assert data_flow_service._current_beat_index is None
        assert data_flow_service._sequence_service is None

    def test_set_context(self, data_flow_service, sample_sequence_data):
        """Test setting sequence and beat context"""
        data_flow_service.set_context(sample_sequence_data, 0)

        assert data_flow_service._current_sequence == sample_sequence_data
        assert data_flow_service._current_beat_index == 0

    def test_process_turn_change_blue_motion(self, data_flow_service, sample_beat_data):
        """Test processing turn changes for blue motion"""
        # Set up signal spy
        signal_spy = Mock()
        data_flow_service.beat_data_updated.connect(signal_spy)

        # Process turn change
        updated_beat = data_flow_service.process_turn_change(
            sample_beat_data, "blue", 2.5
        )

        # Verify beat data was updated
        assert updated_beat.blue_motion.turns == 2.5
        assert updated_beat.red_motion.turns == 0.5  # Unchanged

        # Verify signal was emitted
        signal_spy.assert_called_once_with(updated_beat, 0)

    def test_process_turn_change_red_motion(self, data_flow_service, sample_beat_data):
        """Test processing turn changes for red motion"""
        # Set up signal spy
        signal_spy = Mock()
        data_flow_service.pictograph_refresh_needed.connect(signal_spy)

        # Process turn change
        updated_beat = data_flow_service.process_turn_change(
            sample_beat_data, "red", 1.75
        )

        # Verify beat data was updated
        assert updated_beat.red_motion.turns == 1.75
        assert updated_beat.blue_motion.turns == 1.0  # Unchanged

        # Verify signal was emitted
        signal_spy.assert_called_once_with(updated_beat)

    def test_process_turn_change_with_sequence_context(
        self, data_flow_service, sample_sequence_data, sample_beat_data
    ):
        """Test processing turn changes with sequence context"""
        # Set context
        data_flow_service.set_context(sample_sequence_data, 0)

        # Set up signal spy
        signal_spy = Mock()
        data_flow_service.sequence_modified.connect(signal_spy)

        # Process turn change
        updated_beat = data_flow_service.process_turn_change(
            sample_beat_data, "blue", 3.0
        )

        # Verify sequence was updated
        assert data_flow_service._current_sequence.beats[0].blue_motion.turns == 3.0

        # Verify signal was emitted
        signal_spy.assert_called_once()

    def test_process_orientation_change_blue_motion(
        self, data_flow_service, sample_beat_data
    ):
        """Test processing orientation changes for blue motion"""
        # Process orientation change
        updated_beat = data_flow_service.process_orientation_change(
            sample_beat_data, "blue", "anti"
        )

        # Verify beat data was updated
        assert updated_beat.blue_motion.motion_type == MotionType.ANTI
        assert updated_beat.red_motion.motion_type == MotionType.ANTI  # Unchanged

    def test_process_orientation_change_invalid_type(
        self, data_flow_service, sample_beat_data
    ):
        """Test processing orientation changes with invalid motion type"""
        # Process orientation change with invalid type
        updated_beat = data_flow_service.process_orientation_change(
            sample_beat_data, "blue", "invalid_type"
        )

        # Verify beat data was unchanged
        assert updated_beat == sample_beat_data

    def test_determine_panel_mode_none_beat(self, data_flow_service):
        """Test panel mode determination with None beat data"""
        panel_mode = data_flow_service.determine_panel_mode(None)
        assert panel_mode == "orientation"

    def test_determine_panel_mode_start_position(self, data_flow_service):
        """Test panel mode determination for start position"""
        # Use beat_number=1 but add metadata to indicate start position
        start_beat = BeatData(beat_number=1, metadata={"is_start_position": True})
        panel_mode = data_flow_service.determine_panel_mode(start_beat)
        assert panel_mode == "orientation"

    def test_determine_panel_mode_regular_beat(
        self, data_flow_service, sample_beat_data
    ):
        """Test panel mode determination for regular beat"""
        panel_mode = data_flow_service.determine_panel_mode(sample_beat_data)
        assert panel_mode == "turns"

    def test_get_current_sequence(self, data_flow_service, sample_sequence_data):
        """Test getting current sequence"""
        assert data_flow_service.get_current_sequence() is None

        data_flow_service.set_context(sample_sequence_data, 0)
        assert data_flow_service.get_current_sequence() == sample_sequence_data

    def test_get_current_beat_index(self, data_flow_service, sample_sequence_data):
        """Test getting current beat index"""
        assert data_flow_service.get_current_beat_index() is None

        data_flow_service.set_context(sample_sequence_data, 2)
        assert data_flow_service.get_current_beat_index() == 2
