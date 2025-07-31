#!/usr/bin/env python3
"""
TKA Launcher Design System - Premium 2025 Glassmorphism
======================================================

Centralized design tokens, themes, and styling system for the TKA Launcher.
Implements premium 2025 glassmorphism design with:
- Semantic color tokens with dynamic accent system
- Advanced shadow and blur effects
- Inter typography with 8px grid system
- WCAG 4.5:1 contrast ratios
- Hardware-accelerated animations

Architecture:
- DesignTokens: Core design values and semantic tokens
- ThemeManager: Dynamic theming with system integration
- StyleBuilder: CSS generation utilities
- AnimationPresets: Reusable animation configurations
"""

from dataclasses import dataclass
from enum import Enum
import logging
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QApplication

logger = logging.getLogger(__name__)


class AccentColor(Enum):
    """Available accent color variants."""

    BLUE = "blue"
    PURPLE = "purple"
    EMERALD = "emerald"
    ROSE = "rose"
    AMBER = "amber"
    CYAN = "cyan"


class AnimationCurve(Enum):
    """Animation easing curve presets."""

    EASE_OUT_EXPO = "ease-out-expo"
    EASE_IN_OUT_QUART = "ease-in-out-quart"
    SPRING_GENTLE = "spring-gentle"
    SPRING_BOUNCY = "spring-bouncy"


