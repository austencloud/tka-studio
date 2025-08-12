"""
UI Setup Manager - REFACTORED VERSION

REFACTORED:
- ✅ Uses TabFactory for consistent tab creation
- ✅ Uses UIErrorRecoveryService for all fallback UI
- ✅ Simplified _load_components method (50 lines instead of 100+)
- ✅ Removed duplicate error handling patterns
- ✅ Single responsibility: UI structure setup only

PROVIDES:
- Single, clean UI setup flow
- Consistent error handling via dedicated services
- Proper separation of concerns
- Testable components
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
import logging
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget

from desktop.modern.core.error_handling import ErrorSeverity, StandardErrorHandler
from desktop.modern.presentation.components.menu_bar import MenuBarWidget

from .error_recovery import UIErrorRecoveryService
from .tab_factory import TabFactory
from .tab_management import ITabManagementService, TabManagementService


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class IUISetupManager(ABC):
    """Interface for UI setup operations."""

    @abstractmethod
    def setup_main_ui(
        self,
        main_window: QMainWindow,
        container: DIContainer,
        progress_callback: Callable | None = None,
        session_service=None,
    ) -> QTabWidget:
        """Setup the main UI components and return the tab widget."""


class UISetupManager(IUISetupManager):
    """
    REFACTORED UI setup manager using TabFactory and UIErrorRecoveryService.

    Single responsibility: Setup main UI structure and coordinate component loading.
    """

    def __init__(self):
        """Initialize with focused services."""
        self.tab_widget: QTabWidget | None = None
        self.menu_bar: MenuBarWidget | None = None
        self.tab_management_service: ITabManagementService = TabManagementService()
        self.tab_factory = TabFactory()
        self.error_recovery = UIErrorRecoveryService()

    def setup_main_ui(
        self,
        main_window: QMainWindow,
        container: DIContainer,
        progress_callback: Callable | None = None,
        session_service=None,
    ) -> QTabWidget:
        """
        Setup main UI with clean, linear flow and proper error handling.

        REFACTORED: Uses dedicated services for tab creation and error recovery.
        """
        try:
            # Step 1: Create main structure
            self._create_main_structure(main_window, progress_callback)

            # Step 2: Initialize tab management
            self._initialize_tab_management(container, progress_callback)

            # Step 3: Load components
            self._load_components(container, session_service, progress_callback)

            # Step 4: Connect signals
            self._connect_signals(progress_callback)

            return self.tab_widget

        except Exception as e:
            StandardErrorHandler.handle_ui_error(
                "UI setup",
                e,
                logger,
                fallback_action=lambda: self.error_recovery.create_fallback_main_ui(
                    main_window, "UI setup failure"
                ),
            )
            # Return the fallback UI using error recovery service
            return self.error_recovery.create_fallback_main_ui(
                main_window, "UI setup failure"
            )

    def _create_main_structure(
        self, main_window: QMainWindow, progress_callback: Callable | None = None
    ) -> None:
        """Create the basic UI structure."""
        try:
            if progress_callback:
                progress_callback(10, "Creating main UI structure...")

            # Create central widget
            central_widget = QWidget()
            central_widget.setStyleSheet("background: transparent;")
            main_window.setCentralWidget(central_widget)

            # Create main layout
            layout = QVBoxLayout(central_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            # Create menu bar
            def size_provider():
                return main_window.size()

            self.menu_bar = MenuBarWidget(
                parent=central_widget, size_provider=size_provider
            )
            layout.addWidget(self.menu_bar)

            # Create tab widget
            self.tab_widget = self._create_tab_widget()
            layout.addWidget(self.tab_widget)

        except Exception as e:
            StandardErrorHandler.handle_ui_error("main structure creation", e, logger)
            raise

    def _create_tab_widget(self) -> QTabWidget:
        """Create and configure the main tab widget."""
        tab_widget = QTabWidget()
        tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        tab_widget.tabBar().setVisible(False)  # Use menu bar navigation
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

    def _initialize_tab_management(
        self, container: DIContainer, progress_callback: Callable | None = None
    ) -> None:
        """Initialize tab management service."""
        try:
            if progress_callback:
                progress_callback(30, "Initializing tab management...")

            self.tab_management_service.initialize_tabs(self.tab_widget, container)

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Tab management initialization", e, logger, ErrorSeverity.WARNING
            )

    def _load_components(
        self,
        container: DIContainer,
        session_service,
        progress_callback: Callable | None = None,
    ) -> None:
        """
        Load all UI components using TabFactory.

        REFACTORED: 20 lines instead of 100+ lines with duplicate patterns.
        """
        if progress_callback:
            progress_callback(50, "Loading components...")

        try:
            # Use TabFactory to create all tabs with consistent error handling
            tab_results = self.tab_factory.create_all_tabs(container)

            # Add all created tabs to the widget
            for tab_id, tab_info in tab_results.items():
                self.tab_widget.addTab(tab_info["widget"], tab_info["display_name"])

                # Register tab with management service
                tab_index = self.tab_widget.indexOf(tab_info["widget"])
                self.tab_management_service.register_existing_tab(
                    tab_id, tab_info["widget"], tab_index
                )

                if tab_info["success"]:
                    pass  # Tab added successfully
                else:
                    logger.warning(f"⚠️ Added {tab_id} tab in recovery mode")

            if progress_callback:
                progress_callback(75, f"Loaded {len(tab_results)} tabs")

            # CRITICAL FIX: Switch to default tab after all tabs are created
            self.tab_management_service.switch_to_tab("construct")
            logger.info("✅ Switched to default construct tab")

        except Exception as e:
            StandardErrorHandler.handle_ui_error(
                "component loading",
                e,
                logger,
                fallback_action=lambda: self._add_emergency_tab(),
            )
            # Add emergency tab if TabFactory completely fails
            self._add_emergency_tab()

        # CRITICAL FIX: Don't hide the tab widget - it should be visible
        # The tab widget needs to be visible for tabs to display properly

    def _add_emergency_tab(self) -> None:
        """Add emergency tab when TabFactory fails completely."""
        try:
            emergency_tab = self.error_recovery.create_recovery_info_tab(
                "TabFactory failure"
            )
            self.tab_widget.addTab(emergency_tab, "🚨 Emergency")
        except Exception as e:
            logger.exception(f"❌ Even emergency tab creation failed: {e}")

    def _connect_signals(self, progress_callback: Callable | None = None) -> None:
        """Connect UI signals."""
        try:
            if progress_callback:
                progress_callback(90, "Connecting signals...")

            if self.menu_bar and self.tab_management_service:
                self.menu_bar.tab_changed.connect(
                    self.tab_management_service.switch_to_tab
                )
                self.menu_bar.settings_requested.connect(self._handle_settings_request)

            # Connect generate tab to construct tab for sequence generation
            self._connect_generate_to_construct_signals()

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Signal connection", e, logger, ErrorSeverity.WARNING
            )

    def _connect_generate_to_construct_signals(self) -> None:
        """Connect generate tab signals to construct tab for sequence generation."""
        try:
            # Get the generate tab and construct tab from tab management service
            if not self.tab_management_service:
                logger.warning("Tab management service not available")
                return

            generate_tab = self.tab_management_service._tabs.get("generate")
            construct_tab = self.tab_management_service._tabs.get("construct")

            if generate_tab and construct_tab:
                # Connect sequence_generated signal to construct tab's sequence loading
                if hasattr(generate_tab, "sequence_generated") and hasattr(
                    construct_tab, "load_generated_sequence"
                ):
                    generate_tab.sequence_generated.connect(
                        construct_tab.load_generated_sequence
                    )
                    logger.info(
                        "✅ Connected generate tab to construct tab for sequence generation"
                    )
                else:
                    logger.warning(
                        "Generate or construct tab missing required methods for signal connection"
                    )
            else:
                logger.warning(
                    f"Generate tab: {generate_tab}, Construct tab: {construct_tab}"
                )

        except Exception as e:
            logger.exception(f"Failed to connect generate to construct signals: {e}")

    def _handle_settings_request(self) -> None:
        """Handle settings button click - delegate to settings service."""
        try:
            from desktop.modern.application.services.ui.settings_service import (
                SettingsService,
            )

            # Find main window
            main_window = None
            if self.menu_bar and self.menu_bar.parent():
                widget = self.menu_bar.parent()
                while widget and not isinstance(widget, QMainWindow):
                    widget = widget.parent()
                main_window = widget

            if main_window:
                settings_service = SettingsService()
                settings_service.show_settings_dialog(main_window)
            else:
                logger.warning("⚠️ Could not find main window for settings dialog")

        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Settings dialog", e, logger, ErrorSeverity.WARNING
            )
