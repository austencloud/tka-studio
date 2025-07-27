"""
Browse View Model - MVVM Pattern for Browse Tab

Handles view-specific state and logic, decoupled from business logic.
Provides data binding between the view and model layers.
"""

from typing import List, Optional

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.tabs.browse.models import FilterType


class BrowseViewModel(QObject):
    """
    ViewModel for the Browse tab implementing MVVM pattern.
    
    Manages view-specific state and provides signals for UI updates.
    Decouples view state from business logic.
    """

    # Signals for view updates
    sequences_changed = pyqtSignal(list)  # List[SequenceData]
    loading_changed = pyqtSignal(bool)
    filter_changed = pyqtSignal(object, object)  # filter_type, filter_value
    selection_changed = pyqtSignal(str)  # sequence_id
    error_occurred = pyqtSignal(str)  # error_message
    progress_updated = pyqtSignal(int, int, str)  # current, total, message

    def __init__(self):
        super().__init__()
        
        # View state
        self._current_sequences: List[SequenceData] = []
        self._selected_sequence_id: Optional[str] = None
        self._current_filter_type: Optional[FilterType] = None
        self._current_filter_value = None
        self._is_loading = False
        self._error_message: Optional[str] = None

    @property
    def current_sequences(self) -> List[SequenceData]:
        """Get current filtered sequences."""
        return self._current_sequences.copy()

    @property
    def selected_sequence_id(self) -> Optional[str]:
        """Get currently selected sequence ID."""
        return self._selected_sequence_id

    @property
    def current_filter_type(self) -> Optional[FilterType]:
        """Get current filter type."""
        return self._current_filter_type

    @property
    def current_filter_value(self):
        """Get current filter value."""
        return self._current_filter_value

    @property
    def is_loading(self) -> bool:
        """Check if currently loading."""
        return self._is_loading

    @property
    def sequence_count(self) -> int:
        """Get number of current sequences."""
        return len(self._current_sequences)

    def set_sequences(self, sequences: List[SequenceData]) -> None:
        """Update the sequence list and notify views."""
        self._current_sequences = sequences.copy()
        self.sequences_changed.emit(sequences)

    def add_sequences(self, sequences: List[SequenceData]) -> None:
        """Add sequences to current list (for progressive loading)."""
        self._current_sequences.extend(sequences)
        self.sequences_changed.emit(self._current_sequences)

    def clear_sequences(self) -> None:
        """Clear all sequences."""
        self._current_sequences.clear()
        self.sequences_changed.emit([])

    def set_loading(self, loading: bool) -> None:
        """Update loading state and notify views."""
        if self._is_loading != loading:
            self._is_loading = loading
            self.loading_changed.emit(loading)

    def set_filter(self, filter_type: FilterType, filter_value) -> None:
        """Update current filter and notify views."""
        self._current_filter_type = filter_type
        self._current_filter_value = filter_value
        self.filter_changed.emit(filter_type, filter_value)

    def set_selected_sequence(self, sequence_id: Optional[str]) -> None:
        """Update selected sequence and notify views."""
        if self._selected_sequence_id != sequence_id:
            self._selected_sequence_id = sequence_id
            self.selection_changed.emit(sequence_id or "")

    def set_error(self, error_message: str) -> None:
        """Set error state and notify views."""
        self._error_message = error_message
        self.error_occurred.emit(error_message)

    def clear_error(self) -> None:
        """Clear error state."""
        self._error_message = None

    def update_progress(self, current: int, total: int, message: str = "") -> None:
        """Update loading progress and notify views."""
        self.progress_updated.emit(current, total, message)

    def get_sequence_by_id(self, sequence_id: str) -> Optional[SequenceData]:
        """Get sequence by ID from current list."""
        for sequence in self._current_sequences:
            if sequence.id == sequence_id:
                return sequence
        return None

    def get_filter_description(self) -> str:
        """Get human-readable description of current filter."""
        if self._current_filter_type is None:
            return "All sequences"
        
        filter_type = self._current_filter_type
        filter_value = self._current_filter_value
        
        if filter_type == FilterType.STARTING_LETTER:
            return f"Sequences starting with {filter_value}"
        elif filter_type == FilterType.CONTAINS_LETTERS:
            return f"Sequences containing {filter_value}"
        elif filter_type == FilterType.LENGTH:
            return f"Sequences of length {filter_value}"
        elif filter_type == FilterType.DIFFICULTY:
            return f"Level {filter_value} sequences"
        elif filter_type == FilterType.STARTING_POSITION:
            return f"Sequences starting in {filter_value}"
        elif filter_type == FilterType.AUTHOR:
            return f"Sequences by {filter_value}"
        elif filter_type == FilterType.FAVORITES:
            return "Favorite sequences"
        elif filter_type == FilterType.RECENT:
            return "Recently added sequences"
        else:
            return f"Filtered sequences ({filter_type.value})"

    def reset(self) -> None:
        """Reset all view state to defaults."""
        self.clear_sequences()
        self.set_loading(False)
        self.set_selected_sequence(None)
        self._current_filter_type = None
        self._current_filter_value = None
        self.clear_error()
