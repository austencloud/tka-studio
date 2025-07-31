"""
Settings Service Implementation.

Handles persistent configuration, user preferences, and settings validation
with proper defaults following TKA patterns.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from desktop.modern.core.interfaces import ISettingsService

logger = logging.getLogger(__name__)


class SettingsService(ISettingsService):
    """
    Service for managing launcher settings with persistence.

    Follows TKA's clean architecture principles with immutable data patterns
    and proper error handling.
    """

    def __init__(self, settings_file: Optional[Path] = None):
        """Initialize the settings service."""
        if settings_file:
            self._settings_file = settings_file
        else:
            # Try to find the settings file relative to the current directory
            # This handles both cases: running from TKA root and from launcher directory
            config_path = Path.cwd() / "config" / "settings.json"
            if config_path.exists():
                self._settings_file = config_path
            else:
                # Fallback to the original path
                self._settings_file = (
                    Path.cwd() / "launcher" / "config" / "settings.json"
                )
        self._settings: Dict[str, Any] = {}
        self._defaults = self._create_default_settings()

        # Ensure settings directory exists
        self._settings_file.parent.mkdir(parents=True, exist_ok=True)

        # Load existing settings
        self._load_settings()

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        value = self._settings.get(key, default)
        if value is None:
            value = self._defaults.get(key, default)
        return value

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        old_value = self._settings.get(key)
        self._settings[key] = value

        # Auto-save on change
        self._save_settings()

        if old_value != value:
            logger.debug(f"Setting changed: {key} = {value}")

    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings as a dictionary."""
        # Merge defaults with current settings
        all_settings = self._defaults.copy()
        all_settings.update(self._settings)
        return all_settings

    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        self._settings = self._defaults.copy()
        self._save_settings()
        logger.info("Settings reset to defaults")

    def export_settings(self, file_path: Path) -> bool:
        """Export settings to a file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.get_all_settings(), f, indent=2, ensure_ascii=False)
            logger.info(f"Settings exported to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export settings: {e}")
            return False

    def import_settings(self, file_path: Path) -> bool:
        """Import settings from a file."""
        try:
            if not file_path.exists():
                logger.error(f"Settings file not found: {file_path}")
                return False

            with open(file_path, encoding="utf-8") as f:
                imported_settings = json.load(f)

            # Validate imported settings
            validation_errors = self._validate_settings_dict(imported_settings)
            if validation_errors:
                logger.error(f"Invalid settings in import file: {validation_errors}")
                return False

            # Update settings
            self._settings.update(imported_settings)
            self._save_settings()

            logger.info(f"Settings imported from {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to import settings: {e}")
            return False

    def validate_settings(self) -> List[str]:
        """Validate current settings and return any errors."""
        return self._validate_settings_dict(self._settings)

    def _load_settings(self) -> None:
        """Load settings from file."""
        try:
            if self._settings_file.exists():
                with open(self._settings_file, encoding="utf-8") as f:
                    self._settings = json.load(f)

                # Validate loaded settings
                validation_errors = self.validate_settings()
                if validation_errors:
                    logger.warning(f"Invalid settings detected: {validation_errors}")
                    # Keep valid settings, reset invalid ones to defaults
                    self._fix_invalid_settings()

                logger.info(f"Settings loaded from {self._settings_file}")
            else:
                logger.info("No settings file found, using defaults")

        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            self._settings = {}

    def _save_settings(self) -> None:
        """Save settings to file."""
        try:
            with open(self._settings_file, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
            logger.debug(f"Settings saved to {self._settings_file}")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def _create_default_settings(self) -> Dict[str, Any]:
        """Create default settings."""
        return {
            # UI Settings
            "launch_mode": "docked",  # Default to docked mode
            "window_width": 1000,
            "window_height": 700,
            "dock_width": 110,
            "target_screen_index": 0,
            # Behavior Settings
            "auto_hide_dock": True,
            "dock_auto_hide_delay": 1000,  # milliseconds
            "animation_duration": 300,
            "enable_animations": True,
            "show_tooltips": True,
            # Application Settings
            "auto_launch_favorites": False,
            "remember_window_position": True,
            "minimize_to_tray": False,
            "start_with_system": False,
            # Visual Settings
            "theme": "dark",
            "glassmorphism_intensity": 0.8,
            "blur_radius": 15,
            "accent_color": "#6366f1",
            "font_size": 16,
            # Advanced Settings
            "debug_mode": False,
            "log_level": "INFO",
            "max_recent_apps": 10,
            "search_delay": 200,  # milliseconds
            # State Persistence
            "first_run": True,
            "total_launches": 0,
            "last_version": "2.0.0",
        }

    def _validate_settings_dict(self, settings: Dict[str, Any]) -> List[str]:
        """Validate a settings dictionary and return errors."""
        errors = []

        # Validate launch_mode
        if "launch_mode" in settings:
            if settings["launch_mode"] not in ["window", "docked"]:
                errors.append("launch_mode must be 'window' or 'docked'")

        # Validate numeric settings
        numeric_settings = {
            "window_width": (400, 3840),
            "window_height": (300, 2160),
            "dock_width": (50, 300),
            "target_screen_index": (0, 10),
            "dock_auto_hide_delay": (0, 10000),
            "animation_duration": (50, 2000),
            "font_size": (8, 32),
            "max_recent_apps": (1, 50),
            "search_delay": (0, 1000),
        }

        for setting, (min_val, max_val) in numeric_settings.items():
            if setting in settings:
                value = settings[setting]
                if not isinstance(value, (int, float)) or not (
                    min_val <= value <= max_val
                ):
                    errors.append(
                        f"{setting} must be a number between {min_val} and {max_val}"
                    )

        # Validate boolean settings
        boolean_settings = [
            "auto_hide_dock",
            "enable_animations",
            "show_tooltips",
            "auto_launch_favorites",
            "remember_window_position",
            "minimize_to_tray",
            "start_with_system",
            "debug_mode",
            "first_run",
        ]

        for setting in boolean_settings:
            if setting in settings and not isinstance(settings[setting], bool):
                errors.append(f"{setting} must be a boolean value")

        # Validate theme
        if "theme" in settings:
            if settings["theme"] not in ["light", "dark", "auto"]:
                errors.append("theme must be 'light', 'dark', or 'auto'")

        # Validate log_level
        if "log_level" in settings:
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if settings["log_level"] not in valid_levels:
                errors.append(f"log_level must be one of {valid_levels}")

        return errors

    def _fix_invalid_settings(self) -> None:
        """Fix invalid settings by resetting them to defaults."""
        validation_errors = self.validate_settings()
        if not validation_errors:
            return

        # Reset invalid settings to defaults
        for key, value in self._settings.items():
            temp_dict = {key: value}
            if self._validate_settings_dict(temp_dict):
                # This setting is invalid, reset to default
                if key in self._defaults:
                    self._settings[key] = self._defaults[key]
                    logger.warning(
                        f"Reset invalid setting {key} to default: {self._defaults[key]}"
                    )
                else:
                    # Remove unknown setting
                    del self._settings[key]
                    logger.warning(f"Removed unknown setting: {key}")

        # Save corrected settings
        self._save_settings()
