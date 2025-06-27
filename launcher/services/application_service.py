"""
Application Service Implementation.

Manages application discovery, configuration, and metadata management
without dealing with the actual launching process.
"""

import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from domain.models import (
    ApplicationData,
    ApplicationCategory,
    ApplicationStatus,
)
from core.interfaces import IApplicationService, ILauncherStateService

logger = logging.getLogger(__name__)


class ApplicationService(IApplicationService):
    """
    Service for managing applications with immutable data patterns.

    Follows TKA's clean architecture principles with dependency injection
    and separation of concerns.
    """

    def __init__(self, state_service: Optional[ILauncherStateService] = None):
        """Initialize the application service."""
        self._state_service = state_service
        self._default_applications = self._create_default_applications()

        # Initialize applications in state if state service is available
        if self._state_service:
            self._initialize_applications()

    def get_all_applications(self) -> List[ApplicationData]:
        """Get all available applications."""
        if self._state_service:
            state = self._state_service.get_current_state()
            return [app for app in state.applications.values() if app.enabled]
        else:
            return [app for app in self._default_applications if app.enabled]

    def get_application(self, app_id: str) -> Optional[ApplicationData]:
        """Get application by ID."""
        if self._state_service:
            state = self._state_service.get_current_state()
            app = state.get_application(app_id)
            return app if app and app.enabled else None
        else:
            for app in self._default_applications:
                if app.id == app_id and app.enabled:
                    return app
            return None

    def get_applications_by_category(
        self, category: ApplicationCategory
    ) -> List[ApplicationData]:
        """Get applications in a specific category."""
        if self._state_service:
            state = self._state_service.get_current_state()
            return state.get_applications_by_category(category)
        else:
            return [
                app
                for app in self._default_applications
                if app.category == category and app.enabled
            ]

    def get_categories(self) -> List[ApplicationCategory]:
        """Get all available categories."""
        apps = self.get_all_applications()
        categories = set(app.category for app in apps)
        return sorted(categories, key=lambda c: c.value)

    def add_application(self, app: ApplicationData) -> None:
        """Add a new application."""
        if self._state_service:
            self._state_service.add_application(app)
            logger.info(f"Added application: {app.title}")
        else:
            # Remove existing app with same ID
            self._default_applications = [
                a for a in self._default_applications if a.id != app.id
            ]
            self._default_applications.append(app)
            logger.info(f"Added application to defaults: {app.title}")

    def update_application(self, app: ApplicationData) -> None:
        """Update an existing application."""
        if self._state_service:
            self._state_service.add_application(app)  # add_application handles updates
            logger.info(f"Updated application: {app.title}")
        else:
            # Update in defaults
            for i, existing_app in enumerate(self._default_applications):
                if existing_app.id == app.id:
                    self._default_applications[i] = app
                    logger.info(f"Updated application in defaults: {app.title}")
                    break

    def remove_application(self, app_id: str) -> None:
        """Remove an application."""
        if self._state_service:
            self._state_service.remove_application(app_id)
            logger.info(f"Removed application: {app_id}")
        else:
            self._default_applications = [
                app for app in self._default_applications if app.id != app_id
            ]
            logger.info(f"Removed application from defaults: {app_id}")

    def search_applications(self, query: str) -> List[ApplicationData]:
        """Search applications by title, description, or category."""
        if not query.strip():
            return self.get_all_applications()

        query_lower = query.lower()
        apps = self.get_all_applications()

        matching_apps = []
        for app in apps:
            if (
                query_lower in app.title.lower()
                or query_lower in app.description.lower()
                or query_lower in app.category.value.lower()
            ):
                matching_apps.append(app)

        return matching_apps

    def get_favorite_applications(self) -> List[ApplicationData]:
        """Get all favorite applications."""
        if self._state_service:
            state = self._state_service.get_current_state()
            return state.get_favorite_applications()
        else:
            return [
                app
                for app in self._default_applications
                if app.is_favorite and app.enabled
            ]

    def toggle_favorite(self, app_id: str) -> Optional[ApplicationData]:
        """Toggle favorite status of an application."""
        app = self.get_application(app_id)
        if not app:
            return None

        updated_app = app.update(is_favorite=not app.is_favorite)
        self.update_application(updated_app)

        logger.info(f"Toggled favorite for {app.title}: {updated_app.is_favorite}")
        return updated_app

    def _initialize_applications(self) -> None:
        """Initialize applications in the state service."""
        if not self._state_service:
            logger.warning("No state service available for application initialization")
            return

        state = self._state_service.get_current_state()

        # Add default applications if they don't exist in state
        for default_app in self._default_applications:
            if default_app.id not in state.applications:
                self._state_service.add_application(default_app)

        logger.info(
            f"Initialized {len(self._default_applications)} default applications"
        )

    def _create_default_applications(self) -> List[ApplicationData]:
        """Create the default set of applications."""
        # Get TKA root directory (launcher's parent)
        tka_root = Path(__file__).parent.parent.parent

        return [
            # Desktop Applications
            ApplicationData(
                id="desktop_legacy",
                title="TKA Desktop (Legacy)",
                description="Launch the legacy TKA Desktop application with full feature set",
                icon="🏛️",
                category=ApplicationCategory.DESKTOP,
                command="python main.py",
                working_dir=tka_root / "src" / "desktop" / "legacy",
                display_order=1,
            ),
            ApplicationData(
                id="desktop_modern",
                title="TKA Desktop (Modern)",
                description="Launch the modern TKA Desktop application with updated architecture",
                icon="✨",
                category=ApplicationCategory.DESKTOP,
                command="python main.py",
                working_dir=tka_root / "src" / "desktop" / "modern",
                display_order=2,
            ),
            ApplicationData(
                id="sequence_workbench",
                title="Sequence Workbench",
                description="Standalone sequence workbench for development and testing",
                icon="🎯",
                category=ApplicationCategory.DESKTOP,
                command="python standalone_sequence_workbench_exact.py",
                working_dir=tka_root / "src" / "desktop" / "modern",
                display_order=3,
            ),
            # Web Applications
            ApplicationData(
                id="web_app",
                title="TKA Web Interface",
                description="Launch the web-based TKA interface in your browser",
                icon="🌐",
                category=ApplicationCategory.WEB,
                command="npm run dev",
                working_dir=tka_root / "src" / "web" / "animator",
                display_order=3,
            ),
            ApplicationData(
                id="landing_page",
                title="TKA Landing Page",
                description="Launch the TKA marketing and information website",
                icon="🏠",
                category=ApplicationCategory.WEB,
                command="npm run dev",
                working_dir=tka_root / "src" / "web" / "landing",
                display_order=4,
            ),
            ApplicationData(
                id="animator",
                title="Pictograph Animator",
                description="Launch the pictograph animation tool",
                icon="🎬",
                category=ApplicationCategory.WEB,
                command="npm run dev",
                working_dir=tka_root / "src" / "web" / "animator",
                display_order=5,
            ),
            # Development Tools
            ApplicationData(
                id="test_suite",
                title="Test Suite",
                description="Run the comprehensive TKA test suite",
                icon="🧪",
                category=ApplicationCategory.DEVELOPMENT,
                command="pytest",
                working_dir=tka_root,
                display_order=6,
            ),
            # Note: Removed dev_server, test_runner_focused, code_formatter, settings, and about applications
            # as requested to simplify the launcher interface
        ]
