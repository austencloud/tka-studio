"""
Component Loader - FOCUSED SERVICE

Handles all UI component loading that was previously scattered across
6 different methods in UISetupManager (600+ lines of duplicate code).

ELIMINATES:
- _create_instant_construct_tab_with_background_upgrade()
- _load_construct_tab_aggressively_optimized()
- _create_minimal_construct_tab()
- _load_construct_tab_optimized()
- _create_construct_tab_placeholder()
- _setup_lazy_construct_tab()

PROVIDES:
- Single loading interface
- Consistent error handling
- Clean separation of concerns
"""

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QTabWidget, QVBoxLayout, QWidget

from desktop.modern.core.interfaces.session_services import ISessionStateTracker
from desktop.modern.presentation.views.browse.browse_tab import BrowseTab
from desktop.modern.presentation.views.construct.construct_tab import ConstructTab

from .tab_management import ITabManagementService


class ComponentLoader:
    """
    Focused service for loading UI components.

    Replaces 600+ lines of duplicate loading code with clean,
    single-responsibility methods.
    """

    def load_construct_tab(
        self,
        tab_widget: QTabWidget,
        tab_management_service: ITabManagementService,
        container,
        session_service: ISessionStateTracker | None = None,
    ) -> None:
        """
        Load construct tab - SINGLE method replaces 6 complex methods.
        """
        try:
            # Create construct tab
            construct_tab = ConstructTab(container)

            # Connect to session service if provided
            if session_service and hasattr(construct_tab, "sequence_modified"):
                construct_tab.sequence_modified.connect(
                    lambda seq_data: self._handle_sequence_modified(
                        seq_data, session_service
                    )
                )

            # Style and add to UI
            construct_tab.setStyleSheet("background: transparent;")
            tab_index = tab_widget.addTab(construct_tab, "🔧 Construct")

            # Register with tab management
            tab_management_service.register_existing_tab(
                "construct", construct_tab, tab_index
            )

            # Hide during startup
            construct_tab.hide()
            construct_tab.setVisible(False)

            print("✅ Construct tab loaded successfully")

        except Exception as e:
            print(f"❌ Failed to load construct tab: {e}")
            # Create fallback
            self._create_construct_fallback(tab_widget, tab_management_service)

    def load_browse_tab(
        self, tab_widget: QTabWidget, tab_management_service: ITabManagementService
    ) -> None:
        """Load browse tab with clean error handling."""
        try:
            # Get TKA root directory
            tka_root = Path(__file__).parent.parent.parent.parent.parent
            sequences_dir = tka_root / "data" / "sequences"
            settings_file = tka_root / "settings.json"

            # Ensure directories exist
            sequences_dir.mkdir(parents=True, exist_ok=True)

            # Create browse tab
            browse_tab = BrowseTab(
                sequences_dir=sequences_dir, settings_file=settings_file
            )

            browse_tab.setStyleSheet("background: transparent;")
            browse_tab_index = tab_widget.addTab(browse_tab, "📚 Browse")

            # Register with tab management
            tab_management_service.register_existing_tab(
                "browse", browse_tab, browse_tab_index
            )

            # Hide during startup
            browse_tab.hide()
            browse_tab.setVisible(False)

            print("✅ Browse tab loaded successfully")

        except Exception as e:
            print(f"❌ Failed to load browse tab: {e}")
            # Continue without browse tab - not critical

    def _handle_sequence_modified(
        self, sequence_data, session_service: ISessionStateTracker
    ) -> None:
        """Handle sequence modification from construct tab."""
        try:
            sequence_id = (
                sequence_data.id if hasattr(sequence_data, "id") else str(sequence_data)
            )
            session_service.update_current_sequence(sequence_data, sequence_id)
        except Exception as e:
            print(f"⚠️ Failed to update session with sequence: {e}")

    def _create_construct_fallback(
        self, tab_widget: QTabWidget, tab_management_service: ITabManagementService
    ) -> None:
        """Create fallback placeholder if construct tab fails to load."""
        fallback = QWidget()
        layout = QVBoxLayout(fallback)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        error_label = QLabel("🚧 Construct tab failed to load")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet(
            "color: #ff6b6b; font-size: 16px; background: transparent; padding: 20px;"
        )

        layout.addWidget(error_label)
        fallback.setStyleSheet("background: transparent;")

        tab_index = tab_widget.addTab(fallback, "🔧 Construct")
        tab_management_service.register_existing_tab("construct", fallback, tab_index)
