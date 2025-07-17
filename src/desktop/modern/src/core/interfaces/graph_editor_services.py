"""
Graph Editor Service Interfaces

Interface definitions for graph editor services following TKA's clean architecture.
These interfaces define contracts for graph editor operations, data flow management,
and state coordination that must work identically across desktop and web platforms.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

from domain.models.beat_data import BeatData
from domain.models.enums import MotionType
from domain.models.sequence_data import SequenceData


class GraphEditorMode(Enum):
    """Graph editor operation modes."""

    EDIT = "edit"
    VIEW = "view"
    ANALYZE = "analyze"


class IGraphEditorDataFlowManager(ABC):
    """Interface for graph editor data flow management operations."""

    @abstractmethod
    def set_context(self, sequence: SequenceData, beat_index: int) -> None:
        """
        Set current sequence and beat context.

        Args:
            sequence: Current sequence data
            beat_index: Index of current beat

        Note:
            Web implementation: Uses state management instead of direct object references
        """
        pass

    @abstractmethod
    def process_turn_change(
        self, beat_data: BeatData, arrow_color: str, new_turns: float
    ) -> BeatData:
        """
        Process turn change and trigger all necessary updates.

        Args:
            beat_data: Beat data to modify
            arrow_color: Color of arrow being modified
            new_turns: New turn value

        Returns:
            Updated beat data

        Note:
            Web implementation: Triggers state updates and re-renders
        """
        pass

    @abstractmethod
    def process_motion_type_change(
        self, beat_data: BeatData, arrow_color: str, new_motion_type: MotionType
    ) -> BeatData:
        """
        Process motion type change and trigger updates.

        Args:
            beat_data: Beat data to modify
            arrow_color: Color of arrow being modified
            new_motion_type: New motion type

        Returns:
            Updated beat data

        Note:
            Web implementation: Updates state and triggers re-renders
        """
        pass

    @abstractmethod
    def process_location_change(
        self, beat_data: BeatData, arrow_color: str, new_location: str
    ) -> BeatData:
        """
        Process location change and trigger updates.

        Args:
            beat_data: Beat data to modify
            arrow_color: Color of arrow being modified
            new_location: New location

        Returns:
            Updated beat data

        Note:
            Web implementation: Updates state and triggers UI updates
        """
        pass

    @abstractmethod
    def validate_change(
        self, beat_data: BeatData, change_type: str, new_value: Any
    ) -> bool:
        """
        Validate a proposed change before applying.

        Args:
            beat_data: Beat data to validate change against
            change_type: Type of change (turn, motion_type, location)
            new_value: New value to validate

        Returns:
            True if valid, False otherwise

        Note:
            Web implementation: Same validation logic across platforms
        """
        pass

    @abstractmethod
    def get_change_history(self) -> List[Dict[str, Any]]:
        """
        Get history of changes made in current session.

        Returns:
            List of change records

        Note:
            Web implementation: Uses browser storage for persistence
        """
        pass

    @abstractmethod
    def undo_last_change(self) -> Optional[BeatData]:
        """
        Undo the last change made.

        Returns:
            Beat data after undo, or None if no changes to undo

        Note:
            Web implementation: Uses state management for undo functionality
        """
        pass

    @abstractmethod
    def redo_last_change(self) -> Optional[BeatData]:
        """
        Redo the last undone change.

        Returns:
            Beat data after redo, or None if no changes to redo

        Note:
            Web implementation: Uses state management for redo functionality
        """
        pass


class IGraphEditorCoordinator(ABC):
    """Interface for graph editor coordination operations."""

    @abstractmethod
    def initialize_editor(self, sequence: SequenceData, beat_index: int) -> None:
        """
        Initialize the graph editor with sequence and beat context.

        Args:
            sequence: Sequence data to edit
            beat_index: Index of beat to edit

        Note:
            Web implementation: Sets up component state and event handlers
        """
        pass

    @abstractmethod
    def set_editor_mode(self, mode: GraphEditorMode) -> None:
        """
        Set the graph editor mode.

        Args:
            mode: Editor mode to set

        Note:
            Web implementation: Updates UI state and available controls
        """
        pass

    @abstractmethod
    def get_editor_mode(self) -> GraphEditorMode:
        """
        Get current editor mode.

        Returns:
            Current editor mode
        """
        pass

    @abstractmethod
    def save_current_state(self) -> bool:
        """
        Save current editor state.

        Returns:
            True if saved successfully, False otherwise

        Note:
            Web implementation: Saves to browser storage or server
        """
        pass

    @abstractmethod
    def load_editor_state(self, state_id: str) -> bool:
        """
        Load a saved editor state.

        Args:
            state_id: ID of state to load

        Returns:
            True if loaded successfully, False otherwise

        Note:
            Web implementation: Loads from browser storage or server
        """
        pass

    @abstractmethod
    def get_available_actions(self) -> List[str]:
        """
        Get available actions for current context.

        Returns:
            List of available action names

        Note:
            Web implementation: Returns actions available in current UI state
        """
        pass

    @abstractmethod
    def execute_action(self, action_name: str, parameters: Dict[str, Any]) -> bool:
        """
        Execute an editor action.

        Args:
            action_name: Name of action to execute
            parameters: Action parameters

        Returns:
            True if executed successfully, False otherwise

        Note:
            Web implementation: Executes action and updates state
        """
        pass

    @abstractmethod
    def get_editor_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about editor usage.

        Returns:
            Dictionary of editor statistics

        Note:
            Web implementation: May include performance metrics
        """
        pass


