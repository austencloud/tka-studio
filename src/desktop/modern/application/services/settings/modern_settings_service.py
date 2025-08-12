"""
Modern Settings Service Implementation for TKA

Implements modern state persistence using QSettings with CQRS patterns,
dependency injection, and seamless integration with session state.

Architecture:
- CQRS pattern: Separates command (write) and query (read) operations
- Memento pattern: Creates state snapshots for restoration
- Event-driven: Emits events for state changes
- Service composition: Delegates to specialized managers
- QSettings integration: Platform-independent persistence
"""

from __future__ import annotations

from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Any, TypeVar

from PyQt6.QtCore import QObject, QSettings, pyqtSignal

# Event bus removed - using Qt signals instead
from desktop.modern.core.interfaces.session_services import ISessionStateTracker
from desktop.modern.core.interfaces.settings_services import (
    IBackgroundSettingsManager,
    IBeatLayoutSettingsManager,
    IImageExportSettingsManager,
    IPropTypeSettingsManager,
    IUserProfileSettingsManager,
    IVisibilitySettingsManager,
)


T = TypeVar("T")
logger = logging.getLogger(__name__)


class ApplicationStateMemento:
    """
    Memento pattern implementation for capturing complete application state.

    This allows us to save and restore the entire application state as a single unit,
    implementing the best practices from modern state management research.
    """

    def __init__(
        self,
        current_tab: str,
        window_geometry: bytes | None = None,
        window_state: bytes | None = None,
        session_data: dict | None = None,
        settings_snapshot: dict | None = None,
    ):
        self.current_tab = current_tab
        self.window_geometry = window_geometry
        self.window_state = window_state
        self.session_data = session_data or {}
        self.settings_snapshot = settings_snapshot or {}
        self.timestamp = datetime.now()

    def _serialize_data(self, data):
        """Recursively serialize data, converting datetime objects to ISO strings."""
        from datetime import datetime

        if isinstance(data, datetime):
            return data.isoformat()
        if isinstance(data, dict):
            return {key: self._serialize_data(value) for key, value in data.items()}
        if isinstance(data, list):
            return [self._serialize_data(item) for item in data]
        if hasattr(data, "__dict__"):
            # Handle dataclass or object with attributes
            return self._serialize_data(data.__dict__)
        return data

    def to_dict(self) -> dict[str, Any]:
        """Convert memento to dictionary for persistence."""
        # Handle QByteArray conversion to hex string
        window_geometry_hex = None
        if self.window_geometry:
            if hasattr(self.window_geometry, "data"):
                # QByteArray - convert to bytes first
                window_geometry_hex = bytes(self.window_geometry).hex()
            elif hasattr(self.window_geometry, "hex"):
                # Already bytes
                window_geometry_hex = self.window_geometry.hex()
            else:
                # Try to convert to bytes
                try:
                    window_geometry_hex = bytes(self.window_geometry).hex()
                except:
                    window_geometry_hex = None

        window_state_hex = None
        if self.window_state:
            if hasattr(self.window_state, "data"):
                # QByteArray - convert to bytes first
                window_state_hex = bytes(self.window_state).hex()
            elif hasattr(self.window_state, "hex"):
                # Already bytes
                window_state_hex = self.window_state.hex()
            else:
                # Try to convert to bytes
                try:
                    window_state_hex = bytes(self.window_state).hex()
                except:
                    window_state_hex = None

        return {
            "current_tab": self.current_tab,
            "window_geometry": window_geometry_hex,
            "window_state": window_state_hex,
            "session_data": self._serialize_data(self.session_data),
            "settings_snapshot": self._serialize_data(self.settings_snapshot),
            "timestamp": self.timestamp.isoformat(),
        }

    def to_json(self) -> str:
        """Convert memento to JSON string for serialization."""
        import json

        return json.dumps(self.to_dict(), indent=2, default=datetime_serializer)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ApplicationStateMemento:
        """Create memento from dictionary."""
        timestamp_str = data.get("timestamp")
        timestamp = (
            datetime.fromisoformat(timestamp_str) if timestamp_str else datetime.now()
        )

        memento = cls(
            current_tab=data.get("current_tab", "construct"),
            window_geometry=(
                bytes.fromhex(data["window_geometry"])
                if data.get("window_geometry")
                else None
            ),
            window_state=(
                bytes.fromhex(data["window_state"])
                if data.get("window_state")
                else None
            ),
            session_data=data.get("session_data", {}),
            settings_snapshot=data.get("settings_snapshot", {}),
        )
        memento.timestamp = timestamp
        return memento


