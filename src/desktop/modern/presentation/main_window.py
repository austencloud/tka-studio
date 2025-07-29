"""
TKA Main Window - Extracted from main.py for better organization

This module contains the main window class that was previously embedded in main.py.
Extracted to follow Single Responsibility Principle and reduce main.py complexity.
"""

import logging
from typing import TYPE_CHECKING, Optional

from PyQt6.QtWidgets import QApplication, QMainWindow

if TYPE_CHECKING:
    from desktop.modern.presentation.components.ui.splash_screen import SplashScreen


class TKAMainWindow(QMainWindow):
    """
    Main application window for TKA.

    Handles window lifecycle, state persistence, and orchestrates the main UI components.
    """

    def __init__(
        self,
        container=None,
        splash_screen: Optional["SplashScreen"] = None,
        target_screen=None,
    ):
        super().__init__()

        # Hide window immediately to prevent temporary flash
        self.hide()

        self.container = container
        self.splash = splash_screen
        self.target_screen = target_screen

        # Initialize Modern State Persistence System
        self._setup_modern_state_persistence()

        if self.container:
            self._initialize_application_orchestrator()
            self._connect_state_persistence_events()
            self._setup_settings_service()
            self._restore_tab_state()

    def _initialize_application_orchestrator(self) -> None:
        """Initialize the application orchestrator and main UI."""
        from desktop.modern.application.services.core.application_orchestrator import (
            ApplicationOrchestrator,
        )

        # Create orchestrator with default services
        self.orchestrator = ApplicationOrchestrator()
        self.tab_widget = self.orchestrator.initialize_application(
            self,
            self.splash,
            self.target_screen,
        )

    def _setup_modern_state_persistence(self) -> None:
        """Set up the modern state persistence system."""
        try:
            from PyQt6.QtWidgets import QApplication

            from desktop.modern.application.services.core.application_state_manager import (
                integrate_with_application_startup,
            )
            from desktop.modern.application.services.settings.modern_settings_service import (
                ModernSettingsService,
            )
            from desktop.modern.core.dependency_injection.settings_service_registration import (
                create_configured_settings_container,
            )

            # Create DI container with all settings services
            self.settings_container = create_configured_settings_container(
                "TKA", "KineticConstructor"
            )

            # Get the settings service for immediate use
            self.settings_service = self.settings_container.resolve(
                ModernSettingsService
            )

            # Integrate with Qt application lifecycle
            self.state_manager = integrate_with_application_startup(
                self.settings_container,
                self,  # main window
                QApplication.instance(),  # Qt app
            )

            print("✅ Modern state persistence system activated!")

        except Exception as e:
            print(f"⚠️ Failed to initialize modern state persistence: {e}")
            import traceback

            traceback.print_exc()
            # Continue without state persistence rather than crash
            self.settings_container = None
            self.settings_service = None
            self.state_manager = None

    def _setup_settings_service(self) -> None:
        """Create simple settings service for tab restoration."""
        try:
            from desktop.modern.application.services.settings.modern_settings_service import (
                ModernSettingsService,
            )
            from desktop.modern.core.dependency_injection.settings_service_registration import (
                create_configured_settings_container,
            )

            # Create a minimal settings container just for tab state
            if not hasattr(self, "settings_service"):
                settings_container = create_configured_settings_container(
                    "TKA", "KineticConstructor"
                )
                self.settings_service = settings_container.resolve(
                    ModernSettingsService
                )
                print("✅ Created minimal settings service for tab restoration")

        except Exception as e:
            print(f"⚠️ Failed to create settings service: {e}")

    def _connect_state_persistence_events(self) -> None:
        """Connect UI events to state persistence system."""
        try:
            if not hasattr(self, "state_manager") or not self.state_manager:
                return

            # Connect tab widget changes if available
            if hasattr(self, "tab_widget") and self.tab_widget:
                # Connect tab change events with proper state saving
                if hasattr(self.tab_widget, "currentChanged"):
                    self.tab_widget.currentChanged.connect(self._on_tab_changed)

                # Connect other tab widget events if they exist
                if hasattr(self.tab_widget, "tabBarClicked"):
                    self.tab_widget.tabBarClicked.connect(
                        lambda: self.state_manager.mark_user_interaction("tab_click")
                    )

            print("🔗 Connected state persistence events to UI")

        except Exception as e:
            print(f"⚠️ Failed to connect state persistence events: {e}")

    def _on_tab_changed(self, index):
        """Handle tab change events and save current tab state."""
        try:
            if hasattr(self, "settings_service") and self.settings_service:
                # Save current tab index and name
                self.settings_service.execute_setting_command(
                    "ui_state", "current_tab_index", index
                )

                # Also save tab name for human-readable restoration
                if hasattr(self, "tab_widget") and self.tab_widget:
                    tab_name = self.tab_widget.tabText(index)
                    self.settings_service.execute_setting_command(
                        "ui_state", "current_tab_name", tab_name
                    )
                    print(f"💾 Saved tab state: index={index}, name='{tab_name}'")

            # Mark user interaction for auto-save
            if hasattr(self, "state_manager") and self.state_manager:
                self.state_manager.mark_user_interaction("tab_change")

        except Exception as e:
            print(f"⚠️ Failed to save tab state: {e}")

    def _restore_tab_state(self):
        """Restore the previously active tab on application startup."""
        try:
            if not hasattr(self, "settings_service") or not self.settings_service:
                print("⚠️ No settings service available for tab restoration")
                return

            if not hasattr(self, "tab_widget") or not self.tab_widget:
                print("⚠️ No tab widget available for tab restoration")
                return

            # Get the last saved tab index
            saved_tab_index = self.settings_service.query_setting(
                "ui_state", "current_tab_index", 0
            )
            saved_tab_name = self.settings_service.query_setting(
                "ui_state", "current_tab_name", ""
            )

            print(f"🔄 Restoring tab: index={saved_tab_index}, name='{saved_tab_name}'")

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
            from desktop.modern.presentation.components.menu_bar.menu_bar_widget import (
                MenuBarWidget,
            )

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
        return getattr(self, "settings_service", None)

    def show(self):
        """Override show to ensure tab widget is properly displayed."""
        super().show()

        # Mark user interaction for state persistence
        if hasattr(self, "state_manager") and self.state_manager:
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
        """Handle window resize events."""
        super().resizeEvent(a0)

        # Mark user interaction for state persistence
        if hasattr(self, "state_manager") and self.state_manager:
            self.state_manager.mark_user_interaction("window_resize")

        if hasattr(self, "orchestrator"):
            self.orchestrator.handle_window_resize(self)
