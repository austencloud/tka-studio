#!/usr/bin/env python3
"""
Kinetic Constructor - Main Application Entry Point

Modified to support different application modes via Application Factory.
Modern modular architecture with dependency injection and clean separation of concerns.
"""

# CRITICAL: Path setup MUST be first - before any other imports
# This ensures VS Code debugger can find all modules
import sys
from pathlib import Path

# Check if tka_paths has already been imported (e.g., from root main.py)
if "tka_paths" not in sys.modules:
    # Only do manual path setup if tka_paths hasn't been imported
    # Get the TKA project root (3 levels up from this file)
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[2]  # main.py -> modern -> desktop -> TKA

    # Define the same paths as root main.py - MUST match exactly
    src_paths = [
        project_root
        / "src"
        / "desktop"
        / "modern"
        / "src",  # Modern src (highest priority)
        project_root / "src" / "desktop",  # Desktop directory
        project_root / "src",  # Shared src (lowest priority)
        project_root / "launcher",
        project_root / "packages",
    ]

    # Add paths in reverse order since insert(0) puts them at the beginning
    for path in reversed(src_paths):
        if path.exists() and str(path) not in sys.path:
            sys.path.insert(0, str(path))

    print(
        f"[PATH_SETUP] Added {len([p for p in src_paths if p.exists()])} paths for VS Code debugger compatibility"
    )
    print(f"[PATH_SETUP] First 5 sys.path entries:")
    for i, path in enumerate(sys.path[:5]):
        print(f"  {i}: {path}")
else:
    print("🔧 [PATH_SETUP] Skipping manual path setup - tka_paths already imported")

# Now safe to import everything else
import argparse
import logging
import os
from typing import TYPE_CHECKING, Optional

# Path setup is now handled at the top of the file


if TYPE_CHECKING:
    from desktop.modern.presentation.components.ui.splash_screen import SplashScreen
    from desktop.modern.core.application.application_factory import ApplicationMode

from PyQt6.QtCore import QTimer, QtMsgType, qInstallMessageHandler
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget


def _install_qt_message_handler():
    """Install Qt message handler to suppress CSS property warnings and other noise."""

    def qt_message_handler(msg_type, context, message):
        # ULTRA-AGGRESSIVE SUPPRESSION: Block ALL CSS and styling warnings to eliminate processing overhead
        suppressed_patterns = [
            "unknown property",
            "text-shadow",
            "transform",
            "transition",
            "box-shadow",
            "backdrop-filter",
            "qobject::setparent",
            "qbasictimer",
            "timers cannot be started",
            "different thread",
            "qwidget",
            "qpainter",
            "stylesheet",
            "css",
            "style",
            "font",
            "color",
            "border",
            "margin",
            "padding",
            "background",
            "qml",
            "opengl",
            "shader",
            "texture",
            "pixmap",
            "image",
        ]

        message_lower = message.lower()
        if any(pattern in message_lower for pattern in suppressed_patterns):
            return  # Completely suppress these messages to eliminate processing overhead

        # Only show critical errors
        if msg_type == QtMsgType.QtCriticalMsg or msg_type == QtMsgType.QtFatalMsg:
            print(f"Qt {msg_type.name}: {message}")

    qInstallMessageHandler(qt_message_handler)


