"""
Centralized Design System for TKA Modern UI

This module provides the core design system that coordinates all visual styling
across the application. It integrates glassmorphism effects, typography, spacing,
and component-specific styling into a unified system.
"""

from functools import lru_cache
from typing import Any, Dict, Optional

from .core.types import ComponentType, StyleVariant
from .glassmorphism_styles import (
    GlassmorphismColors,
    GlassmorphismEffects,
    GlassmorphismStyleGenerator,
)


class DesignSystem:
    """
    Central design system that provides consistent styling across the application.

    This class coordinates all visual elements including colors, typography,
    spacing, and component-specific styles while maintaining the glassmorphism
    aesthetic throughout the application.
    """

    def __init__(self):
        """Initialize the design system with default configuration."""
        self._colors = GlassmorphismColors()
        self._effects = GlassmorphismEffects()
        self._style_generator = GlassmorphismStyleGenerator()
        self._component_styles = self._initialize_component_styles()

    def _initialize_component_styles(self) -> Dict[ComponentType, Dict[str, Any]]:
        """Initialize the component style definitions."""
        return {
            ComponentType.BUTTON: self._get_button_styles(),
            ComponentType.TAB_BUTTON: self._get_tab_button_styles(),
            ComponentType.MENU_BAR: self._get_menu_bar_styles(),
            ComponentType.TAB_CONTAINER: self._get_tab_container_styles(),
            ComponentType.PANEL: self._get_panel_styles(),
            ComponentType.DIALOG: self._get_dialog_styles(),
            ComponentType.CONTAINER: self._get_container_styles(),
            ComponentType.INPUT: self._get_input_styles(),
            ComponentType.CHECKBOX: self._get_checkbox_styles(),
            ComponentType.SLIDER: self._get_slider_styles(),
            ComponentType.LABEL: self._get_label_styles(),
            ComponentType.CARD: self._get_card_styles(),
            ComponentType.LIST_ITEM: self._get_list_item_styles(),
            ComponentType.OVERLAY: self._get_overlay_styles(),
            ComponentType.TOOLTIP: self._get_tooltip_styles(),
            ComponentType.SEQUENCE_VIEWER: self._get_sequence_viewer_styles(),
        }

    def create_component_style(
        self,
        component_type: ComponentType,
        variant: StyleVariant = StyleVariant.DEFAULT,
        **kwargs,
    ) -> str:
        """
        Create CSS styling for a specific component type and variant.

        Args:
            component_type: The type of component to style
            variant: The style variant to apply
            **kwargs: Additional component-specific options

        Returns:
            CSS string for the component
        """
        if component_type not in self._component_styles:
            raise ValueError(f"Unsupported component type: {component_type}")

        component_config = self._component_styles[component_type]
        variant_styles = component_config.get(
            variant.value, component_config.get("default", {})
        )

        # Apply any kwargs as overrides
        final_styles = {**variant_styles}
        if kwargs:
            final_styles.update(kwargs)

        return self._convert_style_dict_to_css(final_styles)

    def _convert_style_dict_to_css(self, style_dict: Dict[str, str]) -> str:
        """Convert a dictionary of CSS properties to a CSS string."""
        css_rules = []
        for property_name, value in style_dict.items():
            # Handle special font properties that need prefixes
            if property_name == "size":
                css_property = "font-size"
            elif property_name == "weight":
                css_property = "font-weight"
            else:
                # Convert Python-style property names to CSS
                css_property = property_name.replace("_", "-")
            css_rules.append(f"{css_property}: {value};")
        return " ".join(css_rules)

    # Component Style Definitions
    def _get_button_styles(self) -> Dict[str, Dict[str, str]]:
        """Get button component styles for all variants."""
        return {
            "default": {
                "background-color": self._colors.GLASS_BASE,
                "border": f"1px solid {self._colors.BORDER_SUBTLE}",
                "border-radius": self._effects.RADIUS_MEDIUM,
                "padding": self._effects.PADDING_MEDIUM,
                "color": self._colors.TEXT_PRIMARY,
                "font-weight": "500",
                "transition": self._effects.TRANSITION_NORMAL,
                "box-shadow": self._effects.SHADOW_SUBTLE,
            },
            "accent": {
                "background-color": self._colors.ACCENT_BASE,
                "border": f"1px solid {self._colors.ACCENT_BORDER}",
                "border-radius": self._effects.RADIUS_MEDIUM,
                "padding": self._effects.PADDING_MEDIUM,
                "color": self._colors.TEXT_PRIMARY,
                "font-weight": "600",
                "transition": self._effects.TRANSITION_NORMAL,
                "box-shadow": self._effects.SHADOW_ACCENT,
            },
            "subtle": {
                "background-color": "transparent",
                "border": f"1px solid {self._colors.BORDER_SUBTLE}",
                "border-radius": self._effects.RADIUS_MEDIUM,
                "padding": self._effects.PADDING_MEDIUM,
                "color": self._colors.TEXT_SECONDARY,
                "font-weight": "400",
                "transition": self._effects.TRANSITION_NORMAL,
            },
            "prominent": {
                "background-color": self._colors.GLASS_LIGHTER,
                "border": f"2px solid {self._colors.BORDER_STRONG}",
                "border-radius": self._effects.RADIUS_LARGE,
                "padding": self._effects.PADDING_LARGE,
                "color": self._colors.TEXT_PRIMARY,
                "font-weight": "700",
                "transition": self._effects.TRANSITION_NORMAL,
                "box-shadow": self._effects.SHADOW_NORMAL,
            },
        }

    def _get_tab_button_styles(self) -> Dict[str, Dict[str, str]]:
        """Get tab button component styles for all variants."""
        return {
            "default": {
                "background-color": "transparent",
                "border": "none",
                "border-bottom": f"2px solid transparent",
                "padding": "12px 20px",
                "color": self._colors.TEXT_MUTED,
                "font-weight": "500",
                "transition": self._effects.TRANSITION_FAST,
            },
            "accent": {
                "background-color": self._colors.GLASS_BASE,
                "border": "none",
                "border-bottom": f"2px solid {self._colors.ACCENT_BORDER}",
                "padding": "12px 20px",
                "color": self._colors.TEXT_PRIMARY,
                "font-weight": "600",
                "transition": self._effects.TRANSITION_FAST,
            },
        }

    def _get_menu_bar_styles(self) -> Dict[str, Dict[str, str]]:
        """Get menu bar component styles."""
        return {
            "default": {
                "background-color": self._colors.GLASS_BASE,
                "border-bottom": f"1px solid {self._colors.BORDER_SUBTLE}",
                "padding": "8px 16px",
                "box-shadow": self._effects.SHADOW_SUBTLE,
            },
        }

    def _get_tab_container_styles(self) -> Dict[str, Dict[str, str]]:
        """Get tab container component styles."""
        return {
            "default": {
                "background-color": self._colors.GLASS_BASE,
                "border": f"1px solid {self._colors.BORDER_SUBTLE}",
                "border-radius": self._effects.RADIUS_LARGE,
                "box-shadow": self._effects.SHADOW_NORMAL,
            },
        }

    def _get_panel_styles(self) -> Dict[str, Dict[str, str]]:
        """Get panel component styles for all variants."""
        return {
            "default": {
                "background-color": self._colors.GLASS_BASE,
                "border": f"1px solid {self._colors.BORDER_SUBTLE}",
                "border-radius": self._effects.RADIUS_MEDIUM,
                "padding": self._effects.PADDING_LARGE,
                "box-shadow": self._effects.SHADOW_SUBTLE,
            },
            "accent": {
                "background-color": self._colors.ACCENT_BASE,
                "border": f"1px solid {self._colors.ACCENT_BORDER}",
                "border-radius": self._effects.RADIUS_MEDIUM,
                "padding": self._effects.PADDING_LARGE,
                "box-shadow": self._effects.SHADOW_ACCENT,
            },
            "subtle": {
                "background-color": "rgba(255, 255, 255, 0.05)",
                "border": f"1px solid {self._colors.BORDER_SUBTLE}",
                "border-radius": self._effects.RADIUS_MEDIUM,
                "padding": self._effects.PADDING_LARGE,
            },
        }

    def _get_dialog_styles(self) -> Dict[str, Dict[str, str]]:
        """Get dialog component styles."""
        return {
            "default": {
                "background-color": self._colors.GLASS_LIGHT,
                "border": f"1px solid {self._colors.BORDER_NORMAL}",
                "border-radius": self._effects.RADIUS_LARGE,
                "padding": "24px",
                "box-shadow": "0 8px 32px rgba(0, 0, 0, 0.2)",
            },
        }

    def _get_container_styles(self) -> Dict[str, Dict[str, str]]:
        """Get container component styles."""
        return {
            "default": {
                "background-color": "transparent",
                "padding": "16px",
            },
            "glass": {
                "background-color": self._colors.GLASS_BASE,
                "border": f"1px solid {self._colors.BORDER_SUBTLE}",
                "border-radius": self._effects.RADIUS_MEDIUM,
                "padding": "16px",
            },
        }

    def _get_input_styles(self) -> Dict[str, Dict[str, str]]:
        """Get input component styles for all variants."""
        return {
            "default": {
                "background-color": self._colors.GLASS_BASE,
                "border": f"1px solid {self._colors.BORDER_SUBTLE}",
                "border-radius": self._effects.RADIUS_MEDIUM,
                "padding": "8px 12px",
                "color": self._colors.TEXT_PRIMARY,
                "font-size": "14px",
                "transition": self._effects.TRANSITION_NORMAL,
            },
            "accent": {
                "background-color": self._colors.GLASS_BASE,
                "border": f"2px solid {self._colors.ACCENT_BORDER}",
                "border-radius": self._effects.RADIUS_MEDIUM,
                "padding": "8px 12px",
                "color": self._colors.TEXT_PRIMARY,
                "font-size": "14px",
                "transition": self._effects.TRANSITION_NORMAL,
                "box-shadow": self._effects.SHADOW_ACCENT,
            },
        }

    def _get_checkbox_styles(self) -> Dict[str, Dict[str, str]]:
        """Get checkbox component styles."""
        return {
            "default": {
                "background-color": self._colors.GLASS_BASE,
                "border": f"2px solid {self._colors.BORDER_NORMAL}",
                "border-radius": "4px",
                "width": "18px",
                "height": "18px",
                "transition": self._effects.TRANSITION_FAST,
            },
        }

    def _get_slider_styles(self) -> Dict[str, Dict[str, str]]:
        """Get slider component styles."""
        return {
            "default": {
                "background-color": self._colors.GLASS_BASE,
                "border": f"1px solid {self._colors.BORDER_SUBTLE}",
                "border-radius": "10px",
                "height": "4px",
            },
        }

    def _get_label_styles(self) -> Dict[str, Dict[str, str]]:
        """Get label component styles for all variants."""
        return {
            "default": {
                "color": self._colors.TEXT_PRIMARY,
                "font-size": "14px",
                "font-weight": "400",
            },
            "accent": {
                "color": self._colors.TEXT_PRIMARY,
                "font-size": "14px",
                "font-weight": "600",
            },
            "muted": {
                "color": self._colors.TEXT_MUTED,
                "font-size": "12px",
                "font-weight": "400",
            },
            "prominent": {
                "color": self._colors.TEXT_PRIMARY,
                "font-size": "16px",
                "font-weight": "700",
            },
        }

    def _get_card_styles(self) -> Dict[str, Dict[str, str]]:
        """Get card component styles for all variants."""
        return {
            "default": {
                "background-color": self._colors.GLASS_BASE,
                "border": f"1px solid {self._colors.BORDER_SUBTLE}",
                "border-radius": self._effects.RADIUS_LARGE,
                "padding": "16px",
                "box-shadow": self._effects.SHADOW_SUBTLE,
                "transition": self._effects.TRANSITION_NORMAL,
            },
            "accent": {
                "background-color": self._colors.ACCENT_BASE,
                "border": f"1px solid {self._colors.ACCENT_BORDER}",
                "border-radius": self._effects.RADIUS_LARGE,
                "padding": "16px",
                "box-shadow": self._effects.SHADOW_ACCENT,
                "transition": self._effects.TRANSITION_NORMAL,
            },
        }

    def _get_list_item_styles(self) -> Dict[str, Dict[str, str]]:
        """Get list item component styles."""
        return {
            "default": {
                "background-color": "transparent",
                "padding": "8px 12px",
                "border-bottom": f"1px solid {self._colors.BORDER_SUBTLE}",
                "color": self._colors.TEXT_PRIMARY,
                "transition": self._effects.TRANSITION_FAST,
            },
            "accent": {
                "background-color": self._colors.ACCENT_BASE,
                "padding": "8px 12px",
                "border-bottom": f"1px solid {self._colors.ACCENT_BORDER}",
                "color": self._colors.TEXT_PRIMARY,
                "transition": self._effects.TRANSITION_FAST,
            },
        }

    def _get_overlay_styles(self) -> Dict[str, Dict[str, str]]:
        """Get overlay component styles."""
        return {
            "default": {
                "background-color": "rgba(0, 0, 0, 0.4)",
            },
        }

    def _get_tooltip_styles(self) -> Dict[str, Dict[str, str]]:
        """Get tooltip component styles."""
        return {
            "default": {
                "background-color": "rgba(0, 0, 0, 0.8)",
                "border": f"1px solid {self._colors.BORDER_SUBTLE}",
                "border-radius": self._effects.RADIUS_SMALL,
                "padding": "6px 10px",
                "color": self._colors.TEXT_PRIMARY,
                "font-size": "12px",
                "box-shadow": self._effects.SHADOW_NORMAL,
            },
        }

    def _get_sequence_viewer_styles(self) -> Dict[str, Dict[str, str]]:
        """Get sequence viewer component styles."""
        return {
            "default": {
                "background-color": self._colors.GLASS_BASE,
                "border": f"1px solid {self._colors.BORDER_SUBTLE}",
                "border-radius": self._effects.RADIUS_LARGE,
                "padding": "20px",
                "box-shadow": self._effects.SHADOW_NORMAL,
            },
        }

    # Utility methods for common styling needs
    def get_color(self, color_name: str) -> str:
        """Get a color value by name from the color palette."""
        return getattr(self._colors, color_name.upper(), self._colors.TEXT_PRIMARY)

    def get_effect(self, effect_name: str) -> str:
        """Get an effect value by name from the effects collection."""
        return getattr(self._effects, effect_name.upper(), "")

    def create_hover_style(self, base_style: str) -> str:
        """Create a hover variant of a base style with enhanced effects."""
        # This is a simplified version - could be expanded for more sophisticated hover effects
        hover_additions = f"""
            background-color: {self._colors.GLASS_LIGHT};
            box-shadow: {self._effects.SHADOW_NORMAL};
            transform: translateY(-1px);
        """
        return f"{base_style} {hover_additions}"


