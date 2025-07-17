"""
UI Service Interfaces

Interface definitions for UI-related services following TKA's clean architecture.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Callable

from domain.models.sequence_data import SequenceData
from domain.models.beat_data import BeatData


class IThumbnailGenerationService(ABC):
    """Interface for thumbnail generation operations."""

    @abstractmethod
    def generate_sequence_thumbnail(
        self,
        sequence: SequenceData,
        output_path: Path,
        fullscreen_preview: bool = False,
    ) -> Optional[Path]:
        """
        Generate a thumbnail image for the given sequence.

        Args:
            sequence: The sequence to generate thumbnail for
            output_path: Where to save the thumbnail image
            fullscreen_preview: Whether this is for fullscreen preview (affects quality/options)

        Returns:
            Path to the generated thumbnail, or None if generation failed
        """
        pass


class IUISetupManager(ABC):
    """Interface for UI setup and initialization operations."""

    @abstractmethod
    def setup_main_window(self, window: Any) -> None:
        """
        Setup main window configuration.

        Args:
            window: Main window object to configure
        """
        pass

    @abstractmethod
    def setup_component_layouts(self, container: Any) -> None:
        """
        Setup component layouts within container.

        Args:
            container: Container widget to setup layouts for
        """
        pass

    @abstractmethod
    def apply_theme(self, theme_name: str) -> bool:
        """
        Apply UI theme.

        Args:
            theme_name: Name of theme to apply

        Returns:
            True if theme was applied successfully
        """
        pass

    @abstractmethod
    def get_available_themes(self) -> List[str]:
        """
        Get list of available themes.

        Returns:
            List of theme names
        """
        pass


class ISequenceStateReader(ABC):
    """Interface for reading sequence state information."""

    @abstractmethod
    def get_current_sequence_state(self) -> Dict[str, Any]:
        """
        Get current sequence state.

        Returns:
            Dictionary containing sequence state information
        """
        pass

    @abstractmethod
    def get_beat_state(self, beat_index: int) -> Optional[Dict[str, Any]]:
        """
        Get state for specific beat.

        Args:
            beat_index: Index of beat to get state for

        Returns:
            Beat state dictionary or None if not found
        """
        pass

    @abstractmethod
    def get_selection_state(self) -> Dict[str, Any]:
        """
        Get current selection state.

        Returns:
            Dictionary containing selection state
        """
        pass

    @abstractmethod
    def is_sequence_modified(self) -> bool:
        """
        Check if sequence has been modified.

        Returns:
            True if sequence has unsaved changes
        """
        pass


class IWindowDiscoveryService(ABC):
    """Interface for window discovery operations."""

    @abstractmethod
    def discover_main_window(self) -> Optional[Any]:
        """
        Discover the main application window.

        Returns:
            Main window object or None if not found
        """
        pass

    @abstractmethod
    def discover_child_windows(self, parent_window: Any) -> List[Any]:
        """
        Discover child windows of parent.

        Args:
            parent_window: Parent window to search

        Returns:
            List of child window objects
        """
        pass

    @abstractmethod
    def find_window_by_title(self, title: str) -> Optional[Any]:
        """
        Find window by title.

        Args:
            title: Window title to search for

        Returns:
            Window object or None if not found
        """
        pass

    @abstractmethod
    def find_window_by_class(self, class_name: str) -> Optional[Any]:
        """
        Find window by class name.

        Args:
            class_name: Window class name to search for

        Returns:
            Window object or None if not found
        """
        pass


class IComponentVisibilityManager(ABC):
    """Interface for component visibility management."""

    @abstractmethod
    def set_component_visible(self, component_id: str, visible: bool) -> None:
        """
        Set component visibility.

        Args:
            component_id: Unique identifier for component
            visible: Whether component should be visible
        """
        pass

    @abstractmethod
    def is_component_visible(self, component_id: str) -> bool:
        """
        Check if component is visible.

        Args:
            component_id: Unique identifier for component

        Returns:
            True if component is visible
        """
        pass

    @abstractmethod
    def toggle_component_visibility(self, component_id: str) -> bool:
        """
        Toggle component visibility.

        Args:
            component_id: Unique identifier for component

        Returns:
            New visibility state
        """
        pass

    @abstractmethod
    def get_all_component_states(self) -> Dict[str, bool]:
        """
        Get visibility states for all components.

        Returns:
            Dictionary mapping component IDs to visibility states
        """
        pass

    @abstractmethod
    def show_all_components(self) -> None:
        """Show all components."""
        pass

    @abstractmethod
    def hide_all_components(self) -> None:
        """Hide all components."""
        pass


class ITabStateManager(ABC):
    """Interface for tab state management."""

    @abstractmethod
    def set_active_tab(self, tab_id: str) -> None:
        """
        Set active tab.

        Args:
            tab_id: Unique identifier for tab
        """
        pass

    @abstractmethod
    def get_active_tab(self) -> Optional[str]:
        """
        Get active tab.

        Returns:
            Active tab ID or None if no tab is active
        """
        pass

    @abstractmethod
    def get_tab_state(self, tab_id: str) -> Dict[str, Any]:
        """
        Get state for specific tab.

        Args:
            tab_id: Unique identifier for tab

        Returns:
            Tab state dictionary
        """
        pass

    @abstractmethod
    def set_tab_state(self, tab_id: str, state: Dict[str, Any]) -> None:
        """
        Set state for specific tab.

        Args:
            tab_id: Unique identifier for tab
            state: State data to set
        """
        pass

    @abstractmethod
    def get_all_tab_states(self) -> Dict[str, Dict[str, Any]]:
        """
        Get states for all tabs.

        Returns:
            Dictionary mapping tab IDs to their state dictionaries
        """
        pass


class IHotkeyRegistry(ABC):
    """Interface for hotkey registration and management."""

    @abstractmethod
    def register_hotkey(self, key_combination: str, callback: Callable) -> bool:
        """
        Register a hotkey.

        Args:
            key_combination: Key combination string (e.g., "Ctrl+S")
            callback: Function to call when hotkey is pressed

        Returns:
            True if registration was successful
        """
        pass

    @abstractmethod
    def unregister_hotkey(self, key_combination: str) -> bool:
        """
        Unregister a hotkey.

        Args:
            key_combination: Key combination string

        Returns:
            True if unregistration was successful
        """
        pass

    @abstractmethod
    def handle_key_event(self, key_event: Any) -> bool:
        """
        Handle key event and trigger appropriate callback.

        Args:
            key_event: Key event object

        Returns:
            True if event was handled by a hotkey
        """
        pass

    @abstractmethod
    def get_registered_hotkeys(self) -> Dict[str, str]:
        """
        Get all registered hotkeys.

        Returns:
            Dictionary mapping key combinations to descriptions
        """
        pass

    @abstractmethod
    def is_hotkey_registered(self, key_combination: str) -> bool:
        """
        Check if hotkey is registered.

        Args:
            key_combination: Key combination string

        Returns:
            True if hotkey is registered
        """
        pass


class IWindowStateManager(ABC):
    """Interface for window state management."""

    @abstractmethod
    def save_window_state(self, window_id: str, state: Dict[str, Any]) -> None:
        """
        Save window state.

        Args:
            window_id: Unique identifier for window
            state: State data to save
        """
        pass

    @abstractmethod
    def load_window_state(self, window_id: str) -> Optional[Dict[str, Any]]:
        """
        Load window state.

        Args:
            window_id: Unique identifier for window

        Returns:
            Window state dictionary or None if not found
        """
        pass

    @abstractmethod
    def get_default_window_state(self, window_id: str) -> Dict[str, Any]:
        """
        Get default window state.

        Args:
            window_id: Unique identifier for window

        Returns:
            Default window state dictionary
        """
        pass

    @abstractmethod
    def reset_window_state(self, window_id: str) -> None:
        """
        Reset window state to defaults.

        Args:
            window_id: Unique identifier for window
        """
        pass


class IUILayoutProvider(ABC):
    """
    Interface for UI layout provider operations.
    
    Provides basic UI layout information and component sizing.
    """

    @abstractmethod
    def get_main_window_size(self) -> Any:
        """Get the main window size."""
        pass

    @abstractmethod
    def get_workbench_size(self) -> Any:
        """Get the workbench area size."""
        pass

    @abstractmethod
    def get_picker_size(self) -> Any:
        """Get the option picker size."""
        pass

    @abstractmethod
    def get_layout_ratio(self) -> Tuple[int, int]:
        """Get the layout ratio (workbench:picker)."""
        pass

    @abstractmethod
    def set_layout_ratio(self, ratio: Tuple[int, int]) -> None:
        """Set the layout ratio."""
        pass

    @abstractmethod
    def calculate_component_size(self, component_type: str, parent_size: Any) -> Any:
        """Calculate component size based on parent and type."""
        pass

    @abstractmethod
    def set_main_window_size(self, size: Any) -> None:
        """Set the main window size."""
        pass