class TKAMainWindow(QMainWindow):
    def __init__(
        self,
        container=None,
        splash_screen: Optional["SplashScreen"] = None,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
    ):
        super().__init__()

        # Hide window immediately to prevent temporary flash
        self.hide()

        self.container = container
        self.splash = splash_screen
        self.target_screen = target_screen
        self.parallel_mode = parallel_mode
        self.parallel_geometry = parallel_geometry

        # 🚀 Initialize Modern State Persistence System
        self._setup_modern_state_persistence()

        if self.container:
            from desktop.modern.application.services.core.application_orchestrator import (
                ApplicationOrchestrator,
            )

            # Create orchestrator with default services (it will create its own lifecycle manager)
            self.orchestrator = ApplicationOrchestrator()
            self.tab_widget = self.orchestrator.initialize_application(
                self,
                splash_screen,
                target_screen,
                parallel_mode,
                parallel_geometry,
            )
            
            # Connect tab changes to state persistence
            self._connect_state_persistence_events()
            
            # Create simple settings service for tab restoration
            try:
                from desktop.modern.core.dependency_injection.settings_service_registration import create_configured_settings_container
                from desktop.modern.application.services.settings.modern_settings_service import ModernSettingsService
                
                # Create a minimal settings container just for tab state
                if not hasattr(self, 'settings_service'):
                    settings_container = create_configured_settings_container("TKA", "KineticConstructor")
                    self.settings_service = settings_container.resolve(ModernSettingsService)
                    print("✅ Created minimal settings service for tab restoration")
                    
            except Exception as e:
                print(f"⚠️ Failed to create settings service: {e}")
            
            # Restore the last active tab after everything is set up
            if hasattr(self, 'tab_widget') and self.tab_widget:
                self._restore_tab_state()

    def _setup_modern_state_persistence(self) -> None:
        """Set up the modern state persistence system."""
        try:
            print(f"🔍 DEBUG: Starting state persistence setup. Container: {self.container}")
            
            from desktop.modern.core.dependency_injection.settings_service_registration import create_configured_settings_container
            from desktop.modern.application.services.core.application_state_manager import integrate_with_application_startup
            from desktop.modern.application.services.settings.modern_settings_service import ModernSettingsService
            
            # Create DI container with all settings services
            self.settings_container = create_configured_settings_container("TKA", "KineticConstructor")
            print(f"🔍 DEBUG: Created settings container: {self.settings_container}")
            
            # Get the settings service for immediate use
            self.settings_service = self.settings_container.resolve(ModernSettingsService)
            print(f"🔍 DEBUG: Resolved settings service: {self.settings_service}")
            
            # Integrate with Qt application lifecycle
            self.state_manager = integrate_with_application_startup(
                self.settings_container, 
                self,  # main window
                QApplication.instance()  # Qt app
            )
            print(f"🔍 DEBUG: Created state manager: {self.state_manager}")
            
            print("✅ Modern state persistence system activated!")
            
            # Restore the previously active tab
            self._restore_tab_state()
            
        except Exception as e:
            print(f"⚠️ Failed to initialize modern state persistence: {e}")
            import traceback
            traceback.print_exc()
            # Continue without state persistence rather than crash
            self.settings_container = None
            self.settings_service = None
            self.state_manager = None

    def _connect_state_persistence_events(self) -> None:
        """Connect UI events to state persistence system."""
        try:
            if not hasattr(self, 'state_manager') or not self.state_manager:
                return
                
            # Connect tab widget changes if available
            if hasattr(self, 'tab_widget') and self.tab_widget:
                # Connect tab change events with proper state saving
                if hasattr(self.tab_widget, 'currentChanged'):
                    self.tab_widget.currentChanged.connect(self._on_tab_changed)
                    
                # Connect other tab widget events if they exist
                if hasattr(self.tab_widget, 'tabBarClicked'):
                    self.tab_widget.tabBarClicked.connect(
                        lambda: self.state_manager.mark_user_interaction("tab_click")
                    )
                    
            print("🔗 Connected state persistence events to UI")
            
        except Exception as e:
            print(f"⚠️ Failed to connect state persistence events: {e}")

    def _on_tab_changed(self, index):
        """Handle tab change events and save current tab state."""
        try:
            if hasattr(self, 'settings_service') and self.settings_service:
                # Save current tab index and name
                self.settings_service.execute_setting_command("ui_state", "current_tab_index", index)
                
                # Also save tab name for human-readable restoration
                if hasattr(self, 'tab_widget') and self.tab_widget:
                    tab_name = self.tab_widget.tabText(index)
                    self.settings_service.execute_setting_command("ui_state", "current_tab_name", tab_name)
                    print(f"💾 Saved tab state: index={index}, name='{tab_name}'")
            
            # Mark user interaction for auto-save
            if hasattr(self, 'state_manager') and self.state_manager:
                self.state_manager.mark_user_interaction("tab_change")
                
        except Exception as e:
            print(f"⚠️ Failed to save tab state: {e}")

    def _restore_tab_state(self):
        """Restore the previously active tab on application startup."""
        try:
            if not hasattr(self, 'settings_service') or not self.settings_service:
                print("⚠️ No settings service available for tab restoration")
                return
                
            if not hasattr(self, 'tab_widget') or not self.tab_widget:
                print("⚠️ No tab widget available for tab restoration")
                return
            
            # Get the last saved tab index
            saved_tab_index = self.settings_service.query_setting("ui_state", "current_tab_index", 0)
            saved_tab_name = self.settings_service.query_setting("ui_state", "current_tab_name", "")
            
            print(f"� Restoring tab: index={saved_tab_index}, name='{saved_tab_name}'")
            
            # Validate the tab index is within bounds
            if 0 <= saved_tab_index < self.tab_widget.count():
                self.tab_widget.setCurrentIndex(saved_tab_index)
                
                # Update navigation buttons to match the restored tab
                self._update_navigation_buttons_for_restored_tab(saved_tab_index)
                
                print(f"✅ Tab restoration complete: {saved_tab_name}")
            else:
                print(f"⚠️ Invalid tab index {saved_tab_index}, keeping default tab")
                
        except Exception as e:
            print(f"⚠️ Failed to restore tab state: {e}")
            import traceback
            traceback.print_exc()

    def _update_navigation_buttons_for_restored_tab(self, tab_index: int):
        """Update navigation buttons to reflect the restored tab."""
        try:
            # Map tab index to tab name
            tab_names = ["construct", "browse", "learn", "sequence_card"]
            if 0 <= tab_index < len(tab_names):
                tab_name = tab_names[tab_index]
                
                # Find the menu bar widget by searching children
                menu_bar = self._find_menu_bar_widget()
                if menu_bar:
                    menu_bar.set_active_tab(tab_name)
                    print(f"🎯 Navigation buttons updated for {tab_name} tab")
                    
        except Exception as e:
            print(f"⚠️ Failed to update navigation buttons: {e}")
            
    def _find_menu_bar_widget(self):
        """Find the menu bar widget by searching through child widgets."""
        try:
            from desktop.modern.presentation.components.menu_bar.menu_bar_widget import MenuBarWidget
            
            # Search through all child widgets recursively
            def find_widget_of_type(parent, widget_type):
                if isinstance(parent, widget_type):
                    return parent
                for child in parent.findChildren(widget_type):
                    return child
                return None
                
            return find_widget_of_type(self, MenuBarWidget)
            
        except Exception as e:
            print(f"⚠️ Error finding menu bar: {e}")
            return None

    def get_settings_service(self):
        """Get the modern settings service for use by other components."""
        return getattr(self, 'settings_service', None)

    def _attach_production_debugger(self) -> None:
        try:
            from debug import attach_to_application, get_production_debugger
            from PyQt6.QtCore import QTimer

            QTimer.singleShot(1000, lambda: self._do_debugger_attachment())
        except Exception:
            pass

    def _do_debugger_attachment(self) -> None:
        try:
            from debug import attach_to_application, get_production_debugger

            attach_to_application(self)
        except Exception:
            import traceback

            traceback.print_exc()

    def show(self):
        """Override show to ensure tab widget is properly displayed."""
        super().show()
        
        # Mark user interaction for state persistence
        if hasattr(self, 'state_manager') and self.state_manager:
            self.state_manager.mark_user_interaction("window_show")
        
        # WINDOW MANAGEMENT FIX: Ensure tab widget is shown when main window is shown
        if hasattr(self, "tab_widget") and self.tab_widget:
            self.tab_widget.show()
            self.tab_widget.setVisible(True)
            # Also show the current tab
            current_tab = self.tab_widget.currentWidget()
            if current_tab:
                current_tab.show()
                current_tab.setVisible(True)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        
        # Mark user interaction for state persistence
        if hasattr(self, 'state_manager') and self.state_manager:
            self.state_manager.mark_user_interaction("window_resize")
            
        if hasattr(self, "orchestrator"):
            self.orchestrator.handle_window_resize(self)


