"""
Layout Manager Service

Service for managing grid layout and section organization.
"""

from desktop.modern.core.interfaces.browse_services import ILayoutManager
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QWidget


class LayoutManagerService(ILayoutManager):
    """Service for managing grid layout and sections."""

    def __init__(self, grid_layout: QGridLayout):
        """Initialize with the grid layout to manage."""
        self.grid_layout = grid_layout

    def clear_grid(self) -> None:
        """Clear all items from the grid layout."""
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def add_section_header(self, section_name: str, current_row: int) -> int:
        """Add a section header to the grid."""
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

        title_label = QLabel(section_name)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.9); background: transparent; border: none;"
        )
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        if current_row > 0:
            current_row += 1
        self.grid_layout.addWidget(header_widget, current_row, 0, 1, 3)

        return current_row

    def add_thumbnail_to_grid(self, thumbnail: QWidget, row: int, col: int) -> None:
        """Add a thumbnail widget to the grid at specified position."""
        self.grid_layout.addWidget(thumbnail, row, col)

    def set_row_stretch(self, row: int, stretch: int) -> None:
        """Set stretch factor for a grid row."""
        self.grid_layout.setRowStretch(row, stretch)

    def get_row_count(self) -> int:
        """Get the current number of rows in the grid."""
        return self.grid_layout.rowCount()

    def add_empty_state(self) -> None:
        """Add empty state message to the grid."""
        empty_label = QLabel("No sequences found")
        empty_label.setFont(QFont("Segoe UI", 14))
        empty_label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_layout.addWidget(empty_label, 0, 0, 1, 3)

    def add_loading_fallback(self) -> None:
        """Add loading fallback message to the grid."""
        loading_label = QLabel("Loading sequences...")
        loading_label.setFont(QFont("Segoe UI", 14))
        loading_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_layout.addWidget(loading_label, 0, 0, 1, 3)
