"""
Settings Service Interfaces

Interface definitions for settings services following TKA's clean architecture.
These interfaces define contracts for all settings management operations without
being tied to specific storage implementations (file system vs web storage).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class PropType(Enum):
    """Enumeration of available prop types."""

    STAFF = "Staff"
    FAN = "Fan"
    BUUGENG = "Buugeng"
    CLUB = "Club"
    SWORD = "Sword"
    GUITAR = "Guitar"
    UKULELE = "Ukulele"


class IBackgroundSettingsManager(ABC):
    """Interface for background settings management operations."""

    @abstractmethod
    def get_available_backgrounds(self) -> list[str]:
        """
        Get list of available background types.

        Returns:
            List of background type names

        Note:
            Web implementation: May need to validate asset availability
        """

    @abstractmethod
    def get_current_background(self) -> str:
        """
        Get the currently selected background type.

        Returns:
            Current background type name

        Note:
            Web implementation: Retrieved from localStorage
        """

    @abstractmethod
    def set_background(self, background_type: str) -> bool:
        """
        Set the background type.

        Args:
            background_type: Background type to set

        Returns:
            True if successful, False if invalid background type

        Note:
            Web implementation: Stored in localStorage, may trigger CSS updates
        """

    @abstractmethod
    def is_valid_background(self, background_type: str) -> bool:
        """
        Check if the background type is valid.

        Args:
            background_type: Background type to validate

        Returns:
            True if valid, False otherwise

        Note:
            Web implementation: May need to check asset availability in browser
        """


class IVisibilitySettingsManager(ABC):
    """Interface for visibility settings management operations."""

    @abstractmethod
    def get_glyph_visibility(self, glyph_name: str) -> bool:
        """
        Get visibility state for a specific glyph type.

        Args:
            glyph_name: Name of the glyph type

        Returns:
            True if visible, False if hidden

        Note:
            Web implementation: Retrieved from localStorage with fallback defaults
        """

    @abstractmethod
    def set_glyph_visibility(self, glyph_name: str, visible: bool) -> None:
        """
        Set visibility state for a specific glyph type.

        Args:
            glyph_name: Name of the glyph type
            visible: Visibility state to set

        Note:
            Web implementation: Stored in localStorage, may trigger UI updates
        """

    @abstractmethod
    def get_motion_visibility(self, motion_color: str) -> bool:
        """
        Get visibility for motion arrows (red/blue).

        Args:
            motion_color: Color of the motion ("red" or "blue")

        Returns:
            True if visible, False if hidden
        """

    @abstractmethod
    def set_motion_visibility(self, motion_color: str, visible: bool) -> None:
        """
        Set visibility for motion arrows (red/blue).

        Args:
            motion_color: Color of the motion ("red" or "blue")
            visible: Visibility state to set
        """

    @abstractmethod
    def get_non_radial_visibility(self) -> bool:
        """
        Get visibility state for non-radial points.

        Returns:
            True if visible, False if hidden
        """

    @abstractmethod
    def set_non_radial_visibility(self, visible: bool) -> None:
        """
        Set visibility state for non-radial points.

        Args:
            visible: Visibility state to set
        """

    @abstractmethod
    def get_all_visibility_settings(self) -> dict[str, bool]:
        """
        Get all visibility settings as a dictionary.

        Returns:
            Dictionary mapping glyph names to visibility states

        Note:
            Web implementation: Aggregated from multiple localStorage keys
        """

    @abstractmethod
    def reset_to_defaults(self) -> None:
        """
        Reset all visibility settings to defaults.

        Note:
            Web implementation: Clears relevant localStorage keys
        """

    @abstractmethod
    def get_grid_visibility(self) -> bool:
        """
        Get grid visibility setting.

        Returns:
            True if grid is visible, False if hidden
        """

    @abstractmethod
    def set_grid_visibility(self, visible: bool) -> None:
        """
        Set grid visibility setting.

        Args:
            visible: Grid visibility state to set
        """


class IBeatLayoutSettingsManager(ABC):
    """Interface for beat frame layout settings management operations."""

    @abstractmethod
    def get_layout_for_length(self, sequence_length: int) -> tuple[int, int]:
        """
        Get the layout (rows, cols) for a given sequence length.

        Args:
            sequence_length: Length of the sequence

        Returns:
            Tuple of (rows, columns) for the layout

        Note:
            Web implementation: Retrieved from localStorage with calculated fallbacks
        """

    @abstractmethod
    def set_layout_for_length(self, sequence_length: int, rows: int, cols: int) -> None:
        """
        Set the layout for a specific sequence length.

        Args:
            sequence_length: Length of the sequence
            rows: Number of rows
            cols: Number of columns

        Note:
            Web implementation: Stored in localStorage with structured keys
        """

    @abstractmethod
    def get_default_sequence_length(self) -> int:
        """
        Get the default sequence length setting.

        Returns:
            Default sequence length
        """

    @abstractmethod
    def set_default_sequence_length(self, length: int) -> None:
        """
        Set the default sequence length.

        Args:
            length: Default sequence length (must be positive)
        """

    @abstractmethod
    def get_layout_options_for_length(
        self, sequence_length: int
    ) -> dict[str, tuple[int, int]]:
        """
        Get available layout options for a sequence length.

        Args:
            sequence_length: Length of the sequence

        Returns:
            Dictionary mapping layout descriptions to (rows, cols) tuples

        Note:
            Web implementation: Calculated dynamically, may cache results
        """


class IPropTypeSettingsManager(ABC):
    """Interface for prop type settings management operations."""

    @abstractmethod
    def get_current_prop_type(self) -> PropType:
        """
        Get the currently selected prop type.

        Returns:
            Current prop type enum value

        Note:
            Web implementation: Retrieved from localStorage, parsed to enum
        """

    @abstractmethod
    def set_prop_type(self, prop_type: PropType) -> None:
        """
        Set the current prop type.

        Args:
            prop_type: Prop type to set

        Note:
            Web implementation: Stored in localStorage as string value
        """

    @abstractmethod
    def get_available_prop_types(self) -> list[PropType]:
        """
        Get all available prop types.

        Returns:
            List of available prop type enum values
        """

    @abstractmethod
    def is_valid_prop_type(self, prop_type: PropType) -> bool:
        """
        Check if a prop type is valid.

        Args:
            prop_type: Prop type to validate

        Returns:
            True if valid, False otherwise
        """

    @abstractmethod
    def get_prop_setting(self, setting_key: str, default: Any = None) -> Any:
        """
        Get a prop-related setting.

        Args:
            setting_key: Key for the setting
            default: Default value if setting not found

        Returns:
            Setting value or default

        Note:
            Web implementation: Retrieved from localStorage with prop_ prefix
        """

    @abstractmethod
    def set_prop_setting(self, setting_key: str, value: Any) -> None:
        """
        Set a prop-related setting.

        Args:
            setting_key: Key for the setting
            value: Value to set

        Note:
            Web implementation: Stored in localStorage with prop_ prefix
        """


class IUserProfileSettingsManager(ABC):
    """Interface for user profile settings management operations."""

    @abstractmethod
    def get_current_user(self) -> str:
        """
        Get the current active user.

        Returns:
            Current user name

        Note:
            Web implementation: Retrieved from localStorage
        """

    @abstractmethod
    def set_current_user(self, username: str) -> None:
        """
        Set the current active user.

        Args:
            username: User name to set as current

        Note:
            Web implementation: Stored in localStorage, may trigger profile switch
        """

    @abstractmethod
    def get_all_users(self) -> list[str]:
        """
        Get all available user profiles.

        Returns:
            List of user names

        Note:
            Web implementation: Retrieved from localStorage as JSON array
        """

    @abstractmethod
    def add_user(self, username: str) -> bool:
        """
        Add a new user profile.

        Args:
            username: User name to add

        Returns:
            True if successful, False if username invalid or already exists

        Note:
            Web implementation: Updates localStorage user list
        """

    @abstractmethod
    def remove_user(self, username: str) -> bool:
        """
        Remove a user profile.

        Args:
            username: User name to remove

        Returns:
            True if successful, False if user not found or is last user

        Note:
            Web implementation: Updates localStorage and cleans up user-specific data
        """

    @abstractmethod
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

        Note:
            Web implementation: Retrieved from localStorage with user_ prefix
        """

    @abstractmethod
    def set_user_setting(self, username: str, setting_key: str, value: Any) -> None:
        """
        Set a setting for a specific user.

        Args:
            username: User name
            setting_key: Key for the setting
            value: Value to set

        Note:
            Web implementation: Stored in localStorage with user_ prefix
        """


