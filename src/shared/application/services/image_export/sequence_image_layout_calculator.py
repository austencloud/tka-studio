"""
Modern Layout Calculator

This service calculates optimal layouts and dimensions for exported images,
replicating the legacy system's layout logic exactly.
"""

import logging
import math

from desktop.modern.core.interfaces.image_export_services import (
    ISequenceImageLayoutCalculator,
)

logger = logging.getLogger(__name__)


class SequenceImageLayoutCalculator(ISequenceImageLayoutCalculator):
    """
    Modern implementation of layout calculator.

    This calculator replicates the legacy system's layout logic exactly,
    ensuring exported images have the same dimensions and proportions.
    """

    def __init__(self):
        # EXACT legacy layout mappings from default_layouts.json
        # Legacy format is [rows, columns], we convert to (columns, rows) for modern use
        # CRITICAL: These must match legacy exactly for pixel-perfect output
        self.layout_mappings = {
            1: (1, 1),  # Legacy: [1, 1] -> (1 col, 1 row)
            2: (2, 1),  # Legacy: [1, 2] -> (2 cols, 1 row)
            3: (3, 1),  # Legacy: [1, 3] -> (3 cols, 1 row)
            4: (4, 1),  # Legacy: [1, 4] -> (4 cols, 1 row)
            5: (4, 2),  # Legacy: [2, 4] -> (4 cols, 2 rows)
            6: (4, 2),  # Legacy: [2, 4] -> (4 cols, 2 rows)
            7: (4, 2),  # Legacy: [2, 4] -> (4 cols, 2 rows)
            8: (4, 2),  # Legacy: [2, 4] -> (4 cols, 2 rows)
            9: (4, 3),  # Legacy: [3, 4] -> (4 cols, 3 rows)
            10: (4, 3),  # Legacy: [3, 4] -> (4 cols, 3 rows)
            11: (4, 3),  # Legacy: [3, 4] -> (4 cols, 3 rows)
            12: (3, 4),  # Legacy: [4, 3] -> (3 cols, 4 rows) - CRITICAL FIX!
            13: (4, 4),  # Legacy: [4, 4] -> (4 cols, 4 rows)
            14: (4, 4),  # Legacy: [4, 4] -> (4 cols, 4 rows)
            15: (4, 4),  # Legacy: [4, 4] -> (4 cols, 4 rows)
            16: (4, 4),  # Legacy: [4, 4] -> (4 cols, 4 rows)
            17: (5, 4),  # Legacy: [4, 5] -> (5 cols, 4 rows)
            18: (5, 4),  # Legacy: [4, 5] -> (5 cols, 4 rows)
            19: (5, 4),  # Legacy: [4, 5] -> (5 cols, 4 rows)
            20: (5, 4),  # Legacy: [4, 5] -> (5 cols, 4 rows)
            21: (4, 6),  # Legacy: [6, 4] -> (4 cols, 6 rows)
            22: (4, 6),  # Legacy: [6, 4] -> (4 cols, 6 rows)
            23: (4, 6),  # Legacy: [6, 4] -> (4 cols, 6 rows)
            24: (4, 6),  # Legacy: [6, 4] -> (4 cols, 6 rows)
            25: (4, 7),  # Legacy: [7, 4] -> (4 cols, 7 rows)
        }

    def calculate_layout(
        self, num_beats: int, include_start_position: bool
    ) -> tuple[int, int]:
        """
        Calculate optimal layout (columns, rows) for the given number of beats.

        This replicates the legacy layout calculation logic exactly.
        """
        logger.debug(
            f"Calculating layout for {num_beats} beats, include_start_position={include_start_position}"
        )

        # EXACT legacy logic replication:
        # 1. First get the base layout for just the beats (without start position)
        # 2. Then adjust if start position is included

        # Handle edge cases
        if num_beats <= 0:
            return (1, 1)

        # Get base layout for beats only (using default_layouts.json mappings)
        if num_beats in self.layout_mappings:
            base_columns, base_rows = self.layout_mappings[num_beats]
        else:
            # For larger sequences, calculate dynamically
            base_columns, base_rows = self._calculate_dynamic_layout(num_beats)

        # Apply legacy start position logic:
        # If including start position, add an extra column
        if include_start_position and num_beats > 0:
            columns = base_columns + 1
            rows = base_rows
        else:
            columns = base_columns
            rows = base_rows

        logger.debug(f"Base layout for {num_beats} beats: {base_columns}x{base_rows}")
        logger.debug(
            f"Final layout with include_start_position={include_start_position}: {columns}x{rows}"
        )

        return (columns, rows)

    def calculate_image_dimensions(
        self, columns: int, rows: int, beat_size: int, additional_height: int = 0
    ) -> tuple[int, int]:
        """
        Calculate image dimensions based on layout.

        This replicates the legacy dimension calculation exactly.
        """
        logger.debug(
            f"Calculating dimensions for {columns}x{rows} layout, beat_size={beat_size}, additional_height={additional_height}"
        )

        # Legacy calculation: simple multiplication
        width = columns * beat_size
        height = rows * beat_size + additional_height

        # Ensure minimum dimensions
        width = max(width, 300)  # Minimum width
        height = max(height, 300)  # Minimum height

        logger.debug(f"Calculated dimensions: {width}x{height}")
        return (width, height)

    def _calculate_dynamic_layout(self, total_positions: int) -> tuple[int, int]:
        """
        Calculate layout dynamically for sequences larger than predefined mappings.

        This uses the same algorithm as the legacy system for consistency.
        """
        # Legacy algorithm: try to create a roughly square layout
        # with a slight preference for wider layouts

        # Start with square root as base
        sqrt_positions = math.sqrt(total_positions)

        # Try different column counts around the square root
        best_columns = int(sqrt_positions)
        best_rows = math.ceil(total_positions / best_columns)
        best_aspect_ratio = abs(
            best_columns / best_rows - 1.0
        )  # Closer to 1.0 is more square

        # Test nearby column counts
        for test_columns in range(max(1, best_columns - 2), best_columns + 3):
            test_rows = math.ceil(total_positions / test_columns)

            # Skip if this creates too many empty positions
            if test_columns * test_rows - total_positions > test_columns:
                continue

            # Calculate aspect ratio (prefer slightly wider layouts)
            aspect_ratio = test_columns / test_rows
            aspect_ratio_score = abs(
                aspect_ratio - 1.2
            )  # Prefer 1.2:1 ratio (slightly wider)

            # Update if this is better
            if aspect_ratio_score < best_aspect_ratio:
                best_columns = test_columns
                best_rows = test_rows
                best_aspect_ratio = aspect_ratio_score

        return (best_columns, best_rows)

    def get_layout_for_sequence_length(self, sequence_length: int) -> tuple[int, int]:
        """
        Get the standard layout for a given sequence length.

        This is a convenience method that uses the most common settings.
        """
        return self.calculate_layout(sequence_length, include_start_position=True)

    def calculate_beat_positions(
        self, num_beats: int, columns: int, rows: int, beat_size: int, margin: int = 10
    ) -> list[tuple[int, int]]:
        """
        Calculate the pixel positions for each beat in the layout.

        Returns a list of (x, y) coordinates for each beat position.
        """
        positions = []

        for i in range(num_beats):
            row = i // columns
            col = i % columns

            x = margin + col * (beat_size + margin)
            y = margin + row * (beat_size + margin)

            positions.append((x, y))

        return positions

    def calculate_optimal_beat_size(
        self,
        target_width: int,
        target_height: int,
        columns: int,
        rows: int,
        additional_height: int = 0,
    ) -> int:
        """
        Calculate optimal beat size to fit within target dimensions.

        This is useful for creating images that fit specific size constraints.
        """
        # Calculate available space
        available_width = target_width
        available_height = target_height - additional_height

        # Calculate beat size based on constraints
        beat_size_by_width = available_width // columns
        beat_size_by_height = available_height // rows

        # Use the smaller constraint to ensure everything fits
        optimal_beat_size = min(beat_size_by_width, beat_size_by_height)

        # Ensure minimum beat size
        optimal_beat_size = max(optimal_beat_size, 100)

        logger.debug(
            f"Calculated optimal beat size: {optimal_beat_size} for target {target_width}x{target_height}"
        )
        return optimal_beat_size

    def validate_layout(self, columns: int, rows: int, num_beats: int) -> bool:
        """
        Validate that a layout can accommodate the required number of beats.

        Returns True if the layout is valid, False otherwise.
        """
        total_positions = columns * rows
        return total_positions >= num_beats

    def get_layout_efficiency(self, columns: int, rows: int, num_beats: int) -> float:
        """
        Calculate layout efficiency (how well the layout uses available space).

        Returns a value between 0.0 and 1.0, where 1.0 means perfect efficiency.
        """
        if columns <= 0 or rows <= 0:
            return 0.0

        total_positions = columns * rows
        if total_positions == 0:
            return 0.0

        efficiency = num_beats / total_positions
        return min(1.0, efficiency)  # Cap at 1.0
