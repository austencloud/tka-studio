"""
High Priority Service Interfaces

Interface definitions for high-priority services following TKA's clean architecture.
These interfaces define contracts for critical operations that must work identically
across desktop and web platforms for complete coverage.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class SessionState(Enum):
    """Session state enumeration."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    RESTORING = "restoring"
    SAVING = "saving"


class ISessionRestorationCoordinator(ABC):
    """Interface for session restoration coordination operations."""

    @abstractmethod
    def save_session_state(self, session_data: dict[str, Any]) -> bool:
        """
        Save current session state.

        Args:
            session_data: Session data to save

        Returns:
            True if saved successfully, False otherwise

        Note:
            Web implementation: Uses browser storage (localStorage/sessionStorage)
        """

    @abstractmethod
    def restore_session_state(self) -> dict[str, Any] | None:
        """
        Restore session state from storage.

        Returns:
            Restored session data or None if no session found

        Note:
            Web implementation: Retrieves from browser storage
        """

    @abstractmethod
    def clear_session_state(self) -> bool:
        """
        Clear stored session state.

        Returns:
            True if cleared successfully, False otherwise

        Note:
            Web implementation: Clears browser storage
        """


class IDatasetManager(ABC):
    """Interface for dataset management operations."""

    @abstractmethod
    def load_dataset(self, dataset_name: str) -> Any | None:
        """
        Load a dataset.

        Args:
            dataset_name: Name of dataset to load

        Returns:
            Dataset data or None if not found

        Note:
            Web implementation: Loads from server or browser storage
        """

    @abstractmethod
    def save_dataset(self, dataset_name: str, data: Any) -> bool:
        """
        Save a dataset.

        Args:
            dataset_name: Name of dataset to save
            data: Dataset data to save

        Returns:
            True if saved successfully, False otherwise

        Note:
            Web implementation: Saves to server or browser storage
        """

    @abstractmethod
    def delete_dataset(self, dataset_name: str) -> bool:
        """
        Delete a dataset.

        Args:
            dataset_name: Name of dataset to delete

        Returns:
            True if deleted successfully, False otherwise

        Note:
            Web implementation: Deletes from server or browser storage
        """

    @abstractmethod
    def list_datasets(self) -> list[str]:
        """
        list available datasets.

        Returns:
            list of dataset names

        Note:
            Web implementation: lists from server or browser storage
        """


class IDataManager(ABC):
    """Interface for data management operations."""

    @abstractmethod
    def get_data(self, key: str) -> Any | None:
        """
        Get data by key.

        Args:
            key: Data key

        Returns:
            Data value or None if not found

        Note:
            Web implementation: Retrieved from browser storage or server
        """

    @abstractmethod
    def set_data(self, key: str, value: Any) -> bool:
        """
        Set data by key.

        Args:
            key: Data key
            value: Data value

        Returns:
            True if set successfully, False otherwise

        Note:
            Web implementation: Saves to browser storage or server
        """

    @abstractmethod
    def delete_data(self, key: str) -> bool:
        """
        Delete data by key.

        Args:
            key: Data key to delete

        Returns:
            True if deleted successfully, False otherwise

        Note:
            Web implementation: Deletes from browser storage or server
        """

    @abstractmethod
    def has_data(self, key: str) -> bool:
        """
        Check if data exists for key.

        Args:
            key: Data key to check

        Returns:
            True if data exists, False otherwise
        """

    @abstractmethod
    def clear_all_data(self) -> bool:
        """
        Clear all managed data.

        Returns:
            True if cleared successfully, False otherwise

        Note:
            Web implementation: Clears browser storage or server data
        """

    @abstractmethod
    def get_data_keys(self) -> list[str]:
        """
        Get all data keys.

        Returns:
            list of data keys

        Note:
            Web implementation: Retrieved from browser storage or server
        """

    @abstractmethod
    def backup_data(self, backup_name: str) -> bool:
        """
        Create backup of all data.

        Args:
            backup_name: Name for backup

        Returns:
            True if backup created successfully, False otherwise

        Note:
            Web implementation: Creates backup in browser storage
        """


class IOptionDataService(ABC):
    """Interface for option data service operations."""

    @abstractmethod
    def get_option_data(self, option_id: str) -> dict[str, Any] | None:
        """
        Get option data by ID.

        Args:
            option_id: ID of option to get

        Returns:
            Option data or None if not found

        Note:
            Web implementation: Retrieved from browser storage or server
        """

    @abstractmethod
    def save_option_data(self, option_id: str, data: dict[str, Any]) -> bool:
        """
        Save option data.

        Args:
            option_id: ID of option to save
            data: Option data to save

        Returns:
            True if saved successfully, False otherwise

        Note:
            Web implementation: Saves to browser storage or server
        """

    @abstractmethod
    def delete_option_data(self, option_id: str) -> bool:
        """
        Delete option data.

        Args:
            option_id: ID of option to delete

        Returns:
            True if deleted successfully, False otherwise

        Note:
            Web implementation: Deletes from browser storage or server
        """


class IPictographCSVManager(ABC):
    """Interface for pictograph CSV management operations."""

    @abstractmethod
    def load_csv_data(self, csv_path: str) -> list[dict[str, Any]] | None:
        """
        Load CSV data from file.

        Args:
            csv_path: Path to CSV file

        Returns:
            list of CSV row dictionaries or None if failed

        Note:
            Web implementation: Loads from server or file upload
        """

    @abstractmethod
    def save_csv_data(self, csv_path: str, data: list[dict[str, Any]]) -> bool:
        """
        Save CSV data to file.

        Args:
            csv_path: Path to save CSV file
            data: list of CSV row dictionaries

        Returns:
            True if saved successfully, False otherwise

        Note:
            Web implementation: Downloads CSV or saves to server
        """

    @abstractmethod
    def validate_csv_format(self, data: list[dict[str, Any]]) -> tuple[bool, list[str]]:
        """
        Validate CSV data format.

        Args:
            data: CSV data to validate

        Returns:
            tuple of (is_valid, error_messages)

        Note:
            Web implementation: Same validation logic across platforms
        """