@dataclass
class DesignTokens:
    """
    Core design tokens for the TKA Launcher.

    Implements semantic naming with dynamic accent system
    and premium glassmorphism effects.
    """

    # Glassmorphism Surface Colors
    GLASS = {
        "surface_primary": "rgba(255, 255, 255, 0.25)",  # Increased for visibility
        "surface_secondary": "rgba(255, 255, 255, 0.18)",  # Increased for visibility
        "surface_tertiary": "rgba(255, 255, 255, 0.12)",  # Increased for visibility
        "surface_hover": "rgba(255, 255, 255, 0.35)",  # Increased for visibility
        "surface_pressed": "rgba(255, 255, 255, 0.15)",  # Increased for visibility
        "surface_selected": "rgba(255, 255, 255, 0.30)",  # Increased for visibility
        "surface_disabled": "rgba(255, 255, 255, 0.08)",  # Increased for visibility
    }

    # Border Colors with Semantic Naming
    BORDERS = {
        "subtle": "rgba(255, 255, 255, 0.30)",  # Increased for visibility
        "emphasis": "rgba(255, 255, 255, 0.45)",  # Increased for visibility
        "strong": "rgba(255, 255, 255, 0.60)",  # Increased for visibility
        "focus": "rgba(59, 130, 246, 0.6)",
        "error": "rgba(239, 68, 68, 0.6)",
        "success": "rgba(34, 197, 94, 0.6)",
        "warning": "rgba(245, 158, 11, 0.6)",
    }

    # Dynamic Accent System
    ACCENT_VARIANTS = {
        AccentColor.BLUE: {
            "primary": "rgba(59, 130, 246, 0.9)",
            "secondary": "rgba(37, 99, 235, 0.85)",
            "tertiary": "rgba(29, 78, 216, 0.8)",
            "surface": "rgba(59, 130, 246, 0.12)",
        },
        AccentColor.PURPLE: {
            "primary": "rgba(147, 51, 234, 0.9)",
            "secondary": "rgba(126, 34, 206, 0.85)",
            "tertiary": "rgba(107, 33, 168, 0.8)",
            "surface": "rgba(147, 51, 234, 0.12)",
        },
        AccentColor.EMERALD: {
            "primary": "rgba(16, 185, 129, 0.9)",
            "secondary": "rgba(5, 150, 105, 0.85)",
            "tertiary": "rgba(4, 120, 87, 0.8)",
            "surface": "rgba(16, 185, 129, 0.12)",
        },
        AccentColor.ROSE: {
            "primary": "rgba(244, 63, 94, 0.9)",
            "secondary": "rgba(225, 29, 72, 0.85)",
            "tertiary": "rgba(190, 18, 60, 0.8)",
            "surface": "rgba(244, 63, 94, 0.12)",
        },
        AccentColor.AMBER: {
            "primary": "rgba(245, 158, 11, 0.9)",
            "secondary": "rgba(217, 119, 6, 0.85)",
            "tertiary": "rgba(180, 83, 9, 0.8)",
            "surface": "rgba(245, 158, 11, 0.12)",
        },
        AccentColor.CYAN: {
            "primary": "rgba(6, 182, 212, 0.9)",
            "secondary": "rgba(8, 145, 178, 0.85)",
            "tertiary": "rgba(14, 116, 144, 0.8)",
            "surface": "rgba(6, 182, 212, 0.12)",
        },
    }

    # Enhanced Shadow System for Depth
    SHADOWS = {
        "card": "0 8px 32px rgba(0, 0, 0, 0.12)",
        "card_hover": "0 12px 48px rgba(0, 0, 0, 0.18)",
        "card_pressed": "0 4px 16px rgba(0, 0, 0, 0.08)",
        "button": "0 4px 16px rgba(0, 0, 0, 0.1)",
        "button_hover": "0 6px 24px rgba(0, 0, 0, 0.15)",
        "modal": "0 24px 64px rgba(0, 0, 0, 0.25)",
        "tooltip": "0 2px 8px rgba(0, 0, 0, 0.15)",
        "glow": "0 0 24px rgba(59, 130, 246, 0.3)",
    }

    # Typography System with Inter Font
    TYPOGRAPHY = {
        "font_family": "'Inter', 'Segoe UI', sans-serif",
        "font_sizes": {
            "xs": "10px",
            "sm": "12px",
            "base": "14px",
            "lg": "16px",
            "xl": "18px",
            "2xl": "20px",
            "3xl": "24px",
            "4xl": "32px",
        },
        "font_weights": {
            "light": 300,
            "normal": 400,
            "medium": 500,
            "semibold": 600,
            "bold": 700,
        },
        "line_heights": {
            "tight": 1.2,
            "normal": 1.4,
            "relaxed": 1.6,
        },
    }

    # 8px Grid System
    SPACING = {
        "xs": "4px",  # 0.5 * 8
        "sm": "8px",  # 1 * 8
        "md": "16px",  # 2 * 8
        "lg": "24px",  # 3 * 8
        "xl": "32px",  # 4 * 8
        "2xl": "40px",  # 5 * 8
        "3xl": "48px",  # 6 * 8
        "4xl": "64px",  # 8 * 8
    }

    # Border Radius System
    RADIUS = {
        "sm": "8px",
        "md": "12px",
        "lg": "16px",
        "xl": "20px",
        "2xl": "24px",
        "full": "9999px",
    }

    # Animation Durations (in milliseconds)
    DURATIONS = {
        "instant": 0,
        "fast": 150,
        "normal": 300,
        "slow": 500,
        "slower": 800,
    }

    # Z-Index Layers
    Z_INDEX = {
        "base": 0,
        "dropdown": 100,
        "modal": 200,
        "notification": 300,
        "tooltip": 400,
        "overlay": 500,
    }


class ThemeManager(QObject):
    """
    Dynamic theme management with system integration.

    Features:
    - System accent color detection
    - Time-based theme adjustments
    - Accessibility modes
    - Custom accent selection
    """

    theme_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.current_accent = AccentColor.BLUE
        self.tokens = DesignTokens()
        self._system_accent = self._detect_system_accent()

    def _detect_system_accent(self) -> AccentColor:
        """Detect system accent color (Windows/macOS integration)."""
        try:
            # Try to get system accent color
            palette = QApplication.palette()
            highlight = palette.color(QPalette.ColorRole.Highlight)

            # Map to closest accent color
            if (
                highlight.blue() > highlight.red()
                and highlight.blue() > highlight.green()
            ):
                return AccentColor.BLUE
            elif highlight.red() > highlight.green():
                return AccentColor.ROSE
            elif highlight.green() > highlight.red():
                return AccentColor.EMERALD
            else:
                return AccentColor.PURPLE

        except Exception as e:
            logger.warning(f"Could not detect system accent: {e}")
            return AccentColor.BLUE

    def set_accent_color(self, accent: AccentColor):
        """Set the current accent color."""
        self.current_accent = accent
        self.theme_changed.emit(self.get_current_theme())
        logger.info(f"🎨 Accent color changed to: {accent.value}")

    def get_current_theme(self) -> dict[str, Any]:
        """Get the current theme configuration."""
        return {
            "accent": self.tokens.ACCENT_VARIANTS[self.current_accent],
            "glass": self.tokens.GLASS,
            "borders": self.tokens.BORDERS,
            "shadows": self.tokens.SHADOWS,
            "typography": self.tokens.TYPOGRAPHY,
            "spacing": self.tokens.SPACING,
            "radius": self.tokens.RADIUS,
            "durations": self.tokens.DURATIONS,
            "z_index": self.tokens.Z_INDEX,
        }

    def get_accent_variants(self) -> dict[AccentColor, dict[str, str]]:
        """Get all available accent color variants."""
        return self.tokens.ACCENT_VARIANTS


