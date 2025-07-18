"""
Modern Browse Tab - Layout Matching Legacy Structure

Rewritten to match the Legacy browse tab layout exactly:
- Horizontal layout with 2:1 ratio (left stack : sequence viewer)
- Left stack contains filter selection and sequence browser
- Navigation via QStackedWidget switching
"""

from pathlib import Path
from typing import Optional

from presentation.tabs.browse.components.filter_selection_panel import (
    FilterSelectionPanel,
)
from presentation.tabs.browse.components.sequence_browser_panel import (
    SequenceBrowserPanel,
)
from presentation.tabs.browse.components.sequence_viewer_panel import (
    SequenceViewerPanel,
)
from presentation.tabs.browse.models import FilterType
from presentation.tabs.browse.services.browse_service import BrowseService
from presentation.tabs.browse.services.browse_state_service import BrowseStateService
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QStackedWidget, QWidget


class ModernBrowseTab(QWidget):
    """
    Modern Browse Tab matching Legacy layout structure exactly.

    Layout:
    - Main horizontal layout (2:1 ratio)
    - Left: internal_left_stack (QStackedWidget)
      - Index 0: Filter selection panel
      - Index 1: Sequence browser panel
    - Right: Sequence viewer panel
    """

    # Signals for communication with main app
    sequence_selected = pyqtSignal(str)  # sequence_id
    open_in_construct = pyqtSignal(str)  # sequence_id

    def __init__(
        self, sequences_dir: Path, settings_file: Path, parent: Optional[QWidget] = None
    ):
        """Initialize the modern browse tab with Legacy-matching layout."""
        super().__init__(parent)

        # Initialize services
        self.browse_service = BrowseService(sequences_dir)
        self.state_service = BrowseStateService(settings_file)

        # Setup Legacy-matching layout
        self._setup_legacy_layout()
        self._connect_signals()

        # Load initial state
        QTimer.singleShot(100, self._load_initial_state)

    def _setup_legacy_layout(self) -> None:
        """Setup layout exactly matching Legacy structure."""
        # Main horizontal layout (2:1 ratio like Legacy)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left side - Internal stack for filter selection and sequence browsing
        self.internal_left_stack = QStackedWidget()

        # Create panels
        self.filter_selection_panel = FilterSelectionPanel(self.browse_service)
        self.sequence_browser_panel = SequenceBrowserPanel(
            self.browse_service, self.state_service
        )

        # Add panels to stack (matching Legacy indexes)
        self.internal_left_stack.addWidget(
            self.filter_selection_panel
        )  # 0 - Filter selection
        self.internal_left_stack.addWidget(
            self.sequence_browser_panel
        )  # 1 - Sequence list

        # Start with filter selection visible (matching Legacy)
        self.internal_left_stack.setCurrentIndex(0)

        # Right side - Sequence viewer
        self.sequence_viewer_panel = SequenceViewerPanel()

        # Add to main layout with 2:1 ratio (matching Legacy exactly)
        main_layout.addWidget(self.internal_left_stack, 2)  # 66.7% width
        main_layout.addWidget(self.sequence_viewer_panel, 1)  # 33.3% width

    def _connect_signals(self) -> None:
        """Connect component signals."""
        # Filter selection signals
        self.filter_selection_panel.filter_selected.connect(self._on_filter_selected)

        # Browser panel signals
        self.sequence_browser_panel.sequence_selected.connect(
            self.sequence_selected.emit
        )
        self.sequence_browser_panel.open_in_construct.connect(
            self.open_in_construct.emit
        )
        self.sequence_browser_panel.back_to_filters.connect(self._show_filter_selection)

    def _load_initial_state(self) -> None:
        """Load initial data and restore state."""
        # Load sequences
        sequences = self.browse_service.load_sequences()
        print(f"📚 Loaded {len(sequences)} sequences in browse tab")

        # Always start with filter selection visible
        self._show_filter_selection()

    def _on_filter_selected(self, filter_type: FilterType, filter_value) -> None:
        """Handle filter selection - switch to sequence browser."""
        print(f"🔍 Filter selected: {filter_type} = {filter_value}")

        # Save filter state
        self.state_service.set_filter(filter_type, filter_value)

        # Apply filter and show results
        filtered_sequences = self.browse_service.apply_filter(filter_type, filter_value)
        self.sequence_browser_panel.show_sequences(filtered_sequences)
        print(f"📋 Filtered to {len(filtered_sequences)} sequences")

        # Switch to sequence browser view (matching Legacy navigation)
        self._show_sequence_browser()

    def _show_filter_selection(self) -> None:
        """Show filter selection panel (index 0)."""
        self.internal_left_stack.setCurrentIndex(0)
        print("🔄 Switched to filter selection view")

    def _show_sequence_browser(self) -> None:
        """Show sequence browser panel (index 1)."""
        self.internal_left_stack.setCurrentIndex(1)
        print("🔄 Switched to sequence browser view")

    def refresh_sequences(self) -> None:
        """Refresh sequence data from disk."""
        self.browse_service.clear_cache()

        # If we're currently showing filtered results, reapply the filter
        filter_type, filter_value = self.state_service.get_current_filter()
        if filter_type:
            filtered_sequences = self.browse_service.apply_filter(
                filter_type, filter_value
            )
            self.sequence_browser_panel.show_sequences(filtered_sequences)
