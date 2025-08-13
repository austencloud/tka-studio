"""
Option Sizing Service - Pure Calculation Logic

Handles sizing calculations without Qt dependencies.
Extracted from multiple presentation files to maintain clean architecture.
"""

from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)


class OptionPickerSizeCalculator:
    """
    Pure service for option sizing calculations.

    No Qt dependencies - returns pure calculation results.
    """

    def __init__(self):
        """Initialize sizing service with default parameters."""
        self._min_frame_size = 60
        self._border_ratio = 0.015

    def calculate_section_dimensions(
        self,
        letter_type: LetterType,
        main_window_width: int,
    ) -> dict[str, int]:
        """
        Calculate section layout dimensions.

        FIXED: Use legacy calculation logic to match legacy behavior exactly.
        Returns dimension dictionary - presentation layer applies to Qt layouts.
        """
        try:
            # FIXED: Use legacy logic exactly
            # Legacy: width = self.mw_size_provider().width() // 2
            # But main_window_width is now the scroll area width, so use it directly
            base_width = main_window_width  # This is actually the scroll area width

            if letter_type in [LetterType.TYPE1, LetterType.TYPE2, LetterType.TYPE3]:
                # Individual sections: use FULL base width (matches legacy)
                section_width = base_width
                return {
                    "width": section_width,
                    "columns": 8,
                    "section_type": "individual",
                }

            elif letter_type in [LetterType.TYPE4, LetterType.TYPE5, LetterType.TYPE6]:
                # FIXED: Each individual grouped section gets 1/3 of the available width
                # They are displayed side by side, so each one should be 1/3 width
                section_width = base_width // 3

                return {
                    "width": section_width,
                    "columns": 8,  # Keep 8 columns for consistency
                    "section_type": "grouped_individual",
                }

            else:
                # Fallback for unknown types
                return {
                    "width": base_width,
                    "columns": 8,
                    "section_type": "fallback",
                }

        except Exception as e:
            print(f"❌ [OPTION_SIZING] Error calculating section dimensions: {e}")
            return {
                "width": 400,  # Fallback width
                "columns": 8,
                "section_type": "error",
            }

    def calculate_option_frame_size(
        self, main_window_size, option_picker_width: int, spacing: int = 3
    ) -> int:
        """
        Calculate frame size using improved sizing strategy.

        FIXED: Adjusted calculation to account for container-based option picker sizing.
        The legacy formula assumed option picker was exactly half the main window width,
        but now it's constrained to fit within its container panel.
        """
        try:
            main_window_width = main_window_size.width()

            # SIMPLIFIED: Use the standard legacy formula without artificial compensation
            # Since option picker now uses full container width, no compensation needed
            size_option_1 = main_window_width // 16
            size_option_2 = option_picker_width // 8
            base_size = max(size_option_1, size_option_2)

            # Calculate border width using existing method
            border_width = self.calculate_border_width(base_size)

            # Adjust for border and spacing (Legacy: size -= 2 * bw + spacing)
            adjusted_size = base_size - (2 * border_width) - spacing

            # Apply minimum size constraint
            final_size = max(adjusted_size, self._min_frame_size)

            return final_size

        except Exception as e:
            print(f"❌ [OPTION_SIZING] Error calculating frame size: {e}")
            return self._min_frame_size

    def calculate_border_width(self, base_size: int) -> int:
        """
        Calculate border width for frames.

        Legacy formula: max(1, int(size * 0.015))
        """
        try:
            return max(1, int(base_size * self._border_ratio))
        except Exception:
            return 1

    def apply_size_constraints(self, size: int) -> int:
        """
        Apply size constraints to ensure reasonable frame sizes.

        Args:
            size: Calculated size

        Returns:
            Size with constraints applied
        """
        return max(size, self._min_frame_size)

    def calculate_frame_dimensions(
        self, main_window_size, option_picker_width: int, spacing: int = 3
    ) -> dict[str, int]:
        """
        Calculate complete frame dimensions including padding.

        Returns dictionary with frame_size, component_size, and padding.
        """
        try:
            # Calculate the component size
            component_size = self.calculate_option_frame_size(
                main_window_size, option_picker_width, spacing
            )

            # Frame size includes padding (Legacy: +8 for frame padding)
            frame_padding = 0
            frame_size = component_size + frame_padding

            return {
                "component_size": component_size,
                "frame_size": frame_size,
                "padding": frame_padding,
                "border_width": self.calculate_border_width(component_size),
            }

        except Exception as e:
            print(f"❌ [OPTION_SIZING] Error calculating frame dimensions: {e}")
            fallback_size = self._min_frame_size
            return {
                "component_size": fallback_size,
                "frame_size": fallback_size + 8,
                "padding": 8,
                "border_width": 1,
            }
