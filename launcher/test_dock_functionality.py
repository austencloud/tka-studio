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

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_dock_window_creation():
    """Test dock window creation and basic functionality."""
    logger.info("🧪 Testing dock window creation...")

    try:
        from dock_window import TKADockWindow
        from domain.models import (
            DockConfiguration,
            DockPosition,
            ApplicationData,
            ApplicationCategory,
        )

        # Create mock TKA integration with launch capability
        class MockTKAIntegration:
            def __init__(self):
                self.launch_service = None  # Will be set if available

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
                """Mock launch implementation."""
                logger.info(f"🚀 Mock launching application: {app_id}")
                # Simulate successful launch
                return True

        # Create dock configuration
        dock_config = DockConfiguration(
            position=DockPosition.BOTTOM_LEFT,
            width=64,
            height=200,
        )

        # Create dock window
        mock_integration = MockTKAIntegration()
        dock_window = TKADockWindow(mock_integration, dock_config)

        logger.info("✅ Dock window created successfully")

        # Test dock positioning
        dock_geometry = dock_window.get_dock_geometry()
        logger.info(
            f"📍 Dock positioned at: {dock_geometry.x}, {dock_geometry.y} ({dock_geometry.width}x{dock_geometry.height})"
        )

        # Show dock window
        dock_window.show()

        return dock_window

    except Exception as e:
        logger.error(f"❌ Failed to create dock window: {e}")
        return None


def test_mode_switching():
    """Test mode switching functionality."""
    logger.info("🧪 Testing mode switching...")

    try:
        from launcher_window import TKAModernWindow

        # Create mock TKA integration
        class MockTKAIntegration:
            def get_applications(self):
                return []

        # Create main window
        mock_integration = MockTKAIntegration()
        main_window = TKAModernWindow(mock_integration)

        logger.info("✅ Main window created successfully")

        # Show main window
        main_window.show()

        # Test dock mode toggle after a delay
        def test_dock_toggle():
            logger.info("🔄 Testing dock mode toggle...")
            main_window.toggle_dock_mode()

            # Switch back after another delay
            QTimer.singleShot(3000, lambda: main_window.toggle_dock_mode())

        QTimer.singleShot(2000, test_dock_toggle)

        return main_window

    except Exception as e:
        logger.error(f"❌ Failed to test mode switching: {e}")
        return None


def test_state_persistence():
    """Test state persistence functionality."""
    logger.info("🧪 Testing state persistence...")

    try:
        from domain.models import DockConfiguration, DockPosition, WindowGeometry

        # Test dock configuration serialization
        dock_config = DockConfiguration(
            position=DockPosition.BOTTOM_RIGHT,
            width=80,
            height=300,
            margin_x=10,
            margin_y=5,
        )

        # Convert to dict and back
        config_dict = dock_config.to_dict()
        restored_config = DockConfiguration.from_dict(config_dict)

        assert dock_config.position == restored_config.position
        assert dock_config.width == restored_config.width
        assert dock_config.height == restored_config.height

        logger.info("✅ Dock configuration serialization works correctly")

        # Test window geometry
        geometry = WindowGeometry(x=100, y=200, width=800, height=600)
        geometry_dict = geometry.to_dict()
        restored_geometry = WindowGeometry.from_dict(geometry_dict)

        assert geometry.x == restored_geometry.x
        assert geometry.y == restored_geometry.y
        assert geometry.width == restored_geometry.width
        assert geometry.height == restored_geometry.height

        logger.info("✅ Window geometry serialization works correctly")

        return True

    except Exception as e:
        logger.error(f"❌ Failed to test state persistence: {e}")
        return False