class IImageExportSettingsManager(ABC):
    """Interface for image export settings management operations."""

    @abstractmethod
    def get_export_format(self) -> str:
        """
        Get the current export format.

        Returns:
            Export format name (e.g., "PNG", "JPEG")

        Note:
            Web implementation: Retrieved from localStorage
        """

    @abstractmethod
    def set_export_format(self, format_name: str) -> bool:
        """
        Set the export format.

        Args:
            format_name: Export format to set

        Returns:
            True if successful, False if invalid format

        Note:
            Web implementation: Stored in localStorage, validates against supported formats
        """

    @abstractmethod
    def get_supported_formats(self) -> list[str]:
        """
        Get list of supported export formats.

        Returns:
            List of supported format names

        Note:
            Web implementation: May differ from desktop due to browser support
        """

    @abstractmethod
    def get_export_quality(self) -> int:
        """
        Get export quality (0-100).

        Returns:
            Export quality percentage
        """

    @abstractmethod
    def set_export_quality(self, quality: int) -> bool:
        """
        Set export quality (0-100).

        Args:
            quality: Quality percentage (0-100)

        Returns:
            True if successful, False if invalid quality
        """

    @abstractmethod
    def get_export_dimensions(self) -> tuple[int, int]:
        """
        Get export dimensions (width, height).

        Returns:
            Tuple of (width, height) in pixels
        """

    @abstractmethod
    def set_export_dimensions(self, width: int, height: int) -> bool:
        """
        Set export dimensions.

        Args:
            width: Width in pixels
            height: Height in pixels

        Returns:
            True if successful, False if invalid dimensions
        """

    @abstractmethod
    def get_include_background(self) -> bool:
        """
        Get whether to include background in export.

        Returns:
            True if background should be included, False otherwise
        """

    @abstractmethod
    def set_include_background(self, include: bool) -> None:
        """
        Set whether to include background in export.

        Args:
            include: Whether to include background
        """

    @abstractmethod
    def get_scale_factor(self) -> float:
        """
        Get the scale factor for export.

        Returns:
            Scale factor (typically 1.0 for normal size)
        """

    @abstractmethod
    def set_scale_factor(self, scale: float) -> bool:
        """
        Set the scale factor for export.

        Args:
            scale: Scale factor (must be positive)

        Returns:
            True if successful, False if invalid scale
        """

    @abstractmethod
    def get_quality_presets(self) -> dict[str, int]:
        """
        Get available quality presets.

        Returns:
            Dictionary mapping preset names to quality values
        """

    @abstractmethod
    def apply_quality_preset(self, preset_name: str) -> bool:
        """
        Apply a quality preset.

        Args:
            preset_name: Name of the preset to apply

        Returns:
            True if successful, False if invalid preset
        """
