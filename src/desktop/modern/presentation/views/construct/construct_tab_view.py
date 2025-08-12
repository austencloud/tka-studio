"""
ConstructTab View - PURE UI COMPONENT

Extracted from the 22KB ConstructTab god object.
Handles ONLY UI creation, layout, and styling.

RESPONSIBILITIES:
- UI widget creation and layout via ConstructTabLayoutManager
- Styling and visual appearance
- User interaction handling (clicks, etc.)
- Qt-specific UI behavior

DOES NOT HANDLE:
- Business logic (that's the controller)
- Service coordination (that's the controller)
- State management (that's the controller)
"""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtWidgets import QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.presentation.managers.construct.layout_manager import (
    ConstructTabLayoutManager,
)


class ConstructTabView(QWidget):
    """
    FOCUSED view for construct tab UI.

    Extracted from ConstructTab god object to separate UI concerns.
    Handles only UI creation and layout via ConstructTabLayoutManager.
    """

    def __init__(self, parent_widget: QWidget):
        super().__init__(parent_widget)
        self._parent_widget = parent_widget
        self._layout_manager: ConstructTabLayoutManager | None = None

    def setup_ui(
        self,
        container: DIContainer,
        progress_callback: Callable | None = None,
        option_picker_ready_callback: Callable | None = None,
    ) -> None:
        """
        Setup the UI using the ConstructTabLayoutManager.

        This integrates with the existing layout system.
        """
        try:
            # Create layout manager with callbacks
            self._layout_manager = ConstructTabLayoutManager(
                container=container,
                progress_callback=progress_callback,
                option_picker_ready_callback=option_picker_ready_callback,
            )

            # Let layout manager setup the UI on parent widget
            self._layout_manager.setup_ui(self._parent_widget)


        except Exception as e:
            print(f"❌ Failed to setup ConstructTabView UI: {e}")

    def force_picker_update(self) -> None:
        """Force picker update - delegate to layout manager."""
        if self._layout_manager and hasattr(
            self._layout_manager, "force_picker_update"
        ):
            self._layout_manager.force_picker_update()

    def update_layout(self) -> None:
        """Update the layout - called on resize events."""
        self.update()
        if self._layout_manager:
            # Trigger any layout-specific updates if needed
            pass
