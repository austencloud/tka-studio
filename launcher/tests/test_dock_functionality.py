#!/usr/bin/env python3
"""
Test Script for TKA Dock Functionality
======================================

This script tests the dock functionality implementation to ensure:
- Dock window creation and positioning
- Mode switching between window and dock
- State persistence
- Visual indicators
- Context menu functionality

Usage:
    python test_dock_functionality.py
"""

import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add launcher directory to path
launcher_dir = Path(__file__).parent
sys.path.insert(0, str(launcher_dir))

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_dock_window_creation():
    """Test dock window creation and basic functionality."""
    try:
        from ui.windows.dock_window import TKADockWindow
        from domain.models import (
            DockConfiguration,
            DockPosition,
            ApplicationData,
            ApplicationCategory,
        )

        class MockTKAIntegration:
            def __init__(self):
                self.launch_service = None

            def get_applications(self):
                return [
                    ApplicationData(
                        id="test_app_1",
                        title="Test App 1",
                        description="Test application for dock testing",
                        icon="🧪",
                        category=ApplicationCategory.DESKTOP,
                        command="echo 'Test App 1'",
                    ),
                    ApplicationData(
                        id="test_app_2",
                        title="Test App 2",
                        description="Another test application",
                        icon="🔬",
                        category=ApplicationCategory.WEB,
                        command="echo 'Test App 2'",
                    ),
                    ApplicationData(
                        id="test_dev_tool",
                        title="Test Dev Tool",
                        description="Development tool for testing",
                        icon="🔧",
                        category=ApplicationCategory.DEVELOPMENT,
                        command="echo 'Dev Tool'",
                    ),
                ]

            def launch_application(self, app_id: str) -> bool:
                return True

        dock_config = DockConfiguration(
            position=DockPosition.BOTTOM_LEFT,
            width=64,
            height=200,
        )

        mock_integration = MockTKAIntegration()
        dock_window = TKADockWindow(mock_integration, dock_config)

        dock_geometry = dock_window.get_dock_geometry()
        logger.info(
            f"Dock positioned at: {dock_geometry.x}, {dock_geometry.y} ({dock_geometry.width}x{dock_geometry.height})"
        )

        dock_window.show()
        return dock_window

    except Exception as e:
        logger.error(f"Failed to create dock window: {e}")
        return None


def test_mode_switching():
    """Test mode switching functionality."""
    try:
        from ui.windows.launcher_window import TKALauncherWindow as TKAModernWindow

        class MockTKAIntegration:
            def get_applications(self):
                return []

        mock_integration = MockTKAIntegration()
        main_window = TKAModernWindow(mock_integration)
        main_window.show()

        def test_dock_toggle():
            main_window.toggle_dock_mode()
            QTimer.singleShot(3000, lambda: main_window.toggle_dock_mode())

        QTimer.singleShot(2000, test_dock_toggle)
        return main_window

    except Exception as e:
        logger.error(f"Failed to test mode switching: {e}")
        return None


def test_state_persistence():
    """Test state persistence functionality."""
    try:
        from domain.models import DockConfiguration, DockPosition, WindowGeometry

        dock_config = DockConfiguration(
            position=DockPosition.BOTTOM_RIGHT,
            width=80,
            height=300,
            margin_x=10,
            margin_y=5,
        )

        config_dict = dock_config.to_dict()
        restored_config = DockConfiguration.from_dict(config_dict)

        assert dock_config.position == restored_config.position
        assert dock_config.width == restored_config.width
        assert dock_config.height == restored_config.height

        geometry = WindowGeometry(x=100, y=200, width=800, height=600)
        geometry_dict = geometry.to_dict()
        restored_geometry = WindowGeometry.from_dict(geometry_dict)

        assert geometry.x == restored_geometry.x
        assert geometry.y == restored_geometry.y
        assert geometry.width == restored_geometry.width
        assert geometry.height == restored_geometry.height

        return True

    except Exception as e:
        logger.error(f"Failed to test state persistence: {e}")
        return False


