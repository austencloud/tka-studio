"""
Construct Tab Component Factory

Creates construct tab components with proper dependency injection.
Replaces the None initialization pattern with proper factory creation.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from PyQt6.QtWidgets import QLabel, QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.construct_tab_services import (
    IConstructTabComponentFactory,
)
from desktop.modern.core.interfaces.core_services import ILayoutService


if TYPE_CHECKING:
    from shared.application.services.workbench.beat_selection_service import (
        BeatSelectionService,
    )


class ConstructTabComponentFactory(IConstructTabComponentFactory):
    """
    Factory for creating construct tab components with proper dependency injection.

    Eliminates the None initialization anti-pattern by creating components
    with all their dependencies properly injected.
    """

    def __init__(
        self,
        container: DIContainer,
        progress_callback: Callable[[int, str], None] | None = None,
    ):
        self._container = container
        self._progress_callback = progress_callback

    def create_workbench(self) -> tuple[QWidget, Any]:
        """Create workbench component and return (widget, component)."""
        self._report_progress(10, "Creating workbench...")

        from desktop.modern.presentation.components.sequence_workbench.sequence_workbench import (
            SequenceWorkbench,
        )

        # Resolve dependencies
        layout_service = self._container.resolve(ILayoutService)
        beat_selection_service: BeatSelectionService = self._container.resolve(
            "BeatSelectionService"
        )

        # Create workbench
        workbench = SequenceWorkbench(
            container=self._container,
            layout_service=layout_service,
            beat_selection_service=beat_selection_service,
        )

        # Initialize workbench
        workbench.initialize()
        widget = workbench.get_widget()

        self._report_progress(20, "Workbench created")
        return widget, workbench

    def create_start_position_picker(self) -> tuple[QWidget, Any]:
        """Create start position picker and return (widget, component)."""
        self._report_progress(30, "Creating start position picker...")

        try:
            # Import here to avoid circular dependencies
            from desktop.modern.presentation.components.start_position_picker.start_position_picker import (
                StartPositionPicker,
            )

            # Create start position picker
            start_position_picker = StartPositionPicker(self._container)
            start_position_picker.initialize()
            widget = start_position_picker.get_widget()

            self._report_progress(40, "Start position picker created")
            return widget, start_position_picker

        except Exception as e:
            print(f"Warning: Could not create start position picker: {e}")

            # Create placeholder widget
            placeholder = self.create_placeholder_widget(
                "Start Position Picker not available"
            )
            self._report_progress(40, "Start position picker placeholder created")
            return placeholder, None

    def create_option_picker(self) -> tuple[QWidget, Any]:
        """Create option picker and return (widget, component)."""
        self._report_progress(50, "Creating option picker...")

        try:
            # Import here to avoid circular dependencies
            from desktop.modern.presentation.components.option_picker.option_picker import (
                OptionPicker,
            )

            # Create option picker
            option_picker = OptionPicker(self._container)
            option_picker.initialize()
            widget = option_picker.get_widget()

            self._report_progress(60, "Option picker created")
            return widget, option_picker

        except Exception as e:
            print(f"Warning: Could not create option picker: {e}")

            # Create placeholder widget
            placeholder = self.create_placeholder_widget("Option Picker not available")
            self._report_progress(60, "Option picker placeholder created")
            return placeholder, None

    def create_graph_editor(self) -> tuple[QWidget, Any]:
        """Create graph editor and return (widget, component)."""
        self._report_progress(70, "Creating graph editor...")

        try:
            # Import here to avoid circular dependencies
            from desktop.modern.presentation.components.graph_editor.graph_editor import (
                GraphEditor,
            )

            # Resolve dependencies
            graph_service = self._container.resolve("GraphEditorDataFlowService")

            # Create graph editor
            graph_editor = GraphEditor(
                graph_service=graph_service,
                workbench_width=800,  # Default values
                workbench_height=600,
            )

            widget = graph_editor  # GraphEditor is already a QWidget

            self._report_progress(80, "Graph editor created")
            return widget, graph_editor

        except Exception as e:
            print(f"Warning: Could not create graph editor: {e}")

            # Create placeholder widget
            placeholder = self.create_placeholder_widget("Graph Editor not available")
            self._report_progress(80, "Graph editor placeholder created")
            return placeholder, None

    def create_generate_panel(self) -> tuple[QWidget, Any]:
        """Create generate panel and return (widget, component)."""
        self._report_progress(85, "Creating generate panel...")

        try:
            # Use the real GeneratePanel with controller instead of non-existent GenerateControls
            from desktop.modern.presentation.components.generate_tab.generate_panel import (
                GeneratePanel,
            )

            # Create generate panel with container for dependency injection
            generate_panel = GeneratePanel(container=self._container)
            generate_panel.initialize()
            widget = generate_panel

            self._report_progress(90, "Generate panel created")
            return widget, generate_panel

        except Exception as e:
            print(f"Warning: Could not create generate panel: {e}")

            # Create placeholder widget
            placeholder = self.create_placeholder_widget("Generate Panel not available")
            self._report_progress(90, "Generate panel placeholder created")
            return placeholder, None

    def create_export_panel(self) -> tuple[QWidget, Any]:
        """Create export panel and return (widget, component)."""
        self._report_progress(95, "Creating export panel...")

        try:
            # Import here to avoid circular dependencies
            from desktop.modern.presentation.components.export_panel.export_panel import (
                ExportPanel,
            )

            # Create export panel
            export_panel = ExportPanel(self._container)
            export_panel.initialize()
            widget = export_panel.get_widget()

            self._report_progress(100, "Export panel created")
            return widget, export_panel

        except Exception as e:
            print(f"Warning: Could not create export panel: {e}")

            # Create placeholder widget
            placeholder = self.create_placeholder_widget("Export Panel not available")
            self._report_progress(100, "Export panel placeholder created")
            return placeholder, None

    def create_placeholder_widget(self, text: str) -> QWidget:
        """Create a placeholder widget for deferred loading."""
        placeholder = QLabel(text)
        placeholder.setStyleSheet(
            "color: #888; font-size: 14px; padding: 20px; text-align: center;"
        )
        return placeholder

    def _report_progress(self, progress: int, message: str):
        """Report progress if callback is available."""
        if self._progress_callback:
            self._progress_callback(progress, message)
