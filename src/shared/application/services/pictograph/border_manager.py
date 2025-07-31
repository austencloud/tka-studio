"""
Pictograph Border Service - Pure Business Logic

Handles all border calculations, color determination, and sizing logic
without any Qt dependencies.
"""

import logging

from desktop.modern.core.interfaces.core_services import IPictographBorderManager
from desktop.modern.domain.models import LetterType

logger = logging.getLogger(__name__)


class BorderConfiguration:
    """Configuration for border appearance and calculations."""

    def __init__(
        self,
        width_percentage: float = 0.015,
        minimum_width: int = 1,
        enabled: bool = True,
        primary_color: str = "#000000",
        secondary_color: str = "#000000",
    ):
        self.width_percentage = width_percentage
        self.minimum_width = minimum_width
        self.enabled = enabled
        self.primary_color = primary_color
        self.secondary_color = secondary_color


class BorderDimensions:
    """Border dimension calculations."""

    def __init__(self, outer_width: float, inner_width: float, adjusted_size: int):
        self.outer_width = outer_width
        self.inner_width = inner_width
        self.adjusted_size = adjusted_size


class PictographBorderManager(IPictographBorderManager):
    """
    Pure business service for pictograph border management.

    Handles border calculations, color determination, and sizing logic
    without any Qt dependencies.
    """

    # Letter type to color mapping
    LETTER_TYPE_COLORS = {
        LetterType.TYPE1: ("#36c3ff", "#6F2DA8"),  # Cyan, Purple
        LetterType.TYPE2: ("#6F2DA8", "#6F2DA8"),  # Purple, Purple
        LetterType.TYPE3: ("#26e600", "#6F2DA8"),  # Green, Purple
        LetterType.TYPE4: ("#26e600", "#26e600"),  # Green, Green
        LetterType.TYPE5: ("#00b3ff", "#26e600"),  # Blue, Green
        LetterType.TYPE6: ("#eb7d00", "#eb7d00"),  # Orange, Orange
    }

    # Special colors
    GOLD_COLOR = "#FFD700"
    DEFAULT_COLOR = "#000000"

    def __init__(self):
        """Initialize the border service with default configuration."""
        self._config = BorderConfiguration()
        self._original_primary_color = self.DEFAULT_COLOR
        self._original_secondary_color = self.DEFAULT_COLOR

        logger.debug("Pictograph border service initialized")

    # Border Width Calculations
    def calculate_border_width(self, size: int) -> int:
        """
        Calculate border width based on size using the standard formula.

        Args:
            size: The base size to calculate border width for

        Returns:
            int: The calculated border width
        """
        calculated_width = int(size * self._config.width_percentage)
        return max(self._config.minimum_width, calculated_width)

    def get_border_adjusted_size(self, target_size: int) -> int:
        """
        Get size adjusted for border width.

        Args:
            target_size: The target size before border adjustment

        Returns:
            int: The size adjusted for borders (minimum 50)
        """
        border_width = self.calculate_border_width(target_size)
        adjusted_size = target_size - (2 * border_width)
        return max(50, adjusted_size)  # Minimum viable size

    def calculate_floating_dimensions(self, view_width: int) -> BorderDimensions:
        """
        Calculate floating-point border dimensions for precise drawing.

        Args:
            view_width: Width of the view for calculations

        Returns:
            BorderDimensions: Calculated dimensions for drawing
        """
        # Legacy formula: max(1.0, view_width * 0.016)
        outer_border_width = max(1.0, view_width * 0.016)
        inner_border_width = max(1.0, view_width * 0.016)
        adjusted_size = int(view_width - (2 * outer_border_width))

        return BorderDimensions(
            outer_width=outer_border_width,
            inner_width=inner_border_width,
            adjusted_size=max(50, adjusted_size),
        )

    # Color Management
    def determine_colors_for_letter_type(
        self, letter_type: LetterType
    ) -> tuple[str, str]:
        """
        Determine border colors based on letter type.

        Args:
            letter_type: The letter type to get colors for

        Returns:
            Tuple[str, str]: (primary_color, secondary_color)
        """
        return self.LETTER_TYPE_COLORS.get(
            letter_type, (self.DEFAULT_COLOR, self.DEFAULT_COLOR)
        )

    def apply_letter_type_colors(self, letter_type: LetterType) -> BorderConfiguration:
        """
        Apply colors for a specific letter type and return updated configuration.

        Args:
            letter_type: The letter type to apply colors for

        Returns:
            BorderConfiguration: Updated configuration with new colors
        """
        primary, secondary = self.determine_colors_for_letter_type(letter_type)

        # Store originals for reset capability
        self._original_primary_color = primary
        self._original_secondary_color = secondary

        # Update current configuration
        self._config.primary_color = primary
        self._config.secondary_color = secondary

        logger.debug(f"Applied colors for {letter_type}: {primary}, {secondary}")
        return self._config

    def apply_gold_colors(self) -> BorderConfiguration:
        """
        Apply gold colors (typically used for hover states).

        Returns:
            BorderConfiguration: Updated configuration with gold colors
        """
        self._config.primary_color = self.GOLD_COLOR
        self._config.secondary_color = self.GOLD_COLOR

        logger.debug("Applied gold border colors")
        return self._config

    def apply_custom_colors(self, primary: str, secondary: str) -> BorderConfiguration:
        """
        Apply custom border colors.

        Args:
            primary: Primary border color
            secondary: Secondary border color

        Returns:
            BorderConfiguration: Updated configuration with custom colors
        """
        self._config.primary_color = primary
        self._config.secondary_color = secondary

        logger.debug(f"Applied custom colors: {primary}, {secondary}")
        return self._config

    def reset_to_original_colors(self) -> BorderConfiguration:
        """
        Reset border colors to their original values.

        Returns:
            BorderConfiguration: Configuration with original colors restored
        """
        self._config.primary_color = self._original_primary_color
        self._config.secondary_color = self._original_secondary_color

        logger.debug("Reset to original border colors")
        return self._config

    # Configuration Management
    def enable_borders(self) -> BorderConfiguration:
        """
        Enable border rendering.

        Returns:
            BorderConfiguration: Updated configuration with borders enabled
        """
        self._config.enabled = True
        logger.debug("Borders enabled")
        return self._config

    def disable_borders(self) -> BorderConfiguration:
        """
        Disable border rendering.

        Returns:
            BorderConfiguration: Updated configuration with borders disabled
        """
        self._config.enabled = False
        logger.debug("Borders disabled")
        return self._config

    def set_border_width_percentage(self, percentage: float) -> BorderConfiguration:
        """
        Set the border width percentage.

        Args:
            percentage: Border width as percentage of size (e.g., 0.015 = 1.5%)

        Returns:
            BorderConfiguration: Updated configuration
        """
        self._config.width_percentage = max(0.0, percentage)
        logger.debug(f"Border width percentage set to: {percentage}")
        return self._config

    def set_minimum_border_width(self, width: int) -> BorderConfiguration:
        """
        Set the minimum border width.

        Args:
            width: Minimum border width in pixels

        Returns:
            BorderConfiguration: Updated configuration
        """
        self._config.minimum_width = max(0, width)
        logger.debug(f"Minimum border width set to: {width}")
        return self._config

    # State Access
    def get_current_configuration(self) -> BorderConfiguration:
        """
        Get the current border configuration.

        Returns:
            BorderConfiguration: Current configuration
        """
        return self._config

    def is_borders_enabled(self) -> bool:
        """
        Check if borders are currently enabled.

        Returns:
            bool: True if borders are enabled
        """
        return self._config.enabled

    def get_current_colors(self) -> tuple[str, str]:
        """
        Get the current border colors.

        Returns:
            Tuple[str, str]: (primary_color, secondary_color)
        """
        return (self._config.primary_color, self._config.secondary_color)

    def get_original_colors(self) -> tuple[str, str]:
        """
        Get the original border colors.

        Returns:
            Tuple[str, str]: (original_primary_color, original_secondary_color)
        """
        return (self._original_primary_color, self._original_secondary_color)

    # Validation and Utilities
    def validate_configuration(self) -> bool:
        """
        Validate the current configuration.

        Returns:
            bool: True if configuration is valid
        """
        if self._config.width_percentage < 0:
            return False
        if self._config.minimum_width < 0:
            return False

        # Validate color format (basic check)
        for color in [self._config.primary_color, self._config.secondary_color]:
            if not isinstance(color, str) or not color.startswith("#"):
                return False

        return True