class IGraphEditorStateManager(ABC):
    """Interface for graph editor state management operations."""

    @abstractmethod
    def get_current_beat_data(self) -> Optional[BeatData]:
        """
        Get current beat data being edited.

        Returns:
            Current beat data or None if none selected

        Note:
            Web implementation: Retrieved from component state
        """
        pass

    @abstractmethod
    def set_current_beat_data(self, beat_data: BeatData) -> None:
        """
        Set current beat data being edited.

        Args:
            beat_data: Beat data to set as current

        Note:
            Web implementation: Updates component state and triggers re-render
        """
        pass

    @abstractmethod
    def get_current_sequence(self) -> Optional[SequenceData]:
        """
        Get current sequence being edited.

        Returns:
            Current sequence data or None if none loaded
        """
        pass

    @abstractmethod
    def set_current_sequence(self, sequence: SequenceData) -> None:
        """
        Set current sequence being edited.

        Args:
            sequence: Sequence data to set as current

        Note:
            Web implementation: Updates state and refreshes editor
        """
        pass

    @abstractmethod
    def get_current_beat_index(self) -> Optional[int]:
        """
        Get index of current beat being edited.

        Returns:
            Current beat index or None if none selected
        """
        pass

    @abstractmethod
    def set_current_beat_index(self, beat_index: int) -> None:
        """
        Set index of current beat being edited.

        Args:
            beat_index: Beat index to set as current

        Note:
            Web implementation: Updates state and refreshes editor
        """
        pass

    @abstractmethod
    def get_editor_state(self) -> Dict[str, Any]:
        """
        Get complete editor state.

        Returns:
            Dictionary containing all editor state

        Note:
            Web implementation: Serializable state for persistence
        """
        pass

    @abstractmethod
    def set_editor_state(self, state: Dict[str, Any]) -> None:
        """
        Set complete editor state.

        Args:
            state: State dictionary to apply

        Note:
            Web implementation: Restores state from serialized data
        """
        pass

    @abstractmethod
    def is_modified(self) -> bool:
        """
        Check if editor state has been modified.

        Returns:
            True if modified, False otherwise
        """
        pass

    @abstractmethod
    def mark_as_saved(self) -> None:
        """
        Mark current state as saved.

        Note:
            Web implementation: Clears modified flag
        """
        pass

    @abstractmethod
    def reset_to_original(self) -> None:
        """
        Reset editor to original state.

        Note:
            Web implementation: Restores from original state backup
        """
        pass


