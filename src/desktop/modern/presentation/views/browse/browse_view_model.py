"""
Browse View Model - MVVM Pattern for Browse Tab

Handles view-specific state and logic, decoupled from business logic.
Provides data binding between the view and model layers.
"""

from __future__ import annotations

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.views.browse.models import FilterType


class BrowseViewModel(QObject):
    """
    ViewModel for the Browse tab implementing MVVM pattern.

    Manages view-specific state and provides signals for UI updates.
    Decouples view state from business logic.
    """

    # Signals for view updates
    sequences_changed = pyqtSignal(list)  # list[SequenceData]
    loading_changed = pyqtSignal(bool)
    filter_changed = pyqtSignal(object, object)  # filter_type, filter_value
    selection_changed = pyqtSignal(str)  # sequence_id
    error_occurred = pyqtSignal(str)  # error_message
    progress_updated = pyqtSignal(int, int, str)  # current, total, message

    def __init__(self):
        super().__init__()

        # View state
        self._current_sequences: list[SequenceData] = []
        self._selected_sequence_id: str | None = None
        self._current_filter_type: FilterType | None = None
        self._current_filter_value = None
        self._is_loading = False
        self._error_message: str | None = None

    @property
    def current_sequences(self) -> list[SequenceData]:
        """Get current filtered sequences."""
        return self._current_sequences.copy()

    @property
    def selected_sequence_id(self) -> str | None:
        """Get currently selected sequence ID."""
        return self._selected_sequence_id

    @property
    def current_filter_type(self) -> FilterType | None:
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

    def set_sequences(self, sequences: list[SequenceData]) -> None:
        """Update the sequence list and notify views."""
        self._current_sequences = sequences.copy()
        self.sequences_changed.emit(sequences)

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

    def set_selected_sequence(self, sequence_id: str | None) -> None:
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

    def get_sequence_by_id(self, sequence_id: str) -> SequenceData | None:
        """Get sequence by ID from current list."""
        for sequence in self._current_sequences:
            if sequence.id == sequence_id:
                return sequence
        return None

    def reset(self) -> None:
        """Reset all view state to defaults."""
        self.clear_sequences()
        self.set_loading(False)
        self.set_selected_sequence(None)
        self._current_filter_type = None
        self._current_filter_value = None
        self.clear_error()
