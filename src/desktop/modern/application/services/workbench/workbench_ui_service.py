"""
Workbench UI Service

Handles all UI-related functionality for the workbench component.
Extracted from the large workbench component to improve maintainability.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from PyQt6.QtWidgets import QVBoxLayout, QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.construct_tab_services import IWorkbenchUIService
from desktop.modern.core.interfaces.core_services import ILayoutService
from desktop.modern.domain.models import SequenceData
from desktop.modern.presentation.components.sequence_workbench.indicator_section import (
    WorkbenchIndicatorSection,
)


if TYPE_CHECKING:
    from shared.application.services.workbench.beat_selection_service import (
        BeatSelectionService,
    )

    from desktop.modern.presentation.components.workbench.beat_frame_section import (
        WorkbenchBeatFrameSection,
    )


class WorkbenchUIService(IWorkbenchUIService):
    """
    Service for managing workbench UI components and layout.

    Responsibilities:
    - UI setup and layout management
    - Component creation and initialization
    - UI state updates
    - Visual feedback display
    """

    def __init__(
        self,
        container: DIContainer,
        layout_service: ILayoutService,
        beat_selection_service: BeatSelectionService,
    ):
        self._container = container
        self._layout_service = layout_service
        self._beat_selection_service = beat_selection_service

        # UI components
        self._main_widget: QWidget | None = None
        self._indicator_section: WorkbenchIndicatorSection | None = None
        self._beat_frame_section: WorkbenchBeatFrameSection | None = None

    def setup_workbench_ui(self, parent: QWidget) -> QWidget:
        """Set up workbench UI and return the main widget."""
        # Create main widget
        self._main_widget = QWidget(parent)
        main_layout = QVBoxLayout(self._main_widget)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # Create indicator section
        self._indicator_section = WorkbenchIndicatorSection(
            dictionary_service=self._safe_resolve("SequenceDictionaryService"),
            parent=self._main_widget,
        )
        main_layout.addWidget(self._indicator_section, 0)

        # Create beat frame section
        from desktop.modern.presentation.components.workbench.beat_frame_section import (
            WorkbenchBeatFrameSection,
        )

        self._beat_frame_section = WorkbenchBeatFrameSection(
            layout_service=self._layout_service,
            beat_selection_service=self._beat_selection_service,
            parent=self._main_widget,
        )
        main_layout.addWidget(self._beat_frame_section, 1)

        # Ensure widget is visible
        self._main_widget.show()
        self._main_widget.setVisible(True)

        return self._main_widget

    def update_sequence_display(self, sequence: SequenceData | None) -> None:
        """Update sequence display."""
        # Update indicator section
        if self._indicator_section:
            self._indicator_section.update_sequence(sequence)

        # Update beat frame section
        if self._beat_frame_section:
            self._beat_frame_section.set_sequence(sequence)

    def update_beat_selection(self, beat_index: int | None) -> None:
        """Update beat selection display."""
        if self._beat_frame_section:
            self._beat_frame_section.set_button_enabled(
                "delete_beat", beat_index is not None
            )

    def show_operation_feedback(
        self, operation: str, message: str, duration: int = 3000
    ) -> None:
        """Show operation feedback to user."""
        if self._beat_frame_section:
            self._beat_frame_section.show_button_message(operation, message, duration)

    def get_beat_frame_section(self) -> Optional[WorkbenchBeatFrameSection]:
        """Get the beat frame section component."""
        return self._beat_frame_section

    def get_indicator_section(self) -> WorkbenchIndicatorSection | None:
        """Get the indicator section component."""
        return self._indicator_section

    def _safe_resolve(self, service_key: str):
        """Safely resolve a service, returning None if not available."""
        try:
            return self._container.resolve(service_key)
        except Exception:
            return None
