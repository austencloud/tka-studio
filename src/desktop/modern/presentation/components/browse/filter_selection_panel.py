"""
Filter Selection Panel - Centered & Balanced Design

Properly centered composition with visual balance, consistent groupings,
and constrained width for optimal readability and aesthetic appeal.

Design principles:
- Centered composition for visual balance
- Constrained width (600px max) for focus
- Consistent 3-column button grids
- Natural button widths (no stretching)
- Generous white space and breathing room
- Clear visual hierarchy maintained
"""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from desktop.modern.application.services.browse.browse_service import BrowseService
from desktop.modern.application.services.browse.dictionary_data_manager import (
    DictionaryDataManager,
)
from desktop.modern.domain.models.browse_models import FilterType
from desktop.modern.presentation.styles.mixins import StyleMixin

from .components.categories_section import CategoriesSection
from .components.filter_header import FilterHeader
from .components.quick_access_section import QuickAccessSection


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
        """Setup the centered, balanced layout."""
        # Main container with centering
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Add flexible space on left
        main_layout.addStretch()

        # Centered content container with constrained width
        content_widget = QWidget()
        content_widget.setMaximumWidth(600)  # Constrained for focus
        content_widget.setMinimumWidth(500)  # Minimum for usability

        # Content layout with generous spacing
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(36)

        # Build centered content using components
        self._setup_components(content_layout)

        # Add content to main layout
        main_layout.addWidget(content_widget)

        # Add flexible space on right
        main_layout.addStretch()

    def _setup_components(self, layout: QVBoxLayout) -> None:
        """Setup all the sub-components."""
        # Header
        self.header = FilterHeader("Sequence Library")
        layout.addWidget(self.header)

        # Quick Access Section
        self.quick_access = QuickAccessSection()
        self.quick_access.filter_selected.connect(self._handle_filter_selection)
        layout.addWidget(self.quick_access)

        # Categories Section
        self.categories = CategoriesSection(self.dictionary_manager)
        self.categories.filter_selected.connect(self._handle_filter_selection)
        layout.addWidget(self.categories)

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
