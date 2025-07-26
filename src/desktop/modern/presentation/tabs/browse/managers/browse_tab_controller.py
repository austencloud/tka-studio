"""
Browse Tab Controller - Main coordinator for Browse Tab functionality

This class is responsible for:
- Coordinating between all browse tab managers and components
- Managing the overall browse tab workflow
- Handling high-level state management
- Connecting signals between components
- Providing the main interface for browse tab operations
"""

import logging
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QStackedWidget, QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.tabs.browse.managers.browse_action_handler import (
    BrowseActionHandler,
)
from desktop.modern.presentation.tabs.browse.managers.browse_data_manager import (
    BrowseDataManager,
)
from desktop.modern.presentation.tabs.browse.managers.browse_navigation_manager import (
    BrowseNavigationManager,
    BrowsePanel,
)
from desktop.modern.presentation.tabs.browse.models import FilterType

logger = logging.getLogger(__name__)


class BrowseTabController(QObject):
    """
    Main controller for the Browse tab.
    
    Coordinates between all managers and components to provide
    a unified interface for browse tab operations.
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
    ):
        """
        Initialize the browse tab controller.
        
        Args:
            container: Dependency injection container
            data_dir: Directory containing dictionary data
            sequences_dir: Directory containing sequence files
            stacked_widget: The stacked widget for panel navigation
            parent_widget: Parent widget for dialogs
        """
        super().__init__()
        
        self.container = container
        self.data_dir = data_dir
        self.sequences_dir = sequences_dir
        self.parent_widget = parent_widget
        
        # Initialize managers
        self.data_manager = BrowseDataManager(data_dir)
        self.action_handler = BrowseActionHandler(container, sequences_dir, parent_widget)
        self.navigation_manager = BrowseNavigationManager(stacked_widget)
        
        # Current state
        self.current_filter_type: Optional[FilterType] = None
        self.current_filter_value = None
        self.current_sequences: list[SequenceData] = []
        self.current_sequence: Optional[SequenceData] = None
        
        # Connect signals
        self._connect_signals()

    def initialize(self) -> None:
        """Initialize the controller and load initial data."""
        try:
            logger.info("🚀 Initializing Browse Tab Controller...")
            
            # Start data loading
            self.data_loading_started.emit()
            self.data_manager.load_all_sequences()
            
            # Navigate to initial panel
            self.navigation_manager.navigate_to_filter_selection()
            
            logger.info("✅ Browse Tab Controller initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Browse Tab Controller: {e}")
            self.error_occurred.emit(f"Failed to initialize: {str(e)}")

    def apply_filter(self, filter_type: FilterType, filter_value) -> None:
        """
        Apply a filter and navigate to browser panel.
        
        Args:
            filter_type: Type of filter to apply
            filter_value: Value to filter by
        """
        try:
            logger.info(f"🔍 Applying filter: {filter_type.value} = {filter_value}")
            
            # Store current filter
            self.current_filter_type = filter_type
            self.current_filter_value = filter_value
            
            # Apply filter using data manager
            self.current_sequences = self.data_manager.apply_filter(filter_type, filter_value)
            
            logger.info(f"📊 Filter applied: {len(self.current_sequences)} sequences found")
            
            # Navigate to browser with filtered data
            self.navigation_manager.navigate_to_browser(self.current_sequences)
            
        except Exception as e:
            logger.error(f"❌ Failed to apply filter: {e}")
            self.error_occurred.emit(f"Failed to apply filter: {str(e)}")

    def select_sequence(self, sequence_id: str) -> None:
        """
        Select a sequence and navigate to viewer panel.
        
        Args:
            sequence_id: ID of the sequence to select
        """
        try:
            logger.info(f"🎯 Selecting sequence: {sequence_id}")
            
            # Get sequence data
            sequence_data = self.data_manager.get_sequence_data(sequence_id)
            if not sequence_data:
                logger.error(f"❌ Sequence not found: {sequence_id}")
                self.error_occurred.emit(f"Sequence not found: {sequence_id}")
                return
            
            # Store current sequence
            self.current_sequence = sequence_data
            
            # Navigate to viewer with sequence data
            self.navigation_manager.navigate_to_viewer(sequence_data)
            
            logger.info(f"✅ Sequence selected: {sequence_data.word}")
            
        except Exception as e:
            logger.error(f"❌ Failed to select sequence: {e}")
            self.error_occurred.emit(f"Failed to select sequence: {str(e)}")

    def edit_current_sequence(self) -> None:
        """Edit the currently selected sequence."""
        if self.current_sequence:
            sequence_id = self.action_handler.handle_edit_sequence(self.current_sequence.id)
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
        if self.current_sequence:
            return self.action_handler.handle_save_image(
                self.current_sequence, variation_index
            )
        else:
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
        if self.current_sequence:
            success = self.action_handler.handle_delete_variation(
                self.current_sequence, variation_index
            )
            if success:
                # Refresh data after deletion
                self.refresh_data()
            return success
        else:
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
        if self.current_sequence and self.current_sequence.thumbnails:
            return self.action_handler.handle_fullscreen_view(
                self.current_sequence.thumbnails, variation_index
            )
        else:
            logger.warning("⚠️ No sequence or thumbnails available for fullscreen")
            return False

    def go_back(self) -> bool:
        """
        Navigate back to the previous panel.
        
        Returns:
            True if navigation was successful, False otherwise
        """
        return self.navigation_manager.go_back()

    def refresh_data(self) -> None:
        """Refresh all data from disk."""
        try:
            logger.info("🔄 Refreshing browse data...")
            self.data_manager.refresh_data()
            
            # Re-apply current filter if any
            if self.current_filter_type and self.current_filter_value:
                self.apply_filter(self.current_filter_type, self.current_filter_value)
            
            logger.info("✅ Data refreshed successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to refresh data: {e}")
            self.error_occurred.emit(f"Failed to refresh data: {str(e)}")

    def get_current_panel(self) -> BrowsePanel:
        """Get the current active panel."""
        return self.navigation_manager.get_current_panel()

    def get_current_sequences(self) -> list[SequenceData]:
        """Get the current filtered sequences."""
        return self.current_sequences

    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get the currently selected sequence."""
        return self.current_sequence

    def get_loading_errors(self) -> list[str]:
        """Get any loading errors."""
        return self.data_manager.get_loading_errors()

    def _connect_signals(self) -> None:
        """Connect signals between managers and components."""
        # Data manager signals
        self.data_manager.dictionary_manager.data_loaded.connect(
            self._on_data_loaded
        )
        
        # Navigation manager signals
        self.navigation_manager.panel_changed.connect(
            self._on_panel_changed
        )

    def _on_data_loaded(self, count: int) -> None:
        """Handle data loading completion."""
        logger.info(f"📊 Data loaded: {count} sequences")
        self.data_loading_finished.emit(count)

    def _on_panel_changed(self, panel_name: str) -> None:
        """Handle panel change events."""
        logger.debug(f"📍 Panel changed to: {panel_name}")
