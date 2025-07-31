"""
Beat Selection Manager - Qt Presentation Layer

Handles Qt-specific events and visual updates for beat selection.
Delegates all business logic to BeatSelectionService.
"""

from typing import Optional

from PyQt6.QtCore import QObject, Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget

from shared.application.services.workbench.beat_selection_service import (
    BeatSelectionService,
    SelectionChangeResult,
    SelectionType,
)

from .beat_view import BeatView


class BeatSelector(QObject):
    """
    Qt presentation manager for beat selection.

    Handles Qt events and visual updates while delegating business logic
    to BeatSelectionService.
    """

    # Qt Signals
    selection_changed = pyqtSignal(object)  # Optional[int] - beat index or None
    selection_cleared = pyqtSignal()
    multiple_selection_changed = pyqtSignal(list)  # List[int] - beat indices

    def __init__(self, selection_service: BeatSelectionService, parent_widget: QWidget):
        super().__init__(parent_widget)

        self._selection_service = selection_service
        self._parent_widget = parent_widget
        self._beat_views: list[BeatView] = []
        self._start_position_view = None

        # Configure parent widget for keyboard navigation
        self._parent_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    # Configuration Methods
    def register_beat_views(self, beat_views: list[BeatView]):
        """Register beat views and update service."""
        self._beat_views = beat_views
        self._selection_service.set_beat_count(len(beat_views))

        # Connect signals from beat views
        for i, beat_view in enumerate(beat_views):
            beat_view.beat_clicked.connect(lambda idx=i: self.select_beat(idx))

    def register_start_position_view(self, start_position_view):
        """Register start position view."""
        self._start_position_view = start_position_view

        # Connect start position click signal
        if hasattr(start_position_view, "start_pos_beat_clicked"):
            start_position_view.start_pos_beat_clicked.connect(
                lambda: self.select_start_position()
            )

    def set_multi_selection_enabled(self, enabled: bool):
        """Enable or disable multi-selection mode."""
        result = self._selection_service.set_multi_selection_enabled(enabled)
        self._handle_selection_change(result)

    def set_keyboard_navigation_enabled(self, enabled: bool):
        """Enable or disable keyboard navigation."""
        self._selection_service.set_keyboard_navigation_enabled(enabled)

    # Selection Methods
    def select_beat(self, beat_index: int):
        """Select a specific beat."""
        result = self._selection_service.select_beat(beat_index)
        self._handle_selection_change(result)

    def select_start_position(self):
        """Select the start position."""
        result = self._selection_service.select_start_position()
        self._handle_selection_change(result)

    def add_to_selection(self, beat_index: int):
        """Add a beat to the current selection (multi-selection mode)."""
        result = self._selection_service.add_to_selection(beat_index)
        self._handle_selection_change(result)

    def remove_from_selection(self, beat_index: int):
        """Remove a beat from the current selection."""
        result = self._selection_service.remove_from_selection(beat_index)
        self._handle_selection_change(result)

    def clear_selection(self):
        """Clear all selections."""
        result = self._selection_service.clear_selection()
        self._handle_selection_change(result)
        if result.changed:
            self.selection_cleared.emit()

    # Keyboard Navigation
    def select_next_beat(self):
        """Select the next beat (keyboard navigation)."""
        result = self._selection_service.select_next_beat()
        self._handle_selection_change(result)

    def select_previous_beat(self):
        """Select the previous beat (keyboard navigation)."""
        result = self._selection_service.select_previous_beat()
        self._handle_selection_change(result)

    def focus_selected_beat(self):
        """Set focus to the currently selected beat."""
        selected_index = self._selection_service.get_selected_index()
        if selected_index is not None and selected_index < len(self._beat_views):
            self._beat_views[selected_index].setFocus()

    # Query Methods
    def get_selected_index(self) -> Optional[int]:
        """Get the currently selected beat index."""
        return self._selection_service.get_selected_index()

    def get_selected_indices(self) -> list[int]:
        """Get all selected beat indices."""
        return self._selection_service.get_selected_indices()

    def is_beat_selected(self, beat_index: int) -> bool:
        """Check if a specific beat is selected."""
        return self._selection_service.is_beat_selected(beat_index)

    def is_start_position_selected(self) -> bool:
        """Check if the start position is selected."""
        return self._selection_service.is_start_position_selected()

    # Visual Update Methods
    def _handle_selection_change(self, result: SelectionChangeResult):
        """Handle selection change result and update visuals."""
        if not result.changed:
            return

        # Update visual state based on the change
        self._update_visual_selection(result)

        # Emit appropriate signals
        if result.selection_type == SelectionType.BEAT:
            self.selection_changed.emit(result.selected_index)
            if len(result.current_indices) > 1:
                self.multiple_selection_changed.emit(result.current_indices)
        elif result.selection_type == SelectionType.START_POSITION:
            self.selection_changed.emit(self._selection_service.START_POSITION_INDEX)

    def _update_visual_selection(self, result: SelectionChangeResult):
        """Update Qt visual state based on selection change."""
        # Clear previous visual selections from beats
        for idx in result.previous_indices:
            if idx < len(self._beat_views):
                self._beat_views[idx].set_selected(False)

        # Clear start position if it was previously selected
        if (
            self._start_position_view
            and result.selection_type != SelectionType.START_POSITION
        ):
            self._start_position_view.set_selected(False)

        # Set new visual selections
        if result.selection_type == SelectionType.BEAT:
            for idx in result.current_indices:
                if idx < len(self._beat_views):
                    self._beat_views[idx].set_selected(True)
        elif result.selection_type == SelectionType.START_POSITION:
            if self._start_position_view:
                self._start_position_view.set_selected(True)

    def _clear_all_visual_selections(self):
        """Clear visual selection from all components."""
        # Clear beat views
        for beat_view in self._beat_views:
            beat_view.set_selected(False)

        # Clear start position view
        if self._start_position_view:
            self._start_position_view.set_selected(False)
