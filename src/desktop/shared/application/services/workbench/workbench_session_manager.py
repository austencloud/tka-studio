"""
Workbench Session Manager - Framework-Agnostic Business Logic

Manages workbench-specific session restoration logic without Qt dependencies.
Coordinates with SessionRestorationCoordinator and handles workbench restoration state.

Following established patterns:
- Framework-agnostic (no Qt dependencies)
- Single responsibility (session management only)
- Event-driven coordination
- Delegates to existing session services
"""

import logging

from desktop.modern.core.interfaces.workbench_services import (
    IWorkbenchSessionManager,
    SessionRestorationPhase,
    SessionRestorationResult,
)
from desktop.modern.domain.models.beat_data import BeatData

logger = logging.getLogger(__name__)


class WorkbenchSessionManager(IWorkbenchSessionManager):
    """
    Framework-agnostic session management for workbench.

    Responsibilities:
    - Handle workbench-specific session restoration
    - Coordinate with SessionRestorationCoordinator
    - Manage restoration timing and phases
    - Prevent auto-save loops during restoration
    - Extract and validate session data for workbench
    """

    def __init__(
        self,
        workbench_state_manager=None,
        session_restoration_coordinator=None,
        event_bus=None,
    ):
        """
        Initialize workbench session manager.

        Args:
            workbench_state_manager: WorkbenchStateManager for state coordination
            session_restoration_coordinator: SessionRestorationCoordinator for session operations
            event_bus: Event bus for publishing restoration events
        """
        self._state_manager = workbench_state_manager
        self._session_coordinator = session_restoration_coordinator
        self._event_bus = event_bus

        # Restoration state
        self._current_phase = SessionRestorationPhase.NOT_STARTED
        self._restoration_errors: list[str] = []
        self._restoration_completed = False
        self._pending_session_data = None

        # Workbench callback for UI updates during restoration
        self._workbench_callback = None

        logger.debug("WorkbenchSessionManager initialized")

    def set_workbench_callback(self, callback):
        """
        Set callback to notify workbench of restoration events.

        Args:
            callback: Function to call with (start_position_data, pictograph_data, from_restoration)
        """
        self._workbench_callback = callback

    # Session Restoration Operations
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
        try:
            self._current_phase = SessionRestorationPhase.PREPARING
            self._restoration_errors = []

            # Extract session data from event
            state_data = event_data.get("state_data", {})
            sequence_data = state_data.get("sequence_data")
            start_position_data = state_data.get("start_position_data")

            # Check for sequence start position in sequence data itself
            sequence_start_position = None
            if sequence_data:
                if (
                    hasattr(sequence_data, "start_position")
                    and sequence_data.start_position
                ):
                    sequence_start_position = sequence_data.start_position
                elif isinstance(sequence_data, dict) and sequence_data.get(
                    "start_position"
                ):
                    sequence_start_position = sequence_data["start_position"]

            # Activate restoration mode in state manager
            if self._state_manager:
                self._state_manager.begin_restoration()

            # Store data for restoration
            self._pending_session_data = {
                "sequence_data": sequence_data,
                "start_position_data": start_position_data or sequence_start_position,
                "original_event_data": event_data,
            }

            logger.debug("Session restoration prepared from event")
            return SessionRestorationResult.success_result(
                SessionRestorationPhase.PREPARING
            )

        except Exception as e:
            logger.error(f"Failed to prepare restoration from event: {e}")
            self._restoration_errors.append(str(e))
            self._current_phase = SessionRestorationPhase.FAILED
            return SessionRestorationResult.failure_result(
                SessionRestorationPhase.FAILED, [str(e)]
            )

    def execute_restoration(self) -> SessionRestorationResult:
        """
        Execute the restoration with pending session data.

        Returns:
            SessionRestorationResult with restoration details
        """
        if not self._pending_session_data:
            error = "No pending session data to restore"
            logger.warning(error)
            self._restoration_errors.append(error)
            return SessionRestorationResult.failure_result(
                SessionRestorationPhase.FAILED, [error]
            )

        try:
            sequence_restored = False
            start_position_restored = False

            sequence_data = self._pending_session_data.get("sequence_data")
            start_position_data = self._pending_session_data.get("start_position_data")

            # Restore sequence
            if sequence_data and self._state_manager:
                self._current_phase = SessionRestorationPhase.RESTORING_SEQUENCE
                result = self._state_manager.set_sequence(
                    sequence_data, from_restoration=True
                )
                if result.changed:
                    sequence_restored = True
                    logger.debug("Sequence restored from session")
                else:
                    logger.debug("Sequence restoration had no changes")

            # Restore start position
            if start_position_data and self._state_manager:
                self._current_phase = SessionRestorationPhase.RESTORING_START_POSITION

                # Convert dict to BeatData if needed
                if isinstance(start_position_data, dict):
                    start_position_data = BeatData.from_dict(start_position_data)

                result = self._state_manager.set_start_position(
                    start_position_data, from_restoration=True
                )
                if result.changed:
                    start_position_restored = True
                    logger.debug("Start position restored from session")
                else:
                    logger.debug("Start position restoration had no changes")

                # CRITICAL FIX: Notify workbench UI during restoration
                # This ensures the UI is updated even if state didn't change
                if self._workbench_callback:
                    try:
                        self._workbench_callback(start_position_data, None, True)
                        logger.debug(
                            "Workbench UI notified of start position restoration"
                        )
                    except Exception as e:
                        logger.error(
                            f"Failed to notify workbench during restoration: {e}"
                        )

            # Finalize restoration
            self._current_phase = SessionRestorationPhase.FINALIZING

            if self._state_manager:
                self._state_manager.complete_restoration()

            self._current_phase = SessionRestorationPhase.COMPLETED
            self._restoration_completed = True
            self._pending_session_data = None

            logger.info(
                f"Session restoration completed - sequence: {sequence_restored}, start_position: {start_position_restored}"
            )

            return SessionRestorationResult.success_result(
                SessionRestorationPhase.COMPLETED,
                sequence_restored,
                start_position_restored,
            )

        except Exception as e:
            logger.error(f"Failed to execute restoration: {e}")
            self._restoration_errors.append(str(e))
            self._current_phase = SessionRestorationPhase.FAILED

            # Reset restoration state on failure
            if self._state_manager:
                self._state_manager.reset_restoration_state()

            return SessionRestorationResult.failure_result(
                SessionRestorationPhase.FAILED, [str(e)]
            )

    def handle_restoration_event(self, event_data: dict) -> SessionRestorationResult:
        """
        Handle complete restoration from event (convenience method).

        Args:
            event_data: Event data from session restoration event

        Returns:
            SessionRestorationResult with restoration details
        """
        # Begin restoration
        prepare_result = self.begin_restoration_from_event(event_data)
        if not prepare_result.success:
            return prepare_result

        # Execute restoration
        return self.execute_restoration()

    # Restoration for Missing Start Position (Special Case)
    def handle_missing_start_position_restoration(self) -> None:
        """
        Handle restoration when no start position data is available.

        This ensures the start position view is properly initialized even when cleared.
        """
        try:
            if self._state_manager:
                # Set start position to None to trigger proper clearing
                self._state_manager.set_start_position(None, from_restoration=True)

            logger.debug("Missing start position restoration handled")

        except Exception as e:
            logger.error(f"Failed to handle missing start position restoration: {e}")
            self._restoration_errors.append(str(e))

    # State Queries
    def get_current_phase(self) -> SessionRestorationPhase:
        """Get current restoration phase."""
        return self._current_phase

    def is_restoration_completed(self) -> bool:
        """Check if restoration has completed."""
        return self._restoration_completed

    def is_restoration_in_progress(self) -> bool:
        """Check if restoration is currently in progress."""
        return self._current_phase not in [
            SessionRestorationPhase.NOT_STARTED,
            SessionRestorationPhase.COMPLETED,
            SessionRestorationPhase.FAILED,
        ]

    def has_pending_restoration_data(self) -> bool:
        """Check if there's pending restoration data."""
        return self._pending_session_data is not None

    def get_restoration_errors(self) -> list[str]:
        """Get list of restoration errors."""
        return self._restoration_errors.copy()

    # Event Subscription Management
    def setup_event_subscriptions(self) -> list[str]:
        """
        Setup event subscriptions for session restoration.

        Returns:
            List of subscription IDs for cleanup
        """
        subscription_ids = []

        try:
            return subscription_ids

        except Exception as e:
            logger.error(f"Error setting up event subscriptions: {e}")

        return subscription_ids

    def _on_sequence_restored_event(self, event):
        """Handle sequence restoration event."""
        try:
            result = self.handle_restoration_event(event.__dict__)

            if not result.success:
                logger.error(f"Session restoration failed: {result.errors}")
            else:
                logger.info(f"Session restoration succeeded: {result.phase}")

        except Exception as e:
            logger.error(f"Error handling sequence restoration event: {e}")

    # Cleanup and Reset
    def cleanup_event_subscriptions(self, subscription_ids: list[str]) -> None:
        """Clean up event subscriptions."""
        if self._event_bus:
            for sub_id in subscription_ids:
                try:
                    self._event_bus.unsubscribe(sub_id)
                except Exception as e:
                    logger.error(f"Error unsubscribing from event: {e}")
            logger.debug("Session restoration event subscriptions cleaned up")

    def reset_restoration_state(self) -> None:
        """Reset all restoration state."""
        self._current_phase = SessionRestorationPhase.NOT_STARTED
        self._restoration_errors = []
        self._restoration_completed = False
        self._pending_session_data = None

        if self._state_manager:
            self._state_manager.reset_restoration_state()

        logger.debug("Restoration state reset")

    # Diagnostics
    def get_restoration_status_summary(self) -> dict:
        """Get comprehensive restoration status for debugging."""
        return {
            "current_phase": self._current_phase.value,
            "restoration_completed": self._restoration_completed,
            "is_in_progress": self.is_restoration_in_progress(),
            "has_pending_data": self.has_pending_restoration_data(),
            "error_count": len(self._restoration_errors),
            "errors": self._restoration_errors.copy(),
            "state_manager_available": self._state_manager is not None,
            "session_coordinator_available": self._session_coordinator is not None,
            "event_bus_available": self._event_bus is not None,
        }
