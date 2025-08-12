"""
Option Picker Size Service

Platform-agnostic service for option picker sizing calculations and validation.
Contains pure business logic extracted from OptionPickerSizeManager.
"""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtCore import QSize


class OptionPickerSizeService:
    """
    Platform-agnostic service for option picker sizing calculations.

    Responsibilities:
    - Calculating optimal picker width based on available space
    - Validating picker width accuracy
    - Defining sizing rules and constraints
    """

    def __init__(self, mw_size_provider: Callable[[], QSize]):
        self._mw_size_provider = mw_size_provider
        self._last_calculated_width = 0
        self._sizing_deferred_count = 0
        self._max_deferred_attempts = 10

    def calculate_optimal_width(self, parent_width: int = 0) -> int:
        """Calculate optimal picker width based on parent and main window."""
        # First try to use parent width if available
        if parent_width > 0:
            # Validate parent width is reasonable
            if parent_width > 640:  # Not default/initial width
                self._last_calculated_width = parent_width
                return parent_width

        # Fallback to main window calculation
        main_window_size = self._mw_size_provider()
        if main_window_size.width() > 1000:
            # Use half the main window width as a reasonable estimate
            available_width = main_window_size.width() // 2
            self._last_calculated_width = available_width
            return available_width

        # Final fallback for very small windows
        fallback_width = 400
        self._last_calculated_width = fallback_width
        return fallback_width

    def is_width_accurate(self, picker_width: int) -> bool:
        """Check if the picker width appears accurate and not from premature measurement."""
        try:
            # Width should be positive
            if picker_width <= 0:
                return False

            # Get main window size for validation
            main_window_size = self._mw_size_provider()
            main_window_width = main_window_size.width()

            if main_window_width <= 0:
                return False

            # Picker width should be between 20% and 80% of main window width
            # (typical range for option picker in a layout)
            min_expected = main_window_width * 0.2
            max_expected = main_window_width * 0.8

            if not (min_expected <= picker_width <= max_expected):
                return False

            # Additional check: avoid the specific problematic width (622px)
            # This suggests the widget was measured during an intermediate layout state
            return picker_width != 622

        except Exception:
            return False

    def should_defer_sizing(self) -> bool:
        """Check if sizing should be deferred due to startup conditions."""
        if self._sizing_deferred_count >= self._max_deferred_attempts:
            return False

        self._sizing_deferred_count += 1
        return True

    def reset_deferred_count(self) -> None:
        """Reset the deferred sizing count."""
        self._sizing_deferred_count = 0

    def get_sizing_delay(self, during_startup: bool = False) -> int:
        """Get appropriate delay for sizing operations."""
        return 500 if during_startup else 50

    def get_layout_constraints(self) -> dict:
        """Get layout constraints and sizing rules."""
        return {
            "min_width": 200,
            "max_width_ratio": 0.8,  # 80% of main window
            "min_width_ratio": 0.2,  # 20% of main window
            "default_fallback_width": 400,
            "problematic_widths": [622],  # Known problematic widths
            "reasonable_parent_threshold": 640,
        }
