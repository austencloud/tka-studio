"""
Immutable Domain Models for TKA Launcher.

Following TKA's clean architecture patterns with frozen dataclasses and .update() methods.
These models represent the core business entities without any UI coupling.
"""

from dataclasses import dataclass, field, replace
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid


class LaunchMode(Enum):
    """Launcher display modes."""

    WINDOW = "window"
    DOCKED = "docked"


class DockPosition(Enum):
    """Dock positioning options."""

    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"


class ApplicationStatus(Enum):
    """Application execution status."""

    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


class ApplicationCategory(Enum):
    """Application categories for organization."""

    DESKTOP = "Desktop Applications"
    WEB = "Web Applications"
    DEVELOPMENT = "Development Tools"
    UTILITIES = "Utilities"


@dataclass(frozen=True)
class ApplicationData:
    """
    Immutable data for a launchable application.

    REPLACES: AppDefinition (config/app_definitions.py)

    This model represents a single application that can be launched
    from the TKA Launcher without any UI coupling.
    """

    # Core identity
    id: str
    title: str
    description: str

    # Visual representation
    icon: str
    category: ApplicationCategory

    # Launch configuration
    command: Optional[str] = None
    working_dir: Optional[Path] = None
    environment_vars: Dict[str, str] = field(default_factory=dict)

    # State and metadata
    enabled: bool = True
    status: ApplicationStatus = ApplicationStatus.STOPPED
    process_id: Optional[int] = None
    last_launched: Optional[str] = None  # ISO timestamp
    launch_count: int = 0

    # UI preferences
    display_order: int = 0
    is_favorite: bool = False
    custom_icon_path: Optional[Path] = None

    def update(self, **kwargs) -> "ApplicationData":
        """Create a new instance with updated fields."""
        return replace(self, **kwargs)

    def with_status(
        self, status: ApplicationStatus, process_id: Optional[int] = None
    ) -> "ApplicationData":
        """Update application status and process ID."""
        return self.update(status=status, process_id=process_id)

    def increment_launch_count(self) -> "ApplicationData":
        """Increment the launch count."""
        return self.update(launch_count=self.launch_count + 1)

    def mark_launched(
        self, timestamp: str, process_id: Optional[int] = None
    ) -> "ApplicationData":
        """Mark application as launched with timestamp."""
        return self.update(
            last_launched=timestamp,
            launch_count=self.launch_count + 1,
            status=ApplicationStatus.STARTING,
            process_id=process_id,
        )


