#!/usr/bin/env python3
"""
Base Theme System - Smart Theming Foundation
===========================================

Intelligent theming system for TKA Launcher with:
- System accent color integration
- Time-based theme adjustments
- Accessibility modes
- Custom accent selection
- Performance-optimized theme switching

Architecture:
- BaseTheme: Core theme functionality
- SystemIntegration: OS-level theme detection
- TimeBasedTheme: Dynamic time-based adjustments
- AccessibilityTheme: WCAG-compliant variants
"""

from abc import abstractmethod
import datetime
import logging
from typing import Any, Dict, Optional

from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QApplication

from ..design_system import AccentColor, DesignTokens

logger = logging.getLogger(__name__)


class BaseTheme(QObject):
    """
    Base theme class providing core theming functionality.

    Features:
    - Theme state management
    - Color palette generation
    - Animation coordination
    - Performance optimization
    """

    theme_changed = pyqtSignal(dict)

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.tokens = DesignTokens()
        self._current_palette = {}
        self._is_dark_mode = True  # TKA Launcher is primarily dark

    @abstractmethod
    def generate_palette(self) -> Dict[str, Any]:
        """Generate the theme color palette."""

    def apply_theme(self):
        """Apply the theme to the application."""
        palette = self.generate_palette()
        self._current_palette = palette
        self.theme_changed.emit(palette)
        logger.info(f"🎨 Applied theme: {self.name}")

    def get_current_palette(self) -> Dict[str, Any]:
        """Get the current theme palette."""
        return self._current_palette.copy()


class SystemIntegration:
    """
    System-level theme integration.

    Features:
    - OS accent color detection
    - Dark/light mode detection
    - System preference monitoring
    - Cross-platform compatibility
    """

    @staticmethod
    def detect_system_accent() -> AccentColor:
        """Detect the system accent color."""
        try:
            app = QApplication.instance()
            if not app:
                return AccentColor.BLUE

            palette = app.palette()
            highlight = palette.color(QPalette.ColorRole.Highlight)

            # Convert QColor to closest AccentColor
            hue = highlight.hue()

            if 200 <= hue <= 260:  # Blue range
                return AccentColor.BLUE
            elif 260 < hue <= 320:  # Purple range
                return AccentColor.PURPLE
            elif 80 <= hue <= 160:  # Green range
                return AccentColor.EMERALD
            elif hue > 320 or hue <= 20:  # Red range
                return AccentColor.ROSE
            elif 20 < hue <= 80:  # Yellow/Orange range
                return AccentColor.AMBER
            elif 160 < hue < 200:  # Cyan range
                return AccentColor.CYAN
            else:
                return AccentColor.BLUE

        except Exception as e:
            logger.warning(f"Could not detect system accent: {e}")
            return AccentColor.BLUE

    @staticmethod
    def is_dark_mode() -> bool:
        """Detect if system is in dark mode."""
        try:
            app = QApplication.instance()
            if not app:
                return True

            palette = app.palette()
            window_color = palette.color(QPalette.ColorRole.Window)

            # If window background is dark, assume dark mode
            return window_color.lightness() < 128

        except Exception as e:
            logger.warning(f"Could not detect dark mode: {e}")
            return True  # Default to dark mode for TKA


class TimeBasedTheme(BaseTheme):
    """
    Time-based theme with dynamic adjustments.

    Features:
    - Color temperature shifts based on time
    - Automatic day/night transitions
    - Circadian rhythm consideration
    - Smooth transitions
    """

    def __init__(self, base_accent: AccentColor = AccentColor.BLUE):
        super().__init__("Time-Based")
        self.base_accent = base_accent
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._update_time_based_colors)
        self._update_timer.start(60000)  # Update every minute

    def generate_palette(self) -> Dict[str, Any]:
        """Generate time-based color palette."""
        current_hour = datetime.datetime.now().hour

        # Calculate color temperature shift
        if 6 <= current_hour <= 18:  # Daytime
            temperature_shift = 0.0  # Neutral
        elif 18 < current_hour <= 22:  # Evening
            temperature_shift = 0.1  # Slightly warmer
        else:  # Night
            temperature_shift = 0.2  # Warmer, easier on eyes

        # Get base palette
        base_palette = self.tokens.ACCENT_VARIANTS[self.base_accent].copy()

        # Apply temperature shift
        adjusted_palette = self._apply_temperature_shift(
            base_palette, temperature_shift
        )

        return {
            "accent": adjusted_palette,
            "glass": self.tokens.GLASS,
            "borders": self.tokens.BORDERS,
            "shadows": self.tokens.SHADOWS,
            "typography": self.tokens.TYPOGRAPHY,
            "spacing": self.tokens.SPACING,
            "radius": self.tokens.RADIUS,
            "durations": self.tokens.DURATIONS,
            "z_index": self.tokens.Z_INDEX,
            "time_shift": temperature_shift,
        }

    def _apply_temperature_shift(
        self, palette: Dict[str, str], shift: float
    ) -> Dict[str, str]:
        """Apply color temperature shift to palette."""
        adjusted = {}

        for key, color_str in palette.items():
            # Parse RGBA color
            if "rgba(" in color_str:
                # Extract RGBA values
                rgba_part = color_str.split("rgba(")[1].split(")")[0]
                r, g, b, a = map(float, rgba_part.split(","))

                # Apply warm shift (increase red, decrease blue)
                r = min(255, r + (shift * 20))
                b = max(0, b - (shift * 15))

                adjusted[key] = f"rgba({int(r)}, {int(g)}, {int(b)}, {a})"
            else:
                adjusted[key] = color_str

        return adjusted

    def _update_time_based_colors(self):
        """Update colors based on current time."""
        self.apply_theme()

    def set_base_accent(self, accent: AccentColor):
        """Set the base accent color."""
        self.base_accent = accent
        self.apply_theme()