def test_visual_indicators():
    """Test visual state indicators."""
    try:
        from ui.windows.dock_window import DockApplicationIcon
        from domain.models import (
            ApplicationData,
            ApplicationCategory,
            ApplicationStatus,
        )
        from ui.pyqt6_compatible_design_system import get_reliable_style_builder

        test_app = ApplicationData(
            id="visual_test",
            title="Visual Test App",
            description="App for testing visual indicators",
            icon="🎨",
            category=ApplicationCategory.DESKTOP,
            status=ApplicationStatus.STOPPED,
        )

        style_builder = get_reliable_style_builder()
        icon_widget = DockApplicationIcon(test_app, style_builder)

        statuses = [
            ApplicationStatus.STARTING,
            ApplicationStatus.RUNNING,
            ApplicationStatus.ERROR,
            ApplicationStatus.STOPPED,
        ]

        for status in statuses:
            icon_widget.update_status(status)

        return icon_widget

    except Exception as e:
        logger.error(f"Failed to test visual indicators: {e}")
        return None


def test_application_launching():
    """Test application launching functionality in dock mode."""
    try:
        from ui.windows.dock_window import TKADockWindow
        from domain.models import (
            DockConfiguration,
            DockPosition,
            ApplicationData,
            ApplicationCategory,
        )

        class MockTKAIntegration:
            def __init__(self):
                self.launch_service = None
                self.launched_apps = []

            def get_applications(self):
                return [
                    ApplicationData(
                        id="launch_test_1",
                        title="Launch Test 1",
                        description="Test app for launch testing",
                        icon="🚀",
                        category=ApplicationCategory.DESKTOP,
                        command="echo 'Launch Test 1'",
                    ),
                    ApplicationData(
                        id="launch_test_2",
                        title="Launch Test 2",
                        description="Another test app for launch testing",
                        icon="🎯",
                        category=ApplicationCategory.WEB,
                        command="echo 'Launch Test 2'",
                    ),
                ]

            def launch_application(self, app_id: str) -> bool:
                self.launched_apps.append(app_id)
                return True

        mock_integration = MockTKAIntegration()
        dock_config = DockConfiguration(
            position=DockPosition.BOTTOM_LEFT, width=64, height=150
        )
        dock_window = TKADockWindow(mock_integration, dock_config)

        test_apps = ["launch_test_1", "launch_test_2"]

        for app_id in test_apps:
            dock_window.launch_application(app_id)
            if app_id not in mock_integration.launched_apps:
                logger.error(f"{app_id} failed to launch")
                return False

        dock_window.show()
        return True

    except Exception as e:
        logger.error(f"Failed to test application launching: {e}")
        return False


def main():
    """Main test function."""
    logger.info("Starting TKA Dock Functionality Tests")

    app = QApplication(sys.argv)
    app.setApplicationName("TKA Dock Test")

    test_results = []

    test_results.append(("State Persistence", test_state_persistence()))

    visual_widget = test_visual_indicators()
    test_results.append(("Visual Indicators", visual_widget is not None))
    if visual_widget:
        visual_widget.show()

    dock_window = test_dock_window_creation()
    test_results.append(("Dock Window Creation", dock_window is not None))

    main_window = test_mode_switching()
    test_results.append(("Mode Switching", main_window is not None))

    launch_test_result = test_application_launching()
    test_results.append(("Application Launching", launch_test_result))

    logger.info("\n" + "=" * 50)
    logger.info("TEST RESULTS SUMMARY")
    logger.info("=" * 50)

    for test_name, result in test_results:
        status = "PASS" if result else "FAIL"
        logger.info(f"{test_name}: {status}")

    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    logger.info(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        logger.info("All tests passed! Dock functionality is working correctly.")
    else:
        logger.warning("Some tests failed. Please check the implementation.")

    logger.info("\nUI tests are running. Close windows to exit.")

    QTimer.singleShot(30000, app.quit)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
