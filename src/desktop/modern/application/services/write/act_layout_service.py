"""
Act Layout Service

Service for calculating layout dimensions and positioning for acts.
Handles grid layout calculations and responsive sizing.
"""

from __future__ import annotations

import logging
import math

from desktop.modern.core.interfaces.write_services import IActLayoutService


logger = logging.getLogger(__name__)


class ActLayoutService(IActLayoutService):
    """
    Service for calculating act layout and grid positioning.

    Provides calculations for optimal grid dimensions, sequence sizing,
    and positioning within act sheets.
    """

    def __init__(self, min_sequence_size: int = 150, max_sequence_size: int = 300):
        """
        Initialize the act layout service.

        Args:
            min_sequence_size: Minimum size for sequence thumbnails
            max_sequence_size: Maximum size for sequence thumbnails
        """
        self.min_sequence_size = min_sequence_size
        self.max_sequence_size = max_sequence_size

        logger.info(
            f"ActLayoutService initialized (size range: {min_sequence_size}-{max_sequence_size})"
        )

    def calculate_grid_dimensions(self, sequence_count: int) -> tuple[int, int]:
        """
        Calculate optimal grid dimensions for sequences.

        Args:
            sequence_count: Number of sequences to arrange

        Returns:
            Tuple of (columns, rows)
        """
        if sequence_count <= 0:
            return (0, 0)

        # For small counts, use simple layouts
        if sequence_count == 1:
            return (1, 1)
        if sequence_count == 2:
            return (2, 1)
        if sequence_count == 3:
            return (3, 1)
        if sequence_count == 4:
            return (2, 2)

        # For larger counts, aim for roughly square grids
        # with a preference for more columns than rows (wider layout)

        # Start with square root
        sqrt_count = math.sqrt(sequence_count)

        # Try different column counts around the square root
        best_cols = int(sqrt_count)
        best_rows = math.ceil(sequence_count / best_cols)
        best_ratio = max(best_cols, best_rows) / min(best_cols, best_rows)

        # Test nearby column counts to find better aspect ratios
        for cols in range(max(1, int(sqrt_count) - 2), int(sqrt_count) + 4):
            rows = math.ceil(sequence_count / cols)

            # Skip if too many empty cells
            empty_cells = (cols * rows) - sequence_count
            if empty_cells > cols:  # More than one full row empty
                continue

            # Calculate aspect ratio (prefer wider layouts)
            ratio = max(cols, rows) / min(cols, rows)

            # Prefer wider layouts by giving bonus to more columns
            width_bonus = 0.1 if cols > rows else 0
            adjusted_ratio = ratio - width_bonus

            if adjusted_ratio < best_ratio:
                best_cols = cols
                best_rows = rows
                best_ratio = adjusted_ratio

        logger.debug(
            f"Grid for {sequence_count} sequences: {best_cols}x{best_rows} "
            f"(aspect ratio: {best_ratio:.2f})"
        )

        return (best_cols, best_rows)

    def calculate_sequence_size(
        self,
        available_width: int,
        available_height: int,
        grid_cols: int,
        grid_rows: int,
        padding: int = 10,
    ) -> tuple[int, int]:
        """
        Calculate size for individual sequences in the grid.

        Args:
            available_width: Available width for the grid
            available_height: Available height for the grid
            grid_cols: Number of columns in the grid
            grid_rows: Number of rows in the grid
            padding: Padding between sequences

        Returns:
            Tuple of (width, height) for each sequence
        """
        if grid_cols <= 0 or grid_rows <= 0:
            return (self.min_sequence_size, self.min_sequence_size)

        # Calculate available space per sequence
        total_h_padding = padding * (grid_cols + 1)  # Between sequences + edges
        total_v_padding = padding * (grid_rows + 1)  # Between sequences + edges

        available_per_col = (available_width - total_h_padding) / grid_cols
        available_per_row = (available_height - total_v_padding) / grid_rows

        # Use the smaller dimension to maintain square sequences
        sequence_size = min(available_per_col, available_per_row)

        # Clamp to min/max bounds
        sequence_size = max(
            self.min_sequence_size, min(self.max_sequence_size, sequence_size)
        )

        # Convert to integer
        sequence_size = int(sequence_size)

        logger.debug(
            f"Calculated sequence size: {sequence_size}x{sequence_size} "
            f"(available: {available_width}x{available_height}, "
            f"grid: {grid_cols}x{grid_rows})"
        )

        return (sequence_size, sequence_size)

    def get_sequence_position(self, index: int, grid_cols: int) -> tuple[int, int]:
        """
        Get grid position for a sequence index.

        Args:
            index: 0-based sequence index
            grid_cols: Number of columns in the grid

        Returns:
            Tuple of (column, row) position (0-based)
        """
        if grid_cols <= 0:
            return (0, 0)

        col = index % grid_cols
        row = index // grid_cols

        return (col, row)

    def calculate_total_grid_size(
        self, sequence_count: int, sequence_size: int, padding: int = 10
    ) -> tuple[int, int]:
        """
        Calculate total size needed for a grid of sequences.

        Args:
            sequence_count: Number of sequences
            sequence_size: Size of each sequence (assumed square)
            padding: Padding between sequences

        Returns:
            Tuple of (total_width, total_height) needed
        """
        if sequence_count <= 0:
            return (0, 0)

        grid_cols, grid_rows = self.calculate_grid_dimensions(sequence_count)

        total_width = (grid_cols * sequence_size) + ((grid_cols + 1) * padding)
        total_height = (grid_rows * sequence_size) + ((grid_rows + 1) * padding)

        return (total_width, total_height)

    def get_sequence_rect(
        self, index: int, grid_cols: int, sequence_size: int, padding: int = 10
    ) -> tuple[int, int, int, int]:
        """
        Get the bounding rectangle for a sequence at the given index.

        Args:
            index: 0-based sequence index
            grid_cols: Number of columns in the grid
            sequence_size: Size of each sequence (assumed square)
            padding: Padding between sequences

        Returns:
            Tuple of (x, y, width, height) for the sequence rectangle
        """
        col, row = self.get_sequence_position(index, grid_cols)

        x = padding + (col * (sequence_size + padding))
        y = padding + (row * (sequence_size + padding))

        return (x, y, sequence_size, sequence_size)

    def find_sequence_at_position(
        self, x: int, y: int, sequence_count: int, sequence_size: int, padding: int = 10
    ) -> int:
        """
        Find which sequence index is at a given position.

        Args:
            x: X coordinate
            y: Y coordinate
            sequence_count: Total number of sequences
            sequence_size: Size of each sequence
            padding: Padding between sequences

        Returns:
            Sequence index, or -1 if no sequence at that position
        """
        grid_cols, grid_rows = self.calculate_grid_dimensions(sequence_count)

        # Calculate which grid cell this position is in
        cell_width = sequence_size + padding
        cell_height = sequence_size + padding

        # Adjust for initial padding offset
        adjusted_x = x - padding
        adjusted_y = y - padding

        if adjusted_x < 0 or adjusted_y < 0:
            return -1

        col = adjusted_x // cell_width
        row = adjusted_y // cell_height

        # Check if within grid bounds
        if col >= grid_cols or row >= grid_rows:
            return -1

        # Calculate sequence index
        index = (row * grid_cols) + col

        # Check if index is valid (not beyond sequence count)
        if index >= sequence_count:
            return -1

        # Check if position is actually within the sequence bounds (not in padding area)
        seq_x = padding + (col * cell_width)
        seq_y = padding + (row * cell_height)

        if (
            x >= seq_x
            and x < seq_x + sequence_size
            and y >= seq_y
            and y < seq_y + sequence_size
        ):
            return index

        return -1

    def set_size_constraints(self, min_size: int, max_size: int) -> None:
        """
        Update the size constraints for sequences.

        Args:
            min_size: Minimum sequence size
            max_size: Maximum sequence size
        """
        self.min_sequence_size = max(50, min_size)  # Absolute minimum
        self.max_sequence_size = max(self.min_sequence_size, max_size)

        logger.info(
            f"Updated size constraints: {self.min_sequence_size}-{self.max_sequence_size}"
        )

    def get_recommended_dimensions_for_space(
        self,
        available_width: int,
        available_height: int,
        sequence_count: int,
        padding: int = 10,
    ) -> tuple[int, int, int]:
        """
        Get recommended grid dimensions and sequence size for available space.

        Args:
            available_width: Available width
            available_height: Available height
            sequence_count: Number of sequences to fit
            padding: Padding between sequences

        Returns:
            Tuple of (grid_cols, grid_rows, sequence_size)
        """
        if sequence_count <= 0:
            return (0, 0, self.min_sequence_size)

        best_cols, best_rows = self.calculate_grid_dimensions(sequence_count)
        sequence_width, sequence_height = self.calculate_sequence_size(
            available_width, available_height, best_cols, best_rows, padding
        )

        # Use the smaller dimension for square sequences
        sequence_size = min(sequence_width, sequence_height)

        return (best_cols, best_rows, sequence_size)
