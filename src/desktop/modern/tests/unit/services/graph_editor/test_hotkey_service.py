"""
Tests for GraphEditorHotkeyService

Simple, reliable tests that work with or without Qt installed.
"""

from unittest.mock import Mock

import pytest


def test_hotkey_service_creation():
    """Test that hotkey service can be created"""
    from application.services.graph_editor.graph_editor_hotkey_service import (
        GraphEditorHotkeyService,
    )

    # Mock graph service
    mock_graph_service = Mock()

    # Create service
    service = GraphEditorHotkeyService(mock_graph_service)

    # Verify initialization
    assert service.graph_service == mock_graph_service
    assert service.base_increment == 5
    assert service.shift_increment == 20
    assert service.ctrl_shift_increment == 200


def test_movement_increments():
    """Test movement increment configuration"""
    from application.services.graph_editor.graph_editor_hotkey_service import (
        GraphEditorHotkeyService,
    )

    mock_graph_service = Mock()
    service = GraphEditorHotkeyService(mock_graph_service)

    # Test default increments
    increments = service.get_movement_increments()
    assert increments == (5, 20, 200)

    # Test setting custom increments
    service.set_movement_increments(10, 30, 100)
    increments = service.get_movement_increments()
    assert increments == (10, 30, 100)


def test_movement_delta_calculation():
    """Test movement delta calculation"""
    from application.services.graph_editor.graph_editor_hotkey_service import (
        GraphEditorHotkeyService,
        Qt,
    )

    mock_graph_service = Mock()
    service = GraphEditorHotkeyService(mock_graph_service)

    # Test WASD movement deltas
    assert service._get_movement_delta(Qt.Key.Key_W, 10) == (0, -10)  # Up
    assert service._get_movement_delta(Qt.Key.Key_A, 10) == (-10, 0)  # Left
    assert service._get_movement_delta(Qt.Key.Key_S, 10) == (0, 10)  # Down
    assert service._get_movement_delta(Qt.Key.Key_D, 10) == (10, 0)  # Right

    # Test invalid key
    assert service._get_movement_delta("invalid", 10) == (0, 0)


def test_callback_handling():
    """Test callback function handling"""
    from application.services.graph_editor.graph_editor_hotkey_service import (
        GraphEditorHotkeyService,
        QKeyEvent,
        Qt,
    )

    mock_graph_service = Mock()
    mock_graph_service.get_selected_beat.return_value = {"id": "test_beat"}

    service = GraphEditorHotkeyService(mock_graph_service)

    # Set up callback mocks
    service.on_arrow_moved = Mock()
    service.on_rotation_override = Mock()
    service.on_special_placement_removal = Mock()
    service.on_prop_placement_override = Mock()

    # Test WASD movement (mocked selected arrow)
    with pytest.MonkeyPatch().context() as m:
        m.setattr(service, "_get_selected_arrow", lambda: "blue")

        key_event = QKeyEvent(Qt.Key.Key_W, Qt.KeyboardModifier.NoModifier)
        result = service.handle_key_event(key_event)

        assert result is True
        service.on_arrow_moved.assert_called_once_with("blue", 0, -5)

    # Test X key (rotation override)
    with pytest.MonkeyPatch().context() as m:
        m.setattr(service, "_get_selected_arrow", lambda: "red")

        key_event = QKeyEvent(Qt.Key.Key_X, Qt.KeyboardModifier.NoModifier)
        result = service.handle_key_event(key_event)

        assert result is True
        service.on_rotation_override.assert_called_once_with("red")


def test_no_selected_arrow():
    """Test behavior when no arrow is selected"""
    from application.services.graph_editor.graph_editor_hotkey_service import (
        GraphEditorHotkeyService,
        QKeyEvent,
        Qt,
    )

    mock_graph_service = Mock()
    service = GraphEditorHotkeyService(mock_graph_service)

    # Mock no selected arrow
    with pytest.MonkeyPatch().context() as m:
        m.setattr(service, "_get_selected_arrow", lambda: None)

        key_event = QKeyEvent(Qt.Key.Key_W, Qt.KeyboardModifier.NoModifier)
        result = service.handle_key_event(key_event)

        assert result is False


def test_modifier_key_handling():
    """Test modifier key handling for movement increments"""
    from application.services.graph_editor.graph_editor_hotkey_service import (
        GraphEditorHotkeyService,
        QKeyEvent,
        Qt,
    )

    mock_graph_service = Mock()
    service = GraphEditorHotkeyService(mock_graph_service)
    service.on_arrow_moved = Mock()

    with pytest.MonkeyPatch().context() as m:
        m.setattr(service, "_get_selected_arrow", lambda: "blue")

        # Test base movement (no modifiers)
        key_event = QKeyEvent(Qt.Key.Key_W, Qt.KeyboardModifier.NoModifier)
        service.handle_key_event(key_event)
        service.on_arrow_moved.assert_called_with("blue", 0, -5)  # base increment

        service.on_arrow_moved.reset_mock()

        # Test shift movement
        key_event = QKeyEvent(Qt.Key.Key_W, Qt.KeyboardModifier.ShiftModifier)
        service.handle_key_event(key_event)
        service.on_arrow_moved.assert_called_with("blue", 0, -20)  # shift increment

        service.on_arrow_moved.reset_mock()

        # Test ctrl+shift movement
        key_event = QKeyEvent(
            Qt.Key.Key_W,
            Qt.KeyboardModifier.ShiftModifier | Qt.KeyboardModifier.ControlModifier,
        )
        service.handle_key_event(key_event)
        service.on_arrow_moved.assert_called_with(
            "blue", 0, -200
        )  # ctrl+shift increment


if __name__ == "__main__":
    pytest.main([__file__])
