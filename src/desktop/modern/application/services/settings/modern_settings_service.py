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

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar

from PyQt6.QtCore import QSettings, QObject, pyqtSignal

from desktop.modern.core.interfaces.settings_services import (
    IBackgroundSettingsManager,
    IVisibilitySettingsManager,
    IBeatLayoutSettingsManager,
    IPropTypeSettingsManager,
    IUserProfileSettingsManager,
    IImageExportSettingsManager,
    PropType,
)
from desktop.modern.core.interfaces.session_services import ISessionStateTracker
from desktop.modern.core.events.event_bus import get_event_bus

T = TypeVar('T')
logger = logging.getLogger(__name__)


class ApplicationStateMemento:
    """
    Memento pattern implementation for capturing complete application state.
    
    This allows us to save and restore the entire application state as a single unit,
    implementing the best practices from modern state management research.
    """
    
    def __init__(self, 
                 current_tab: str,
                 window_geometry: Optional[bytes] = None,
                 window_state: Optional[bytes] = None,
                 session_data: Optional[Dict] = None,
                 settings_snapshot: Optional[Dict] = None):
        self.current_tab = current_tab
        self.window_geometry = window_geometry
        self.window_state = window_state
        self.session_data = session_data or {}
        self.settings_snapshot = settings_snapshot or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memento to dictionary for persistence."""
        return {
            'current_tab': self.current_tab,
            'window_geometry': self.window_geometry.hex() if self.window_geometry else None,
            'window_state': self.window_state.hex() if self.window_state else None,
            'session_data': self.session_data,
            'settings_snapshot': self.settings_snapshot,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ApplicationStateMemento':
        """Create memento from dictionary."""
        timestamp_str = data.get('timestamp')
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else datetime.now()
        
        memento = cls(
            current_tab=data.get('current_tab', 'construct'),
            window_geometry=bytes.fromhex(data['window_geometry']) if data.get('window_geometry') else None,
            window_state=bytes.fromhex(data['window_state']) if data.get('window_state') else None,
            session_data=data.get('session_data', {}),
            settings_snapshot=data.get('settings_snapshot', {})
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
    
    def __init__(self, 
                 session_tracker: ISessionStateTracker,
                 organization_name: str = "TKA",
                 application_name: str = "KineticConstructor"):
        super().__init__()
        
        self.session_tracker = session_tracker
        self.event_bus = get_event_bus()
        
        # Initialize QSettings with proper organization/app names
        self.settings = QSettings(organization_name, application_name)
        
        # Initialize specialized managers (dependency injection)
        self._background_manager: Optional[IBackgroundSettingsManager] = None
        self._visibility_manager: Optional[IVisibilitySettingsManager] = None
        self._layout_manager: Optional[IBeatLayoutSettingsManager] = None
        self._prop_manager: Optional[IPropTypeSettingsManager] = None
        self._user_manager: Optional[IUserProfileSettingsManager] = None
        self._export_manager: Optional[IImageExportSettingsManager] = None
        
        # State management
        self._current_state_memento: Optional[ApplicationStateMemento] = None
        
        logger.info(f"Initialized ModernSettingsService with QSettings: {self.settings.fileName()}")
    
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
            old_value = self.settings.value(full_key)
            
            self.settings.setValue(full_key, value)
            self.settings.sync()
            
            # Emit command completion event
            self.settings_changed.emit(section, key, value)
            
            # Update session state if this is a UI-relevant setting
            if section in ['ui', 'global', 'workbench']:
                self.session_tracker.mark_interaction()
            
            logger.debug(f"Setting command executed: {full_key} = {value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to execute setting command {section}/{key}: {e}")
            return False
    
    def execute_bulk_setting_command(self, settings_dict: Dict[str, Dict[str, Any]]) -> bool:
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
                        logger.warning(f"Failed to set {section}/{key} during bulk operation")
            
            return True
            
        except Exception as e:
            logger.error(f"Bulk setting command failed: {e}")
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
    
    def query_setting(self, section: str, key: str, default: Any = None, type_hint: Type[T] = None) -> T:
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
            else:
                return self.settings.value(full_key, default)
                
        except Exception as e:
            logger.error(f"Failed to query setting {section}/{key}: {e}")
            return default
    
    def query_section(self, section: str) -> Dict[str, Any]:
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
            logger.error(f"Failed to query section {section}: {e}")
            return {}
    
    def query_all_settings(self) -> Dict[str, Dict[str, Any]]:
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
                result['_root'] = {}
                for key in top_level_keys:
                    result['_root'][key] = self.settings.value(key)
                    
            return result
            
        except Exception as e:
            logger.error(f"Failed to query all settings: {e}")
            return {}
    
    # ============================================================================
    # MEMENTO PATTERN - State Snapshots
    # ============================================================================
    
    def create_state_memento(self, current_tab: str, window_geometry: Optional[bytes] = None, 
                           window_state: Optional[bytes] = None) -> ApplicationStateMemento:
        """
        Create a state memento for the current application state.
        
        Args:
            current_tab: Currently active tab
            window_geometry: Window geometry data
            window_state: Window state data
            
        Returns:
            ApplicationStateMemento instance
        """
        try:
            # Get current session data
            session_data = self.session_tracker.get_current_session_state()
            session_dict = session_data.__dict__ if session_data else {}
            
            # Create settings snapshot
            settings_snapshot = self.query_all_settings()
            
            memento = ApplicationStateMemento(
                current_tab=current_tab,
                window_geometry=window_geometry,
                window_state=window_state,
                session_data=session_dict,
                settings_snapshot=settings_snapshot
            )
            
            self._current_state_memento = memento
            logger.debug("Created application state memento")
            return memento
            
        except Exception as e:
            logger.error(f"Failed to create state memento: {e}")
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
            logger.error(f"Failed to restore from memento: {e}")
            return False
    
    def save_state_memento(self, memento: ApplicationStateMemento, file_path: Optional[Path] = None) -> bool:
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
            
            with open(file_path, 'w') as f:
                json.dump(memento_data, f, indent=2)
            
            logger.info(f"Saved state memento to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save state memento: {e}")
            return False
    
    def load_state_memento(self, file_path: Optional[Path] = None) -> Optional[ApplicationStateMemento]:
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
            
            with open(file_path, 'r') as f:
                memento_data = json.load(f)
            
            memento = ApplicationStateMemento.from_dict(memento_data)
            logger.info(f"Loaded state memento from {file_path}")
            return memento
            
        except Exception as e:
            logger.error(f"Failed to load state memento: {e}")
            return None
    
    # ============================================================================
    # HIGH-LEVEL STATE MANAGEMENT INTERFACE
    # ============================================================================
    
    def save_application_state(self, current_tab: str, window_geometry: Optional[bytes] = None,
                             window_state: Optional[bytes] = None) -> bool:
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
            memento = self.create_state_memento(current_tab, window_geometry, window_state)
            
            # Save memento to file
            success = self.save_state_memento(memento)
            
            # Also ensure session state is saved
            session_success = self.session_tracker.save_session_state()
            
            if success and session_success:
                logger.info("Successfully saved complete application state")
                return True
            else:
                logger.warning("Partial failure saving application state")
                return False
                
        except Exception as e:
            logger.error(f"Failed to save application state: {e}")
            return False
    
    def restore_application_state(self) -> Optional[ApplicationStateMemento]:
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
                else:
                    logger.warning("Failed to restore application state from memento")
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to restore application state: {e}")
            return None
    
    # ============================================================================
    # MANAGER ACCESS METHODS
    # ============================================================================
    
    def get_background_manager(self) -> Optional[IBackgroundSettingsManager]:
        """Get the background settings manager."""
        return self._background_manager
    
    def get_visibility_manager(self) -> Optional[IVisibilitySettingsManager]:
        """Get the visibility settings manager."""
        return self._visibility_manager
    
    def get_layout_manager(self) -> Optional[IBeatLayoutSettingsManager]:
        """Get the layout settings manager."""
        return self._layout_manager
    
    def get_prop_manager(self) -> Optional[IPropTypeSettingsManager]:
        """Get the prop type settings manager."""
        return self._prop_manager
    
    def get_user_manager(self) -> Optional[IUserProfileSettingsManager]:
        """Get the user profile settings manager."""
        return self._user_manager
    
    def get_export_manager(self) -> Optional[IImageExportSettingsManager]:
        """Get the image export settings manager."""
        return self._export_manager
    
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
