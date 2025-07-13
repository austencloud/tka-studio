"""
UI Setup Manager

Pure service for managing UI component setup and initialization.
Extracted from KineticConstructorModern to follow single responsibility principle.

PROVIDES:
- Main window UI setup
- Menu bar and navigation integration
- Tab widget creation and configuration
- Header layout with title and settings
- Construct tab loading with progress tracking
- Component styling and layout management
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Optional

from core.interfaces.session_services import ISessionStateTracker
from presentation.components.menu_bar import MenuBarWidget
from presentation.tabs.construct.construct_tab_widget import ConstructTabWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QLabel,
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .tab_management import ITabManagementService, TabManagementService

if TYPE_CHECKING:
    from core.dependency_injection.di_container import DIContainer


class IUISetupManager(ABC):
    """Interface for UI setup operations."""

    @abstractmethod
    def setup_main_ui(
        self,
        main_window: QMainWindow,
        container: "DIContainer",
        progress_callback: Optional[Callable] = None,
    ) -> QTabWidget:
        """Setup the main UI components and return the tab widget."""

    @abstractmethod
    def create_tab_widget(self) -> QTabWidget:
        """Create and configure the main tab widget."""


class UISetupManager(IUISetupManager):
    """
    Pure service for UI setup and component management.

    Handles all UI initialization without business logic dependencies.
    Uses clean separation of concerns following TKA architecture.
    """

    def __init__(self):
        """Initialize UI setup manager."""
        self.tab_widget: Optional[QTabWidget] = None
        self.menu_bar: Optional[MenuBarWidget] = None
        self.tab_management_service: ITabManagementService = TabManagementService()

    def setup_main_ui(
        self,
        main_window: QMainWindow,
        container: "DIContainer",
        progress_callback: Optional[Callable] = None,
        session_service=None,
    ) -> QTabWidget:
        """Setup the main UI components and return the tab widget."""
        if progress_callback:
            progress_callback(65, "Creating central widget...")

        # Create central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        main_window.setCentralWidget(central_widget)

        if progress_callback:
            progress_callback(67, "Setting up main layout...")

        # Create main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for menu bar
        layout.setSpacing(0)

        if progress_callback:
            progress_callback(68, "Creating menu bar...")

        # Create menu bar with size provider
        size_provider = lambda: main_window.size()
        self.menu_bar = MenuBarWidget(
            parent=central_widget, size_provider=size_provider
        )
        layout.addWidget(self.menu_bar)

        if progress_callback:
            progress_callback(70, "Creating tab interface...")

        # Create tab widget
        self.tab_widget = self.create_tab_widget()
        layout.addWidget(self.tab_widget)

        if progress_callback:
            progress_callback(72, "Initializing tab management...")

        # Initialize tab management service
        self.tab_management_service.initialize_tabs(self.tab_widget, container)

        if progress_callback:
            progress_callback(75, "Loading construct tab...")

        # Load construct tab completely during splash screen phase
        self._load_construct_tab(container, progress_callback, session_service)

        if progress_callback:
            progress_callback(90, "Connecting menu bar signals...")

        # Connect menu bar to tab management
        self._connect_menu_bar_signals()

        if progress_callback:
            progress_callback(95, "Finalizing interface...")

        return self.tab_widget

    def create_tab_widget(self) -> QTabWidget:
        """Create and configure the main tab widget."""
        tab_widget = QTabWidget()
        tab_widget.setTabPosition(QTabWidget.TabPosition.North)

        # Hide the tab bar since we use the menu bar navigation instead
        tab_widget.tabBar().setVisible(False)

        tab_widget.setStyleSheet(
            """
            QTabWidget::pane {
                border: none;
                background: transparent;
                margin-top: 0px;
            }
        """
        )
        return tab_widget

    def _load_construct_tab(
        self,
        container: "DIContainer",
        progress_callback: Optional[Callable] = None,
        session_service=None,
    ) -> None:
        """Load construct tab with granular progress updates."""
        try:
            # Step 1: Initialize container (76-78%)
            if progress_callback:
                progress_callback(76, "Preparing construct tab dependencies...")

            if progress_callback:
                progress_callback(78, "Loading pictograph dataset...")

            # Lazy import construct tab only when loading
            from presentation.tabs.construct.construct_tab_widget import (
                ConstructTabWidget,
            )

            if progress_callback:
                progress_callback(80, "Initializing construct tab services...")

            if progress_callback:
                progress_callback(82, "Setting up option picker components...")

            # Step 3: Create widget with progress callback (84-90%)
            if progress_callback:
                progress_callback(84, "Creating construct tab widget...")

            # Create internal progress callback with enhanced feedback
            def internal_progress_callback(step: str, progress: float):
                if progress_callback:
                    # Map internal progress (0.0-1.0) to our range (84-90%)
                    mapped_progress = 84 + (progress * 6)  # 6% range for internal steps
                    progress_callback(int(mapped_progress), f"🔧 {step}")

            if progress_callback:
                progress_callback(86, "Initializing UI components...")

            # Create construct tab
            construct_tab = ConstructTabWidget(
                container, progress_callback=internal_progress_callback
            )

            # CRITICAL: Connect construct tab to session service for auto-save
            self._connect_construct_tab_to_session(construct_tab, session_service)

            if progress_callback:
                progress_callback(88, "Configuring construct tab styling...")

            construct_tab.setStyleSheet("background: transparent;")

            if progress_callback:
                progress_callback(90, "Adding construct tab to interface...")

            tab_index = self.tab_widget.addTab(construct_tab, "🔧 Construct")

            # Register construct tab with tab management service
            self.tab_management_service.register_existing_tab(
                "construct", construct_tab, tab_index
            )

            # WINDOW MANAGEMENT FIX: Keep widgets hidden during splash screen
            # They will be shown when the main window is displayed
            self.tab_widget.hide()
            self.tab_widget.setVisible(False)
            construct_tab.hide()
            construct_tab.setVisible(False)

            # Set construct tab as current tab
            self.tab_widget.setCurrentIndex(0)

            if progress_callback:
                progress_callback(92, "Construct tab fully loaded and ready!")

        except Exception as e:
            import traceback

            print(f"⚠️ Error loading construct tab: {e}")
            print(f"🔍 Full traceback:")
            traceback.print_exc()
            if progress_callback:
                progress_callback(85, "Construct tab load failed, using fallback...")

            # Create fallback placeholder
            fallback_placeholder = QLabel("🚧 Construct tab loading failed...")
            fallback_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_placeholder.setStyleSheet(
                "color: white; font-size: 14px; background: transparent;"
            )
            self.tab_widget.addTab(fallback_placeholder, "🔧 Construct")

    def _connect_construct_tab_to_session(
        self,
        construct_tab: ConstructTabWidget,
        session_state_tracker: ISessionStateTracker,
    ) -> None:
        """Connect construct tab sequence modifications to session service for auto-save."""
        try:
            if not session_state_tracker:
                return

            # Connect sequence modification signals to session service
            def on_sequence_modified(sequence_data):
                """Handle sequence modification from construct tab."""
                # Update session with current sequence
                sequence_id = (
                    sequence_data.id
                    if hasattr(sequence_data, "id")
                    else str(sequence_data)
                )
                session_state_tracker.update_current_sequence(
                    sequence_data, sequence_id
                )

            # Connect the signal
            construct_tab.sequence_modified.connect(on_sequence_modified)

        except Exception as e:
            print(f"⚠️ Failed to connect construct tab to session service: {e}")

    def _create_settings_button(self):
        """Create settings button using dependency injection."""
        from presentation.components.ui.settings.settings_button import SettingsButton

        return SettingsButton()

    def _show_settings(self, main_window: QMainWindow) -> None:
        """Open the settings dialog using dependency injection."""
        try:
            from core.dependency_injection.di_container import get_container
            from core.interfaces.core_services import IUIStateManager
            from presentation.components.ui.settings.settings_dialog import (
                SettingsDialog,
            )

            # Get UI state service from container
            container = get_container()
            ui_state_service = container.resolve(IUIStateManager)
            dialog = SettingsDialog(ui_state_service, main_window, container)

            # Connect to settings changes if needed
            dialog.settings_changed.connect(
                lambda key, value: self._on_setting_changed(key, value, main_window)
            )

            # Show the dialog
            _ = dialog.exec()

            # Clean up dialog resources after it closes
            dialog.deleteLater()

        except Exception as e:
            print(f"⚠️ Failed to open settings dialog: {e}")
            import traceback

            traceback.print_exc()

    def _on_setting_changed(self, key: str, value, main_window: QMainWindow) -> None:
        """Handle settings changes from the dialog."""
        print(f"🔧 Setting changed: {key} = {value}")

        # Handle background changes
        if key == "background_type":
            # Delegate to background manager
            from application.services.ui.background_manager import BackgroundManager

            background_manager = BackgroundManager()
            background_manager.apply_background_change(main_window, value)

    def _connect_menu_bar_signals(self):
        """Connect menu bar signals to tab management."""
        if self.menu_bar and self.tab_management_service:
            # Connect tab change signal
            self.menu_bar.tab_changed.connect(self.tab_management_service.switch_to_tab)

            # Connect settings signal to actually open the settings dialog
            self.menu_bar.settings_requested.connect(self._handle_settings_request)

    def _handle_settings_request(self):
        """Handle settings button click by opening the settings dialog."""
        print("🔧 Settings button clicked - attempting to open dialog...")
        try:
            from core.dependency_injection.di_container import get_container
            from core.interfaces.core_services import IUIStateManager
            from presentation.components.ui.settings.settings_dialog import (
                SettingsDialog,
            )

            print("🔧 Imports successful, finding main window...")

            # Get main window reference
            main_window = None
            if self.menu_bar and self.menu_bar.parent():
                widget = self.menu_bar.parent()
                while widget and not isinstance(widget, QMainWindow):
                    widget = widget.parent()
                main_window = widget

            if not main_window:
                print("⚠️ Could not find main window for settings dialog")
                return

            print("🔧 Main window found, getting container...")

            # Get UI state service from container
            container = get_container()
            ui_state_service = container.resolve(IUIStateManager)
            
            print("🔧 Creating settings dialog...")
            dialog = SettingsDialog(ui_state_service, main_window, container)

            # Connect to settings changes if needed
            dialog.settings_changed.connect(
                lambda key, value: self._on_setting_changed(key, value, main_window)
            )

            print("🔧 Showing settings dialog...")
            # Show the dialog
            result = dialog.exec()
            print(f"🔧 Settings dialog closed with result: {result}")

            # Clean up dialog resources after it closes
            dialog.deleteLater()

        except Exception as e:
            print(f"⚠️ Failed to open settings dialog: {e}")
            import traceback

            traceback.print_exc()
