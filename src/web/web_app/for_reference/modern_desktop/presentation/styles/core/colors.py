"""
Centralized color palette for the design system.
"""

from __future__ import annotations

from dataclasses import dataclass

# Import existing glassmorphism components
from ..glassmorphism_styles import GlassmorphismColors


@dataclass
class ColorPalette:
    """Comprehensive color palette extending glassmorphism colors."""

    # Glass Colors (from existing system)
    GLASS_BASE = GlassmorphismColors.GLASS_BASE
    GLASS_LIGHT = GlassmorphismColors.GLASS_LIGHT
    GLASS_LIGHTER = GlassmorphismColors.GLASS_LIGHTER

    # Border Colors (from existing system)
    BORDER_SUBTLE = GlassmorphismColors.BORDER_SUBTLE
    BORDER_NORMAL = GlassmorphismColors.BORDER_NORMAL
    BORDER_STRONG = GlassmorphismColors.BORDER_STRONG

    # Accent Colors (from existing system)
    ACCENT_BASE = GlassmorphismColors.ACCENT_BASE
    ACCENT_HOVER = GlassmorphismColors.ACCENT_HOVER
    ACCENT_ACTIVE = GlassmorphismColors.ACCENT_ACTIVE
    ACCENT_BORDER = GlassmorphismColors.ACCENT_BORDER
    ACCENT_BORDER_HOVER = GlassmorphismColors.ACCENT_BORDER_HOVER

    # Text Colors (from existing system)
    TEXT_PRIMARY = GlassmorphismColors.TEXT_PRIMARY
    TEXT_SECONDARY = GlassmorphismColors.TEXT_SECONDARY
    TEXT_MUTED = GlassmorphismColors.TEXT_MUTED
    TEXT_DISABLED = GlassmorphismColors.TEXT_DISABLED

    # Additional semantic colors
    OVERLAY_DARK = "rgba(0, 0, 0, 0.9)"
    OVERLAY_LIGHT = "rgba(0, 0, 0, 0.5)"

    # Contextual colors
    WARNING_BASE = "rgba(255, 193, 7, 0.3)"
    WARNING_BORDER = "rgba(255, 193, 7, 0.5)"
    SUCCESS_BASE = "rgba(40, 167, 69, 0.3)"
    SUCCESS_BORDER = "rgba(40, 167, 69, 0.5)"
    ERROR_BASE = "rgba(220, 53, 69, 0.3)"
    ERROR_BORDER = "rgba(220, 53, 69, 0.5)"
