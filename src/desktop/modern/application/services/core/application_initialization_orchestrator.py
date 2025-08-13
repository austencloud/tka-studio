"""
Application Initialization Orchestrator

High-level service for coordinating application initialization.
Extracted from ApplicationLifecycleManager to follow single responsibility principle.

PROVIDES:
- High-level application initialization coordination
- Progress callback management
- Application metadata management
- Service composition and coordination
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable

from PyQt6.QtWidgets import QMainWindow

from desktop.modern.application.services.core.session_restoration_coordinator import (
    ISessionRestorationCoordinator,
)
from desktop.modern.application.services.core.window_management_service import (
    IWindowManagementService,
)
from desktop.modern.application.services.ui.window_discovery_service import (
    IWindowDiscoveryService,
)
from desktop.modern.core.interfaces.session_services import ISessionStateTracker


class IApplicationInitializationOrchestrator(ABC):
    """Interface for application initialization orchestration."""

    @abstractmethod
    def initialize_application(
        self,
        main_window: QMainWindow,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
        progress_callback: Callable | None = None,
    ) -> None:
        """Initialize application with proper lifecycle management."""

    @abstractmethod
    def cleanup_application(self) -> None:
        """Cleanup application resources."""

    @abstractmethod
    def get_application_info(self) -> dict:
        """Get application information and status."""


class ApplicationInitializationOrchestrator(IApplicationInitializationOrchestrator):
    """
    High-level service for coordinating application initialization.

    Composes other services to handle the complete application initialization process
    without implementing specific logic directly.
    """

    def __init__(
        self,
        window_service: IWindowManagementService,
        session_coordinator: ISessionRestorationCoordinator,
        window_discovery_service: IWindowDiscoveryService,
        session_service: ISessionStateTracker | None = None,
    ):
        """Initialize application initialization orchestrator."""
        self.window_service = window_service
        self.session_coordinator = session_coordinator
        self.window_discovery_service = window_discovery_service
        self.session_service = session_service
        self.api_enabled = True

    def initialize_application(
        self,
        main_window: QMainWindow,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
        progress_callback: Callable | None = None,
    ) -> None:
        """Initialize application with proper lifecycle management."""
        if progress_callback:
            progress_callback(10, "Initializing application lifecycle...")

        # Register main window with discovery service for size provider functionality
        self.window_discovery_service.register_main_window(main_window)

        # Set window title based on mode
        if parallel_mode:
            main_window.setWindowTitle("TKA Modern - Parallel Testing")
        else:
            main_window.setWindowTitle("🚀 Kinetic Constructor")

        if progress_callback:
            progress_callback(30, "Setting window dimensions...")

        # Set window dimensions using window management service
        self.window_service.set_window_dimensions(
            main_window, target_screen, parallel_mode, parallel_geometry
        )

        if progress_callback:
            progress_callback(60, "Preparing session restoration...")

        # Load session state if available using session coordinator
        if self.session_service:
            self.session_coordinator.load_and_prepare_session(self.session_service)

        if progress_callback:
            progress_callback(85, "Session restoration prepared...")

        if progress_callback:
            progress_callback(95, "Application lifecycle initialized")

    def trigger_deferred_session_restoration(self) -> None:
        """Trigger deferred session restoration after UI components are ready."""
        self.session_coordinator.trigger_deferred_restoration_if_pending()

    def cleanup_application(self) -> None:
        """Cleanup application resources."""
        # Currently no cleanup needed, but provides extension point

    def get_application_info(self) -> dict:
        """Get application information and status."""
        screen_info = self.window_service.validate_screen_configuration()

        return {
            "api_enabled": self.api_enabled,
            "session_service_available": self.session_service is not None,
            "screen_configuration": screen_info,
            "services": {
                "window_management": type(self.window_service).__name__,
                "session_coordination": type(self.session_coordinator).__name__,
            },
        }

    def set_session_service(self, session_service: ISessionStateTracker) -> None:
        """Set the session service for lifecycle integration."""
        self.session_service = session_service

    # Delegate window management methods for backward compatibility
    def set_window_dimensions(
        self,
        main_window: QMainWindow,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
    ) -> None:
        """Delegate to window management service."""
        self.window_service.set_window_dimensions(
            main_window, target_screen, parallel_mode, parallel_geometry
        )

    def determine_target_screen(self, parallel_mode=False, monitor=""):
        """Delegate to window management service."""
        return self.window_service.determine_target_screen(parallel_mode, monitor)

    def validate_screen_configuration(self) -> dict:
        """Delegate to window management service."""
        return self.window_service.validate_screen_configuration()