@dataclass(frozen=True)
class WindowGeometry:
    """Immutable window geometry data."""

    x: int
    y: int
    width: int
    height: int

    def update(self, **kwargs) -> "WindowGeometry":
        """Create a new instance with updated fields."""
        return replace(self, **kwargs)

    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary for serialization."""
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}

    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> "WindowGeometry":
        """Create from dictionary."""
        return cls(x=data["x"], y=data["y"], width=data["width"], height=data["height"])


@dataclass(frozen=True)
class DockConfiguration:
    """
    Immutable dock configuration data.

    Represents dock-specific settings and positioning.
    """

    position: DockPosition = DockPosition.BOTTOM_LEFT
    width: int = 64
    height: int = 48  # Will match Windows taskbar height
    margin_x: int = 0
    margin_y: int = 0
    always_on_top: bool = True
    auto_hide: bool = False
    screen_index: int = 0

    def update(self, **kwargs) -> "DockConfiguration":
        """Create a new instance with updated fields."""
        return replace(self, **kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "position": self.position.value,
            "width": self.width,
            "height": self.height,
            "margin_x": self.margin_x,
            "margin_y": self.margin_y,
            "always_on_top": self.always_on_top,
            "auto_hide": self.auto_hide,
            "screen_index": self.screen_index,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DockConfiguration":
        """Create from dictionary."""
        return cls(
            position=DockPosition(data.get("position", DockPosition.BOTTOM_LEFT.value)),
            width=data.get("width", 64),
            height=data.get("height", 48),
            margin_x=data.get("margin_x", 0),
            margin_y=data.get("margin_y", 0),
            always_on_top=data.get("always_on_top", True),
            auto_hide=data.get("auto_hide", False),
            screen_index=data.get("screen_index", 0),
        )


@dataclass(frozen=True)
class ScreenData:
    """Immutable screen/monitor data."""

    index: int
    name: str
    geometry: WindowGeometry
    is_primary: bool = False
    scale_factor: float = 1.0

    def update(self, **kwargs) -> "ScreenData":
        """Create a new instance with updated fields."""
        return replace(self, **kwargs)


@dataclass(frozen=True)
class LauncherState:
    """
    Immutable launcher state data.

    This model represents the complete state of the launcher including
    mode, geometry, screen configuration, and application states.
    """

    # Core state
    mode: LaunchMode = LaunchMode.WINDOW

    # Window state
    window_geometry: Optional[WindowGeometry] = None
    docked_geometry: Optional[WindowGeometry] = None
    dock_configuration: DockConfiguration = field(default_factory=DockConfiguration)

    # Screen configuration
    target_screen_index: int = 0
    available_screens: List[ScreenData] = field(default_factory=list)

    # Application state
    applications: Dict[str, ApplicationData] = field(default_factory=dict)

    # UI state
    search_query: str = ""
    selected_category: Optional[ApplicationCategory] = None
    show_favorites_only: bool = False

    # Session data
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    first_run: bool = True
    total_launches: int = 0

    def update(self, **kwargs) -> "LauncherState":
        """Create a new instance with updated fields."""
        return replace(self, **kwargs)

    def with_mode(self, mode: LaunchMode) -> "LauncherState":
        """Update launcher mode."""
        return self.update(mode=mode)

    def with_window_geometry(self, geometry: WindowGeometry) -> "LauncherState":
        """Update window geometry."""
        return self.update(window_geometry=geometry)

    def with_docked_geometry(self, geometry: WindowGeometry) -> "LauncherState":
        """Update docked geometry."""
        return self.update(docked_geometry=geometry)

    def with_dock_configuration(
        self, dock_config: DockConfiguration
    ) -> "LauncherState":
        """Update dock configuration."""
        return self.update(dock_configuration=dock_config)

    def with_application(self, app: ApplicationData) -> "LauncherState":
        """Update or add an application."""
        new_apps = self.applications.copy()
        new_apps[app.id] = app
        return self.update(applications=new_apps)

    def with_application_status(
        self, app_id: str, status: ApplicationStatus, process_id: Optional[int] = None
    ) -> "LauncherState":
        """Update application status."""
        if app_id not in self.applications:
            return self

        updated_app = self.applications[app_id].with_status(status, process_id)
        return self.with_application(updated_app)

    def with_search_query(self, query: str) -> "LauncherState":
        """Update search query."""
        return self.update(search_query=query)

    def with_selected_category(
        self, category: Optional[ApplicationCategory]
    ) -> "LauncherState":
        """Update selected category."""
        return self.update(selected_category=category)

    def get_application(self, app_id: str) -> Optional[ApplicationData]:
        """Get application by ID."""
        return self.applications.get(app_id)

    def get_applications_by_category(
        self, category: ApplicationCategory
    ) -> List[ApplicationData]:
        """Get all applications in a category."""
        return [
            app
            for app in self.applications.values()
            if app.category == category and app.enabled
        ]

    def get_running_applications(self) -> List[ApplicationData]:
        """Get all currently running applications."""
        return [
            app
            for app in self.applications.values()
            if app.status == ApplicationStatus.RUNNING
        ]

    def get_favorite_applications(self) -> List[ApplicationData]:
        """Get all favorite applications."""
        return [
            app for app in self.applications.values() if app.is_favorite and app.enabled
        ]


@dataclass(frozen=True)
class LaunchRequest:
    """Immutable data for an application launch request."""

    application_id: str
    timestamp: str
    session_id: str
    user_initiated: bool = True
    launch_options: Dict[str, Any] = field(default_factory=dict)

    def update(self, **kwargs) -> "LaunchRequest":
        """Create a new instance with updated fields."""
        return replace(self, **kwargs)


@dataclass(frozen=True)
class LaunchResult:
    """Immutable data for an application launch result."""

    request: LaunchRequest
    success: bool
    process_id: Optional[int] = None
    error_message: Optional[str] = None
    execution_time_ms: int = 0

    def update(self, **kwargs) -> "LaunchResult":
        """Create a new instance with updated fields."""
        return replace(self, **kwargs)

    @classmethod
    def success_result(
        cls, request: LaunchRequest, process_id: int, execution_time_ms: int = 0
    ) -> "LaunchResult":
        """Create a successful launch result."""
        return cls(
            request=request,
            success=True,
            process_id=process_id,
            execution_time_ms=execution_time_ms,
        )

    @classmethod
    def error_result(
        cls, request: LaunchRequest, error_message: str, execution_time_ms: int = 0
    ) -> "LaunchResult":
        """Create an error launch result."""
        return cls(
            request=request,
            success=False,
            error_message=error_message,
            execution_time_ms=execution_time_ms,
        )
