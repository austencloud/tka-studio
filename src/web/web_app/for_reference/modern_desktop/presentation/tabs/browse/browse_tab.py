"""
Modern Browse Tab - Refactored with Manager Classes

Refactored to use focused manager classes for better separation of responsibilities:
- BrowseTabController: Main coordinator for all browse tab operations
- BrowseDataManager: Handles data conversion and sequence operations
- BrowseActionHandler: Processes user actions (edit, save, delete, fullscreen)
- BrowseNavigationManager: Manages navigation between panels

This provides better maintainability and testability while preserving the same
public interface and functionality.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QStackedWidget, QWidget

from desktop.modern.application.services.browse.browse_state_service import (
    BrowseStateService,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.presentation.components.browse.components.filter_selection_panel import (
    FilterSelectionPanel,
)
from desktop.modern.presentation.components.browse.sequence_browser_panel import (
    SequenceBrowserPanel,
)
from desktop.modern.presentation.views.browse.managers import (
    BrowseTabController,
)
from desktop.modern.presentation.views.browse.models import FilterType


logger = logging.getLogger(__name__)


class BrowseTab(QWidget):
    """
    Modern Browse Tab refactored with manager classes.

    Layout:
    - Main horizontal layout (2:1 ratio)
    - Left: internal_left_stack (QStackedWidget)
      - Index 0: Filter selection panel
      - Index 1: Sequence browser panel
    - Right: Sequence viewer panel

    Features:
    - Coordinated through BrowseTabController
    - Focused manager classes for different responsibilities
    - Maintains same public interface as before
    - Better separation of concerns and testability
    """

    # Signals for communication with main app
    sequence_selected = pyqtSignal(str)  # sequence_id
    open_in_construct = pyqtSignal(str)  # sequence_id

    def __init__(
        self,
        sequences_dir: Path,
        settings_file: Path,
        container: DIContainer,
        parent: QWidget | None = None,
    ):
        """
        Initialize the modern browse tab with manager-based architecture.

        Args:
            sequences_dir: Directory containing sequence files
            settings_file: Settings file path
            container: Dependency injection container with registered services
            parent: Parent widget
        """
        super().__init__(parent)

        # Store paths and container
        self.sequences_dir = sequences_dir
        self.settings_file = settings_file
        self.container = container

        # Find the TKA root directory and construct the data path
        tka_root = Path(__file__).resolve()
        while tka_root.parent != tka_root and tka_root.name != "TKA":
            tka_root = tka_root.parent
        self.data_dir = tka_root / "data"

        # Initialize state service for backward compatibility
        self.state_service = BrowseStateService(settings_file)

        # Setup basic layout structure first
        self._setup_basic_layout()

        # Initialize services needed by components
        self._initialize_component_services()

        # Create panels that depend on services
        self._create_panels()

        # Initialize the controller with all components
        # NOTE: Fixed initialization order - viewer_panel is now created in _create_panels()
        self.controller = BrowseTabController(
            container=container,
            data_dir=self.data_dir,
            sequences_dir=sequences_dir,
            stacked_widget=self.internal_left_stack,
            parent_widget=self,
            viewer_panel=self.sequence_viewer_panel,
        )

        # Connect signals
        self._connect_signals()

        # Initialize the controller
        QTimer.singleShot(100, self._initialize_controller)

    def _initialize_component_services(self) -> None:
        """Initialize services needed by UI components using dependency injection."""
        # Register browse services with the container
        from desktop.modern.core.dependency_injection.browse_service_registration import (
            register_browse_services,
        )

        register_browse_services(
            container=self.container,
            sequences_dir=self.sequences_dir,
            data_dir=self.data_dir,
            stacked_widget=self.internal_left_stack,
            viewer_panel=None,  # Will be created later
            parent_widget=self,
        )

        # Resolve services from container
        from desktop.modern.core.interfaces.browse_services import (
            IBrowseService,
            IDictionaryDataManager,
            IProgressiveLoadingService,
        )

        self.browse_service = self.container.resolve(IBrowseService)
        self.dictionary_manager = self.container.resolve(IDictionaryDataManager)
        self.progressive_loading_service = self.container.resolve(
            IProgressiveLoadingService
        )

    def _setup_basic_layout(self) -> None:
        """Setup basic layout structure without service-dependent components."""
        # Main horizontal layout (2:1 ratio like Legacy)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left side - Internal stack for filter selection and sequence browsing
        self.internal_left_stack = QStackedWidget()

        # Right side - Sequence viewer panel (will be created after services)
        # Add to main layout with 2:1 ratio
        main_layout.addWidget(self.internal_left_stack, 2)

        # Placeholder for viewer panel (will be added after service initialization)
        self.main_layout = main_layout

    def _create_panels(self) -> None:
        """Create panels that depend on services."""
        # Create panels with required services
        self.filter_selection_panel = FilterSelectionPanel(
            self.browse_service, self.dictionary_manager
        )
        self.sequence_browser_panel = SequenceBrowserPanel(
            self.browse_service,
            self.state_service,
            self.progressive_loading_service,
            self.container,
        )

        # Add panels to stack (matching Legacy indexes)
        self.internal_left_stack.addWidget(
            self.filter_selection_panel
        )  # 0 - Filter selection
        self.internal_left_stack.addWidget(
            self.sequence_browser_panel
        )  # 1 - Sequence list

        # Start with filter selection visible (matching Legacy)
        self.internal_left_stack.setCurrentIndex(0)

        # Create sequence viewer panel with state service
        from desktop.modern.presentation.components.browse.modern_sequence_viewer_panel import (
            ModernSequenceViewerPanel,
        )

        self.sequence_viewer_panel = ModernSequenceViewerPanel(self.state_service)

        # Add viewer panel to main layout
        self.main_layout.addWidget(self.sequence_viewer_panel, 1)

        # Update navigation manager with viewer panel reference
        # (Since services were registered before viewer panel was created)
        from desktop.modern.core.interfaces.browse_services import (
            IBrowseNavigationManager,
        )

        try:
            navigation_manager = self.container.resolve(IBrowseNavigationManager)
            navigation_manager.set_viewer_panel(self.sequence_viewer_panel)
            logger.info(
                f"🔗 Updated navigation manager with viewer panel: {self.sequence_viewer_panel}"
            )

            # Validate the setup worked
            if (
                hasattr(navigation_manager, "viewer_panel")
                and navigation_manager.viewer_panel is not None
            ):
                logger.info("✅ Viewer panel successfully set in navigation manager")
            else:
                logger.error("❌ Failed to set viewer panel in navigation manager")

        except Exception as e:
            logger.exception(
                f"❌ Failed to update navigation manager with viewer panel: {e}"
            )
            import traceback

            traceback.print_exc()

    def _initialize_controller(self) -> None:
        """Initialize the controller and start the browse tab."""
        # Connect controller signals
        self._connect_controller_signals()

        # Initialize the controller
        self.controller.initialize()

    def _connect_signals(self) -> None:
        """Connect component signals to controller methods."""
        # Filter selection signals
        self.filter_selection_panel.filter_selected.connect(self._on_filter_selected)

        # Browser panel signals
        self.sequence_browser_panel.sequence_selected.connect(
            self._on_sequence_selected
        )
        self.sequence_browser_panel.open_in_construct.connect(
            self.open_in_construct.emit
        )
        self.sequence_browser_panel.back_to_filters.connect(self._show_filter_selection)

        # Sequence viewer panel signals
        self.sequence_viewer_panel.sequence_action.connect(self._on_sequence_action)
        self.sequence_viewer_panel.back_to_browser.connect(self._show_sequence_browser)

        # Controller signals (will be connected after controller is created)

    def _on_filter_selected(self, filter_type: FilterType, filter_value) -> None:
        """Handle filter selection with stable layout approach."""
        # Save filter state for backward compatibility
        self.state_service.set_filter(filter_type, filter_value)

        # IMMEDIATE: Switch to sequence browser with stable skeleton layout
        self._show_sequence_browser_with_stable_layout(filter_type, filter_value)

        # THEN: Start progressive loading (after UI is stable)
        QTimer.singleShot(
            50, lambda: self.controller.apply_filter(filter_type, filter_value)
        )

    def _on_sequence_selected(self, sequence_id: str) -> None:
        """Handle sequence selection - delegate to controller."""
        try:
            logger.info(f"🎯 Sequence selected: {sequence_id}")

            # Delegate to controller
            self.controller.select_sequence(sequence_id)

            # Update UI components with selected sequence
            sequence_data = self.controller.get_current_sequence()
            if sequence_data:
                # Directly update viewer panel as backup (in case navigation manager fails)
                if hasattr(self.sequence_viewer_panel, "show_sequence"):
                    self.sequence_viewer_panel.show_sequence(sequence_data)
                    logger.info(
                        f"✅ Viewer panel updated directly with sequence: {sequence_data.word}"
                    )
                else:
                    logger.error("❌ Viewer panel missing show_sequence method")
            else:
                logger.error(f"❌ No sequence data available for {sequence_id}")

            # Emit signal for external listeners
            self.sequence_selected.emit(sequence_id)

        except Exception as e:
            logger.exception(
                f"❌ Failed to handle sequence selection for {sequence_id}: {e}"
            )
            import traceback

            traceback.print_exc()

    def _on_sequence_action(self, action_type: str, sequence_id: str) -> None:
        """Handle sequence action from viewer panel - delegate to controller."""
        if action_type == "edit":
            self.controller.edit_current_sequence()
        elif action_type == "save":
            # Get current variation index from viewer panel
            current_variation_index = getattr(
                self.sequence_viewer_panel, "current_variation_index", 0
            )
            self.controller.save_current_image(current_variation_index)
        elif action_type == "delete":
            # Get current variation index from viewer panel
            current_variation_index = getattr(
                self.sequence_viewer_panel, "current_variation_index", 0
            )
            success = self.controller.delete_current_variation(current_variation_index)
            if success:
                # Refresh the viewer panel
                sequence_data = self.controller.get_current_sequence()
                if sequence_data:
                    self.sequence_viewer_panel.show_sequence(sequence_data)
        elif action_type == "fullscreen":
            # Get current variation index from viewer panel
            current_variation_index = getattr(
                self.sequence_viewer_panel, "current_variation_index", 0
            )
            self.controller.view_fullscreen(current_variation_index)
        else:
            logger.warning(f"Unknown action type: {action_type}")

    def _show_filter_selection(self) -> None:
        """Show filter selection panel."""
        self.internal_left_stack.setCurrentIndex(0)

    def _show_sequence_browser(self) -> None:
        """Show sequence browser panel."""
        self.internal_left_stack.setCurrentIndex(1)

    def _show_sequence_browser_with_stable_layout(
        self, filter_type: FilterType, filter_value
    ) -> None:
        """Show sequence browser with immediate skeleton layout for stable UX."""
        # Switch to sequence browser panel immediately (no delay)
        self.internal_left_stack.setCurrentIndex(1)

        # Tell the browser panel to prepare stable layout with skeleton
        self.sequence_browser_panel.prepare_stable_layout_for_filter(
            filter_type, filter_value
        )

        logger.info(
            f"🎯 Immediately switched to stable sequence browser for {filter_type.value}: {filter_value}"
        )

    # Connect controller signals after initialization
