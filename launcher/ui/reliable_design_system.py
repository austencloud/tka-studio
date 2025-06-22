"""
Reliable Design System - Single Implementation Path
=================================================

Replaces the dual enhanced/fallback system with one solid implementation
using proven PyQt6 techniques. No conditional loading or fallbacks.
"""

from typing import Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication


class ReliableTokens:
    """Reliable design tokens optimized for PyQt6 visibility."""

    # ENHANCED VISIBILITY - Increased opacity for better readability
    GLASS = {
        "primary": "rgba(40, 40, 40, 0.95)",  # Much more opaque
        "secondary": "rgba(50, 50, 50, 0.90)",  # Visible contrast
        "tertiary": "rgba(35, 35, 35, 0.85)",  # Still glassmorphic feel
        "hover": "rgba(55, 55, 55, 0.95)",  # Clear hover state
        "pressed": "rgba(30, 30, 30, 0.98)",  # Tactile feedback
        "selected": "rgba(45, 45, 45, 0.98)",  # Clear selection
    }

    # ACCENT BORDERS - Replace backdrop blur with colored borders
    BORDERS = {
        "default": "1px solid rgba(255, 255, 255, 0.15)",
        "hover": "1px solid rgba(255, 255, 255, 0.25)",
        "focus": "2px solid rgba(59, 130, 246, 0.6)",
        "selected": "2px solid rgba(59, 130, 246, 0.8)",
    }

    # RELIABLE SHADOWS - Use QGraphicsDropShadowEffect compatible values
    SHADOWS = {
        "card": {"blur": 15, "offset": (0, 4), "color": "rgba(0, 0, 0, 0.2)"},
        "card_hover": {"blur": 20, "offset": (0, 8), "color": "rgba(0, 0, 0, 0.3)"},
        "button": {"blur": 8, "offset": (0, 2), "color": "rgba(0, 0, 0, 0.15)"},
        "glow": {"blur": 12, "offset": (0, 0), "color": "rgba(59, 130, 246, 0.4)"},
    }

    # ACCENT COLORS - Keep existing excellent system
    ACCENTS = {
        "blue": {"primary": "#3B82F6", "surface": "rgba(59, 130, 246, 0.15)"},
        "purple": {"primary": "#9333EA", "surface": "rgba(147, 51, 234, 0.15)"},
        "emerald": {"primary": "#10B981", "surface": "rgba(16, 185, 129, 0.15)"},
        "rose": {"primary": "#F43F5E", "surface": "rgba(244, 63, 94, 0.15)"},
        "amber": {"primary": "#F59E0B", "surface": "rgba(245, 158, 11, 0.15)"},
        "cyan": {"primary": "#06B6D4", "surface": "rgba(6, 182, 212, 0.15)"},
    }

    # TYPOGRAPHY - Simplified for reliability
    TYPOGRAPHY = {
        "font_family": "'Inter', 'Segoe UI', sans-serif",
        "sizes": {"sm": 12, "base": 14, "lg": 16, "xl": 18, "title": 20},
        "weights": {"normal": 400, "medium": 500, "semibold": 600, "bold": 700},
    }

    # SPACING - 8px grid system
    SPACING = {"xs": 4, "sm": 8, "md": 16, "lg": 24, "xl": 32}

    # RADIUS - Consistent rounding
    RADIUS = {"sm": 8, "md": 12, "lg": 16, "xl": 20}


class ReliableStyleBuilder:
    """Builds reliable CSS using only proven PyQt6 patterns."""

    def __init__(self):
        self.tokens = ReliableTokens()
        self.current_accent = "blue"

    def glass_surface(self, variant: str = "primary") -> str:
        """Generate reliable glassmorphism CSS."""
        return f"""
            background-color: {self.tokens.GLASS[variant]};
            border: {self.tokens.BORDERS["default"]};
        """

    def glass_surface_hover(self, variant: str = "primary") -> str:
        """Generate hover glassmorphism CSS."""
        return f"""
            background-color: {self.tokens.GLASS["hover"]};
            border: {self.tokens.BORDERS["hover"]};
        """

    def accent_button(self) -> str:
        """Generate accent button CSS."""
        accent = self.tokens.ACCENTS[self.current_accent]
        return f"""
            background-color: {accent["primary"]};
            border: 1px solid {accent["primary"]};
            color: #ffffff;
        """

    def secondary_button(self) -> str:
        """Generate secondary button CSS."""
        return f"""
            {self.glass_surface("secondary")}
            color: rgba(255, 255, 255, 0.9);
        """

    def typography(self, size: str = "base", weight: str = "normal") -> str:
        """Generate typography CSS."""
        return f"""
            font-family: {self.tokens.TYPOGRAPHY["font_family"]};
            font-size: {self.tokens.TYPOGRAPHY["sizes"][size]}px;
            font-weight: {self.tokens.TYPOGRAPHY["weights"][weight]};
        """


# Global instances
_reliable_style_builder = ReliableStyleBuilder()


def get_reliable_style_builder() -> ReliableStyleBuilder:
    """Get the global reliable style builder."""
    return _reliable_style_builder
