"""
Settings provider for fade animations.
Integrates with the modern TKA settings system.
"""

from desktop.modern.core.interfaces.animation_interfaces import (
    EasingType,
    IFadeSettingsProvider,
)
from desktop.modern.core.interfaces.settings_interfaces import ISettingsCoordinator


class FadeSettingsProvider(IFadeSettingsProvider):
    """Provider for fade animation settings using the modern settings system."""

    # Settings keys
    FADES_ENABLED_KEY = "ui.animations.fades_enabled"
    DEFAULT_DURATION_KEY = "ui.animations.default_duration"
    DEFAULT_EASING_KEY = "ui.animations.default_easing"

    def __init__(self, settings_coordinator: ISettingsCoordinator):
        self._settings = settings_coordinator
        self._setup_default_settings()

    def _setup_default_settings(self) -> None:
        """Ensure default settings exist."""
        defaults = {
            self.FADES_ENABLED_KEY: True,
            self.DEFAULT_DURATION_KEY: 250,
            self.DEFAULT_EASING_KEY: "IN_OUT_QUAD",
        }

        for key, default_value in defaults.items():
            if self._settings.get_setting(key) is None:
                self._settings.set_setting(key, default_value)

    def get_fades_enabled(self) -> bool:
        """Check if fade animations are enabled."""
        return self._settings.get_setting(self.FADES_ENABLED_KEY, True)

    def get_default_duration(self) -> int:
        """Get default animation duration in milliseconds."""
        return self._settings.get_setting(self.DEFAULT_DURATION_KEY, 250)

    def get_default_easing(self) -> EasingType:
        """Get default easing type."""
        easing_name = self._settings.get_setting(self.DEFAULT_EASING_KEY, "IN_OUT_QUAD")
        try:
            return EasingType[easing_name]
        except KeyError:
            return EasingType.IN_OUT_QUAD

    def set_fades_enabled(self, enabled: bool) -> None:
        """Enable or disable fade animations."""
        self._settings.set_setting(self.FADES_ENABLED_KEY, enabled)

    def set_default_duration(self, duration: int) -> None:
        """Set default animation duration."""
        self._settings.set_setting(self.DEFAULT_DURATION_KEY, duration)

    def set_default_easing(self, easing: EasingType) -> None:
        """Set default easing type."""
        self._settings.set_setting(self.DEFAULT_EASING_KEY, easing.name)
