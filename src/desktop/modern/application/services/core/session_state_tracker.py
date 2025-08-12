"""
Session State Service Implementation

Provides robust auto-save/restore functionality for TKA applications.
Automatically saves user state after interactions and restores exactly where they left off.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta
import json
import logging
from pathlib import Path
from typing import Any
import uuid

from PyQt6.QtCore import QTimer

from desktop.modern.core.interfaces.core_services import IUIStateManager
from desktop.modern.core.interfaces.organization_services import IFileSystemService
from desktop.modern.core.interfaces.session_services import (
    ISessionStateTracker,
    SessionRestoreResult,
    SessionState,
)


logger = logging.getLogger(__name__)


class SessionStateTracker(ISessionStateTracker):
    """
    Production implementation of session state management.

    Provides VSCode-like auto-save/restore functionality with:
    - Debounced auto-save after user interactions
    - Graceful error handling for corrupted/missing files
    - Session staleness detection
    - Integration with existing TKA services
    """

    def __init__(
        self,
        ui_state_service: IUIStateManager,
        file_system_service: IFileSystemService,
        event_bus: Any | None = None,
    ):
        """
        Initialize session state service.

        Args:
            ui_state_service: UI state management service
            file_system_service: File system service for persistence
            event_bus: Event bus for state synchronization (optional)
        """
        self.ui_state_service = ui_state_service
        self.file_system_service = file_system_service
        self.event_bus = event_bus or get_event_bus()

        # Session file location alongside user_settings.json
        # Navigate from: src/application/services/core/ -> modern/
        modern_dir = Path(__file__).parent.parent.parent.parent.parent
        self.session_file = modern_dir / "session_state.json"

        # Current session state
        self._current_session = SessionState()

        # Auto-save configuration
        self.auto_save_enabled = True
        self.auto_save_delay_ms = 2000  # 2 second delay after last interaction
        self.session_staleness_hours = 24  # Consider session stale after 24 hours

        # Setup auto-save timer
        self._auto_save_timer = QTimer()
        self._setup_auto_save_timer()

    def _setup_auto_save_timer(self) -> None:
        """Setup debounced auto-save timer."""
        if self._auto_save_timer:
            self._auto_save_timer.setSingleShot(True)
            self._auto_save_timer.timeout.connect(self._perform_auto_save)

    def save_session_state(self) -> bool:
        """Save current session state to persistent storage."""
        try:
            # Update last interaction timestamp
            self._current_session.last_interaction = datetime.now()

            # Convert session state to dictionary
            session_data = {
                "session_metadata": {
                    "session_id": self._current_session.session_id,
                    "created_at": self._current_session.created_at.isoformat(),
                    "last_interaction": self._current_session.last_interaction.isoformat(),
                    "tka_version": self._current_session.tka_version,
                },
                "workbench_state": {
                    "selected_beat_index": self._current_session.selected_beat_index,
                    "selected_beat_data": self._current_session.selected_beat_data,
                    "start_position_data": self._current_session.start_position_data,
                },
                "graph_editor_state": {
                    "visible": self._current_session.graph_editor_visible,
                    "selected_beat_index": self._current_session.graph_editor_selected_beat_index,
                    "selected_arrow": self._current_session.graph_editor_selected_arrow,
                    "height": self._current_session.graph_editor_height,
                },
                "ui_state": {
                    "active_tab": self._current_session.active_tab,
                    "beat_layout": self._current_session.beat_layout,
                    "component_visibility": self._current_session.component_visibility,
                },
            }

            # Write to file using file system service
            self.file_system_service.write_file(
                self.session_file, json.dumps(session_data, indent=2)
            )

            logger.debug("Session state saved successfully")
            return True

        except Exception as e:
            logger.exception(f"Failed to save session state: {e}")
            return False

    def load_session_state(self) -> SessionRestoreResult:
        """Load session state from persistent storage."""
        try:
            # Check if session file exists
            if not self.session_file.exists():
                logger.info("No session file found - starting with clean state")
                return SessionRestoreResult(
                    success=True, session_restored=False, session_data=None
                )

            # Read session file
            content = self.file_system_service.read_file(self.session_file)
            session_data = json.loads(content)

            # Parse session metadata
            metadata = session_data.get("session_metadata", {})
            last_interaction_str = metadata.get("last_interaction")

            if last_interaction_str:
                last_interaction = datetime.fromisoformat(last_interaction_str)

                # Check if session is too stale
                if not self._is_session_fresh(last_interaction):
                    logger.info("Session is too stale - starting with clean state")
                    return SessionRestoreResult(
                        success=True,
                        session_restored=False,
                        session_data=None,
                        warnings=["Session was too old to restore"],
                    )

            # Restore session state
            restored_session = self._parse_session_data(session_data)
            self._current_session = restored_session

            return SessionRestoreResult(
                success=True, session_restored=True, session_data=restored_session
            )

        except json.JSONDecodeError as e:
            logger.exception(f"Session file is corrupted: {e}")
            return SessionRestoreResult(
                success=True,
                session_restored=False,
                session_data=None,
                error_message="Session file was corrupted",
            )
        except Exception as e:
            logger.exception(f"Failed to load session state: {e}")
            return SessionRestoreResult(
                success=False,
                session_restored=False,
                session_data=None,
                error_message=str(e),
            )

    def update_current_sequence(self, sequence_data: Any, sequence_id: str) -> None:
        """Update current sequence in session state."""
        # Removed repetitive log statements

        try:
            # Convert sequence data to serializable format
            if hasattr(sequence_data, "to_dict"):
                # Use custom to_dict() method which properly handles enum serialization
                serializable_data = sequence_data.to_dict()
            elif hasattr(sequence_data, "__dict__"):
                serializable_data = (
                    asdict(sequence_data)
                    if hasattr(sequence_data, "__dataclass_fields__")
                    else vars(sequence_data)
                )
            else:
                serializable_data = sequence_data

            self._current_session.current_sequence_id = sequence_id
            self._current_session.current_sequence_data = serializable_data

            # Trigger auto-save
            self.mark_interaction()

            logger.debug(f"Updated current sequence: {sequence_id}")

        except Exception as e:
            logger.exception(f"Failed to update current sequence: {e}")

    def update_workbench_state(
        self,
        beat_index: int | None,
        beat_data: Any | None,
        start_position: Any | None,
    ) -> None:
        """Update workbench selection state."""
        try:
            self._current_session.selected_beat_index = beat_index

            # SERIALIZATION PATH SELECTION: Convert beat data to serializable format
            # Multiple paths are necessary due to diverse object types with different capabilities:
            # 1. to_dict() - Preferred: Domain models with proper enum serialization
            # 2. dict check - Already serialized data
            # 3. asdict() - Dataclass fallback (may have enum issues)
            # 4. direct assignment - Primitive types or pre-serialized data
            if beat_data:
                if hasattr(beat_data, "to_dict"):
                    # PREFERRED: Custom to_dict() method handles enum serialization correctly
                    self._current_session.selected_beat_data = beat_data.to_dict()
                elif isinstance(beat_data, dict):
                    # ALREADY SERIALIZED: Use as-is
                    self._current_session.selected_beat_data = beat_data
                elif hasattr(beat_data, "__dataclass_fields__"):
                    # FALLBACK: asdict() for dataclasses (may cause enum serialization issues)
                    self._current_session.selected_beat_data = asdict(beat_data)
                else:
                    # PRIMITIVE: Direct assignment for basic types
                    self._current_session.selected_beat_data = beat_data
            else:
                self._current_session.selected_beat_data = None

            # Convert start position to serializable format
            if start_position:
                if hasattr(start_position, "to_dict"):
                    # Use custom to_dict() method which properly handles enum serialization
                    self._current_session.start_position_data = start_position.to_dict()
                elif isinstance(start_position, dict):
                    self._current_session.start_position_data = start_position
                elif hasattr(start_position, "__dataclass_fields__"):
                    # Fallback to asdict() but this may cause enum serialization issues
                    self._current_session.start_position_data = asdict(start_position)
                else:
                    self._current_session.start_position_data = start_position
            else:
                self._current_session.start_position_data = None

            # Trigger auto-save
            self.mark_interaction()

            logger.debug(f"Updated workbench state: beat_index={beat_index}")

        except Exception as e:
            logger.exception(f"Failed to update workbench state: {e}")

    def update_graph_editor_state(
        self,
        visible: bool,
        beat_index: int | None,
        selected_arrow: str | None,
        height: int | None = None,
    ) -> None:
        """Update graph editor state."""
        try:
            self._current_session.graph_editor_visible = visible
            self._current_session.graph_editor_selected_beat_index = beat_index
            self._current_session.graph_editor_selected_arrow = selected_arrow

            if height is not None:
                self._current_session.graph_editor_height = height

            # Trigger auto-save
            self.mark_interaction()

            logger.debug(
                f"Updated graph editor state: visible={visible}, beat_index={beat_index}"
            )

        except Exception as e:
            logger.exception(f"Failed to update graph editor state: {e}")

    def update_ui_state(
        self,
        active_tab: str,
        beat_layout: dict[str, Any] | None = None,
        component_visibility: dict[str, bool] | None = None,
    ) -> None:
        """Update UI state information."""
        try:
            self._current_session.active_tab = active_tab

            if beat_layout is not None:
                self._current_session.beat_layout = beat_layout.copy()

            if component_visibility is not None:
                self._current_session.component_visibility = component_visibility.copy()

            # Trigger auto-save
            self.mark_interaction()

            logger.debug(f"Updated UI state: active_tab={active_tab}")

        except Exception as e:
            logger.exception(f"Failed to update UI state: {e}")

    def should_restore_session(self) -> bool:
        """Determine if session should be restored (not too stale)."""
        try:
            if not self.session_file.exists():
                return False

            content = self.file_system_service.read_file(self.session_file)
            session_data = json.loads(content)

            metadata = session_data.get("session_metadata", {})
            last_interaction_str = metadata.get("last_interaction")

            if not last_interaction_str:
                return False

            last_interaction = datetime.fromisoformat(last_interaction_str)
            return self._is_session_fresh(last_interaction)

        except Exception as e:
            logger.exception(f"Failed to check session staleness: {e}")
            return False

    def mark_interaction(self) -> None:
        """Mark user interaction to trigger debounced auto-save."""
        if not self.auto_save_enabled:
            return

        try:
            # Update last interaction timestamp
            self._current_session.last_interaction = datetime.now()

            # Restart auto-save timer (debounced)
            if self._auto_save_timer:
                self._auto_save_timer.stop()
                self._auto_save_timer.start(self.auto_save_delay_ms)

        except Exception as e:
            logger.exception(f"Failed to mark interaction: {e}")

    def clear_session(self) -> bool:
        """Clear current session state and remove session file."""
        try:
            # Reset current session to defaults
            self._current_session = SessionState()

            # Remove session file if it exists
            if self.session_file.exists():
                self.session_file.unlink()

            logger.info("Session state cleared successfully")
            return True

        except Exception as e:
            logger.exception(f"Failed to clear session: {e}")
            return False

    def get_current_session_state(self) -> SessionState | None:
        """Get current session state without loading from file."""
        return self._current_session

    def is_auto_save_enabled(self) -> bool:
        """Check if auto-save is currently enabled."""
        return self.auto_save_enabled

    def set_auto_save_enabled(self, enabled: bool) -> None:
        """Enable or disable auto-save functionality."""
        self.auto_save_enabled = enabled

        if not enabled and self._auto_save_timer:
            self._auto_save_timer.stop()

        logger.info(f"Auto-save {'enabled' if enabled else 'disabled'}")

    def _perform_auto_save(self) -> None:
        """Perform auto-save operation (called by timer)."""
        try:
            success = self.save_session_state()
            if success:
                logger.debug("Auto-save completed successfully")
            else:
                logger.warning("Auto-save failed")

        except Exception as e:
            logger.exception(f"Auto-save error: {e}")

    def _is_session_fresh(self, last_interaction: datetime) -> bool:
        """Check if session is fresh enough to restore."""
        staleness_threshold = datetime.now() - timedelta(
            hours=self.session_staleness_hours
        )
        return last_interaction > staleness_threshold

    def _parse_session_data(self, session_data: dict[str, Any]) -> SessionState:
        """Parse session data from JSON into SessionState object."""
        try:
            # Parse metadata
            metadata = session_data.get("session_metadata", {})
            created_at = datetime.fromisoformat(
                metadata.get("created_at", datetime.now().isoformat())
            )
            last_interaction = datetime.fromisoformat(
                metadata.get("last_interaction", datetime.now().isoformat())
            )

            # Parse sequence data
            sequence_info = session_data.get("current_sequence", {})

            # Parse workbench state
            workbench_state = session_data.get("workbench_state", {})

            # Parse graph editor state
            graph_editor_state = session_data.get("graph_editor_state", {})

            # Parse UI state
            ui_state = session_data.get("ui_state", {})

            return SessionState(
                # Session metadata
                session_id=metadata.get("session_id", str(uuid.uuid4())),
                created_at=created_at,
                last_interaction=last_interaction,
                tka_version=metadata.get("tka_version", "modern"),
                # Sequence data
                current_sequence_id=sequence_info.get("sequence_id"),
                current_sequence_data=sequence_info.get("sequence_data"),
                # Workbench state
                selected_beat_index=workbench_state.get("selected_beat_index"),
                selected_beat_data=workbench_state.get("selected_beat_data"),
                start_position_data=workbench_state.get("start_position_data"),
                # Graph editor state
                graph_editor_visible=graph_editor_state.get("visible", False),
                graph_editor_selected_beat_index=graph_editor_state.get(
                    "selected_beat_index"
                ),
                graph_editor_selected_arrow=graph_editor_state.get("selected_arrow"),
                graph_editor_height=graph_editor_state.get("height", 300),
                # UI state
                active_tab=ui_state.get("active_tab", "sequence_builder"),
                beat_layout=ui_state.get("beat_layout", {}),
                component_visibility=ui_state.get("component_visibility", {}),
            )

        except Exception as e:
            logger.exception(f"Failed to parse session data: {e}")
            # Return default session state on parse error
            return SessionState()

    # Missing interface methods implementation
    def export_session_state(self) -> str:
        """Export current session state as JSON string (interface implementation)."""
        try:
            current_state = self._capture_current_state()
            session_data = {
                "version": "1.0",
                "timestamp": datetime.now().isoformat(),
                "session_id": str(uuid.uuid4()),
                "state": asdict(current_state),
            }
            return json.dumps(session_data, indent=2)
        except Exception as e:
            logger.exception(f"Failed to export session state: {e}")
            return "{}"

    def import_session_state(self, session_json: str) -> bool:
        """Import session state from JSON string (interface implementation)."""
        try:
            session_data = json.loads(session_json)

            # Validate basic structure
            if "state" not in session_data:
                logger.error("Invalid session data: missing 'state' field")
                return False

            # Parse the session state
            session_state = self._parse_session_data(session_data["state"])

            # Restore the state
            result = self.restore_session(session_state)
            return result.success

        except json.JSONDecodeError as e:
            logger.exception(f"Failed to parse session JSON: {e}")
            return False
        except Exception as e:
            logger.exception(f"Failed to import session state: {e}")
            return False

    def migrate_session_state(self, from_version: str, to_version: str) -> bool:
        """Migrate session state between versions (interface implementation)."""
        try:
            logger.info(f"Migrating session state from {from_version} to {to_version}")

            # For now, we only support migration to current version
            if to_version != "1.0":
                logger.warning(f"Unsupported target version: {to_version}")
                return False

            # Version 1.0 is our current format, so no migration needed
            if from_version == "1.0":
                logger.info("No migration needed - already at target version")
                return True

            # Add migration logic here for future versions
            logger.warning(f"Migration from {from_version} not implemented yet")
            return False

        except Exception as e:
            logger.exception(f"Failed to migrate session state: {e}")
            return False
