"""
Core Orchestrator Service Interfaces

Interface definitions for core orchestration services following TKA's clean architecture.
These interfaces handle application lifecycle and coordination operations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class IApplicationOrchestrator(ABC):
    """Interface for application orchestration operations."""

    @abstractmethod
    def initialize_application(
        self, progress_callback: Callable[[str, int], None] | None = None
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

    @abstractmethod
    def shutdown_application(self) -> bool:
        """
        Gracefully shutdown the application.

        Returns:
            True if shutdown completed successfully

        Note:
            Web implementation: Cleans up resources and saves state
        """

    @abstractmethod
    def get_initialization_status(self) -> dict[str, Any]:
        """
        Get current initialization status.

        Returns:
            Status dictionary with initialization progress

        Note:
            Web implementation: Returns loading state for UI feedback
        """

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

    @abstractmethod
    def restart_application(self) -> bool:
        """
        Restart the application.

        Returns:
            True if restart initiated successfully

        Note:
            Web implementation: May reload page or reset application state
        """


class IApplicationInitializationOrchestrator(ABC):
    """Interface for application initialization orchestration operations."""

    @abstractmethod
    def initialize_services(
        self,
        container: Any,
        progress_callback: Callable[[str, int], None] | None = None,
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

    @abstractmethod
    def initialize_ui_components(
        self,
        main_window: Any,
        progress_callback: Callable[[str, int], None] | None = None,
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

    @abstractmethod
    def load_user_preferences(self) -> bool:
        """
        Load user preferences and settings.

        Returns:
            True if preferences loaded successfully

        Note:
            Web implementation: Loads from localStorage or server
        """

    @abstractmethod
    def restore_session_state(self) -> bool:
        """
        Restore previous session state.

        Returns:
            True if session restored successfully

        Note:
            Web implementation: Restores from sessionStorage or server
        """

    @abstractmethod
    def validate_dependencies(self) -> tuple[bool, list[str]]:
        """
        Validate all required dependencies.

        Returns:
            Tuple of (all_valid, missing_dependencies)

        Note:
            Web implementation: Checks browser capabilities and resources
        """

    @abstractmethod
    def get_initialization_order(self) -> list[str]:
        """
        Get the order of initialization steps.

        Returns:
            List of initialization step names in order

        Note:
            Web implementation: May differ from desktop due to async nature
        """

    @abstractmethod
    def rollback_initialization(self, failed_step: str) -> None:
        """
        Rollback initialization to handle failures.

        Args:
            failed_step: Name of step that failed

        Note:
            Web implementation: Cleans up partially initialized resources
        """


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

    @abstractmethod
    def register_ui_services(self, container: Any) -> None:
        """
        Register UI-related services.

        Args:
            container: Dependency injection container

        Note:
            Web implementation: Registers DOM/browser-specific services
        """

    @abstractmethod
    def register_data_services(self, container: Any) -> None:
        """
        Register data management services.

        Args:
            container: Dependency injection container

        Note:
            Web implementation: May use different storage backends
        """

    @abstractmethod
    def register_background_services(self, container: Any) -> None:
        """
        Register background and animation services.

        Args:
            container: Dependency injection container

        Note:
            Web implementation: Registers CSS/WebGL animation services
        """

    @abstractmethod
    def get_registered_services(self) -> list[str]:
        """
        Get list of registered service names.

        Returns:
            List of service identifiers

        Note:
            Web implementation: Returns service registry information
        """

    @abstractmethod
    def validate_service_dependencies(self) -> tuple[bool, list[str]]:
        """
        Validate service dependency chain.

        Returns:
            Tuple of (all_valid, missing_dependencies)

        Note:
            Web implementation: Checks for circular dependencies
        """

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


class IWindowManagementService(ABC):
    """Interface for window management operations."""

    @abstractmethod
    def create_main_window(self, config: dict[str, Any]) -> Any:
        """
        Create main application window.

        Args:
            config: Window configuration dictionary

        Returns:
            Main window object

        Note:
            Web implementation: Sets up main DOM container or viewport
        """

    @abstractmethod
    def show_window(self, window: Any) -> None:
        """
        Show window.

        Args:
            window: Window object to show

        Note:
            Web implementation: Sets CSS visibility or display properties
        """

    @abstractmethod
    def hide_window(self, window: Any) -> None:
        """
        Hide window.

        Args:
            window: Window object to hide

        Note:
            Web implementation: Hides via CSS or removes from DOM
        """

    @abstractmethod
    def resize_window(self, window: Any, size: tuple[int, int]) -> None:
        """
        Resize window.

        Args:
            window: Window object to resize
            size: (width, height) dimensions

        Note:
            Web implementation: Updates CSS dimensions
        """

    @abstractmethod
    def center_window(self, window: Any) -> None:
        """
        Center window on screen.

        Args:
            window: Window object to center

        Note:
            Web implementation: Centers in viewport using CSS
        """

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

    @abstractmethod
    def get_window_geometry(self, window: Any) -> dict[str, int]:
        """
        Get window geometry.

        Args:
            window: Window object

        Returns:
            Dictionary with x, y, width, height

        Note:
            Web implementation: Returns element bounding box or viewport size
        """

    @abstractmethod
    def set_window_geometry(self, window: Any, geometry: dict[str, int]) -> None:
        """
        Set window geometry.

        Args:
            window: Window object
            geometry: Dictionary with x, y, width, height

        Note:
            Web implementation: Updates CSS position and dimensions
        """

    @abstractmethod
    def minimize_window(self, window: Any) -> None:
        """
        Minimize window.

        Args:
            window: Window object to minimize

        Note:
            Web implementation: May hide or reduce to tab/taskbar
        """

    @abstractmethod
    def maximize_window(self, window: Any) -> None:
        """
        Maximize window.

        Args:
            window: Window object to maximize

        Note:
            Web implementation: Expands to full viewport or container
        """

    @abstractmethod
    def restore_window(self, window: Any) -> None:
        """
        Restore window from minimized/maximized state.

        Args:
            window: Window object to restore

        Note:
            Web implementation: Restores previous size and position
        """

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

    @abstractmethod
    def save_window_state(self, window: Any) -> dict[str, Any]:
        """
        Save window state.

        Args:
            window: Window object

        Returns:
            Window state dictionary

        Note:
            Web implementation: Saves to localStorage or session
        """

    @abstractmethod
    def restore_window_state(self, window: Any, state: dict[str, Any]) -> None:
        """
        Restore window state.

        Args:
            window: Window object
            state: Window state dictionary

        Note:
            Web implementation: Restores from localStorage or session
        """
