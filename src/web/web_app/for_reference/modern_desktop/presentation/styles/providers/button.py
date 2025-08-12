"""
Button style provider implementation.
"""

from __future__ import annotations

from . import StyleProvider
from ..core.types import StyleVariant
from ..glassmorphism_styles import GlassmorphismStyleGenerator


class ButtonStyleProvider(StyleProvider):
    """Style provider for button components."""

    def __init__(self, design_system):
        self.design_system = design_system

    def generate_style(
        self,
        variant: StyleVariant = StyleVariant.DEFAULT,
        size: str = "medium",
        **kwargs,
    ) -> str:
        """Generate button styling using the existing glassmorphism system."""
        # Map StyleVariant to glassmorphism variant strings
        variant_map = {
            StyleVariant.DEFAULT: "default",
            StyleVariant.ACCENT: "accent",
            StyleVariant.SUBTLE: "subtle",
        }

        glassmorphism_variant = variant_map.get(variant, "default")

        # Use existing glassmorphism button generator
        return GlassmorphismStyleGenerator.create_button_style(
            variant=glassmorphism_variant,
            size=size,
            custom_properties=kwargs.get("custom_properties"),
        )
