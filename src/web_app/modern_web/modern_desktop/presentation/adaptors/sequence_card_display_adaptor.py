"""
Qt Adaptor for Sequence Card Display Service

Bridges between the framework-agnostic display service and Qt UI components.
Converts service callbacks to Qt signals for UI communication.
"""

from __future__ import annotations

import logging
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.core.interfaces.sequence_card_services import (
    DisplayState,
    ISequenceCardDisplayService,
    SequenceCardData,
)


logger = logging.getLogger(__name__)


class SequenceCardDisplayAdaptor(QObject):
    """Qt adaptor for sequence card display service."""

    # Qt signals for UI communication
    sequences_loaded = pyqtSignal(
        list
    )  # Emitted when sequences are loaded and ready for display
    loading_state_changed = pyqtSignal(bool)  # Emitted when loading state changes
    progress_updated = pyqtSignal(int, int)  # Emitted with (current, total) progress

    def __init__(
        self,
        display_service: ISequenceCardDisplayService,
        parent: Optional[QObject] = None,
    ):
        """
        Initialize the Qt adaptor.

        Args:
            display_service: The framework-agnostic display service
            parent: Parent QObject
        """
        super().__init__(parent)
        self.display_service = display_service

        # Set up callbacks to bridge service to Qt signals
        self._setup_service_callbacks()

        logger.info("Sequence card display adaptor initialized")

    def _setup_service_callbacks(self) -> None:
        """Set up callbacks to convert service notifications to Qt signals."""
        # Set callback for sequences loaded
        self.display_service.set_sequences_loaded_callback(self._on_sequences_loaded)

        # Set callback for loading state changes
        self.display_service.set_loading_state_callback(self._on_loading_state_changed)

        # Set callback for progress updates
        self.display_service.set_progress_callback(self._on_progress_updated)

    def _on_sequences_loaded(self, sequences: list[SequenceCardData]) -> None:
        """Handle sequences loaded callback from service."""
        logger.info(
            f"Adaptor: sequences loaded, emitting signal with {len(sequences)} sequences"
        )
        self.sequences_loaded.emit(sequences)

    def _on_loading_state_changed(self, is_loading: bool) -> None:
        """Handle loading state change callback from service."""
        logger.info(f"Adaptor: loading state changed to {is_loading}")
        self.loading_state_changed.emit(is_loading)

    def _on_progress_updated(self, current: int, total: int) -> None:
        """Handle progress update callback from service."""
        self.progress_updated.emit(current, total)

    # Delegate methods to the underlying service
    def display_sequences(self, length: int, column_count: int) -> None:
        """Display sequences of specified length."""
        logger.info(
            f"Adaptor: display_sequences called with length={length}, columns={column_count}"
        )
        self.display_service.display_sequences(length, column_count)

    def get_display_state(self) -> DisplayState:
        """Get current display state."""
        return self.display_service.get_display_state()

    def cancel_current_operation(self) -> None:
        """Cancel current loading operation."""
        self.display_service.cancel_current_operation()

    def get_current_sequences(self) -> list[SequenceCardData]:
        """Get currently loaded sequences."""
        return self.display_service.get_current_sequences()
