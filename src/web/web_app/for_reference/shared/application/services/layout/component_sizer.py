"""
Component Sizing Service

Calculates optimal component sizes based on container constraints.
Framework-agnostic service for responsive component sizing.
"""

import logging
from enum import Enum
from typing import NamedTuple

from desktop.modern.core.interfaces.core_services import IComponentSizer

logger = logging.getLogger(__name__)


class ComponentType(Enum):
    """Types of components that can be sized."""

    PICTOGRAPH_FRAME = "pictograph_frame"
    BEAT_FRAME = "beat_frame"
    OPTION_FRAME = "option_frame"


class SizeConstraints(NamedTuple):
    """Size constraints for component sizing calculations."""

    min_size: int
    max_size: int
    border_width_ratio: float = 0.015
    spacing: int = 3


class Dimensions(NamedTuple):
    """Component dimensions."""

    width: int
    height: int


class Size(NamedTuple):
    """Size representation."""

    width: int
    height: int


class ComponentSizer(IComponentSizer):
    """
    Calculates optimal component sizes based on container constraints.

    Provides centralized sizing logic for different component types,
    ensuring consistent sizing behavior across the application.
    """

    def __init__(self):
        """Initialize the component sizer."""

    def calculate_pictograph_frame_size(
        self, container_width: int, constraints: SizeConstraints | None = None
    ) -> int:
        """
        Calculate optimal frame size for pictograph components.

        Args:
            container_width: Width of the container widget
            constraints: Optional size constraints, uses defaults if not provided

        Returns:
            Optimal frame size as integer
        """
        if constraints is None:
            constraints = SizeConstraints(
                min_size=60, max_size=200, border_width_ratio=0.015, spacing=3
            )

        try:
            # Calculate base size from container
            container_based_size = container_width // 8
            size = container_based_size

            # Calculate border width based on size
            border_width = max(1, int(size * constraints.border_width_ratio))

            # Calculate final size accounting for borders and spacing
            final_size = size - (2 * border_width) - constraints.spacing

            # Apply constraints
            final_size = self.apply_size_constraints(
                final_size, constraints.min_size, constraints.max_size
            )

            logger.debug(
                f"Calculated pictograph frame size: {final_size} "
                f"(container: {container_width}, base: {container_based_size})"
            )

            return final_size

        except Exception as e:
            logger.warning(f"Error calculating pictograph frame size: {e}")
            return constraints.min_size if constraints else 60

    def calculate_responsive_dimensions(
        self, parent_size: tuple[int, int], component_type: ComponentType
    ) -> Dimensions:
        """
        Calculate responsive dimensions for different component types.

        Args:
            parent_size: Size of the parent container
            component_type: Type of component to size

        Returns:
            Optimal dimensions for the component
        """
        if component_type == ComponentType.PICTOGRAPH_FRAME:
            # For pictograph frames, use square dimensions
            size = self.calculate_pictograph_frame_size(parent_size.width)
            return Dimensions(width=size, height=size)

        elif component_type == ComponentType.BEAT_FRAME:
            # Beat frames use different proportions
            width = min(parent_size.width // 6, 150)
            height = min(parent_size.height // 8, 120)
            return Dimensions(width=width, height=height)

        elif component_type == ComponentType.OPTION_FRAME:
            # Option frames are typically smaller
            size = min(parent_size.width // 10, 100)
            return Dimensions(width=size, height=size)

        else:
            # Default fallback
            logger.warning(f"Unknown component type: {component_type}")
            return Dimensions(width=100, height=100)

    def apply_size_constraints(
        self, proposed_size: int, min_size: int, max_size: int
    ) -> int:
        """
        Apply min/max constraints to proposed size.

        Args:
            proposed_size: The initially calculated size
            min_size: Minimum allowable size
            max_size: Maximum allowable size

        Returns:
            Size value constrained within the specified bounds
        """
        return max(min_size, min(proposed_size, max_size))

    def calculate_container_based_size(
        self, container_width: int, divisor: int = 8
    ) -> int:
        """
        Calculate size based on container width division.

        Args:
            container_width: Width of the container
            divisor: Division factor (default: 8)

        Returns:
            Calculated size based on container width
        """
        return container_width // divisor

    def calculate_border_width(self, component_size: int, ratio: float = 0.015) -> int:
        """
        Calculate border width based on component size.

        Args:
            component_size: Size of the component
            ratio: Border width ratio (default: 0.015)

        Returns:
            Calculated border width (minimum 1)
        """
        return max(1, int(component_size * ratio))

    def calculate_final_size(
        self, base_size: int, border_width: int, spacing: int = 0
    ) -> int:
        """
        Calculate final size accounting for borders and spacing.

        Args:
            base_size: Base component size
            border_width: Width of borders
            spacing: Additional spacing to account for

        Returns:
            Final size after accounting for borders and spacing
        """
        return base_size - (2 * border_width) - spacing

    # Interface implementation methods
    def calculate_component_size(
        self, component_type: str, content_size: tuple[int, int]
    ) -> tuple[int, int]:
        """Calculate component size based on content (interface implementation)."""
        content_width, content_height = content_size

        # Map string to enum
        comp_type = ComponentType.PICTOGRAPH_FRAME
        if component_type == "beat_frame":
            comp_type = ComponentType.BEAT_FRAME
        elif component_type == "option_frame":
            comp_type = ComponentType.OPTION_FRAME

        # Use existing calculation logic
        dimensions = self.calculate_size(comp_type, content_width, content_height)
        return (dimensions.width, dimensions.height)

    def apply_responsive_sizing(
        self, base_size: tuple[int, int], viewport_size: tuple[int, int]
    ) -> tuple[int, int]:
        """Apply responsive sizing rules (interface implementation)."""
        base_width, base_height = base_size
        viewport_width, viewport_height = viewport_size

        # Calculate scale factor based on viewport
        scale_x = viewport_width / 1920  # Assume 1920 as base width
        scale_y = viewport_height / 1080  # Assume 1080 as base height
        scale_factor = min(
            scale_x, scale_y
        )  # Use smaller scale to maintain aspect ratio

        # Apply scaling with minimum bounds
        scaled_width = max(50, int(base_width * scale_factor))
        scaled_height = max(50, int(base_height * scale_factor))

        return (scaled_width, scaled_height)
