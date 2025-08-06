"""
Pictograph Display Section Component for TKA Graph Editor
========================================================

Manages the top section of the graph editor containing the large pictograph display
and detailed information panel. This component maintains the 1:1 aspect ratio for
the pictograph and provides optimal layout for beat visualization.

Features:
- Large centered pictograph display with 1:1 aspect ratio
- Integrated detailed information panel
- Responsive layout with proper spacing
- Clean component separation following TKA architecture

Architecture:
- Follows TKA presentation layer patterns
- Uses dependency injection for pictograph component
- Maintains clean separation between display and data logic
- Supports signal-based communication with parent components
"""

from __future__ import annotations

import logging
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QSizePolicy, QVBoxLayout, QWidget

from desktop.modern.domain.models import BeatData
from desktop.modern.presentation.components.pictograph.views import (
    BasePictographView,
    create_pictograph_view,
)

from .detailed_info_panel import DetailedInfoPanel


logger = logging.getLogger(__name__)


class PictographDisplaySection(QWidget):
    """
    Top section of the graph editor containing pictograph display and information panel.

    This component manages the layout and coordination between the large pictograph
    display and the detailed information panel. It ensures proper sizing, maintains
    the 1:1 aspect ratio for the pictograph, and provides a clean interface for
    updating the display based on beat selection.

    Layout Structure:
    - Horizontal layout with pictograph (left) and info panel (right)
    - Pictograph: Fixed 1:1 aspect ratio, centered vertically
    - Info panel: Takes remaining horizontal space, expandable
    """

    # Signals for communication with parent components
    pictograph_updated = pyqtSignal(
        int, object
    )  # Emitted when pictograph is updated (beat_index, beat_data)
    info_panel_updated = pyqtSignal(
        int, object
    )  # Emitted when info panel is updated (BeatData or None)

    def __init__(self, parent=None):
        """
        Initialize the pictograph display section with responsive sizing.

        Args:
            parent: Parent widget (typically the graph editor)
        """
        super().__init__(parent)

        # Responsive sizing configuration
        self._min_pictograph_size = 200  # Minimum size constraint
        self._max_pictograph_size = 500  # Maximum size constraint
        self._current_pictograph_size = 280  # Initial size (will be recalculated)

        # Layout configuration
        self._info_panel_min_width = 180
        self._info_panel_max_width = 250
        self._component_spacing = 15
        self._container_margins = 8

        # State tracking
        self._current_beat_index: Optional[int] = None
        self._current_beat_data: Optional[BeatData] = None
        self._resize_pending = False

        # Initialize components
        self._pictograph_component: Optional[BasePictographView] = None
        self._info_panel: Optional[DetailedInfoPanel] = None

        self._setup_ui()
        logger.debug("PictographDisplaySection initialized with responsive sizing")

    def _calculate_optimal_pictograph_size(self) -> int:
        """
        Calculate optimal pictograph size based on available container space.

        Returns:
            int: Optimal pictograph size (width and height, maintaining 1:1 aspect ratio)
        """
        # Get current container width
        container_width = self.width()
        if container_width <= 0:
            # If container not yet sized, use current size
            return self._current_pictograph_size

        # Calculate reserved space
        reserved_space = (
            self._info_panel_min_width  # Minimum space for info panel
            + self._component_spacing  # Space between components
            + (self._container_margins * 2)  # Left and right margins
        )

        # Calculate available width for pictograph
        available_width = container_width - reserved_space

        # Apply size constraints (min/max) and maintain square aspect ratio
        optimal_size = max(
            self._min_pictograph_size, min(self._max_pictograph_size, available_width)
        )

        logger.debug(
            f"Calculated optimal pictograph size: {optimal_size}px "
            f"(container: {container_width}px, available: {available_width}px)"
        )

        return optimal_size

    def _update_pictograph_size(self, new_size: int) -> None:
        """
        Update the pictograph component size dynamically.

        Args:
            new_size: New size for the pictograph (width and height)
        """
        if new_size == self._current_pictograph_size:
            return  # No change needed

        self._current_pictograph_size = new_size

        if self._pictograph_component:
            self._pictograph_component.setFixedSize(new_size, new_size)
            logger.debug(f"Pictograph size updated to {new_size}px")

    def _setup_ui(self):
        """Set up the pictograph display section UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Create horizontal layout for pictograph and info panel
        display_layout = QHBoxLayout()
        display_layout.setSpacing(15)

        # Left side: Large square pictograph display (takes most space now!)
        pictograph_container = self._create_pictograph_container()
        display_layout.addWidget(
            pictograph_container, 2
        )  # Give it more space (2:1 ratio)

        # Right side: Detailed information panel (takes remaining space)
        self._info_panel = DetailedInfoPanel(parent=self)
        self._info_panel.setMinimumWidth(180)  # Slightly smaller minimum
        self._info_panel.setMaximumWidth(
            250
        )  # Limit max width so pictograph gets more space
        self._info_panel.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        display_layout.addWidget(self._info_panel, 1)  # Takes remaining width

        layout.addLayout(display_layout, 1)  # Give it stretch

    def _create_pictograph_container(self) -> QWidget:
        """
        Create the pictograph container with proper sizing and centering.

        Returns:
            QWidget: Container widget with centered pictograph component
        """
        pictograph_container = QWidget()
        pictograph_container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,  # Allow it to expand!
        )
        pictograph_layout = QVBoxLayout(pictograph_container)
        pictograph_layout.setContentsMargins(
            8, 8, 8, 8
        )  # Small margin for glassmorphism border
        pictograph_layout.setSpacing(0)

        # Create the TKA pictograph view with responsive sizing
        self._pictograph_component = create_pictograph_view("base", parent=self)

        # Calculate initial optimal size
        initial_size = self._calculate_optimal_pictograph_size()
        self._pictograph_component.setFixedSize(initial_size, initial_size)
        self._current_pictograph_size = initial_size

        self._pictograph_component.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )

        # Center the pictograph component vertically and horizontally
        pictograph_layout.addStretch()
        pictograph_layout.addWidget(
            self._pictograph_component, 0, Qt.AlignmentFlag.AlignCenter
        )
        pictograph_layout.addStretch()

        # Don't set fixed width - let it expand to use available space

        return pictograph_container

    def resizeEvent(self, event):
        """
        Handle resize events to update pictograph size dynamically.

        Args:
            event: QResizeEvent containing old and new size information
        """
        super().resizeEvent(event)

        # Avoid recursive resize events
        if self._resize_pending:
            return

        self._resize_pending = True

        try:
            # Calculate new optimal size based on new container dimensions
            new_size = self._calculate_optimal_pictograph_size()

            # Update pictograph size if it changed significantly
            if (
                abs(new_size - self._current_pictograph_size) > 5
            ):  # 5px threshold to avoid micro-adjustments
                self._update_pictograph_size(new_size)

        finally:
            self._resize_pending = False

    def update_display(self, beat_index: int, beat_data: Optional[BeatData]):
        """
        Update both the pictograph and information panel with new beat data.

        Args:
            beat_index: Index of the beat (-1 for start position)
            beat_data: Beat data to display (None to clear)
        """
        self._current_beat_index = beat_index
        self._current_beat_data = beat_data

        # Update pictograph component
        if beat_data and beat_data.pictograph_data and self._pictograph_component:
            self._pictograph_component.update_from_pictograph_data(
                beat_data.pictograph_data
            )
            self.pictograph_updated.emit(beat_index, beat_data)
            logger.debug(
                f"Pictograph updated for beat {beat_index}: {beat_data.letter}"
            )
        elif self._pictograph_component:
            self._pictograph_component.clear_pictograph()
            logger.debug("Pictograph cleared")

        # Update information panel
        if self._info_panel:
            self._info_panel.update_beat_info(beat_index, beat_data)
            self.info_panel_updated.emit(beat_index, beat_data)

    def update_pictograph_only(self, beat_index: int, beat_data: BeatData):
        """
        Update only the pictograph component without changing the info panel.

        This method is useful for real-time updates during editing where the
        pictograph needs to reflect changes but the info panel should remain stable.

        Args:
            beat_index: Index of the beat being updated
            beat_data: Beat data to display in the pictograph
        """
        if self._pictograph_component and beat_data and beat_data.pictograph_data:
            self._pictograph_component.update_from_pictograph_data(
                beat_data.pictograph_data
            )
            self.pictograph_updated.emit(beat_index, beat_data)
            logger.debug(f"Pictograph-only update: {beat_data.letter}")

    def update_info_panel_only(self, beat_index: int, beat_data: Optional[BeatData]):
        """
        Update only the information panel without changing the pictograph.

        This method is useful when the beat information changes but the visual
        representation should remain the same.

        Args:
            beat_index: Index of the beat (-1 for start position)
            beat_data: Beat data to display (None to clear)
        """
        if self._info_panel:
            self._info_panel.update_beat_info(beat_index, beat_data)
            self.info_panel_updated.emit(beat_index, beat_data)

    def clear_display(self):
        """Clear both the pictograph and information panel"""
        self.update_display(-1, None)

    def get_pictograph_component(self) -> Optional[BasePictographView]:
        """
        Get the pictograph view for direct access if needed.

        Returns:
            BasePictographView: The pictograph view instance
        """
        return self._pictograph_component

    def get_info_panel(self) -> Optional[DetailedInfoPanel]:
        """
        Get the info panel component for direct access if needed.

        Returns:
            DetailedInfoPanel: The info panel component instance
        """
        return self._info_panel

    def get_current_beat_data(self) -> Optional[BeatData]:
        """
        Get the currently displayed beat data.

        Returns:
            BeatData: Currently displayed beat data, or None if no beat is displayed
        """
        return self._current_beat_data

    def get_current_beat_index(self) -> Optional[int]:
        """
        Get the currently displayed beat index.

        Returns:
            int: Currently displayed beat index, or None if no beat is displayed
        """
        return self._current_beat_index

    def set_pictograph_size(self, size: int):
        """
        Update the pictograph size dynamically (legacy method - now uses responsive system).

        Args:
            size: New size for the pictograph (width and height)
        """
        # Apply size constraints from responsive system
        constrained_size = max(
            self._min_pictograph_size, min(self._max_pictograph_size, size)
        )

        # Use the responsive update method
        self._update_pictograph_size(constrained_size)

        logger.debug(
            f"Pictograph size set to {constrained_size}px (requested: {size}px)"
        )

    def get_current_pictograph_size(self) -> int:
        """
        Get the current pictograph size.

        Returns:
            int: Current pictograph size (width and height)
        """
        return self._current_pictograph_size

    def get_size_constraints(self) -> tuple[int, int]:
        """
        Get the minimum and maximum size constraints for the pictograph.

        Returns:
            tuple[int, int]: (min_size, max_size)
        """
        return (self._min_pictograph_size, self._max_pictograph_size)

    def set_size_constraints(self, min_size: int, max_size: int):
        """
        Update the size constraints for responsive sizing.

        Args:
            min_size: Minimum pictograph size
            max_size: Maximum pictograph size
        """
        self._min_pictograph_size = max(100, min_size)  # Absolute minimum of 100px
        self._max_pictograph_size = min(800, max_size)  # Absolute maximum of 800px

        # Recalculate size with new constraints
        new_size = self._calculate_optimal_pictograph_size()
        self._update_pictograph_size(new_size)

        logger.debug(
            f"Size constraints updated: min={self._min_pictograph_size}px, max={self._max_pictograph_size}px"
        )
