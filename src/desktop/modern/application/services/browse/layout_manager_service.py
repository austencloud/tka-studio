"""
Layout Manager Service

Service for managing grid layout and section organization.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QWidget

from desktop.modern.core.interfaces.browse_services import ILayoutManager


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
        """Add a modern section header to the grid."""
        header_widget = QFrame()
        header_widget.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(100, 150, 255, 0.15),
                    stop:1 rgba(150, 100, 255, 0.15)
                );
                border: 1px solid rgba(100, 150, 255, 0.3);
                border-radius: 10px;
                margin: 12px 0px;
                padding: 8px 16px;
            }
        """
        )

        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 12, 20, 12)

        title_label = QLabel(section_name)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(
            """
            QLabel {
                color: rgba(80, 120, 200, 0.95);
                background: transparent;
                border: none;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
            """
        )
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        if current_row > 0:
            current_row += 1
        self.grid_layout.addWidget(header_widget, current_row, 0, 1, 3)

        return current_row

    def add_skeleton_section_header(self, section_name: str, current_row: int) -> int:
        """Add a skeleton section header placeholder to the grid."""
        skeleton_header = QFrame()
        skeleton_header.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f5f5f5,
                    stop:0.5 #e8e8e8,
                    stop:1 #f5f5f5
                );
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                margin: 10px 0px;
                min-height: 35px;
            }
        """
        )

        header_layout = QHBoxLayout(skeleton_header)
        header_layout.setContentsMargins(15, 8, 15, 8)

        # Skeleton title placeholder
        title_skeleton = QLabel()
        title_skeleton.setFixedSize(120, 16)
        title_skeleton.setStyleSheet(
            """
            QLabel {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e0e0e0,
                    stop:0.5 #d0d0d0,
                    stop:1 #e0e0e0
                );
                border-radius: 3px;
            }
        """
        )
        header_layout.addWidget(title_skeleton)
        header_layout.addStretch()

        if current_row > 0:
            current_row += 1
        self.grid_layout.addWidget(skeleton_header, current_row, 0, 1, 3)

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
