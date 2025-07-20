#!/usr/bin/env python3
"""
TKA Integration Service - Bridge to TKA Services
===============================================

Clean integration layer between the fluent launcher and TKA's existing
services and dependency injection system.

Responsibilities:
- Interface with TKA's DI container
- Application discovery and management
- Launch coordination
- Settings and state management

Architecture:
- Adapter pattern for TKA services
- Graceful fallback for missing services
- Clean error handling and logging
"""

import logging
import sys
from pathlib import Path
from typing import List, Optional

# Add paths for TKA imports
launcher_dir = Path(__file__).parent
parent_dir = launcher_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

logger = logging.getLogger(__name__)


class TKAIntegrationService:
    """
    Service for integrating with TKA's existing infrastructure.

    Provides a clean interface to TKA services while handling
    fallbacks and error conditions gracefully.
    """

    def __init__(self):
        """Initialize TKA integration."""
        logger.info("🔗 Initializing TKA integration service...")

        self.container = None
        self.app_service = None
        self.launch_service = None
        self.settings_service = None

        # Initialize TKA services
        self._initialize_tka_services()

        logger.info("✅ TKA integration service initialized")

    def _initialize_tka_services(self):
        """Initialize TKA services with graceful fallback."""
        try:
            # Try to import and use TKA's DI container
            from core.di_integration import get_launcher_container
            from core.interfaces import (
                IApplicationService,
                IApplicationLaunchService,
                ISettingsService,
            )

            # Get the DI container - use launcher's own container for better control
            self.container = get_launcher_container(use_tka_container=False)

            # Resolve services by their interfaces (not concrete classes)
            self.app_service = self.container.resolve(IApplicationService)
            self.launch_service = self.container.resolve(IApplicationLaunchService)
            self.settings_service = self.container.resolve(ISettingsService)

            logger.info("✅ TKA services initialized successfully")

        except ImportError as e:
            logger.warning(f"⚠️ TKA services not available, using fallback: {e}")
            self._initialize_fallback_services()
        except Exception as e:
            logger.error(f"❌ Failed to initialize TKA services: {e}")
            self._initialize_fallback_services()

    def _initialize_fallback_services(self):
        """Initialize fallback services when TKA services are unavailable."""
        logger.info("🔄 Initializing fallback services...")

        # Create minimal fallback implementations
        self.app_service = FallbackApplicationService()
        self.launch_service = FallbackLaunchService()
        self.settings_service = FallbackSettingsService()

        logger.info("✅ Fallback services initialized")

    def get_applications(self) -> List:
        """Get the list of available applications."""
        try:
            if self.app_service:
                applications = self.app_service.get_all_applications()
                logger.info(f"📱 Retrieved {len(applications)} applications")
                return applications
            else:
                logger.warning("⚠️ No application service available")
                return []

        except Exception as e:
            logger.error(f"❌ Failed to get applications: {e}")
            return []

    def launch_application(self, app_id: str) -> bool:
        """Launch an application by ID."""
        try:
            if self.launch_service:
                # Create launch request
                from domain.models import LaunchRequest
                from datetime import datetime

                request = LaunchRequest(
                    application_id=app_id,
                    timestamp=datetime.now().isoformat(),
                    session_id="launcher",
                    user_initiated=True,
                    launch_options={},
                )

                # Launch the application
                result = self.launch_service.launch_application(request)

                if result.success:
                    logger.info(f"🚀 Successfully launched application: {app_id}")
                    return True
                else:
                    logger.error(
                        f"❌ Failed to launch application: {result.error_message}"
                    )
                    return False
            else:
                logger.warning(f"⚠️ No launch service available for {app_id}")
                return False

        except Exception as e:
            logger.error(f"❌ Error launching application {app_id}: {e}")
            return False

    def get_settings(self) -> dict:
        """Get launcher settings."""
        try:
            if self.settings_service:
                return self.settings_service.get_all_settings()
            else:
                return {}
        except Exception as e:
            logger.error(f"❌ Failed to get settings: {e}")
            return {}

    def save_settings(self, settings: dict):
        """Save launcher settings."""
        try:
            if self.settings_service:
                self.settings_service.update_settings(settings)
                logger.info("💾 Settings saved successfully")
            else:
                logger.warning("⚠️ No settings service available")
        except Exception as e:
            logger.error(f"❌ Failed to save settings: {e}")

    def cleanup(self):
        """Cleanup TKA integration resources."""
        logger.info("🧹 Cleaning up TKA integration...")

        try:
            # Cleanup any resources if needed
            pass
        except Exception as e:
            logger.warning(f"⚠️ TKA integration cleanup warning: {e}")


