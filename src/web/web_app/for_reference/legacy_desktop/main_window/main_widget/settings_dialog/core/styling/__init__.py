from __future__ import annotations
"""
Styling components for glassmorphism design system using coordinator pattern.

This package contains the refactored components that were extracted from
the monolithic GlassmorphismStyler class to follow the Single Responsibility Principle.
"""

from .color_manager import ColorManager
from .component_styler import ComponentStyler
from .effect_manager import EffectManager
from .glassmorphism_coordinator import GlassmorphismCoordinator
from .layout_styler import LayoutStyler
from .typography_manager import TypographyManager

__all__ = [
    "GlassmorphismCoordinator",
    "ColorManager",
    "TypographyManager",
    "ComponentStyler",
    "EffectManager",
    "LayoutStyler",
]
