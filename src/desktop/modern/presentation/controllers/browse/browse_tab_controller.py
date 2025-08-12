"""
Browse Tab Controller - Simplified Coordinator

This class is responsible for:
- Coordinating between managers and components
- High-level workflow orchestration
- Delegating view state to BrowseViewModel
- Connecting signals between components

Simplified: View state management moved to BrowseViewModel,
direct UI manipulation minimized.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QStackedWidget, QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.managers.browse.browse_navigation_manager import (
    BrowsePanel,
)
from desktop.modern.presentation.views.browse.browse_view_model import BrowseViewModel
from desktop.modern.presentation.views.browse.errors import FilterError, NavigationError
from desktop.modern.presentation.views.browse.models import FilterType


logger = logging.getLogger(__name__)


class BrowseTabController(QObject):
    """
    Simplified controller for the Browse tab.

    Focuses on coordination and delegates view state management to BrowseViewModel.
    """

    # Signals
    sequence_selected_for_editing = pyqtSignal(str)  # sequence_id
    data_loading_started = pyqtSignal()
    data_loading_finished = pyqtSignal(int)  # count
    error_occurred = pyqtSignal(str)  # error_message

    def __init__(
        self,
        container: DIContainer,
        data_dir: Path,
        sequences_dir: Path,
        stacked_widget: QStackedWidget,
        parent_widget: QWidget,
        viewer_panel=None,
    ):
        """
        Initialize the browse tab controller.

        Args:
            container: Dependency injection container
            data_dir: Directory containing dictionary data
            sequences_dir: Directory containing sequence files
            stacked_widget: The stacked widget for panel navigation
            parent_widget: Parent widget for dialogs
            viewer_panel: Optional viewer panel widget (separate from stacked widget)
        """
        super().__init__()

        self.container = container
        self.data_dir = data_dir
        self.sequences_dir = sequences_dir
        self.stacked_widget = stacked_widget
        self.parent_widget = parent_widget

        # Initialize view model for state management
        self.view_model = BrowseViewModel()

        # Resolve managers from DI container
        from desktop.modern.core.interfaces.browse_services import (
            IBrowseActionHandler,
            IBrowseDataManager,
            IBrowseNavigationManager,
        )

        self.data_manager = container.resolve(IBrowseDataManager)
        self.action_handler = container.resolve(IBrowseActionHandler)
        self.navigation_manager = container.resolve(IBrowseNavigationManager)

        # Connect signals
        self._connect_signals()

    def initialize(self) -> None:
        """Initialize the controller and load initial data."""
        try:
            # Start data loading
            self.view_model.set_loading(True)
            self.data_loading_started.emit()
            self.data_manager.load_all_sequences()

        except Exception as e:
            error_msg = f"Failed to initialize: {e!s}"
            logger.exception(f"❌ {error_msg}")
            self.view_model.set_error(error_msg)
            self.error_occurred.emit(error_msg)

    def apply_filter(self, filter_type: FilterType, filter_value) -> None:
        """
        Apply a filter and coordinate the update process.

        Args:
            filter_type: Type of filter to apply
            filter_value: Value to filter by
        """
        try:
            logger.info(f"🔍 Applying filter: {filter_type.value} = {filter_value}")

            # Update view model with filter
            self.view_model.set_filter(filter_type, filter_value)
            self.view_model.set_loading(True)

            # Navigate to browser panel
            self._navigate_to_browser()

            # Start progressive loading
            self._start_progressive_loading(filter_type, filter_value)

        except Exception as e:
            error_msg = f"Failed to apply filter {filter_type.value}: {e!s}"
            logger.exception(f"❌ {error_msg}")
            self.view_model.set_error(error_msg)
            self.error_occurred.emit(error_msg)

    def select_sequence(self, sequence_id: str) -> None:
        """
        Select a sequence and update view model.

        Args:
            sequence_id: ID of the sequence to select
        """
        try:
            logger.info(f"🎯 Selecting sequence: {sequence_id}")

            # Get sequence data
            sequence_data = self.data_manager.get_sequence_data(sequence_id)
            if not sequence_data:
                raise FilterError(f"Sequence not found: {sequence_id}")

            # Update view model
            self.view_model.set_selected_sequence(sequence_id)

            # Navigate to viewer with sequence data
            self.navigation_manager.navigate_to_viewer(sequence_data)

            logger.info(f"✅ Sequence selected: {sequence_data.word}")

        except Exception as e:
            error_msg = f"Failed to select sequence: {e!s}"
            logger.exception(f"❌ {error_msg}")
            self.view_model.set_error(error_msg)
            self.error_occurred.emit(error_msg)

    def edit_current_sequence(self) -> None:
        """Edit the currently selected sequence."""
        selected_id = self.view_model.selected_sequence_id
        if selected_id:
            sequence_id = self.action_handler.handle_edit_sequence(selected_id)
            self.sequence_selected_for_editing.emit(sequence_id)
        else:
            logger.warning("⚠️ No sequence selected for editing")

    def save_current_image(self, variation_index: int = 0) -> bool:
        """
        Save the current sequence image.

        Args:
            variation_index: Index of the variation to save

        Returns:
            True if save was successful, False otherwise
        """
        selected_id = self.view_model.selected_sequence_id
        if selected_id:
            sequence_data = self.view_model.get_sequence_by_id(selected_id)
            if sequence_data:
                return self.action_handler.handle_save_image(
                    sequence_data, variation_index
                )

        logger.warning("⚠️ No sequence selected for saving")
        return False

    def delete_current_variation(self, variation_index: int = 0) -> bool:
        """
        Delete a variation of the current sequence.

        Args:
            variation_index: Index of the variation to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        selected_id = self.view_model.selected_sequence_id
        if selected_id:
            sequence_data = self.view_model.get_sequence_by_id(selected_id)
            if sequence_data:
                success = self.action_handler.handle_delete_variation(
                    sequence_data, variation_index
                )
                if success:
                    # Refresh data after deletion
                    self.refresh_data()
                return success

        logger.warning("⚠️ No sequence selected for deletion")
        return False

    def view_fullscreen(self, variation_index: int = 0) -> bool:
        """
        View the current sequence in fullscreen.

        Args:
            variation_index: Index of the variation to view

        Returns:
            True if fullscreen was opened successfully, False otherwise
        """
        selected_id = self.view_model.selected_sequence_id
        if selected_id:
            sequence_data = self.view_model.get_sequence_by_id(selected_id)
            if sequence_data and sequence_data.thumbnails:
                return self.action_handler.handle_fullscreen_view(
                    sequence_data.thumbnails, variation_index
                )

        logger.warning("⚠️ No sequence or thumbnails available for fullscreen")
        return False

    def go_back(self) -> bool:
        """
        Navigate back to the previous panel.

        Returns:
            True if navigation was successful, False otherwise
        """
        try:
            return self.navigation_manager.go_back()
        except Exception as e:
            raise NavigationError(f"Failed to navigate back: {e}") from e

    def refresh_data(self) -> None:
        """Refresh all data from disk."""
        try:
            logger.info("🔄 Refreshing browse data...")
            self.data_manager.refresh_data()

            # Re-apply current filter if any
            if self.view_model.current_filter_type:
                self.apply_filter(
                    self.view_model.current_filter_type,
                    self.view_model.current_filter_value,
                )

            logger.info("✅ Data refreshed successfully")

        except Exception as e:
            error_msg = f"Failed to refresh data: {e!s}"
            logger.exception(f"❌ {error_msg}")
            self.view_model.set_error(error_msg)
            self.error_occurred.emit(error_msg)

    def get_current_panel(self) -> BrowsePanel:
        """Get the current active panel."""
        return self.navigation_manager.get_current_panel()

    def get_current_sequences(self) -> list[SequenceData]:
        """Get the current filtered sequences from view model."""
        return self.view_model.current_sequences

    def get_current_sequence(self) -> SequenceData | None:
        """Get the currently selected sequence from view model."""
        selected_id = self.view_model.selected_sequence_id
        if selected_id:
            return self.view_model.get_sequence_by_id(selected_id)
        return None

    def get_loading_errors(self) -> list[str]:
        """Get any loading errors."""
        return self.data_manager.get_loading_errors()

    def _connect_signals(self) -> None:
        """Connect signals between managers and components."""
        # Data manager signals
        self.data_manager.dictionary_manager.data_loaded.connect(self._on_data_loaded)

        # Navigation manager signals
        self.navigation_manager.panel_changed.connect(self._on_panel_changed)

        # View model signals can be connected by UI components directly

    def _on_data_loaded(self, count: int) -> None:
        """Handle data loading completion."""

        self.view_model.set_loading(False)
        self.data_loading_finished.emit(count)

    def _navigate_to_browser(self) -> None:
        """Navigate to browser panel."""
        try:
            if self.navigation_manager:
                logger.info("🔄 Navigating to browser panel...")
                self.navigation_manager.navigate_to_browser([])
                logger.info("✅ Navigation completed")
            else:
                raise NavigationError("Navigation manager is None")
        except Exception as e:
            raise NavigationError(f"Failed to navigate to browser: {e}") from e

    def _start_progressive_loading(self, filter_type: FilterType, filter_value) -> None:
        """Start progressive loading of sequences."""
        try:
            browser_panel = self.stacked_widget.widget(1)  # Browser panel is at index 1

            if browser_panel and hasattr(browser_panel, "show_sequences_progressive"):
                logger.info("🔄 Starting progressive loading in browser panel")
                browser_panel.show_sequences_progressive(
                    filter_type, filter_value, chunk_size=6
                )
            else:
                # Fallback to blocking loading if progressive not available
                logger.warning(
                    "⚠️ Progressive loading not available, falling back to blocking"
                )
                sequences = self.data_manager.apply_filter(filter_type, filter_value)
                self.view_model.set_sequences(sequences)
                self._update_browser_panel_with_sequences(sequences)

        except Exception as e:
            error_msg = f"Failed to start progressive loading: {e!s}"
            logger.exception(f"❌ {error_msg}")
            self.view_model.set_error(error_msg)

    def _update_browser_panel_with_sequences(self, sequences) -> None:
        """Update the browser panel with sequences."""
        try:
            # Get the browser panel from the stacked widget
            browser_panel = self.stacked_widget.widget(1)  # Browser panel is at index 1

            if browser_panel and hasattr(browser_panel, "show_sequences"):
                logger.info(
                    f"🔄 Updating browser panel with {len(sequences)} sequences"
                )
                browser_panel.show_sequences(
                    sequences,
                    self.view_model.current_filter_type,
                    self.view_model.current_filter_value,
                )
            else:
                logger.warning(
                    "⚠️ Browser panel not found or doesn't have show_sequences method"
                )

        except Exception as e:
            logger.exception(f"❌ Failed to update browser panel: {e}")

    def _on_panel_changed(self, panel_name: str) -> None:
        """Handle panel change events."""
        logger.debug(f"📍 Panel changed to: {panel_name}")
