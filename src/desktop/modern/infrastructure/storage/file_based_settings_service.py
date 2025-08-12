"""
File-based Settings Service for TKA

Provides persistent settings storage using JSON files.
"""

from __future__ import annotations

from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Any

from desktop.modern.core.interfaces.core_services import ISettingsCoordinator


logger = logging.getLogger(__name__)


class FileBasedSettingsService(ISettingsCoordinator):
    """
    File-based implementation of ISettingsService.

    Stores settings as JSON files in a data directory.
    Suitable for production and headless modes.
    """

    def __init__(self, data_dir: str = "data/settings"):
        """
        Initialize with data directory.

        Args:
            data_dir: Directory to store settings files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.settings_file = self.data_dir / "settings.json"
        self.settings: dict[str, Any] = self._load_initial_settings()
        logger.info(
            f"FileBasedSettingsService initialized with data_dir: {self.data_dir}"
        )

    def _load_initial_settings(self) -> dict[str, Any]:
        """Load initial settings from file or create defaults."""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, encoding="utf-8") as f:
                    settings = json.load(f)
                logger.debug(f"Loaded settings from {self.settings_file}")
                return settings
            except (OSError, json.JSONDecodeError) as e:
                logger.warning(f"Failed to load settings file: {e}, using defaults")

        # Return default settings
        default_settings = {
            "window_width": 1920,
            "window_height": 1080,
            "layout_ratio": [3, 1],
            "theme": "default",
            "auto_save": True,
            "last_sequence": None,
            "recent_files": [],
            "created_at": datetime.now().isoformat(),
        }

        # Save defaults immediately
        self._save_to_file(default_settings)
        return default_settings

    def _save_to_file(self, settings: dict[str, Any]) -> bool:
        """Save settings to file."""
        try:
            # Add timestamp
            settings["last_modified"] = datetime.now().isoformat()

            # Write to temporary file first, then rename for atomic operation
            temp_path = self.settings_file.with_suffix(".tmp")
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)

            # Atomic rename
            temp_path.replace(self.settings_file)

            logger.debug(f"Saved settings to {self.settings_file}")
            return True

        except Exception as e:
            logger.exception(f"Failed to save settings: {e}")
            return False

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        value = self.settings.get(key, default)
        logger.debug(f"Got setting {key}: {value}")
        return value

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        self.settings[key] = value
        logger.debug(f"Set setting {key}: {value}")

    def save_settings(self) -> None:
        """Save settings to persistent storage."""
        success = self._save_to_file(self.settings)
        if success:
            logger.info("Settings saved successfully")
        else:
            logger.error("Failed to save settings")

    def load_settings(self) -> None:
        """Load settings from persistent storage."""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, encoding="utf-8") as f:
                    loaded_settings = json.load(f)

                # Update current settings with loaded values
                self.settings.update(loaded_settings)
                logger.info(f"Settings loaded successfully from {self.settings_file}")

            except (OSError, json.JSONDecodeError) as e:
                logger.exception(f"Failed to load settings: {e}")
        else:
            logger.warning(f"Settings file not found: {self.settings_file}")

    def get_all_settings(self) -> dict[str, Any]:
        """Get all settings as a dictionary."""
        return self.settings.copy()

    def clear_settings(self) -> None:
        """Clear all settings (keep only essential ones)."""
        essential_keys = ["created_at"]
        essential_settings = {
            key: self.settings.get(key)
            for key in essential_keys
            if key in self.settings
        }

        self.settings = essential_settings
        logger.info("Settings cleared (essential settings preserved)")

    def reset_to_defaults(self) -> None:
        """Reset settings to default values."""
        self.settings = {
            "window_width": 1920,
            "window_height": 1080,
            "layout_ratio": [3, 1],
            "theme": "default",
            "auto_save": True,
            "last_sequence": None,
            "recent_files": [],
            "created_at": self.settings.get("created_at", datetime.now().isoformat()),
            "reset_at": datetime.now().isoformat(),
        }
        self.save_settings()
        logger.info("Settings reset to defaults")
