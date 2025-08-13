"""
Sequence Card Display Service Implementation

Handles display logic and UI coordination for sequence cards.
"""

from __future__ import annotations

from collections.abc import Callable
import logging

from desktop.modern.core.interfaces.sequence_card_services import (
    DisplayState,
    ISequenceCardDisplayService,
)


logger = logging.getLogger(__name__)


class SequenceCardDisplayService(ISequenceCardDisplayService):
    """Implementation of sequence card display operations."""

    def __init__(self):
        """Initialize the display service."""
        self._display_state = DisplayState()
        self._progress_callback: Callable[[int, int], None] | None = None
        self._sequences_loaded_callback: Callable[[list], None] | None = None
        self._loading_state_callback: Callable[[bool], None] | None = None
        self._is_cancelled = False
        logger.info("SequenceCardDisplayService initialized")

    def display_sequences(self, length: int, column_count: int) -> None:
        """Display sequences of specified length."""
        logger.info(f"Displaying sequences: length={length}, columns={column_count}")
        self._display_state.is_loading = True
        self._display_state.current_length = length
        self._is_cancelled = False

        # TODO: Implement actual sequence loading logic
        # For now, just update the state
        self._display_state.is_loading = False

    def get_display_state(self) -> DisplayState:
        """Get current display state."""
        return self._display_state

    def cancel_current_operation(self) -> None:
        """Cancel current loading operation."""
        logger.info("Cancelling current display operation")
        self._is_cancelled = True
        self._display_state.is_loading = False

    def set_progress_callback(self, callback: Callable[[int, int], None]) -> None:
        """Set progress update callback."""
        self._progress_callback = callback

    def set_sequences_loaded_callback(self, callback: Callable[[list], None]) -> None:
        """Set sequences loaded callback."""
        self._sequences_loaded_callback = callback

    def set_loading_state_callback(self, callback: Callable[[bool], None]) -> None:
        """Set loading state change callback."""
        self._loading_state_callback = callback

    def format_sequence_data(self, data):
        """Format sequence data for display."""
        return data

    def update_display(self, sequence_data):
        """Update the display with new sequence data."""
        pass
