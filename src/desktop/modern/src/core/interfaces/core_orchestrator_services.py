"""
Core Orchestrator Service Interfaces

Interface definitions for core orchestration services following TKA's clean architecture.
These interfaces handle application lifecycle and coordination operations.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple


class IApplicationOrchestrator(ABC):
    """Interface for application orchestration operations."""

    @abstractmethod
    def initialize_application(
        self, 
        progress_callback: Optional[Callable[[str, int], None]] = None
    ) -> bool:
        """
        Initialize the complete application.

        Args:
            progress_callback: Optional callback for progress updates

        Returns:
            True if initialization succeeded

        Note:
            Web implementation: Handles async initialization and loading
        """
        pass

    @abstractmethod
    def shutdown_application(self) -> bool:
        """
        Gracefully shutdown the application.

        Returns:
            True if shutdown completed successfully

        Note:
            Web implementation: Cleans up resources and saves state
        """
        pass

    @abstractmethod
    def get_initialization_status(self) -> Dict[str, Any]:
        """
        Get current initialization status.

        Returns:
            Status dictionary with initialization progress

        Note:
            Web implementation: Returns loading state for UI feedback
        """
        pass

    @abstractmethod
    def register_shutdown_handler(self, handler: Callable[[], None]) -> str:
        """
        Register shutdown handler.

        Args:
            handler: Function to call during shutdown

        Returns:
            Handler identifier for removal

        Note:
            Web implementation: Uses beforeunload event or similar
        """
        pass

    @abstractmethod
    def unregister_shutdown_handler(self, handler_id: str) -> bool:
        """
        Unregister shutdown handler.

        Args:
            handler_id: Handler identifier from registration

        Returns:
            True if handler was removed

        Note:
            Web implementation: Removes event listener
        """
        pass

    @abstractmethod
    def restart_application(self) -> bool:
        """
        Restart the application.

        Returns:
            True if restart initiated successfully

        Note:
            Web implementation: May reload page or reset application state
        """
        pass


class IApplicationInitializationOrchestrator(ABC):
    """Interface for application initialization orchestration operations."""

    @abstractmethod
    def initialize_services(
        self, 
        container: Any,
        progress_callback: Optional[Callable[[str, int], None]] = None
    ) -> bool:
        """
        Initialize all application services.

        Args:
            container: Dependency injection container
            progress_callback: Optional progress callback

        Returns:
            True if all services initialized successfully

        Note:
            Web implementation: Handles async service initialization
        """
        pass

    @abstractmethod
    def initialize_ui_components(
        self, 
        main_window: Any,
        progress_callback: Optional[Callable[[str, int], None]] = None
    ) -> bool:
        """
        Initialize UI components.

        Args:
            main_window: Main window or root element
            progress_callback: Optional progress callback

        Returns:
            True if UI initialization succeeded

        Note:
            Web implementation: Sets up DOM structure and event handlers
        """
        pass

    @abstractmethod
    def load_user_preferences(self) -> bool:
        """
        Load user preferences and settings.

        Returns:
            True if preferences loaded successfully

        Note:
            Web implementation: Loads from localStorage or server
        """
        pass

    @abstractmethod
    def restore_session_state(self) -> bool:
        """
        Restore previous session state.

        Returns:
            True if session restored successfully

        Note:
            Web implementation: Restores from sessionStorage or server
        """
        pass

    @abstractmethod
    def validate_dependencies(self) -> Tuple[bool, List[str]]:
        """
        Validate all required dependencies.

        Returns:
            Tuple of (all_valid, missing_dependencies)

        Note:
            Web implementation: Checks browser capabilities and resources
        """
        pass

    @abstractmethod
    def get_initialization_order(self) -> List[str]:
        """
        Get the order of initialization steps.

        Returns:
            List of initialization step names in order

        Note:
            Web implementation: May differ from desktop due to async nature
        """
        pass

    @abstractmethod
    def rollback_initialization(self, failed_step: str) -> None:
        """
        Rollback initialization to handle failures.

        Args:
            failed_step: Name of step that failed

        Note:
            Web implementation: Cleans up partially initialized resources
        """
        pass


class IServiceRegistrationManager(ABC):
    """Interface for service registration management operations."""

    @abstractmethod
    def register_core_services(self, container: Any) -> None:
        """
        Register core application services.

        Args:
            container: Dependency injection container

        Note:
            Web implementation: Registers web-compatible service implementations
        """
        pass

    @abstractmethod
    def register_ui_services(self, container: Any) -> None:
        """
        Register UI-related services.

        Args:
            container: Dependency injection container

        Note:
            Web implementation: Registers DOM/browser-specific services
        """
        pass

    @abstractmethod
    def register_data_services(self, container: Any) -> None:
        """
        Register data management services.

        Args:
            container: Dependency injection container

        Note:
            Web implementation: May use different storage backends
        """
        pass

    @abstractmethod
    def register_background_services(self, container: Any) -> None:
        """
        Register background and animation services.

        Args:
            container: Dependency injection container

        Note:
            Web implementation: Registers CSS/WebGL animation services
        """
        pass

    @abstractmethod
    def get_registered_services(self) -> List[str]:
        """
        Get list of registered service names.

        Returns:
            List of service identifiers

        Note:
            Web implementation: Returns service registry information
        """
        pass

    @abstractmethod
    def validate_service_dependencies(self) -> Tuple[bool, List[str]]:
        """
        Validate service dependency chain.

        Returns:
            Tuple of (all_valid, missing_dependencies)

        Note:
            Web implementation: Checks for circular dependencies
        """
        pass

    @abstractmethod
    def unregister_service(self, service_name: str) -> bool:
        """
        Unregister a service.

        Args:
            service_name: Name of service to unregister

        Returns:
            True if service was unregistered

        Note:
            Web implementation: Cleans up service resources
        """
        pass


class IWindowManagementService(ABC):
    """Interface for window management operations."""

    @abstractmethod
    def create_main_window(self, config: Dict[str, Any]) -> Any:
        """
        Create main application window.

        Args:
            config: Window configuration dictionary

        Returns:
            Main window object

        Note:
            Web implementation: Sets up main DOM container or viewport
        """
        pass

    @abstractmethod
    def show_window(self, window: Any) -> None:
        """
        Show window.

        Args:
            window: Window object to show

        Note:
            Web implementation: Sets CSS visibility or display properties
        """
        pass

    @abstractmethod
    def hide_window(self, window: Any) -> None:
        """
        Hide window.

        Args:
            window: Window object to hide

        Note:
            Web implementation: Hides via CSS or removes from DOM
        """
        pass

    @abstractmethod
    def resize_window(self, window: Any, size: Tuple[int, int]) -> None:
        """
        Resize window.

        Args:
            window: Window object to resize
            size: (width, height) dimensions

        Note:
            Web implementation: Updates CSS dimensions
        """
        pass

    @abstractmethod
    def center_window(self, window: Any) -> None:
        """
        Center window on screen.

        Args:
            window: Window object to center

        Note:
            Web implementation: Centers in viewport using CSS
        """
        pass

    @abstractmethod
    def set_window_title(self, window: Any, title: str) -> None:
        """
        Set window title.

        Args:
            window: Window object
            title: Title text

        Note:
            Web implementation: Updates document.title or header element
        """
        pass

    @abstractmethod
    def get_window_geometry(self, window: Any) -> Dict[str, int]:
        """
        Get window geometry.

        Args:
            window: Window object

        Returns:
            Dictionary with x, y, width, height

        Note:
            Web implementation: Returns element bounding box or viewport size
        """
        pass

    @abstractmethod
    def set_window_geometry(
        self, 
        window: Any, 
        geometry: Dict[str, int]
    ) -> None:
        """
        Set window geometry.

        Args:
            window: Window object
            geometry: Dictionary with x, y, width, height

        Note:
            Web implementation: Updates CSS position and dimensions
        """
        pass

    @abstractmethod
    def minimize_window(self, window: Any) -> None:
        """
        Minimize window.

        Args:
            window: Window object to minimize

        Note:
            Web implementation: May hide or reduce to tab/taskbar
        """
        pass

    @abstractmethod
    def maximize_window(self, window: Any) -> None:
        """
        Maximize window.

        Args:
            window: Window object to maximize

        Note:
            Web implementation: Expands to full viewport or container
        """
        pass

    @abstractmethod
    def restore_window(self, window: Any) -> None:
        """
        Restore window from minimized/maximized state.

        Args:
            window: Window object to restore

        Note:
            Web implementation: Restores previous size and position
        """
        pass

    @abstractmethod
    def is_window_maximized(self, window: Any) -> bool:
        """
        Check if window is maximized.

        Args:
            window: Window object to check

        Returns:
            True if window is maximized

        Note:
            Web implementation: Checks CSS or DOM state
        """
        pass

    @abstractmethod
    def is_window_minimized(self, window: Any) -> bool:
        """
        Check if window is minimized.

        Args:
            window: Window object to check

        Returns:
            True if window is minimized

        Note:
            Web implementation: Checks visibility state
        """
        pass

    @abstractmethod
    def save_window_state(self, window: Any) -> Dict[str, Any]:
        """
        Save window state.

        Args:
            window: Window object

        Returns:
            Window state dictionary

        Note:
            Web implementation: Saves to localStorage or session
        """
        pass

    @abstractmethod
    def restore_window_state(
        self, 
        window: Any, 
        state: Dict[str, Any]
    ) -> None:
        """
        Restore window state.

        Args:
            window: Window object
            state: Window state dictionary

        Note:
            Web implementation: Restores from localStorage or session
        """
        pass
