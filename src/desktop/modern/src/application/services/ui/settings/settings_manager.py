"""
Settings Manager - Core Settings Management

Handles core settings operations including get, set, save, load, import, export.
Extracted from UIStateManager to follow single responsibility principle.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from core.events.event_bus import UIEvent, get_event_bus

logger = logging.getLogger(__name__)


class SettingsManager:
    """
    Core settings management service.

    Handles:
    - Getting and setting individual settings
    - Loading and saving settings to file
    - Default settings management
    - Settings import/export
    """

    def __init__(self, settings_file_path: Optional[Path] = None):
        """Initialize settings service."""
        # Settings file path - use modern directory if not provided
        if settings_file_path is None:
            modern_dir = Path(__file__).parent.parent.parent.parent.parent.parent
            self._settings_file = modern_dir / "user_settings.json"
        else:
            self._settings_file = settings_file_path

        # Event bus for notifications
        self._event_bus = get_event_bus()

        # Settings storage
        self._user_settings: Dict[str, Any] = {}
        self._default_settings = self._load_default_settings()

        # Load saved settings
        self._load_settings()

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self._user_settings.get(key, self._default_settings.get(key, default))

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        self._user_settings[key] = value
        self._save_settings()

        # Publish setting change event
        event = UIEvent(
            component="settings",
            action="updated",
            state_data={"key": key, "value": value},
            source="settings_service",
        )
        self._event_bus.publish(event)

    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings."""
        # Merge defaults with user settings, user settings take precedence
        all_settings = self._default_settings.copy()
        all_settings.update(self._user_settings)
        return all_settings

    def clear_settings(self) -> None:
        """Clear all user settings (revert to defaults)."""
        self._user_settings.clear()
        self._save_settings()

        # Publish settings cleared event
        event = UIEvent(
            component="settings",
            action="cleared",
            state_data={},
            source="settings_service",
        )
        self._event_bus.publish(event)

    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        self.clear_settings()

    def export_settings(self, file_path: Path) -> bool:
        """Export settings to file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.get_all_settings(), f, indent=2)
            logger.info(f"Settings exported to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export settings: {e}")
            return False

    def import_settings(self, file_path: Path) -> bool:
        """Import settings from file."""
        try:
            if not file_path.exists():
                logger.warning(f"Settings file not found: {file_path}")
                return False

            with open(file_path, "r", encoding="utf-8") as f:
                imported_settings = json.load(f)

            # Validate imported settings
            if not isinstance(imported_settings, dict):
                logger.error("Invalid settings format")
                return False

            # Update user settings
            self._user_settings.update(imported_settings)
            self._save_settings()

            # Publish settings imported event
            event = UIEvent(
                component="settings",
                action="imported",
                state_data={"file_path": str(file_path)},
                source="settings_service",
            )
            self._event_bus.publish(event)

            logger.info(f"Settings imported from {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to import settings: {e}")
            return False

    def _load_settings(self) -> None:
        """Load settings from file."""
        try:
            if self._settings_file.exists():
                with open(self._settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Extract user_settings if it exists, otherwise use the whole data
                    if isinstance(data, dict) and "user_settings" in data:
                        self._user_settings = data["user_settings"]
                    elif isinstance(data, dict):
                        self._user_settings = data
                    else:
                        logger.warning("Invalid settings file format")
                        self._user_settings = {}
            else:
                logger.info("No settings file found, using defaults")
                self._user_settings = {}
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            self._user_settings = {}

    def _save_settings(self) -> None:
        """Save settings to file."""
        try:
            # Ensure directory exists
            self._settings_file.parent.mkdir(parents=True, exist_ok=True)

            # Save just the user settings
            with open(self._settings_file, "w", encoding="utf-8") as f:
                json.dump(self._user_settings, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def _load_default_settings(self) -> Dict[str, Any]:
        """Load default settings."""
        return {
            "background_type": "Aurora",
            "beat_layout": "horizontal",
            "prop_type": "staff",
            "visibility": {
                "grid": True,
                "props": True,
                "arrows": True,
                "tka": True,
                "vtg": True,
                "elemental": True,
                "positions": True,
                "reversals": True,
                "non_radial": True,
            },
            "image_export": {
                "format": "png",
                "quality": 95,
                "include_metadata": True,
            },
            "user_profile": {
                "name": "",
                "level": "beginner",
            },
        }
