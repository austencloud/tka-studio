"""
Start Position UI Service

Handles UI state management and layout calculations for start position components.
Extracts UI logic from presentation components while keeping it separate from business logic.
"""

from __future__ import annotations

import logging
from typing import Any

from desktop.modern.core.interfaces.start_position_services import (
    IStartPositionUIService,
)


try:
    from PyQt6.QtCore import QSize
except ImportError:
    # Mock QSize for environments without PyQt6
    class QSize:
        def __init__(self, width=0, height=0):
            self._width = width
            self._height = height

        def width(self):
            return self._width

        def height(self):
            return self._height


logger = logging.getLogger(__name__)


class StartPositionUIService(IStartPositionUIService):
    """
    Service for managing start position UI state and layout calculations.

    Responsibilities:
    - Calculating optimal sizes for position option components
    - Managing grid layout configurations
    - Providing responsive layout parameters
    - Handling UI state for different picker modes
    """

    # Start position configurations (matching the presentation layer constants)
    DIAMOND_START_POSITIONS = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
    BOX_START_POSITIONS = ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]

    # Advanced picker positions (16 positions like legacy) - CORRECTED
    DIAMOND_ADVANCED_POSITIONS = [
        "alpha1_alpha1",
        "alpha3_alpha3",
        "alpha5_alpha5",
        "alpha7_alpha7",
        "beta1_beta1",
        "beta3_beta3",
        "beta5_beta5",
        "beta7_beta7",
        "gamma1_gamma1",
        "gamma3_gamma3",
        "gamma5_gamma5",
        "gamma7_gamma7",
        "gamma9_gamma9",
        "gamma11_gamma11",
        "gamma13_gamma13",
        "gamma15_gamma15",
    ]

    BOX_ADVANCED_POSITIONS = [
        "alpha2_alpha2",
        "alpha4_alpha4",
        "alpha6_alpha6",
        "alpha8_alpha8",
        "beta2_beta2",
        "beta4_beta4",
        "beta6_beta6",
        "beta8_beta8",
        "gamma2_gamma2",
        "gamma4_gamma4",
        "gamma6_gamma6",
        "gamma8_gamma8",
        "gamma10_gamma10",
        "gamma12_gamma12",
        "gamma14_gamma14",
        "gamma16_gamma16",
    ]

    def __init__(self):
        """Initialize the start position UI service."""
        logger.debug("StartPositionUIService initialized")

    def calculate_option_size(
        self, container_width: int, is_advanced: bool = False
    ) -> int:
        """
        Calculate the appropriate size for start position options.

        Args:
            container_width: Width of the container
            is_advanced: True for advanced picker, False for basic

        Returns:
            Size in pixels for the option components
        """
        try:
            # Improved sizing formula for better space utilization
            if is_advanced:
                # Advanced picker: size for 4x4 grid to fit in available space
                # Account for spacing and margins in the calculation
                spacing_total = 10 * 3  # 3 gaps between 4 items (reduced spacing)
                margin_total = 8 * 2  # margins on both sides (reduced margins)
                available_width = container_width - spacing_total - margin_total
                size = available_width // 4  # Divide by 4 for 4 columns
                min_size = 80  # Smaller minimum for better fit
                max_size = 150  # Smaller maximum to prevent overflow
            else:
                # Regular picker: size for 3 items in a row
                spacing_total = 15 * 2  # 2 gaps between 3 items (reduced spacing)
                margin_total = 12 * 2  # margins on both sides (reduced margins)
                available_width = container_width - spacing_total - margin_total
                size = available_width // 3  # Divide by 3 for 3 columns
                min_size = 100
                max_size = 200

            # Ensure reasonable size range
            size = max(size, min_size)
            size = min(size, max_size)

            logger.debug(
                f"Calculated option size: {size}px (advanced={is_advanced}, container={container_width}px)"
            )
            return size

        except Exception as e:
            logger.error(f"Error calculating option size: {e}")
            # Safe fallback
            return 80 if is_advanced else 100

    def get_grid_layout_config(
        self, grid_mode: str, is_advanced: bool = False
    ) -> dict[str, Any]:
        """
        Get grid layout configuration for positioning options.

        Args:
            grid_mode: Grid mode ("diamond" or "box")
            is_advanced: True for advanced picker, False for basic

        Returns:
            Dictionary with layout configuration
        """
        try:
            if is_advanced:
                # Advanced picker: 4x4 grid layout with reduced spacing
                config = {
                    "rows": 4,
                    "cols": 4,
                    "spacing": 10,  # Reduced from 15 to fit better
                    "margin": 8,  # Reduced from 12 to fit better
                    "fixed_layout": True,
                    "position_count": 16,
                }
            else:
                # Basic picker: responsive layout for 3 positions
                config = {
                    "rows": 1,  # Prefer single row if space allows
                    "cols": 3,
                    "spacing": 15,  # Reduced from 20
                    "margin": 12,  # Reduced from 18
                    "fixed_layout": False,  # Responsive layout
                    "position_count": 3,
                }

            config["grid_mode"] = grid_mode
            config["is_advanced"] = is_advanced

            logger.debug(f"Generated grid layout config: {config}")
            return config

        except Exception as e:
            logger.error(f"Error generating grid layout config: {e}")
            # Safe fallback
            return {
                "rows": 1,
                "cols": 3,
                "spacing": 15,
                "margin": 12,
                "fixed_layout": False,
                "position_count": 3,
                "grid_mode": grid_mode,
                "is_advanced": is_advanced,
            }

    def get_positions_for_mode(
        self, grid_mode: str, is_advanced: bool = False
    ) -> list[str]:
        """
        Get the list of positions to display for a given mode.

        Args:
            grid_mode: Grid mode ("diamond" or "box")
            is_advanced: True for 16 positions, False for 3 positions

        Returns:
            List of position keys to display
        """
        try:
            if is_advanced:
                # Advanced picker shows 16 positions
                if grid_mode == "diamond":
                    positions = self.DIAMOND_ADVANCED_POSITIONS
                else:
                    positions = self.BOX_ADVANCED_POSITIONS
            # Basic picker shows 3 positions
            elif grid_mode == "diamond":
                positions = self.DIAMOND_START_POSITIONS
            else:
                positions = self.BOX_START_POSITIONS

            logger.debug(
                f"Retrieved {len(positions)} positions for {grid_mode} mode (advanced={is_advanced})"
            )
            return positions.copy()  # Return a copy to prevent modification

        except Exception as e:
            logger.error(f"Error getting positions for mode {grid_mode}: {e}")
            # Safe fallback - basic diamond positions
            return self.DIAMOND_START_POSITIONS.copy()

    def calculate_responsive_layout(
        self, container_size: QSize, position_count: int
    ) -> dict[str, Any]:
        """
        Calculate responsive layout parameters for position options.

        Args:
            container_size: Size of the container widget
            position_count: Number of positions to display

        Returns:
            Dictionary with layout parameters (rows, cols, spacing, etc.)
        """
        try:
            container_width = container_size.width()
            container_height = container_size.height()

            # Calculate option size
            is_advanced = position_count > 3
            option_size = self.calculate_option_size(container_width, is_advanced)

            # Calculate spacing and margins
            spacing = 20 if not is_advanced else 15
            margin = 18 if not is_advanced else 12

            # Calculate how many columns can fit
            available_width = container_width - (2 * margin)
            max_cols = max(1, available_width // (option_size + spacing))

            if is_advanced:
                # Advanced picker: prefer 4x4 grid, but adapt if needed
                if max_cols >= 4:
                    cols = 4
                    rows = 4
                elif max_cols >= 2:
                    cols = max_cols
                    rows = (position_count + cols - 1) // cols
                else:
                    cols = 1
                    rows = position_count
            # Basic picker: prefer single row, but adapt if needed
            elif max_cols >= position_count:
                cols = position_count
                rows = 1
            else:
                cols = max_cols
                rows = (position_count + cols - 1) // cols

            layout_params = {
                "rows": rows,
                "cols": cols,
                "option_size": option_size,
                "spacing": spacing,
                "margin": margin,
                "container_width": container_width,
                "container_height": container_height,
                "position_count": position_count,
                "is_advanced": is_advanced,
            }

            logger.debug(f"Calculated responsive layout: {layout_params}")
            return layout_params

        except Exception as e:
            logger.error(f"Error calculating responsive layout: {e}")
            # Safe fallback
            return {
                "rows": 1,
                "cols": min(position_count, 3),
                "option_size": 100,
                "spacing": 15,
                "margin": 12,
                "container_width": container_size.width(),
                "container_height": container_size.height(),
                "position_count": position_count,
                "is_advanced": False,
            }

    def should_use_single_row_layout(
        self, container_width: int, position_count: int, option_size: int, spacing: int
    ) -> bool:
        """
        Determine if positions should be laid out in a single row.

        Args:
            container_width: Available container width
            position_count: Number of positions to display
            option_size: Size of each option
            spacing: Spacing between options

        Returns:
            True if single row layout is optimal, False otherwise
        """
        try:
            # Calculate total width needed for single row
            total_width_needed = (position_count * option_size) + (
                (position_count - 1) * spacing
            )

            # Add some buffer for margins
            buffer = 100

            result = (total_width_needed + buffer) <= container_width
            logger.debug(
                f"Single row layout check: needed={total_width_needed}, available={container_width}, use_single_row={result}"
            )

            return result

        except Exception as e:
            logger.error(f"Error checking single row layout: {e}")
            return position_count <= 3  # Safe fallback

    def get_layout_style_config(self, is_advanced: bool = False) -> dict[str, str]:
        """
        Get style configuration for layout components.

        Args:
            is_advanced: True for advanced picker styling, False for basic

        Returns:
            Dictionary with style configuration
        """
        try:
            if is_advanced:
                # Advanced picker has denser layout
                return {
                    "container_style": "background: rgba(255,255,255,0.15); border-radius: 24px;",
                    "scroll_style": "background: transparent; border: none;",
                    "option_spacing": "12px",
                    "container_padding": "12px",
                }
            # Basic picker has more spacious layout
            return {
                "container_style": "background: rgba(255,255,255,0.18); border-radius: 28px;",
                "scroll_style": "background: transparent; border: none; border-radius: 16px;",
                "option_spacing": "20px",
                "container_padding": "18px",
            }

        except Exception as e:
            logger.error(f"Error getting layout style config: {e}")
            # Safe fallback
            return {
                "container_style": "background: rgba(255,255,255,0.18); border-radius: 24px;",
                "scroll_style": "background: transparent; border: none;",
                "option_spacing": "15px",
                "container_padding": "15px",
            }
