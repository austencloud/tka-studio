"""
Modern Browse Tab - Layout Matching Legacy Structure

Rewritten to match the Legacy browse tab layout exactly:
- Horizontal layout with 2:1 ratio (left stack : sequence viewer)
- Left stack contains filter selection and sequence browser
- Navigation via QStackedWidget switching
"""

from pathlib import Path
from typing import List, Optional

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
from presentation.tabs.browse.services.modern_dictionary_data_manager import (
    ModernDictionaryDataManager,
)
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
        # Find the TKA root directory and construct the data path
        tka_root = Path(__file__).resolve()
        while tka_root.parent != tka_root and tka_root.name != "TKA":
            tka_root = tka_root.parent
        data_dir = tka_root / "data"

        self.dictionary_manager = ModernDictionaryDataManager(data_dir)
        self.browse_service = BrowseService(sequences_dir)
        self.state_service = BrowseStateService(settings_file)

        # Connect data manager signals
        self.dictionary_manager.data_loaded.connect(self._on_data_loaded)
        self.dictionary_manager.loading_progress.connect(self._on_loading_progress)

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
        self.filter_selection_panel = FilterSelectionPanel(
            self.browse_service, self.dictionary_manager
        )
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
        # Load sequences from dictionary
        self.dictionary_manager.load_all_sequences()

        # Always start with filter selection visible
        self._show_filter_selection()

    def _on_data_loaded(self, count: int) -> None:
        """Handle data loading completion."""
        print(f"📚 Loaded {count} sequences from dictionary")

        # Check for loading errors
        errors = self.dictionary_manager.get_loading_errors()
        if errors:
            print(f"⚠️  {len(errors)} loading errors occurred")
            for error in errors[:5]:  # Show first 5 errors
                print(f"   - {error}")

    def _on_loading_progress(self, message: str, current: int, total: int) -> None:
        """Handle loading progress updates."""
        if (
            current % 10 == 0 or current == total
        ):  # Update every 10th item or at completion
            print(f"🔄 {message} ({current}/{total})")

    def _on_filter_selected(self, filter_type: FilterType, filter_value) -> None:
        """Handle filter selection - switch to sequence browser."""
        print(f"🔍 Filter selected: {filter_type} = {filter_value}")

        # Save filter state
        self.state_service.set_filter(filter_type, filter_value)

        # Apply filter using dictionary manager
        filtered_sequences = self._apply_dictionary_filter(filter_type, filter_value)
        self.sequence_browser_panel.show_sequences(filtered_sequences)
        print(f"📋 Filtered to {len(filtered_sequences)} sequences")

        # Switch to sequence browser view (matching Legacy navigation)
        self._show_sequence_browser()

    def _apply_dictionary_filter(self, filter_type: FilterType, filter_value) -> List:
        """Apply filter using the dictionary data manager."""
        records = []

        if filter_type == FilterType.STARTING_LETTER:
            if isinstance(filter_value, str):
                # Handle letter ranges like "A-D"
                if "-" in filter_value and len(filter_value) == 3:
                    start_letter, end_letter = filter_value.split("-")
                    letters = [
                        chr(i) for i in range(ord(start_letter), ord(end_letter) + 1)
                    ]
                    records = self.dictionary_manager.get_records_by_starting_letters(
                        letters
                    )
                elif filter_value == "All Letters":
                    records = self.dictionary_manager.get_all_records()
                else:
                    # Single letter
                    records = self.dictionary_manager.get_records_by_starting_letter(
                        filter_value
                    )
            elif isinstance(filter_value, list):
                records = self.dictionary_manager.get_records_by_starting_letters(
                    filter_value
                )

        elif filter_type == FilterType.LENGTH:
            if isinstance(filter_value, int):
                records = self.dictionary_manager.get_records_by_length(filter_value)
            elif filter_value == "All":
                records = self.dictionary_manager.get_all_records()

        elif filter_type == FilterType.DIFFICULTY:
            if filter_value == "All":
                records = self.dictionary_manager.get_all_records()
            else:
                records = self.dictionary_manager.get_records_by_difficulty(
                    filter_value
                )

        elif filter_type == FilterType.AUTHOR:
            if filter_value == "All Authors":
                records = self.dictionary_manager.get_all_records()
            else:
                records = self.dictionary_manager.get_records_by_author(filter_value)

        elif filter_type == FilterType.GRID_MODE:
            if filter_value == "All":
                records = self.dictionary_manager.get_all_records()
            else:
                records = self.dictionary_manager.get_records_by_grid_mode(filter_value)

        elif filter_type == FilterType.FAVORITES:
            records = self.dictionary_manager.get_favorite_records()

        elif filter_type == FilterType.RECENT:
            records = self.dictionary_manager.get_recent_records()

        else:
            records = self.dictionary_manager.get_all_records()

        # Convert SequenceRecord to SequenceData format for compatibility
        return self._convert_records_to_sequence_data(records)

    def _convert_records_to_sequence_data(self, records) -> List:
        """Convert SequenceRecord objects to SequenceData format."""
        from domain.models.sequence_data import SequenceData

        sequence_data_list = []
        for record in records:
            # Create SequenceData object
            sequence_data = SequenceData(
                word=record.word,
                thumbnails=record.thumbnails,
                author=record.author,
                level=record.level,
                sequence_length=record.sequence_length,
                date_added=record.date_added,
                grid_mode=record.grid_mode,
                prop_type=record.prop_type,
                is_favorite=record.is_favorite,
                is_circular=record.is_circular,
                starting_position=record.starting_position,
                difficulty_level=record.difficulty_level,
                tags=record.tags,
            )
            sequence_data_list.append(sequence_data)

        return sequence_data_list

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
        # Clear and reload dictionary data
        self.dictionary_manager.refresh_data()

        # If we're currently showing filtered results, reapply the filter
        filter_type, filter_value = self.state_service.get_current_filter()
        if filter_type:
            filtered_sequences = self._apply_dictionary_filter(
                filter_type, filter_value
            )
            self.sequence_browser_panel.show_sequences(filtered_sequences)
