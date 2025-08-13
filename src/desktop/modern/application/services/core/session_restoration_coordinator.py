"""
Session Restoration Coordinator

Service for coordinating session restoration between services.
Extracted from ApplicationLifecycleManager to follow single responsibility principle.

PROVIDES:
- Session loading coordination
- Deferred session restoration triggering
- Event publishing for session restoration
"""

from abc import ABCMeta

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.application.services.sequence.sequence_restorer import (
    ISequenceRestorer,
)
from desktop.modern.core.interfaces.core_services import ISessionRestorationCoordinator
from desktop.modern.core.interfaces.session_services import (
    ISessionStateTracker,
    SessionState,
)


class QObjectABCMeta(type(QObject), ABCMeta):
    """Metaclass that combines QObject's metaclass with ABCMeta."""


class SessionRestorationCoordinator(
    QObject, ISessionRestorationCoordinator, metaclass=QObjectABCMeta
):
    """
    Service for coordinating session restoration between services.

    Handles session loading coordination and Qt signal emission
    without any window management or domain logic dependencies.
    """

    # Qt signals for session restoration events
    sequence_restored = pyqtSignal(dict)  # sequence restoration data
    tab_restored = pyqtSignal(str)  # active_tab

    def __init__(self, sequence_restoration_service: ISequenceRestorer | None = None):
        """Initialize session restoration coordinator."""
        super().__init__()
        self.sequence_restoration_service = sequence_restoration_service
        self._pending_session_data = None

    def load_and_prepare_session(
        self, session_service: ISessionStateTracker
    ) -> SessionState | None:
        """Load and prepare session data for restoration."""
        if not session_service:
            return None

        try:
            restore_result = session_service.load_session_state()

            if restore_result.success and restore_result.session_restored:
                self._pending_session_data = restore_result.session_data
                return restore_result.session_data
            else:
                if restore_result.warnings:
                    for warning in restore_result.warnings:
                        print(f"⚠️ Session warning: {warning}")
                return None
        except Exception as e:
            print(f"⚠️ Failed to restore session: {e}")
            return None

    def trigger_deferred_restoration(self, session_data: SessionState) -> None:
        """Trigger deferred session restoration after UI components are ready."""
        if session_data:
            self._apply_restored_session_to_ui(session_data)
            self._pending_session_data = None  # Clear after use

    def trigger_deferred_restoration_if_pending(self) -> None:
        """Trigger deferred session restoration if there's pending data."""
        if self._pending_session_data:
            self.trigger_deferred_restoration(self._pending_session_data)

    def _apply_restored_session_to_ui(self, session_data: SessionState) -> None:
        """Apply restored session data to UI components."""
        try:
            # Restore sequence if available
            if session_data.current_sequence_id and session_data.current_sequence_data:
                # Use sequence restoration service if available
                if self.sequence_restoration_service:
                    sequence_data = (
                        self.sequence_restoration_service.restore_sequence_from_session(
                            session_data
                        )
                    )
                else:
                    # Fallback: use raw session data
                    sequence_data = session_data.current_sequence_data

                if sequence_data:
                    # Emit Qt signal for sequence restoration
                    restoration_data = {
                        "sequence_data": sequence_data,
                        "sequence_id": session_data.current_sequence_id,
                        "selected_beat_index": session_data.selected_beat_index,
                        "start_position_data": session_data.start_position_data,
                    }
                    self.sequence_restored.emit(restoration_data)

            # Restore UI state
            if session_data.active_tab:
                # Emit Qt signal for tab restoration
                self.tab_restored.emit(session_data.active_tab)

        except Exception as e:
            print(f"⚠️ Failed to apply restored session to UI: {e}")
