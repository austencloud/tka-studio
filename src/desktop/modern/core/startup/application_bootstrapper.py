"""
Application Bootstrapper for TKA Application

Handles application initialization sequence, dependency injection, and startup coordination.
Extracted from main.py to follow Single Responsibility Principle.

This class centralizes all application bootstrapping concerns including:
- Dependency injection container creation
- Service initialization coordination
- Application lifecycle management
- Splash screen coordination
- Main window creation and setup
"""

import logging
from typing import Optional

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from desktop.modern.core.application.application_factory import ApplicationFactory
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.error_handling import StandardErrorHandler

from .configuration_manager import ApplicationConfiguration
from .qt_application_manager import QtApplicationManager


class ApplicationBootstrapper:
    """
    Manages application initialization sequence and startup coordination.

    Provides centralized bootstrapping logic to replace scattered initialization
    code throughout main.py.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._container: Optional[DIContainer] = None
        self._qt_manager: Optional[QtApplicationManager] = None

    def bootstrap_application(
        self, config: ApplicationConfiguration
    ) -> Optional[DIContainer]:
        """
        Bootstrap the complete application based on configuration.

        Args:
            config: Application configuration

        Returns:
            DIContainer: For headless/test modes, None for UI modes

        Raises:
            BootstrapError: If critical initialization fails
        """
        try:
            self.logger.info(f"🚀 Bootstrapping TKA application in {config.mode} mode")

            # Create dependency injection container
            self._container = self._create_container(config)

            # Initialize services
            self._initialize_services()

            # Handle mode-specific bootstrapping
            if config.mode == "test":
                return self._bootstrap_test_mode(config)
            else:
                return self._bootstrap_ui_mode(config)

        except Exception as e:
            StandardErrorHandler.handle_initialization_error(
                "Application bootstrapping",
                e,
                self.logger,
                is_critical=True,
                suggested_action="Check configuration and dependencies",
            )
            raise

    def _create_container(self, config: ApplicationConfiguration) -> DIContainer:
        """Create and configure dependency injection container."""
        try:
            container = ApplicationFactory.create_app(config.mode)
            self.logger.debug(f"✅ Created DI container for {config.mode} mode")
            return container

        except Exception as e:
            StandardErrorHandler.handle_initialization_error(
                "DI container creation", e, self.logger, is_critical=True
            )
            raise

    def _initialize_services(self) -> None:
        """Initialize event-driven architecture services."""
        try:
            from desktop.modern.core.service_locator import initialize_services

            if not initialize_services():
                self.logger.warning(
                    "⚠️ Failed to initialize event-driven services - falling back to legacy architecture"
                )
            else:
                self.logger.info("✅ Event-driven services initialized successfully")

        except Exception as e:
            self.logger.error(f"❌ Error initializing event-driven services: {e}")
            self.logger.warning("⚠️ Continuing with legacy architecture")

    def _bootstrap_test_mode(self, config: ApplicationConfiguration) -> DIContainer:
        """Bootstrap application for test mode."""
        self.logger.info(f"✅ {config.mode.title()} mode - application ready")

        if config.mode == "test":
            available_services = list(self._container.get_registrations().keys())
            self.logger.info(f"📋 Available services: {available_services}")

        return self._container

    def _bootstrap_ui_mode(self, config: ApplicationConfiguration) -> None:
        """Bootstrap application for UI modes (production/recording)."""
        try:
            # Create Qt application manager
            self._qt_manager = QtApplicationManager()
            qt_app = self._qt_manager.create_qt_application(config)

            # Set up UI with splash screen
            self._setup_ui_with_splash(config, qt_app)

            # Run Qt event loop
            exit_code = self._qt_manager.run_event_loop()
            return exit_code

        except Exception as e:
            StandardErrorHandler.handle_initialization_error(
                "UI mode bootstrapping", e, self.logger, is_critical=True
            )
            raise

    def _setup_ui_with_splash(
        self, config: ApplicationConfiguration, qt_app: QApplication
    ) -> None:
        """Set up UI components with splash screen coordination."""
        try:
            # Import splash screen when needed
            from desktop.modern.presentation.components.ui.splash_screen import (
                SplashScreen,
            )

            target_screen = self._qt_manager._target_screen

            # Create and show splash screen
            splash = SplashScreen(target_screen=target_screen)
            fade_in_animation = splash.show_animated()

            # Set up initialization sequence
            def start_initialization():
                try:
                    splash.update_progress(5, "Initializing application...")
                    qt_app.processEvents()

                    # Small delay to ensure splash is visible
                    QTimer.singleShot(
                        50,
                        lambda: self._continue_initialization(
                            config, splash, target_screen
                        ),
                    )

                except Exception as e:
                    self.logger.error(f"Failed to start initialization: {e}")
                    import traceback

                    traceback.print_exc()

            # Connect splash animation to initialization
            fade_in_animation.finished.connect(start_initialization)

            # Handle test generation if requested
            if config.test_generation:
                self._schedule_test_generation()

        except Exception as e:
            StandardErrorHandler.handle_initialization_error(
                "UI setup with splash", e, self.logger, is_critical=True
            )
            raise

    def _continue_initialization(
        self, config: ApplicationConfiguration, splash, target_screen
    ) -> None:
        """Continue initialization after splash screen is shown."""
        try:
            from desktop.modern.main import TKAMainWindow

            splash.update_progress(
                15, "Creating main window and loading all components..."
            )
            QApplication.instance().processEvents()

            # Create main window
            window = TKAMainWindow(
                container=self._container,
                splash_screen=splash,
                target_screen=target_screen,
                parallel_mode=config.parallel_testing,
                parallel_geometry=config.geometry,
            )

            # Complete startup
            self._complete_startup(splash, window)

        except Exception as e:
            self.logger.error(f"Failed to continue initialization: {e}")
            import traceback

            traceback.print_exc()

    def _complete_startup(self, splash, window) -> None:
        """Complete the startup sequence."""
        try:
            splash.update_progress(100, "Application ready!")
            QApplication.instance().processEvents()

            # Show main window
            window.show()
            window.raise_()
            window.activateWindow()

            # Hide splash screen
            splash.hide_animated()

            self.logger.info("✅ Application startup completed successfully")

        except Exception as e:
            self.logger.error(f"Failed to complete startup: {e}")

    def _schedule_test_generation(self) -> None:
        """Schedule test generation to run after initialization."""

        def run_tests_after_init():
            try:
                from test_generation_simple import test_generation_functionality

                test_success = test_generation_functionality()
                if not test_success:
                    self.logger.error("❌ Generation tests failed!")
                else:
                    self.logger.info("✅ Generation tests completed successfully")

            except Exception as e:
                self.logger.error(f"❌ Failed to run generation tests: {e}")
                import traceback

                traceback.print_exc()

        # Run tests after a short delay to ensure app is fully initialized
        QTimer.singleShot(2000, run_tests_after_init)
