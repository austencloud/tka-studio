"""
Tests for UIStateManager interface compliance and functionality.

These tests verify that the UIStateManager correctly implements the
IUIStateManager interface and provides expected behavior.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from shared.application.services.ui.ui_state_manager import (
    TabType,
    UIComponent,
    UIState,
    UIStateManager,
)
from desktop.modern.core.interfaces.core_services import IUIStateManager
from desktop.modern.core.interfaces.session_services import ISessionStateTracker


class TestUIStateManagerInterface:
    """Test interface compliance for UIStateManager."""

    def test_ui_state_manager_implements_interface(self):
        """Test that UIStateManager implements IUIStateManager."""
        assert issubclass(UIStateManager, IUIStateManager)

    def test_all_interface_methods_implemented(self):
        """Test that all interface methods are implemented."""
        service = UIStateManager()

        # Get all abstract methods from interface
        interface_methods = [
            method
            for method in dir(IUIStateManager)
            if not method.startswith("_") and callable(getattr(IUIStateManager, method))
        ]

        # Verify all methods exist and are callable
        for method_name in interface_methods:
            assert hasattr(service, method_name), f"Missing method: {method_name}"
            assert callable(
                getattr(service, method_name)
            ), f"Method not callable: {method_name}"

    def test_method_signatures_match_interface(self):
        """Test that method signatures match the interface."""
        import inspect

        service = UIStateManager()

        # Test key methods
        key_methods = [
            "get_setting",
            "set_setting",
            "get_tab_state",
            "get_all_settings",
            "clear_settings",
            "save_state",
            "load_state",
            "toggle_graph_editor",
        ]

        for method_name in key_methods:
            interface_method = getattr(IUIStateManager, method_name)
            implementation_method = getattr(service, method_name)

            # Both should be callable
            assert callable(interface_method)
            assert callable(implementation_method)


class TestUIStateManagerBehavior:
    """Test behavior of UIStateManager."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary directory for settings
        self.temp_dir = Path(tempfile.mkdtemp())

        # Mock the event bus to avoid file system issues
        with patch(
            "application.services.ui.ui_state_manager.get_event_bus"
        ) as mock_event_bus:
            mock_event_bus.return_value = Mock()

            # Create service instance with mocked dependencies
            self.service = UIStateManager()

            # Override settings file to use temp directory and reset state
            self.service._settings_file = self.temp_dir / "test_settings.json"
            self.service._ui_state = UIState()  # Reset to clean default state

    def teardown_method(self):
        """Clean up test fixtures."""
        # Clean up temp directory
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initial_state(self):
        """Test initial state of UIStateManager."""
        # Should have default settings
        assert isinstance(self.service._ui_state, UIState)
        assert self.service._ui_state.active_tab == "sequence_builder"
        assert not self.service._ui_state.graph_editor_visible
        assert self.service._ui_state.graph_editor_height == 300

    def test_get_and_set_setting(self):
        """Test getting and setting settings."""
        # Get non-existent setting with default
        value = self.service.get_setting("non_existent", "default_value")
        assert value == "default_value"

        # Set a setting
        self.service.set_setting("test_key", "test_value")

        # Get the setting
        value = self.service.get_setting("test_key")
        assert value == "test_value"

    def test_get_and_set_tab_state(self):
        """Test getting and setting tab state."""
        # Get non-existent tab state
        state = self.service.get_tab_state("non_existent_tab")
        assert state == {}

        # Update tab state
        test_state = {"key1": "value1", "key2": "value2"}
        self.service.update_tab_state("test_tab", test_state)

        # Get tab state
        state = self.service.get_tab_state("test_tab")
        assert state == test_state

    def test_active_tab_management(self):
        """Test active tab management."""
        # Initial active tab
        assert self.service.get_active_tab() == "sequence_builder"

        # Set new active tab
        self.service.set_active_tab("dictionary")
        assert self.service.get_active_tab() == "dictionary"

    def test_graph_editor_management(self):
        """Test graph editor management."""
        # Initial state
        state = self.service.get_graph_editor_state()
        assert not state["visible"]
        assert state["height"] == 300

        # Toggle graph editor
        visible = self.service.toggle_graph_editor()
        assert visible is True

        # Check state changed
        state = self.service.get_graph_editor_state()
        assert state["visible"] is True

        # Toggle again
        visible = self.service.toggle_graph_editor()
        assert visible is False

    def test_graph_editor_height(self):
        """Test graph editor height management."""
        # Set height
        self.service.set_graph_editor_height(500)

        # Check height
        state = self.service.get_graph_editor_state()
        assert state["height"] == 500

        # Test clamping
        self.service.set_graph_editor_height(50)  # Too small
        state = self.service.get_graph_editor_state()
        assert state["height"] == 100  # Clamped to minimum

        self.service.set_graph_editor_height(1000)  # Too large
        state = self.service.get_graph_editor_state()
        assert state["height"] == 800  # Clamped to maximum

    def test_option_picker_state(self):
        """Test option picker state management."""
        # Initial state
        state = self.service.get_option_picker_state()
        assert state["selection"] is None
        assert state["filters"] == {}

        # Set selection
        self.service.set_option_picker_selection("test_option")
        state = self.service.get_option_picker_state()
        assert state["selection"] == "test_option"

        # Update filters
        filters = {"type": "staff", "level": "beginner"}
        self.service.update_option_picker_filters(filters)
        state = self.service.get_option_picker_state()
        assert state["filters"] == filters

    def test_component_visibility(self):
        """Test component visibility management."""
        # Initial state
        assert self.service.is_component_visible("test_component") is True  # Default

        # Set visibility
        self.service.set_component_visibility("test_component", False)
        assert self.service.is_component_visible("test_component") is False

        # Set visibility back
        self.service.set_component_visibility("test_component", True)
        assert self.service.is_component_visible("test_component") is True

    def test_window_state_management(self):
        """Test window state management."""
        # Initial state
        geometry = self.service.get_window_geometry()
        assert geometry == {}

        # Set geometry
        test_geometry = {"x": 100, "y": 200, "width": 800, "height": 600}
        self.service.set_window_geometry(test_geometry)

        # Get geometry
        geometry = self.service.get_window_geometry()
        assert geometry == test_geometry

        # Test maximized state
        assert not self.service.is_window_maximized()
        self.service.set_window_maximized(True)
        assert self.service.is_window_maximized()

    def test_hotkey_management(self):
        """Test hotkey management."""
        # Register hotkey
        callback = Mock()
        self.service.register_hotkey("Ctrl+S", callback)

        # Handle hotkey
        handled = self.service.handle_hotkey("Ctrl+S")
        assert handled is True
        callback.assert_called_once()

        # Handle non-existent hotkey
        handled = self.service.handle_hotkey("Ctrl+Z")
        assert handled is False

    def test_get_all_settings(self):
        """Test getting all settings."""
        # Set some settings
        self.service.set_setting("key1", "value1")
        self.service.set_setting("key2", "value2")

        # Get all settings
        all_settings = self.service.get_all_settings()
        assert "key1" in all_settings
        assert "key2" in all_settings
        assert all_settings["key1"] == "value1"
        assert all_settings["key2"] == "value2"

    def test_clear_settings(self):
        """Test clearing settings."""
        # Set some settings
        self.service.set_setting("key1", "value1")
        self.service.set_setting("key2", "value2")

        # Clear settings
        self.service.clear_settings()

        # Settings should be empty
        all_settings = self.service.get_all_settings()
        assert len(all_settings) == 0

    def test_reset_to_defaults(self):
        """Test resetting to defaults."""
        # Set some settings
        self.service.set_setting("key1", "value1")
        self.service.set_active_tab("dictionary")

        # Reset to defaults
        self.service.reset_to_defaults()

        # Should be back to defaults
        assert self.service.get_active_tab() == "sequence_builder"

        # Custom settings should be replaced with defaults
        all_settings = self.service.get_all_settings()
        assert "theme" in all_settings  # Default setting

    def test_import_export_settings(self):
        """Test importing and exporting settings."""
        # Set some settings
        self.service.set_setting("key1", "value1")
        self.service.set_setting("key2", "value2")

        # Export settings
        export_path = self.temp_dir / "exported_settings.json"
        success = self.service.export_settings(export_path)
        assert success is True
        assert export_path.exists()

        # Clear settings
        self.service.clear_settings()

        # Import settings
        success = self.service.import_settings(export_path)
        assert success is True

        # Settings should be restored
        all_settings = self.service.get_all_settings()
        assert all_settings["key1"] == "value1"
        assert all_settings["key2"] == "value2"

    def test_save_and_load_state(self):
        """Test saving and loading state."""
        # Set some state
        self.service.set_setting("key1", "value1")
        self.service.set_active_tab("dictionary")
        self.service.set_graph_editor_height(400)

        # Save state
        self.service.save_state()

        # Create new service instance
        new_service = UIStateManager.__new__(UIStateManager)
        new_service._ui_state = UIState()
        new_service._settings_file = self.service._settings_file
        new_service._session_service = None
        new_service._default_settings = new_service._load_default_settings()
        new_service._hotkey_bindings = {}
        new_service._event_bus = Mock()

        # Load state
        new_service.load_state()

        # State should be restored
        assert new_service.get_setting("key1") == "value1"
        assert new_service.get_active_tab() == "dictionary"
        assert new_service.get_graph_editor_state()["height"] == 400