class IGraphEditorHotkeyManager(ABC):
    """Interface for graph editor hotkey management operations."""

    @abstractmethod
    def register_hotkey(
        self, key_sequence: str, action: Callable[[], None], description: str
    ) -> None:
        """
        Register a hotkey with action.

        Args:
            key_sequence: Key sequence (e.g., "Ctrl+S")
            action: Action function to execute
            description: Human-readable description

        Note:
            Web implementation: Uses addEventListener for keydown events
        """
        pass

    @abstractmethod
    def unregister_hotkey(self, key_sequence: str) -> None:
        """
        Unregister a hotkey.

        Args:
            key_sequence: Key sequence to unregister

        Note:
            Web implementation: Removes event listener
        """
        pass

    @abstractmethod
    def get_registered_hotkeys(self) -> Dict[str, str]:
        """
        Get all registered hotkeys.

        Returns:
            Dictionary mapping key sequences to descriptions
        """
        pass

    @abstractmethod
    def is_hotkey_active(self, key_sequence: str) -> bool:
        """
        Check if a hotkey is currently active.

        Args:
            key_sequence: Key sequence to check

        Returns:
            True if active, False otherwise
        """
        pass

    @abstractmethod
    def enable_hotkeys(self) -> None:
        """
        Enable hotkey processing.

        Note:
            Web implementation: Activates event listeners
        """
        pass

    @abstractmethod
    def disable_hotkeys(self) -> None:
        """
        Disable hotkey processing.

        Note:
            Web implementation: Deactivates event listeners
        """
        pass

    @abstractmethod
    def get_hotkey_help(self) -> List[Tuple[str, str]]:
        """
        Get help information for all hotkeys.

        Returns:
            List of tuples (key_sequence, description)
        """
        pass


class IGraphEditorEventManager(ABC):
    """Interface for graph editor event management operations."""

    @abstractmethod
    def register_event_handler(
        self, event_type: str, handler: Callable[[Any], None]
    ) -> None:
        """
        Register an event handler.

        Args:
            event_type: Type of event to handle
            handler: Handler function

        Note:
            Web implementation: Uses custom event system or framework events
        """
        pass

    @abstractmethod
    def unregister_event_handler(
        self, event_type: str, handler: Callable[[Any], None]
    ) -> None:
        """
        Unregister an event handler.

        Args:
            event_type: Type of event
            handler: Handler function to remove

        Note:
            Web implementation: Removes event listener
        """
        pass

    @abstractmethod
    def emit_event(self, event_type: str, data: Any) -> None:
        """
        Emit an event with data.

        Args:
            event_type: Type of event to emit
            data: Event data

        Note:
            Web implementation: Dispatches custom event
        """
        pass

    @abstractmethod
    def get_event_history(self) -> List[Dict[str, Any]]:
        """
        Get history of events.

        Returns:
            List of event records

        Note:
            Web implementation: May use browser storage for persistence
        """
        pass

    @abstractmethod
    def clear_event_history(self) -> None:
        """
        Clear event history.

        Note:
            Web implementation: Clears stored event data
        """
        pass


class IGraphEditorValidationService(ABC):
    """Interface for graph editor validation operations."""

    @abstractmethod
    def validate_beat_data(self, beat_data: BeatData) -> Tuple[bool, List[str]]:
        """
        Validate beat data for consistency.

        Args:
            beat_data: Beat data to validate

        Returns:
            Tuple of (is_valid, error_messages)

        Note:
            Web implementation: Same validation logic across platforms
        """
        pass

    @abstractmethod
    def validate_sequence_data(self, sequence: SequenceData) -> Tuple[bool, List[str]]:
        """
        Validate sequence data for consistency.

        Args:
            sequence: Sequence data to validate

        Returns:
            Tuple of (is_valid, error_messages)

        Note:
            Web implementation: Same validation logic across platforms
        """
        pass

    @abstractmethod
    def validate_change(
        self, current_data: BeatData, proposed_change: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        Validate a proposed change.

        Args:
            current_data: Current beat data
            proposed_change: Proposed change data

        Returns:
            Tuple of (is_valid, error_messages)

        Note:
            Web implementation: Same validation logic across platforms
        """
        pass

    @abstractmethod
    def get_validation_rules(self) -> Dict[str, Any]:
        """
        Get validation rules.

        Returns:
            Dictionary of validation rules

        Note:
            Web implementation: Static rules, can be shared configuration
        """
        pass
