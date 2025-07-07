#!/usr/bin/env python3
"""
TKA Integration Service - Clean Bridge to TKA Services
====================================================

Simple integration layer between the fluent launcher and TKA's 
dependency injection system.

Responsibilities:
- Interface with TKA's DI container
- Application discovery and management  
- Launch coordination
- Settings and state management

Architecture:
- Direct integration with TKA services (no fallbacks)
- Clean error handling and logging
- Follows TKA's dependency injection patterns
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

    Provides a clean interface to TKA services using standard
    dependency injection patterns.
    """

    def __init__(self):
        """Initialize TKA integration."""
        self.container = None
        self.app_service = None
        self.launch_service = None
        self.settings_service = None

        # Initialize TKA services
        self._initialize_tka_services()

        logger.info("✅ TKA integration service ready")

    def _initialize_tka_services(self):
        """Initialize TKA services using the launcher DI container."""
        try:
            # Use launcher's DI container with launcher applications
            from core.di_integration import get_launcher_container
            from launcher.core.interfaces import (
                IApplicationService,
                IApplicationLaunchService,
                ISettingsService,
            )

            # Get the DI container configured with launcher services
            # Use launcher container to ensure we have launcher applications
            self.container = get_launcher_container(use_tka_container=False)

            # Resolve services by their interfaces
            self.app_service = self.container.resolve(IApplicationService)
            self.launch_service = self.container.resolve(IApplicationLaunchService)
            self.settings_service = self.container.resolve(ISettingsService)

            logger.info("✅ TKA services initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize TKA services: {e}")
            raise RuntimeError("TKA services are required for launcher operation") from e

    def get_applications(self) -> List:
        """Get the list of available applications."""
        try:
            if self.app_service:
                applications = self.app_service.get_all_applications()
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
            if self.container:
                self.container.cleanup()
        except Exception as e:
            logger.warning(f"⚠️ TKA integration cleanup warning: {e}")
