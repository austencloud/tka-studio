"""
Application Lifecycle Manager

Pure service for managing application lifecycle and startup sequence.
Extracted from KineticConstructorModern to follow single responsibility principle.

PROVIDES:
- Application initialization sequence
- Window positioning and sizing
- Parallel testing mode detection
- Screen detection and multi-monitor support
- API server startup coordination
"""

from typing import Optional, Tuple, Callable
from abc import ABC, abstractmethod
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QRect


class IApplicationLifecycleManager(ABC):
    """Interface for application lifecycle operations."""

    @abstractmethod
    def initialize_application(
        self,
        main_window: QMainWindow,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
        progress_callback: Optional[Callable] = None,
    ) -> None:
        """Initialize application with proper lifecycle management."""
        pass

    @abstractmethod
    def set_window_dimensions(
        self,
        main_window: QMainWindow,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
    ) -> None:
        """Set window dimensions using modern responsive design."""
        pass

    @abstractmethod
    def detect_parallel_testing_mode(self) -> Tuple[bool, str, str]:
        """Detect if we're running in parallel testing mode."""
        pass


class ApplicationLifecycleManager(IApplicationLifecycleManager):
    """
    Pure service for application lifecycle management.

    Handles application initialization, window management, and startup coordination
    without business logic dependencies. Uses clean separation of concerns.
    """

    def __init__(self):
        """Initialize application lifecycle manager."""
        self.api_enabled = True

    def initialize_application(
        self,
        main_window: QMainWindow,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
        progress_callback: Optional[Callable] = None,
    ) -> None:
        """Initialize application with proper lifecycle management."""
        if progress_callback:
            progress_callback(10, "Initializing application lifecycle...")

        # Set window title based on mode
        if parallel_mode:
            main_window.setWindowTitle("TKA Modern - Parallel Testing")
        else:
            main_window.setWindowTitle("🚀 Kinetic Constructor")

        # Set window dimensions
        self.set_window_dimensions(
            main_window, target_screen, parallel_mode, parallel_geometry
        )

        if progress_callback:
            progress_callback(15, "Application lifecycle initialized")

    def set_window_dimensions(
        self,
        main_window: QMainWindow,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
    ) -> None:
        """Set window dimensions using modern responsive design: 90% of screen size."""
        # Check for parallel testing mode first
        if parallel_mode and parallel_geometry:
            try:
                x, y, width, height = map(int, parallel_geometry.split(","))
                main_window.setGeometry(x, y, width, height)
                main_window.setMinimumSize(1400, 900)
                print(f"🔄 Modern positioned at: {x},{y} ({width}x{height})")
                return
            except Exception as e:
                print(f"⚠️ Failed to apply parallel testing geometry: {e}")
                # Fall through to normal positioning

        # Use target screen for consistent positioning
        screen = target_screen or QGuiApplication.primaryScreen()

        if not screen:
            main_window.setGeometry(100, 100, 1400, 900)
            main_window.setMinimumSize(1400, 900)
            return

        # Calculate responsive dimensions (90% of screen)
        available_geometry = screen.availableGeometry()
        window_width = int(available_geometry.width() * 0.9)
        window_height = int(available_geometry.height() * 0.9)
        x = available_geometry.x() + int(
            (available_geometry.width() - window_width) / 2
        )
        y = available_geometry.y() + int(
            (available_geometry.height() - window_height) / 2
        )

        main_window.setGeometry(x, y, window_width, window_height)
        main_window.setMinimumSize(1400, 900)

    def detect_parallel_testing_mode(self) -> Tuple[bool, str, str]:
        """Detect if we're running in parallel testing mode."""
        import argparse
        import os

        # Check command line arguments
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--parallel-testing", action="store_true")
        parser.add_argument(
            "--monitor", choices=["primary", "secondary", "left", "right"]
        )
        args, _ = parser.parse_known_args()

        # Check environment variables
        env_parallel = os.environ.get("TKA_PARALLEL_TESTING", "").lower() == "true"
        env_monitor = os.environ.get("TKA_PARALLEL_MONITOR", "")
        env_geometry = os.environ.get("TKA_PARALLEL_GEOMETRY", "")

        parallel_mode = args.parallel_testing or env_parallel
        monitor = args.monitor or env_monitor

        if parallel_mode:
            print(f"🔄 Modern Parallel Testing Mode: {monitor} monitor")
            if env_geometry:
                print(f"   📐 Target geometry: {env_geometry}")

        return parallel_mode, monitor, env_geometry

    def determine_target_screen(self, parallel_mode=False, monitor=""):
        """Determine target screen for application placement."""
        screens = QGuiApplication.screens()

        # Override screen selection for parallel testing
        if parallel_mode and len(screens) > 1:
            if monitor in ["secondary", "right"]:
                # Determine which screen is physically on the right
                primary_screen = screens[0]
                secondary_screen = screens[1]

                # If secondary has higher X coordinate, it's on the right
                if secondary_screen.geometry().x() > primary_screen.geometry().x():
                    target_screen = secondary_screen
                    print(
                        f"🔄 Modern forced to RIGHT monitor (secondary) for parallel testing"
                    )
                else:
                    target_screen = primary_screen
                    print(
                        f"🔄 Modern forced to RIGHT monitor (primary) for parallel testing"
                    )

            elif monitor in ["primary", "left"]:
                # Determine which screen is physically on the left
                primary_screen = screens[0]
                secondary_screen = screens[1]

                # If secondary has lower X coordinate, it's on the left
                if secondary_screen.geometry().x() < primary_screen.geometry().x():
                    target_screen = secondary_screen
                    print(
                        f"🔄 Modern forced to LEFT monitor (secondary) for parallel testing"
                    )
                else:
                    target_screen = primary_screen
                    print(
                        f"🔄 Modern forced to LEFT monitor (primary) for parallel testing"
                    )
            else:
                target_screen = screens[1]  # Default to secondary
        else:
            # Normal behavior: prefer secondary monitor if available
            target_screen = (
                screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
            )

        return target_screen

    def start_api_server(self, enable_api=True) -> bool:
        """Start the API server if dependencies are available."""
        if not enable_api:
            print("🚫 API server is disabled")
            return False

        try:
            from infrastructure.api.api_integration import start_api_server
            import platform

            # Enhanced logging for Windows
            if platform.system() == "Windows":
                print("🪟 Starting API server on Windows...")
                print("   Note: Some ports may require administrator privileges")

            # Start API server
            success = start_api_server(enabled=enable_api, auto_port=True)

            if success:
                print("🌐 TKA API server started successfully")
                from infrastructure.api.api_integration import get_api_integration

                api = get_api_integration()
                server_url = api.get_server_url()
                docs_url = api.get_docs_url()
                if server_url:
                    print(f"   📍 Server: {server_url}")
                if docs_url:
                    print(f"   📚 Docs: {docs_url}")
                return True
            else:
                print("⚠️ API server startup failed - continuing without API")
                return False

        except ImportError as e:
            print(f"⚠️ API server dependencies not available: {e}")
            print("   To enable API features: pip install fastapi uvicorn")
            print("   Continuing without API server...")
            return False
        except PermissionError as e:
            print(f"⚠️ Windows permission error for API server: {e}")
            print("   Possible solutions:")
            print("   1. Run as administrator")
            print("   2. Check Windows Firewall/Antivirus settings")
            print("   3. The application will continue without API server")
            return False
        except OSError as e:
            if "10013" in str(e):  # Windows socket permission error
                print(f"⚠️ Windows socket permission error: {e}")
                print("   This is a common Windows security restriction")
                print("   The application will continue without API server")
            else:
                print(f"⚠️ Network error starting API server: {e}")
                print("   Continuing without API server...")
            return False
        except Exception as e:
            print(f"⚠️ Unexpected error starting API server: {e}")
            print("   This does not affect the main application functionality")
            print("   Continuing without API server...")
            return False

    def get_application_info(self) -> dict:
        """Get application information and status."""
        return {
            "title": "🚀 Kinetic Constructor",
            "version": "Modern",
            "api_enabled": self.api_enabled,
            "minimum_size": (1400, 900),
            "responsive_sizing": True,
        }

    def validate_screen_configuration(self) -> dict:
        """Validate screen configuration and return status."""
        screens = QGuiApplication.screens()
        primary_screen = QGuiApplication.primaryScreen()

        return {
            "screen_count": len(screens),
            "primary_screen_available": primary_screen is not None,
            "multi_monitor_support": len(screens) > 1,
            "screen_geometries": [
                {
                    "index": i,
                    "geometry": screen.geometry(),
                    "available_geometry": screen.availableGeometry(),
                }
                for i, screen in enumerate(screens)
            ],
        }