# Global design system instance
_design_system_instance: Optional[DesignSystem] = None


@lru_cache(maxsize=1)
def get_design_system() -> DesignSystem:
    """
    Get the global design system instance.

    This function ensures there's only one design system instance throughout
    the application lifecycle, providing consistency and performance.

    Returns:
        The global DesignSystem instance
    """
    global _design_system_instance
    if _design_system_instance is None:
        _design_system_instance = DesignSystem()
    return _design_system_instance


def reset_design_system() -> None:
    """
    Reset the global design system instance.

    This is mainly useful for testing or when configuration changes require
    a fresh design system instance.
    """
    global _design_system_instance
    _design_system_instance = None
    get_design_system.cache_clear()


# Convenience functions for quick styling
def get_button_style(variant: StyleVariant = StyleVariant.DEFAULT, **kwargs) -> str:
    """Quick function to get button styling."""
    return get_design_system().create_component_style(
        ComponentType.BUTTON, variant, **kwargs
    )


def get_panel_style(variant: StyleVariant = StyleVariant.DEFAULT, **kwargs) -> str:
    """Quick function to get panel styling."""
    return get_design_system().create_component_style(
        ComponentType.PANEL, variant, **kwargs
    )


def get_label_style(variant: StyleVariant = StyleVariant.DEFAULT, **kwargs) -> str:
    """Quick function to get label styling."""
    return get_design_system().create_component_style(
        ComponentType.LABEL, variant, **kwargs
    )
