"""
Design tokens for typography, spacing, shadows, and other design primitives.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..glassmorphism_styles import GlassmorphismEffects


@dataclass
class DesignTokens:
    """Complete design token system for consistent styling."""

    # Typography
    font_family: str = '"Inter", "Segoe UI", sans-serif'
    font_sizes: dict[str, str] = None
    font_weights: dict[str, int] = None
    line_heights: dict[str, str] = None
    letter_spacings: dict[str, str] = None

    # Spacing
    spacing: dict[str, str] = None

    # Border radius
    radius: dict[str, str] = None

    # Shadows
    shadows: dict[str, str] = None

    # Transitions
    transitions: dict[str, str] = None

    def __post_init__(self):
        """Initialize default values for design tokens."""
        if self.font_sizes is None:
            self.font_sizes = {
                "xs": "10px",
                "sm": "11px",
                "base": "12px",
                "lg": "13px",
                "xl": "14px",
                "2xl": "16px",
                "3xl": "18px",
                "4xl": "20px",
            }

        if self.font_weights is None:
            self.font_weights = {
                "light": 300,
                "normal": 400,
                "medium": 500,
                "semibold": 600,
                "bold": 700,
            }

        if self.line_heights is None:
            self.line_heights = {"tight": "1.2", "normal": "1.4", "relaxed": "1.6"}

        if self.letter_spacings is None:
            self.letter_spacings = {"tight": "-0.5px", "normal": "0px", "wide": "0.5px"}

        if self.spacing is None:
            self.spacing = {
                "0": "0px",
                "1": "2px",
                "2": "4px",
                "3": "8px",
                "4": "12px",
                "5": "16px",
                "6": "20px",
                "7": "24px",
                "8": "32px",
                "9": "40px",
                "10": "48px",
            }

        if self.radius is None:
            self.radius = {
                "none": "0px",
                "sm": GlassmorphismEffects.RADIUS_SMALL,
                "base": GlassmorphismEffects.RADIUS_MEDIUM,
                "lg": GlassmorphismEffects.RADIUS_LARGE,
                "xl": GlassmorphismEffects.RADIUS_XLARGE,
                "full": "9999px",
            }

        if self.shadows is None:
            self.shadows = {
                "none": "none",
                "sm": GlassmorphismEffects.SHADOW_SUBTLE,
                "base": GlassmorphismEffects.SHADOW_NORMAL,
                "accent": GlassmorphismEffects.SHADOW_ACCENT,
                "accent-hover": GlassmorphismEffects.SHADOW_ACCENT_HOVER,
            }

        if self.transitions is None:
            # Note: CSS transitions not supported in PyQt6 - use QPropertyAnimation instead
            self.transitions = {
                "fast": "0.15s ease",
                "normal": "0.2s ease",
                "slow": "0.3s ease",
            }
