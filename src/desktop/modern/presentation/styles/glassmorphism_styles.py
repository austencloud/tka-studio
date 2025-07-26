"""
Glassmorphism Style System for TKA Modern UI

Centralized glassmorphism styling system that provides consistent visual elements
across the application. This system maintains the app's modern glass aesthetic
with subtle transparency, blur effects, and elegant interactions.
"""

from typing import Dict, Optional


class GlassmorphismColors:
    """Central color palette for glassmorphism effects."""

    # Base glass colors
    GLASS_BASE = "rgba(255, 255, 255, 0.1)"
    GLASS_LIGHT = "rgba(255, 255, 255, 0.15)"
    GLASS_LIGHTER = "rgba(255, 255, 255, 0.2)"

    # Border colors
    BORDER_SUBTLE = "rgba(255, 255, 255, 0.2)"
    BORDER_NORMAL = "rgba(255, 255, 255, 0.3)"
    BORDER_STRONG = "rgba(255, 255, 255, 0.4)"

    # Accent colors (blue theme)
    ACCENT_BASE = "rgba(64, 150, 255, 0.3)"
    ACCENT_HOVER = "rgba(64, 150, 255, 0.4)"
    ACCENT_ACTIVE = "rgba(64, 150, 255, 0.5)"
    ACCENT_BORDER = "rgba(64, 150, 255, 0.5)"
    ACCENT_BORDER_HOVER = "rgba(64, 150, 255, 0.6)"

    # Text colors
    TEXT_PRIMARY = "rgba(255, 255, 255, 1.0)"
    TEXT_SECONDARY = "rgba(255, 255, 255, 0.9)"
    TEXT_MUTED = "rgba(255, 255, 255, 0.8)"
    TEXT_DISABLED = "rgba(255, 255, 255, 0.4)"

    # Shadow colors
    SHADOW_SUBTLE = "rgba(0, 0, 0, 0.1)"
    SHADOW_NORMAL = "rgba(0, 0, 0, 0.15)"
    SHADOW_ACCENT = "rgba(64, 150, 255, 0.2)"
    SHADOW_ACCENT_HOVER = "rgba(64, 150, 255, 0.25)"


class GlassmorphismEffects:
    """Standardized glassmorphism effects and properties."""

    # Border radius values
    RADIUS_SMALL = "8px"
    RADIUS_MEDIUM = "10px"
    RADIUS_LARGE = "12px"
    RADIUS_XLARGE = "16px"

    # Padding values
    PADDING_SMALL = "8px 12px"
    PADDING_MEDIUM = "12px 16px"
    PADDING_LARGE = "16px 24px"

    # Margin values
    MARGIN_TINY = "1px"
    MARGIN_SMALL = "2px"
    MARGIN_MEDIUM = "4px"
    MARGIN_LARGE = "8px"

    # Shadow effects
    SHADOW_SUBTLE = f"0 2px 8px {GlassmorphismColors.SHADOW_SUBTLE}"
    SHADOW_NORMAL = f"0 4px 12px {GlassmorphismColors.SHADOW_NORMAL}"
    SHADOW_ACCENT = f"0 4px 15px {GlassmorphismColors.SHADOW_ACCENT}"
    SHADOW_ACCENT_HOVER = f"0 6px 20px {GlassmorphismColors.SHADOW_ACCENT_HOVER}"

    # Transitions
    TRANSITION_FAST = "all 0.15s ease"
    TRANSITION_NORMAL = "all 0.2s ease"
    TRANSITION_SLOW = "all 0.3s ease"