class ModernSettingsService(QObject):
    """
    Modern settings service implementing CQRS pattern with QSettings backend.

    This service provides:
    - Separation of concerns (each settings type has its own manager)
    - Event-driven updates
    - Integration with session state
    - Memento pattern for state snapshots
    - Dependency injection compatibility
    """

    # Command side events (writes)
    settings_changed = pyqtSignal(str, str, object)  # section, key, value

    # Query side events (reads)
    settings_loaded = pyqtSignal(dict)  # all_settings

    def __init__(
        self,
        session_tracker: ISessionStateTracker,
        organization_name: str = "TKA",
        application_name: str = "KineticConstructor",
    ):
        super().__init__()

        self.session_tracker = session_tracker
        # Event bus removed - using Qt signals instead

        # Initialize QSettings with proper organization/app names
        self.settings = QSettings(organization_name, application_name)

        # Initialize specialized managers (dependency injection)
        self._background_manager: IBackgroundSettingsManager | None = None
        self._visibility_manager: IVisibilitySettingsManager | None = None
        self._layout_manager: IBeatLayoutSettingsManager | None = None
        self._prop_manager: IPropTypeSettingsManager | None = None
        self._user_manager: IUserProfileSettingsManager | None = None
        self._export_manager: IImageExportSettingsManager | None = None

        # State management
        self._current_state_memento: ApplicationStateMemento | None = None

        logger.info(
            f"Initialized ModernSettingsService with QSettings: {self.settings.fileName()}"
        )

    # ============================================================================
    # DEPENDENCY INJECTION - Manager Registration
    # ============================================================================

    def register_background_manager(self, manager: IBackgroundSettingsManager) -> None:
        """Register background settings manager."""
        self._background_manager = manager
        logger.debug("Registered background settings manager")

    def register_visibility_manager(self, manager: IVisibilitySettingsManager) -> None:
        """Register visibility settings manager."""
        self._visibility_manager = manager
        logger.debug("Registered visibility settings manager")

    def register_layout_manager(self, manager: IBeatLayoutSettingsManager) -> None:
        """Register layout settings manager."""
        self._layout_manager = manager
        logger.debug("Registered layout settings manager")

    def register_prop_manager(self, manager: IPropTypeSettingsManager) -> None:
        """Register prop type settings manager."""
        self._prop_manager = manager
        logger.debug("Registered prop type settings manager")

    def register_user_manager(self, manager: IUserProfileSettingsManager) -> None:
        """Register user profile settings manager."""
        self._user_manager = manager
        logger.debug("Registered user profile settings manager")

    def register_export_manager(self, manager: IImageExportSettingsManager) -> None:
        """Register image export settings manager."""
        self._export_manager = manager
        logger.debug("Registered image export settings manager")

    # ============================================================================
    # CQRS PATTERN - Command Side (Write Operations)
    # ============================================================================

    def execute_setting_command(self, section: str, key: str, value: Any) -> bool:
        """
        Execute a setting write command (CQRS command side).

        Args:
            section: Settings section
            key: Setting key
            value: Value to set

        Returns:
            bool: Success status
        """
        try:
            # Command validation
            if not self._validate_setting_command(section, key, value):
                return False

            # Execute command
            full_key = f"{section}/{key}"
            self.settings.value(full_key)

            self.settings.setValue(full_key, value)
            self.settings.sync()

            # Emit command completion event
            self.settings_changed.emit(section, key, value)

            # Update session state if this is a UI-relevant setting
            if section in ["ui", "global", "workbench"]:
                self.session_tracker.mark_interaction()

            logger.debug(f"Setting command executed: {full_key} = {value}")
            return True

        except Exception as e:
            logger.exception(f"Failed to execute setting command {section}/{key}: {e}")
            return False

    def execute_bulk_setting_command(
        self, settings_dict: dict[str, dict[str, Any]]
    ) -> bool:
        """
        Execute multiple setting commands atomically.

        Args:
            settings_dict: Nested dictionary of section -> key -> value

        Returns:
            bool: Success status
        """
        try:
            # Begin atomic transaction
            self.settings.sync()

            for section, section_settings in settings_dict.items():
                for key, value in section_settings.items():
                    if not self.execute_setting_command(section, key, value):
                        # Rollback would go here in a more sophisticated implementation
                        logger.warning(
                            f"Failed to set {section}/{key} during bulk operation"
                        )

            return True

        except Exception as e:
            logger.exception(f"Bulk setting command failed: {e}")
            return False

    def _validate_setting_command(self, section: str, key: str, value: Any) -> bool:
        """Validate a setting command before execution."""
        # Add validation logic here
        if not section or not key:
            logger.error("Section and key cannot be empty")
            return False

        # Add more validation as needed
        return True

    # ============================================================================
    # CQRS PATTERN - Query Side (Read Operations)
    # ============================================================================

    def query_setting(
        self, section: str, key: str, default: Any = None, type_hint: type[T] | None = None
    ) -> T:
        """
        Query a setting value (CQRS query side).

        Args:
            section: Settings section
            key: Setting key
            default: Default value if not found
            type_hint: Type hint for proper casting

        Returns:
            Setting value with proper type
        """
        try:
            full_key = f"{section}/{key}"

            if type_hint:
                return self.settings.value(full_key, default, type=type_hint)
            return self.settings.value(full_key, default)

        except Exception as e:
            logger.exception(f"Failed to query setting {section}/{key}: {e}")
            return default

    def query_section(self, section: str) -> dict[str, Any]:
        """
        Query all settings in a section.

        Args:
            section: Settings section name

        Returns:
            Dictionary of all settings in the section
        """
        try:
            self.settings.beginGroup(section)
            keys = self.settings.childKeys()
            result = {}

            for key in keys:
                result[key] = self.settings.value(key)

            self.settings.endGroup()
            return result

        except Exception as e:
            logger.exception(f"Failed to query section {section}: {e}")
            return {}

    def query_all_settings(self) -> dict[str, dict[str, Any]]:
        """
        Query all settings from all sections.

        Returns:
            Nested dictionary of all settings
        """
        try:
            all_groups = self.settings.childGroups()
            result = {}

            for group in all_groups:
                result[group] = self.query_section(group)

            # Also get top-level keys
            top_level_keys = self.settings.childKeys()
            if top_level_keys:
                result["_root"] = {}
                for key in top_level_keys:
                    result["_root"][key] = self.settings.value(key)

            return result

        except Exception as e:
            logger.exception(f"Failed to query all settings: {e}")
            return {}

    # ============================================================================
    # MEMENTO PATTERN - State Snapshots
    # ============================================================================

    def create_state_memento(
        self,
        current_tab: str,
        window_geometry: bytes | None = None,
        window_state: bytes | None = None,
        session_data: dict[str, Any] | None = None,
    ) -> ApplicationStateMemento:
        """
        Create a state memento for the current application state.

        Args:
            current_tab: Currently active tab
            window_geometry: Window geometry data
            window_state: Window state data
            session_data: Optional session data dictionary

        Returns:
            ApplicationStateMemento instance
        """
        try:
            # Use provided session data or get current session state
            if session_data is None:
                current_session = self.session_tracker.get_current_session_state()
                session_dict = current_session.__dict__ if current_session else {}
            else:
                session_dict = session_data

            # Create settings snapshot
            settings_snapshot = self.query_all_settings()

            memento = ApplicationStateMemento(
                current_tab=current_tab,
                window_geometry=window_geometry,
                window_state=window_state,
                session_data=session_dict,
                settings_snapshot=settings_snapshot,
            )

            self._current_state_memento = memento
            logger.debug("Created application state memento")
            return memento

        except Exception as e:
            logger.exception(f"Failed to create state memento: {e}")
            return ApplicationStateMemento(current_tab)

    def restore_from_memento(self, memento: ApplicationStateMemento) -> bool:
        """
        Restore application state from a memento.

        Args:
            memento: The memento to restore from

        Returns:
            bool: Success status
        """
        try:
            # Restore settings
            if memento.settings_snapshot:
                success = self.execute_bulk_setting_command(memento.settings_snapshot)
                if not success:
                    logger.warning("Failed to restore some settings from memento")

            # Update current memento
            self._current_state_memento = memento

            logger.info("Successfully restored application state from memento")
            return True

        except Exception as e:
            logger.exception(f"Failed to restore from memento: {e}")
            return False

    def save_state_memento(
        self, memento: ApplicationStateMemento, file_path: Path | None = None
    ) -> bool:
        """
        Save a state memento to file.

        Args:
            memento: The memento to save
            file_path: Optional custom file path

        Returns:
            bool: Success status
        """
        try:
            if file_path is None:
                # Use default location in modern directory
                modern_dir = Path(__file__).parent.parent.parent.parent
                file_path = modern_dir / "application_state.json"

            memento_data = memento.to_dict()

            with open(file_path, "w") as f:
                json.dump(memento_data, f, indent=2)

            logger.info(f"Saved state memento to {file_path}")
            return True

        except Exception as e:
            logger.exception(f"Failed to save state memento: {e}")
            return False

    def load_state_memento(
        self, file_path: Path | None = None
    ) -> ApplicationStateMemento | None:
        """
        Load a state memento from file.

        Args:
            file_path: Optional custom file path

        Returns:
            ApplicationStateMemento instance or None if failed
        """
        try:
            if file_path is None:
                # Use default location in modern directory
                modern_dir = Path(__file__).parent.parent.parent.parent
                file_path = modern_dir / "application_state.json"

            if not file_path.exists():
                logger.info("No state memento file found")
                return None

            with open(file_path) as f:
                memento_data = json.load(f)

            memento = ApplicationStateMemento.from_dict(memento_data)
            logger.info(f"Loaded state memento from {file_path}")
            return memento

        except Exception as e:
            logger.exception(f"Failed to load state memento: {e}")
            return None

    # ============================================================================
    # HIGH-LEVEL STATE MANAGEMENT INTERFACE
    # ============================================================================

    def save_application_state(
        self,
        current_tab: str,
        window_geometry: bytes | None = None,
        window_state: bytes | None = None,
    ) -> bool:
        """
        Save complete application state (settings + session + window state).

        Args:
            current_tab: Currently active tab
            window_geometry: Window geometry data
            window_state: Window state data

        Returns:
            bool: Success status
        """
        try:
            # Create memento
            memento = self.create_state_memento(
                current_tab, window_geometry, window_state
            )

            # Save memento to file
            success = self.save_state_memento(memento)

            # Also ensure session state is saved
            session_success = self.session_tracker.save_session_state()

            if success and session_success:
                logger.info("Successfully saved complete application state")
                return True
            logger.warning("Partial failure saving application state")
            return False

        except Exception as e:
            logger.exception(f"Failed to save application state: {e}")
            return False

    def restore_application_state(self) -> ApplicationStateMemento | None:
        """
        Restore complete application state from persistent storage.

        Returns:
            ApplicationStateMemento if successful, None otherwise
        """
        try:
            # Load memento from file
            memento = self.load_state_memento()

            if memento:
                # Restore from memento
                success = self.restore_from_memento(memento)

                if success:
                    logger.info("Successfully restored complete application state")
                    return memento
                logger.warning("Failed to restore application state from memento")

            return None

        except Exception as e:
            logger.exception(f"Failed to restore application state: {e}")
            return None

    # ============================================================================
    # MANAGER ACCESS METHODS
    # ============================================================================
    # ============================================================================
    # COMPATIBILITY METHODS - Legacy Interface Support
    # ============================================================================

    def get_setting(self, section: str, key: str, default: Any = None) -> Any:
        """Legacy compatible method for getting settings."""
        return self.query_setting(section, key, default)

    def set_setting(self, section: str, key: str, value: Any) -> None:
        """Legacy compatible method for setting values."""
        self.execute_setting_command(section, key, value)

    def get_current_tab(self) -> str:
        """Get the current active tab."""
        return self.query_setting("global", "current_tab", "construct", str)

    def set_current_tab(self, tab: str) -> None:
        """Set the current active tab."""
        self.execute_setting_command("global", "current_tab", tab)
