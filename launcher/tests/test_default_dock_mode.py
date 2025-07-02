#!/usr/bin/env python3
"""
Test that the launcher starts in dock mode by default.
"""

import sys
import tempfile
import os
from pathlib import Path

# Add the launcher directory to the path
sys.path.insert(0, str(Path(__file__).parent / "launcher"))


def test_default_dock_mode():
    """Test that launcher starts in dock mode by default without any saved settings."""

    # Use a temporary directory for settings to ensure clean state
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up environment to use temp directory for settings
        os.environ["TKA_SETTINGS_DIR"] = temp_dir

        try:
            from config.settings import SettingsManager, LauncherSettings

            # Create a fresh settings manager (no existing config file)
            settings_path = Path(temp_dir) / "launcher_settings.json"
            settings_manager = SettingsManager(settings_path)

            # Check default values
            print(f"Default launch_mode: {settings_manager.get('launch_mode')}")
            print(
                f"Default auto_start_docked: {settings_manager.get('auto_start_docked')}"
            )
            print(
                f"Should restore to docked: {settings_manager.should_restore_to_docked()}"
            )

            # Verify defaults
            assert (
                settings_manager.get("launch_mode") == "docked"
            ), f"Expected 'docked', got '{settings_manager.get('launch_mode')}'"
            assert (
                settings_manager.get("auto_start_docked") == True
            ), f"Expected True, got {settings_manager.get('auto_start_docked')}"
            assert (
                settings_manager.should_restore_to_docked() == True
            ), "Should restore to docked by default"

            print("✅ Default dock mode test passed!")

        except Exception as e:
            print(f"❌ Test failed: {e}")
            raise
        finally:
            # Clean up environment
            if "TKA_SETTINGS_DIR" in os.environ:
                del os.environ["TKA_SETTINGS_DIR"]


def test_launcher_config_defaults():
    """Test that launcher config also defaults to docked mode."""
    try:
        from config.config.launcher_config import WindowConfig, LauncherConfiguration

        # Test WindowConfig defaults
        window_config = WindowConfig()
        print(f"WindowConfig default mode: {window_config.mode}")
        assert (
            window_config.mode == "docked"
        ), f"Expected 'docked', got '{window_config.mode}'"

        # Test LauncherConfiguration defaults
        launcher_config = LauncherConfiguration()
        print(f"LauncherConfiguration window mode: {launcher_config.window.mode}")
        assert (
            launcher_config.window.mode == "docked"
        ), f"Expected 'docked', got '{launcher_config.window.mode}'"

        print("✅ Launcher config defaults test passed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    print("🧪 Testing default dock mode configuration...")
    test_default_dock_mode()
    test_launcher_config_defaults()
    print("🎉 All default dock mode tests passed!")
