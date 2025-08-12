"""
Graph Editor Configuration Constants
===================================
Centralized configuration for all magic numbers and constants used throughout the graph editor.
"""

from __future__ import annotations


class AnimationConfig:
    """Animation timing and behavior constants"""

    DURATION_MS = 400
    TOGGLE_POSITION_DURATION_MS = 300  # For toggle tab position animation
    EASING_CURVE_TYPE = "OutCubic"
    COOLDOWN_PERIOD_MS = 100
    PROGRESS_TIMER_INTERVAL_MS = 50
    HEIGHT_TOLERANCE_PX = 5  # For preventing micro-adjustments


class LayoutConfig:
    """Layout and sizing constants"""

    PICTOGRAPH_SIZE_RATIO = 1  # Percentage of graph editor height
    PICTOGRAPH_MIN_SIZE = 150
    PICTOGRAPH_BORDER_WIDTH = 4
    PICTOGRAPH_VIEW_RATIO = 0.95  # Percentage of container for view

    # Panel sizing
    PANEL_BORDER_WIDTH = 4
    PANEL_BORDER_RADIUS = 8
    PANEL_PADDING = 8

    # Graph editor sizing
    MIN_WORKBENCH_HEIGHT = 200  # Minimum reasonable workbench height
    PREFERRED_HEIGHT_DIVISOR = 3.5  # workbench_height // 3.5
    PREFERRED_WIDTH_DIVISOR = 4  # workbench_width // 4

    # Container margins and spacing
    CONTAINER_MARGINS = 0
    CONTAINER_SPACING = 0
    MAIN_LAYOUT_MARGINS = 8
    MAIN_LAYOUT_SPACING = 8


class UIConfig:
    """UI component constants"""

    TOGGLE_TAB_MIN_WIDTH = 156
    TOGGLE_TAB_MIN_HEIGHT = 36
    TOGGLE_TAB_MAX_WIDTH = 180
    TOGGLE_TAB_MAX_HEIGHT = 42

    TURN_BUTTON_SIZE = 40
    TURN_BUTTON_HEIGHT = 30
    TURN_DISPLAY_HEIGHT = 40

    # Font sizes
    HAND_INDICATOR_FONT_SIZE = 18
    TURN_DISPLAY_FONT_SIZE = 16
    TOGGLE_TAB_FONT_SIZE = 12
    MOTION_TYPE_FONT_SIZE = 12

    # Initial sizes
    INITIAL_PICTOGRAPH_SIZE = 200
    DEFAULT_WORKBENCH_WIDTH = 800
    DEFAULT_WORKBENCH_HEIGHT = 600

    # Dialog sizes
    TURN_DIALOG_WIDTH = 420
    TURN_DIALOG_HEIGHT = 120
    TURN_BUTTON_WIDTH = 50
    TURN_BUTTON_HEIGHT = 40
    CANCEL_BUTTON_WIDTH = 60
    CANCEL_BUTTON_HEIGHT = 30


class ColorConfig:
    """Color constants for styling"""

    SELECTION_HIGHLIGHT_COLOR = "#FFD700"  # Gold

    # Blue theme
    BLUE_PRIMARY = "#2E3192"
    BLUE_BORDER = "#6496FF"

    # Red theme
    RED_PRIMARY = "#ED1C24"
    RED_BORDER = "#FF6464"

    # Toggle tab gradient
    TOGGLE_GRADIENT_START = "#6a11cb"
    TOGGLE_GRADIENT_END = "#2575fc"
    TOGGLE_GRADIENT_HOVER_START = "#7a21db"
    TOGGLE_GRADIENT_HOVER_END = "#3585fc"
    TOGGLE_GRADIENT_PRESSED_START = "#5a01bb"
    TOGGLE_GRADIENT_PRESSED_END = "#1565ec"

    # Button hover colors
    BUTTON_HOVER_LIGHT = "#f0f0f0"
    BUTTON_PRESSED_LIGHT = "#e0e0e0"

    # Background colors
    PICTOGRAPH_BACKGROUND = "rgba(255, 255, 255, 0.95)"
    GRAPH_EDITOR_GRADIENT_START = "rgba(255, 255, 255, 0.25)"
    GRAPH_EDITOR_GRADIENT_MID = "rgba(255, 255, 255, 0.15)"
    GRAPH_EDITOR_GRADIENT_END = "rgba(255, 255, 255, 0.10)"


class TurnConfig:
    """Turn adjustment constants"""

    MIN_TURN_VALUE = 0.0
    MAX_TURN_VALUE = 3.0
    LEFT_CLICK_INCREMENT = 1.0
    RIGHT_CLICK_INCREMENT = 0.5
    LEFT_CLICK_DECREMENT = -1.0
    RIGHT_CLICK_DECREMENT = -0.5


class StateConfig:
    """State management constants"""

    BEAT_INDEX_INVALID = -1
    MINIMUM_GRAPH_HEIGHT = 100  # Below this, consider collapsed
    WIDTH_SYNC_TOLERANCE = 5  # Pixels - skip micro-adjustments
    RESIZE_TOLERANCE = 10  # Pixels - skip micro-adjustments for resize
    POSITIONING_DEFER_MS = 100  # Milliseconds to defer positioning


class SizeConfig:
    """Size calculation constants"""

    PICTOGRAPH_WIDTH_RATIO = 0.4  # Use 40% of graph editor width
    PICTOGRAPH_HEIGHT_RATIO = 0.85  # Use 85% of graph editor height
    SCALE_FACTOR_PRECISION = 3  # Decimal places for scale factor logging
