"""
Interface definitions for workbench session management services in TKA.

These interfaces define contracts for session restoration, workbench state management,
and session coordination operations within the workbench context.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import NamedTuple, Optional

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


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
    """Interface for workbench session management operations."""

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
            bool: True if restoration is completed, False otherwise
        """

    @abstractmethod
    def is_restoration_in_progress(self) -> bool:
        """
        Check if restoration is currently in progress.

        Returns:
            bool: True if restoration is in progress, False otherwise
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
            List[str]: Copy of restoration errors
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


class ISessionCoordinator(ABC):
    """Interface for coordinating session operations across components."""

    @abstractmethod
    def coordinate_session_save(self, session_data: dict) -> bool:
        """
        Coordinate saving session data across components.

        Args:
            session_data: Session data to save

        Returns:
            bool: True if save succeeded, False otherwise
        """

    @abstractmethod
    def coordinate_session_load(self) -> Optional[dict]:
        """
        Coordinate loading session data from storage.

        Returns:
            Optional[dict]: Loaded session data or None if not available
        """

    @abstractmethod
    def coordinate_session_clear(self) -> bool:
        """
        Coordinate clearing session data.

        Returns:
            bool: True if clear succeeded, False otherwise
        """

    @abstractmethod
    def get_session_metadata(self) -> dict:
        """
        Get metadata about current session.

        Returns:
            dict: Session metadata information
        """


class IWorkbenchStateCoordinator(ABC):
    """Interface for coordinating workbench state across restoration operations."""

    @abstractmethod
    def begin_restoration_mode(self) -> None:
        """Begin restoration mode to prevent auto-save loops."""

    @abstractmethod
    def complete_restoration_mode(self) -> None:
        """Complete restoration mode and resume normal operations."""

    @abstractmethod
    def is_in_restoration_mode(self) -> bool:
        """
        Check if currently in restoration mode.

        Returns:
            bool: True if in restoration mode, False otherwise
        """

    @abstractmethod
    def update_sequence_state(
        self, sequence_data: Optional[SequenceData], from_restoration: bool = False
    ) -> bool:
        """
        Update sequence state during restoration.

        Args:
            sequence_data: New sequence data
            from_restoration: Whether update is from restoration

        Returns:
            bool: True if state changed, False otherwise
        """

    @abstractmethod
    def update_start_position_state(
        self, start_position_data: Optional[BeatData], from_restoration: bool = False
    ) -> bool:
        """
        Update start position state during restoration.

        Args:
            start_position_data: New start position data
            from_restoration: Whether update is from restoration

        Returns:
            bool: True if state changed, False otherwise
        """

    @abstractmethod
    def get_current_workbench_state(self) -> dict:
        """
        Get current workbench state snapshot.

        Returns:
            dict: Current state information
        """