class AccessibilityTheme(BaseTheme):
    """
    Accessibility-focused theme variant.

    Features:
    - WCAG 4.5:1 contrast ratios
    - Reduced motion options
    - High contrast mode
    - Focus indicators
    """

    def __init__(self, high_contrast: bool = False, reduced_motion: bool = False):
        super().__init__("Accessibility")
        self.high_contrast = high_contrast
        self.reduced_motion = reduced_motion

    def generate_palette(self) -> Dict[str, Any]:
        """Generate accessibility-compliant palette."""
        base_tokens = DesignTokens()

        if self.high_contrast:
            # High contrast variant
            glass_colors = {
                "surface_primary": "rgba(255, 255, 255, 0.25)",
                "surface_secondary": "rgba(255, 255, 255, 0.20)",
                "surface_tertiary": "rgba(255, 255, 255, 0.15)",
                "surface_hover": "rgba(255, 255, 255, 0.35)",
                "surface_pressed": "rgba(255, 255, 255, 0.15)",
                "surface_selected": "rgba(255, 255, 255, 0.30)",
                "surface_disabled": "rgba(255, 255, 255, 0.10)",
            }

            border_colors = {
                "subtle": "rgba(255, 255, 255, 0.40)",
                "emphasis": "rgba(255, 255, 255, 0.60)",
                "strong": "rgba(255, 255, 255, 0.80)",
                "focus": "rgba(59, 130, 246, 1.0)",
                "error": "rgba(239, 68, 68, 1.0)",
                "success": "rgba(34, 197, 94, 1.0)",
                "warning": "rgba(245, 158, 11, 1.0)",
            }
        else:
            glass_colors = base_tokens.GLASS
            border_colors = base_tokens.BORDERS

        # Adjust animation durations for reduced motion
        durations = base_tokens.DURATIONS.copy()
        if self.reduced_motion:
            durations = {key: min(150, value) for key, value in durations.items()}

        return {
            "accent": base_tokens.ACCENT_VARIANTS[AccentColor.BLUE],
            "glass": glass_colors,
            "borders": border_colors,
            "shadows": base_tokens.SHADOWS,
            "typography": base_tokens.TYPOGRAPHY,
            "spacing": base_tokens.SPACING,
            "radius": base_tokens.RADIUS,
            "durations": durations,
            "z_index": base_tokens.Z_INDEX,
            "accessibility": {
                "high_contrast": self.high_contrast,
                "reduced_motion": self.reduced_motion,
            },
        }

    def set_high_contrast(self, enabled: bool):
        """Enable or disable high contrast mode."""
        self.high_contrast = enabled
        self.apply_theme()

    def set_reduced_motion(self, enabled: bool):
        """Enable or disable reduced motion."""
        self.reduced_motion = enabled
        self.apply_theme()


class SmartThemeManager(QObject):
    """
    Intelligent theme manager that coordinates all theme variants.

    Features:
    - Automatic theme selection
    - Smooth theme transitions
    - User preference persistence
    - Performance optimization
    """

    theme_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.current_theme = None
        self.available_themes = {}
        self._setup_default_themes()

    def _setup_default_themes(self):
        """Setup default theme variants."""
        # System-integrated theme
        system_accent = SystemIntegration.detect_system_accent()
        self.available_themes["system"] = TimeBasedTheme(system_accent)

        # Accessibility theme
        self.available_themes["accessibility"] = AccessibilityTheme()

        # High contrast theme
        self.available_themes["high_contrast"] = AccessibilityTheme(high_contrast=True)

        # Connect theme signals
        for theme in self.available_themes.values():
            theme.theme_changed.connect(self.theme_changed.emit)

    def set_active_theme(self, theme_name: str):
        """Set the active theme."""
        if theme_name in self.available_themes:
            self.current_theme = self.available_themes[theme_name]
            self.current_theme.apply_theme()
            logger.info(f"🎨 Switched to theme: {theme_name}")
        else:
            logger.warning(f"Theme not found: {theme_name}")

    def get_current_theme(self) -> Optional[BaseTheme]:
        """Get the current active theme."""
        return self.current_theme

    def get_available_themes(self) -> Dict[str, BaseTheme]:
        """Get all available themes."""
        return self.available_themes.copy()

    def auto_select_theme(self):
        """Automatically select the best theme based on system settings."""
        # Start with system theme
        self.set_active_theme("system")


# Global theme manager instance
_smart_theme_manager = None


def get_smart_theme_manager() -> SmartThemeManager:
    """Get the global smart theme manager instance."""
    global _smart_theme_manager
    if _smart_theme_manager is None:
        _smart_theme_manager = SmartThemeManager()
        _smart_theme_manager.auto_select_theme()
    return _smart_theme_manager
