"""
Workbench Services Interfaces

Defines interfaces for workbench-related services including graph editor,
full screen viewer, and dictionary services.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from domain.models import SequenceData


class IGraphEditorService(ABC):
    """Interface for graph editor services."""

    @abstractmethod
    def open_graph_editor(self) -> None:
        """Open the graph editor."""
        pass

    @abstractmethod
    def close_graph_editor(self) -> None:
        """Close the graph editor."""
        pass

    @abstractmethod
    def get_current_graph(self) -> dict[str, Any]:
        """Get the current graph data."""
        pass


class IFullScreenViewer(ABC):
    """Interface for full screen viewer services."""

    @abstractmethod
    def enter_full_screen(self) -> None:
        """Enter full screen mode."""
        pass

    @abstractmethod
    def exit_full_screen(self) -> None:
        """Exit full screen mode."""
        pass

    @abstractmethod
    def is_full_screen(self) -> bool:
        """Check if currently in full screen mode."""
        pass


class IDictionaryService(ABC):
    """Interface for dictionary services."""

    @abstractmethod
    def add_sequence_to_dictionary(self, sequence_data: dict[str, Any]) -> None:
        """Add a sequence to the dictionary."""
        pass

    @abstractmethod
    def remove_sequence_from_dictionary(self, sequence_id: str) -> None:
        """Remove a sequence from the dictionary."""
        pass

    @abstractmethod
    def search_dictionary(self, query: str) -> list[dict[str, Any]]:
        """Search the dictionary for sequences."""
        pass


class IBeatDeletionService(ABC):
    """Interface for beat deletion services."""

    @abstractmethod
    def delete_beat(self, sequence: SequenceData, beat_index: int) -> SequenceData:
        """Delete a beat from the sequence."""
        pass

    @abstractmethod
    def can_delete_beat(self, sequence: SequenceData, beat_index: int) -> bool:
        """Check if a beat can be deleted."""
        pass

    @abstractmethod
    def get_deletion_confirmation_message(self, beat_index: int) -> str:
        """Get confirmation message for beat deletion."""
        pass


class ISequenceWorkbenchService(ABC):
    """Interface for sequence workbench services."""

    @abstractmethod
    def load_sequence(self, sequence: SequenceData) -> None:
        """Load a sequence into the workbench."""
        pass

    @abstractmethod
    def save_sequence(self) -> SequenceData:
        """Save the current sequence from the workbench."""
        pass

    @abstractmethod
    def get_current_sequence(self) -> SequenceData | None:
        """Get the currently loaded sequence."""
        pass

    @abstractmethod
    def clear_workbench(self) -> None:
        """Clear the workbench."""
        pass

    @abstractmethod
    def is_sequence_modified(self) -> bool:
        """Check if the current sequence has been modified."""
        pass

    @abstractmethod
    def set_beat_selection(self, beat_index: int) -> None:
        """Set the selected beat."""
        pass

    @abstractmethod
    def get_beat_selection(self) -> int | None:
        """Get the currently selected beat index."""
        pass
