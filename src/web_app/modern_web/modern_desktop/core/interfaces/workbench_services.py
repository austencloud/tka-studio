"""
Workbench Service Interfaces

Interface definitions for workbench-related services following TKA's clean architecture.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, NamedTuple

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


class WorkbenchState(Enum):
    """Workbench operational states."""

    EMPTY = "empty"
    SEQUENCE_LOADED = "sequence_loaded"
    START_POSITION_SET = "start_position_set"
    BOTH_SET = "both_set"
    RESTORING = "restoring"


class StateChangeResult(NamedTuple):
    """Result of a state change operation."""

    changed: bool
    previous_state: WorkbenchState
    new_state: WorkbenchState
    sequence_changed: bool
    start_position_changed: bool

    @classmethod
    def create_no_change(cls, current_state: WorkbenchState):
        """Create a no-change result."""
        return cls(False, current_state, current_state, False, False)

    @classmethod
    def create_sequence_changed(
        cls, prev_state: WorkbenchState, new_state: WorkbenchState
    ):
        """Create a sequence change result."""
        return cls(True, prev_state, new_state, True, False)

    @classmethod
    def create_start_position_changed(
        cls, prev_state: WorkbenchState, new_state: WorkbenchState
    ):
        """Create a start position change result."""
        return cls(True, prev_state, new_state, False, True)

    @classmethod
    def create_both_changed(cls, prev_state: WorkbenchState, new_state: WorkbenchState):
        """Create a both changed result."""
        return cls(True, prev_state, new_state, True, True)


class IWorkbenchStateManager(ABC):
    """Interface for workbench state management operations."""

    @abstractmethod
    def set_sequence(
        self, sequence: SequenceData | None, from_restoration: bool = False
    ) -> StateChangeResult:
        """
        Set current sequence and update workbench state.

        Args:
            sequence: New sequence data (None to clear)
            from_restoration: Whether this is from session restoration

        Returns:
            StateChangeResult with change details
        """

    @abstractmethod
    def set_start_position(
        self, start_position: BeatData | None, from_restoration: bool = False
    ) -> StateChangeResult:
        """
        Set start position and update workbench state.

        Args:
            start_position: New start position data (None to clear)
            from_restoration: Whether this is from session restoration

        Returns:
            StateChangeResult with change details
        """

    @abstractmethod
    def clear_all_state(self) -> StateChangeResult:
        """Clear all workbench state."""

    @abstractmethod
    def get_current_sequence(self) -> SequenceData | None:
        """Get current sequence."""

    @abstractmethod
    def get_start_position(self) -> BeatData | None:
        """Get current start position."""

    @abstractmethod
    def get_workbench_state(self) -> WorkbenchState:
        """Get current workbench state."""

    @abstractmethod
    def has_sequence(self) -> bool:
        """Check if workbench has a sequence."""

    @abstractmethod
    def has_start_position(self) -> bool:
        """Check if workbench has a start position."""

    @abstractmethod
    def is_empty(self) -> bool:
        """Check if workbench is completely empty."""

    @abstractmethod
    def is_restoring(self) -> bool:
        """Check if workbench is in restoration mode."""

    @abstractmethod
    def is_restoration_complete(self) -> bool:
        """Check if restoration has completed."""

    @abstractmethod
    def should_enable_sequence_operations(self) -> bool:
        """Check if sequence operations should be enabled."""

    @abstractmethod
    def should_enable_export_operations(self) -> bool:
        """Check if export operations should be enabled."""

    @abstractmethod
    def should_enable_transform_operations(self) -> bool:
        """Check if transform operations should be enabled."""

    @abstractmethod
    def should_enable_clear_operation(self) -> bool:
        """Check if clear operation should be enabled."""

    @abstractmethod
    def should_prevent_auto_save(self) -> bool:
        """Check if auto-save should be prevented (during restoration)."""

    @abstractmethod
    def get_complete_sequence_with_start_position(self) -> SequenceData | None:
        """Get sequence with start position included if both exist."""

    @abstractmethod
    def begin_restoration(self) -> None:
        """Begin restoration mode."""

    @abstractmethod
    def complete_restoration(self) -> None:
        """Complete restoration mode."""

    @abstractmethod
    def reset_restoration_state(self) -> None:
        """Reset restoration state."""

    @abstractmethod
    def validate_state_consistency(self) -> tuple[bool, list[str]]:
        """
        Validate current state consistency.

        Returns:
            Tuple of (is_valid, list_of_issues)
        """

    @abstractmethod
    def get_state_summary(self) -> dict[str, Any]:
        """Get comprehensive state summary for debugging."""


class IWorkbenchClipboardService(ABC):
    """Interface for workbench clipboard operations."""

    @abstractmethod
    def copy_beat(self, beat_data: BeatData) -> bool:
        """Copy beat to clipboard."""

    @abstractmethod
    def copy_sequence_section(
        self, sequence: SequenceData, start_idx: int, end_idx: int
    ) -> bool:
        """Copy sequence section to clipboard."""

    @abstractmethod
    def paste_beat(self, target_index: int) -> BeatData | None:
        """Paste beat from clipboard."""

    @abstractmethod
    def paste_sequence_section(self, target_index: int) -> list[BeatData] | None:
        """Paste sequence section from clipboard."""

    @abstractmethod
    def has_beat_in_clipboard(self) -> bool:
        """Check if clipboard contains beat data."""

    @abstractmethod
    def has_sequence_section_in_clipboard(self) -> bool:
        """Check if clipboard contains sequence section."""

    @abstractmethod
    def clear_clipboard(self) -> None:
        """Clear clipboard contents."""


class IWorkbenchExportService(ABC):
    """Interface for workbench export operations."""

    @abstractmethod
    def export_sequence_as_json(self, sequence: SequenceData, output_path: str) -> bool:
        """Export sequence as JSON file."""

    @abstractmethod
    def export_sequence_as_image(
        self, sequence: SequenceData, output_path: str
    ) -> bool:
        """Export sequence as image file."""

    @abstractmethod
    def export_beat_as_image(self, beat_data: BeatData, output_path: str) -> bool:
        """Export individual beat as image file."""

    @abstractmethod
    def get_supported_export_formats(self) -> list[str]:
        """Get list of supported export formats."""


class SessionRestorationPhase(Enum):
    """Phases of session restoration."""

    NOT_STARTED = "not_started"
    PREPARING = "preparing"
    RESTORING_SEQUENCE = "restoring_sequence"
    RESTORING_START_POSITION = "restoring_start_position"
    FINALIZING = "finalizing"
    COMPLETED = "completed"
    FAILED = "failed"


class SessionRestorationResult(NamedTuple):
    """Result of a session restoration operation."""

    success: bool
    phase: SessionRestorationPhase
    sequence_restored: bool
    start_position_restored: bool
    errors: list[str]

    @classmethod
    def success_result(
        cls,
        phase: SessionRestorationPhase,
        sequence_restored: bool = False,
        start_position_restored: bool = False,
    ):
        """Create a successful restoration result."""
        return cls(True, phase, sequence_restored, start_position_restored, [])

    @classmethod
    def failure_result(cls, phase: SessionRestorationPhase, errors: list[str]):
        """Create a failed restoration result."""
        return cls(False, phase, False, False, errors)


class IWorkbenchSessionManager(ABC):
    """Interface for workbench session management and restoration."""

    @abstractmethod
    def begin_restoration_from_event(
        self, event_data: dict
    ) -> SessionRestorationResult:
        """
        Begin restoration from session restoration event.

        Args:
            event_data: Event data from session restoration event

        Returns:
            SessionRestorationResult with restoration details
        """

    @abstractmethod
    def execute_restoration(self) -> SessionRestorationResult:
        """
        Execute the restoration with pending session data.

        Returns:
            SessionRestorationResult with restoration details
        """

    @abstractmethod
    def handle_restoration_event(self, event_data: dict) -> SessionRestorationResult:
        """
        Handle complete restoration from event (convenience method).

        Args:
            event_data: Event data from session restoration event

        Returns:
            SessionRestorationResult with restoration details
        """

    @abstractmethod
    def handle_missing_start_position_restoration(self) -> None:
        """
        Handle restoration when no start position data is available.

        This ensures the start position view is properly initialized even when cleared.
        """

    @abstractmethod
    def get_current_phase(self) -> SessionRestorationPhase:
        """
        Get current restoration phase.

        Returns:
            SessionRestorationPhase: Current phase of restoration
        """

    @abstractmethod
    def is_restoration_completed(self) -> bool:
        """
        Check if restoration has completed.

        Returns:
            bool: True if restoration completed, False otherwise
        """

    @abstractmethod
    def is_restoration_in_progress(self) -> bool:
        """
        Check if restoration is currently in progress.

        Returns:
            bool: True if restoration in progress, False otherwise
        """

    @abstractmethod
    def has_pending_restoration_data(self) -> bool:
        """
        Check if there's pending restoration data.

        Returns:
            bool: True if pending data exists, False otherwise
        """

    @abstractmethod
    def get_restoration_errors(self) -> list[str]:
        """
        Get list of restoration errors.

        Returns:
            List[str]: List of error messages from restoration attempts
        """

    @abstractmethod
    def setup_event_subscriptions(self) -> list[str]:
        """
        Setup event subscriptions for session restoration.

        Returns:
            List[str]: List of subscription IDs for cleanup
        """

    @abstractmethod
    def cleanup_event_subscriptions(self, subscription_ids: list[str]) -> None:
        """
        Clean up event subscriptions.

        Args:
            subscription_ids: List of subscription IDs to clean up
        """

    @abstractmethod
    def reset_restoration_state(self) -> None:
        """Reset all restoration state."""

    @abstractmethod
    def get_restoration_status_summary(self) -> dict:
        """
        Get comprehensive restoration status for debugging.

        Returns:
            dict: Status summary with restoration details
        """


class IBeatSelectionService(ABC):
    """Interface for beat selection operations."""

    @abstractmethod
    def select_beat(self, beat_index: int) -> bool:
        """Select a beat by index."""

    @abstractmethod
    def select_multiple_beats(self, beat_indices: list[int]) -> bool:
        """Select multiple beats."""

    @abstractmethod
    def deselect_all(self) -> None:
        """Deselect all beats."""

    @abstractmethod
    def get_selected_beats(self) -> list[int]:
        """Get list of selected beat indices."""

    @abstractmethod
    def get_primary_selection(self) -> int | None:
        """Get primary selected beat index."""

    @abstractmethod
    def is_beat_selected(self, beat_index: int) -> bool:
        """Check if beat is selected."""

    @abstractmethod
    def get_selection_count(self) -> int:
        """Get number of selected beats."""


class IGraphEditorService(ABC):
    """Interface for graph editor operations."""

    @abstractmethod
    def create_graph(self, sequence_data: Any) -> Any:
        """Create a graph from sequence data."""

    @abstractmethod
    def update_graph(self, graph_id: str, updates: Any) -> bool:
        """Update an existing graph."""

    @abstractmethod
    def delete_graph(self, graph_id: str) -> bool:
        """Delete a graph."""

    @abstractmethod
    def get_graph(self, graph_id: str) -> Any | None:
        """Get graph by ID."""

    @abstractmethod
    def list_graphs(self) -> list[Any]:
        """List all available graphs."""


class IFullScreenViewer(ABC):
    """Interface for full screen viewing operations."""

    @abstractmethod
    def show_fullscreen(self, content: Any) -> None:
        """Show content in fullscreen mode."""

    @abstractmethod
    def hide_fullscreen(self) -> None:
        """Hide fullscreen mode."""

    @abstractmethod
    def is_fullscreen(self) -> bool:
        """Check if currently in fullscreen mode."""

    @abstractmethod
    def toggle_fullscreen(self, content: Any = None) -> bool:
        """Toggle fullscreen mode."""


class IBeatDeletionService(ABC):
    """Interface for beat deletion operations."""

    @abstractmethod
    def delete_beat(self, beat_index: int) -> bool:
        """Delete a beat at the specified index."""

    @abstractmethod
    def delete_beats(self, beat_indices: list[int]) -> bool:
        """Delete multiple beats."""

    @abstractmethod
    def delete_beat_range(self, start_index: int, end_index: int) -> bool:
        """Delete a range of beats."""

    @abstractmethod
    def can_delete_beat(self, beat_index: int) -> bool:
        """Check if a beat can be deleted."""


class IDictionaryService(ABC):
    """Interface for dictionary operations."""

    @abstractmethod
    def get_pictograph(self, letter: str) -> Any | None:
        """Get pictograph by letter."""

    @abstractmethod
    def get_all_pictographs(self) -> list[Any]:
        """Get all available pictographs."""

    @abstractmethod
    def search_pictographs(self, query: str) -> list[Any]:
        """Search pictographs by query."""

    @abstractmethod
    def get_pictograph_variations(self, base_letter: str) -> list[Any]:
        """Get variations of a pictograph."""


class ISequenceWorkbenchService(ABC):
    """Interface for sequence workbench operations."""

    @abstractmethod
    def create_sequence(self, name: str) -> Any:
        """Create a new sequence."""

    @abstractmethod
    def load_sequence(self, sequence_id: str) -> Any | None:
        """Load an existing sequence."""

    @abstractmethod
    def save_sequence(self, sequence: Any) -> bool:
        """Save a sequence."""

    @abstractmethod
    def get_current_sequence(self) -> Any | None:
        """Get the currently active sequence."""

    @abstractmethod
    def set_current_sequence(self, sequence: Any) -> None:
        """Set the current active sequence."""


class IClipboardAdapter(ABC):
    """
    Interface for clipboard adapter implementations.

    Provides framework-agnostic clipboard operations that can be implemented
    for different platforms (Qt, web, etc.).
    """

    @abstractmethod
    def set_text(self, text: str) -> bool:
        """
        Set text in the clipboard.

        Args:
            text: Text to set in clipboard

        Returns:
            bool: True if successful, False otherwise
        """

    @abstractmethod
    def get_text(self) -> str:
        """
        Get text from the clipboard.

        Returns:
            str: Text from clipboard, empty string if none or error
        """

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if clipboard is available for operations.

        Returns:
            bool: True if clipboard is available
        """
