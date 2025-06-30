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

import logging
from typing import Optional

from domain.models.core_models import BeatData
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from presentation.components.pictograph.pictograph_component import PictographComponent
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
    pictograph_updated = pyqtSignal(BeatData)  # Emitted when pictograph is updated
    info_panel_updated = pyqtSignal(
        int, object
    )  # Emitted when info panel is updated (BeatData or None)

    def __init__(self, parent=None, pictograph_size: int = 140):
        """
        Initialize the pictograph display section.

        Args:
            parent: Parent widget (typically the graph editor)
            pictograph_size: Size for the pictograph component (default: 140px)
        """
        super().__init__(parent)
        self._pictograph_size = pictograph_size
        self._current_beat_index: Optional[int] = None
        self._current_beat_data: Optional[BeatData] = None

        # Initialize components
        self._pictograph_component: Optional[PictographComponent] = None
        self._info_panel: Optional[DetailedInfoPanel] = None

        self._setup_ui()
        logger.debug(
            f"PictographDisplaySection initialized with size {pictograph_size}"
        )

    def _setup_ui(self):
        """Set up the pictograph display section UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Create horizontal layout for pictograph and info panel
        display_layout = QHBoxLayout()
        display_layout.setSpacing(15)

        # Left side: Large square pictograph display (1:1 aspect ratio, maximized)
        pictograph_container = self._create_pictograph_container()
        display_layout.addWidget(pictograph_container, 0)  # Fixed width, no stretch

        # Right side: Detailed information panel (takes remaining space)
        self._info_panel = DetailedInfoPanel(parent=self)
        self._info_panel.setMinimumWidth(200)
        self._info_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        display_layout.addWidget(self._info_panel, 1)  # Takes all remaining width

        layout.addLayout(display_layout, 1)  # Give it stretch

    def _create_pictograph_container(self) -> QWidget:
        """
        Create the pictograph container with proper sizing and centering.

        Returns:
            QWidget: Container widget with centered pictograph component
        """
        pictograph_container = QWidget()
        pictograph_container.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )
        pictograph_layout = QVBoxLayout(pictograph_container)
        pictograph_layout.setContentsMargins(
            5, 5, 5, 5
        )  # Small margin for glassmorphism border
        pictograph_layout.setSpacing(0)

        # Create the TKA pictograph component with specified size
        self._pictograph_component = PictographComponent(parent=self)
        self._pictograph_component.setFixedSize(
            self._pictograph_size, self._pictograph_size
        )  # Force 1:1 aspect ratio
        self._pictograph_component.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )

        # Center the pictograph component vertically and horizontally
        pictograph_layout.addStretch()
        pictograph_layout.addWidget(self._pictograph_component)
        pictograph_layout.addStretch()

        # Set container width to match pictograph width plus margins
        pictograph_container.setFixedWidth(self._pictograph_size + 10)

        return pictograph_container

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
        if beat_data and self._pictograph_component:
            self._pictograph_component.update_from_beat(beat_data)
            self.pictograph_updated.emit(beat_data)
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

    def update_pictograph_only(self, beat_data: BeatData):
        """
        Update only the pictograph component without changing the info panel.

        This method is useful for real-time updates during editing where the
        pictograph needs to reflect changes but the info panel should remain stable.

        Args:
            beat_data: Beat data to display in the pictograph
        """
        if self._pictograph_component:
            self._pictograph_component.update_from_beat(beat_data)
            self.pictograph_updated.emit(beat_data)
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

    def get_pictograph_component(self) -> Optional[PictographComponent]:
        """
        Get the pictograph component for direct access if needed.

        Returns:
            PictographComponent: The pictograph component instance
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
        Update the pictograph size dynamically.

        Args:
            size: New size for the pictograph (width and height)
        """
        if self._pictograph_component:
            self._pictograph_size = size
            self._pictograph_component.setFixedSize(size, size)
            # Update container width
            if self._pictograph_component.parent():
                self._pictograph_component.parent().setFixedWidth(size + 10)
            logger.debug(f"Pictograph size updated to {size}px")
