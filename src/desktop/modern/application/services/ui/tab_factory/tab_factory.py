"""
Tab Factory Service

Handles all tab creation in a consistent, upfront manner.
Replaces complex on-demand tab creation in TabManagementService.
"""

from __future__ import annotations

from collections.abc import Callable
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget

from desktop.modern.core.error_handling import StandardErrorHandler

from ..error_recovery.ui_error_recovery_service import UIErrorRecoveryService


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class TabDefinition:
    """Definition for a tab to be created."""

    def __init__(
        self,
        tab_id: str,
        display_name: str,
        creator_func: Callable,
        is_required: bool = True,
    ):
        self.tab_id = tab_id
        self.display_name = display_name
        self.creator_func = creator_func
        self.is_required = is_required


class TabFactory:
    """
    Factory for creating all application tabs upfront with consistent error handling.

    Eliminates complex on-demand creation and provides fallback tabs for failures.
    """

    def __init__(self):
        self.error_recovery = UIErrorRecoveryService()
        self.created_tabs: dict[str, QWidget] = {}

        # Define all available tabs
        self.tab_definitions = [
            TabDefinition(
                "construct", "🔧 Construct", self._create_construct_tab, True
            ),
            TabDefinition("generate", "🤖 Generate", self._create_generate_tab, True),
            TabDefinition("browse", "🔍 Browse", self._create_browse_tab, True),
            TabDefinition("write", "✍️ Write", self._create_write_tab, True),
            TabDefinition("learn", "🧠 Learn", self._create_learn_tab, False),
            TabDefinition(
                "sequence_card",
                "📋 Sequence Card",
                self._create_sequence_card_tab,
                False,
            ),
        ]

    def create_all_tabs(self, container: DIContainer) -> dict[str, dict[str, any]]:
        """
        Create all tabs upfront with consistent error handling.

        Args:
            container: DI container for service resolution

        Returns:
            Dict mapping tab_id to {"widget": QWidget, "display_name": str, "success": bool}
        """
        results = {}

        for tab_def in self.tab_definitions:
            try:
                # Create the tab
                tab_widget = tab_def.creator_func(container)

                if tab_widget:
                    results[tab_def.tab_id] = {
                        "widget": tab_widget,
                        "display_name": tab_def.display_name,
                        "success": True,
                    }
                    self.created_tabs[tab_def.tab_id] = tab_widget

                else:
                    raise Exception(f"Tab creator returned None for {tab_def.tab_id}")

            except Exception as e:
                # Handle tab creation failure
                error_context = f"{tab_def.tab_id} tab creation failed"
                StandardErrorHandler.handle_ui_error(
                    error_context,
                    e,
                    logger,
                    fallback_action=lambda: self._create_fallback_tab(tab_def),
                )

                # Create fallback tab
                fallback_tab = self._create_fallback_tab(tab_def)
                results[tab_def.tab_id] = {
                    "widget": fallback_tab,
                    "display_name": f"{tab_def.display_name} (Recovery)",
                    "success": False,
                }
                self.created_tabs[tab_def.tab_id] = fallback_tab

                if tab_def.is_required:
                    logger.exception(
                        f"❌ Required tab {tab_def.tab_id} failed, using fallback"
                    )
                else:
                    logger.warning(
                        f"⚠️ Optional tab {tab_def.tab_id} failed, using fallback"
                    )

        logger.info(f"📋 Tab creation complete: {len(results)} tabs created")
        return results

    def get_created_tab(self, tab_id: str) -> QWidget | None:
        """Get a previously created tab by ID."""
        return self.created_tabs.get(tab_id)

    def _create_construct_tab(self, container: DIContainer) -> QWidget:
        """Create the construct tab."""
        from desktop.modern.presentation.views.construct.construct_tab import (
            ConstructTab,
        )

        return ConstructTab(container=container)

    def _create_generate_tab(self, container: DIContainer) -> QWidget:
        """Create the generate tab."""
        from desktop.modern.presentation.views.generate.generate_tab import GenerateTab

        return GenerateTab(container=container)

    def _create_browse_tab(self, container: DIContainer) -> QWidget:
        """Create the browse tab."""
        logger.info("🔧 [TAB_FACTORY] Creating MODERN BrowseTab")
        from desktop.modern.presentation.views.browse.browse_tab import BrowseTab

        # Get TKA root directory
        tka_root = Path(__file__).parent.parent.parent.parent.parent.parent
        sequences_dir = tka_root / "data" / "sequences"
        settings_file = tka_root / "settings.json"

        # Ensure directories exist
        sequences_dir.mkdir(parents=True, exist_ok=True)

        browse_tab = BrowseTab(
            sequences_dir=sequences_dir,
            settings_file=settings_file,
            container=container,
        )
        logger.info(f"✅ [TAB_FACTORY] MODERN BrowseTab created: {id(browse_tab)}")
        return browse_tab

    def _create_write_tab(self, container: DIContainer) -> QWidget:
        """Create the write tab."""
        from desktop.modern.presentation.views.write import WriteTab

        return WriteTab(container=container)

    def _create_learn_tab(self, container: DIContainer) -> QWidget:
        """Create the learn tab."""
        try:
            from desktop.modern.presentation.views.learn import LearnTab

            return container.resolve(LearnTab)
        except Exception:
            # If learn tab can't be resolved, create placeholder
            return self._create_placeholder_tab("learn")

    def _create_sequence_card_tab(self, container: DIContainer) -> QWidget:
        """Create the sequence card tab."""
        try:
            print("🔧 [TAB_FACTORY] Attempting to create sequence card tab...")
            from desktop.modern.presentation.views.sequence_card import SequenceCardTab

            print("🔧 [TAB_FACTORY] SequenceCardTab imported successfully")
            result = container.resolve(SequenceCardTab)
            print("🔧 [TAB_FACTORY] SequenceCardTab resolved successfully")
            return result
        except Exception as e:
            print(f"❌ [TAB_FACTORY] Failed to create sequence card tab: {e}")
            print(f"❌ [TAB_FACTORY] Exception type: {type(e)}")
            import traceback

            print(f"❌ [TAB_FACTORY] Full traceback:\n{traceback.format_exc()}")
            # If sequence card tab can't be resolved, create placeholder
            return self._create_placeholder_tab("sequence_card")

    def _create_placeholder_tab(self, tab_id: str) -> QWidget:
        """Create a placeholder tab for future implementation."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont
        from PyQt6.QtWidgets import QLabel, QVBoxLayout

        placeholder = QWidget()
        layout = QVBoxLayout(placeholder)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create coming soon message
        display_name = tab_id.replace("_", " ").title()
        label = QLabel(f"🚧 {display_name} Tab\n\nComing Soon!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Segoe UI", 18, QFont.Weight.Medium))
        label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                background: rgba(40, 40, 40, 0.3);
                border: 2px dashed rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 40px;
                margin: 20px;
            }
        """
        )

        layout.addWidget(label)
        return placeholder

    def _create_fallback_tab(self, tab_def: TabDefinition) -> QWidget:
        """Create fallback tab for failed tab creation."""
        if tab_def.tab_id == "construct":
            return self.error_recovery.create_fallback_construct_tab(
                f"Failed to create full {tab_def.tab_id} tab"
            )
        if tab_def.tab_id == "browse":
            return self.error_recovery.create_fallback_browse_tab(
                f"Failed to create full {tab_def.tab_id} tab"
            )
        if tab_def.tab_id == "write":
            # For write, create a basic fallback with error message
            from PyQt6.QtCore import Qt
            from PyQt6.QtGui import QFont
            from PyQt6.QtWidgets import QLabel, QVBoxLayout

            fallback = QWidget()
            layout = QVBoxLayout(fallback)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            label = QLabel("⚠️ Write Tab Error\n\nFailed to load write tab services")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFont(QFont("Segoe UI", 16, QFont.Weight.Medium))
            label.setStyleSheet(
                """
                QLabel {
                    color: rgba(255, 255, 255, 0.8);
                    background: rgba(40, 40, 40, 0.3);
                    border: 2px dashed rgba(255, 100, 100, 0.5);
                    border-radius: 10px;
                    padding: 40px;
                    margin: 20px;
                }
            """
            )

            layout.addWidget(label)
            return fallback
        # For other tabs, create placeholder
        return self._create_placeholder_tab(tab_def.tab_id)

    def get_tab_definitions(self) -> list[TabDefinition]:
        """Get all tab definitions."""
        return self.tab_definitions.copy()

    def add_tab_definition(self, tab_def: TabDefinition) -> None:
        """Add a new tab definition (for extensions)."""
        self.tab_definitions.append(tab_def)

    def get_creation_status(self) -> dict[str, bool]:
        """Get creation status for all tabs."""
        return {
            tab_id: tab_id in self.created_tabs
            for tab_id in [td.tab_id for td in self.tab_definitions]
        }
