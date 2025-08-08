"""
Session State Service Interfaces

Defines interfaces for session state management in TKA applications.
Provides auto-save/restore functionality for user workflow continuity.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid


@dataclass
class SessionState:
    """
    Complete session state representation for TKA application.

    Note:
        Web implementation: Should be serializable to JSON for localStorage/IndexedDB.
        All fields must be compatible with web storage and migration.
    """

    # Current sequence data
    current_sequence_id: str | None = None
    current_sequence_data: dict[str, Any] | None = None

    # Workbench state
    selected_beat_index: int | None = None
    selected_beat_data: dict[str, Any] | None = None
    start_position_data: dict[str, Any] | None = None

    # Graph editor state
    graph_editor_visible: bool = False
    graph_editor_selected_beat_index: int | None = None
    graph_editor_selected_arrow: str | None = None
    graph_editor_height: int = 300

    # Active tab and workbench configuration
    active_tab: str = "sequence_builder"
    beat_layout: dict[str, Any] = field(default_factory=dict)

    # Component visibility states
    component_visibility: dict[str, bool] = field(default_factory=dict)

    # Last interaction timestamp for staleness detection
    last_interaction: datetime = field(default_factory=datetime.now)

    # Session metadata
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    tka_version: str = "modern"


@dataclass
class SessionRestoreResult:
    """
    Result of session restoration attempt.

    Note:
        Web implementation: Used for async restoration and error reporting in web adapters.
    """

    success: bool
    session_restored: bool = False
    session_data: SessionState | None = None
    error_message: str | None = None
    warnings: list = field(default_factory=list)


class ISessionStateTracker(ABC):
    """
    Interface for session state management in TKA applications.

    Provides auto-save/restore, session migration, and cross-platform session export/import.
    """

    @abstractmethod
    def save_session_state(self) -> bool:
        """
        Save current session state to persistent storage.

        Returns:
            bool: True if save was successful, False otherwise

        Note:
            Web implementation: Persists to localStorage/IndexedDB, may be async.
        """

    @abstractmethod
    def load_session_state(self) -> SessionRestoreResult:
        """
        Load session state from persistent storage.

        Returns:
            SessionRestoreResult: Result of restoration attempt

        Note:
            Web implementation: Loads from localStorage/IndexedDB, may be async.
        """

    @abstractmethod
    def update_current_sequence(self, sequence_data: Any, sequence_id: str) -> None:
        """
        Update current sequence in session state.

        Args:
            sequence_data: The sequence data to store
            sequence_id: Unique identifier for the sequence

        Note:
            Web implementation: Triggers auto-save and may debounce updates for performance.
        """

    @abstractmethod
    def update_workbench_state(
        self,
        beat_index: int | None,
        beat_data: Any | None,
        start_position: Any | None,
    ) -> None:
        """
        Update workbench selection state.

        Args:
            beat_index: Currently selected beat index
            beat_data: Currently selected beat data
            start_position: Current start position data

        Note:
            Web implementation: Updates state and triggers UI refresh if needed.
        """

    @abstractmethod
    def update_graph_editor_state(
        self,
        visible: bool,
        beat_index: int | None,
        selected_arrow: str | None,
        height: int | None = None,
    ) -> None:
        """
        Update graph editor state.

        Args:
            visible: Whether graph editor is visible
            beat_index: Selected beat index in graph editor
            selected_arrow: Selected arrow identifier
            height: Graph editor height (optional)

        Note:
            Web implementation: Updates state and may trigger re-render.
        """

    @abstractmethod
    def update_ui_state(
        self,
        active_tab: str,
        beat_layout: dict[str, Any] | None = None,
        component_visibility: dict[str, bool] | None = None,
    ) -> None:
        """
        Update UI state information.

        Args:
            active_tab: Currently active tab
            beat_layout: Beat layout configuration
            component_visibility: Component visibility states

        Note:
            Web implementation: Updates state and may persist to localStorage.
        """

    @abstractmethod
    def should_restore_session(self) -> bool:
        """
        Determine if session should be restored (not too stale).

        Returns:
            bool: True if session should be restored, False if too stale

        Note:
            Web implementation: May use timestamp and staleness policy for browser sessions.
        """

    @abstractmethod
    def mark_interaction(self) -> None:
        """
        Mark user interaction to trigger debounced auto-save.
        This method should be called after any meaningful user interaction.

        Note:
            Web implementation: Used to debounce auto-save and update last interaction timestamp.
        """

    @abstractmethod
    def clear_session(self) -> bool:
        """
        Clear current session state and remove session file.

        Returns:
            bool: True if clear was successful, False otherwise

        Note:
            Web implementation: Removes session from localStorage/IndexedDB.
        """

    @abstractmethod
    def get_current_session_state(self) -> SessionState | None:
        """
        Get current session state without loading from file.

        Returns:
            Optional[SessionState]: Current session state or None

        Note:
            Web implementation: Returns in-memory state, not from storage.
        """

    @abstractmethod
    def is_auto_save_enabled(self) -> bool:
        """
        Check if auto-save is currently enabled.

        Returns:
            bool: True if auto-save is enabled, False otherwise

        Note:
            Web implementation: May be user-configurable in browser settings.
        """

    @abstractmethod
    def set_auto_save_enabled(self, enabled: bool) -> None:
        """
        Enable or disable auto-save functionality.

        Args:
            enabled: Whether to enable auto-save

        Note:
            Web implementation: May update a flag in localStorage or user profile.
        """

    @abstractmethod
    def export_session_state(self) -> str:
        """
        Export current session state as a JSON string for backup or sync.

        Returns:
            str: JSON-serialized session state

        Note:
            Web implementation: Used for download/export or cloud sync.
        """

    @abstractmethod
    def import_session_state(self, session_json: str) -> bool:
        """
        Import session state from a JSON string.

        Args:
            session_json: JSON-serialized session state

        Returns:
            bool: True if import was successful, False otherwise

        Note:
            Web implementation: Used for upload/import or cloud sync.
        """

    @abstractmethod
    def migrate_session_state(self, from_version: str, to_version: str) -> bool:
        """
        Migrate session state from one version to another for compatibility.

        Args:
            from_version: Source version string
            to_version: Target version string

        Returns:
            bool: True if migration was successful, False otherwise

        Note:
            Web implementation: Used for forward/backward compatibility in browser storage.
        """


# Alias for backward compatibility
ISessionStateService = ISessionStateTracker