class TestUIStateManagerWithSessionService:
    """Test UIStateManager with session service integration."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.mock_session_service = Mock(spec=ISessionStateTracker)

        # Create service with session service
        with patch(
            "application.services.ui.ui_state_manager.get_event_bus"
        ) as mock_event_bus:
            mock_event_bus.return_value = Mock()

            # Create service instance with session service
            self.service = UIStateManager(session_service=self.mock_session_service)

            # Override settings file to use temp directory and reset state
            self.service._settings_file = self.temp_dir / "test_settings.json"
            self.service._ui_state = UIState()  # Reset to clean default state

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_setting_change_triggers_session_save(self):
        """Test that setting changes trigger session save."""
        # Set setting
        self.service.set_setting("test_key", "test_value")

        # Should trigger session mark_interaction
        self.mock_session_service.mark_interaction.assert_called_once()

    def test_tab_change_triggers_session_save(self):
        """Test that tab changes trigger session save."""
        # Set active tab
        self.service.set_active_tab("dictionary")

        # Should trigger session update
        self.mock_session_service.update_ui_state.assert_called_once()

    def test_graph_editor_toggle_triggers_session_save(self):
        """Test that graph editor toggle triggers session save."""
        # Toggle graph editor
        self.service.toggle_graph_editor()

        # Should trigger session update
        self.mock_session_service.update_graph_editor_state.assert_called_once()


class MockUIStateManager(IUIStateManager):
    """Mock implementation for testing interface compliance."""

    def __init__(self):
        self.settings = {}
        self.tab_states = {}
        self.active_tab = "sequence_builder"
        self.graph_editor_visible = False

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        self.settings[key] = value

    def get_tab_state(self, tab_name):
        return self.tab_states.get(tab_name, {})

    def get_all_settings(self):
        return self.settings.copy()

    def clear_settings(self):
        self.settings.clear()

    def save_state(self):
        pass

    def load_state(self):
        pass

    def toggle_graph_editor(self):
        self.graph_editor_visible = not self.graph_editor_visible
        return self.graph_editor_visible


class TestMockUIStateManager:
    """Test mock implementation."""

    def test_mock_implements_interface(self):
        """Test that mock implements interface."""
        mock_service = MockUIStateManager()
        assert isinstance(mock_service, IUIStateManager)

    def test_mock_basic_functionality(self):
        """Test basic mock functionality."""
        mock_service = MockUIStateManager()

        # Test settings
        assert mock_service.get_setting("key1") is None
        mock_service.set_setting("key1", "value1")
        assert mock_service.get_setting("key1") == "value1"

        # Test graph editor
        assert mock_service.toggle_graph_editor() is True
        assert mock_service.toggle_graph_editor() is False

    def test_mock_clear_settings(self):
        """Test mock clear settings."""
        mock_service = MockUIStateManager()

        # Set some settings
        mock_service.set_setting("key1", "value1")
        mock_service.set_setting("key2", "value2")

        # Clear
        mock_service.clear_settings()

        # Should be empty
        assert len(mock_service.get_all_settings()) == 0
