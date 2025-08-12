"""
Codex Component

Main container component for the codex functionality.
Coordinates control panel, scroll area, and pictograph grid.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from desktop.modern.domain.services.codex import (
    CodexDataService,
    CodexOperationsService,
)
from desktop.modern.presentation.components.codex.control_panel import CodexControlPanel
from desktop.modern.presentation.components.codex.pictograph_grid import (
    CodexPictographGrid,
)
from desktop.modern.presentation.components.codex.scroll_area import CodexScrollArea


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class CodexComponent(QWidget):
    """
    Main codex component that coordinates all codex functionality.

    Provides the complete codex interface including:
    - Control panel for operations
    - Scrollable pictograph grid
    - Data management and operations
    """

    # Signals for external communication
    error_occurred = pyqtSignal(str)
    operation_completed = pyqtSignal(str)  # Operation name

    def __init__(self, container: DIContainer, parent=None):
        super().__init__(parent)

        self.container = container

        # Set object name for styling
        self.setObjectName("codex_component")

        # Get services
        self.data_service = container.resolve(CodexDataService)
        self.operations_service = container.resolve(CodexOperationsService)

        # Component references
        self.control_panel: CodexControlPanel | None = None
        self.scroll_area: CodexScrollArea | None = None
        self.pictograph_grid: CodexPictographGrid | None = None

        # Setup UI
        self._setup_ui()

        # Connect signals
        self._connect_signals()

        logger.info("CodexComponent initialized")

    def _setup_ui(self) -> None:
        """Setup the main UI structure."""
        try:
            # Main layout
            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setSpacing(0)

            # Create control panel
            self.control_panel = CodexControlPanel(self.container, self)
            main_layout.addWidget(self.control_panel)

            # Create scroll area
            self.scroll_area = CodexScrollArea(self.container, self)

            # Create pictograph grid
            self.pictograph_grid = CodexPictographGrid(self.container, self)

            # Set grid as scroll area content
            self.scroll_area.setWidget(self.pictograph_grid)

            # Add scroll area to main layout
            main_layout.addWidget(self.scroll_area, 1)  # Give it stretch

            # Apply component styling - solid background to block animated backgrounds
            self.setStyleSheet("""
                CodexComponent {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                }
            """)

            logger.debug("Codex UI setup complete")

        except Exception as e:
            logger.error(f"Failed to setup codex UI: {e}")
            self.error_occurred.emit(f"Failed to initialize codex: {e!s}")

    def _connect_signals(self) -> None:
        """Connect component signals."""
        if self.control_panel:
            # Connect control panel signals
            self.control_panel.rotate_requested.connect(self._handle_rotate)
            self.control_panel.mirror_requested.connect(self._handle_mirror)
            self.control_panel.color_swap_requested.connect(self._handle_color_swap)
            self.control_panel.orientation_changed.connect(
                self._handle_orientation_change
            )

    def _handle_rotate(self) -> None:
        """Handle rotate operation."""
        try:
            logger.debug("Handling rotate operation")

            # Get current pictograph data
            current_data = self.data_service.get_all_pictograph_data()

            # Apply rotation operation
            rotated_data = self.operations_service.apply_operation_to_all(
                current_data, "rotate"
            )

            # Update the grid
            if self.pictograph_grid:
                self.pictograph_grid.update_all_pictographs(rotated_data)

            self.operation_completed.emit("rotate")
            logger.info("Rotate operation completed")

        except Exception as e:
            logger.error(f"Failed to rotate pictographs: {e}")
            self.error_occurred.emit(f"Failed to rotate pictographs: {e!s}")

    def _handle_mirror(self) -> None:
        """Handle mirror operation."""
        try:
            logger.debug("Handling mirror operation")

            # Get current pictograph data
            current_data = self.data_service.get_all_pictograph_data()

            # Apply mirror operation
            mirrored_data = self.operations_service.apply_operation_to_all(
                current_data, "mirror"
            )

            # Update the grid
            if self.pictograph_grid:
                self.pictograph_grid.update_all_pictographs(mirrored_data)

            self.operation_completed.emit("mirror")
            logger.info("Mirror operation completed")

        except Exception as e:
            logger.error(f"Failed to mirror pictographs: {e}")
            self.error_occurred.emit(f"Failed to mirror pictographs: {e!s}")

    def _handle_color_swap(self) -> None:
        """Handle color swap operation."""
        try:
            logger.debug("Handling color swap operation")

            # Get current pictograph data
            current_data = self.data_service.get_all_pictograph_data()

            # Apply color swap operation
            swapped_data = self.operations_service.apply_operation_to_all(
                current_data, "color_swap"
            )

            # Update the grid
            if self.pictograph_grid:
                self.pictograph_grid.update_all_pictographs(swapped_data)

            self.operation_completed.emit("color_swap")
            logger.info("Color swap operation completed")

        except Exception as e:
            logger.error(f"Failed to swap colors: {e}")
            self.error_occurred.emit(f"Failed to swap colors: {e!s}")

    def _handle_orientation_change(self, orientation: str) -> None:
        """
        Handle orientation change.

        Args:
            orientation: New orientation setting
        """
        try:
            logger.debug(f"Handling orientation change to: {orientation}")

            # For now, just log the change
            # In a full implementation, this would update the pictograph rendering

            self.operation_completed.emit(f"orientation_{orientation}")
            logger.info(f"Orientation changed to: {orientation}")

        except Exception as e:
            logger.error(f"Failed to change orientation: {e}")
            self.error_occurred.emit(f"Failed to change orientation: {e!s}")

    def refresh_codex(self) -> None:
        """Refresh the entire codex display."""
        try:
            logger.debug("Refreshing codex")

            # Refresh data service
            self.data_service.refresh_data()

            # Refresh grid
            if self.pictograph_grid:
                self.pictograph_grid.refresh_grid()

            logger.info("Codex refreshed successfully")

        except Exception as e:
            logger.error(f"Failed to refresh codex: {e}")
            self.error_occurred.emit(f"Failed to refresh codex: {e!s}")

    def set_pictograph_size(self, size: int) -> None:
        """
        Set the size for pictograph displays.

        Args:
            size: New size in pixels
        """
        if self.pictograph_grid:
            self.pictograph_grid.set_pictograph_size(size)

    def get_current_orientation(self) -> str:
        """Get the current orientation setting."""
        if self.control_panel:
            return self.control_panel.get_current_orientation()
        return "Diamond"

    def set_orientation(self, orientation: str) -> None:
        """Set the orientation setting."""
        if self.control_panel:
            self.control_panel.set_orientation(orientation)

    def scroll_to_top(self) -> None:
        """Scroll to the top of the codex."""
        if self.scroll_area:
            self.scroll_area.scroll_to_top()

    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the codex."""
        if self.scroll_area:
            self.scroll_area.scroll_to_bottom()
