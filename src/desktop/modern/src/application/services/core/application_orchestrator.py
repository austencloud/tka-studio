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

import logging
from abc import ABC, abstractmethod
from typing import Callable, Optional

logger = logging.getLogger(__name__)

from core.dependency_injection.di_container import DIContainer
from PyQt6.QtWidgets import QMainWindow, QTabWidget

from application.services.core.application_initialization_orchestrator import (
    ApplicationInitializationOrchestrator,
    IApplicationInitializationOrchestrator,
)
from application.services.core.service_registration_manager import (
    IServiceRegistrationManager,
    ServiceRegistrationManager,
)

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
                    from core.interfaces.session_services import ISessionStateTracker

                    from application.services.core.session_restoration_coordinator import (
                        ISessionRestorationCoordinator,
                    )
                    from application.services.core.window_management_service import (
                        IWindowManagementService,
                    )

                    window_service = container.resolve(IWindowManagementService)
                    session_coordinator = container.resolve(
                        ISessionRestorationCoordinator
                    )
                    session_service = container.resolve(ISessionStateTracker)

                except Exception as e:
                    logger.error(
                        f"⚠️ [ORCHESTRATOR] Could not resolve all services: {e}"
                    )

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

            # Create window discovery service if needed
            window_discovery_service = None
            try:
                from application.services.ui.window_discovery_service import (
                    IWindowDiscoveryService,
                )

                window_discovery_service = container.resolve(IWindowDiscoveryService)
            except Exception:
                from application.services.ui.window_discovery_service import (
                    WindowDiscoveryService,
                )

                window_discovery_service = WindowDiscoveryService()

            self.lifecycle_manager = ApplicationInitializationOrchestrator(
                window_service,
                session_coordinator,
                window_discovery_service,
                session_service,
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

        # Arrow pooling completely removed - using legacy direct arrow creation approach
        if progress_callback:
            progress_callback(56, "Direct arrow creation ready")

        # PERFORMANCE OPTIMIZATION: Initialize pictograph pool with lazy loading
        try:
            from application.services.pictograph_pool_manager import (
                PictographPoolManager,
            )

            # Initialize the pool using lazy initialization for faster startup
            pool_manager = self.container.resolve(PictographPoolManager)
            pool_manager.initialize_pool(progress_callback=progress_callback, lazy=True)

            if progress_callback:
                progress_callback(59, "Pictograph pool ready (lazy mode)")
        except Exception as e:
            logger.error(f"❌ Failed to initialize pictograph pool: {e}")
            if progress_callback:
                progress_callback(59, "❌ Pictograph pool initialization failed")

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

        # CRITICAL FIX: Do NOT mark startup complete to prevent pool expansion freeze
        # Pool expansion was causing 30+ second delays after "Application ready"
        # The pool will work fine with on-demand creation when needed

        # CRITICAL: Force proper sizing after layout is fully established
        self._trigger_post_layout_sizing(main_window)

        return self.tab_widget

    def _trigger_post_layout_sizing(self, main_window: QMainWindow) -> None:
        """Trigger proper sizing after main window layout is fully established."""
        from PyQt6.QtCore import QTimer

        def force_option_picker_resize():
            """Force option picker to recalculate with proper dimensions."""
            try:
                # Find the construct tab and its option picker
                if hasattr(self, "tab_widget") and self.tab_widget:
                    construct_tab = None
                    for i in range(self.tab_widget.count()):
                        widget = self.tab_widget.widget(i)
                        if hasattr(widget, "layout_manager"):
                            construct_tab = widget
                            break

                    if construct_tab and hasattr(construct_tab, "layout_manager"):
                        layout_manager = construct_tab.layout_manager
                        if hasattr(layout_manager, "picker_stack"):
                            # Get the option picker from the stack
                            option_picker = None
                            for i in range(layout_manager.picker_stack.count()):
                                widget = layout_manager.picker_stack.widget(i)
                                # Check if this widget has sections (direct option picker scroll)
                                if hasattr(widget, "sections"):
                                    option_picker = widget
                                    break
                                # Check if this is a container with an option picker inside
                                elif hasattr(widget, "layout") and widget.layout():
                                    for j in range(widget.layout().count()):
                                        child_item = widget.layout().itemAt(j)
                                        if child_item and child_item.widget():
                                            child_widget = child_item.widget()
                                            # Check if child has sections (OptionPickerScroll)
                                            if hasattr(child_widget, "sections"):
                                                option_picker = child_widget
                                                break
                                            # Check if child has option_picker_scroll (OptionPickerWidget)
                                            elif hasattr(
                                                child_widget, "option_picker_scroll"
                                            ):
                                                scroll_widget = (
                                                    child_widget.option_picker_scroll
                                                )
                                                if hasattr(scroll_widget, "sections"):
                                                    option_picker = scroll_widget
                                                    break
                                    if option_picker:
                                        break

                            if option_picker:
                                option_picker._update_size()
                            else:
                                logger.warning(
                                    "⚠️ [POST-LAYOUT] Option picker not found in stack"
                                )
                        else:
                            logger.warning(
                                "⚠️ [POST-LAYOUT] Picker stack not found in layout manager"
                            )
                    else:
                        logger.warning(
                            "⚠️ [POST-LAYOUT] Construct tab or layout manager not found"
                        )
                else:
                    logger.warning("⚠️ [POST-LAYOUT] Tab widget not available")
            except Exception as e:
                logger.error(
                    f"❌ [POST-LAYOUT] Error forcing option picker resize: {e}"
                )

        # Use a timer to ensure the main window layout is fully processed
        QTimer.singleShot(100, force_option_picker_resize)

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

        def progress_callback(progress: int, message: str):
            if splash_screen:
                splash_screen.update_progress(progress, message)

        return progress_callback
