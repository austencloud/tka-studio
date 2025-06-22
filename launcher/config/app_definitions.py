"""
Application Definitions for TKA Unified Launcher.
Defines all available applications and their metadata.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class AppDefinition:
    """Definition of a launchable application."""

    id: str
    title: str
    description: str
    icon: str
    category: str
    command: Optional[str] = None
    working_dir: Optional[str] = None
    enabled: bool = True


class AppDefinitions:
    """Manages application definitions."""

    def __init__(self):
        """Initialize with default application definitions."""
        self._apps = self._create_default_apps()

    def _create_default_apps(self) -> List[AppDefinition]:
        """Create the default set of applications."""
        return [
            # Desktop Applications
            AppDefinition(
                id="desktop_legacy",
                title="TKA Desktop (Legacy)",
                description="Launch the legacy TKA Desktop application with full feature set",
                icon="🏛️",
                category="Desktop Applications",
            ),
            AppDefinition(
                id="desktop_modern",
                title="TKA Desktop (Modern)",
                description="Launch the modern TKA Desktop application with updated architecture",
                icon="✨",
                category="Desktop Applications",
            ),
            # Web Applications
            AppDefinition(
                id="web_app",
                title="TKA Web Interface",
                description="Launch the web-based TKA interface in your browser",
                icon="🌐",
                category="Web Applications",
            ),
            # Development Tools
            AppDefinition(
                id="dev_tools",
                title="Development Tools",
                description="Access TKA development and debugging tools",
                icon="🛠️",
                category="Development Tools",
            ),
            AppDefinition(
                id="test_suite",
                title="Test Suite",
                description="Run the comprehensive TKA test suite",
                icon="🧪",
                category="Development Tools",
            ),
            # Utilities
            AppDefinition(
                id="settings",
                title="Launcher Settings",
                description="Configure launcher preferences and behavior",
                icon="⚙️",
                category="Utilities",
            ),
            AppDefinition(
                id="about",
                title="About TKA",
                description="Information about The Kinetic Constructor project",
                icon="ℹ️",
                category="Utilities",
            ),
        ]

    def get_all(self) -> List[AppDefinition]:
        """Get all application definitions."""
        return [app for app in self._apps if app.enabled]

    def get_by_id(self, app_id: str) -> Optional[AppDefinition]:
        """Get an application by ID."""
        for app in self._apps:
            if app.id == app_id and app.enabled:
                return app
        return None

    def get_by_category(self, category: str) -> List[AppDefinition]:
        """Get all applications in a category."""
        return [app for app in self._apps if app.category == category and app.enabled]

    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        categories = set(app.category for app in self._apps if app.enabled)
        return sorted(categories)

    def add_app(self, app: AppDefinition):
        """Add a new application definition."""
        # Remove existing app with same ID
        self._apps = [a for a in self._apps if a.id != app.id]
        self._apps.append(app)

    def remove_app(self, app_id: str):
        """Remove an application definition."""
        self._apps = [app for app in self._apps if app.id != app_id]

    def enable_app(self, app_id: str):
        """Enable an application."""
        app = self.get_by_id(app_id)
        if app:
            app.enabled = True

    def disable_app(self, app_id: str):
        """Disable an application."""
        for app in self._apps:
            if app.id == app_id:
                app.enabled = False
                break

    def reload(self):
        """Reload application definitions."""
        # For now, just recreate defaults
        # In the future, this could load from a config file
        self._apps = self._create_default_apps()
