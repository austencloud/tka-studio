"""
Layout Service Interfaces

Interface definitions for layout calculation services following TKA's clean architecture.
These interfaces define contracts for beat layout calculations, grid layouts, responsive scaling,
and cross-platform layout operations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from desktop.modern.domain.models.sequence_data import SequenceData


class ComponentType(Enum):
    """Types of components that can be sized and positioned."""

    PICTOGRAPH_FRAME = "pictograph_frame"
    BEAT_FRAME = "beat_frame"
    OPTION_FRAME = "option_frame"
    SEQUENCE_FRAME = "sequence_frame"


class LayoutMode(Enum):
    """Layout modes for different display scenarios."""

    GRID = "grid"
    FLOW = "flow"
    FIXED = "fixed"
    RESPONSIVE = "responsive"


class Size:
    """Size representation for cross-platform compatibility."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


class Position:
    """Position representation for cross-platform compatibility."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class IBeatLayoutCalculator(ABC):
    """
    Interface for comprehensive beat layout calculations.

    Handles layout calculations for beat frame sequences, grid layouts,
    and responsive scaling using TKA's carefully designed layout algorithms.
    """

    @abstractmethod
    def calculate_beat_frame_layout(
        self, sequence: SequenceData, container_size: tuple[int, int]
    ) -> dict[str, Any]:
        """
        Calculate layout for beat frames using carefully designed algorithm.

        Args:
            sequence: Sequence data containing beats
            container_size: Container dimensions (width, height)

        Returns:
            Dict containing layout information with 'rows' and 'columns' keys
        """

    @abstractmethod
    def get_optimal_grid_layout(
        self, item_count: int, container_size: tuple[int, int]
    ) -> tuple[int, int]:
        """
        Get optimal grid layout (rows, cols) for items.

        Args:
            item_count: Number of items to layout
            container_size: Container dimensions (width, height)

        Returns:
            Tuple of (rows, cols) for optimal layout
        """

    @abstractmethod
    def calculate_horizontal_beat_layout(
        self,
        beat_count: int,
        container_size: tuple[int, int],
        base_size: tuple[int, int],
        padding: int,
        spacing: int,
    ) -> dict[str, Any]:
        """
        Calculate horizontal layout for beats.

        Args:
            beat_count: Number of beats to layout
            container_size: Container dimensions
            base_size: Base size for each beat
            padding: Padding around layout
            spacing: Spacing between beats

        Returns:
            Dict containing horizontal layout information
        """

    @abstractmethod
    def calculate_grid_beat_layout(
        self,
        beat_count: int,
        container_size: tuple[int, int],
        base_size: tuple[int, int],
        padding: int,
        spacing: int,
    ) -> dict[str, Any]:
        """
        Calculate grid layout for beats.

        Args:
            beat_count: Number of beats to layout
            container_size: Container dimensions
            base_size: Base size for each beat
            padding: Padding around layout
            spacing: Spacing between beats

        Returns:
            Dict containing grid layout information
        """


class IResponsiveScalingCalculator(ABC):
    """Interface for responsive scaling calculation operations."""

    @abstractmethod
    def calculate_scaling_factor(
        self, container_size: Size, content_size: Size
    ) -> float:
        """
        Calculate appropriate scaling factor for content within container.

        Args:
            container_size: Size of the container
            content_size: Size of the content to scale

        Returns:
            Scaling factor to apply

        Note:
            Web implementation: Uses CSS scale transforms or viewport units
        """

    @abstractmethod
    def get_density_scaling_factor(self, density: str) -> float:
        """
        Get scaling factor for screen density.

        Args:
            density: Screen density ("low", "normal", "high", "extra_high")

        Returns:
            Scaling factor for the density

        Note:
            Web implementation: Uses devicePixelRatio and CSS media queries
        """

    @abstractmethod
    def calculate_context_aware_scaling(self, context: str, base_size: Size) -> float:
        """
        Calculate scaling for specific usage context.

        Args:
            context: Context identifier (e.g., "editor", "picker", "export")
            base_size: Base size for the context

        Returns:
            Context-appropriate scaling factor

        Note:
            Web implementation: May use CSS container queries
        """

    @abstractmethod
    def get_breakpoint_scaling(self, viewport_width: int) -> float:
        """
        Get scaling factor based on viewport width breakpoints.

        Args:
            viewport_width: Width of the viewport

        Returns:
            Scaling factor for the breakpoint

        Note:
            Web implementation: Uses CSS breakpoints and media queries
        """

    @abstractmethod
    def calculate_adaptive_scaling(
        self, available_space: Size, min_size: Size, max_size: Size
    ) -> float:
        """
        Calculate adaptive scaling that respects size constraints.

        Args:
            available_space: Available space for content
            min_size: Minimum allowed size
            max_size: Maximum allowed size

        Returns:
            Adaptive scaling factor

        Note:
            Web implementation: Uses CSS clamp() or JavaScript calculations
        """


class IBeatResizer(ABC):
    """Interface for beat frame resizing operations."""

    @abstractmethod
    def calculate_beat_size(self, container_size: Size, num_columns: int) -> Size:
        """
        Calculate optimal beat frame size based on container and column count.

        Args:
            container_size: Size of the container
            num_columns: Number of columns in the layout

        Returns:
            Calculated beat frame size

        Note:
            Web implementation: Uses CSS Grid or Flexbox calculations
        """

    @abstractmethod
    def resize_beat_frames(self, beat_frames: list[Any], new_size: Size) -> None:
        """
        Resize multiple beat frames to new size.

        Args:
            beat_frames: List of beat frame components
            new_size: New size to apply

        Note:
            Web implementation: Updates CSS properties or style attributes
        """

    @abstractmethod
    def calculate_scroll_requirements(
        self, content_size: Size, container_size: Size
    ) -> dict[str, bool]:
        """
        Calculate if scrolling is needed and in which directions.

        Args:
            content_size: Size of the content
            container_size: Size of the container

        Returns:
            Dictionary with 'horizontal' and 'vertical' scroll requirements

        Note:
            Web implementation: Uses CSS overflow properties
        """

    @abstractmethod
    def get_optimal_aspect_ratio(self) -> float:
        """
        Get optimal aspect ratio for beat frames.

        Returns:
            Aspect ratio (width/height)

        Note:
            Web implementation: May use CSS aspect-ratio property
        """

    @abstractmethod
    def validate_beat_size(self, size: Size, min_size: Size, max_size: Size) -> Size:
        """
        Validate and adjust beat size within constraints.

        Args:
            size: Proposed size
            min_size: Minimum allowed size
            max_size: Maximum allowed size

        Returns:
            Validated and adjusted size
        """


class IComponentSizer(ABC):
    """Interface for component sizing operations."""

    @abstractmethod
    def calculate_component_size(
        self, component_type: ComponentType, container_size: Size
    ) -> Size:
        """
        Calculate size for a specific component type.

        Args:
            component_type: Type of component to size
            container_size: Size of the container

        Returns:
            Calculated component size

        Note:
            Web implementation: Uses CSS sizing strategies for each component type
        """

    @abstractmethod
    def get_size_constraints(self, component_type: ComponentType) -> dict[str, Any]:
        """
        Get size constraints for a component type.

        Args:
            component_type: Type of component

        Returns:
            Dictionary with min_size, max_size, and other constraints

        Note:
            Web implementation: Constraints may be defined in CSS custom properties
        """

    @abstractmethod
    def calculate_optimal_grid_size(
        self, item_count: int, container_size: Size
    ) -> tuple[int, int]:
        """
        Calculate optimal grid dimensions for item count and container.

        Args:
            item_count: Number of items to layout
            container_size: Size of the container

        Returns:
            Tuple of (rows, columns) for optimal grid

        Note:
            Web implementation: Uses CSS Grid auto-fit or auto-fill
        """

    @abstractmethod
    def apply_responsive_constraints(
        self, base_size: Size, viewport_size: Size
    ) -> Size:
        """
        Apply responsive constraints to base size.

        Args:
            base_size: Base component size
            viewport_size: Current viewport size

        Returns:
            Responsive adjusted size

        Note:
            Web implementation: Uses CSS media queries and viewport units
        """


class IComponentPositionCalculator(ABC):
    """Interface for component positioning operations."""

    @abstractmethod
    def calculate_component_positions(
        self, layout_config: dict[str, Any]
    ) -> dict[str, Position]:
        """
        Calculate positions for UI components based on layout configuration.

        Args:
            layout_config: Configuration dictionary for layout

        Returns:
            Dictionary mapping component IDs to positions

        Note:
            Web implementation: Uses CSS positioning or CSS Grid/Flexbox
        """

    @abstractmethod
    def calculate_grid_positions(
        self, rows: int, cols: int, container_size: Size
    ) -> list[Position]:
        """
        Calculate positions for grid layout.

        Args:
            rows: Number of rows
            cols: Number of columns
            container_size: Size of the container

        Returns:
            List of positions for grid items

        Note:
            Web implementation: Uses CSS Grid template areas or calculations
        """

    @abstractmethod
    def calculate_flow_positions(
        self, items: list[Any], container_size: Size
    ) -> list[Position]:
        """
        Calculate positions for flow layout.

        Args:
            items: List of items to position
            container_size: Size of the container

        Returns:
            List of positions for flow items

        Note:
            Web implementation: Uses CSS Flexbox or flow layout
        """

    @abstractmethod
    def get_layout_bounds(
        self, positions: list[Position], sizes: list[Size]
    ) -> dict[str, int]:
        """
        Get bounds of a layout based on positions and sizes.

        Args:
            positions: List of component positions
            sizes: List of component sizes

        Returns:
            Dictionary with 'width', 'height', 'left', 'top' bounds

        Note:
            Web implementation: Uses getBoundingClientRect() equivalent
        """

    @abstractmethod
    def apply_spacing_constraints(
        self, positions: list[Position], spacing: int
    ) -> list[Position]:
        """
        Apply spacing constraints to positions.

        Args:
            positions: List of positions to adjust
            spacing: Spacing value to apply

        Returns:
            List of adjusted positions with spacing applied

        Note:
            Web implementation: Uses CSS gap or margin properties
        """


class IDimensionCalculator(ABC):
    """Interface for dimension calculation operations."""

    @abstractmethod
    def calculate_optimal_size(self, constraints: dict[str, Any]) -> Size:
        """
        Calculate optimal size based on constraints.

        Args:
            constraints: Dictionary with size constraints

        Returns:
            Calculated optimal size

        Note:
            Web implementation: Uses CSS calculations or JavaScript sizing
        """

    @abstractmethod
    def get_screen_dimensions(self) -> Size:
        """
        Get current screen/viewport dimensions.

        Returns:
            Screen dimensions

        Note:
            Web implementation: Uses window.innerWidth/innerHeight
        """

    @abstractmethod
    def calculate_container_dimensions(self, parent_size: Size, margin: int) -> Size:
        """
        Calculate container dimensions with margin.

        Args:
            parent_size: Size of the parent container
            margin: Margin to apply

        Returns:
            Container dimensions with margin applied
        """

    @abstractmethod
    def get_content_dimensions(self, element: Any) -> Size:
        """
        Get dimensions of content within an element.

        Args:
            element: Element to measure

        Returns:
            Content dimensions

        Note:
            Web implementation: Uses getBoundingClientRect() or similar
        """

    @abstractmethod
    def calculate_aspect_ratio_size(self, base_size: Size, target_ratio: float) -> Size:
        """
        Calculate size that maintains aspect ratio.

        Args:
            base_size: Base size to adjust
            target_ratio: Target aspect ratio (width/height)

        Returns:
            Size adjusted to maintain aspect ratio

        Note:
            Web implementation: May use CSS aspect-ratio property
        """

    @abstractmethod
    def validate_size_constraints(
        self, size: Size, min_size: Size, max_size: Size
    ) -> Size:
        """
        Validate size against constraints and adjust if needed.

        Args:
            size: Size to validate
            min_size: Minimum allowed size
            max_size: Maximum allowed size

        Returns:
            Validated size within constraints
        """
