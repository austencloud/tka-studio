"""
Modern Browse Control Panel

The control panel that sits above the browser area and navigation panel.
Provides sort controls, filter description, and sequence count display.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.application.services.browse.browse_state_service import (
    BrowseStateService,
)
from desktop.modern.domain.models.browse_models import FilterType
from desktop.modern.presentation.components.browse.sort_widget import SortWidget


class BrowseControlPanel(QFrame):
    """
    Modern control panel for Browse tab.

    Sits above the browser area and provides:
    - Back to filters button
    - Filter description label
    - Sort widget with buttons
    - Results count label
    """

    # Signals
    back_to_filters = pyqtSignal()
    sort_changed = pyqtSignal(str)  # sort_method

    def __init__(
        self, state_service: BrowseStateService, parent: QWidget | None = None
    ):
        super().__init__(parent)

        self.state_service = state_service
        self.current_filter_description = "No filter applied"
        self.current_count = 0

        self._setup_ui()
        self._apply_styling()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup the control panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # Top row: Back button, title, sort widget
        top_row = QHBoxLayout()
        top_row.setSpacing(15)

        # Back button
        self.back_button = QPushButton("← Back to Filters")
        self.back_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.back_button.setStyleSheet(
            """
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.15);
            }
        """
        )
        top_row.addWidget(self.back_button)

        # Title
        self.title_label = QLabel("Sequence Browser")
        self.title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: white;")
        top_row.addWidget(self.title_label)

        top_row.addStretch()

        # Sort widget
        self.sort_widget = SortWidget(self.state_service)
        top_row.addWidget(self.sort_widget)

        layout.addLayout(top_row)

        # Bottom row: Filter description and count
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(15)

        # Filter description label
        self.filter_label = QLabel(self.current_filter_description)
        self.filter_label.setFont(QFont("Segoe UI", 11))
        self.filter_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        bottom_row.addWidget(self.filter_label)

        bottom_row.addStretch()

        # Count label
        self.count_label = QLabel(f"Sequences: {self.current_count}")
        self.count_label.setFont(QFont("Segoe UI", 11))
        self.count_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        bottom_row.addWidget(self.count_label)

        layout.addLayout(bottom_row)

    def _apply_styling(self) -> None:
        """Apply modern glassmorphism styling."""
        self.setStyleSheet(
            """
            BrowseControlPanel {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
            }
        """
        )

    def _connect_signals(self) -> None:
        """Connect control panel signals."""
        self.back_button.clicked.connect(self.back_to_filters.emit)
        self.sort_widget.sort_changed.connect(self.sort_changed.emit)

    def update_filter_description(
        self, filter_type: FilterType | None, filter_values: Any
    ) -> None:
        """Update the filter description label."""
        if filter_type is None:
            description = "All sequences"
        elif filter_type == FilterType.STARTING_LETTER:
            description = f"Sequences starting with {filter_values}"
        elif filter_type == FilterType.CONTAINS_LETTERS:
            description = f"Sequences containing {filter_values}"
        elif filter_type == FilterType.LENGTH:
            description = f"Sequences of length {filter_values}"
        elif filter_type == FilterType.DIFFICULTY:
            description = f"Level {filter_values} sequences"
        elif filter_type == FilterType.STARTING_POSITION:
            description = f"Sequences starting in {filter_values}"
        elif filter_type == FilterType.AUTHOR:
            description = f"Sequences by {filter_values}"
        elif filter_type == FilterType.FAVORITES:
            description = "Favorite sequences"
        elif filter_type == FilterType.RECENT:
            description = "Recently added sequences"
        else:
            description = f"Filtered sequences ({filter_type.value})"

        self.current_filter_description = description
        self.filter_label.setText(description)

    def update_count(self, count) -> None:
        """Update the sequence count label."""
        if isinstance(count, str):
            # Handle string count (e.g., "Loading...")
            self.count_label.setText(count)
        else:
            # Handle integer count
            self.current_count = count
            if count == 0:
                self.count_label.setText("No sequences")
            elif count == 1:
                self.count_label.setText("1 sequence")
            else:
                self.count_label.setText(f"{count} sequences")

    def get_current_sort_method(self) -> str:
        """Get the current sort method."""
        return self.sort_widget.get_current_sort_method()

    def set_sort_method(self, sort_method: str) -> None:
        """Set the sort method."""
        self.sort_widget.set_sort_method(sort_method)
