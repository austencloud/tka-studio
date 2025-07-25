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
from presentation.tabs.construct.construct_tab import ConstructTab
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QMainWindow, QTabWidget, QVBoxLayout, QWidget

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
        session_service=None,
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

        # REVERT: Load construct tab during splash screen like it was working perfectly
        self._load_construct_tab(container, progress_callback, session_service)

        if progress_callback:
            progress_callback(90, "Connecting menu bar signals...")

        # Connect menu bar to tab management
        self._connect_menu_bar_signals()

        if progress_callback:
            progress_callback(95, "Finalizing interface...")

        return self.tab_widget

    def _create_instant_construct_tab_with_background_upgrade(
        self,
        container: "DIContainer",
        progress_callback: Optional[Callable] = None,
        session_service=None,
    ) -> None:
        """Create an instant minimal construct tab that upgrades to full version in background."""
        try:
            if progress_callback:
                progress_callback(76, "Creating instant construct tab...")

            # Create instant minimal tab
            from PyQt6.QtCore import Qt, QTimer
            from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

            instant_tab = QWidget()
            layout = QVBoxLayout(instant_tab)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Professional loading interface
            title_label = QLabel("🔧 Construct Tab")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setStyleSheet(
                """
                QLabel {
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    background: transparent;
                    padding: 20px;
                }
            """
            )

            status_label = QLabel("Initializing interface...")
            status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            status_label.setStyleSheet(
                """
                QLabel {
                    color: #888;
                    font-size: 14px;
                    background: transparent;
                    padding: 10px;
                }
            """
            )

            layout.addWidget(title_label)
            layout.addWidget(status_label)
            instant_tab.setStyleSheet("background: transparent;")

            if progress_callback:
                progress_callback(85, "Adding instant construct tab...")

            # Add to tab widget immediately
            tab_index = self.tab_widget.addTab(instant_tab, "🔧 Construct")
            self.tab_management_service.register_existing_tab(
                "construct", instant_tab, tab_index
            )

            if progress_callback:
                progress_callback(90, "Instant construct tab ready!")

            # Hide during splash screen
            self.tab_widget.hide()
            self.tab_widget.setVisible(False)

            # Enhanced background upgrade function with progress feedback
            def upgrade_to_full_construct_tab():
                try:
                    # Create progress callback for user feedback
                    def background_progress_callback(progress: int, message: str):
                        status_label.setText(f"Loading: {message} ({progress}%)")
                        print(f"🔧 Background [{progress}%]: {message}")

                    status_label.setText("Loading full interface...")
                    print("🔧 Background: Starting full construct tab loading...")

                    # Import and create real construct tab with progress feedback
                    from presentation.tabs.construct.construct_tab import (
                        ConstructTab,
                    )

                    construct_tab = ConstructTab(
                        container, progress_callback=background_progress_callback
                    )

                    # Connect to session service
                    self._connect_construct_tab_to_session(
                        construct_tab, session_service
                    )
                    construct_tab.setStyleSheet("background: transparent;")

                    # Replace instant tab with real tab
                    current_index = self.tab_widget.indexOf(instant_tab)
                    if current_index >= 0:
                        status_label.setText("Finalizing interface...")

                        self.tab_widget.removeTab(current_index)
                        new_index = self.tab_widget.insertTab(
                            current_index, construct_tab, "🔧 Construct"
                        )

                        # Register with tab management
                        self.tab_management_service.register_existing_tab(
                            "construct", construct_tab, new_index
                        )

                        # If this tab was current, keep it current
                        if self.tab_widget.currentIndex() == current_index:
                            self.tab_widget.setCurrentIndex(new_index)

                        print("✅ Background: Full construct tab loaded successfully!")

                except Exception as e:
                    print(f"❌ Background: Failed to upgrade construct tab: {e}")
                    status_label.setText("Failed to load - click to retry")

                    # Add click handler for retry
                    def retry_loading():
                        QTimer.singleShot(100, upgrade_to_full_construct_tab)

                    instant_tab.mousePressEvent = lambda event: retry_loading()
                    import traceback

                    traceback.print_exc()

            # Start background upgrade after 1 second (reduced delay for better UX)
            QTimer.singleShot(1000, upgrade_to_full_construct_tab)

        except Exception as e:
            print(f"❌ Failed to create instant construct tab: {e}")
            import traceback

            traceback.print_exc()

    def _load_construct_tab_aggressively_optimized(
        self,
        container: "DIContainer",
        progress_callback: Optional[Callable] = None,
        session_service=None,
    ) -> None:
        """Load construct tab during splash with aggressive optimizations to minimize load time."""
        try:
            if progress_callback:
                progress_callback(76, "Loading construct tab (optimized)...")

            # OPTIMIZATION 1: Import only when needed to reduce import time
            from presentation.tabs.construct.construct_tab import (
                ConstructTab,
            )

            if progress_callback:
                progress_callback(80, "Creating construct components...")

            # OPTIMIZATION 2: Temporarily reduce pool demands during construct tab creation
            # Store original pool settings
            from application.services.pictograph_pool_manager import (
                PictographPoolManager,
            )

            pool_manager = container.resolve(PictographPoolManager)

            # Temporarily disable pool expansion during construct tab loading
            original_startup_complete = pool_manager._startup_complete
            pool_manager._startup_complete = False  # Prevent pool expansion

            try:
                # Create construct tab with minimal pool usage
                construct_tab = ConstructTab(
                    container, progress_callback=progress_callback
                )

                if progress_callback:
                    progress_callback(88, "Finalizing construct tab...")

                # Connect to session service
                self._connect_construct_tab_to_session(construct_tab, session_service)
                construct_tab.setStyleSheet("background: transparent;")

                # Add to tab widget
                tab_index = self.tab_widget.addTab(construct_tab, "🔧 Construct")

                # Register with tab management service
                self.tab_management_service.register_existing_tab(
                    "construct", construct_tab, tab_index
                )

                if progress_callback:
                    progress_callback(90, "Construct tab ready!")

                # Hide during splash screen
                self.tab_widget.hide()
                self.tab_widget.setVisible(False)

            finally:
                # Restore original pool settings
                pool_manager._startup_complete = original_startup_complete

        except Exception as e:
            print(f"❌ Failed to load optimized construct tab: {e}")
            import traceback

            traceback.print_exc()

            # Fallback to minimal tab if loading fails
            if progress_callback:
                progress_callback(90, "Using fallback interface...")

    def _create_minimal_construct_tab(
        self,
        container: "DIContainer",
        progress_callback: Optional[Callable] = None,
        session_service=None,
    ) -> None:
        """Create a minimal construct tab that loads quickly and upgrades to full version on first use."""
        try:
            if progress_callback:
                progress_callback(76, "Creating minimal construct tab...")

            # Create a simple placeholder that looks like the real tab but loads instantly
            from PyQt6.QtCore import Qt
            from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

            minimal_tab = QWidget()
            layout = QVBoxLayout(minimal_tab)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Add a loading message that looks professional
            loading_label = QLabel("🔧 Construct Tab")
            loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            loading_label.setStyleSheet(
                """
                QLabel {
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    background: transparent;
                    padding: 20px;
                }
            """
            )

            # Add a subtle message
            info_label = QLabel("Loading interface components...")
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_label.setStyleSheet(
                """
                QLabel {
                    color: #888;
                    font-size: 14px;
                    background: transparent;
                    padding: 10px;
                }
            """
            )

            layout.addWidget(loading_label)
            layout.addWidget(info_label)
            minimal_tab.setStyleSheet("background: transparent;")

            # Make the entire tab clickable to load the real construct tab
            def load_full_construct_tab():
                try:
                    # Get tab index
                    tab_index = self.tab_widget.indexOf(minimal_tab)

                    # Import and create real construct tab
                    from presentation.tabs.construct.construct_tab import (
                        ConstructTab,
                    )

                    print("🔧 Loading full construct tab...")
                    construct_tab = ConstructTab(container, progress_callback=None)

                    # Connect to session service
                    self._connect_construct_tab_to_session(
                        construct_tab, session_service
                    )
                    construct_tab.setStyleSheet("background: transparent;")

                    # Replace minimal tab with real tab
                    if tab_index >= 0:
                        self.tab_widget.removeTab(tab_index)
                        new_index = self.tab_widget.insertTab(
                            tab_index, construct_tab, "🔧 Construct"
                        )
                        self.tab_widget.setCurrentIndex(new_index)

                        # Register with tab management
                        self.tab_management_service.register_existing_tab(
                            "construct", construct_tab, new_index
                        )

                        print("✅ Full construct tab loaded!")

                except Exception as e:
                    print(f"❌ Failed to load full construct tab: {e}")
                    import traceback

                    traceback.print_exc()

            # Auto-load the full construct tab after a short delay
            from PyQt6.QtCore import QTimer

            def auto_load_after_delay():
                info_label.setText("Loading full interface...")
                QTimer.singleShot(100, load_full_construct_tab)  # Load after 100ms

            # Start auto-loading after 1 second to let the UI settle
            QTimer.singleShot(1000, auto_load_after_delay)

            if progress_callback:
                progress_callback(85, "Adding minimal construct tab...")

            # Add to tab widget
            tab_index = self.tab_widget.addTab(minimal_tab, "🔧 Construct")

            # Register with tab management service
            self.tab_management_service.register_existing_tab(
                "construct", minimal_tab, tab_index
            )

            if progress_callback:
                progress_callback(88, "Minimal construct tab ready!")

            # Hide during splash screen
            self.tab_widget.hide()
            self.tab_widget.setVisible(False)

        except Exception as e:
            print(f"❌ Failed to create minimal construct tab: {e}")
            import traceback

            traceback.print_exc()

    def _load_construct_tab_optimized(
        self,
        container: "DIContainer",
        progress_callback: Optional[Callable] = None,
        session_service=None,
    ) -> None:
        """Load construct tab with optimizations to reduce loading time."""
        try:
            if progress_callback:
                progress_callback(76, "Initializing construct tab...")

            # OPTIMIZATION 1: Import only when needed
            from presentation.tabs.construct.construct_tab import (
                ConstructTab,
            )

            if progress_callback:
                progress_callback(78, "Creating construct tab components...")

            # OPTIMIZATION 2: Create construct tab with progress tracking
            construct_tab = ConstructTab(container, progress_callback=progress_callback)

            if progress_callback:
                progress_callback(85, "Configuring construct tab...")

            # Connect to session service
            self._connect_construct_tab_to_session(construct_tab, session_service)
            construct_tab.setStyleSheet("background: transparent;")

            if progress_callback:
                progress_callback(88, "Adding construct tab to interface...")

            # Add to tab widget
            tab_index = self.tab_widget.addTab(construct_tab, "🔧 Construct")

            # Register with tab management service
            self.tab_management_service.register_existing_tab(
                "construct", construct_tab, tab_index
            )

            if progress_callback:
                progress_callback(90, "Construct tab ready!")

            # OPTIMIZATION 3: Hide widgets during splash screen
            self.tab_widget.hide()
            self.tab_widget.setVisible(False)

        except Exception as e:
            print(f"❌ Failed to load optimized construct tab: {e}")
            import traceback

            traceback.print_exc()

            # Fallback to placeholder if loading fails
            if progress_callback:
                progress_callback(90, "Using fallback construct tab...")

    def _create_construct_tab_placeholder(
        self,
        container: "DIContainer",
        session_service=None,
    ) -> None:
        """Create a simple placeholder for the construct tab that loads the real tab on first access."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

        # Create placeholder widget
        placeholder = QWidget()
        layout = QVBoxLayout(placeholder)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add loading message
        loading_label = QLabel("🔧 Construct Tab")
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_label.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
                padding: 20px;
            }
        """
        )

        # Add load button
        load_button = QPushButton("Load Construct Tab")
        load_button.setStyleSheet(
            """
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """
        )

        # Connect load button to actually load the construct tab
        def load_real_construct_tab():
            load_button.setText("Loading...")
            load_button.setEnabled(False)

            # Load the real construct tab
            try:
                # Get the placeholder tab index and title
                placeholder_index = self.tab_widget.indexOf(placeholder)
                tab_title = (
                    self.tab_widget.tabText(placeholder_index)
                    if placeholder_index >= 0
                    else "🔧 Construct"
                )

                # Create the construct tab directly without using _load_construct_tab
                from presentation.tabs.construct.construct_tab import (
                    ConstructTab,
                )

                print("🔧 Creating construct tab widget...")
                construct_tab = ConstructTab(container, progress_callback=None)

                # Connect to session service
                self._connect_construct_tab_to_session(construct_tab, session_service)
                construct_tab.setStyleSheet("background: transparent;")

                # Replace the placeholder tab
                if placeholder_index >= 0:
                    self.tab_widget.removeTab(placeholder_index)
                    new_index = self.tab_widget.insertTab(
                        placeholder_index, construct_tab, tab_title
                    )
                else:
                    new_index = self.tab_widget.addTab(construct_tab, tab_title)

                # Register with tab management service
                self.tab_management_service.register_existing_tab(
                    "construct", construct_tab, new_index
                )

                # Set as current tab
                self.tab_widget.setCurrentIndex(new_index)

                print("✅ Construct tab loaded successfully!")

            except Exception as e:
                print(f"❌ Failed to load construct tab: {e}")
                import traceback

                traceback.print_exc()
                load_button.setText("Load Failed - Try Again")
                load_button.setEnabled(True)

        load_button.clicked.connect(load_real_construct_tab)

        layout.addWidget(loading_label)
        layout.addWidget(load_button)

        placeholder.setStyleSheet("background: transparent;")

        # Add placeholder to tab widget
        tab_index = self.tab_widget.addTab(placeholder, "🔧 Construct")

        # Register placeholder with tab management service
        self.tab_management_service.register_existing_tab(
            "construct", placeholder, tab_index
        )

        # Set construct tab as current tab
        self.tab_widget.setCurrentIndex(0)

    def _setup_lazy_construct_tab(
        self,
        container: "DIContainer",
        progress_callback: Optional[Callable] = None,
        session_service=None,
    ) -> None:
        """Setup construct tab with lazy loading for faster startup."""
        try:
            if progress_callback:
                progress_callback(76, "Creating construct tab placeholder...")

            # Create a lightweight placeholder for the construct tab
            placeholder = self._create_construct_placeholder()

            if progress_callback:
                progress_callback(78, "Registering lazy construct tab...")

            # Add placeholder to tab widget
            tab_index = self.tab_widget.addTab(placeholder, "🔧 Construct")

            # Register placeholder with tab management service
            self.tab_management_service.register_existing_tab(
                "construct", placeholder, tab_index
            )

            # Store references for lazy loading
            self._construct_container = container
            self._construct_session_service = session_service
            self._construct_placeholder = placeholder
            self._construct_tab_index = tab_index
            self._construct_loaded = False

            # Set construct tab as current tab
            self.tab_widget.setCurrentIndex(0)

            if progress_callback:
                progress_callback(80, "Construct tab placeholder ready!")

            # Schedule background loading after a short delay
            self._schedule_background_construct_loading()

        except Exception as e:
            import traceback

            print(f"⚠️ Error setting up lazy construct tab: {e}")
            traceback.print_exc()
            if progress_callback:
                progress_callback(80, "Construct tab setup failed, using fallback...")

            # Fallback to immediate loading
            self._load_construct_tab(container, progress_callback, session_service)

    def _create_construct_placeholder(self) -> QWidget:
        """Create a lightweight placeholder for the construct tab."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

        placeholder = QWidget()
        layout = QVBoxLayout(placeholder)

        # Create loading message
        loading_label = QLabel("🔧 Loading Construct Tab...")
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_label.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                padding: 20px;
            }
        """
        )

        layout.addWidget(loading_label)
        placeholder.setStyleSheet("background: transparent;")

        return placeholder

    def _schedule_background_construct_loading(self) -> None:
        """Schedule background loading of the construct tab."""

        def background_load():
            """Background thread function to load construct tab."""
            try:
                import time

                # Small delay to let UI finish loading
                time.sleep(0.2)

                # Load construct tab in background
                from PyQt6.QtCore import QTimer

                def load_on_main_thread():
                    """Load construct tab on main thread."""
                    if not self._construct_loaded:
                        self._load_construct_tab_lazy()

                # Schedule loading on main thread
                QTimer.singleShot(100, load_on_main_thread)

            except Exception as e:
                print(f"❌ Background construct tab loading failed: {e}")

        # Start background thread
        import threading

        thread = threading.Thread(target=background_load, daemon=True)
        thread.start()

    def _load_construct_tab_lazy(self) -> None:
        """Load the actual construct tab and replace the placeholder."""
        try:
            print("🔧 [LAZY_LOAD] Starting background construct tab loading...")

            # Load the actual construct tab
            from presentation.tabs.construct.construct_tab import (
                ConstructTab,
            )

            # Create construct tab without progress callback (background loading)
            construct_tab = ConstructTab(
                self._construct_container, progress_callback=None
            )

            # Connect to session service if available
            if self._construct_session_service and hasattr(
                construct_tab, "connect_to_session"
            ):
                construct_tab.connect_to_session(self._construct_session_service)

            # Set styling
            construct_tab.setStyleSheet("background: transparent;")

            # Replace placeholder with actual tab
            self.tab_widget.removeTab(self._construct_tab_index)
            self.tab_widget.insertTab(
                self._construct_tab_index, construct_tab, "🔧 Construct"
            )

            # Update tab management service
            self.tab_management_service.register_existing_tab(
                "construct", construct_tab, self._construct_tab_index
            )

            # Keep current tab selection
            self.tab_widget.setCurrentIndex(self._construct_tab_index)

            # Mark as loaded
            self._construct_loaded = True

            print("✅ [LAZY_LOAD] Construct tab loaded successfully in background!")

        except Exception as e:
            import traceback

            print(f"❌ [LAZY_LOAD] Failed to load construct tab: {e}")
            traceback.print_exc()

            # Update placeholder with error message
            try:
                from PyQt6.QtCore import Qt
                from PyQt6.QtWidgets import QLabel

                error_label = QLabel("❌ Failed to load Construct Tab")
                error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                error_label.setStyleSheet(
                    "color: red; font-size: 16px; background: transparent;"
                )

                # Replace placeholder content
                if hasattr(self, "_construct_placeholder"):
                    layout = self._construct_placeholder.layout()
                    if layout:
                        # Clear existing widgets
                        while layout.count():
                            child = layout.takeAt(0)
                            if child.widget():
                                child.widget().deleteLater()
                        layout.addWidget(error_label)
            except Exception as inner_e:
                print(f"❌ [LAZY_LOAD] Failed to update error message: {inner_e}")

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
            from presentation.tabs.construct.construct_tab import (
                ConstructTab,
            )

            if progress_callback:
                progress_callback(80, "Initializing construct tab services...")

            if progress_callback:
                progress_callback(82, "Setting up option picker components...")

            # Step 3: Create widget with progress callback (84-90%)
            if progress_callback:
                progress_callback(84, "🔧 Creating construct tab widget...")

            # Create construct tab with direct progress callback
            construct_tab = ConstructTab(container, progress_callback=progress_callback)

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

            if progress_callback:
                progress_callback(91, "Adding browse tab to interface...")

            # Add Browse tab
            self._add_browse_tab(container, progress_callback)

            # WINDOW MANAGEMENT FIX: Keep widgets hidden during splash screen
            # They will be shown when the main window is displayed
            self.tab_widget.hide()
            self.tab_widget.setVisible(False)
            construct_tab.hide()
            construct_tab.setVisible(False)

            # Set construct tab as current tab
            self.tab_widget.setCurrentIndex(0)

            if progress_callback:
                progress_callback(94, "Construct tab fully loaded and ready!")

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

    def _add_browse_tab(
        self,
        container: "DIContainer",
        progress_callback: Optional[Callable] = None,
    ) -> None:
        """Add Browse tab to the interface."""
        try:
            if progress_callback:
                progress_callback(91, "Loading browse tab...")

            # Import browse tab
            # Create browse tab with required paths
            # Using TKA's standard directories
            from pathlib import Path

            from presentation.tabs.browse.browse_tab import BrowseTab

            # Get TKA root directory
            tka_root = Path(
                __file__
            ).parent.parent.parent.parent.parent  # Navigate to TKA root
            sequences_dir = tka_root / "data" / "sequences"
            settings_file = tka_root / "settings.json"

            # Ensure directories exist
            sequences_dir.mkdir(parents=True, exist_ok=True)

            # Create browse tab
            browse_tab = BrowseTab(
                sequences_dir=sequences_dir, settings_file=settings_file
            )

            browse_tab.setStyleSheet("background: transparent;")

            if progress_callback:
                progress_callback(92, "Adding browse tab to interface...")

            # Add to tab widget
            browse_tab_index = self.tab_widget.addTab(browse_tab, "📚 Browse")

            # Register with tab management service
            self.tab_management_service.register_existing_tab(
                "browse", browse_tab, browse_tab_index
            )

            # Keep hidden during splash screen
            browse_tab.hide()
            browse_tab.setVisible(False)

            if progress_callback:
                progress_callback(93, "Browse tab loaded successfully!")

        except Exception as e:
            import traceback

            print(f"⚠️ Error loading browse tab: {e}")
            print(f"🔍 Full traceback:")
            traceback.print_exc()
            if progress_callback:
                progress_callback(
                    92, "Browse tab load failed, continuing without it..."
                )

    def _connect_construct_tab_to_session(
        self,
        construct_tab: ConstructTab,
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
