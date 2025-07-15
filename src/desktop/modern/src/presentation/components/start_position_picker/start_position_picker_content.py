"""
Start Position Picker Content Component

Handles the main content area with position options and grid layout.
Extracted from the main StartPositionPicker for better maintainability.
"""

import logging
from enum import Enum
from typing import List

from application.services.pictograph_pool_manager import PictographPoolManager
from core.interfaces.start_position_services import (
    IStartPositionDataService,
    IStartPositionUIService,
)
from presentation.components.start_position_picker.start_position_option import (
    StartPositionOption,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication, QGridLayout, QScrollArea, QVBoxLayout, QWidget

logger = logging.getLogger(__name__)


class PickerMode(Enum):
    """Picker display modes."""

    BASIC = "basic"
    ADVANCED = "advanced"
    AUTO = "auto"


class StartPositionPickerContent(QWidget):
    """
    Content component for start position picker.

    Responsibilities:
    - Position option creation and management
    - Grid layout arrangement (basic vs advanced)
    - Position loading and sizing
    - Scroll area management
    """

    position_selected = pyqtSignal(str)

    def __init__(
        self,
        pool_manager: PictographPoolManager,
        data_service: IStartPositionDataService,
        ui_service: IStartPositionUIService,
        parent=None,
    ):
        super().__init__(parent)

        # Dependencies
        self.pool_manager = pool_manager
        self.data_service = data_service
        self.ui_service = ui_service

        # State
        self.position_options: List[StartPositionOption] = []
        self._loading_positions = False  # Flag to prevent infinite loops

        # UI components
        self.main_container = None
        self.grid_layout = None
        self.scroll_area = None

        self._setup_ui()
        logger.debug("StartPositionPickerContent initialized")

    def _setup_ui(self):
        """Setup the content UI - EXACT copy from original."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Main content area (single container that adapts)
        self.main_container = QWidget()
        self.grid_layout = QGridLayout(self.main_container)
        self.grid_layout.setSpacing(15)

        # Scroll area for content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setWidget(self.main_container)

        # Apply scroll area styling - EXACT copy from original
        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                background: transparent;
                border: none;
                border-radius: 16px;
            }
        """
        )

        layout.addWidget(self.scroll_area)

    def load_positions(self, grid_mode: str, is_advanced: bool):
        """Load position options based on mode - EXACT logic from original."""
        # Prevent infinite loops with a stronger guard
        if self._loading_positions:
            logger.warning(
                "Already loading positions, skipping to prevent infinite loop"
            )
            return

        self._loading_positions = True

        try:
            mode_str = "advanced" if is_advanced else "basic"
            logger.debug(f"Starting to load positions for {mode_str} mode")

            # Get position keys for current mode using UI service
            position_keys = self.ui_service.get_positions_for_mode(
                grid_mode, is_advanced
            )

            logger.debug(f"Loading {len(position_keys)} positions for {mode_str} mode")

            # Create position options
            self._create_position_options(position_keys, grid_mode)

            # Arrange in grid first
            self._arrange_positions_for_mode(is_advanced)

            # Apply sizing after layout is arranged to avoid interference
            self._apply_sizing_to_all_options(is_advanced)

            logger.info(
                f"Loaded {len(self.position_options)} positions in {mode_str} mode"
            )

        except Exception as e:
            logger.error(f"Error loading positions for current mode: {e}")
            # Create fallback options
            self._create_fallback_options(grid_mode)
        finally:
            # Use QTimer to reset the flag after a short delay to prevent rapid calls
            QTimer.singleShot(50, self._reset_loading_flag)

    def _reset_loading_flag(self):
        """Reset the loading flag after a delay - EXACT copy from original."""
        self._loading_positions = False

    def _create_position_options(self, position_keys: List[str], grid_mode: str):
        """Create position option widgets - EXACT logic from original."""
        # Clear existing options and properly cleanup pool resources
        for option in self.position_options:
            try:
                # Explicitly cleanup pool resources before removing
                if hasattr(option, "_cleanup_pool_resources"):
                    option._cleanup_pool_resources()
                option.setParent(None)
            except Exception as e:
                logger.warning(f"Error cleaning up position option: {e}")
        self.position_options.clear()

        # Create new options
        for position_key in position_keys:
            try:
                option = StartPositionOption(
                    position_key=position_key,
                    pool_manager=self.pool_manager,
                    data_service=self.data_service,
                    grid_mode=grid_mode,
                    enhanced_styling=True,
                    parent=self,
                )
                option.position_selected.connect(self._on_position_selected)
                self.position_options.append(option)

            except Exception as e:
                logger.warning(f"Failed to create option for {position_key}: {e}")

    def _create_fallback_options(self, grid_mode: str):
        """Create fallback options if normal loading fails - EXACT logic from original."""
        fallback_positions = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
        logger.warning(f"Creating fallback options: {fallback_positions}")
        self._create_position_options(fallback_positions, grid_mode)

    def _apply_option_sizing(self, option: StartPositionOption, is_advanced: bool):
        """Apply appropriate sizing to position option - EXACT logic from original."""
        try:
            # Get main window width for sizing calculation
            main_window = self.window()
            container_width = main_window.width() if main_window else 1000

            # Calculate size using UI service
            size = self.ui_service.calculate_option_size(container_width, is_advanced)

            # Apply the calculated size to the container
            option.setFixedSize(size, size)

            # Update the pictograph size to match the container
            if hasattr(option, "update_pictograph_size"):
                option.update_pictograph_size(size)
                logger.debug(
                    f"Applied sizing: container={size}px, advanced={is_advanced}"
                )

            option.show()
            option.setVisible(True)

        except Exception as e:
            logger.warning(f"Failed to apply option sizing: {e}")
            # Fallback sizing
            default_size = 100 if is_advanced else 120
            option.setFixedSize(default_size, default_size)

            # Apply fallback pictograph sizing too
            if hasattr(option, "update_pictograph_size"):
                option.update_pictograph_size(default_size)

    def _apply_sizing_to_all_options(self, is_advanced: bool):
        """Apply sizing to all position options after layout is arranged - EXACT logic from original."""
        for option in self.position_options:
            self._apply_option_sizing(option, is_advanced)

    def _arrange_positions_for_mode(self, is_advanced: bool):
        """Arrange position options based on mode - EXACT logic from original."""
        # Determine layout based on mode and position count
        if is_advanced:
            self._arrange_advanced_layout()
        else:
            # AUTO mode - decide based on position count
            if len(self.position_options) <= 3:
                self._arrange_basic_layout()
            else:
                self._arrange_advanced_layout()

    def _arrange_basic_layout(self):
        """Arrange 3 positions responsively - EXACT logic from original."""
        # Always arrange horizontally in a single row for Simple mode
        # This matches the legacy behavior where 3 positions are displayed horizontally
        for i, option in enumerate(self.position_options):
            self.grid_layout.addWidget(option, 0, i)
            # Ensure widgets are visible and properly sized
            option.show()
            option.setVisible(True)

        # Set column stretch to ensure horizontal distribution
        for i in range(len(self.position_options)):
            self.grid_layout.setColumnStretch(i, 1)

        # Force complete layout recalculation
        self.grid_layout.activate()
        self.grid_layout.update()
        self.main_container.updateGeometry()

        # Process events to ensure layout is applied
        QApplication.processEvents()

        logger.debug(
            f"✅ Arranged {len(self.position_options)} positions horizontally in basic mode"
        )

    def _arrange_advanced_layout(self):
        """Arrange positions in 4x4 grid - EXACT logic from original."""
        for i, option in enumerate(self.position_options):
            row, col = divmod(i, 4)
            self.grid_layout.addWidget(option, row, col)

        # Force layout update
        self.grid_layout.update()
        self.main_container.updateGeometry()

        logger.debug(
            f"✅ Arranged {len(self.position_options)} positions in 4x4 advanced grid"
        )

    def clear_grid_layout(self):
        """Clear all widgets from grid layout and reset its structure - EXACT logic from original."""
        # Remove all widgets from the layout
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item and item.widget():
                item.widget().setParent(None)

        # Reset column stretches to prevent layout conflicts
        for i in range(10):  # Clear up to 10 columns (more than we'll ever use)
            self.grid_layout.setColumnStretch(i, 0)

        # Force the grid layout to completely reset its internal structure
        # This ensures clean transitions between different grid arrangements
        self.grid_layout.invalidate()

        # Clear any cached geometry information
        self.main_container.updateGeometry()

        logger.debug("Grid layout cleared and structure reset for mode switching")

    def apply_sizing(self, container_width: int, is_advanced: bool):
        """Apply sizing to all position options."""
        for option in self.position_options:
            self._apply_option_sizing(option, is_advanced)

    def _on_position_selected(self, position_key: str):
        """Handle position selection from option."""
        logger.debug(f"Position selected in content: {position_key}")
        self.position_selected.emit(position_key)
