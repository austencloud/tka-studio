"""
Main Filter Selection Panel Component

Orchestrates all sub-components into a cohesive filter interface.
"""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from application.services.browse.dictionary_data_manager import DictionaryDataManager
from desktop.modern.application.services.browse.browse_service import BrowseService
from desktop.modern.domain.models.browse_models import FilterType
from desktop.modern.presentation.styles.mixins import StyleMixin

from .accordion_filter_panel import AccordionFilterPanel
from .filter_header import FilterHeader
from .quick_access_section import QuickAccessSection


class FilterSelectionPanel(QWidget, StyleMixin):
    """
    Centered, balanced filter selection interface.

    Features proper visual composition with:
    - Centered layout with constrained width
    - Consistent 3-column button grids
    - Natural button sizing (no stretching)
    - Balanced visual hierarchy
    - Generous white space for breathing room
    """

    filter_selected = pyqtSignal(FilterType, object)

    def __init__(
        self,
        browse_service: BrowseService,
        dictionary_manager: DictionaryDataManager,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.browse_service = browse_service
        self.dictionary_manager = dictionary_manager

        # Active state tracking
        self.active_filter_type = None
        self.active_filter_value = None

        # Component references
        self.header = None
        self.quick_access = None
        self.categories = None

        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self) -> None:
        """Setup the full-width layout that expands to fill parent."""
        # Main layout that fills the entire parent container
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)  # Reduced margins
        main_layout.setSpacing(8)  # Much tighter spacing between sections

        # Build components directly in main layout (no centering widget)
        self._setup_components(main_layout)

    def _setup_components(self, layout: QVBoxLayout) -> None:
        """Setup all the sub-components with proper space allocation."""
        # Header section (1/7 of height) - Fixed allocation with more breathing room
        header_widget = QWidget()
        header_widget.setMaximumHeight(
            120
        )  # Increased from 100px for less cramped feel
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)

        # Header + Quick Access on same line
        header_row_layout = QHBoxLayout()

        # Header on left
        self.header = FilterHeader("Sequence Library")
        header_row_layout.addWidget(self.header)

        # Stretch to push Quick Access to right
        header_row_layout.addStretch()

        # Quick Access buttons on right (without title)
        self.quick_access = QuickAccessSection()
        self.quick_access.filter_selected.connect(self._handle_filter_selection)
        header_row_layout.addWidget(self.quick_access)

        header_layout.addLayout(header_row_layout)
        header_layout.addStretch()  # Fill remaining header space

        layout.addWidget(header_widget)

        # Categories Section (6/7 of height) - Expandable content area
        self.categories = AccordionFilterPanel(self.dictionary_manager)
        self.categories.filter_selected.connect(self._handle_filter_selection)
        layout.addWidget(self.categories, 6)  # Stretch factor of 6 (vs 1 for header)

    def _handle_filter_selection(self, filter_type: FilterType, filter_value) -> None:
        """Handle filter selection from any component."""
        print(f"🔍 [FILTER] Selected: {filter_type.value} = {filter_value}")

        # Update active state
        self.active_filter_type = filter_type
        self.active_filter_value = filter_value

        # Update all component states
        self._update_active_states()

        # Emit signal
        self.filter_selected.emit(filter_type, filter_value)

    def _update_active_states(self) -> None:
        """Update visual states across all components."""
        if self.quick_access:
            self.quick_access.set_active_filter(
                self.active_filter_type, self.active_filter_value
            )
        if self.categories:
            self.categories.set_active_filter(
                self.active_filter_type, self.active_filter_value
            )

    def set_active_filter(
        self, filter_type: FilterType | None, filter_value=None
    ) -> None:
        """Set active filter from external source."""
        self.active_filter_type = filter_type
        self.active_filter_value = filter_value
        self._update_active_states()

    def _apply_styling(self) -> None:
        """Apply clean, centered background styling."""
        self.setStyleSheet("""
            FilterSelectionPanel {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 20px;
            }
        """)