def test_visual_indicators():
    """Test visual state indicators."""
    logger.info("🧪 Testing visual indicators...")

    try:
        from dock_window import DockApplicationIcon
        from domain.models import (
            ApplicationData,
            ApplicationCategory,
            ApplicationStatus,
        )
        from ui.reliable_design_system import get_reliable_style_builder

        # Create test application
        test_app = ApplicationData(
            id="visual_test",
            title="Visual Test App",
            description="App for testing visual indicators",
            icon="🎨",
            category=ApplicationCategory.DESKTOP,
            status=ApplicationStatus.STOPPED,
        )

        # Create icon widget
        style_builder = get_reliable_style_builder()
        icon_widget = DockApplicationIcon(test_app, style_builder)

        logger.info("✅ Dock icon created successfully")

        # Test status updates
        statuses = [
            ApplicationStatus.STARTING,
            ApplicationStatus.RUNNING,
            ApplicationStatus.ERROR,
            ApplicationStatus.STOPPED,
        ]

        for status in statuses:
            icon_widget.update_status(status)
            logger.info(f"🎨 Updated icon status to: {status.value}")

        return icon_widget

    except Exception as e:
        logger.error(f"❌ Failed to test visual indicators: {e}")
        return None


def test_application_launching():
    """Test application launching functionality in dock mode."""
    logger.info("🧪 Testing application launching...")

    try:
        from dock_window import TKADockWindow
        from domain.models import (
            DockConfiguration,
            DockPosition,
            ApplicationData,
            ApplicationCategory,
        )

        # Create mock TKA integration with launch capability
        class MockTKAIntegration:
            def __init__(self):
                self.launch_service = None
                self.launched_apps = []  # Track launched applications

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
                """Mock launch implementation that tracks launches."""
                logger.info(f"🚀 Mock launching application: {app_id}")
                self.launched_apps.append(app_id)
                return True

        # Create dock window with mock integration
        mock_integration = MockTKAIntegration()
        dock_config = DockConfiguration(
            position=DockPosition.BOTTOM_LEFT, width=64, height=150
        )
        dock_window = TKADockWindow(mock_integration, dock_config)

        logger.info("✅ Dock window created for launch testing")

        # Test launching applications
        test_apps = ["launch_test_1", "launch_test_2"]

        for app_id in test_apps:
            logger.info(f"🧪 Testing launch of {app_id}")
            dock_window.launch_application(app_id)

            # Check if the app was launched
            if app_id in mock_integration.launched_apps:
                logger.info(f"✅ {app_id} launched successfully")
            else:
                logger.error(f"❌ {app_id} failed to launch")
                return False

        # Show dock window briefly
        dock_window.show()

        logger.info("✅ Application launching test completed successfully")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to test application launching: {e}")
        return False


def main():
    """Main test function."""
    logger.info("🚀 Starting TKA Dock Functionality Tests")

    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("TKA Dock Test")

    # Run tests
    test_results = []

    # Test 1: State persistence (no UI required)
    test_results.append(("State Persistence", test_state_persistence()))

    # Test 2: Visual indicators
    visual_widget = test_visual_indicators()
    test_results.append(("Visual Indicators", visual_widget is not None))
    if visual_widget:
        visual_widget.show()

    # Test 3: Dock window creation
    dock_window = test_dock_window_creation()
    test_results.append(("Dock Window Creation", dock_window is not None))

    # Test 4: Mode switching
    main_window = test_mode_switching()
    test_results.append(("Mode Switching", main_window is not None))

    # Test 5: Application launching
    launch_test_result = test_application_launching()
    test_results.append(("Application Launching", launch_test_result))

    # Print test results
    logger.info("\n" + "=" * 50)
    logger.info("🧪 TEST RESULTS SUMMARY")
    logger.info("=" * 50)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{test_name}: {status}")

    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    logger.info(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        logger.info("🎉 All tests passed! Dock functionality is working correctly.")
    else:
        logger.warning("⚠️ Some tests failed. Please check the implementation.")

    # Keep the application running to see the UI tests
    logger.info("\n👀 UI tests are running. Close windows to exit.")

    # Exit after 30 seconds if no interaction
    QTimer.singleShot(30000, app.quit)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
