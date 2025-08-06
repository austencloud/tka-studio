"""
OptionPickerRefreshOrchestrator

Handles debounced loading and refresh coordination for option picker.
Manages the complex refresh logic with animation coordination.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from PyQt6.QtCore import QTimer

from desktop.modern.domain.models.sequence_data import SequenceData


if TYPE_CHECKING:
    from shared.application.services.option_picker.option_configuration_service import (
        OptionConfigurationService,
    )


class OptionPickerRefreshOrchestrator:
    """
    Orchestrates refresh operations for option picker.

    Responsibilities:
    - Managing debounced loading with timer
    - Coordinating refresh operations
    - Handling transition state management
    - Managing pending sequence data
    """

    def __init__(
        self,
        option_config_service: OptionConfigurationService,
        refresh_callback: Callable[[SequenceData], None],
    ):
        self._option_config_service = option_config_service
        self._refresh_callback = refresh_callback

        # State tracking
        self._pending_sequence_data: SequenceData | None = None
        self._is_preparing_for_transition = False

        # Debounced refresh setup
        debounce_delay = self._option_config_service.get_debounce_delay()
        self._refresh_timer = QTimer()
        self._refresh_timer.setSingleShot(True)
        self._refresh_timer.timeout.connect(self._perform_refresh)

    def load_options_from_sequence(self, sequence_data: SequenceData) -> None:
        """Load options with debouncing."""
        self._pending_sequence_data = sequence_data

        # Get debounce delay from config service
        delay = self._option_config_service.get_debounce_delay()
        self._refresh_timer.start(delay)

    def prepare_for_transition(self) -> None:
        """Prepare content for widget transition by loading without fade animations."""
        self._is_preparing_for_transition = True
        try:
            # If we have pending sequence data, load it directly without fades
            if self._pending_sequence_data:
                sequence_data = self._pending_sequence_data
                self._pending_sequence_data = None
                self._refresh_callback(sequence_data)
        finally:
            self._is_preparing_for_transition = False

    def _perform_refresh(self) -> None:
        """Perform refresh operation."""
        if self._pending_sequence_data is None:
            return

        sequence_data = self._pending_sequence_data
        self._pending_sequence_data = None

        try:
            # Delegate to the callback
            self._refresh_callback(sequence_data)
        except Exception as e:
            print(f"❌ [REFRESH] Error during refresh: {e}")

    def is_preparing_for_transition(self) -> bool:
        """Check if currently preparing for transition."""
        return self._is_preparing_for_transition
