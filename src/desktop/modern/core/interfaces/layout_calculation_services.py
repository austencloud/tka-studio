"""
Interface definitions for layout calculation services in TKA.

These interfaces define contracts for layout calculations, including beat layouts,
grid layouts, component positioning, and responsive scaling operations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from desktop.modern.domain.models.sequence_data import SequenceData


class IBeatLayoutCalculator(ABC):
    """Interface for beat layout calculation operations."""

    @abstractmethod
    def calculate_beat_frame_layout(
        self, sequence: SequenceData, container_size: tuple[int, int]
    ) -> dict[str, Any]:
        """
        Calculate layout for beat frames in a sequence.

        Args:
            sequence: The sequence data containing beats
            container_size: The container dimensions (width, height)

        Returns:
            Dict containing layout information (rows, columns, positions)
        """

    @abstractmethod
    def get_optimal_grid_layout(
        self, item_count: int, container_size: tuple[int, int]
    ) -> tuple[int, int]:
        """
        Get optimal grid layout (rows, cols) for items.

        Args:
            item_count: Number of items to arrange
            container_size: Container dimensions (width, height)

        Returns:
            Tuple of (rows, columns) for optimal arrangement
        """


class IComponentPositionCalculator(ABC):
    """Interface for calculating component positions within layouts."""

    @abstractmethod
    def calculate_component_positions(
        self, layout_config: dict[str, Any]
    ) -> dict[str, tuple[int, int]]:
        """
        Calculate positions for UI components based on layout configuration.

        Args:
            layout_config: Configuration dictionary for layout

        Returns:
            Dict mapping component IDs to (x, y) positions
        """

    @abstractmethod
    def calculate_center_position(
        self, item_size: tuple[int, int], container_size: tuple[int, int]
    ) -> tuple[int, int]:
        """
        Calculate centered position for an item within a container.

        Args:
            item_size: Size of the item (width, height)
            container_size: Size of the container (width, height)

        Returns:
            Tuple of (x, y) position for centering
        """

    @abstractmethod
    def calculate_grid_positions(
        self,
        item_count: int,
        rows: int,
        columns: int,
        container_size: tuple[int, int],
        item_size: tuple[int, int],
        spacing: int = 0,
        padding: int = 0,
    ) -> dict[int, tuple[int, int]]:
        """
        Calculate positions for items in a grid layout.

        Args:
            item_count: Number of items to position
            rows: Number of rows in grid
            columns: Number of columns in grid
            container_size: Container dimensions
            item_size: Size of each item
            spacing: Space between items
            padding: Padding around edges

        Returns:
            Dict mapping item indices to (x, y) positions
        """


class IResponsiveScalingCalculator(ABC):
    """Interface for responsive scaling calculations."""

    @abstractmethod
    def calculate_responsive_scaling(
        self, content_size: tuple[int, int], container_size: tuple[int, int]
    ) -> float:
        """
        Calculate responsive scaling factor for content within container.

        Args:
            content_size: Original content dimensions (width, height)
            container_size: Target container dimensions (width, height)

        Returns:
            float: Scaling factor to apply
        """

    @abstractmethod
    def calculate_aspect_aware_scaling(
        self,
        content_size: tuple[int, int],
        container_size: tuple[int, int],
        maintain_aspect_ratio: bool = True,
    ) -> tuple[float, float]:
        """
        Calculate scaling factors that may be aspect-aware.

        Args:
            content_size: Original content dimensions
            container_size: Target container dimensions
            maintain_aspect_ratio: Whether to maintain aspect ratio

        Returns:
            Tuple of (scale_x, scale_y) factors
        """

    @abstractmethod
    def get_minimum_scale_factor(self) -> float:
        """
        Get the minimum allowable scale factor.

        Returns:
            float: Minimum scale factor (e.g., 0.1 for 10% minimum)
        """

    @abstractmethod
    def get_maximum_scale_factor(self) -> float:
        """
        Get the maximum allowable scale factor.

        Returns:
            float: Maximum scale factor (e.g., 5.0 for 500% maximum)
        """


class IComponentSizer(ABC):
    """Interface for calculating component sizes."""

    @abstractmethod
    def calculate_component_size(
        self, component_type: str, parent_size: tuple[int, int], **kwargs
    ) -> tuple[int, int]:
        """
        Calculate size for a component based on its type and parent.

        Args:
            component_type: Type of component (e.g., 'beat_frame', 'option_picker')
            parent_size: Size of parent container
            **kwargs: Additional sizing parameters

        Returns:
            Tuple of (width, height) for the component
        """

    @abstractmethod
    def calculate_minimum_size(self, component_type: str) -> tuple[int, int]:
        """
        Calculate minimum size for a component type.

        Args:
            component_type: Type of component

        Returns:
            Tuple of minimum (width, height)
        """

    @abstractmethod
    def calculate_preferred_size(
        self, component_type: str, available_space: tuple[int, int]
    ) -> tuple[int, int]:
        """
        Calculate preferred size for a component within available space.

        Args:
            component_type: Type of component
            available_space: Available space (width, height)

        Returns:
            Tuple of preferred (width, height)
        """


class IDimensionCalculator(ABC):
    """Interface for dimension calculations across the layout system."""

    @abstractmethod
    def calculate_total_dimensions(
        self,
        item_count: int,
        item_size: tuple[int, int],
        layout: tuple[int, int],
        spacing: int = 0,
        padding: int = 0,
    ) -> tuple[int, int]:
        """
        Calculate total dimensions needed for a layout.

        Args:
            item_count: Number of items
            item_size: Size of each item
            layout: Layout as (rows, columns)
            spacing: Space between items
            padding: Padding around edges

        Returns:
            Tuple of total (width, height) needed
        """

    @abstractmethod
    def calculate_available_space(
        self, container_size: tuple[int, int], reserved_space: dict[str, int]
    ) -> tuple[int, int]:
        """
        Calculate available space after reserving space for other elements.

        Args:
            container_size: Total container size
            reserved_space: Dict with 'top', 'bottom', 'left', 'right' reserved pixels

        Returns:
            Tuple of available (width, height)
        """

    @abstractmethod
    def get_aspect_ratio(self, size: tuple[int, int]) -> float:
        """
        Calculate aspect ratio from size.

        Args:
            size: Size tuple (width, height)

        Returns:
            float: Aspect ratio (width/height)
        """