class GlassmorphismStyleGenerator:
    """Utility class for generating consistent glassmorphism styles."""

    @staticmethod
    def create_button_style(
        variant: str = "default",
        size: str = "medium",
        custom_properties: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Generate glassmorphism button styling.

        Args:
            variant: Button variant ('default', 'accent', 'subtle')
            size: Button size ('small', 'medium', 'large')
            custom_properties: Optional custom CSS properties

        Returns:
            CSS string for the button
        """
        # Base properties
        base_properties = {
            "border-radius": GlassmorphismEffects.RADIUS_MEDIUM,
            "font-weight": "500",
            "text-align": "center",
            "transition": GlassmorphismEffects.TRANSITION_NORMAL,
        }

        # Size-specific properties
        size_properties = {
            "small": {
                "padding": GlassmorphismEffects.PADDING_SMALL,
                "font-size": "12px",
                "min-height": "32px",
                "max-height": "32px",
            },
            "medium": {
                "padding": GlassmorphismEffects.PADDING_MEDIUM,
                "font-size": "13px",
                "min-height": "48px",
                "max-height": "48px",
            },
            "large": {
                "padding": GlassmorphismEffects.PADDING_LARGE,
                "font-size": "14px",
                "min-height": "56px",
                "max-height": "56px",
            },
        }

        # Variant-specific properties
        if variant == "accent":
            normal_bg = GlassmorphismColors.ACCENT_BASE
            normal_border = GlassmorphismColors.ACCENT_BORDER
            hover_bg = GlassmorphismColors.ACCENT_HOVER
            hover_border = GlassmorphismColors.ACCENT_BORDER_HOVER
            text_color = GlassmorphismColors.TEXT_PRIMARY
            shadow = GlassmorphismEffects.SHADOW_ACCENT
            hover_shadow = GlassmorphismEffects.SHADOW_ACCENT_HOVER
        elif variant == "subtle":
            normal_bg = GlassmorphismColors.GLASS_BASE
            normal_border = GlassmorphismColors.BORDER_SUBTLE
            hover_bg = GlassmorphismColors.GLASS_LIGHT
            hover_border = GlassmorphismColors.BORDER_NORMAL
            text_color = GlassmorphismColors.TEXT_MUTED
            shadow = GlassmorphismEffects.SHADOW_SUBTLE
            hover_shadow = GlassmorphismEffects.SHADOW_NORMAL
        else:  # default
            normal_bg = GlassmorphismColors.GLASS_BASE
            normal_border = GlassmorphismColors.BORDER_NORMAL
            hover_bg = GlassmorphismColors.GLASS_LIGHT
            hover_border = GlassmorphismColors.BORDER_STRONG
            text_color = GlassmorphismColors.TEXT_SECONDARY
            shadow = GlassmorphismEffects.SHADOW_SUBTLE
            hover_shadow = GlassmorphismEffects.SHADOW_NORMAL

        # Merge all properties
        properties = {
            **base_properties,
            **size_properties.get(size, size_properties["medium"]),
        }
        if custom_properties:
            properties.update(custom_properties)

        # Generate CSS
        css_properties = []
        for prop, value in properties.items():
            css_properties.append(f"{prop}: {value};")

        return f"""
        QPushButton {{
            background: {normal_bg};
            border: 1px solid {normal_border};
            color: {text_color};
            {' '.join(css_properties)}
            margin: {GlassmorphismEffects.MARGIN_SMALL};
        }}
        
        QPushButton:hover {{
            background: {hover_bg};
            border: 1px solid {hover_border};
            color: {GlassmorphismColors.TEXT_PRIMARY};
        }}
        
        QPushButton:pressed {{
            background: {GlassmorphismColors.GLASS_LIGHTER};
        }}
        
        QPushButton:disabled {{
            background: {GlassmorphismColors.GLASS_BASE};
            border: 1px solid {GlassmorphismColors.BORDER_SUBTLE};
            color: {GlassmorphismColors.TEXT_DISABLED};
        }}
        """

    @staticmethod
    def create_tab_style(active_variant: str = "accent") -> str:
        """
        Generate glassmorphism tab styling.

        Args:
            active_variant: Variant for active tab styling

        Returns:
            CSS string for tabs
        """
        if active_variant == "accent":
            active_bg = GlassmorphismColors.ACCENT_BASE
            active_border = GlassmorphismColors.ACCENT_BORDER
            active_hover_bg = GlassmorphismColors.ACCENT_HOVER
            active_hover_border = GlassmorphismColors.ACCENT_BORDER_HOVER
            active_shadow = GlassmorphismEffects.SHADOW_ACCENT
            active_hover_shadow = GlassmorphismEffects.SHADOW_ACCENT_HOVER
        else:
            active_bg = GlassmorphismColors.GLASS_LIGHT
            active_border = GlassmorphismColors.BORDER_STRONG
            active_hover_bg = GlassmorphismColors.GLASS_LIGHTER
            active_hover_border = GlassmorphismColors.BORDER_STRONG
            active_shadow = GlassmorphismEffects.SHADOW_NORMAL
            active_hover_shadow = GlassmorphismEffects.SHADOW_NORMAL

        return f"""
        QPushButton {{
            background: {GlassmorphismColors.GLASS_BASE};
            border: 1px solid {GlassmorphismColors.BORDER_NORMAL};
            border-radius: {GlassmorphismEffects.RADIUS_MEDIUM};
            color: {GlassmorphismColors.TEXT_SECONDARY};
            font-size: 13px;
            font-weight: 500;
            padding: {GlassmorphismEffects.PADDING_MEDIUM};
            margin: {GlassmorphismEffects.MARGIN_SMALL};
            text-align: center;
            min-height: 48px;
            max-height: 48px;
        }}
        
        QPushButton:hover {{
            background: {GlassmorphismColors.GLASS_LIGHT};
            border: 1px solid {GlassmorphismColors.BORDER_STRONG};
            color: {GlassmorphismColors.TEXT_PRIMARY};
        }}
        
        QPushButton:checked {{
            background: {active_bg};
            border: 1px solid {active_border};
            color: {GlassmorphismColors.TEXT_PRIMARY};
            font-weight: 600;
        }}
        
        QPushButton:checked:hover {{
            background: {active_hover_bg};
            border: 1px solid {active_hover_border};
        }}
        
        QPushButton:pressed {{
            background: {GlassmorphismColors.GLASS_LIGHTER};
        }}
        """

    @staticmethod
    def create_container_style(
        variant: str = "default",
        blur_effect: bool = True,
        custom_properties: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Generate glassmorphism container styling.

        Args:
            variant: Container variant ('default', 'subtle', 'prominent')
            blur_effect: Whether to include backdrop blur effect
            custom_properties: Optional custom CSS properties

        Returns:
            CSS string for the container
        """
        base_properties = {
            "border-radius": GlassmorphismEffects.RADIUS_LARGE,
            "margin": GlassmorphismEffects.MARGIN_MEDIUM,
        }

        if variant == "subtle":
            background = "rgba(255, 255, 255, 0.05)"
            border = "rgba(255, 255, 255, 0.1)"
        elif variant == "prominent":
            background = "rgba(255, 255, 255, 0.15)"
            border = "rgba(255, 255, 255, 0.3)"
        else:  # default
            background = "rgba(255, 255, 255, 0.1)"
            border = "rgba(255, 255, 255, 0.2)"

        blur_css = "backdrop-filter: blur(10px);" if blur_effect else ""

        if custom_properties:
            base_properties.update(custom_properties)

        css_properties = []
        for prop, value in base_properties.items():
            css_properties.append(f"{prop}: {value};")

        return f"""
        QWidget {{
            background: {background};
            border: 1px solid {border};
            {' '.join(css_properties)}
            {blur_css}
        }}
        """
