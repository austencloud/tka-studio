"""
Integration tests for Graph Editor functionality

Tests the complete data flow from beat selection through modification to UI updates.
"""
from __future__ import annotations

from pathlib import Path
import sys
from unittest.mock import Mock

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication
import pytest


# Add modern/src to path for imports
modern_src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from application.services.graph_editor.graph_editor_data_flow_manager import (
    GraphEditorDataFlowManager as GraphEditorDataFlowService,
)
from application.services.graph_editor.graph_editor_hotkey_manager import (
    GraphEditorHotkeyManager as GraphEditorHotkeyService,
)
from core.interfaces.workbench_services import IGraphEditorService
from domain.models.beat_data import BeatData
from domain.models.enums import Location, MotionType, RotationDirection
from domain.models.motion_models import MotionData
from domain.models.sequence_data import SequenceData


class TestGraphEditorIntegration:
    """Integration tests for the complete graph editor workflow"""

    @pytest.fixture
    def qapp(self):
        """Create QApplication for Qt tests"""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        return app
        # Don't quit the app as it might be used by other tests

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
        return BeatData(
            beat_number=1,
            blue_motion=blue_motion,
            red_motion=red_motion,
        )

    @pytest.fixture
    def sample_sequence_data(self, sample_beat_data):
        """Create sample sequence data for testing"""
        return SequenceData(name="Test Sequence", beats=[sample_beat_data])

    @pytest.fixture
    def mock_graph_service(self):
        """Create a mock graph service"""
        service = Mock(spec=IGraphEditorService)
        service.get_selected_beat.return_value = None
        service.apply_turn_adjustment.return_value = True
        service.apply_orientation_adjustment.return_value = True
        return service

    @pytest.fixture
    def data_flow_service(self):
        """Create data flow service for testing"""
        return GraphEditorDataFlowService()

    @pytest.fixture
    def hotkey_service(self, mock_graph_service):
        """Create hotkey service for testing"""
        return GraphEditorHotkeyService(mock_graph_service)

    def test_data_flow_turn_change_propagation(
        self, data_flow_service, sample_beat_data, sample_sequence_data
    ):
        """Test that turn changes propagate through the data flow service"""
        # Set up context
        data_flow_service.set_context(sample_sequence_data, 0)

        # Set up signal spies
        beat_updated_spy = Mock()
        pictograph_refresh_spy = Mock()
        sequence_modified_spy = Mock()

        data_flow_service.beat_data_updated.connect(beat_updated_spy)
        data_flow_service.pictograph_refresh_needed.connect(pictograph_refresh_spy)
        data_flow_service.sequence_modified.connect(sequence_modified_spy)

        # Process turn change
        updated_beat = data_flow_service.process_turn_change(
            sample_beat_data, "blue", 2.5
        )

        # Verify data was updated
        assert updated_beat.blue_motion.turns == 2.5
        assert updated_beat.red_motion.turns == 0.5  # Unchanged

        # Verify signals were emitted
        beat_updated_spy.assert_called_once_with(updated_beat, 0)
        pictograph_refresh_spy.assert_called_once_with(updated_beat)
        sequence_modified_spy.assert_called_once()

    def test_hotkey_service_wasd_movement(self, hotkey_service, sample_beat_data):
        """Test WASD movement through hotkey service"""
        # Mock selected beat
        hotkey_service.graph_service.get_selected_beat.return_value = sample_beat_data

        # Set up signal spy
        arrow_moved_spy = Mock()
        hotkey_service.arrow_moved.connect(arrow_moved_spy)

        # Create W key event
        key_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_W, Qt.KeyboardModifier.NoModifier
        )

        # Handle key event
        handled = hotkey_service.handle_key_event(key_event)

        # Verify handling
        assert handled is True
        arrow_moved_spy.assert_called_once_with("blue", 0, -5)  # Up movement

    def test_hotkey_service_special_commands(self, hotkey_service, sample_beat_data):
        """Test special command keys (X, Z, C)"""
        # Mock selected beat
        hotkey_service.graph_service.get_selected_beat.return_value = sample_beat_data

        # Set up signal spies
        rotation_spy = Mock()
        placement_removal_spy = Mock()
        prop_placement_spy = Mock()

        hotkey_service.rotation_override_requested.connect(rotation_spy)
        hotkey_service.special_placement_removal_requested.connect(
            placement_removal_spy
        )
        hotkey_service.prop_placement_override_requested.connect(prop_placement_spy)

        # Test X key (rotation override)
        x_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_X, Qt.KeyboardModifier.NoModifier
        )
        assert hotkey_service.handle_key_event(x_event) is True
        rotation_spy.assert_called_once_with("blue")

        # Test Z key (special placement removal)
        z_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_Z, Qt.KeyboardModifier.NoModifier
        )
        assert hotkey_service.handle_key_event(z_event) is True
        placement_removal_spy.assert_called_once_with("blue")

        # Test C key (prop placement override)
        c_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_C, Qt.KeyboardModifier.NoModifier
        )
        assert hotkey_service.handle_key_event(c_event) is True
        prop_placement_spy.assert_called_once_with("blue")

    def test_panel_mode_determination(self, data_flow_service):
        """Test panel mode determination logic"""
        # Test None beat
        assert data_flow_service.determine_panel_mode(None) == "orientation"

        # Test start position beat
        start_beat = BeatData(beat_number=1, metadata={"is_start_position": True})
        assert data_flow_service.determine_panel_mode(start_beat) == "orientation"

        # Test regular beat
        regular_beat = BeatData(beat_number=2)
        assert data_flow_service.determine_panel_mode(regular_beat) == "turns"

    def test_orientation_change_propagation(self, data_flow_service, sample_beat_data):
        """Test orientation changes propagate correctly"""
        # Set up signal spy
        beat_updated_spy = Mock()
        data_flow_service.beat_data_updated.connect(beat_updated_spy)

        # Process orientation change
        updated_beat = data_flow_service.process_orientation_change(
            sample_beat_data, "blue", "anti"
        )

        # Verify data was updated
        assert updated_beat.blue_motion.motion_type == MotionType.ANTI
        assert updated_beat.red_motion.motion_type == MotionType.ANTI  # Unchanged

        # Verify signal was emitted
        beat_updated_spy.assert_called_once_with(updated_beat, 0)

    def test_invalid_orientation_handling(self, data_flow_service, sample_beat_data):
        """Test handling of invalid orientation values"""
        # Process invalid orientation change
        updated_beat = data_flow_service.process_orientation_change(
            sample_beat_data, "blue", "invalid_motion_type"
        )

        # Verify data was unchanged
        assert updated_beat == sample_beat_data

    def test_hotkey_modifier_increments(self, hotkey_service, sample_beat_data):
        """Test different movement increments with modifiers"""
        # Mock selected beat
        hotkey_service.graph_service.get_selected_beat.return_value = sample_beat_data

        # Set up signal spy
        arrow_moved_spy = Mock()
        hotkey_service.arrow_moved.connect(arrow_moved_spy)

        # Test Shift modifier (20px increment)
        shift_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_W, Qt.KeyboardModifier.ShiftModifier
        )
        hotkey_service.handle_key_event(shift_event)
        arrow_moved_spy.assert_called_with("blue", 0, -20)

        # Reset spy
        arrow_moved_spy.reset_mock()

        # Test Ctrl+Shift modifier (200px increment)
        ctrl_shift_event = QKeyEvent(
            QKeyEvent.Type.KeyPress,
            Qt.Key.Key_W,
            Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier,
        )
        hotkey_service.handle_key_event(ctrl_shift_event)
        arrow_moved_spy.assert_called_with("blue", 0, -200)
