"""
Application State Persistence Integration

Integrates the modern settings service with the existing TKA application
architecture, providing seamless state persistence and restoration.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow

from desktop.modern.application.services.settings.modern_settings_service import (
    ModernSettingsService,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.settings_service_registration import (
    register_settings_services,
)
from desktop.modern.core.interfaces.session_services import ISessionStateTracker


logger = logging.getLogger(__name__)


class ApplicationStateManager:
    """
    High-level application state management orchestrator.

    Coordinates between the modern settings service, session tracker,
    and Qt application state to provide complete state persistence.
    """

    def __init__(
        self,
        settings_service: ModernSettingsService,
        session_tracker: ISessionStateTracker,
        main_window: Optional[QMainWindow] = None,
    ):
        self.settings_service = settings_service
        self.session_tracker = session_tracker
        self.main_window = main_window

        # Auto-save timer
        self._auto_save_timer = QTimer()
        self._auto_save_timer.setSingleShot(True)
        self._auto_save_timer.timeout.connect(self._perform_auto_save)

        # Auto-save configuration
        self.auto_save_enabled = True
        self.auto_save_delay_ms = 5000  # 5 seconds after last interaction

        logger.info("Initialized ApplicationStateManager")

    def initialize_application_state(self) -> bool:
        """
        Initialize application state on startup.

        This method should be called during application initialization
        to restore the previous session state.

        Returns:
            True if state was successfully restored, False otherwise
        """
        try:
            # Attempt to restore previous state
            restored_memento = self.settings_service.restore_application_state()

            if restored_memento:
                # Apply window state if main window is available
                if self.main_window and restored_memento.window_geometry:
                    try:
                        self.main_window.restoreGeometry(
                            restored_memento.window_geometry
                        )
                        if restored_memento.window_state:
                            self.main_window.restoreState(restored_memento.window_state)
                        logger.debug("Restored window geometry and state")
                    except Exception as e:
                        logger.warning(f"Failed to restore window state: {e}")

                # Restore session state
                session_result = self.session_tracker.load_session_state()
                if session_result.success and session_result.session_restored:
                    pass  # Session restored successfully

                return True
            logger.info("🆕 Starting with clean application state")
            return False

        except Exception as e:
            logger.error(f"❌ Failed to initialize application state: {e}")
            return False

    def save_application_state(self, current_tab: str = None) -> bool:
        """
        Save complete application state.

        Args:
            current_tab: Currently active tab (if known)

        Returns:
            True if state was successfully saved
        """
        try:
            # Determine current tab if not provided
            if current_tab is None:
                current_tab = self._determine_current_tab()

            # Get window state if main window is available
            window_geometry = None
            window_state = None

            if self.main_window:
                try:
                    window_geometry = self.main_window.saveGeometry()
                    window_state = self.main_window.saveState()
                except Exception as e:
                    logger.warning(f"Failed to save window state: {e}")

            # Save complete application state
            success = self.settings_service.save_application_state(
                current_tab, window_geometry, window_state
            )

            if success:
                logger.debug("💾 Application state saved successfully")
            else:
                logger.warning("⚠️ Failed to save application state")

            return success

        except Exception as e:
            logger.error(f"❌ Error saving application state: {e}")
            return False

    def mark_user_interaction(self, interaction_type: str = "general") -> None:
        """
        Mark a user interaction to trigger auto-save.

        Args:
            interaction_type: Type of interaction for logging
        """
        try:
            # Mark interaction in session tracker
            self.session_tracker.mark_interaction()

            # Trigger auto-save timer if enabled
            if self.auto_save_enabled:
                self._auto_save_timer.stop()
                self._auto_save_timer.start(self.auto_save_delay_ms)

            logger.debug(f"🖱️ User interaction marked: {interaction_type}")

        except Exception as e:
            logger.error(f"Failed to mark user interaction: {e}")

    def force_save_state(self) -> bool:
        """
        Force immediate state save (bypassing auto-save timer).

        Returns:
            True if state was successfully saved
        """
        try:
            self._auto_save_timer.stop()
            return self._perform_auto_save()
        except Exception as e:
            logger.error(f"Failed to force save state: {e}")
            return False

    def set_main_window(self, main_window: QMainWindow) -> None:
        """
        Set the main window reference for window state management.

        Args:
            main_window: The main application window
        """
        self.main_window = main_window
        logger.debug("Main window reference set for state management")

    def set_auto_save_enabled(self, enabled: bool) -> None:
        """
        Enable or disable auto-save functionality.

        Args:
            enabled: Whether to enable auto-save
        """
        self.auto_save_enabled = enabled
        self.session_tracker.set_auto_save_enabled(enabled)

        if not enabled:
            self._auto_save_timer.stop()

        logger.info(f"Auto-save {'enabled' if enabled else 'disabled'}")

    def export_application_state(self, file_path: Optional[Path] = None) -> bool:
        """
        Export complete application state to a file.

        Args:
            file_path: Optional custom export path

        Returns:
            True if export was successful
        """
        try:
            # Create current state memento
            current_tab = self._determine_current_tab()

            window_geometry = None
            window_state = None
            if self.main_window:
                window_geometry = self.main_window.saveGeometry()
                window_state = self.main_window.saveState()

            memento = self.settings_service.create_state_memento(
                current_tab, window_geometry, window_state
            )

            # Save memento to file
            success = self.settings_service.save_state_memento(memento, file_path)

            if success:
                logger.info(
                    f"📤 Application state exported to {file_path or 'default location'}"
                )

            return success

        except Exception as e:
            logger.error(f"Failed to export application state: {e}")
            return False

    def import_application_state(self, file_path: Path) -> bool:
        """
        Import application state from a file.

        Args:
            file_path: Path to the state file

        Returns:
            True if import was successful
        """
        try:
            # Load memento from file
            memento = self.settings_service.load_state_memento(file_path)

            if not memento:
                logger.warning("No valid state found in import file")
                return False

            # Restore from memento
            success = self.settings_service.restore_from_memento(memento)

            if success:
                logger.info(f"📥 Application state imported from {file_path}")

                # Apply window state if available
                if self.main_window and memento.window_geometry:
                    self.main_window.restoreGeometry(memento.window_geometry)
                    if memento.window_state:
                        self.main_window.restoreState(memento.window_state)

            return success

        except Exception as e:
            logger.error(f"Failed to import application state: {e}")
            return False

    def get_state_statistics(self) -> dict:
        """
        Get statistics about the current state management.

        Returns:
            Dictionary of state management statistics
        """
        try:
            current_session = self.session_tracker.get_current_session_state()

            stats = {
                "auto_save_enabled": self.auto_save_enabled,
                "session_id": current_session.session_id if current_session else None,
                "last_interaction": (
                    current_session.last_interaction.isoformat()
                    if current_session
                    else None
                ),
                "settings_service_active": self.settings_service is not None,
                "main_window_connected": self.main_window is not None,
                "auto_save_pending": self._auto_save_timer.isActive(),
            }

            return stats

        except Exception as e:
            logger.error(f"Failed to get state statistics: {e}")
            return {"error": str(e)}

    def _perform_auto_save(self) -> bool:
        """Perform auto-save operation (called by timer)."""
        try:
            current_tab = self._determine_current_tab()
            success = self.save_application_state(current_tab)

            if success:
                logger.debug("🔄 Auto-save completed")
            else:
                logger.warning("⚠️ Auto-save failed")

            return success

        except Exception as e:
            logger.error(f"Auto-save error: {e}")
            return False

    def _determine_current_tab(self) -> str:
        """Determine the currently active tab."""
        try:
            # Try to get from settings first
            current_tab = self.settings_service.get_current_tab()

            # If that fails, try to determine from main window
            if not current_tab and self.main_window:
                # Look for tab widget in main window
                tab_widget = self.main_window.findChild(object, "main_tab_widget")
                if tab_widget and hasattr(tab_widget, "currentWidget"):
                    current_widget = tab_widget.currentWidget()
                    if current_widget and hasattr(current_widget, "objectName"):
                        current_tab = current_widget.objectName()

            # Fallback to default
            return current_tab or "construct"

        except Exception as e:
            logger.error(f"Failed to determine current tab: {e}")
            return "construct"


def create_application_state_manager(
    container: DIContainer, main_window: Optional[QMainWindow] = None
) -> ApplicationStateManager:
    """
    Create and configure an application state manager from DI container.

    Args:
        container: DI container with registered services
        main_window: Optional main window reference

    Returns:
        Configured ApplicationStateManager instance

    Raises:
        Exception: If required services are not available
    """
    try:
        # Ensure settings services are registered
        register_settings_services(container)

        # Resolve required services
        settings_service = container.resolve(ModernSettingsService)
        session_tracker = container.resolve(ISessionStateTracker)

        # Create and return manager
        manager = ApplicationStateManager(
            settings_service, session_tracker, main_window
        )

        logger.info("✅ Created ApplicationStateManager with DI container")
        return manager

    except Exception as e:
        logger.error(f"❌ Failed to create ApplicationStateManager: {e}")
        raise


def integrate_with_application_startup(
    container: DIContainer, main_window: QMainWindow, app: QApplication
) -> ApplicationStateManager:
    """
    Integrate state persistence with application startup sequence.

    This function should be called during application initialization
    to set up complete state persistence.

    Args:
        container: DI container with registered services
        main_window: Main application window
        app: QApplication instance

    Returns:
        Configured ApplicationStateManager instance
    """
    try:
        # Create state manager
        state_manager = create_application_state_manager(container, main_window)

        # Initialize application state
        state_restored = state_manager.initialize_application_state()

        # Connect to application events for auto-save
        def on_application_about_to_quit():
            """Save state when application is about to quit."""
            logger.info("💾 Saving application state before quit...")
            state_manager.force_save_state()

        app.aboutToQuit.connect(on_application_about_to_quit)

        # Set up periodic state saving as backup
        backup_timer = QTimer()
        backup_timer.timeout.connect(lambda: state_manager.force_save_state())
        backup_timer.start(30000)  # Save every 30 seconds as backup

        return state_manager

    except Exception as e:
        logger.error(f"❌ Failed to integrate state persistence: {e}")
        raise


# Utility functions for easy integration
def setup_state_persistence_for_window(
    main_window: QMainWindow, container: DIContainer
) -> ApplicationStateManager:
    """
    Quick setup function for adding state persistence to a main window.

    Args:
        main_window: The main application window
        container: DI container with services

    Returns:
        Configured ApplicationStateManager
    """
    app = QApplication.instance()
    return integrate_with_application_startup(container, main_window, app)


def mark_user_interaction_globally(interaction_type: str = "general") -> None:
    """
    Global function to mark user interactions from anywhere in the application.

    This requires the state manager to be stored globally or accessible
    through a service locator pattern.

    Args:
        interaction_type: Type of interaction for logging
    """
    try:
        # This would typically get the state manager from a global registry
        # For now, we'll document the pattern
        logger.debug(f"Global interaction marked: {interaction_type}")
    except Exception as e:
        logger.error(f"Failed to mark global interaction: {e}")
