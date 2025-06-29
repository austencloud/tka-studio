#!/usr/bin/env python3
"""
Component Integration Tests for Refactored TKA Launcher
======================================================

Tests integration between refactored helper classes and components:
- Helper manager compatibility and API consistency
- Import resolution for all new modules
- Component interaction and signal flow
- API compatibility between refactored classes

These tests ensure the refactored architecture maintains functionality
and catches compatibility issues during future refactoring phases.
"""

import pytest
import logging
from unittest.mock import Mock, MagicMock, patch
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QRect, QTimer

# Import all the refactored components
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dock_window import TKADockWindow
from dock_components import DockApplicationIcon
from dock_context_menu import DockContextMenuManager
from dock_position_manager import DockPositionManager
from dock_application_manager import DockApplicationManager
from dock_window_setup import DockWindowSetup
from window_mode_manager import WindowModeManager
from window_geometry_manager import WindowGeometryManager

from domain.models import (
    ApplicationData,
    ApplicationCategory,
    ApplicationStatus,
    DockConfiguration,
    DockPosition,
)
from config.config.launcher_config import LauncherConfig

logger = logging.getLogger(__name__)


class TestRefactoredComponents:
    """Test integration between refactored components."""

    @pytest.fixture
    def sample_applications(self):
        """Create sample application data for testing."""
        return [
            ApplicationData(
                id="app1",
                title="Test App 1",
                description="First test app",
                category=ApplicationCategory.DESKTOP,
                icon="🚀",
                executable_path="/test/app1",
                status=ApplicationStatus.STOPPED,
                display_order=1,
            ),
            ApplicationData(
                id="app2",
                title="Test App 2",
                description="Second test app",
                category=ApplicationCategory.WEB,
                icon="🌐",
                executable_path="/test/app2",
                status=ApplicationStatus.RUNNING,
                display_order=2,
            ),
        ]

    @pytest.fixture
    def mock_tka_integration(self, sample_applications):
        """Create mock TKA integration."""
        mock = Mock()
        mock.get_applications.return_value = sample_applications
        mock.launch_application.return_value = True
        return mock

    @pytest.fixture
    def dock_config(self):
        """Create test dock configuration."""
        return DockConfiguration(
            position=DockPosition.BOTTOM_LEFT,
            width=64,
            height=200,
            margin_x=10,
            margin_y=10,
            always_on_top=True,
            auto_hide=False,
        )

    def test_dock_position_manager_integration(self, dock_config):
        """Test dock position manager functionality."""
        try:
            position_manager = DockPositionManager(dock_config)

            # Test height calculations
            height = position_manager.calculate_dock_height(5)
            assert height > 0
            assert height == position_manager.calculate_actual_dock_height([Mock()] * 5)

            # Test position calculations
            screen_rect = QRect(0, 0, 1920, 1080)
            dock_rect = position_manager.calculate_dock_position(screen_rect, height)
            assert dock_rect.width() == dock_config.width
            assert dock_rect.height() == height

            # Test validation
            assert position_manager.validate_position(dock_rect)

            logger.info("✅ Dock position manager integration test passed")

        except Exception as e:
            pytest.fail(f"❌ Dock position manager integration failed: {e}")

    def test_dock_application_manager_integration(
        self, qtbot, mock_tka_integration, sample_applications
    ):
        """Test dock application manager functionality."""
        try:
            from ui.reliable_design_system import get_reliable_style_builder

            with patch(
                "ui.reliable_design_system.get_reliable_style_builder"
            ) as mock_style:
                mock_style.return_value = Mock()

                app_manager = DockApplicationManager(
                    mock_tka_integration, mock_style.return_value
                )

                # Test application loading
                success = app_manager.load_applications()
                assert success
                assert len(app_manager.get_applications()) == len(sample_applications)

                # Test application retrieval
                app = app_manager.get_application_by_id("app1")
                assert app is not None
                assert app.title == "Test App 1"

                # Test status updates
                app_manager.update_application_status(
                    "app1", ApplicationStatus.STARTING
                )

                # Test manager info
                info = app_manager.get_manager_info()
                assert info["total_applications"] == len(sample_applications)

                logger.info("✅ Dock application manager integration test passed")

        except Exception as e:
            pytest.fail(f"❌ Dock application manager integration failed: {e}")

    def test_dock_window_setup_integration(self, qtbot, dock_config):
        """Test dock window setup functionality."""
        try:
            window_setup = DockWindowSetup(dock_config)

            # Create test widget
            test_widget = QWidget()
            qtbot.addWidget(test_widget)

            # Test window setup
            window_setup.setup_dock_window(test_widget)

            # Test layout setup
            main_layout, icons_container, icons_layout = window_setup.setup_layout(
                test_widget
            )
            assert main_layout is not None
            assert icons_container is not None
            assert icons_layout is not None

            # Test styling
            window_setup.setup_styling(test_widget)

            # Test size configuration
            window_setup.apply_size_configuration(test_widget, 300)
            assert test_widget.width() == dock_config.width
            assert test_widget.height() == 300

            # Test configuration validation
            assert window_setup.validate_configuration()

            logger.info("✅ Dock window setup integration test passed")

        except Exception as e:
            pytest.fail(f"❌ Dock window setup integration failed: {e}")

    def test_dock_context_menu_manager_integration(self, qtbot, sample_applications):
        """Test dock context menu manager functionality."""
        try:
            context_manager = DockContextMenuManager()

            # Test menu creation
            menu = context_manager.create_context_menu(
                "app1", sample_applications, None
            )
            assert menu is not None

            # Test signal connections (signals should exist)
            assert hasattr(context_manager, "launch_requested")
            assert hasattr(context_manager, "stop_requested")
            assert hasattr(context_manager, "restart_requested")

            logger.info("✅ Dock context menu manager integration test passed")

        except Exception as e:
            pytest.fail(f"❌ Dock context menu manager integration failed: {e}")

    def test_dock_components_integration(self, qtbot, sample_applications):
        """Test dock components functionality."""
        try:
            with patch(
                "ui.reliable_design_system.get_reliable_style_builder"
            ) as mock_style:
                mock_style.return_value = Mock()

                # Test dock application icon
                app_data = sample_applications[0]
                icon = DockApplicationIcon(app_data, mock_style.return_value)
                qtbot.addWidget(icon)

                # Test icon properties
                assert icon.app_data == app_data
                assert icon.current_status == app_data.status

                # Test status updates
                icon.update_status(ApplicationStatus.RUNNING)
                assert icon.current_status == ApplicationStatus.RUNNING

                # Test signals exist
                assert hasattr(icon, "launch_requested")
                assert hasattr(icon, "context_menu_requested")

                logger.info("✅ Dock components integration test passed")

        except Exception as e:
            pytest.fail(f"❌ Dock components integration failed: {e}")

    def test_window_mode_manager_integration(self, mock_tka_integration):
        """Test window mode manager functionality."""
        try:
            mode_manager = WindowModeManager()

            # Test initial state
            assert mode_manager.get_current_mode() == "window"

            # Test component setting
            mock_window = Mock()
            mode_manager.set_components(mock_window, mock_tka_integration)
            assert mode_manager.main_window == mock_window
            assert mode_manager.tka_integration == mock_tka_integration

            # Test mode info
            info = mode_manager.get_mode_info()
            assert "current_mode" in info
            assert "has_dock_window" in info

            # Test signals exist
            assert hasattr(mode_manager, "mode_changed")
            assert hasattr(mode_manager, "dock_mode_requested")

            logger.info("✅ Window mode manager integration test passed")

        except Exception as e:
            pytest.fail(f"❌ Window mode manager integration failed: {e}")

    def test_window_geometry_manager_integration(self, qtbot, tmp_path):
        """Test window geometry manager functionality."""
        try:
            # Create test config
            config_file = tmp_path / "test_config.json"
            config = LauncherConfig(config_file)

            geometry_manager = WindowGeometryManager(config)

            # Create test widget
            test_widget = QWidget()
            qtbot.addWidget(test_widget)

            # Test geometry setup
            geometry_manager.setup_window_geometry(test_widget)

            # Test geometry validation
            test_rect = QRect(100, 100, 800, 600)
            assert geometry_manager.validate_geometry(test_rect)

            # Test screen info
            screen_info = geometry_manager.get_screen_info()
            assert "screen_count" in screen_info
            assert "screens" in screen_info

            logger.info("✅ Window geometry manager integration test passed")

        except Exception as e:
            pytest.fail(f"❌ Window geometry manager integration failed: {e}")

    def test_all_imports_resolve(self):
        """Test that all refactored modules can be imported without errors."""
        try:
            # Test all imports work
            import launcher.dock_window
            import launcher.dock_components
            import launcher.dock_context_menu
            import launcher.dock_position_manager
            import launcher.dock_application_manager
            import launcher.dock_window_setup
            import launcher.window_mode_manager
            import launcher.window_geometry_manager

            logger.info("✅ All imports resolve test passed")

        except ImportError as e:
            pytest.fail(f"❌ Import resolution failed: {e}")

    def test_api_compatibility_between_components(
        self, qtbot, mock_tka_integration, dock_config, sample_applications
    ):
        """Test API compatibility between refactored components."""
        try:
            with patch(
                "ui.reliable_design_system.get_reliable_style_builder"
            ) as mock_style:
                mock_style.return_value = Mock()

                # Create all managers
                position_manager = DockPositionManager(dock_config)
                app_manager = DockApplicationManager(
                    mock_tka_integration, mock_style.return_value
                )
                window_setup = DockWindowSetup(dock_config)
                context_manager = DockContextMenuManager()

                # Test that they can work together
                app_manager.load_applications()
                height = position_manager.calculate_actual_dock_height(
                    app_manager.get_applications()
                )

                # Create test widget for setup
                test_widget = QWidget()
                qtbot.addWidget(test_widget)

                window_setup.setup_dock_window(test_widget)
                window_setup.apply_size_configuration(test_widget, height)

                # Test context menu with applications
                menu = context_manager.create_context_menu(
                    "app1", app_manager.get_applications(), None
                )
                assert menu is not None

                logger.info("✅ API compatibility between components test passed")

        except Exception as e:
            pytest.fail(f"❌ API compatibility between components failed: {e}")


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
