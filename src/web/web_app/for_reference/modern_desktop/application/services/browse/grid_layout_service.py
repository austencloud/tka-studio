"""
Grid Layout Service

Handles all grid layout operations for the sequence browser panel.
Provides clean interface for grid management with proper error handling.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QWidget


logger = logging.getLogger(__name__)


class GridLayoutService:
    """
    Service for managing grid layout operations in the sequence browser.

    Handles:
    - Grid layout validation and recreation
    - Section header creation and positioning
    - Thumbnail widget positioning
    - Empty state and fallback displays
    """

    def __init__(
        self, grid_widget: QWidget, initial_grid_layout: QGridLayout | None = None
    ):
        """
        Initialize the grid layout service.

        Args:
            grid_widget: The widget that contains the grid layout
            initial_grid_layout: Optional existing grid layout to manage
        """
        self.grid_widget = grid_widget
        self.grid_layout = initial_grid_layout
        self._ensure_valid_layout()

    def _ensure_valid_layout(self) -> bool:
        """
        Ensure grid layout is valid and recreate if necessary.

        Returns:
            True if layout is valid or was successfully recreated, False otherwise
        """
        if self.grid_layout is None or not bool(self.grid_layout):
            logger.warning(
                "⚠️ [GRID_LAYOUT] Invalid grid layout, attempting to recreate"
            )

            if self.grid_widget:
                self.grid_layout = QGridLayout(self.grid_widget)
                self.grid_layout.setSpacing(15)

                # Set column stretch factors for 3 equal columns
                for col in range(3):
                    self.grid_layout.setColumnStretch(col, 1)

                logger.info(
                    f"🔧 [GRID_LAYOUT] Recreated grid layout: {self.grid_layout}"
                )
                return True
            logger.error(
                "❌ [GRID_LAYOUT] Cannot recreate grid layout - no grid widget"
            )
            return False
        return True

    def clear_grid(self) -> None:
        """Clear all items from the grid layout."""
        if not self._ensure_valid_layout():
            logger.warning(
                "⚠️ [CLEAR_GRID] Cannot ensure valid grid layout, skipping clear"
            )
            return

        item_count = self.grid_layout.count()
        logger.info(f"🔍 [CLEAR_GRID] Clearing {item_count} items from grid")

        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def add_section_header(self, section_name: str, current_row: int) -> int:
        """
        Add a section header to the grid.

        Args:
            section_name: Name of the section
            current_row: Current row position in the grid

        Returns:
            The row number of the added header
        """
        if not self._ensure_valid_layout():
            logger.warning(
                "⚠️ [ADD_SECTION_HEADER] Grid layout invalid, skipping header"
            )
            return current_row

        header_widget = QFrame()
        header_widget.setStyleSheet(
            """
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                margin: 10px 0px;
            }
        """
        )

        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(15, 8, 15, 8)

        # Section title
        title_label = QLabel(section_name)
        title_font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        if current_row > 0:
            current_row += 1
        self.grid_layout.addWidget(header_widget, current_row, 0, 1, 3)

        return current_row

    def add_thumbnail_to_grid(self, thumbnail: QWidget, row: int, col: int) -> None:
        """
        Add a thumbnail widget to the grid at specified position.

        Args:
            thumbnail: The thumbnail widget to add
            row: Grid row position
            col: Grid column position
        """
        if not self._ensure_valid_layout():
            logger.warning("⚠️ [ADD_THUMBNAIL] Grid layout invalid, skipping thumbnail")
            return

        self.grid_layout.addWidget(thumbnail, row, col)

    def add_empty_state(self) -> None:
        """Add empty state message to the grid."""
        if not self._ensure_valid_layout():
            return

        empty_label = QLabel("No sequences found")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 14px;")
        self.grid_layout.addWidget(empty_label, 0, 0, 1, 3)

    def add_loading_fallback(self) -> None:
        """Add loading fallback message to the grid."""
        if not self._ensure_valid_layout():
            return

        loading_label = QLabel("Loading sequences...")
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 14px;")
        self.grid_layout.addWidget(loading_label, 0, 0, 1, 3)

    def get_row_count(self) -> int:
        """Get the current number of rows in the grid."""
        if not self._ensure_valid_layout():
            return 0
        return self.grid_layout.rowCount()

    def get_item_count(self) -> int:
        """Get the current number of items in the grid."""
        if not self._ensure_valid_layout():
            return 0
        return self.grid_layout.count()

    def is_valid(self) -> bool:
        """Check if the grid layout is currently valid."""
        return self.grid_layout is not None and bool(self.grid_layout)