# Fallback service implementations
class FallbackApplicationService:
    """Fallback application service when TKA services are unavailable."""

    def get_all_applications(self):
        """Return a minimal set of default applications."""
        from domain.models import ApplicationData, ApplicationCategory

        # Get the TKA root directory (parent of launcher directory)
        tka_root = Path(__file__).parent.parent

        # Check if we're running in debug mode (debugpy is attached)
        debug_mode = False
        try:
            import debugpy

            debug_mode = debugpy.is_client_connected()
        except ImportError:
            pass

        # Prepare debug command prefix if in debug mode
        debug_prefix = ""
        if debug_mode:
            debug_prefix = "python -m debugpy --listen 5678 --wait-for-client "

        return [
            ApplicationData(
                id="desktop_modern",
                title="TKA Desktop (Modern)",
                description="Modern TKA Desktop application with updated architecture",
                icon="✨",
                category=ApplicationCategory.DESKTOP,
                command="python main.py",  # Modern main.py doesn't need --modern flag
                working_dir=tka_root / "src" / "desktop" / "modern",
                display_order=1,
            ),
            ApplicationData(
                id="sequence_workbench",
                title="Sequence Workbench",
                description="Standalone sequence workbench for development and testing",
                icon="🎯",
                category=ApplicationCategory.DESKTOP,
                command="python standalone_sequence_workbench.py",
                working_dir=tka_root / "src" / "desktop" / "modern",
                display_order=3,
            ),
            ApplicationData(
                id="desktop_modern_debug",
                title="TKA Desktop (Modern) - Debug",
                description="Modern TKA Desktop with debugger attached (port 5679)",
                icon="🐛",
                category=ApplicationCategory.DEVELOPMENT,
                command="python -m debugpy --listen 5679 --wait-for-client main.py",
                working_dir=tka_root / "src" / "desktop" / "modern",
                display_order=1,
            ),
            ApplicationData(
                id="desktop_legacy",
                title="TKA Desktop (Legacy)",
                description="Legacy TKA Desktop application with full feature set",
                icon="🏛️",
                category=ApplicationCategory.DESKTOP,
                command=f"{debug_prefix}python main.py",
                working_dir=tka_root / "src" / "desktop" / "legacy",
                display_order=2,
            ),
            ApplicationData(
                id="desktop_legacy_debug",
                title="TKA Desktop (Legacy) - Debug",
                description="Legacy TKA Desktop with debugger attached (port 5680)",
                icon="🐛",
                category=ApplicationCategory.DEVELOPMENT,
                command="python -m debugpy --listen 5680 --wait-for-client main.py",
                working_dir=tka_root / "src" / "desktop" / "legacy",
                display_order=2,
            ),
            ApplicationData(
                id="web_app",
                title="TKA Web Application",
                description="Web-based TKA interface for browser access",
                icon="🌐",
                category=ApplicationCategory.WEB,
                command="npm run dev",
                working_dir=tka_root / "src" / "web",
                display_order=3,
            ),
            ApplicationData(
                id="dev_tools",
                title="Development Tools",
                description="Developer utilities and debugging tools",
                icon="🔧",
                category=ApplicationCategory.DEVELOPMENT,
                command=f"{debug_prefix}python main.py --dev",
                working_dir=tka_root,
                display_order=4,
            ),
        ]


class FallbackLaunchService:
    """Fallback launch service when TKA services are unavailable."""

    def launch_application(self, request):
        """Simple fallback launch implementation."""
        import subprocess
        from domain.models import LaunchResult

        try:
            # Get application data
            app_service = FallbackApplicationService()
            applications = app_service.get_all_applications()
            app = next(
                (a for a in applications if a.id == request.application_id), None
            )

            if not app:
                return LaunchResult.error_result(request, "Application not found")

            if not app.command:
                return LaunchResult.error_result(
                    request, "No command specified for application"
                )

            # Log launch details for debugging
            logger.info(f"🚀 Launching application: {app.title}")
            logger.info(f"   Command: {app.command}")
            logger.info(f"   Working directory: {app.working_dir}")
            logger.info(f"   Category: {app.category}")

            # Launch the process for GUI applications
            # Don't capture stdout/stderr to allow GUI windows to display properly
            process = subprocess.Popen(
                app.command,
                shell=True,
                cwd=str(app.working_dir) if app.working_dir else None,
                # Allow GUI applications to display by not capturing output
                stdout=None,
                stderr=None,
                # Detach from parent process so GUI apps can run independently
                creationflags=(
                    subprocess.CREATE_NEW_PROCESS_GROUP
                    if hasattr(subprocess, "CREATE_NEW_PROCESS_GROUP")
                    else 0
                ),
            )

            # Return success immediately for GUI applications
            # Don't wait for process completion as GUI apps should run independently
            logger.info(
                f"🚀 Successfully launched GUI application: {app.title} (PID: {process.pid})"
            )
            return LaunchResult.success_result(request, process.pid, 0)

        except Exception as e:
            return LaunchResult.error_result(request, str(e))


class FallbackSettingsService:
    """Fallback settings service when TKA services are unavailable."""

    def __init__(self):
        self.settings = {
            "theme": "dark",
            "window_mode": "window",
            "auto_refresh": True,
            "show_categories": True,
        }

    def get_all_settings(self):
        """Return default settings."""
        return self.settings.copy()

    def update_settings(self, new_settings):
        """Update settings."""
        self.settings.update(new_settings)
