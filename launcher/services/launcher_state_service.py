"""
Launcher State Service Implementation.

Manages the immutable state of the launcher including mode switching,
geometry persistence, and application state tracking.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from desktop.modern.core.interfaces import ILauncherStateService, ISettingsService
from desktop.modern.domain.models import (
    ApplicationCategory,
    ApplicationData,
    ApplicationStatus,
    LauncherState,
    LaunchMode,
    WindowGeometry,
)

logger = logging.getLogger(__name__)


class LauncherStateService(ILauncherStateService):
    """
    Service for managing launcher state with immutable data patterns.

    Follows TKA's clean architecture principles with dependency injection
    and immutable state management.
    """

    def __init__(self, settings_service: Optional[ISettingsService] = None):
        """Initialize the launcher state service."""
        self._settings_service = settings_service
        self._current_state = self._create_initial_state()

        # Load persisted state if available
        if self._settings_service:
            self._current_state = self.load_state()

    def get_current_state(self) -> LauncherState:
        """Get the current launcher state."""
        return self._current_state

    def update_state(self, state: LauncherState) -> None:
        """Update the launcher state."""
        self._current_state = state
        logger.debug(
            f"State updated: mode={state.mode.value}, apps={len(state.applications)}"
        )

    def switch_mode(self, mode: LaunchMode) -> LauncherState:
        """Switch launcher mode and return new state."""
        new_state = self._current_state.with_mode(mode)
        self.update_state(new_state)

        # Persist the mode change
        if self._settings_service:
            self._settings_service.set_setting("launch_mode", mode.value)

        logger.info(f"Switched to {mode.value} mode")
        return new_state

    def save_window_geometry(
        self, geometry: WindowGeometry, mode: LaunchMode
    ) -> LauncherState:
        """Save window geometry for the specified mode."""
        if mode == LaunchMode.WINDOW:
            new_state = self._current_state.with_window_geometry(geometry)
        else:
            new_state = self._current_state.with_docked_geometry(geometry)

        self.update_state(new_state)

        # Persist geometry
        if self._settings_service:
            geometry_key = f"{mode.value}_geometry"
            self._settings_service.set_setting(geometry_key, geometry.to_dict())

        logger.debug(f"Saved {mode.value} geometry: {geometry.width}x{geometry.height}")
        return new_state

    def get_window_geometry(self, mode: LaunchMode) -> Optional[WindowGeometry]:
        """Get saved window geometry for the specified mode."""
        if mode == LaunchMode.WINDOW:
            return self._current_state.window_geometry
        else:
            return self._current_state.docked_geometry

    def update_application_status(
        self, app_id: str, status: ApplicationStatus, process_id: Optional[int] = None
    ) -> LauncherState:
        """Update application status and return new state."""
        new_state = self._current_state.with_application_status(
            app_id, status, process_id
        )
        self.update_state(new_state)

        logger.debug(f"Updated app {app_id} status to {status.value}")
        return new_state

    def persist_state(self) -> None:
        """Persist current state to storage."""
        if not self._settings_service:
            logger.warning("No settings service available for state persistence")
            return

        try:
            # Persist core state
            self._settings_service.set_setting(
                "launch_mode", self._current_state.mode.value
            )
            self._settings_service.set_setting(
                "target_screen_index", self._current_state.target_screen_index
            )
            self._settings_service.set_setting(
                "search_query", self._current_state.search_query
            )
            self._settings_service.set_setting(
                "first_run", self._current_state.first_run
            )
            self._settings_service.set_setting(
                "total_launches", self._current_state.total_launches
            )

            # Persist geometries
            if self._current_state.window_geometry:
                self._settings_service.set_setting(
                    "window_geometry", self._current_state.window_geometry.to_dict()
                )

            if self._current_state.docked_geometry:
                self._settings_service.set_setting(
                    "docked_geometry", self._current_state.docked_geometry.to_dict()
                )

            # Persist application states (only runtime state, not full app data)
            app_states = {}
            for app_id, app in self._current_state.applications.items():
                app_states[app_id] = {
                    "launch_count": app.launch_count,
                    "last_launched": app.last_launched,
                    "is_favorite": app.is_favorite,
                    "display_order": app.display_order,
                }
            self._settings_service.set_setting("application_states", app_states)

            logger.info("Launcher state persisted successfully")

        except Exception as e:
            logger.error(f"Failed to persist launcher state: {e}")

    def load_state(self) -> LauncherState:
        """Load state from storage."""
        if not self._settings_service:
            logger.warning("No settings service available for state loading")
            return self._create_initial_state()

        try:
            # Load core state
            mode_str = self._settings_service.get_setting("launch_mode", "window")
            mode = (
                LaunchMode(mode_str)
                if mode_str in [m.value for m in LaunchMode]
                else LaunchMode.WINDOW
            )

            target_screen = self._settings_service.get_setting("target_screen_index", 0)
            search_query = self._settings_service.get_setting("search_query", "")
            first_run = self._settings_service.get_setting("first_run", True)
            total_launches = self._settings_service.get_setting("total_launches", 0)

            # Load geometries
            window_geometry = None
            window_geom_data = self._settings_service.get_setting("window_geometry")
            if window_geom_data:
                window_geometry = WindowGeometry.from_dict(window_geom_data)

            docked_geometry = None
            docked_geom_data = self._settings_service.get_setting("docked_geometry")
            if docked_geom_data:
                docked_geometry = WindowGeometry.from_dict(docked_geom_data)

            # Create state with loaded data
            state = LauncherState(
                mode=mode,
                window_geometry=window_geometry,
                docked_geometry=docked_geometry,
                target_screen_index=target_screen,
                search_query=search_query,
                first_run=first_run,
                total_launches=total_launches,
                applications=self._current_state.applications,  # Keep current apps
            )

            return state

        except Exception as e:
            logger.error(f"Failed to load launcher state: {e}")
            return self._create_initial_state()

    def _create_initial_state(self) -> LauncherState:
        """Create the initial launcher state with defaults."""
        return LauncherState(
            mode=LaunchMode.WINDOW,
            target_screen_index=0,
            first_run=True,
            total_launches=0,
        )

    def add_application(self, app: ApplicationData) -> LauncherState:
        """Add an application to the state."""
        new_state = self._current_state.with_application(app)
        self.update_state(new_state)
        return new_state

    def remove_application(self, app_id: str) -> LauncherState:
        """Remove an application from the state."""
        if app_id not in self._current_state.applications:
            return self._current_state

        new_apps = self._current_state.applications.copy()
        del new_apps[app_id]
        new_state = self._current_state.update(applications=new_apps)
        self.update_state(new_state)
        return new_state

    def increment_total_launches(self) -> LauncherState:
        """Increment the total launch count."""
        new_state = self._current_state.update(
            total_launches=self._current_state.total_launches + 1
        )
        self.update_state(new_state)
        return new_state

    def mark_not_first_run(self) -> LauncherState:
        """Mark that this is no longer the first run."""
        if not self._current_state.first_run:
            return self._current_state

        new_state = self._current_state.update(first_run=False)
        self.update_state(new_state)

        if self._settings_service:
            self._settings_service.set_setting("first_run", False)

        return new_state
