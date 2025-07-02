#!/usr/bin/env python3
"""
Test script to verify that the launcher starts in docked mode when configured to do so.
"""

import sys
import os
import time
import logging
from pathlib import Path

# Add the launcher directory to the path so we can import from it
launcher_dir = Path(__file__).parent / "launcher"
sys.path.insert(0, str(launcher_dir))

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_dock_startup():
    """Test that the launcher starts in dock mode when configured."""

    logger.info("🧪 Starting dock startup test...")

    try:
        # Step 1: Set the launch mode to docked in settings
        from config.settings import SettingsManager

        settings_manager = SettingsManager()
        logger.info("📋 Setting launch mode to 'docked'...")
        settings_manager.set("launch_mode", "docked")

        # Verify the setting was saved
        if settings_manager.should_restore_to_docked():
            logger.info("✅ Settings configured for docked mode")
        else:
            logger.error("❌ Failed to set docked mode in settings")
            return False

        # Step 2: Import and create the launcher (but don't run the event loop)
        from main import TKAModernLauncherApp

        logger.info("🚀 Creating launcher app...")
        launcher = TKAModernLauncherApp(sys.argv)

        # Step 3: Initialize the launcher
        logger.info("⚙️ Initializing launcher...")
        if not launcher.initialize():
            logger.error("❌ Launcher initialization failed")
            return False

        # Step 4: Setup initial mode (this should trigger dock mode)
        logger.info("🔄 Setting up initial mode...")
        launcher._setup_initial_mode()

        # Step 5: Check if the launcher is in dock mode
        current_mode = launcher.main_window.mode_manager.current_mode
        logger.info(f"📊 Current mode: {current_mode}")

        if current_mode == "docked":
            logger.info("✅ SUCCESS: Launcher started in docked mode!")

            # Check if dock window exists and is visible
            if (
                launcher.main_window.mode_manager.dock_window
                and launcher.main_window.mode_manager.dock_window.isVisible()
            ):
                logger.info("✅ SUCCESS: Dock window is visible!")
            else:
                logger.warning("⚠️ Dock window not visible")

            # Check if main window is hidden
            if not launcher.main_window.isVisible():
                logger.info("✅ SUCCESS: Main window is hidden!")
            else:
                logger.warning("⚠️ Main window is still visible")

            return True
        else:
            logger.error(
                f"❌ FAILURE: Launcher started in {current_mode} mode instead of docked"
            )
            return False

    except Exception as e:
        logger.error(f"💥 Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        # Clean up - reset settings to window mode
        try:
            settings_manager.set("launch_mode", "window")
            logger.info("🧹 Reset launch mode to window")
        except Exception:
            pass


def test_window_startup():
    """Test that the launcher starts in window mode when configured."""

    logger.info("🧪 Starting window startup test...")

    try:
        # Step 1: Set the launch mode to window in settings
        from config.settings import SettingsManager

        settings_manager = SettingsManager()
        logger.info("📋 Setting launch mode to 'window'...")
        settings_manager.set("launch_mode", "window")

        # Step 2: Import and create the launcher
        from main import TKAModernLauncherApp

        logger.info("🚀 Creating launcher app...")
        launcher = TKAModernLauncherApp(sys.argv)

        # Step 3: Initialize and setup
        logger.info("⚙️ Initializing launcher...")
        if not launcher.initialize():
            logger.error("❌ Launcher initialization failed")
            return False

        logger.info("🔄 Setting up initial mode...")
        launcher._setup_initial_mode()

        # Step 4: Check if the launcher is in window mode
        current_mode = launcher.main_window.mode_manager.current_mode
        logger.info(f"📊 Current mode: {current_mode}")

        if current_mode == "window":
            logger.info("✅ SUCCESS: Launcher started in window mode!")

            # Check if main window is visible
            if launcher.main_window.isVisible():
                logger.info("✅ SUCCESS: Main window is visible!")
            else:
                logger.warning("⚠️ Main window not visible")

            return True
        else:
            logger.error(
                f"❌ FAILURE: Launcher started in {current_mode} mode instead of window"
            )
            return False

    except Exception as e:
        logger.error(f"💥 Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    logger.info("🧪 Starting launcher startup mode tests...")

    # Test 1: Window mode startup
    separator = "=" * 60
    logger.info("\n%s", separator)
    logger.info("TEST 1: Window Mode Startup")
    logger.info(separator)
    window_test_passed = test_window_startup()

    # Test 2: Dock mode startup
    logger.info("\n%s", separator)
    logger.info("TEST 2: Dock Mode Startup")
    logger.info(separator)
    dock_test_passed = test_dock_startup()

    # Summary
    logger.info("\n%s", separator)
    logger.info("TEST RESULTS SUMMARY")
    logger.info(separator)
    logger.info(
        f"Window mode test: {'✅ PASSED' if window_test_passed else '❌ FAILED'}"
    )
    logger.info(f"Dock mode test: {'✅ PASSED' if dock_test_passed else '❌ FAILED'}")

    if window_test_passed and dock_test_passed:
        logger.info(
            "🎉 ALL TESTS PASSED! Launcher startup mode detection is working correctly."
        )
        sys.exit(0)
    else:
        logger.error("💥 SOME TESTS FAILED! Check the logs above for details.")
        sys.exit(1)