def detect_parallel_testing_mode():
    import argparse
    import os

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--parallel-testing", action="store_true")
    parser.add_argument("--monitor", choices=["primary", "secondary", "left", "right"])
    args, _ = parser.parse_known_args()

    env_parallel = os.environ.get("TKA_PARALLEL_TESTING", "").lower() == "true"
    env_monitor = os.environ.get("TKA_PARALLEL_MONITOR", "")
    env_geometry = os.environ.get("TKA_PARALLEL_GEOMETRY", "")

    parallel_mode = args.parallel_testing or env_parallel
    monitor = args.monitor or env_monitor

    return parallel_mode, monitor, env_geometry


def create_application():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        # PERFORMANCE OPTIMIZATION: Install Qt message handler to suppress CSS warnings
        _install_qt_message_handler()

    # Create container for dependency injection
    from desktop.modern.core.application.application_factory import (
        ApplicationFactory,
        ApplicationMode,
    )

    container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

    # Initialize services
    try:
        from desktop.modern.core.service_locator import initialize_services

        initialize_services()
    except Exception as e:
        print(f"Warning: Could not initialize services: {e}")

    parallel_mode, monitor, geometry = detect_parallel_testing_mode()
    screens = QGuiApplication.screens()
    if parallel_mode and monitor == "secondary" and len(screens) > 1:
        target_screen = screens[1]
    elif parallel_mode and monitor == "primary":
        target_screen = screens[0]
    else:
        target_screen = (
            screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
        )

    window = TKAMainWindow(
        container=container,
        splash_screen=None,
        target_screen=target_screen,
        parallel_mode=parallel_mode,
        parallel_geometry=geometry,
    )

    return app, window