class IVisibilityStateManager(ABC):
    """Interface for visibility state management operations."""

    @abstractmethod
    def set_visibility(self, element_id: str, visible: bool) -> None:
        """
        Set visibility state for an element.

        Args:
            element_id: ID of element to set visibility for
            visible: Visibility state

        Note:
            Web implementation: Updates CSS display/visibility properties
        """

    @abstractmethod
    def get_visibility(self, element_id: str) -> bool:
        """
        Get visibility state for an element.

        Args:
            element_id: ID of element to check

        Returns:
            True if visible, False otherwise

        Note:
            Web implementation: Checks CSS display/visibility properties
        """

    @abstractmethod
    def toggle_visibility(self, element_id: str) -> bool:
        """
        Toggle visibility state for an element.

        Args:
            element_id: ID of element to toggle

        Returns:
            New visibility state

        Note:
            Web implementation: Toggles CSS display/visibility properties
        """

    @abstractmethod
    def get_all_visibility_states(self) -> dict[str, bool]:
        """
        Get visibility states for all managed elements.

        Returns:
            dictionary mapping element IDs to visibility states

        Note:
            Web implementation: Retrieved from DOM or state management
        """

    @abstractmethod
    def set_all_visibility_states(self, states: dict[str, bool]) -> None:
        """
        Set visibility states for all managed elements.

        Args:
            states: dictionary mapping element IDs to visibility states

        Note:
            Web implementation: Updates DOM or state management
        """

    @abstractmethod
    def save_visibility_state(self, state_name: str) -> bool:
        """
        Save current visibility state.

        Args:
            state_name: Name for saved state

        Returns:
            True if saved successfully, False otherwise

        Note:
            Web implementation: Saves to browser storage
        """

    @abstractmethod
    def load_visibility_state(self, state_name: str) -> bool:
        """
        Load a saved visibility state.

        Args:
            state_name: Name of state to load

        Returns:
            True if loaded successfully, False otherwise

        Note:
            Web implementation: Loads from browser storage
        """

    @abstractmethod
    def get_saved_states(self) -> list[str]:
        """
        Get list of saved visibility states.

        Returns:
            list of saved state names

        Note:
            Web implementation: Retrieved from browser storage
        """


class ISequenceRepository(ABC):
    """Interface for sequence repository operations."""

    @abstractmethod
    def save_sequence(self, sequence_id: str, sequence_data: Any) -> bool:
        """
        Save sequence data.

        Args:
            sequence_id: ID of sequence to save
            sequence_data: Sequence data to save

        Returns:
            True if saved successfully, False otherwise

        Note:
            Web implementation: Saves to browser storage or server
        """

    @abstractmethod
    def load_sequence(self, sequence_id: str) -> Any | None:
        """
        Load sequence data.

        Args:
            sequence_id: ID of sequence to load

        Returns:
            Sequence data or None if not found

        Note:
            Web implementation: Loads from browser storage or server
        """

    @abstractmethod
    def delete_sequence(self, sequence_id: str) -> bool:
        """
        Delete sequence data.

        Args:
            sequence_id: ID of sequence to delete

        Returns:
            True if deleted successfully, False otherwise

        Note:
            Web implementation: Deletes from browser storage or server
        """

    @abstractmethod
    def list_sequences(self) -> list[str]:
        """
        list available sequences.

        Returns:
            list of sequence IDs

        Note:
            Web implementation: lists from browser storage or server
        """

    @abstractmethod
    def sequence_exists(self, sequence_id: str) -> bool:
        """
        Check if sequence exists.

        Args:
            sequence_id: ID of sequence to check

        Returns:
            True if exists, False otherwise
        """

    @abstractmethod
    def get_sequence_metadata(self, sequence_id: str) -> dict[str, Any] | None:
        """
        Get metadata for a sequence.

        Args:
            sequence_id: ID of sequence to get metadata for

        Returns:
            Metadata dictionary or None if not found

        Note:
            Web implementation: Metadata may be cached in browser storage
        """

    @abstractmethod
    def backup_sequences(self, backup_name: str) -> bool:
        """
        Create backup of all sequences.

        Args:
            backup_name: Name for backup

        Returns:
            True if backup created successfully, False otherwise

        Note:
            Web implementation: Creates backup in browser storage
        """

    @abstractmethod
    def restore_sequences(self, backup_name: str) -> bool:
        """
        Restore sequences from backup.

        Args:
            backup_name: Name of backup to restore

        Returns:
            True if restored successfully, False otherwise

        Note:
            Web implementation: Restores from browser storage backup
        """


class IClipboardAdapter(ABC):
    """Interface for clipboard adapter operations."""

    @abstractmethod
    def copy_to_clipboard(self, data: str) -> bool:
        """
        Copy data to clipboard.

        Args:
            data: Data to copy

        Returns:
            True if copied successfully, False otherwise

        Note:
            Web implementation: Uses Clipboard API or fallback methods
        """

    @abstractmethod
    def paste_from_clipboard(self) -> str | None:
        """
        Paste data from clipboard.

        Returns:
            Clipboard data or None if empty/failed

        Note:
            Web implementation: Uses Clipboard API or fallback methods
        """

    @abstractmethod
    def clear_clipboard(self) -> bool:
        """
        Clear clipboard contents.

        Returns:
            True if cleared successfully, False otherwise

        Note:
            Web implementation: Uses Clipboard API or fallback methods
        """
