"""
User Profile Settings Manager Implementation

Implements user profile management with multi-user support,
profile-specific settings, and QSettings persistence.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from PyQt6.QtCore import QObject, QSettings, pyqtSignal


logger = logging.getLogger(__name__)


class UserProfileSettingsManager(QObject):
    """
    Implementation of user profile settings management using QSettings.

    Features:
    - Multi-user profile support
    - Profile-specific settings isolation
    - User validation and management
    - Profile switching with data preservation
    - Default user creation and management
    """

    user_changed = pyqtSignal(str)  # username
    user_added = pyqtSignal(str)  # username
    user_removed = pyqtSignal(str)  # username
    user_setting_changed = pyqtSignal(str, str, object)  # username, setting_key, value

    # Default user name
    DEFAULT_USER = "DefaultUser"

    # Settings that should not be user-specific (shared across all users)
    GLOBAL_SETTINGS = {
        "application/version",
        "application/first_run",
        "global/window_geometry",
        "global/window_state",
    }

    def __init__(self, settings: QSettings):
        super().__init__()
        self.settings = settings

        # Ensure default user exists
        self._ensure_default_user()

        logger.debug("Initialized UserProfileSettingsManager")

    def get_current_user(self) -> str:
        """
        Get the current active user.

        Returns:
            Current user name
        """
        try:
            return self.settings.value(
                "users/current_user", self.DEFAULT_USER, type=str
            )
        except Exception as e:
            logger.error(f"Failed to get current user: {e}")
            return self.DEFAULT_USER

    def set_current_user(self, username: str) -> None:
        """
        Set the current active user.

        Args:
            username: User name to set as current
        """
        try:
            if not self._is_valid_username(username):
                logger.warning(f"Invalid username: {username}")
                return

            # Ensure user exists
            if username not in self.get_all_users():
                self.add_user(username)

            old_user = self.get_current_user()

            self.settings.setValue("users/current_user", username)
            self.settings.sync()

            # Emit change event if user actually changed
            if old_user != username:
                self.user_changed.emit(username)
                logger.info(f"Current user changed from {old_user} to {username}")

        except Exception as e:
            logger.error(f"Failed to set current user {username}: {e}")

    def get_all_users(self) -> list[str]:
        """
        Get all available user profiles.

        Returns:
            List of user names
        """
        try:
            users_json = self.settings.value("users/user_list", "[]", type=str)
            users = json.loads(users_json)

            # Ensure default user is in the list
            if self.DEFAULT_USER not in users:
                users.append(self.DEFAULT_USER)
                self._save_user_list(users)

            return sorted(users)

        except Exception as e:
            logger.error(f"Failed to get all users: {e}")
            return [self.DEFAULT_USER]

    def add_user(self, username: str) -> bool:
        """
        Add a new user profile.

        Args:
            username: User name to add

        Returns:
            True if successful, False if username invalid or already exists
        """
        try:
            if not self._is_valid_username(username):
                logger.warning(f"Invalid username: {username}")
                return False

            users = self.get_all_users()

            if username in users:
                logger.info(f"User {username} already exists")
                return True

            # Add user to list
            users.append(username)
            self._save_user_list(users)

            # Initialize user with default settings
            self._initialize_user_settings(username)

            self.user_added.emit(username)
            logger.info(f"Added new user: {username}")
            return True

        except Exception as e:
            logger.error(f"Failed to add user {username}: {e}")
            return False

    def remove_user(self, username: str) -> bool:
        """
        Remove a user profile.

        Args:
            username: User name to remove

        Returns:
            True if successful, False if user not found or is last user
        """
        try:
            if username == self.DEFAULT_USER:
                logger.warning("Cannot remove default user")
                return False

            users = self.get_all_users()

            if username not in users:
                logger.warning(f"User {username} not found")
                return False

            if len(users) <= 1:
                logger.warning("Cannot remove last user")
                return False

            # Remove user from list
            users.remove(username)
            self._save_user_list(users)

            # Clear user-specific settings
            self._clear_user_settings(username)

            # If removing current user, switch to default
            if self.get_current_user() == username:
                self.set_current_user(self.DEFAULT_USER)

            self.user_removed.emit(username)
            logger.info(f"Removed user: {username}")
            return True

        except Exception as e:
            logger.error(f"Failed to remove user {username}: {e}")
            return False

    def get_user_setting(
        self, username: str, setting_key: str, default: Any = None
    ) -> Any:
        """
        Get a setting for a specific user.

        Args:
            username: User name
            setting_key: Key for the setting
            default: Default value if setting not found

        Returns:
            Setting value or default
        """
        try:
            if not self._user_exists(username):
                logger.warning(f"User {username} does not exist")
                return default

            full_key = f"user_{username}/{setting_key}"
            return self.settings.value(full_key, default)

        except Exception as e:
            logger.error(
                f"Failed to get user setting {setting_key} for {username}: {e}"
            )
            return default

    def set_user_setting(self, username: str, setting_key: str, value: Any) -> None:
        """
        Set a setting for a specific user.

        Args:
            username: User name
            setting_key: Key for the setting
            value: Value to set
        """
        try:
            if not self._user_exists(username):
                logger.warning(f"User {username} does not exist")
                return

            # Check if this is a global setting that shouldn't be user-specific
            if self._is_global_setting(setting_key):
                logger.warning(
                    f"Setting {setting_key} is global and should not be user-specific"
                )
                return

            old_value = self.get_user_setting(username, setting_key)
            full_key = f"user_{username}/{setting_key}"

            self.settings.setValue(full_key, value)
            self.settings.sync()

            # Emit change event if value actually changed
            if old_value != value:
                self.user_setting_changed.emit(username, setting_key, value)
                logger.debug(
                    f"User setting {setting_key} for {username} changed to {value}"
                )

        except Exception as e:
            logger.error(
                f"Failed to set user setting {setting_key} for {username}: {e}"
            )

    def get_current_user_setting(self, setting_key: str, default: Any = None) -> Any:
        """
        Get a setting for the current user.

        Args:
            setting_key: Key for the setting
            default: Default value if setting not found

        Returns:
            Setting value or default
        """
        current_user = self.get_current_user()
        return self.get_user_setting(current_user, setting_key, default)

    def set_current_user_setting(self, setting_key: str, value: Any) -> None:
        """
        Set a setting for the current user.

        Args:
            setting_key: Key for the setting
            value: Value to set
        """
        current_user = self.get_current_user()
        self.set_user_setting(current_user, setting_key, value)

    def get_all_user_settings(self, username: str) -> dict[str, Any]:
        """
        Get all settings for a specific user.

        Args:
            username: User name

        Returns:
            Dictionary of all user settings
        """
        try:
            if not self._user_exists(username):
                return {}

            user_settings = {}

            # Get all keys for this user
            self.settings.beginGroup(f"user_{username}")
            keys = self.settings.childKeys()

            for key in keys:
                user_settings[key] = self.settings.value(key)

            self.settings.endGroup()

            return user_settings

        except Exception as e:
            logger.error(f"Failed to get all user settings for {username}: {e}")
            return {}

    def copy_user_settings(self, from_user: str, to_user: str) -> bool:
        """
        Copy settings from one user to another.

        Args:
            from_user: Source user name
            to_user: Target user name

        Returns:
            True if successful
        """
        try:
            if not self._user_exists(from_user):
                logger.warning(f"Source user {from_user} does not exist")
                return False

            if not self._user_exists(to_user):
                self.add_user(to_user)

            # Get all settings from source user
            source_settings = self.get_all_user_settings(from_user)

            # Copy to target user
            for setting_key, value in source_settings.items():
                self.set_user_setting(to_user, setting_key, value)

            logger.info(
                f"Copied {len(source_settings)} settings from {from_user} to {to_user}"
            )
            return True

        except Exception as e:
            logger.error(
                f"Failed to copy user settings from {from_user} to {to_user}: {e}"
            )
            return False

    def reset_user_settings(self, username: str) -> bool:
        """
        Reset all settings for a user to defaults.

        Args:
            username: User name

        Returns:
            True if successful
        """
        try:
            if not self._user_exists(username):
                logger.warning(f"User {username} does not exist")
                return False

            # Clear all user settings
            self._clear_user_settings(username)

            # Reinitialize with defaults
            self._initialize_user_settings(username)

            logger.info(f"Reset settings for user {username}")
            return True

        except Exception as e:
            logger.error(f"Failed to reset settings for user {username}: {e}")
            return False

    def _ensure_default_user(self) -> None:
        """Ensure the default user exists."""
        try:
            users = self.get_all_users()
            if self.DEFAULT_USER not in users:
                self.add_user(self.DEFAULT_USER)

            # Ensure there's a current user set
            current = self.get_current_user()
            if current not in users:
                self.set_current_user(self.DEFAULT_USER)

        except Exception as e:
            logger.error(f"Failed to ensure default user: {e}")

    def _save_user_list(self, users: list[str]) -> None:
        """Save the user list to settings."""
        try:
            users_json = json.dumps(users)
            self.settings.setValue("users/user_list", users_json)
            self.settings.sync()
        except Exception as e:
            logger.error(f"Failed to save user list: {e}")

    def _is_valid_username(self, username: str) -> bool:
        """Validate username format."""
        if not username or not isinstance(username, str):
            return False

        # Check length
        if len(username) < 1 or len(username) > 50:
            return False

        # Check for invalid characters
        invalid_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
        if any(char in username for char in invalid_chars):
            return False

        return True

    def _user_exists(self, username: str) -> bool:
        """Check if a user exists."""
        return username in self.get_all_users()

    def _is_global_setting(self, setting_key: str) -> bool:
        """Check if a setting should be global (not user-specific)."""
        return setting_key in self.GLOBAL_SETTINGS

    def _initialize_user_settings(self, username: str) -> None:
        """Initialize default settings for a new user."""
        try:
            # Set some default user-specific settings
            default_settings = {
                "profile/created_date": "2024-01-01",
                "preferences/theme": "default",
                "preferences/auto_save": True,
                "preferences/show_tooltips": True,
            }

            for key, value in default_settings.items():
                if self.get_user_setting(username, key) is None:
                    self.set_user_setting(username, key, value)

        except Exception as e:
            logger.error(f"Failed to initialize settings for user {username}: {e}")

    def _clear_user_settings(self, username: str) -> None:
        """Clear all settings for a user."""
        try:
            # Remove all keys in the user's group
            self.settings.beginGroup(f"user_{username}")
            keys = self.settings.childKeys()
            for key in keys:
                self.settings.remove(key)
            self.settings.endGroup()

            # Also remove the group itself if it's empty
            if not self.settings.childKeys():
                self.settings.remove(f"user_{username}")

            self.settings.sync()

        except Exception as e:
            logger.error(f"Failed to clear settings for user {username}: {e}")
