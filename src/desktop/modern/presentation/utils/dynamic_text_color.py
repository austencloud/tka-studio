"""
Dynamic text color utility for ensuring readable text on any background.

This utility provides simple, reliable methods to automatically adjust text color
based on the background color to ensure optimal readability.
"""

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QWidget


def calculate_luminance(color: QColor | tuple[int, int, int]) -> float:
    """
    Calculate the relative luminance of a color using the standard formula.

    Args:
        color: Either a QColor object or (r, g, b) tuple with values 0-255

    Returns:
        Luminance value between 0.0 (black) and 1.0 (white)
    """
    if isinstance(color, QColor):
        r, g, b = color.red(), color.green(), color.blue()
    else:
        r, g, b = color

    # Convert to 0-1 range and apply gamma correction
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0

    # Apply gamma correction
    r_linear = (
        r_norm / 12.92 if r_norm <= 0.03928 else pow((r_norm + 0.055) / 1.055, 2.4)
    )
    g_linear = (
        g_norm / 12.92 if g_norm <= 0.03928 else pow((g_norm + 0.055) / 1.055, 2.4)
    )
    b_linear = (
        b_norm / 12.92 if b_norm <= 0.03928 else pow((b_norm + 0.055) / 1.055, 2.4)
    )

    # Calculate luminance using ITU-R BT.709 coefficients
    return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear


def get_contrasting_text_color(
    background_color: QColor | tuple[int, int, int], threshold: float = 0.5
) -> str:
    """
    Get a contrasting text color (black or white) based on background luminance.

    Args:
        background_color: Background color as QColor or (r, g, b) tuple
        threshold: Luminance threshold (0.0-1.0). Higher values favor black text.

    Returns:
        Hex color string ("#000000" or "#FFFFFF")
    """
    luminance = calculate_luminance(background_color)

    # Return black text for light backgrounds, white text for dark backgrounds
    return "#000000" if luminance > threshold else "#FFFFFF"


def get_widget_background_color(widget: QWidget) -> QColor:
    """
    Get the effective background color of a widget.

    Args:
        widget: The widget to analyze

    Returns:
        QColor representing the widget's background
    """
    # Try to get the background color from the palette
    palette = widget.palette()
    background_color = palette.color(QPalette.ColorRole.Window)

    # If the background is fully transparent, get parent's background
    if background_color.alpha() == 0:
        parent = widget.parent()
        if parent and isinstance(parent, QWidget):
            return get_widget_background_color(parent)

    return background_color


def get_glassmorphism_text_color(
    widget: QWidget,
    glassmorphism_base_color: tuple[int, int, int] = (255, 255, 255),
    glassmorphism_opacity: float = 0.2,
) -> str:
    """
    Get contrasting text color for glassmorphism backgrounds.

    Args:
        widget: The widget with glassmorphism background
        glassmorphism_base_color: Base color of glassmorphism effect (default: white)
        glassmorphism_opacity: Opacity of glassmorphism effect (0.0-1.0)

    Returns:
        Hex color string for optimal text contrast
    """
    # Get the parent's background color
    parent_bg = get_widget_background_color(widget)

    # Simulate the glassmorphism effect by blending colors
    pr, pg, pb = parent_bg.red(), parent_bg.green(), parent_bg.blue()
    gr, gg, gb = glassmorphism_base_color

    # Blend colors based on opacity
    blended_r = int(pr * (1 - glassmorphism_opacity) + gr * glassmorphism_opacity)
    blended_g = int(pg * (1 - glassmorphism_opacity) + gg * glassmorphism_opacity)
    blended_b = int(pb * (1 - glassmorphism_opacity) + gb * glassmorphism_opacity)

    return get_contrasting_text_color((blended_r, blended_g, blended_b))


def apply_dynamic_text_color(
    widget: QWidget,
    background_color: QColor | tuple[int, int, int] | None = None,
    threshold: float = 0.5,
) -> str:
    """
    Apply dynamic text color to a widget based on its background.

    Args:
        widget: The widget to apply the color to
        background_color: Specific background color to use (optional)
        threshold: Luminance threshold for color selection

    Returns:
        The applied color as hex string
    """
    if background_color is None:
        background_color = get_widget_background_color(widget)

    text_color = get_contrasting_text_color(background_color, threshold)

    # Apply the color via stylesheet
    current_style = widget.styleSheet()

    # Simple approach: set the color property
    if "color:" in current_style:
        # Replace existing color
        import re

        new_style = re.sub(r"color:\s*[^;]+;", f"color: {text_color};", current_style)
    else:
        # Add color property
        new_style = current_style + f" color: {text_color};"

    widget.setStyleSheet(new_style)
    return text_color


class DynamicTextColorMixin:
    """
    Mixin class to add dynamic text color capabilities to QWidget subclasses.
    """

    def update_text_color_for_background(
        self, background_color: QColor | tuple[int, int, int] | None = None
    ):
        """Update text color based on background."""
        if hasattr(self, "styleSheet") and hasattr(self, "setStyleSheet"):
            return apply_dynamic_text_color(self, background_color)

    def set_glassmorphism_text_color(
        self,
        glassmorphism_base_color: tuple[int, int, int] = (255, 255, 255),
        glassmorphism_opacity: float = 0.2,
    ):
        """Set text color optimized for glassmorphism backgrounds."""
        if hasattr(self, "styleSheet") and hasattr(self, "setStyleSheet"):
            text_color = get_glassmorphism_text_color(
                self, glassmorphism_base_color, glassmorphism_opacity
            )
            current_style = self.styleSheet()

            if "color:" in current_style:
                import re

                new_style = re.sub(
                    r"color:\s*[^;]+;", f"color: {text_color};", current_style
                )
            else:
                new_style = current_style + f" color: {text_color};"

            self.setStyleSheet(new_style)
            return text_color
