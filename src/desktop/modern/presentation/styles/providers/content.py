"""
Content component style providers (labels, overlays).
"""

from ..core.types import StyleVariant
from . import StyleProvider


class LabelStyleProvider(StyleProvider):
    """Style provider for label components - consolidates scattered text styling."""

    def __init__(self, design_system):
        self.design_system = design_system

    def generate_style(
        self, variant: StyleVariant = StyleVariant.DEFAULT, **kwargs
    ) -> str:
        """Generate label styling to replace scattered rgba() text color usage."""
        colors = self.design_system.colors
        tokens = self.design_system.tokens

        # Map variants to appropriate text colors
        color_map = {
            StyleVariant.DEFAULT: colors.TEXT_SECONDARY,
            StyleVariant.ACCENT: colors.TEXT_PRIMARY,
            StyleVariant.SUBTLE: colors.TEXT_MUTED,
            StyleVariant.MUTED: colors.TEXT_DISABLED,
            StyleVariant.PROMINENT: colors.TEXT_PRIMARY,
        }

        text_color = color_map.get(variant, colors.TEXT_SECONDARY)

        return f"""
        QLabel {{
            color: {text_color};
            background: transparent;
            font-family: {tokens.font_family};
            font-size: {tokens.font_sizes.get(kwargs.get("size", "base"))};
            font-weight: {tokens.font_weights.get(kwargs.get("weight", "normal"))};
        }}
        """


class OverlayStyleProvider(StyleProvider):
    """Style provider for overlay components."""

    def __init__(self, design_system):
        self.design_system = design_system

    def generate_style(
        self, variant: StyleVariant = StyleVariant.DEFAULT, **kwargs
    ) -> str:
        """Generate overlay styling."""
        colors = self.design_system.colors

        background = colors.OVERLAY_DARK
        if variant == StyleVariant.SUBTLE:
            background = colors.OVERLAY_LIGHT

        return f"""
        QWidget {{
            background-color: {background};
        }}
        """
