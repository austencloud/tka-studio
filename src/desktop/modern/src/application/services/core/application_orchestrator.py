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

from abc import ABC, abstractmethod
from typing import Callable, Optional

from application.services.core.application_initialization_orchestrator import (
    ApplicationInitializationOrchestrator,
    IApplicationInitializationOrchestrator,
)
from application.services.core.service_registration_manager import (
    IServiceRegistrationManager,
    ServiceRegistrationManager,
)
from core.dependency_injection.di_container import DIContainer
from presentation.components.ui.splash_screen import SplashScreen
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow, QTabWidget

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


class ApplicationOrchestrator(IApplicationOrchestrator):
    """
    Orchestrates application initialization using focused services.

    Coordinates service registration, UI setup, background management,
    and application lifecycle. Returns clean, maintainable architecture.
    """

    def __init__(
        self,
        service_manager: Optional[IServiceRegistrationManager] = None,
        ui_manager: Optional[IUISetupManager] = None,
        background_manager: Optional[IBackgroundManager] = None,
        lifecycle_manager: Optional[IApplicationInitializationOrchestrator] = None,
        container: Optional[DIContainer] = None,
    ):
        """Initialize with dependency injection."""
        self.service_manager = service_manager or ServiceRegistrationManager()
        self.ui_manager = ui_manager or UISetupManager()
        self.background_manager = background_manager or BackgroundManager()

        # If no lifecycle manager provided, create one with dependencies from container
        if lifecycle_manager is None:
            # Try to resolve dependencies from container
            window_service = None
            session_coordinator = None
            session_service = None

            if container:
                try:
                    from application.services.core.session_restoration_coordinator import (
                        ISessionRestorationCoordinator,
                    )
                    from application.services.core.window_management_service import (
                        IWindowManagementService,
                    )
                    from core.interfaces.session_services import ISessionStateTracker

                    window_service = container.resolve(IWindowManagementService)
                    session_coordinator = container.resolve(
                        ISessionRestorationCoordinator
                    )
                    session_service = container.resolve(ISessionStateTracker)

                except Exception as e:
                    print(f"⚠️ [ORCHESTRATOR] Could not resolve all services: {e}")

            # Create with available services (fallback to defaults if needed)
            if not window_service:
                from application.services.core.window_management_service import (
                    WindowManagementService,
                )

                window_service = WindowManagementService()

            if not session_coordinator:
                from application.services.core.session_restoration_coordinator import (
                    SessionRestorationCoordinator,
                )

                session_coordinator = SessionRestorationCoordinator()

            self.lifecycle_manager = ApplicationInitializationOrchestrator(
                window_service, session_coordinator, session_service
            )
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
        from core.dependency_injection.di_container import get_container

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
            self.lifecycle_manager.session_service,
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

    def _create_progress_callback(
        self, splash_screen: "SplashScreen"
    ) -> Optional[Callable]:
        """Create progress callback for splash screen updates."""
        if splash_screen:

            def progress_callback(progress: int, message: str):
                splash_screen.update_progress(progress, message)

            return progress_callback
        return None
