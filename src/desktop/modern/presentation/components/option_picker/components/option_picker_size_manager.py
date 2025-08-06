"""
OptionPickerSizeManager

Qt-specific wrapper for OptionPickerSizeService.
Handles Qt widget interactions and timing.
"""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtWidgets import QWidget

from desktop.modern.application.services.option_picker.option_picker_size_service import (
    OptionPickerSizeService,
)


class OptionPickerSizeManager:
    """
    Qt-specific manager for option picker sizing.

    Responsibilities:
    - Qt widget interactions and measurements
    - UI timing and readiness checks
    - Bridging Qt widgets with platform-agnostic service
    """

    def __init__(self, widget: QWidget, mw_size_provider: Callable[[], QSize]):
        self._widget = widget
        self._size_service = OptionPickerSizeService(mw_size_provider)
        self._mw_size_provider = mw_size_provider
        self._sizing_deferred_count = 0
        self._max_deferred_attempts = 10
        self._last_calculated_width = 0

    def calculate_optimal_width(self) -> int:
        """Calculate optimal picker width using legacy-style approach."""
        try:
            # Try to get the parent container width (similar to legacy approach)
            if self._widget.parent():
                parent_width = self._widget.parent().width()
                if parent_width > 100:  # Valid width
                    self._last_calculated_width = parent_width
                    return parent_width

            # Fallback to main window calculation (legacy: parent().parent().width() // 2)
            main_window_size = self._mw_size_provider()
            if main_window_size.width() > 800:
                # Use half the main window width (legacy approach)
                calculated_width = main_window_size.width() // 2
                self._last_calculated_width = calculated_width
                return calculated_width

            # Final fallback
            fallback_width = 400
            self._last_calculated_width = fallback_width
            return fallback_width

        except Exception as e:
            print(f"⚠️ [SIZING] Error calculating width: {e}")
            self._last_calculated_width = 400
            return 400

    def is_width_accurate(self, picker_width: int) -> bool:
        """Check if the picker width appears accurate - percentage-based validation."""
        # Simple check: width should be positive
        if picker_width <= 0:
            return False

        # Get main window size for percentage calculations
        try:
            main_window_size = self._mw_size_provider()
            main_window_width = main_window_size.width()

            if main_window_width > 0:
                # Calculate percentage of main window width
                percentage = (picker_width / main_window_width) * 100

                # Valid range: 20% to 80% of main window width
                if percentage < 20 or percentage > 80:
                    return False

                # Check for known problematic widths
                if picker_width == 622:
                    return False

                return True
            # Fallback to absolute values if main window size unavailable
            return 200 <= picker_width <= 2000

        except Exception:
            # Fallback to absolute values on error
            return 200 <= picker_width <= 2000

    def is_ui_ready_for_sizing(self) -> bool:
        """Check if the UI is ready for accurate sizing calculations."""
        try:
            # Check if main window is visible and properly initialized
            main_window = self._widget.window()
            if not main_window:
                return False

            # Check if main window is visible (not during splash screen)
            if not main_window.isVisible():
                return False

            # Check if this widget is visible and has been shown
            if not self._widget.isVisible():
                return False

            # Check if widget has been properly sized (not default/zero size)
            if self._widget.width() <= 0 or self._widget.height() <= 0:
                return False

            return True

        except Exception:
            return False

    def should_defer_sizing(self) -> bool:
        """Check if sizing should be deferred due to startup conditions."""
        if not self.is_ui_ready_for_sizing():
            return self._size_service.should_defer_sizing()

        self._size_service.reset_deferred_count()
        return False

    def get_sizing_delay(self, during_startup: bool = False) -> int:
        """Get appropriate delay for sizing operations."""
        return self._size_service.get_sizing_delay(during_startup)

    def get_layout_constraints(self) -> dict:
        """Get layout constraints and sizing rules."""
        return self._size_service.get_layout_constraints()

    def is_during_startup(self) -> bool:
        """Check if we're currently during application startup phase."""
        try:
            # Check if main window is not yet visible (splash screen phase)
            main_window = self._widget.window()
            if not main_window or not main_window.isVisible():
                return True

            # Check if this widget hasn't been properly shown yet
            if not self._widget.isVisible() or self._widget.width() <= 0:
                return True

            return False

        except Exception:
            # If we can't determine, assume we're during startup to be safe
            return True

    def defer_sizing_if_needed(
        self, sizing_callback: Callable, immediate: bool = False
    ) -> bool:
        """
        Defer sizing if UI is not ready or width is inaccurate.

        Args:
            sizing_callback: Function to call when ready
            immediate: If True, don't defer and return False if not ready

        Returns:
            True if sizing was deferred, False if ready to proceed
        """
        if immediate:
            return False

        if not self.is_ui_ready_for_sizing():
            self._sizing_deferred_count += 1

            if self._sizing_deferred_count < self._max_deferred_attempts:
                QTimer.singleShot(100, sizing_callback)
                return True
            print("⚠️ [SIZING] Max deferred attempts reached, proceeding anyway")
            self._sizing_deferred_count = 0
            return False

        current_width = self._widget.width()
        if not self.is_width_accurate(current_width):
            print("⚠️ [SIZING] Width appears inaccurate, deferring...")
            self._sizing_deferred_count += 1

            if self._sizing_deferred_count < self._max_deferred_attempts:
                QTimer.singleShot(200, sizing_callback)
                return True
            print("⚠️ [SIZING] Max deferred attempts reached, proceeding anyway")
            self._sizing_deferred_count = 0
            return False

        # Ready to proceed
        self._sizing_deferred_count = 0
        return False

    def get_startup_delay(self) -> int:
        """Get appropriate delay based on startup state."""
        return 500 if self.is_during_startup() else 50

    def get_last_calculated_width(self) -> int:
        """Get the last calculated width."""
        return self._last_calculated_width

    def reset_deferred_count(self):
        """Reset the deferred count (useful for testing)."""
        self._sizing_deferred_count = 0
