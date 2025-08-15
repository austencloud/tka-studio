"""
Application Orchestrator

Orchestrates application startup using focused services.
Replaces the monolithic KineticConstructorModern with clean architecture.

PROVIDES:
- Complete application initialization pipeline coordination
- Service composition and orchestration
- Clean separation of concerns
- Progress tracking and error handling
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

from PyQt6.QtWidgets import QMainWindow, QTabWidget

from desktop.modern.src.application.services.core.application_lifecycle_manager import (
    ApplicationLifecycleManager,
    IApplicationLifecycleManager,
)
from desktop.modern.src.application.services.core.service_registration_manager import (
    IServiceRegistrationManager,
    ServiceRegistrationManager,
)
from desktop.modern.src.core.dependency_injection.di_container import DIContainer

from ..ui.background_manager import BackgroundManager, IBackgroundManager
from ..ui.ui_setup_manager import IUISetupManager, UISetupManager


class IApplicationOrchestrator(ABC):
    """Interface for application orchestration."""

    @abstractmethod
    def initialize_application(
        self,
        main_window: QMainWindow,
        splash_screen=None,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
        enable_api=True,
    ) -> QTabWidget:
        """Initialize complete application using orchestrated services."""

    @abstractmethod
    def handle_window_resize(self, main_window: QMainWindow) -> None:
        """Handle main window resize events."""

    @abstractmethod
    def cleanup_application(self) -> None:
        """Clean up application resources."""


class ApplicationOrchestrator(IApplicationOrchestrator):
    """
    Orchestrates application initialization using focused services.

    Coordinates service registration, UI setup, background management,
    and application lifecycle. Returns clean, maintainable architecture.
    """

    def __init__(
        self,
        service_manager: IServiceRegistrationManager | None = None,
        ui_manager: IUISetupManager | None = None,
        background_manager: IBackgroundManager | None = None,
        lifecycle_manager: IApplicationLifecycleManager | None = None,
        container: DIContainer | None = None,
    ):
        """Initialize with dependency injection."""
        self.service_manager = service_manager or ServiceRegistrationManager()
        self.ui_manager = ui_manager or UISetupManager()
        self.background_manager = background_manager or BackgroundManager()

        # If no lifecycle manager provided, create one with session service from container
        if lifecycle_manager is None:
            session_service = None
            if container:
                try:
                    from desktop.modern.src.core.interfaces.session_services import (
                        ISessionStateTracker,
                    )

                    session_service = container.resolve(ISessionStateTracker)

                except Exception as e:
                    print(f"⚠️ [ORCHESTRATOR] Could not resolve session service: {e}")

            self.lifecycle_manager = ApplicationLifecycleManager(session_service)
        else:
            self.lifecycle_manager = lifecycle_manager

        # Store references for cleanup
        self.container = None
        self.background_widget = None
        self.tab_widget = None

    def initialize_application(
        self,
        main_window: QMainWindow,
        splash_screen=None,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
    ) -> QTabWidget:
        """Initialize complete application using orchestrated services."""
        # Create progress callback
        progress_callback = self._create_progress_callback(splash_screen)

        # Step 1: Initialize application lifecycle
        self.lifecycle_manager.initialize_application(
            main_window,
            target_screen,
            parallel_mode,
            parallel_geometry,
            progress_callback,
        )

        # Step 2: Configure services
        from desktop.modern.src.core.dependency_injection import get_container

        if progress_callback:
            progress_callback(45, "Configuring dependency injection...")

        self.container = get_container()

        if progress_callback:
            progress_callback(50, "Registering application services...")

        self.service_manager.register_all_services(self.container)

        if progress_callback:
            progress_callback(55, "Services configured")

        # Step 3: Setup UI
        if progress_callback:
            progress_callback(60, "Initializing user interface...")

        self.tab_widget = self.ui_manager.setup_main_ui(
            main_window,
            self.container,
            progress_callback,
            self.lifecycle_manager._session_service,
        )

        # Step 3.5: Trigger deferred session restoration (after UI is ready)
        if progress_callback:
            progress_callback(85, "Restoring session state...")

        self.lifecycle_manager.trigger_deferred_session_restoration()

        # Step 4: Setup background
        if progress_callback:
            progress_callback(90, "Setting up background...")

        self.background_widget = self.background_manager.setup_background(
            main_window, self.container, progress_callback
        )

        if progress_callback:
            progress_callback(100, "Application ready!")

        return self.tab_widget

    def handle_window_resize(self, main_window: QMainWindow) -> None:
        """Handle main window resize events."""
        if self.background_widget:
            self.background_manager.handle_window_resize(
                main_window, self.background_widget
            )

    def cleanup_application(self) -> None:
        """Clean up application resources."""
        if self.background_widget:
            self.background_manager.cleanup_background(self.background_widget)
            self.background_widget = None

    def get_application_status(self) -> dict:
        """Get current application status."""
        return {
            "services_registered": self.container is not None,
            "ui_initialized": self.tab_widget is not None,
            "background_active": self.background_widget is not None,
            "lifecycle_manager_active": True,
        }

    def handle_setting_change(self, key: str, value, main_window: QMainWindow) -> None:
        """Handle settings changes from UI components."""
        print(f"🔧 Setting changed: {key} = {value}")

        # Handle background changes
        if key == "background_type":
            self.background_manager.apply_background_change(main_window, value)

    def get_available_screens(self) -> list:
        """Get available screens for application placement."""
        screen_config = self.lifecycle_manager.validate_screen_configuration()
        return screen_config["screen_geometries"]

    def switch_to_screen(self, main_window: QMainWindow, screen_index: int) -> bool:
        """Switch application to different screen."""
        try:
            from PyQt6.QtGui import QGuiApplication

            screens = QGuiApplication.screens()
            if 0 <= screen_index < len(screens):
                target_screen = screens[screen_index]
                self.lifecycle_manager.set_window_dimensions(
                    main_window, target_screen=target_screen
                )
                return True
            return False
        except Exception as e:
            print(f"⚠️ Failed to switch to screen {screen_index}: {e}")
            return False

    def get_service_status(self) -> dict:
        """Get status of all managed services."""
        return {
            "service_registration": (
                self.service_manager.get_registration_status()
                if hasattr(self.service_manager, "get_registration_status")
                else {"status": "unknown"}
            ),
            "background_settings": self.background_manager.get_background_settings(),
            "application_info": self.lifecycle_manager.get_application_info(),
        }

    def _create_progress_callback(self, splash_screen) -> Callable | None:
        """Create progress callback for splash screen updates."""
        if splash_screen:

            def progress_callback(progress: int, message: str):
                splash_screen.update_progress(progress, message)

            return progress_callback
        return None

    def get_orchestrator_info(self) -> dict:
        """Get information about the orchestrator and its services."""
        return {
            "orchestrator_version": "1.0.0",
            "service_manager": type(self.service_manager).__name__,
            "ui_manager": type(self.ui_manager).__name__,
            "background_manager": type(self.background_manager).__name__,
            "lifecycle_manager": type(self.lifecycle_manager).__name__,
            "container_available": self.container is not None,
        }
