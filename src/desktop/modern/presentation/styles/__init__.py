"""
TKA Modern UI Styles Module

This module provides a comprehensive styling system for the TKA Modern desktop application.
It includes a centralized design system, glassmorphism effects, component mixins, and
utility functions for consistent UI styling across the application.

Key Components:
- DesignSystem: Central styling coordination
- GlassmorphismStyles: Modern glass aesthetic effects
- StyleMixin: Component integration utilities
- ComponentTypes and StyleVariants: Type definitions
"""

# Component-specific mixins
from __future__ import annotations

from .component_mixins import *

# Type definitions
from .core.types import ComponentType, StyleVariant

# Core design system
from .design_system import (
    DesignSystem,
    get_design_system,
)

# Glassmorphism styling
from .glassmorphism_styles import (
    GlassmorphismColors,
    GlassmorphismEffects,
    GlassmorphismStyleGenerator,
)

# Component integration mixins
from .mixins import (
    StyledWidget,
    StyleMixin,
    apply_dialog_style_to_widget,
    apply_style_to_widget,
)


# Style guide utilities (if available)
try:
    from .style_guide import *
except ImportError:
    # Style guide may not be implemented yet Hi there how are you doing
    pass

# Export all public interfaces
__all__ = [
    # Core design system
    "DesignSystem",
    "get_design_system",
    # Type definitions
    "ComponentType",
    "StyleVariant",
    # Glassmorphism
    "GlassmorphismColors",
    "GlassmorphismEffects",
    "GlassmorphismStyleGenerator",
    # Mixins and utilities
    "StyleMixin",
    "StyledWidget",
    "apply_style_to_widget",
    "apply_dialog_style_to_widget",
]


# Module-level convenience functions
def create_component_style(
    component_type: ComponentType,
    variant: StyleVariant = StyleVariant.DEFAULT,
    **kwargs,
) -> str:
    """
    Module-level convenience function to create component styles.

    Args:
        component_type: The type of component to style
        variant: The style variant to apply
        **kwargs: Additional styling options

    Returns:
        CSS string for the component
    """
    return get_design_system().create_component_style(component_type, variant, **kwargs)


def get_color(color_name: str) -> str:
    """
    Module-level convenience function to get colors from the design system.

    Args:
        color_name: Name of the color to retrieve

    Returns:
        Color value as a string
    """
    return get_design_system().get_color(color_name)


def get_effect(effect_name: str) -> str:
    """
    Module-level convenience function to get effects from the design system.

    Args:
        effect_name: Name of the effect to retrieve

    Returns:
        Effect value as a string
    """
    return get_design_system().get_effect(effect_name)


# Add module-level convenience functions to exports
__all__.extend(
    [
        "create_component_style",
        "get_color",
        "get_effect",
    ]
)
