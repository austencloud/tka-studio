"""
Progressive Loading Event Handler Service

Handles all progressive loading events and callbacks, removing this responsibility
from the SequenceBrowserPanel to keep it lightweight.
"""

from __future__ import annotations

from collections.abc import Callable
import logging

from PyQt6.QtWidgets import QApplication

from desktop.modern.application.services.browse.loading_state_manager_service import (
    LoadingStateManagerService,
)
from desktop.modern.application.services.browse.sequence_display_coordinator_service import (
    SequenceDisplayCoordinatorService,
)
from desktop.modern.application.services.browse.sequence_sorter_service import (
    SequenceSorterService,
)
from desktop.modern.domain.models.sequence_data import SequenceData


logger = logging.getLogger(__name__)


class ProgressiveLoadingEventHandler:
    """Service to handle all progressive loading events and callbacks."""

    def __init__(
        self,
        loading_state_manager: LoadingStateManagerService,
        sequence_display_coordinator: SequenceDisplayCoordinatorService,
        sequence_sorter: SequenceSorterService,
        control_panel=None,
        navigation_sidebar=None,
    ):
        """Initialize with required services."""
        self.loading_state_manager = loading_state_manager
        self.sequence_display_coordinator = sequence_display_coordinator
        self.sequence_sorter = sequence_sorter
        self.control_panel = control_panel
        self.navigation_sidebar = navigation_sidebar

        # State tracking
        self._loading_cancelled = False
        self.all_loaded_sequences: list[SequenceData] = []
        self.current_sequences: list[SequenceData] = []

        # Callbacks
        self.get_current_sort_method: Callable[[], str] | None = None
        self.update_navigation_callback: Callable[[], None] | None = None

    def set_get_sort_method_callback(self, callback: Callable[[], str]) -> None:
        """Set callback to get current sort method."""
        self.get_current_sort_method = callback

    def set_update_navigation_callback(self, callback: Callable[[], None]) -> None:
        """Set callback to update navigation."""
        self.update_navigation_callback = callback

    def on_loading_started(self, total_count: int) -> None:
        """Handle loading started signal."""
        self._loading_cancelled = False
        self.all_loaded_sequences.clear()

        # Keep browsing area visible for progressive loading
        self.loading_state_manager.hide_loading_state()
        logger.info(f"🚀 Started progressive loading: {total_count} sequences to load")

    def on_sequences_chunk_loaded(self, chunk_sequences: list[SequenceData]) -> None:
        """Handle chunk loading with progressive layout addition."""
        logger.info(f"📦 Processing chunk of {len(chunk_sequences)} sequences")

        if self._loading_cancelled:
            logger.info("⛔ Loading cancelled, skipping chunk")
            return

        self.all_loaded_sequences.extend(chunk_sequences)
        total_loaded = len(self.all_loaded_sequences)

        # Update progress
        self.loading_state_manager.update_progress(
            total_loaded, total_loaded, f"Loaded {total_loaded} sequences..."
        )

        if self.control_panel:
            self.control_panel.update_count(total_loaded)

        # Add sequences progressively using service coordinator
        if self.get_current_sort_method:
            sort_method = self.get_current_sort_method()
            self.sequence_display_coordinator.add_sequences_progressively(
                chunk_sequences, sort_method
            )

        # Update navigation as we add sections
        if self.update_navigation_callback:
            self.update_navigation_callback()

        # Process events to keep UI responsive
        QApplication.processEvents()

    def on_loading_progress(self, current: int, total: int) -> None:
        """Handle loading progress update."""
        self.loading_state_manager.update_progress(current, total)

    def on_loading_completed(self, final_sequences: list[SequenceData]) -> None:
        """Handle loading completion."""
        if self._loading_cancelled:
            return

        self.current_sequences = final_sequences
        self.all_loaded_sequences = final_sequences.copy()

        if self.control_panel:
            self.control_panel.update_count(len(final_sequences))

        # No finalization needed - layout was built progressively

        # Update navigation with final state
        if self.update_navigation_callback:
            self.update_navigation_callback()

        logger.info(
            f"✅ Progressive loading completed: {len(final_sequences)} sequences loaded"
        )

    def on_loading_cancelled(self) -> None:
        """Handle loading cancellation."""
        self._loading_cancelled = True

        if self.all_loaded_sequences:
            self.current_sequences = self.all_loaded_sequences
            if self.control_panel:
                self.control_panel.update_count(len(self.all_loaded_sequences))
            logger.info(
                f"⚠️ Loading cancelled: Keeping {len(self.all_loaded_sequences)} loaded sequences"
            )
        else:
            if self.control_panel:
                self.control_panel.update_count(0)
            logger.info("❌ Loading cancelled: No sequences loaded")

    def cancel_loading(self) -> None:
        """Cancel the current loading operation."""
        self._loading_cancelled = True

    def get_current_sequences(self) -> list[SequenceData]:
        """Get the current sequences."""
        return self.current_sequences

    def get_all_loaded_sequences(self) -> list[SequenceData]:
        """Get all loaded sequences."""
        return self.all_loaded_sequences

    def clear_sequences(self) -> None:
        """Clear all sequence data."""
        self.current_sequences.clear()
        self.all_loaded_sequences.clear()
        self._loading_cancelled = False
