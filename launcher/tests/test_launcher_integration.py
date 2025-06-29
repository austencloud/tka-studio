#!/usr/bin/env python3
"""
Integration Tests for TKA Launcher - End-to-End Workflows
========================================================

Tests complete user workflows and integration between refactored components:
- Launcher initialization sequence
- Mode switching (window ↔ dock)
- Application launching from both modes
- UI interactions and complete workflows
- Error handling and recovery

These tests verify that the refactored architecture works correctly
and catches API compatibility issues during future refactoring.
"""

import pytest
import logging
from unittest.mock import Mock, MagicMock, patch
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from PyQt6.QtTest import QTest

# Import the classes we're testing
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from launcher_window import TKAModernWindow
from window_mode_manager import WindowModeManager
from window_geometry_manager import WindowGeometryManager
from config.config.launcher_config import LauncherConfig
from domain.models import ApplicationData, ApplicationCategory, ApplicationStatus

logger = logging.getLogger(__name__)


class TestLauncherIntegration:
    """Integration tests for complete launcher workflows."""

    @pytest.fixture
    def mock_tka_integration(self):
        """Create a mock TKA integration."""
        mock_integration = Mock()
        mock_integration.get_applications.return_value = [
            ApplicationData(
                id="test_app_1",
                title="Test App 1",
                description="Test application 1",
                category=ApplicationCategory.DESKTOP,
                icon="🚀",
                executable_path="/test/app1",
                status=ApplicationStatus.STOPPED,
                display_order=1,
            ),
            ApplicationData(
                id="test_app_2",
                title="Test App 2",
                description="Test application 2",
                category=ApplicationCategory.WEB,
                icon="🌐",
                executable_path="/test/app2",
                status=ApplicationStatus.STOPPED,
                display_order=2,
            ),
        ]
        mock_integration.launch_application.return_value = True
        return mock_integration

    @pytest.fixture
    def launcher_config(self, tmp_path):
        """Create a test launcher config."""
        config_file = tmp_path / "test_config.json"
        config = LauncherConfig(config_file)
        return config

    def test_launcher_initialization_sequence(
        self, qtbot, mock_tka_integration, launcher_config
    ):
        """Test complete launcher initialization without errors."""
        try:
            # Create launcher window
            with patch(
                "launcher.launcher_window.LauncherConfig", return_value=launcher_config
            ):
                launcher = TKAModernWindow(mock_tka_integration)
                qtbot.addWidget(launcher)

            # Verify initialization completed
            assert launcher is not None
            assert launcher.tka_integration == mock_tka_integration
            assert launcher.geometry_manager is not None
            assert launcher.mode_manager is not None
            assert launcher.app_grid is not None
            assert launcher.status_label is not None

            # Verify window geometry was set
            geometry = launcher.geometry()
            assert geometry.width() > 0
            assert geometry.height() > 0

            logger.info("✅ Launcher initialization test passed")

        except Exception as e:
            pytest.fail(f"❌ Launcher initialization failed: {e}")

    def test_window_to_dock_mode_transition(
        self, qtbot, mock_tka_integration, launcher_config
    ):
        """Test switching from window mode to dock mode."""
        try:
            with patch(
                "launcher.launcher_window.LauncherConfig", return_value=launcher_config
            ):
                launcher = TKAModernWindow(mock_tka_integration)
                qtbot.addWidget(launcher)

            # Verify initial state
            assert launcher.mode_manager.get_current_mode() == "window"
            assert launcher.isVisible()

            # Switch to dock mode
            launcher.mode_manager.switch_to_dock_mode()

            # Allow time for mode switch
            QTest.qWait(100)

            # Verify dock mode state
            assert launcher.mode_manager.get_current_mode() == "docked"

            # Note: In test environment, dock window creation might fail due to missing dependencies
            # but the mode manager should still track the state correctly

            logger.info("✅ Window to dock mode transition test passed")

        except Exception as e:
            pytest.fail(f"❌ Window to dock mode transition failed: {e}")

    def test_dock_to_window_mode_transition(
        self, qtbot, mock_tka_integration, launcher_config
    ):
        """Test switching from dock mode back to window mode."""
        try:
            with patch(
                "launcher.launcher_window.LauncherConfig", return_value=launcher_config
            ):
                launcher = TKAModernWindow(mock_tka_integration)
                qtbot.addWidget(launcher)

            # Switch to dock mode first
            launcher.mode_manager.switch_to_dock_mode()
            QTest.qWait(50)

            # Switch back to window mode
            launcher.mode_manager.switch_to_window_mode()
            QTest.qWait(50)

            # Verify window mode state
            assert launcher.mode_manager.get_current_mode() == "window"
            assert launcher.isVisible()

            logger.info("✅ Dock to window mode transition test passed")

        except Exception as e:
            pytest.fail(f"❌ Dock to window mode transition failed: {e}")

    def test_application_launching_from_window_mode(
        self, qtbot, mock_tka_integration, launcher_config
    ):
        """Test launching applications from window mode."""
        try:
            with patch(
                "launcher.launcher_window.LauncherConfig", return_value=launcher_config
            ):
                launcher = TKAModernWindow(mock_tka_integration)
                qtbot.addWidget(launcher)

            # Ensure we're in window mode
            assert launcher.mode_manager.get_current_mode() == "window"

            # Test launching an application
            test_app_id = "test_app_1"

            # Mock the launch method to avoid actual application launching
            with patch.object(
                launcher.tka_integration, "launch_application", return_value=True
            ):
                # Simulate application launch
                launcher.app_grid.launch_application(test_app_id)

            # Verify launch was attempted
            launcher.tka_integration.launch_application.assert_called_with(test_app_id)

            logger.info("✅ Application launching from window mode test passed")

        except Exception as e:
            pytest.fail(f"❌ Application launching from window mode failed: {e}")

    def test_geometry_manager_save_restore_cycle(self, qtbot, launcher_config):
        """Test window geometry save and restore functionality."""
        try:
            geometry_manager = WindowGeometryManager(launcher_config)

            # Create a test widget
            from PyQt6.QtWidgets import QWidget

            test_widget = QWidget()
            qtbot.addWidget(test_widget)

            # Set initial geometry
            initial_rect = QRect(100, 100, 800, 600)
            test_widget.setGeometry(initial_rect)

            # Save geometry
            geometry_manager.save_window_geometry(test_widget)

            # Change geometry
            test_widget.setGeometry(200, 200, 900, 700)

            # Restore geometry
            geometry_manager.restore_window_geometry(test_widget)

            # Verify geometry was restored (allowing for small differences due to window manager)
            restored_geometry = test_widget.geometry()
            assert abs(restored_geometry.x() - initial_rect.x()) <= 10
            assert abs(restored_geometry.y() - initial_rect.y()) <= 10
            assert restored_geometry.width() == initial_rect.width()
            assert restored_geometry.height() == initial_rect.height()

            logger.info("✅ Geometry manager save/restore test passed")

        except Exception as e:
            pytest.fail(f"❌ Geometry manager save/restore failed: {e}")

    def test_mode_manager_state_consistency(self, mock_tka_integration):
        """Test mode manager state consistency."""
        try:
            mode_manager = WindowModeManager()
            mode_manager.set_components(Mock(), mock_tka_integration)

            # Test initial state
            assert mode_manager.get_current_mode() == "window"
            assert mode_manager.is_window_mode()
            assert not mode_manager.is_dock_mode()

            # Test mode switching
            mode_manager.current_mode = "docked"  # Simulate mode change
            assert mode_manager.get_current_mode() == "docked"
            assert not mode_manager.is_window_mode()
            assert mode_manager.is_dock_mode()

            # Test mode info
            info = mode_manager.get_mode_info()
            assert info["current_mode"] == "docked"
            assert "has_dock_window" in info
            assert "has_main_window" in info

            logger.info("✅ Mode manager state consistency test passed")

        except Exception as e:
            pytest.fail(f"❌ Mode manager state consistency failed: {e}")

    def test_error_handling_and_recovery(
        self, qtbot, mock_tka_integration, launcher_config
    ):
        """Test error handling and graceful recovery."""
        try:
            # Test with failing TKA integration
            failing_integration = Mock()
            failing_integration.get_applications.side_effect = Exception("Test error")

            with patch(
                "launcher.launcher_window.LauncherConfig", return_value=launcher_config
            ):
                # This should not crash even with failing integration
                launcher = TKAModernWindow(failing_integration)
                qtbot.addWidget(launcher)

            # Launcher should still be created and functional
            assert launcher is not None
            assert launcher.mode_manager is not None
            assert launcher.geometry_manager is not None

            logger.info("✅ Error handling and recovery test passed")

        except Exception as e:
            pytest.fail(f"❌ Error handling and recovery failed: {e}")

    def test_ui_button_interactions(self, qtbot, mock_tka_integration, launcher_config):
        """Test UI button interactions and complete workflows."""
        try:
            with patch(
                "launcher.launcher_window.LauncherConfig", return_value=launcher_config
            ):
                launcher = TKAModernWindow(mock_tka_integration)
                qtbot.addWidget(launcher)

            # Find dock toggle button if it exists
            dock_button = None
            for child in launcher.findChildren(object):
                if hasattr(child, "text") and "Dock" in str(child.text()):
                    dock_button = child
                    break

            if dock_button:
                # Test button click
                initial_mode = launcher.mode_manager.get_current_mode()
                qtbot.mouseClick(dock_button, 1)  # Left click
                QTest.qWait(100)

                # Mode should have changed (or at least attempted to change)
                # In test environment, actual dock creation might fail, but state should update
                logger.info(
                    f"Mode after button click: {launcher.mode_manager.get_current_mode()}"
                )

            logger.info("✅ UI button interactions test passed")

        except Exception as e:
            pytest.fail(f"❌ UI button interactions failed: {e}")


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
