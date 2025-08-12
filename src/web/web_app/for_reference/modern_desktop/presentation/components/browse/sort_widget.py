from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QWidget,
)

from desktop.modern.application.services.browse.browse_state_service import (
    BrowseStateService,
)
from desktop.modern.domain.models.browse_models import SortMethod
from desktop.modern.presentation.components.browse.sort_button import SortButton


class SortWidget(QWidget):
    """Modern sort widget with horizontal button bar."""

    # Signal emitted when sort method changes
    sort_changed = pyqtSignal(str)  # sort_method

    def __init__(
        self, state_service: BrowseStateService, parent: QWidget | None = None
    ):
        super().__init__(parent)

        self.state_service = state_service
        self.sort_buttons = {}
        self.current_sort_method = "alphabetical"

        self._setup_ui()
        self._connect_signals()
        self._load_initial_state()

    def _setup_ui(self) -> None:
        """Setup the sort widget UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # "Sort:" label
        sort_label = QLabel("Sort:")
        sort_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        sort_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        layout.addWidget(sort_label)

        # Sort buttons
        sort_options = [
            ("A-Z", "alphabetical"),
            ("Length", "length"),
            ("Level", "level"),
            ("Date", "date_added"),
        ]

        for label, method in sort_options:
            button = SortButton(label, method)
            self.sort_buttons[method] = button
            layout.addWidget(button)

        layout.addStretch()

    def _connect_signals(self) -> None:
        """Connect sort button signals."""
        for button in self.sort_buttons.values():
            button.sort_selected.connect(self._on_sort_selected)

    def _load_initial_state(self) -> None:
        """Load initial sort state from service."""
        current_sort = self.state_service.get_current_sort_method()
        self.set_sort_method(current_sort.value)

    def _on_sort_selected(self, sort_method: str) -> None:
        """Handle sort button selection."""
        if sort_method != self.current_sort_method:
            self.set_sort_method(sort_method)

            # Save to state service
            sort_enum = SortMethod(sort_method)
            self.state_service.set_sort_method(sort_enum)

            # Emit signal
            self.sort_changed.emit(sort_method)

    def set_sort_method(self, sort_method: str) -> None:
        """Update the active sort method."""
        self.current_sort_method = sort_method

        # Update button states
        for method, button in self.sort_buttons.items():
            button.set_selected(method == sort_method)

    def get_current_sort_method(self) -> str:
        """Get the current sort method."""
        return self.current_sort_method
