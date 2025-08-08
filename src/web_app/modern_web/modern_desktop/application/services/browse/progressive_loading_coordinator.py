"""
Progressive Loading Coordinator

Coordinates progressive loading of sequences with chunk processing.
Handles the orchestration between progressive loading service and display components.
"""

from __future__ import annotations

from collections.abc import Callable
import logging

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

from desktop.modern.application.services.browse.progressive_loading_service import (
    ProgressiveLoadingService,
)
from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.views.browse.models import FilterType


logger = logging.getLogger(__name__)


class ProgressiveLoadingCoordinator(QObject):
    """
    Coordinates progressive loading operations.

    Acts as a bridge between the ProgressiveLoadingService and the UI components,
    handling chunk processing and coordinating display updates.
    """

    # Signals for coordinating with UI components
    loading_started = pyqtSignal(int)  # total_count
    chunk_processed = pyqtSignal(list)  # List[SequenceData] chunk
    loading_progress = pyqtSignal(int, int)  # current, total
    loading_completed = pyqtSignal(list)  # List[SequenceData] final_result
    loading_cancelled = pyqtSignal()

    def __init__(self, progressive_loading_service: ProgressiveLoadingService):
        """
        Initialize the coordinator.

        Args:
            progressive_loading_service: The service that handles actual progressive loading
        """
        super().__init__()
        self.progressive_loading_service = progressive_loading_service
        self.all_loaded_sequences: list[SequenceData] = []
        self._loading_cancelled = False

        # Callbacks for chunk processing
        self.chunk_display_callback: (
            Callable[[list[SequenceData], str], None] | None
        ) = None
        self.navigation_update_callback: Callable[[], None] | None = None

        self._connect_service_signals()

    def _connect_service_signals(self) -> None:
        """Connect to progressive loading service signals."""
        if self.progressive_loading_service:
            self.progressive_loading_service.loading_started.connect(
                self._on_service_loading_started
            )
            self.progressive_loading_service.sequences_chunk_loaded.connect(
                self._on_service_chunk_loaded
            )
            self.progressive_loading_service.loading_progress.connect(
                self._on_service_loading_progress
            )
            self.progressive_loading_service.loading_completed.connect(
                self._on_service_loading_completed
            )
            self.progressive_loading_service.loading_cancelled.connect(
                self._on_service_loading_cancelled
            )

    def start_progressive_loading(
        self,
        filter_type: FilterType,
        filter_value,
        chunk_size: int = 6,
        sort_method: str = "alphabetical",
    ) -> None:
        """
        Start progressive loading with coordination.

        Args:
            filter_type: Type of filter to apply
            filter_value: Filter value
            chunk_size: Number of sequences per chunk
            sort_method: Method for sorting sequences
        """
        logger.info(
            f"🚀 [COORDINATOR] Starting progressive loading: {filter_type.value} = {filter_value}"
        )

        # Reset state
        self.all_loaded_sequences.clear()
        self._loading_cancelled = False
        self._current_sort_method = sort_method

        # Start the progressive loading service
        if self.progressive_loading_service:
            self.progressive_loading_service.start_progressive_loading(
                filter_type, filter_value, chunk_size
            )
        else:
            logger.error("❌ [COORDINATOR] No progressive loading service available")

    def cancel_loading(self) -> None:
        """Cancel the current loading operation."""
        logger.info("⛔ [COORDINATOR] Cancelling progressive loading")
        self._loading_cancelled = True

        if self.progressive_loading_service:
            self.progressive_loading_service.cancel_loading()

    def _on_service_loading_started(self, total_count: int) -> None:
        """Handle loading started from service."""
        logger.info(
            f"🚀 [COORDINATOR] Loading started: {total_count} sequences to load"
        )
        self.loading_started.emit(total_count)

    def _on_service_chunk_loaded(self, chunk_sequences: list[SequenceData]) -> None:
        """Handle chunk loading from service with coordination."""
        if self._loading_cancelled:
            logger.info("⛔ [COORDINATOR] Loading cancelled, skipping chunk")
            return

        logger.info(
            f"📦 [COORDINATOR] Processing chunk of {len(chunk_sequences)} sequences"
        )

        # Add to our accumulated sequences
        self.all_loaded_sequences.extend(chunk_sequences)
        total_loaded = len(self.all_loaded_sequences)

        # Emit progress
        self.loading_progress.emit(total_loaded, total_loaded)

        # Call display callback if set
        if self.chunk_display_callback:
            self.chunk_display_callback(chunk_sequences, self._current_sort_method)

        # Call navigation update callback if set
        if self.navigation_update_callback:
            self.navigation_update_callback()

        # Emit chunk processed signal
        self.chunk_processed.emit(chunk_sequences)

        # Process events to keep UI responsive
        QApplication.processEvents()

    def _on_service_loading_progress(self, current: int, total: int) -> None:
        """Handle loading progress from service."""
        self.loading_progress.emit(current, total)

    def _on_service_loading_completed(
        self, final_sequences: list[SequenceData]
    ) -> None:
        """Handle loading completion from service."""
        if self._loading_cancelled:
            logger.info("⛔ [COORDINATOR] Loading was cancelled")
            return

        total_loaded = len(self.all_loaded_sequences)
        logger.info(
            f"✅ [COORDINATOR] Progressive loading completed: {total_loaded} sequences loaded"
        )

        # Emit completion signal
        self.loading_completed.emit(self.all_loaded_sequences.copy())

    def _on_service_loading_cancelled(self) -> None:
        """Handle loading cancellation from service."""
        logger.info("⛔ [COORDINATOR] Loading cancelled by service")
        self._loading_cancelled = True
        self.loading_cancelled.emit()