def main():
    """Main entry point with support for different application modes."""

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Import ApplicationMode when needed
    from desktop.modern.core.application.application_factory import ApplicationMode

    # INSTANT FIX: Suppress verbose arrow positioning logs
    try:
        from desktop.modern.core.logging.instant_fix import apply_instant_fix

        apply_instant_fix("quiet")

    except Exception as e:
        logger.warning(
            f"⚠️ Could not apply logging fix: {e} - continuing with default logging"
        )

    # Determine application mode from command line arguments
    app_mode = ApplicationMode.PRODUCTION

    if "--test" in sys.argv:
        app_mode = ApplicationMode.TEST
        # For test mode, just create container and return it
        from desktop.modern.core.application.application_factory import (
            ApplicationFactory,
        )

        container = ApplicationFactory.create_app(app_mode)

        # Initialize services for test mode too
        try:
            from desktop.modern.core.service_locator import initialize_services

            initialize_services()
            logger.info("✅ Event-driven services initialized for test mode")
        except Exception as e:
            logger.warning(
                f"⚠️ Could not initialize event-driven services in test mode: {e}"
            )

        logger.info(f"Test mode - application ready for automated testing")
        logger.info(f"Available services: {list(container.get_registrations().keys())}")
        return container
    elif "--headless" in sys.argv:
        app_mode = ApplicationMode.HEADLESS
        # For headless mode, create container but no UI
        from desktop.modern.core.application.application_factory import (
            ApplicationFactory,
        )

        container = ApplicationFactory.create_app(app_mode)

        # Initialize services for headless mode too
        try:
            from desktop.modern.core.service_locator import initialize_services

            initialize_services()
            logger.info("✅ Event-driven services initialized for headless mode")
        except Exception as e:
            logger.warning(
                f"⚠️ Could not initialize event-driven services in headless mode: {e}"
            )

        logger.info("Headless mode - application ready for server-side processing")
        return container
    elif "--record" in sys.argv:
        app_mode = ApplicationMode.RECORDING
    # For production and recording modes, continue with UI setup
    try:
        # Lazy import ApplicationFactory when needed
        from desktop.modern.core.application.application_factory import (
            ApplicationFactory,
        )

        # Create application using factory
        container = ApplicationFactory.create_app(app_mode)

        # Initialize event-driven architecture services
        try:
            from desktop.modern.core.service_locator import initialize_services

            if not initialize_services():
                logger.warning(
                    "⚠️ Failed to initialize event-driven services - falling back to legacy architecture"
                )
        except Exception as e:
            logger.error(f"❌ Error initializing event-driven services: {e}")
            logger.warning("⚠️ Continuing with legacy architecture")

        # Continue with existing UI setup for production mode
        parallel_mode, monitor, geometry = detect_parallel_testing_mode()
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        # PERFORMANCE OPTIMIZATION: Install Qt message handler to suppress CSS warnings
        _install_qt_message_handler()

        # PERFORMANCE OPTIMIZATION: Apply aggressive startup silencing
        screens = QGuiApplication.screens()

        if parallel_mode and len(screens) > 1:
            if monitor in ["secondary", "right"]:
                primary_screen = screens[0]
                secondary_screen = screens[1]
                if secondary_screen.geometry().x() > primary_screen.geometry().x():
                    target_screen = secondary_screen
                else:
                    target_screen = primary_screen
            elif monitor in ["primary", "left"]:
                primary_screen = screens[0]
                secondary_screen = screens[1]
                if secondary_screen.geometry().x() < primary_screen.geometry().x():
                    target_screen = secondary_screen
                else:
                    target_screen = primary_screen
            else:
                target_screen = screens[1]
        else:
            target_screen = (
                screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
            )

        # Lazy import splash screen when needed
        from desktop.modern.presentation.components.ui.splash_screen import SplashScreen

        # UI setup with splash screen
        splash = SplashScreen(target_screen=target_screen)
        fade_in_animation = splash.show_animated()
        window = None

        def start_initialization():
            nonlocal window
            try:
                # Give splash screen time to fully appear
                splash.update_progress(5, "Initializing application...")
                app.processEvents()

                # Small delay to ensure splash is visible before heavy operations
                QTimer.singleShot(50, lambda: continue_initialization())

            except Exception:
                import traceback

                traceback.print_exc()
                return

        def continue_initialization():
            nonlocal window
            try:
                splash.update_progress(10, "Loading application icon...")
                app.processEvents()
                icon_path = Path(__file__).parent / "images" / "icons" / "app_icon.png"
                if icon_path.exists():
                    app.setWindowIcon(QIcon(str(icon_path)))

                splash.update_progress(
                    15, "Creating main window and loading all components..."
                )
                app.processEvents()

                splash.update_progress(
                    15, "Creating main window and loading all components..."
                )

                window = TKAMainWindow(
                    container=container,
                    splash_screen=splash,
                    target_screen=target_screen,
                    parallel_mode=parallel_mode,
                    parallel_geometry=geometry,
                )

                # Process events to ensure hide takes effect
                app.processEvents()

                complete_startup()
            except Exception:
                import traceback

                traceback.print_exc()
                return

        def complete_startup():
            if window is None:
                return
            splash.update_progress(100, "Application ready!")
            app.processEvents()

            def show_main_window():
                """Show main window exactly when splash finishes fading."""
                window.show()
                window.raise_()
                window.activateWindow()

            # TEMPORARY FIX: Show window immediately for debugging
            show_main_window()

            # Also hide splash screen with callback
            splash.hide_animated()

        fade_in_animation.finished.connect(start_initialization)

        # Run generation tests if requested
        if "--test-generation" in sys.argv:

            def run_tests_after_init():
                try:
                    from test_generation_simple import test_generation_functionality

                    test_success = test_generation_functionality()
                    if not test_success:
                        print("❌ Generation tests failed!")
                except Exception as e:
                    print(f"❌ Failed to run generation tests: {e}")
                    import traceback

                    traceback.print_exc()

            # Run tests after a short delay to ensure app is fully initialized
            QTimer.singleShot(2000, run_tests_after_init)

        return app.exec()

    except Exception as e:
        logger.error(f"Failed to start TKA application: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
