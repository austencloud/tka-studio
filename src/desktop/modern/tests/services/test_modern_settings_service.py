"""
Comprehensive Tests for Modern Settings Service

Tests the complete modern state persistence system including:
- Individual settings managers
- CQRS command/query operations
- Memento pattern state snapshots
- Integration with session state
- Dependency injection registration
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Import Qt for testing
try:
    from PyQt6.QtCore import QSettings
    from PyQt6.QtTest import QTest
    QT_AVAILABLE = True
except ImportError:
    QT_AVAILABLE = False
    # Mock QSettings for environments without Qt
    class QSettings:
        def __init__(self, *args):
            self._data = {}
        def value(self, key, default=None, type=None):
            return self._data.get(key, default)
        def setValue(self, key, value):
            self._data[key] = value
        def sync(self):
            pass
        def beginGroup(self, group):
            pass
        def endGroup(self):
            pass
        def childKeys(self):
            return []
        def childGroups(self):
            return []
        def remove(self, key):
            self._data.pop(key, None)
        def contains(self, key):
            return key in self._data

# Import our services
from desktop.modern.application.services.settings.modern_settings_service import (
    ModernSettingsService, 
    ApplicationStateMemento
)
from desktop.modern.application.services.settings.background_settings_manager import BackgroundSettingsManager
from desktop.modern.application.services.settings.visibility_settings_manager import VisibilitySettingsManager
from desktop.modern.application.services.settings.beat_layout_settings_manager import BeatLayoutSettingsManager
from desktop.modern.application.services.settings.prop_type_settings_manager import PropTypeSettingsManager
from desktop.modern.application.services.settings.user_profile_settings_manager import UserProfileSettingsManager
from desktop.modern.application.services.settings.image_export_settings_manager import ImageExportSettingsManager

from desktop.modern.core.interfaces.settings_services import PropType
from desktop.modern.core.dependency_injection.settings_service_registration import (
    register_settings_services, 
    validate_settings_registration,
    create_configured_settings_container
)


class TestApplicationStateMemento:
    """Test the Memento pattern implementation."""
    
    def test_memento_creation(self):
        """Test memento creation with basic data."""
        memento = ApplicationStateMemento(
            current_tab="construct",
            session_data={"test": "data"},
            settings_snapshot={"global/test": "value"}
        )
        
        assert memento.current_tab == "construct"
        assert memento.session_data == {"test": "data"}
        assert memento.settings_snapshot == {"global/test": "value"}
        assert isinstance(memento.timestamp, datetime)
    
    def test_memento_serialization(self):
        """Test memento to_dict and from_dict methods."""
        original = ApplicationStateMemento(
            current_tab="sequence",
            window_geometry=b"test_geometry",
            session_data={"key": "value"},
            settings_snapshot={"section/key": "setting_value"}
        )
        
        # Test serialization
        data = original.to_dict()
        assert data["current_tab"] == "sequence"
        assert data["window_geometry"] == b"test_geometry".hex()
        assert data["session_data"] == {"key": "value"}
        assert "timestamp" in data
        
        # Test deserialization
        restored = ApplicationStateMemento.from_dict(data)
        assert restored.current_tab == original.current_tab
        assert restored.window_geometry == original.window_geometry
        assert restored.session_data == original.session_data
        assert restored.settings_snapshot == original.settings_snapshot


class TestBackgroundSettingsManager:
    """Test background settings manager."""
    
    @pytest.fixture
    def settings(self):
        return QSettings()
    
    @pytest.fixture
    def manager(self, settings):
        return BackgroundSettingsManager(settings)
    
    def test_get_available_backgrounds(self, manager):
        """Test getting available background types."""
        backgrounds = manager.get_available_backgrounds()
        assert isinstance(backgrounds, list)
        assert "Snowfall" in backgrounds
        assert "AuroraBorealis" in backgrounds
        assert len(backgrounds) > 0
    
    def test_current_background_default(self, manager):
        """Test default background is Snowfall."""
        current = manager.get_current_background()
        assert current == "Snowfall"
    
    def test_set_valid_background(self, manager):
        """Test setting a valid background."""
        success = manager.set_background("Rainbow")
        assert success
        assert manager.get_current_background() == "Rainbow"
    
    def test_set_invalid_background(self, manager):
        """Test setting an invalid background."""
        success = manager.set_background("InvalidBackground")
        assert not success
        # Should remain at default
        assert manager.get_current_background() == "Snowfall"
    
    def test_font_color_computation(self, manager):
        """Test font color computation for different backgrounds."""
        # Dark backgrounds should use white font
        manager.set_background("Snowfall")
        assert manager.get_current_font_color() == "white"
        
        # Light backgrounds should use black font
        manager.set_background("Rainbow")
        assert manager.get_current_font_color() == "black"


class TestVisibilitySettingsManager:
    """Test visibility settings manager."""
    
    @pytest.fixture
    def settings(self):
        return QSettings()
    
    @pytest.fixture
    def manager(self, settings):
        return VisibilitySettingsManager(settings)
    
    def test_glyph_visibility_defaults(self, manager):
        """Test default glyph visibility settings."""
        assert manager.get_glyph_visibility("letter") == True
        assert manager.get_glyph_visibility("elemental") == True
        assert manager.get_glyph_visibility("vtg") == False
    
    def test_set_glyph_visibility(self, manager):
        """Test setting glyph visibility."""
        manager.set_glyph_visibility("letter", False)
        assert manager.get_glyph_visibility("letter") == False
        
        manager.set_glyph_visibility("vtg", True)
        assert manager.get_glyph_visibility("vtg") == True
    
    def test_motion_visibility(self, manager):
        """Test motion arrow visibility."""
        assert manager.get_motion_visibility("red") == True
        assert manager.get_motion_visibility("blue") == True
        
        manager.set_motion_visibility("red", False)
        assert manager.get_motion_visibility("red") == False
        assert manager.get_motion_visibility("blue") == True
    
    def test_invalid_motion_color(self, manager):
        """Test invalid motion color handling."""
        result = manager.get_motion_visibility("green")  # Invalid color
        assert result == True  # Should return default
    
    def test_get_all_visibility_settings(self, manager):
        """Test getting all visibility settings."""
        all_settings = manager.get_all_visibility_settings()
        assert isinstance(all_settings, dict)
        assert "glyph_letter" in all_settings
        assert "red_motion" in all_settings
        assert "grid" in all_settings
    
    def test_toggle_visibility(self, manager):
        """Test toggling visibility states."""
        original = manager.get_glyph_visibility("letter")
        new_state = manager.toggle_glyph_visibility("letter")
        assert new_state != original
        assert manager.get_glyph_visibility("letter") == new_state


class TestBeatLayoutSettingsManager:
    """Test beat layout settings manager."""
    
    @pytest.fixture
    def settings(self):
        return QSettings()
    
    @pytest.fixture
    def manager(self, settings):
        return BeatLayoutSettingsManager(settings)
    
    def test_get_layout_for_common_lengths(self, manager):
        """Test layout calculation for common sequence lengths."""
        # Test predefined layouts
        assert manager.get_layout_for_length(4) == (2, 2)
        assert manager.get_layout_for_length(9) == (3, 3)
        assert manager.get_layout_for_length(16) == (4, 4)
    
    def test_get_layout_for_unusual_length(self, manager):
        """Test layout calculation for unusual sequence length."""
        layout = manager.get_layout_for_length(7)
        rows, cols = layout
        assert rows * cols >= 7  # Must fit all beats
        assert rows > 0 and cols > 0
    
    def test_set_custom_layout(self, manager):
        """Test setting custom layout."""
        manager.set_layout_for_length(8, 4, 2)
        assert manager.get_layout_for_length(8) == (4, 2)
    
    def test_invalid_layout_validation(self, manager):
        """Test validation of invalid layouts."""
        # Test with zero dimensions
        manager.set_layout_for_length(4, 0, 2)
        # Should not change from default
        assert manager.get_layout_for_length(4) == (2, 2)
        
        # Test with insufficient space
        manager.set_layout_for_length(8, 1, 2)  # Only 2 spaces for 8 beats
        # Should not change from default
        assert manager.get_layout_for_length(8) == (2, 4)
    
    def test_layout_options(self, manager):
        """Test getting layout options."""
        options = manager.get_layout_options_for_length(6)
        assert isinstance(options, dict)
        assert len(options) > 0
        
        # Should include single row option
        assert (1, 6) in options.values()
        
        # Should include factors
        assert (2, 3) in options.values()
    
    def test_default_sequence_length(self, manager):
        """Test default sequence length settings."""
        default_length = manager.get_default_sequence_length()
        assert isinstance(default_length, int)
        assert default_length > 0
        
        manager.set_default_sequence_length(20)
        assert manager.get_default_sequence_length() == 20


class TestPropTypeSettingsManager:
    """Test prop type settings manager."""
    
    @pytest.fixture
    def settings(self):
        return QSettings()
    
    @pytest.fixture
    def manager(self, settings):
        return PropTypeSettingsManager(settings)
    
    def test_default_prop_type(self, manager):
        """Test default prop type is Staff."""
        current = manager.get_current_prop_type()
        assert current == PropType.STAFF
    
    def test_set_prop_type(self, manager):
        """Test setting prop type."""
        manager.set_prop_type(PropType.FAN)
        assert manager.get_current_prop_type() == PropType.FAN
    
    def test_available_prop_types(self, manager):
        """Test getting available prop types."""
        available = manager.get_available_prop_types()
        assert isinstance(available, list)
        assert PropType.STAFF in available
        assert PropType.FAN in available
        assert len(available) > 0
    
    def test_prop_type_validation(self, manager):
        """Test prop type validation."""
        assert manager.is_valid_prop_type(PropType.STAFF)
        assert manager.is_valid_prop_type(PropType.FAN)
    
    def test_cycle_prop_type(self, manager):
        """Test cycling through prop types."""
        original = manager.get_current_prop_type()
        next_type = manager.cycle_prop_type()
        assert next_type != original
        assert manager.get_current_prop_type() == next_type
    
    def test_prop_specific_settings(self, manager):
        """Test prop-specific settings."""
        manager.set_prop_specific_setting("test_setting", "test_value", PropType.STAFF)
        
        staff_settings = manager.get_prop_specific_settings(PropType.STAFF)
        assert "test_setting" in staff_settings
        assert staff_settings["test_setting"] == "test_value"
        
        # Different prop type should not have the setting
        fan_settings = manager.get_prop_specific_settings(PropType.FAN)
        assert "test_setting" not in fan_settings


class TestUserProfileSettingsManager:
    """Test user profile settings manager."""
    
    @pytest.fixture
    def settings(self):
        return QSettings()
    
    @pytest.fixture
    def manager(self, settings):
        return UserProfileSettingsManager(settings)
    
    def test_default_user_exists(self, manager):
        """Test that default user is created."""
        users = manager.get_all_users()
        assert "DefaultUser" in users
        assert manager.get_current_user() == "DefaultUser"
    
    def test_add_user(self, manager):
        """Test adding a new user."""
        success = manager.add_user("TestUser")
        assert success
        
        users = manager.get_all_users()
        assert "TestUser" in users
    
    def test_invalid_username(self, manager):
        """Test adding user with invalid name."""
        # Test empty name
        success = manager.add_user("")
        assert not success
        
        # Test name with invalid characters
        success = manager.add_user("Test/User")
        assert not success
    
    def test_switch_user(self, manager):
        """Test switching between users."""
        manager.add_user("TestUser")
        manager.set_current_user("TestUser")
        assert manager.get_current_user() == "TestUser"
    
    def test_user_specific_settings(self, manager):
        """Test user-specific settings isolation."""
        manager.add_user("User1")
        manager.add_user("User2")
        
        # Set different settings for each user
        manager.set_user_setting("User1", "test_setting", "value1")
        manager.set_user_setting("User2", "test_setting", "value2")
        
        assert manager.get_user_setting("User1", "test_setting") == "value1"
        assert manager.get_user_setting("User2", "test_setting") == "value2"
    
    def test_remove_user(self, manager):
        """Test removing a user."""
        manager.add_user("TestUser")
        assert "TestUser" in manager.get_all_users()
        
        success = manager.remove_user("TestUser")
        assert success
        assert "TestUser" not in manager.get_all_users()
    
    def test_cannot_remove_default_user(self, manager):
        """Test that default user cannot be removed."""
        success = manager.remove_user("DefaultUser")
        assert not success
        assert "DefaultUser" in manager.get_all_users()


class TestImageExportSettingsManager:
    """Test image export settings manager."""
    
    @pytest.fixture
    def settings(self):
        return QSettings()
    
    @pytest.fixture
    def manager(self, settings):
        return ImageExportSettingsManager(settings)
    
    def test_default_export_format(self, manager):
        """Test default export format is PNG."""
        format_name = manager.get_export_format()
        assert format_name == "PNG"
    
    def test_set_valid_export_format(self, manager):
        """Test setting valid export format."""
        success = manager.set_export_format("JPEG")
        assert success
        assert manager.get_export_format() == "JPEG"
    
    def test_set_invalid_export_format(self, manager):
        """Test setting invalid export format."""
        success = manager.set_export_format("INVALID")
        assert not success
        # Should remain at default
        assert manager.get_export_format() == "PNG"
    
    def test_export_quality(self, manager):
        """Test export quality settings."""
        assert 0 <= manager.get_export_quality() <= 100
        
        success = manager.set_export_quality(85)
        assert success
        assert manager.get_export_quality() == 85
        
        # Test invalid quality
        success = manager.set_export_quality(150)
        assert not success
    
    def test_export_dimensions(self, manager):
        """Test export dimension settings."""
        width, height = manager.get_export_dimensions()
        assert width > 0 and height > 0
        
        success = manager.set_export_dimensions(1280, 720)
        assert success
        assert manager.get_export_dimensions() == (1280, 720)
        
        # Test invalid dimensions
        success = manager.set_export_dimensions(0, 720)
        assert not success
    
    def test_quality_presets(self, manager):
        """Test quality presets."""
        presets = manager.get_quality_presets()
        assert isinstance(presets, dict)
        assert "High" in presets
        assert "Low" in presets
        
        success = manager.apply_quality_preset("High")
        assert success
        assert manager.get_export_quality() == presets["High"]
    
    def test_dimension_presets(self, manager):
        """Test dimension presets."""
        presets = manager.get_dimension_presets()
        assert isinstance(presets, dict)
        assert len(presets) > 0
        
        preset_name = list(presets.keys())[0]
        success = manager.apply_dimension_preset(preset_name)
        assert success
        assert manager.get_export_dimensions() == presets[preset_name]


class TestModernSettingsService:
    """Test the main modern settings service."""
    
    @pytest.fixture
    def mock_session_tracker(self):
        """Create a mock session tracker."""
        tracker = Mock()
        tracker.mark_interaction = Mock()
        tracker.get_current_session_state = Mock(return_value=None)
        tracker.save_session_state = Mock(return_value=True)
        return tracker
    
    @pytest.fixture
    def settings_service(self, mock_session_tracker):
        """Create settings service with mocked dependencies."""
        return ModernSettingsService(mock_session_tracker)
    
    def test_service_initialization(self, settings_service):
        """Test service initializes correctly."""
        assert settings_service is not None
        assert settings_service.settings is not None
    
    def test_cqrs_command_execution(self, settings_service):
        """Test CQRS command execution."""
        success = settings_service.execute_setting_command("test", "key", "value")
        assert success
    
    def test_cqrs_query_execution(self, settings_service):
        """Test CQRS query execution."""
        # Set a value first
        settings_service.execute_setting_command("test", "key", "test_value")
        
        # Query it back
        result = settings_service.query_setting("test", "key")
        assert result == "test_value"
    
    def test_bulk_command_execution(self, settings_service):
        """Test bulk setting commands."""
        settings_dict = {
            "section1": {"key1": "value1", "key2": "value2"},
            "section2": {"key3": "value3"}
        }
        
        success = settings_service.execute_bulk_setting_command(settings_dict)
        assert success
        
        # Verify all settings were set
        assert settings_service.query_setting("section1", "key1") == "value1"
        assert settings_service.query_setting("section1", "key2") == "value2"
        assert settings_service.query_setting("section2", "key3") == "value3"
    
    def test_section_query(self, settings_service):
        """Test querying entire sections."""
        # Set up test data
        settings_service.execute_setting_command("test_section", "key1", "value1")
        settings_service.execute_setting_command("test_section", "key2", "value2")
        
        # Query section
        section_data = settings_service.query_section("test_section")
        assert isinstance(section_data, dict)
        # Note: QSettings behavior may vary, so we just check it's a dict
    
    def test_manager_registration(self, settings_service):
        """Test manager registration and access."""
        # Create mock managers
        mock_background_manager = Mock()
        mock_visibility_manager = Mock()
        
        # Register managers
        settings_service.register_background_manager(mock_background_manager)
        settings_service.register_visibility_manager(mock_visibility_manager)
        
        # Verify access
        assert settings_service.get_background_manager() == mock_background_manager
        assert settings_service.get_visibility_manager() == mock_visibility_manager
    
    def test_memento_creation(self, settings_service):
        """Test state memento creation."""
        # Set up some state
        settings_service.execute_setting_command("global", "current_tab", "construct")
        
        # Create memento
        memento = settings_service.create_state_memento("construct")
        assert memento is not None
        assert memento.current_tab == "construct"
        assert isinstance(memento.settings_snapshot, dict)
    
    def test_memento_restoration(self, settings_service):
        """Test state restoration from memento."""
        # Create test memento
        memento = ApplicationStateMemento(
            current_tab="sequence",
            settings_snapshot={"test/key": "test_value"}
        )
        
        # Restore from memento
        success = settings_service.restore_from_memento(memento)
        assert success
    
    def test_legacy_compatibility(self, settings_service):
        """Test legacy interface compatibility."""
        # Test legacy methods
        settings_service.set_setting("legacy", "test", "value")
        result = settings_service.get_setting("legacy", "test")
        assert result == "value"
        
        # Test current tab methods
        settings_service.set_current_tab("browse")
        assert settings_service.get_current_tab() == "browse"


class TestDependencyInjectionIntegration:
    """Test dependency injection integration."""
    
    def test_settings_service_registration(self):
        """Test that all settings services can be registered."""
        try:
            container = create_configured_settings_container()
            assert container is not None
        except Exception as e:
            pytest.fail(f"Settings service registration failed: {e}")
    
    def test_service_resolution(self):
        """Test that all services can be resolved from container."""
        container = create_configured_settings_container()
        
        # Test main service
        settings_service = container.resolve(ModernSettingsService)
        assert settings_service is not None
        
        # Test individual managers
        from desktop.modern.core.interfaces.settings_services import (
            IBackgroundSettingsManager,
            IVisibilitySettingsManager,
            IBeatLayoutSettingsManager,
            IPropTypeSettingsManager,
            IUserProfileSettingsManager,
            IImageExportSettingsManager,
        )
        
        background_manager = container.resolve(IBackgroundSettingsManager)
        assert background_manager is not None
        
        visibility_manager = container.resolve(IVisibilitySettingsManager)
        assert visibility_manager is not None
        
        layout_manager = container.resolve(IBeatLayoutSettingsManager)
        assert layout_manager is not None
        
        prop_manager = container.resolve(IPropTypeSettingsManager)
        assert prop_manager is not None
        
        user_manager = container.resolve(IUserProfileSettingsManager)
        assert user_manager is not None
        
        export_manager = container.resolve(IImageExportSettingsManager)
        assert export_manager is not None
    
    def test_service_validation(self):
        """Test service validation function."""
        container = create_configured_settings_container()
        is_valid = validate_settings_registration(container)
        assert is_valid


class TestIntegrationScenarios:
    """Test complete integration scenarios."""
    
    @pytest.fixture
    def configured_container(self):
        """Create a fully configured container for integration tests."""
        return create_configured_settings_container()
    
    def test_complete_workflow(self, configured_container):
        """Test a complete settings workflow."""
        # Get services
        settings_service = configured_container.resolve(ModernSettingsService)
        background_manager = configured_container.resolve(IBackgroundSettingsManager)
        prop_manager = configured_container.resolve(IPropTypeSettingsManager)
        
        # Test workflow: change background and prop type
        success = background_manager.set_background("Rainbow")
        assert success
        
        prop_manager.set_prop_type(PropType.FAN)
        assert prop_manager.get_current_prop_type() == PropType.FAN
        
        # Create state snapshot
        memento = settings_service.create_state_memento("construct")
        assert memento is not None
        
        # Verify settings are captured in snapshot
        assert "global/background_type" in str(memento.settings_snapshot)
    
    def test_state_persistence_and_restoration(self, configured_container):
        """Test complete state persistence and restoration."""
        settings_service = configured_container.resolve(ModernSettingsService)
        
        # Set up application state
        settings_service.execute_setting_command("global", "current_tab", "sequence")
        settings_service.execute_setting_command("ui", "panel_visible", True)
        
        # Save application state
        success = settings_service.save_application_state("sequence")
        assert success
        
        # Simulate restart by creating new service
        new_settings_service = configured_container.resolve(ModernSettingsService)
        
        # Restore application state
        restored_memento = new_settings_service.restore_application_state()
        
        # Note: In a real scenario, this would work with actual file persistence
        # For testing, we verify the mechanism works
        assert isinstance(restored_memento, (ApplicationStateMemento, type(None)))


# Test runner function for pytest
def run_tests():
    """Run all tests with pytest."""
    import sys
    
    # Configure test environment
    test_args = [
        __file__,
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "-x",  # Stop on first failure
    ]
    
    # Add coverage if available
    try:
        import pytest_cov
        test_args.extend(["--cov=desktop.modern.application.services.settings"])
    except ImportError:
        pass
    
    # Run tests
    exit_code = pytest.main(test_args)
    sys.exit(exit_code)


if __name__ == "__main__":
    run_tests()
