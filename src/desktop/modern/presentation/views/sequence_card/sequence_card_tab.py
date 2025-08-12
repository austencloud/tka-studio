"""
Modern Sequence Card Tab Implementation

Main coordinator for the sequence card tab following the learn tab architecture pattern.
Uses clean service injection and maintains visual parity with legacy implementation.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QCoreApplication, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QSizePolicy, QVBoxLayout, QWidget

from desktop.modern.core.interfaces.sequence_card_services import (
    ISequenceCardCacheService,
    ISequenceCardDataService,
    ISequenceCardDisplayService,
    ISequenceCardExportService,
    ISequenceCardLayoutService,
    ISequenceCardSettingsService,
)
from desktop.modern.presentation.components.sequence_card import (
    SequenceCardContentComponent,
    SequenceCardHeaderComponent,
    SequenceCardNavigationComponent,
)


logger = logging.getLogger(__name__)


class SequenceCardTab(QWidget):
    """
    Modern Sequence Card Tab coordinator following clean architecture.

    Provides complete functional parity with legacy sequence card tab while
    following modern service-based architecture patterns.
    """

    # External signals for main app integration
    navigation_requested = pyqtSignal(str)
    tab_state_changed = pyqtSignal(str)

    def __init__(
        self,
        data_service: ISequenceCardDataService,
        cache_service: ISequenceCardCacheService,
        layout_service: ISequenceCardLayoutService,
        display_service: ISequenceCardDisplayService,
        display_adaptor,  # SequenceCardDisplayAdaptor
        export_service: ISequenceCardExportService,
        settings_service: ISequenceCardSettingsService,
        parent: QWidget | None = None,
    ):
        """
        Initialize modern sequence card tab.

        Args:
            data_service: Service for data operations
            cache_service: Service for caching operations
            layout_service: Service for layout calculations
            display_service: Service for display coordination
            display_adaptor: Qt adaptor for display service signals
            export_service: Service for export operations
            settings_service: Service for settings persistence
            parent: Parent widget
        """
        super().__init__(parent)

        # Inject all services
        self.data_service = data_service
        self.cache_service = cache_service
        self.layout_service = layout_service
        self.display_service = display_service
        self.display_adaptor = display_adaptor
        self.export_service = export_service
        self.settings_service = settings_service

        # State
        self.initialized = False
        self._current_scroll_position = 0

        self._setup_ui()
        self._setup_connections()

        logger.info("Modern sequence card tab initialized")

    def _setup_ui(self) -> None:
        """Setup main sequence card tab UI."""
        # Main layout with exact legacy spacing
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Create header component
        self.header = SequenceCardHeaderComponent(
            self.export_service, self.display_service, self
        )
        layout.addWidget(self.header)

        # Content layout - exact legacy structure
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(15)

        # Navigation sidebar - exact legacy width
        self.navigation = SequenceCardNavigationComponent(
            self.settings_service, self.display_service, self
        )
        self.navigation.setFixedWidth(200)
        self.navigation.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )

        # Content display area
        self.content = SequenceCardContentComponent(
            self.display_adaptor, self.cache_service, self.layout_service, self
        )

        content_layout.addWidget(self.navigation, 0)
        content_layout.addWidget(self.content, 1)

        layout.addLayout(content_layout, 1)

    def _setup_connections(self) -> None:
        """Setup signal connections between components."""
        # Navigation signals
        self.navigation.length_selected.connect(self._on_length_selected)
        self.navigation.column_count_changed.connect(self._on_column_count_changed)

        # Header signals
        self.header.refresh_requested.connect(self._on_refresh_requested)

        # Display adaptor signals
        self.display_adaptor.loading_state_changed.connect(
            self._on_loading_state_changed
        )
        self.display_adaptor.progress_updated.connect(self._on_progress_updated)

        # Content signals
        self.content.sequences_displayed.connect(self._on_sequences_displayed)

    def _on_length_selected(self, length: int) -> None:
        """Handle length selection."""
        logger.info(f"Length selected: {length}")

        # Save current scroll position
        self._current_scroll_position = self.content.get_scroll_position()

        # Update header description
        length_text = f"{length}-step" if length > 0 else "all"
        self.header.set_description_text(f"Loading {length_text} sequences...")

        # Process events immediately for responsive UI (legacy technique)
        QCoreApplication.processEvents()

        # Save setting
        self.settings_service.save_selected_length(length)

        # Update display
        column_count = self.settings_service.get_column_count()
        self.display_adaptor.display_sequences(length, column_count)

    def _on_column_count_changed(self, column_count: int) -> None:
        """Handle column count change."""
        logger.info(f"Column count changed: {column_count}")

        # Save current scroll position
        self._current_scroll_position = self.content.get_scroll_position()

        # Update header description
        self.header.set_description_text(
            f"Updating display to show {column_count} preview columns..."
        )

        # Process events immediately for responsive UI (legacy technique)
        QCoreApplication.processEvents()

        # Save setting
        self.settings_service.save_column_count(column_count)

        # Update content display
        self.content.set_column_count(column_count)

        # Refresh display with current length
        current_length = self.settings_service.get_last_selected_length()
        self.display_adaptor.display_sequences(current_length, column_count)

    def _on_refresh_requested(self) -> None:
        """Handle refresh request."""
        logger.info("Refresh requested")

        # Clear cache for fresh data
        self.cache_service.clear_cache()

        # Reload with current settings
        current_length = self.settings_service.get_last_selected_length()
        column_count = self.settings_service.get_column_count()

        self.header.set_description_text("Refreshing...")
        self.display_adaptor.display_sequences(current_length, column_count)

    def _on_loading_state_changed(self, is_loading: bool) -> None:
        """Handle loading state change."""
        if is_loading:
            self.setCursor(Qt.CursorShape.WaitCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

            # Restore scroll position after loading
            QTimer.singleShot(100, self._restore_scroll_position)

    def _on_progress_updated(self, current: int, total: int) -> None:
        """Handle progress updates."""
        # Progress updates are handled by the header component

    def _on_sequences_displayed(self, count: int) -> None:
        """Handle sequences displayed."""
        current_length = self.settings_service.get_last_selected_length()
        column_count = self.settings_service.get_column_count()

        length_text = f"{current_length}-step" if current_length > 0 else "all"

        if count > 0:
            # Calculate number of pages
            grid_dims = self.layout_service.calculate_grid_dimensions(current_length)
            sequences_per_page = grid_dims.total_positions
            page_count = (count + sequences_per_page - 1) // sequences_per_page

            self.header.set_description_text(
                f"Showing {count} {length_text} sequences across {page_count} pages with {column_count} preview columns"
            )
        else:
            self.header.set_description_text(f"No {length_text} sequences found")

    def _restore_scroll_position(self) -> None:
        """Restore the previous scroll position."""
        if self._current_scroll_position > 0:
            self.content.set_scroll_position(self._current_scroll_position)

    def showEvent(self, event) -> None:
        """Handle tab show event - provide immediate UI response."""
        super().showEvent(event)

        if not self.initialized:
            self.initialized = True

            # IMMEDIATE UI RESPONSE: Show tab structure instantly without blocking
            saved_length = self.settings_service.get_last_selected_length()
            saved_columns = self.settings_service.get_column_count()

            # Set up navigation with saved settings immediately
            self.navigation.select_length(saved_length)
            self.navigation.column_combo.setCurrentText(str(saved_columns))
            self.content.set_column_count(saved_columns)

            # Show immediate feedback in header
            length_text = f"{saved_length}-step" if saved_length > 0 else "all"
            self.header.set_description_text(f"Preparing {length_text} sequences...")

            # Process events to ensure immediate UI display
            from PyQt6.QtCore import QCoreApplication

            QCoreApplication.processEvents()

            # Start progressive loading after UI is shown (very short delay)
            QTimer.singleShot(
                10,
                lambda: self._initialize_content_progressive(
                    saved_length, saved_columns
                ),
            )

            # Emit state change
            self.tab_state_changed.emit("sequence_card_initialized")

    def _initialize_content_progressive(self, length: int, column_count: int) -> None:
        """Initialize tab content with progressive loading for immediate UI response."""
        try:
            logger.info(
                f"Starting progressive initialization with length {length}, columns {column_count}"
            )

            # Show loading cursor only after UI is displayed
            self.setCursor(Qt.CursorShape.WaitCursor)

            # Update header to show loading state
            length_text = f"{length}-step" if length > 0 else "all"
            self.header.set_description_text(f"Loading {length_text} sequences...")

            # Process events to ensure header update is visible
            from PyQt6.QtCore import QCoreApplication

            QCoreApplication.processEvents()

            # Start the actual loading process
            self.display_adaptor.display_sequences(length, column_count)

        except Exception as e:
            logger.exception(f"Error initializing content progressively: {e}")
            self.header.set_description_text(f"Error loading sequences: {e}")
        finally:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def resizeEvent(self, event) -> None:
        """Handle resize event."""
        super().resizeEvent(event)

        if self.initialized:
            # Refresh layout after resize with debouncing
            QTimer.singleShot(300, self._refresh_layout_after_resize)

    def _refresh_layout_after_resize(self) -> None:
        """Refresh layout after resize with current settings."""
        if not self.initialized:
            return

        logger.debug("Refreshing layout after resize")

        # Save current scroll position
        self._current_scroll_position = self.content.get_scroll_position()

        # Refresh display with current settings
        current_length = self.settings_service.get_last_selected_length()
        column_count = self.settings_service.get_column_count()
        self.content.set_column_count(column_count)
        self.display_adaptor.display_sequences(current_length, column_count)

    def cleanup(self) -> None:
        """Cleanup resources."""
        try:
            if hasattr(self.display_service, "cancel_current_operation"):
                self.display_service.cancel_current_operation()

            if hasattr(self.export_service, "cancel_export"):
                self.export_service.cancel_export()

            self.cache_service.optimize_memory_usage()

            logger.info("Sequence card tab cleanup completed")
        except Exception as e:
            logger.exception(f"Error during cleanup: {e}")

    def closeEvent(self, event) -> None:
        """Handle close event."""
        self.cleanup()
        super().closeEvent(event)
