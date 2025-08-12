"""
Beat Layout Settings Manager Implementation

Implements beat frame layout settings management with dynamic layout
calculation and QSettings persistence.
"""

from __future__ import annotations

import logging
import math

from PyQt6.QtCore import QObject, QSettings, pyqtSignal


logger = logging.getLogger(__name__)


class BeatLayoutSettingsManager(QObject):
    """
    Implementation of beat layout settings management using QSettings.

    Features:
    - Dynamic layout calculation based on sequence length
    - Customizable layouts for specific sequence lengths
    - Smart defaults with optimal aspect ratios
    - Layout validation and optimization
    - Event notifications for layout changes
    """

    layout_changed = pyqtSignal(int, int, int)  # sequence_length, rows, cols

    # Default sequence length
    DEFAULT_SEQUENCE_LENGTH = 16

    # Predefined optimal layouts for common sequence lengths
    OPTIMAL_LAYOUTS = {
        1: (1, 1),
        2: (1, 2),
        3: (1, 3),
        4: (2, 2),
        5: (1, 5),
        6: (2, 3),
        7: (1, 7),
        8: (2, 4),
        9: (3, 3),
        10: (2, 5),
        12: (3, 4),
        15: (3, 5),
        16: (4, 4),
        20: (4, 5),
        24: (4, 6),
        25: (5, 5),
        30: (5, 6),
        32: (4, 8),
        36: (6, 6),
        40: (5, 8),
        48: (6, 8),
        50: (5, 10),
        64: (8, 8),
    }

    def __init__(self, settings: QSettings):
        super().__init__()
        self.settings = settings
        logger.debug("Initialized BeatLayoutSettingsManager")

    def get_layout_for_length(self, sequence_length: int) -> tuple[int, int]:
        """
        Get the layout (rows, cols) for a given sequence length.

        Args:
            sequence_length: Length of the sequence

        Returns:
            Tuple of (rows, columns) for the layout
        """
        try:
            if sequence_length <= 0:
                logger.warning(f"Invalid sequence length: {sequence_length}")
                return (1, 1)

            # Check for custom setting first
            custom_layout = self._get_custom_layout(sequence_length)
            if custom_layout:
                return custom_layout

            # Use predefined optimal layout if available
            if sequence_length in self.OPTIMAL_LAYOUTS:
                return self.OPTIMAL_LAYOUTS[sequence_length]

            # Calculate optimal layout dynamically
            return self._calculate_optimal_layout(sequence_length)

        except Exception as e:
            logger.exception(f"Failed to get layout for length {sequence_length}: {e}")
            return (1, max(1, sequence_length))

    def set_layout_for_length(self, sequence_length: int, rows: int, cols: int) -> None:
        """
        Set the layout for a specific sequence length.

        Args:
            sequence_length: Length of the sequence
            rows: Number of rows
            cols: Number of columns
        """
        try:
            if not self._validate_layout(sequence_length, rows, cols):
                logger.warning(
                    f"Invalid layout: {rows}x{cols} for length {sequence_length}"
                )
                return

            # Get old layout for comparison
            old_layout = self.get_layout_for_length(sequence_length)

            # Set custom layout
            key = f"layout/custom_{sequence_length}"
            layout_value = f"{rows},{cols}"
            self.settings.setValue(key, layout_value)
            self.settings.sync()

            # Emit change event if layout actually changed
            if old_layout != (rows, cols):
                self.layout_changed.emit(sequence_length, rows, cols)
                logger.info(
                    f"Layout for length {sequence_length} changed to {rows}x{cols}"
                )

        except Exception as e:
            logger.exception(f"Failed to set layout for length {sequence_length}: {e}")

    def get_default_sequence_length(self) -> int:
        """
        Get the default sequence length setting.

        Returns:
            Default sequence length
        """
        try:
            return self.settings.value(
                "layout/default_sequence_length", self.DEFAULT_SEQUENCE_LENGTH, type=int
            )
        except Exception as e:
            logger.exception(f"Failed to get default sequence length: {e}")
            return self.DEFAULT_SEQUENCE_LENGTH

    def set_default_sequence_length(self, length: int) -> None:
        """
        Set the default sequence length.

        Args:
            length: Default sequence length (must be positive)
        """
        try:
            if length <= 0:
                logger.warning(f"Invalid default sequence length: {length}")
                return

            old_length = self.get_default_sequence_length()

            self.settings.setValue("layout/default_sequence_length", length)
            self.settings.sync()

            if old_length != length:
                logger.info(
                    f"Default sequence length changed from {old_length} to {length}"
                )

        except Exception as e:
            logger.exception(f"Failed to set default sequence length: {e}")

    def get_layout_options_for_length(
        self, sequence_length: int
    ) -> dict[str, tuple[int, int]]:
        """
        Get available layout options for a sequence length.

        Args:
            sequence_length: Length of the sequence

        Returns:
            Dictionary mapping layout descriptions to (rows, cols) tuples
        """
        try:
            if sequence_length <= 0:
                return {"1x1": (1, 1)}

            options = {}

            # Add single row option
            options[f"1x{sequence_length}"] = (1, sequence_length)

            # Add single column option if length > 1
            if sequence_length > 1:
                options[f"{sequence_length}x1"] = (sequence_length, 1)

            # Add factorization options
            factors = self._get_factors(sequence_length)
            for rows in factors:
                cols = sequence_length // rows
                if 1 <= rows <= cols <= sequence_length:
                    # Calculate aspect ratio quality (closer to square is better)
                    aspect_ratio = max(rows, cols) / min(rows, cols)
                    if aspect_ratio <= 3.0:  # Reasonable aspect ratios only
                        desc = f"{rows}x{cols}"
                        if rows == cols:
                            desc += " (Square)"
                        elif (rows, cols) == self.OPTIMAL_LAYOUTS.get(sequence_length):
                            desc += " (Optimal)"
                        options[desc] = (rows, cols)

            # Add current custom setting if different
            current = self.get_layout_for_length(sequence_length)
            current_desc = f"{current[0]}x{current[1]}"
            if current_desc not in [desc.split()[0] for desc in options]:
                options[f"{current_desc} (Current)"] = current

            return options

        except Exception as e:
            logger.exception(
                f"Failed to get layout options for length {sequence_length}: {e}"
            )
            return {"1x1": (1, 1)}

    def _get_custom_layout(self, sequence_length: int) -> tuple[int, int] | None:
        """Get custom layout setting if it exists."""
        try:
            key = f"layout/custom_{sequence_length}"
            layout_str = self.settings.value(key, None, type=str)

            if layout_str:
                parts = layout_str.split(",")
                if len(parts) == 2:
                    rows, cols = int(parts[0]), int(parts[1])
                    if self._validate_layout(sequence_length, rows, cols):
                        return (rows, cols)

            return None

        except Exception as e:
            logger.exception(f"Failed to get custom layout for {sequence_length}: {e}")
            return None

    def _calculate_optimal_layout(self, sequence_length: int) -> tuple[int, int]:
        """Calculate optimal layout for a sequence length."""
        try:
            # Find the factors closest to square root for best aspect ratio
            math.sqrt(sequence_length)
            best_rows = 1
            best_cols = sequence_length
            min_aspect_ratio = float("inf")

            for rows in range(1, sequence_length + 1):
                if sequence_length % rows == 0:
                    cols = sequence_length // rows
                    aspect_ratio = max(rows, cols) / min(rows, cols)

                    # Prefer layouts closer to square
                    if aspect_ratio < min_aspect_ratio:
                        min_aspect_ratio = aspect_ratio
                        best_rows = rows
                        best_cols = cols

            return (best_rows, best_cols)

        except Exception as e:
            logger.exception(
                f"Failed to calculate optimal layout for {sequence_length}: {e}"
            )
            return (1, sequence_length)

    def _validate_layout(self, sequence_length: int, rows: int, cols: int) -> bool:
        """Validate that a layout is valid for the sequence length."""
        try:
            if rows <= 0 or cols <= 0:
                return False

            if rows * cols < sequence_length:
                return False

            # Allow some extra space but not too much waste
            return not rows * cols > sequence_length * 2

        except Exception:
            return False

    def _get_factors(self, n: int) -> list[int]:
        """Get all factors of a number."""
        factors = []
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                factors.append(i)
                if i != n // i:
                    factors.append(n // i)
        return sorted(factors)
