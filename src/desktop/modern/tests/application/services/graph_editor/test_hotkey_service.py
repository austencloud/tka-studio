"""
Tests for GraphEditorHotkeyService

Simple, reliable tests that actually pass.
"""

from unittest.mock import MagicMock, Mock

import pytest
from desktop.modern.application.services.graph_editor.graph_editor_hotkey_manager import (
    GraphEditorHotkeyManager as GraphEditorHotkeyService,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication


@pytest.fixture
def mock_graph_service():
    """Mock graph service"""
    mock = Mock()
    mock.get_selected_beat.return_value = Mock()  # Has a selected beat
    return mock


@pytest.fixture
def hotkey_service(mock_graph_service):
    """Create hotkey service instance"""
    service = GraphEditorHotkeyService(mock_graph_service)

    # Set up mock callbacks
    service.on_arrow_moved = Mock()
    service.on_rotation_override = Mock()
    service.on_special_placement_removal = Mock()
    service.on_prop_placement_override = Mock()

    return service


@pytest.fixture
def qapp():
    """Ensure QApplication exists"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


class TestGraphEditorHotkeyService:
    """Test the hotkey service functionality"""

    def test_initialization(self, hotkey_service, mock_graph_service):
        """Test service initializes correctly"""
        assert hotkey_service.graph_service == mock_graph_service
        assert hotkey_service.base_increment == 5
        assert hotkey_service.shift_increment == 20
        assert hotkey_service.ctrl_shift_increment == 200
        assert hotkey_service.on_arrow_moved is not None
        assert hotkey_service.on_rotation_override is not None

    def test_movement_increments_configuration(self, hotkey_service):
        """Test movement increment configuration"""
        # Test default values
        base, shift, ctrl_shift = hotkey_service.get_movement_increments()
        assert base == 5
        assert shift == 20
        assert ctrl_shift == 200

        # Test setting custom values
        hotkey_service.set_movement_increments(10, 50, 500)
        base, shift, ctrl_shift = hotkey_service.get_movement_increments()
        assert base == 10
        assert shift == 50
        assert ctrl_shift == 500

    def test_handle_key_event_no_selected_arrow(
        self, hotkey_service, mock_graph_service
    ):
        """Test key handling when no arrow is selected"""
        # Mock no selected arrow
        mock_graph_service.get_selected_beat.return_value = None

        # Create a mock key event
        key_event = Mock()
        key_event.key.return_value = Qt.Key.Key_W
        key_event.modifiers.return_value = Qt.KeyboardModifier.NoModifier

        # Should return False (not handled)
        result = hotkey_service.handle_key_event(key_event)
        assert result is False

    def test_wasd_movement_basic(self, hotkey_service, qapp):
        """Test basic WASD movement"""
        # Create real key events for each direction
        test_cases = [
            (Qt.Key.Key_W, (0, -5)),  # Up
            (Qt.Key.Key_A, (-5, 0)),  # Left
            (Qt.Key.Key_S, (0, 5)),  # Down
            (Qt.Key.Key_D, (5, 0)),  # Right
        ]

        for key, expected_delta in test_cases:
            # Create key event
            key_event = Mock()
            key_event.key.return_value = key
            key_event.modifiers.return_value = Qt.KeyboardModifier.NoModifier

            # Handle the event
            result = hotkey_service.handle_key_event(key_event)

            # Verify
            assert result is True
            hotkey_service.on_arrow_moved.assert_called_with(
                "blue", expected_delta[0], expected_delta[1]
            )
            hotkey_service.on_arrow_moved.reset_mock()

    def test_wasd_movement_with_shift(self, hotkey_service, qapp):
        """Test WASD movement with Shift modifier"""
        key_event = Mock()
        key_event.key.return_value = Qt.Key.Key_W
        key_event.modifiers.return_value = Qt.KeyboardModifier.ShiftModifier

        result = hotkey_service.handle_key_event(key_event)

        assert result is True
        hotkey_service.on_arrow_moved.assert_called_with(
            "blue", 0, -20
        )  # Shift increment

    def test_wasd_movement_with_ctrl_shift(self, hotkey_service, qapp):
        """Test WASD movement with Ctrl+Shift modifier"""
        key_event = Mock()
        key_event.key.return_value = Qt.Key.Key_W
        key_event.modifiers.return_value = (
            Qt.KeyboardModifier.ShiftModifier | Qt.KeyboardModifier.ControlModifier
        )

        result = hotkey_service.handle_key_event(key_event)

        assert result is True
        hotkey_service.on_arrow_moved.assert_called_with(
            "blue", 0, -200
        )  # Ctrl+Shift increment

    def test_special_commands(self, hotkey_service, qapp):
        """Test X, Z, C special commands"""
        test_cases = [
            (Qt.Key.Key_X, "on_rotation_override"),
            (Qt.Key.Key_Z, "on_special_placement_removal"),
            (Qt.Key.Key_C, "on_prop_placement_override"),
        ]

        for key, expected_callback in test_cases:
            key_event = Mock()
            key_event.key.return_value = key
            key_event.modifiers.return_value = Qt.KeyboardModifier.NoModifier

            result = hotkey_service.handle_key_event(key_event)

            assert result is True
            callback_method = getattr(hotkey_service, expected_callback)
            callback_method.assert_called_with("blue")
            callback_method.reset_mock()

    def test_unhandled_keys(self, hotkey_service, qapp):
        """Test that unhandled keys return False"""
        key_event = Mock()
        key_event.key.return_value = Qt.Key.Key_Space  # Not handled
        key_event.modifiers.return_value = Qt.KeyboardModifier.NoModifier

        result = hotkey_service.handle_key_event(key_event)

        assert result is False
        # No callbacks should be called
        hotkey_service.on_arrow_moved.assert_not_called()
        hotkey_service.on_rotation_override.assert_not_called()

    def test_get_movement_delta(self, hotkey_service):
        """Test movement delta calculation"""
        # Test direct method call
        delta_x, delta_y = hotkey_service._get_movement_delta(Qt.Key.Key_W, 10)
        assert (delta_x, delta_y) == (0, -10)

        delta_x, delta_y = hotkey_service._get_movement_delta(Qt.Key.Key_A, 10)
        assert (delta_x, delta_y) == (-10, 0)

        delta_x, delta_y = hotkey_service._get_movement_delta(Qt.Key.Key_S, 10)
        assert (delta_x, delta_y) == (0, 10)

        delta_x, delta_y = hotkey_service._get_movement_delta(Qt.Key.Key_D, 10)
        assert (delta_x, delta_y) == (10, 0)

        # Test unknown key
        delta_x, delta_y = hotkey_service._get_movement_delta(Qt.Key.Key_Space, 10)
        assert (delta_x, delta_y) == (0, 0)


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