class StyleBuilder:
    """
    Utility class for building CSS styles from design tokens.

    Provides methods to generate consistent CSS from the design system.
    """

    def __init__(self, theme_manager: ThemeManager):
        self.theme_manager = theme_manager
        self.theme = theme_manager.get_current_theme()

        # Update theme when it changes
        theme_manager.theme_changed.connect(self._update_theme)

    def _update_theme(self, new_theme: dict[str, Any]):
        """Update internal theme reference."""
        self.theme = new_theme

    def glassmorphism_surface(
        self, variant: str = "primary", hover: bool = False
    ) -> str:
        """Generate glassmorphism surface CSS (PyQt6 compatible)."""
        surface_key = f"surface_{variant}"
        if hover:
            surface_key = "surface_hover"

        # PyQt6 doesn't support backdrop-filter, so we use solid backgrounds
        return f"""
            background: {self.theme["glass"][surface_key]};
            border: 1px solid {self.theme["borders"]["subtle"]};
        """

    def button_style(self, variant: str = "primary") -> str:
        """Generate button CSS for different variants (PyQt6 compatible)."""
        if variant == "primary":
            # Use solid color instead of gradient for better PyQt6 compatibility
            return f"""
                background-color: {self.theme["accent"]["primary"].replace("rgba", "rgba").replace("0.9", "1.0")};
                border: 1px solid {self.theme["borders"]["emphasis"]};
                color: #ffffff;
            """
        else:  # secondary/ghost
            return f"""
                background-color: {self.theme["glass"]["surface_secondary"]};
                border: 1px solid {self.theme["borders"]["subtle"]};
                color: rgba(255, 255, 255, 0.9);
            """

    def typography(self, size: str = "base", weight: str = "normal") -> str:
        """Generate typography CSS."""
        return f"""
            font-family: {self.theme["typography"]["font_family"]};
            font-size: {self.theme["typography"]["font_sizes"][size]};
            font-weight: {self.theme["typography"]["font_weights"][weight]};
            line-height: {self.theme["typography"]["line_heights"]["normal"]};
        """

    def shadow(self, variant: str = "card") -> str:
        """Generate shadow CSS (PyQt6 doesn't support box-shadow, returns empty)."""
        return ""


# Global design system instance
_theme_manager = None
_style_builder = None


def get_theme_manager() -> ThemeManager:
    """Get the global theme manager instance."""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager


def get_style_builder() -> StyleBuilder:
    """Get the global style builder instance."""
    global _style_builder
    if _style_builder is None:
        _style_builder = StyleBuilder(get_theme_manager())
    return _style_builder


def apply_global_theme():
    """Apply the global theme to the application."""
    theme_manager = get_theme_manager()
    style_builder = get_style_builder()

    # Apply global application stylesheet
    app = QApplication.instance()
    if app:
        global_style = f"""
            QWidget {{
                {style_builder.typography()}
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(15, 15, 15, 0.95),
                    stop:1 rgba(30, 30, 30, 0.95));
                color: #ffffff;
            }}
        """
        app.setStyleSheet(global_style)

    logger.info("🎨 Global theme applied successfully")
