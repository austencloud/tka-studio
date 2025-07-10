"""
Section Layout Service - Pure Business Logic

Handles all section layout calculations including pictograph sizing,
dimension calculations, and layout optimization without Qt dependencies.
"""

import logging
from typing import NamedTuple, Optional

from presentation.components.option_picker.types.letter_types import LetterType

logger = logging.getLogger(__name__)


class LayoutDimensions(NamedTuple):
    """Layout dimension calculations."""

    pictograph_size: int
    section_width: int
    section_height: int
    header_height: int
    content_height: int


class SizingConstraints(NamedTuple):
    """Sizing constraints for layout calculations."""

    main_window_width: int
    container_width: int
    letter_type: str
    spacing: int = 8
    padding: int = 10


class SectionLayoutManager:
    """
    Pure business service for section layout calculations.

    Handles layout algorithms, sizing calculations, and dimension
    optimization without any Qt dependencies.
    """

    # Layout constants
    DEFAULT_PICTOGRAPH_SIZE = 100
    MIN_PICTOGRAPH_SIZE = 60
    MAX_PICTOGRAPH_SIZE = 200
    BORDER_WIDTH_RATIO = 0.015
    MAIN_WINDOW_DIVISOR = 16
    CONTAINER_DIVISOR = 8
    DEFAULT_SPACING = 8
    DEFAULT_PADDING = 10

    # Letter type configurations
    LETTER_TYPE_ROWS = {
        LetterType.TYPE1: 2,  # Two rows
        LetterType.TYPE2: 1,  # One row
        LetterType.TYPE3: 1,  # One row
        LetterType.TYPE4: 1,  # One row
        LetterType.TYPE5: 1,  # One row
        LetterType.TYPE6: 1,  # One row
    }

    BOTTOM_ROW_TYPES = {LetterType.TYPE4, LetterType.TYPE5, LetterType.TYPE6}

    def __init__(self):
        """Initialize the section layout service."""
        self._current_constraints: Optional[SizingConstraints] = None
        self._cached_dimensions: Optional[LayoutDimensions] = None

        logger.debug("Section layout service initialized")

    # Pictograph Size Calculations
    def calculate_pictograph_size(self, constraints: SizingConstraints) -> int:
        """
        Calculate optimal pictograph size using the layout algorithm.

        Args:
            constraints: Sizing constraints including window and container dimensions

        Returns:
            int: Calculated pictograph size
        """
        # Use container width if available, otherwise fall back to main window width
        effective_width = (
            constraints.container_width
            if constraints.container_width > 0
            else constraints.main_window_width
        )
        if effective_width <= 0:
            effective_width = constraints.main_window_width

        # Calculate base size using the proven algorithm
        base_size = max(
            constraints.main_window_width // self.MAIN_WINDOW_DIVISOR,
            effective_width // self.CONTAINER_DIVISOR,
        )

        # Account for border width
        border_width = max(1, int(base_size * self.BORDER_WIDTH_RATIO))

        # Apply spacing adjustment
        final_size = base_size - (2 * border_width) - constraints.spacing

        # Enforce size constraints
        final_size = max(
            self.MIN_PICTOGRAPH_SIZE, min(final_size, self.MAX_PICTOGRAPH_SIZE)
        )

        logger.debug(
            f"Calculated pictograph size: {final_size} (base: {base_size}, constraints: {constraints})"
        )
        return final_size

    def calculate_optimal_size_for_container(
        self, container_width: int, main_window_width: int
    ) -> int:
        """
        Calculate optimal pictograph size for a specific container.

        Args:
            container_width: Width of the container
            main_window_width: Width of the main window

        Returns:
            int: Optimal pictograph size
        """
        constraints = SizingConstraints(
            main_window_width=main_window_width,
            container_width=container_width,
            letter_type=LetterType.TYPE1,  # Default for calculation
            spacing=self.DEFAULT_SPACING,
        )

        return self.calculate_pictograph_size(constraints)

    # Section Dimension Calculations
    def calculate_section_width(self, letter_type: str, total_width: int) -> int:
        """
        Calculate section width based on letter type.

        Args:
            letter_type: The type of letter section
            total_width: Total available width

        Returns:
            int: Calculated section width
        """
        if letter_type in self.BOTTOM_ROW_TYPES:
            # Bottom row sections split width into thirds
            return total_width // 3
        else:
            # Top sections use full width
            return total_width

    def calculate_section_height(
        self, constraints: SizingConstraints, header_height: int
    ) -> LayoutDimensions:
        """
        Calculate complete section dimensions.

        Args:
            constraints: Sizing constraints
            header_height: Height of the section header

        Returns:
            LayoutDimensions: Complete dimension calculations
        """
        # Calculate pictograph size
        pictograph_size = self.calculate_pictograph_size(constraints)

        # Calculate section width
        section_width = self.calculate_section_width(
            constraints.letter_type, constraints.main_window_width
        )

        # Calculate content height based on letter type
        rows = self.LETTER_TYPE_ROWS.get(constraints.letter_type, 1)
        content_height = (
            (rows * pictograph_size)
            + ((rows - 1) * constraints.spacing)
            + constraints.padding
        )

        # Total section height
        total_height = header_height + content_height

        dimensions = LayoutDimensions(
            pictograph_size=pictograph_size,
            section_width=section_width,
            section_height=total_height,
            header_height=header_height,
            content_height=content_height,
        )

        logger.debug(f"Calculated section dimensions: {dimensions}")
        return dimensions

    # Layout Optimization
    def optimize_layout_for_content(
        self, constraints: SizingConstraints, existing_pictographs: int
    ) -> LayoutDimensions:
        """
        Optimize layout dimensions based on actual content.

        Args:
            constraints: Sizing constraints
            existing_pictographs: Number of existing pictographs

        Returns:
            LayoutDimensions: Optimized dimensions
        """
        # Calculate base dimensions
        base_dimensions = self.calculate_section_height(
            constraints, 0
        )  # Will add header later

        # Adjust based on content
        if existing_pictographs == 0:
            # Empty section - minimal height
            content_height = base_dimensions.pictograph_size + constraints.padding
        else:
            # Calculate required rows
            rows = self.LETTER_TYPE_ROWS.get(constraints.letter_type, 1)
            if constraints.letter_type == LetterType.TYPE1:
                # Type 1 can have up to 2 rows, adjust based on content
                actual_rows = min(
                    rows, (existing_pictographs + 7) // 8
                )  # 8 per row estimate
            else:
                actual_rows = 1

            content_height = (
                (actual_rows * base_dimensions.pictograph_size)
                + ((actual_rows - 1) * constraints.spacing)
                + constraints.padding
            )

        return base_dimensions._replace(content_height=content_height)

    # Resize Handling
    def calculate_resize_dimensions(
        self, old_width: int, new_width: int, current_dimensions: LayoutDimensions
    ) -> Optional[LayoutDimensions]:
        """
        Calculate new dimensions after a resize event.

        Args:
            old_width: Previous width
            new_width: New width
            current_dimensions: Current layout dimensions

        Returns:
            LayoutDimensions or None: New dimensions if resize is significant enough
        """
        # Check if resize is significant (more than 5 pixels difference)
        if abs(new_width - old_width) <= 5:
            return None

        # Calculate scaling factor
        scale_factor = new_width / old_width if old_width > 0 else 1.0

        # Apply scaling to pictograph size with constraints
        new_pictograph_size = int(current_dimensions.pictograph_size * scale_factor)
        new_pictograph_size = max(
            self.MIN_PICTOGRAPH_SIZE, min(new_pictograph_size, self.MAX_PICTOGRAPH_SIZE)
        )

        # Recalculate other dimensions
        scale_adjustment = new_pictograph_size / current_dimensions.pictograph_size
        new_content_height = int(current_dimensions.content_height * scale_adjustment)
        new_total_height = current_dimensions.header_height + new_content_height

        return LayoutDimensions(
            pictograph_size=new_pictograph_size,
            section_width=new_width,
            section_height=new_total_height,
            header_height=current_dimensions.header_height,
            content_height=new_content_height,
        )

    # Layout Validation
    def validate_dimensions(self, dimensions: LayoutDimensions) -> bool:
        """
        Validate calculated dimensions.

        Args:
            dimensions: Dimensions to validate

        Returns:
            bool: True if dimensions are valid
        """
        # Check minimum size constraints
        if dimensions.pictograph_size < self.MIN_PICTOGRAPH_SIZE:
            return False

        # Check maximum size constraints
        if dimensions.pictograph_size > self.MAX_PICTOGRAPH_SIZE:
            return False

        # Check that total height makes sense
        if dimensions.section_height < dimensions.header_height:
            return False

        # Check that content height is reasonable
        if dimensions.content_height < 0:
            return False

        return True

    def calculate_minimum_required_space(
        self, letter_type: str, pictograph_count: int
    ) -> LayoutDimensions:
        """
        Calculate minimum space required for a given configuration.

        Args:
            letter_type: Type of the section
            pictograph_count: Number of pictographs to accommodate

        Returns:
            LayoutDimensions: Minimum required dimensions
        """
        # Use minimum pictograph size for calculation
        min_size = self.MIN_PICTOGRAPH_SIZE
        rows = self.LETTER_TYPE_ROWS.get(letter_type, 1)

        # Calculate required content height
        content_height = (
            (rows * min_size)
            + ((rows - 1) * self.DEFAULT_SPACING)
            + self.DEFAULT_PADDING
        )

        # Estimate minimum width based on pictographs per row
        if letter_type == LetterType.TYPE1:
            pictographs_per_row = max(1, pictograph_count // 2)
        else:
            pictographs_per_row = pictograph_count

        min_width = (
            pictographs_per_row * min_size
            + (pictographs_per_row - 1) * self.DEFAULT_SPACING
        )

        return LayoutDimensions(
            pictograph_size=min_size,
            section_width=min_width,
            section_height=content_height + 50,  # Estimate for header
            header_height=50,  # Estimate
            content_height=content_height,
        )

    # Caching and Performance
    def cache_dimensions(
        self, constraints: SizingConstraints, dimensions: LayoutDimensions
    ) -> None:
        """
        Cache calculated dimensions for performance.

        Args:
            constraints: The constraints used for calculation
            dimensions: The calculated dimensions
        """
        self._current_constraints = constraints
        self._cached_dimensions = dimensions

    def get_cached_dimensions(
        self, constraints: SizingConstraints
    ) -> Optional[LayoutDimensions]:
        """
        Get cached dimensions if constraints match.

        Args:
            constraints: Current constraints

        Returns:
            LayoutDimensions or None: Cached dimensions if available and valid
        """
        if self._current_constraints == constraints and self._cached_dimensions:
            return self._cached_dimensions
        return None

    def clear_cache(self) -> None:
        """Clear cached dimensions."""
        self._current_constraints = None
        self._cached_dimensions = None
        logger.debug("Layout cache cleared")

    # Utility Methods
    def get_layout_summary(self, dimensions: LayoutDimensions) -> dict:
        """
        Get a summary of layout information for debugging.

        Args:
            dimensions: Layout dimensions to summarize

        Returns:
            dict: Summary information
        """
        return {
            "pictograph_size": dimensions.pictograph_size,
            "section_width": dimensions.section_width,
            "section_height": dimensions.section_height,
            "header_height": dimensions.header_height,
            "content_height": dimensions.content_height,
            "is_valid": self.validate_dimensions(dimensions),
            "cache_available": self._cached_dimensions is not None,
        }
