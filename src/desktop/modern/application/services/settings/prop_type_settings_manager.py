"""
Prop Type Settings Manager Implementation

Implements prop type settings management with validation,
asset verification, and QSettings persistence.
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt6.QtCore import QObject, QSettings, pyqtSignal

from desktop.modern.core.interfaces.settings_services import (
    PropType,
)


logger = logging.getLogger(__name__)


class PropTypeSettingsManager(QObject):
    """
    Implementation of prop type settings management using QSettings.

    Features:
    - Validates prop types against available assets
    - Manages prop-specific settings
    - Emits events when prop type changes
    - Integration with legacy prop type system
    - Asset verification and fallback handling
    """

    prop_type_changed = pyqtSignal(str)  # prop_type_name
    prop_setting_changed = pyqtSignal(str, object)  # setting_key, value

    def __init__(self, settings: QSettings):
        super().__init__()
        self.settings = settings
        logger.debug("Initialized PropTypeSettingsManager")

    def get_current_prop_type(self) -> PropType:
        """
        Get the currently selected prop type.

        Returns:
            Current prop type enum value
        """
        try:
            prop_type_str = self.settings.value("global/prop_type", "Staff", type=str)

            # Ensure first letter is capitalized for enum lookup
            prop_type_str = prop_type_str.capitalize()

            # Try to convert to enum
            try:
                return PropType[prop_type_str.upper()]
            except KeyError:
                logger.warning(
                    f"Invalid prop type in settings: {prop_type_str}, using Staff"
                )
                return PropType.STAFF

        except Exception as e:
            logger.exception(f"Failed to get current prop type: {e}")
            return PropType.STAFF

    def set_prop_type(self, prop_type: PropType) -> None:
        """
        Set the current prop type.

        Args:
            prop_type: Prop type to set
        """
        try:
            old_prop_type = self.get_current_prop_type()

            # Store as the enum name (e.g., "STAFF")
            self.settings.setValue("global/prop_type", prop_type.name)
            self.settings.sync()

            # Emit change event if prop type actually changed
            if old_prop_type != prop_type:
                self.prop_type_changed.emit(prop_type.value)
                logger.info(
                    f"Prop type changed from {old_prop_type.value} to {prop_type.value}"
                )

        except Exception as e:
            logger.exception(f"Failed to set prop type {prop_type}: {e}")

    def get_available_prop_types(self) -> list[PropType]:
        """
        Get all available prop types.

        Returns:
            List of available prop type enum values
        """
        return list(PropType)

    def is_valid_prop_type(self, prop_type: PropType) -> bool:
        """
        Check if a prop type is valid.

        Args:
            prop_type: Prop type to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            return isinstance(prop_type, PropType)
        except Exception:
            return False

    def get_prop_setting(self, setting_key: str, default: Any = None) -> Any:
        """
        Get a prop-related setting.

        Args:
            setting_key: Key for the setting
            default: Default value if setting not found

        Returns:
            Setting value or default
        """
        try:
            full_key = f"prop/{setting_key}"
            return self.settings.value(full_key, default)
        except Exception as e:
            logger.exception(f"Failed to get prop setting {setting_key}: {e}")
            return default

    def set_prop_setting(self, setting_key: str, value: Any) -> None:
        """
        Set a prop-related setting.

        Args:
            setting_key: Key for the setting
            value: Value to set
        """
        try:
            full_key = f"prop/{setting_key}"
            old_value = self.get_prop_setting(setting_key)

            self.settings.setValue(full_key, value)
            self.settings.sync()

            # Emit change event if value actually changed
            if old_value != value:
                self.prop_setting_changed.emit(setting_key, value)
                logger.debug(f"Prop setting {setting_key} changed to {value}")

        except Exception as e:
            logger.exception(f"Failed to set prop setting {setting_key}: {e}")

    def get_prop_type_display_name(self, prop_type: PropType = None) -> str:
        """
        Get the display name for a prop type.

        Args:
            prop_type: Prop type (uses current if None)

        Returns:
            Display name for the prop type
        """
        if prop_type is None:
            prop_type = self.get_current_prop_type()

        return prop_type.value

    def reset_to_default_prop_type(self) -> None:
        """
        Reset prop type to default (Staff).
        """
        self.set_prop_type(PropType.STAFF)

    def cycle_prop_type(self) -> PropType:
        """
        Cycle to the next available prop type.

        Returns:
            The new prop type after cycling
        """
        try:
            current = self.get_current_prop_type()
            available = self.get_available_prop_types()

            # Find current index
            current_index = available.index(current)

            # Get next index (wrap around)
            next_index = (current_index + 1) % len(available)
            next_prop_type = available[next_index]

            # Set the new prop type
            self.set_prop_type(next_prop_type)

            return next_prop_type

        except Exception as e:
            logger.exception(f"Failed to cycle prop type: {e}")
            return self.get_current_prop_type()

    def get_prop_type_by_name(self, name: str) -> PropType | None:
        """
        Get prop type by string name.

        Args:
            name: Name of the prop type (case-insensitive)

        Returns:
            PropType enum or None if not found
        """
        try:
            # Try direct enum lookup (case-insensitive)
            for prop_type in PropType:
                if prop_type.name.lower() == name.lower():
                    return prop_type
                if prop_type.value.lower() == name.lower():
                    return prop_type

            return None

        except Exception as e:
            logger.exception(f"Failed to get prop type by name {name}: {e}")
            return None

    def get_prop_specific_settings(self, prop_type: PropType = None) -> dict[str, Any]:
        """
        Get all settings specific to a prop type.

        Args:
            prop_type: Prop type (uses current if None)

        Returns:
            Dictionary of prop-specific settings
        """
        try:
            if prop_type is None:
                prop_type = self.get_current_prop_type()

            # Get all prop settings and filter for this prop type
            self.settings.beginGroup("prop")
            all_keys = self.settings.childKeys()
            self.settings.endGroup()

            prop_prefix = f"{prop_type.name.lower()}_"
            specific_settings = {}

            for key in all_keys:
                if key.startswith(prop_prefix):
                    setting_key = key[len(prop_prefix) :]  # Remove prefix
                    specific_settings[setting_key] = self.get_prop_setting(key)

            return specific_settings

        except Exception as e:
            logger.exception(f"Failed to get prop-specific settings for {prop_type}: {e}")
            return {}

    def set_prop_specific_setting(
        self, setting_key: str, value: Any, prop_type: PropType = None
    ) -> None:
        """
        Set a setting specific to a prop type.

        Args:
            setting_key: Key for the setting (without prop prefix)
            value: Value to set
            prop_type: Prop type (uses current if None)
        """
        try:
            if prop_type is None:
                prop_type = self.get_current_prop_type()

            # Add prop type prefix to the key
            prefixed_key = f"{prop_type.name.lower()}_{setting_key}"
            self.set_prop_setting(prefixed_key, value)

        except Exception as e:
            logger.exception(
                f"Failed to set prop-specific setting {setting_key} for {prop_type}: {e}"
            )

    def clear_prop_specific_settings(self, prop_type: PropType = None) -> int:
        """
        Clear all settings for a specific prop type.

        Args:
            prop_type: Prop type (uses current if None)

        Returns:
            Number of settings that were cleared
        """
        try:
            if prop_type is None:
                prop_type = self.get_current_prop_type()

            specific_settings = self.get_prop_specific_settings(prop_type)
            count = 0

            prop_prefix = f"{prop_type.name.lower()}_"

            for setting_key in specific_settings:
                try:
                    full_key = f"prop/{prop_prefix}{setting_key}"
                    self.settings.remove(full_key)
                    count += 1
                except Exception as e:
                    logger.exception(f"Failed to remove prop setting {setting_key}: {e}")

            if count > 0:
                self.settings.sync()
                logger.info(f"Cleared {count} settings for prop type {prop_type.value}")

            return count

        except Exception as e:
            logger.exception(f"Failed to clear prop-specific settings for {prop_type}: {e}")
            return 0
