"""
Simplified Scaling Service for Modern Pictographs.

This service provides basic scaling compatibility for legacy code.
The main scaling logic is now handled directly in the pictograph widget
using a unified container-aware approach.
"""

from typing import Tuple

from core.interfaces.pictograph_services import (
    IScalingService,
    ScalingContext,
)
from core.types import Size
from PyQt6.QtCore import QSize


class PictographScaler(IScalingService):
    """
    Simplified scaling service for compatibility with existing code.

    The actual scaling is now handled by the pictograph widget's unified
    container-aware scaling system. This service provides basic compatibility
    for any remaining legacy code that expects the old interface.
    """

    def __init__(self):
        pass  # No complex state needed

    def calculate_scale(
        self,
        context: ScalingContext,
        container_size: Size,
        scene_size: Size,
        **context_params,
    ) -> Tuple[float, float]:
        """
        Simple scaling calculation for compatibility.

        The actual scaling is now handled by the pictograph widget's unified
        container-aware system. This method provides basic container-to-scene
        scaling for any legacy code that still calls it.

        Args:
            context: The scaling context (ignored - handled by widget)
            container_size: Size of the container widget
            scene_size: Size of the pictograph scene
            **context_params: Additional parameters (ignored)

        Returns:
            Tuple of (scale_x, scale_y) factors based on container fitting
        """
        # Simple container-aware scaling
        if scene_size.width <= 0 or scene_size.height <= 0:
            return (1.0, 1.0)

        scale_x = container_size.width / scene_size.width
        scale_y = container_size.height / scene_size.height

        # Use uniform scaling to maintain aspect ratio
        uniform_scale = min(scale_x, scale_y) * 0.9  # Small margin

        return (uniform_scale, uniform_scale)

    def calculate_scale_factors(
        self,
        context: ScalingContext,
        container_size: QSize,
        scene_size: QSize,
        **context_params,
    ) -> Tuple[float, float]:
        """
        QSize compatibility method for existing code.

        Args:
            context: The scaling context (ignored)
            container_size: Size of the container widget (QSize)
            scene_size: Size of the pictograph scene (QSize)
            **context_params: Additional parameters (ignored)

        Returns:
            Tuple of (scale_x, scale_y) factors
        """
        # Convert QSize to Size for interface compatibility
        container_size_tuple = Size(container_size.width(), container_size.height())
        scene_size_tuple = Size(scene_size.width(), scene_size.height())

        return self.calculate_scale(
            context, container_size_tuple, scene_size_tuple, **context_params
        )

    def get_responsive_border_width(self, target_size: int) -> int:
        """
        Calculate responsive border width based on target size.

        Args:
            target_size: Target size for the pictograph

        Returns:
            Border width in pixels
        """
        # Simple responsive border calculation
        return max(1, int(target_size * 0.015))


# Global function for compatibility with existing code
def get_scaling_service() -> PictographScaler:
    """
    Get the scaling service instance.

    This function provides compatibility with existing code that expects
    a global get_scaling_service() function.

    Returns:
        PictographScaler: The scaling service instance
    """
    return PictographScaler()
