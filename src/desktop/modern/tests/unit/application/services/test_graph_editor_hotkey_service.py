"""
TEST LIFECYCLE: UNIT
PURPOSE: Test GraphEditorHotkeyService keyboard handling functionality
AUTHOR: @ai-agent
"""

import pytest
from unittest.mock import Mock, MagicMock
from PyQt6.QtCore import Qt, QObject
from PyQt6.QtGui import QKeyEvent

from application.services.graph_editor_hotkey_service import GraphEditorHotkeyService
from domain.models.core_models import BeatData, MotionData, MotionType


@pytest.mark.unit
class TestGraphEditorHotkeyService:
    """Test the graph editor hotkey service"""

    @pytest.fixture
    def mock_graph_service(self):
        """Create a mock graph service for testing"""
        service = Mock()
        service.get_selected_beat.return_value = BeatData(beat_number=1)
        return service

    @pytest.fixture
    def hotkey_service(self, mock_graph_service):
        """Create a hotkey service for testing"""
        return GraphEditorHotkeyService(mock_graph_service)

    @pytest.fixture
    def key_event_w(self):
        """Create a W key press event"""
        return QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_W, Qt.KeyboardModifier.NoModifier
        )

    @pytest.fixture
    def key_event_w_shift(self):
        """Create a W key press event with Shift modifier"""
        return QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_W, Qt.KeyboardModifier.ShiftModifier
        )

    @pytest.fixture
    def key_event_w_ctrl_shift(self):
        """Create a W key press event with Ctrl+Shift modifiers"""
        return QKeyEvent(
            QKeyEvent.Type.KeyPress,
            Qt.Key.Key_W,
            Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier,
        )

    def test_service_initialization(self, hotkey_service, mock_graph_service):
        """Test that the service initializes correctly"""
        assert isinstance(hotkey_service, QObject)
        assert hotkey_service.graph_service == mock_graph_service
        assert hotkey_service.base_increment == 5
        assert hotkey_service.shift_increment == 20
        assert hotkey_service.ctrl_shift_increment == 200

    def test_handle_key_event_no_selected_arrow(self, hotkey_service, key_event_w):
        """Test handling key events when no arrow is selected"""
        # Mock no selected beat
        hotkey_service.graph_service.get_selected_beat.return_value = None

        handled = hotkey_service.handle_key_event(key_event_w)
        assert handled is False

    def test_handle_wasd_movement_w_key(self, hotkey_service, key_event_w):
        """Test handling W key for upward movement"""
        # Set up signal spy
        signal_spy = Mock()
        hotkey_service.arrow_moved.connect(signal_spy)

        handled = hotkey_service.handle_key_event(key_event_w)

        assert handled is True
        signal_spy.assert_called_once_with("blue", 0, -5)  # Up movement

    def test_handle_wasd_movement_a_key(self, hotkey_service):
        """Test handling A key for leftward movement"""
        key_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_A, Qt.KeyboardModifier.NoModifier
        )

        # Set up signal spy
        signal_spy = Mock()
        hotkey_service.arrow_moved.connect(signal_spy)

        handled = hotkey_service.handle_key_event(key_event)

        assert handled is True
        signal_spy.assert_called_once_with("blue", -5, 0)  # Left movement

    def test_handle_wasd_movement_s_key(self, hotkey_service):
        """Test handling S key for downward movement"""
        key_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_S, Qt.KeyboardModifier.NoModifier
        )

        # Set up signal spy
        signal_spy = Mock()
        hotkey_service.arrow_moved.connect(signal_spy)

        handled = hotkey_service.handle_key_event(key_event)

        assert handled is True
        signal_spy.assert_called_once_with("blue", 0, 5)  # Down movement

    def test_handle_wasd_movement_d_key(self, hotkey_service):
        """Test handling D key for rightward movement"""
        key_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_D, Qt.KeyboardModifier.NoModifier
        )

        # Set up signal spy
        signal_spy = Mock()
        hotkey_service.arrow_moved.connect(signal_spy)

        handled = hotkey_service.handle_key_event(key_event)

        assert handled is True
        signal_spy.assert_called_once_with("blue", 5, 0)  # Right movement

    def test_handle_wasd_movement_with_shift_modifier(
        self, hotkey_service, key_event_w_shift
    ):
        """Test handling WASD movement with Shift modifier"""
        # Set up signal spy
        signal_spy = Mock()
        hotkey_service.arrow_moved.connect(signal_spy)

        handled = hotkey_service.handle_key_event(key_event_w_shift)

        assert handled is True
        signal_spy.assert_called_once_with("blue", 0, -20)  # Shift increment

    def test_handle_wasd_movement_with_ctrl_shift_modifier(
        self, hotkey_service, key_event_w_ctrl_shift
    ):
        """Test handling WASD movement with Ctrl+Shift modifiers"""
        # Set up signal spy
        signal_spy = Mock()
        hotkey_service.arrow_moved.connect(signal_spy)

        handled = hotkey_service.handle_key_event(key_event_w_ctrl_shift)

        assert handled is True
        signal_spy.assert_called_once_with("blue", 0, -200)  # Ctrl+Shift increment

    def test_handle_x_key_rotation_override(self, hotkey_service):
        """Test handling X key for rotation override"""
        key_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_X, Qt.KeyboardModifier.NoModifier
        )

        # Set up signal spy
        signal_spy = Mock()
        hotkey_service.rotation_override_requested.connect(signal_spy)

        handled = hotkey_service.handle_key_event(key_event)

        assert handled is True
        signal_spy.assert_called_once_with("blue")

    def test_handle_z_key_special_placement_removal(self, hotkey_service):
        """Test handling Z key for special placement removal"""
        key_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_Z, Qt.KeyboardModifier.NoModifier
        )

        # Set up signal spy
        signal_spy = Mock()
        hotkey_service.special_placement_removal_requested.connect(signal_spy)

        handled = hotkey_service.handle_key_event(key_event)

        assert handled is True
        signal_spy.assert_called_once_with("blue")

    def test_handle_c_key_prop_placement_override(self, hotkey_service):
        """Test handling C key for prop placement override"""
        key_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_C, Qt.KeyboardModifier.NoModifier
        )

        # Set up signal spy
        signal_spy = Mock()
        hotkey_service.prop_placement_override_requested.connect(signal_spy)

        handled = hotkey_service.handle_key_event(key_event)

        assert handled is True
        signal_spy.assert_called_once_with("blue")

    def test_handle_unhandled_key(self, hotkey_service):
        """Test handling unrecognized keys"""
        key_event = QKeyEvent(
            QKeyEvent.Type.KeyPress,
            Qt.Key.Key_Q,  # Unhandled key
            Qt.KeyboardModifier.NoModifier,
        )

        handled = hotkey_service.handle_key_event(key_event)
        assert handled is False

    def test_get_movement_delta(self, hotkey_service):
        """Test movement delta calculation"""
        # Test all directions
        assert hotkey_service._get_movement_delta(Qt.Key.Key_W, 10) == (0, -10)
        assert hotkey_service._get_movement_delta(Qt.Key.Key_A, 10) == (-10, 0)
        assert hotkey_service._get_movement_delta(Qt.Key.Key_S, 10) == (0, 10)
        assert hotkey_service._get_movement_delta(Qt.Key.Key_D, 10) == (10, 0)
        assert hotkey_service._get_movement_delta(Qt.Key.Key_Q, 10) == (0, 0)

    def test_set_movement_increments(self, hotkey_service):
        """Test setting custom movement increments"""
        hotkey_service.set_movement_increments(10, 50, 500)

        assert hotkey_service.base_increment == 10
        assert hotkey_service.shift_increment == 50
        assert hotkey_service.ctrl_shift_increment == 500

    def test_get_movement_increments(self, hotkey_service):
        """Test getting movement increments"""
        increments = hotkey_service.get_movement_increments()
        assert increments == (5, 20, 200)
