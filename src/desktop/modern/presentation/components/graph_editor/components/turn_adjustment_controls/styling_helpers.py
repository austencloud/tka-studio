"""
Unified Styling Helpers for TKA Graph Editor Components
======================================================

Provides consistent glassmorphism styling across orientation pickers
and turn adjustment controls with modern 2025 design principles.
"""

# Unified Design Constants
from __future__ import annotations


UNIFIED_BUTTON_WIDTH = 75
UNIFIED_BUTTON_HEIGHT = 55
UNIFIED_BORDER_RADIUS = 10
UNIFIED_BUTTON_SPACING = 10
UNIFIED_PANEL_BORDER_RADIUS = 12


def get_unified_color_scheme(color: str) -> dict:
    """Get unified color scheme for consistent theming."""
    if color == "blue":
        return {
            "base_rgb": "74, 144, 226",
            "hover_rgb": "94, 164, 246",
            "gradient_start": "rgba(74, 144, 226, 0.5)",
            "gradient_end": "rgba(74, 144, 226, 0.2)",
            "border_color": "rgba(74, 144, 226, 0.6)",
        }
    # red
    return {
        "base_rgb": "231, 76, 60",
        "hover_rgb": "251, 96, 80",
        "gradient_start": "rgba(231, 76, 60, 0.5)",
        "gradient_end": "rgba(231, 76, 60, 0.2)",
        "border_color": "rgba(231, 76, 60, 0.6)",
    }


def apply_modern_panel_styling(panel, color):
    """Apply unified modern glassmorphism styling to panels."""
    colors = get_unified_color_scheme(color)

    panel.setStyleSheet(
        f"""
        QGroupBox {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors["gradient_start"]},
                stop:1 {colors["gradient_end"]});
            border: 2px solid {colors["border_color"]};
            border-radius: {UNIFIED_PANEL_BORDER_RADIUS}px;
            margin-top: 0px;
            padding-top: 8px;
            font-weight: bold;
            font-size: 12px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }}
        """
    )


def apply_unified_button_styling(button, color, button_type="standard"):
    """Apply unified button styling for consistent appearance across components."""
    colors = get_unified_color_scheme(color)

    # Adjust font size based on button type
    font_size = 14 if button_type == "turn_value" else 12

    button.setStyleSheet(
        f"""
        QPushButton {{
            background: rgba({colors["base_rgb"]}, 0.4);
            border: 2px solid rgba({colors["base_rgb"]}, 0.6);
            border-radius: {UNIFIED_BORDER_RADIUS}px;
            color: rgba(255, 255, 255, 0.95);
            font-size: {font_size}px;
            font-weight: bold;
            padding: 8px;
        }}
        QPushButton:hover {{
            background: rgba({colors["hover_rgb"]}, 0.5);
            border-color: rgba({colors["hover_rgb"]}, 0.8);
            color: rgba(255, 255, 255, 1.0);
        }}
        QPushButton:pressed {{
            background: rgba({colors["base_rgb"]}, 0.6);
            border-color: rgba({colors["base_rgb"]}, 1.0);
        }}
        QPushButton:checked {{
            background: rgba({colors["base_rgb"]}, 0.8);
            border-color: rgba({colors["base_rgb"]}, 1.0);
            color: rgba(255, 255, 255, 1.0);
            font-weight: bold;
        }}
        """
    )


# Backward compatibility alias
def apply_turn_button_styling(button, color, turn_value):
    """Legacy function for backward compatibility."""
    apply_unified_button_styling(button, color, "turn_value")
