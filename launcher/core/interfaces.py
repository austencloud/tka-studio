"""
Service Interfaces for TKA Launcher.

Following TKA's Protocol-based interface patterns for clean dependency injection
and testability. These interfaces define the contracts for launcher services.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol

from desktop.modern.domain.models import (
    ApplicationCategory,
    ApplicationData,
    ApplicationStatus,
    LauncherState,
    LaunchMode,
    LaunchRequest,
    LaunchResult,
    ScreenData,
    WindowGeometry,
)


class ILauncherStateService(Protocol):
    """
    Service interface for managing launcher state.

    Handles the immutable state management for the launcher including
    mode switching, geometry persistence, and application state tracking.
    """

    def get_current_state(self) -> LauncherState:
        """Get the current launcher state."""
        pass

    def update_state(self, state: LauncherState) -> None:
        """Update the launcher state."""
        pass

    def switch_mode(self, mode: LaunchMode) -> LauncherState:
        """Switch launcher mode and return new state."""
        pass

    def save_window_geometry(
        self, geometry: WindowGeometry, mode: LaunchMode
    ) -> LauncherState:
        """Save window geometry for the specified mode."""
        pass

    def get_window_geometry(self, mode: LaunchMode) -> Optional[WindowGeometry]:
        """Get saved window geometry for the specified mode."""
        pass

    def update_application_status(
        self, app_id: str, status: ApplicationStatus, process_id: Optional[int] = None
    ) -> LauncherState:
        """Update application status and return new state."""
        pass

    def persist_state(self) -> None:
        """Persist current state to storage."""
        pass

    def load_state(self) -> LauncherState:
        """Load state from storage."""
        pass


class IApplicationService(Protocol):
    """
    Service interface for managing applications.

    Handles application discovery, configuration, and metadata management
    without dealing with the actual launching process.
    """

    def get_all_applications(self) -> List[ApplicationData]:
        """Get all available applications."""
        pass

    def get_application(self, app_id: str) -> Optional[ApplicationData]:
        """Get application by ID."""
        pass

    def get_applications_by_category(
        self, category: ApplicationCategory
    ) -> List[ApplicationData]:
        """Get applications in a specific category."""
        pass

    def get_categories(self) -> List[ApplicationCategory]:
        """Get all available categories."""
        pass

    def add_application(self, app: ApplicationData) -> None:
        """Add a new application."""
        pass

    def update_application(self, app: ApplicationData) -> None:
        """Update an existing application."""
        pass

    def remove_application(self, app_id: str) -> None:
        """Remove an application."""
        pass

    def search_applications(self, query: str) -> List[ApplicationData]:
        """Search applications by title, description, or category."""
        pass

    def get_favorite_applications(self) -> List[ApplicationData]:
        """Get all favorite applications."""
        pass

    def toggle_favorite(self, app_id: str) -> Optional[ApplicationData]:
        """Toggle favorite status of an application."""
        pass


class IApplicationLaunchService(Protocol):
    """
    Service interface for launching applications.

    Handles the actual process of launching applications, managing
    process lifecycle, and providing launch feedback.
    """

    def launch_application(self, request: LaunchRequest) -> LaunchResult:
        """Launch an application and return the result."""
        pass

    def stop_application(self, app_id: str) -> bool:
        """Stop a running application."""
        pass

    def is_application_running(self, app_id: str) -> bool:
        """Check if an application is currently running."""
        pass

    def get_running_applications(self) -> List[ApplicationData]:
        """Get all currently running applications."""
        pass

    def get_application_process_id(self, app_id: str) -> Optional[int]:
        """Get the process ID of a running application."""
        pass

    def kill_application(self, app_id: str) -> bool:
        """Force kill an application process."""
        pass

    def restart_application(self, app_id: str) -> LaunchResult:
        """Restart a running application."""
        pass


class IScreenService(Protocol):
    """
    Service interface for screen/monitor management.

    Handles multi-monitor detection, screen geometry calculation,
    and intelligent screen selection for launcher positioning.
    """

    def get_available_screens(self) -> List[ScreenData]:
        """Get all available screens/monitors."""
        pass

    def get_primary_screen(self) -> ScreenData:
        """Get the primary screen."""
        pass

    def get_screen_by_index(self, index: int) -> Optional[ScreenData]:
        """Get screen by index."""
        pass

    def get_current_screen(
        self, window_geometry: WindowGeometry
    ) -> Optional[ScreenData]:
        """Get the screen containing the specified window geometry."""
        pass

    def calculate_docked_geometry(
        self, screen: ScreenData, dock_width: int = 110
    ) -> WindowGeometry:
        """Calculate geometry for horizontal bottom-docked mode overlaying the taskbar."""
        pass

    def calculate_centered_geometry(
        self, screen: ScreenData, width: int, height: int
    ) -> WindowGeometry:
        """Calculate centered window geometry on the specified screen."""
        pass

    def is_geometry_on_screen(
        self, geometry: WindowGeometry, screen: ScreenData
    ) -> bool:
        """Check if geometry is within screen bounds."""
        pass


class IAnimationService(Protocol):
    """
    Service interface for launcher animations.

    Provides Qt-compatible animations for smooth UI transitions,
    mode switching, and visual feedback following 2025 design standards.
    """

    def animate_mode_transition(
        self, widget: Any, target_geometry: WindowGeometry, duration: int = 300
    ) -> str:
        """Animate transition between window and docked modes."""
        pass

    def animate_dock_slide_in(self, widget: Any, duration: int = 300) -> str:
        """Animate dock sliding in from screen edge."""
        pass

    def animate_dock_slide_out(self, widget: Any, duration: int = 300) -> str:
        """Animate dock sliding out to screen edge."""
        pass

    def animate_button_press(self, button: Any, duration: int = 150) -> str:
        """Animate button press feedback."""
        pass

    def animate_hover_enter(self, widget: Any, duration: int = 200) -> str:
        """Animate hover enter effect."""
        pass

    def animate_hover_leave(self, widget: Any, duration: int = 200) -> str:
        """Animate hover leave effect."""
        pass

    def animate_launch_feedback(self, widget: Any, duration: int = 600) -> str:
        """Animate application launch feedback."""
        pass

    def animate_entrance(self, widget: Any, delay: int = 0) -> str:
        """Animate widget entrance with staggered timing."""
        pass

    def stop_animation(self, animation_id: str) -> None:
        """Stop a specific animation."""
        pass

    def stop_all_animations(self) -> None:
        """Stop all active animations."""
        pass


class ISettingsService(Protocol):
    """
    Service interface for launcher settings management.

    Handles persistent configuration, user preferences,
    and settings validation with proper defaults.
    """

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        pass

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        pass

    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings as a dictionary."""
        pass

    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        pass

    def export_settings(self, file_path: Path) -> bool:
        """Export settings to a file."""
        pass

    def import_settings(self, file_path: Path) -> bool:
        """Import settings from a file."""
        pass

    def validate_settings(self) -> List[str]:
        """Validate current settings and return any errors."""
        pass


class IEventBus(Protocol):
    """
    Service interface for event communication.

    Provides decoupled communication between launcher components
    following the observer pattern for clean architecture.
    """

    def publish(self, event_type: str, data: Any = None) -> None:
        """Publish an event."""
        pass

    def subscribe(self, event_type: str, handler: callable) -> str:
        """Subscribe to an event type and return subscription ID."""
        pass

    def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from an event."""
        pass

    def clear_subscriptions(self, event_type: Optional[str] = None) -> None:
        """Clear subscriptions for a specific event type or all events."""
        pass
