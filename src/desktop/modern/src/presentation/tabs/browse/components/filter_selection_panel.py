"""
Filter Selection Panel - Legacy Layout Matching

Matches the Legacy InitialFilterChoiceWidget layout exactly:
- Choose Filter Label header
- Responsive 3-column grid layout
- Glass-morphism styling with modern 2025 design
- Show All button separated at bottom
"""

from typing import Optional

from presentation.tabs.browse.models import FilterType
from presentation.tabs.browse.services.browse_service import BrowseService
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QResizeEvent
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class FilterSelectionPanel(QWidget):
    """
    Filter selection interface matching Legacy InitialFilterChoiceWidget layout.

    Features:
    - Choose Filter Label header
    - Responsive 3-column grid layout
    - Glass-morphism styling
    - Show All button separated at bottom
    """

    # Signals
    filter_selected = pyqtSignal(FilterType, object)  # filter_type, filter_value

    def __init__(self, browse_service: BrowseService, parent: Optional[QWidget] = None):
        """Initialize the filter selection panel."""
        super().__init__(parent)

        self.browse_service = browse_service
        self._grid_columns = 3  # Default columns like Legacy
        self._layout_initialized = False

        self._setup_modern_ui()
        self._connect_signals()

        # Defer layout calculations until widget is shown
        QTimer.singleShot(100, self._finalize_layout_initialization)

    def _setup_modern_ui(self) -> None:
        """Setup modern UI matching Legacy structure."""
        # Main layout with proper spacing
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(16)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Header label (matches Legacy ChooseFilterLabel)
        self.header_label = QLabel("Choose Filter")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        self.header_label.setFont(header_font)

        # Setup responsive grid layout
        self._setup_responsive_grid_layout()

        # Setup filter buttons
        self._setup_filter_buttons()

        # Modern layout with flexible stretches
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.header_label, 0, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(24)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addSpacing(16)
        self.main_layout.addWidget(
            self.show_all_button, 0, Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addStretch(1)

        # Apply container styling
        self._apply_modern_container_styling()

    def _setup_responsive_grid_layout(self) -> None:
        """Setup responsive grid layout that adapts to container size."""
        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.setHorizontalSpacing(16)
        self.grid_layout.setVerticalSpacing(16)

    def _setup_filter_buttons(self) -> None:
        """Setup filter buttons matching Legacy configuration."""
        # Filter button configurations (matching Legacy FILTER_OPTIONS)
        filters = [
            (
                FilterType.STARTING_LETTER,
                "Start Letter",
                "Sequences starting with a specific letter.",
            ),
            (
                FilterType.CONTAINS_LETTERS,
                "Contains Letter",
                "Sequences containing specific letters.",
            ),
            (
                FilterType.SEQUENCE_LENGTH,
                "Length",
                "Sequences by length.",
            ),
            (
                FilterType.DIFFICULTY_LEVEL,
                "Level",
                "Sequences by difficulty level.",
            ),
            (
                FilterType.STARTING_POSITION,
                "Start Position",
                "Sequences by starting position.",
            ),
            (FilterType.AUTHOR, "Author", "Sequences by author."),
            (FilterType.FAVORITES, "Favorites", "Your favorite sequences."),
            (FilterType.MOST_RECENT, "Most Recent", "Recently created sequences."),
            (
                FilterType.GRID_MODE,
                "Grid Mode",
                "Sequences by grid mode (Box or Diamond).",
            ),
        ]

        # Create filter button groups
        self.filter_buttons = {}
        for i, (filter_type, title, description) in enumerate(filters):
            button_group = self._create_filter_button_group(
                filter_type, title, description
            )
            self.filter_buttons[filter_type] = button_group

            row = i // self._grid_columns
            col = i % self._grid_columns
            self.grid_layout.addWidget(button_group, row, col)

        # Create Show All button separately (matching Legacy)
        self.show_all_button = self._create_show_all_button()

    def _create_filter_button_group(
        self, filter_type: FilterType, title: str, description: str
    ) -> QWidget:
        """Create a filter button group matching Legacy FilterButtonGroup."""
        group = QWidget()
        group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        group.setMinimumSize(120, 80)
        group.setMaximumSize(200, 120)

        # Layout
        layout = QVBoxLayout(group)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Main button
        button = QPushButton(title)
        button.setMinimumSize(100, 40)
        button.clicked.connect(lambda: self._on_filter_button_clicked(filter_type))

        # Description label
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setFont(QFont("Segoe UI", 8))

        layout.addWidget(button, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label, 0, Qt.AlignmentFlag.AlignCenter)

        # Apply glass-morphism styling
        group.setStyleSheet(
            """
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin: 4px;
                padding: 8px;
            }
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.15);
            }
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                background: transparent;
                border: none;
            }
        """
        )

        return group

    def _create_show_all_button(self) -> QPushButton:
        """Create the Show All button matching Legacy layout."""
        button = QPushButton("Show All")
        button.setMinimumSize(150, 50)
        button.clicked.connect(
            lambda: self._on_filter_button_clicked(FilterType.ALL_SEQUENCES)
        )

        # Special styling for Show All button
        button.setStyleSheet(
            """
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                color: white;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.4);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.15);
            }
        """
        )

        return button

    def _apply_modern_container_styling(self) -> None:
        """Apply modern container styling."""
        self.setStyleSheet(
            """
            FilterSelectionPanel {
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QLabel {
                color: white;
                background: transparent;
            }
        """
        )

    def _finalize_layout_initialization(self) -> None:
        """Finalize layout initialization after widget is shown."""
        self._layout_initialized = True
        self.update()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize events for responsive grid layout."""
        super().resizeEvent(event)
        if not self._layout_initialized:
            return

        # Adjust grid columns based on width (matching Legacy responsiveness)
        width = self.width()
        if width < 600:
            new_columns = 2
        elif width < 900:
            new_columns = 3
        else:
            new_columns = 4

        if new_columns != self._grid_columns:
            self._grid_columns = new_columns
            self._reorganize_grid()

    def _reorganize_grid(self) -> None:
        """Reorganize the grid layout with new column count."""
        # Remove all items from grid
        items = []
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item:
                items.append(item.widget())

        # Clear grid
        for i in range(self.grid_layout.count()):
            self.grid_layout.takeAt(0)

        # Re-add items with new column count
        for i, widget in enumerate(items):
            if widget:
                row = i // self._grid_columns
                col = i % self._grid_columns
                self.grid_layout.addWidget(widget, row, col)

    def _connect_signals(self) -> None:
        """Connect component signals."""
        pass  # Individual buttons connected in creation methods

    def _on_filter_button_clicked(self, filter_type: FilterType) -> None:
        """Handle filter button click."""
        print(f"🔍 [BROWSE] Filter button clicked: {filter_type.value}")

        if filter_type == FilterType.ALL_SEQUENCES:
            # All sequences - no additional configuration needed
            print("🔍 [BROWSE] Emitting all sequences filter")
            self.filter_selected.emit(filter_type, None)
        else:
            # For now, emit with None - specific filter UIs will be implemented next
            print(f"🔍 [BROWSE] Filter selected: {filter_type.value}")
            self.filter_selected.emit(filter_type, None)
