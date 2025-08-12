"""
PanelFactory

Creates individual UI panels for the construct tab.
Handles the creation of workbench, start position picker, option picker,
graph editor, and generate controls panels.
"""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.presentation.components.option_picker.components.option_picker import (
    OptionPicker,
)
from desktop.modern.presentation.components.start_position_picker.start_position_picker import (
    PickerMode,
    StartPositionPicker,
)
from desktop.modern.presentation.factories.workbench_factory import (
    create_modern_workbench,
)


class PanelFactory:
    """
    Factory class for creating individual UI panels.

    Responsibilities:
    - Creating workbench panel
    - Creating start position picker panel
    - Creating option picker panel
    - Creating graph editor panel
    - Creating generate controls panel
    - Creating export panel (NEW)
    - Handling fallback widgets on errors
    """

    def __init__(
        self,
        container: DIContainer,
        progress_callback: Callable[[int, str], None] | None = None,
    ):
        self.container = container
        self.progress_callback = progress_callback
        self.progress_reporter = progress_callback  # Alias for compatibility

    def create_workbench_panel(self) -> QWidget:
        """Create the workbench panel (left side)."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(4)

        workbench = create_modern_workbench(self.container, panel)
        layout.addWidget(workbench.get_widget())

        return panel, workbench

    def create_start_position_panel(
        self,
    ) -> tuple[QWidget, StartPositionPicker | None]:
        """Create the start position picker panel."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        try:
            from desktop.modern.core.interfaces.start_position_services import (
                IStartPositionDataService,
                IStartPositionOrchestrator,
                IStartPositionUIService,
            )

            data_service = self.container.resolve(IStartPositionDataService)
            ui_service = self.container.resolve(IStartPositionUIService)
            orchestrator = self.container.resolve(IStartPositionOrchestrator)

            # Try to get animation orchestrator for fade transitions
            try:
                from desktop.modern.core.interfaces.animation_core_interfaces import (
                    IAnimationOrchestrator,
                )

                animation_orchestrator = self.container.resolve(IAnimationOrchestrator)
                # Store it in the orchestrator for the picker to access
                orchestrator._container = self.container
            except Exception:
                # Animation system not available - continue without it
                pass

            start_position_picker = StartPositionPicker(
                data_service=data_service,
                ui_service=ui_service,
                orchestrator=orchestrator,
                initial_mode=PickerMode.AUTO,
            )

            layout.addWidget(start_position_picker)
            return widget, start_position_picker

        except Exception as e:
            fallback_label = QLabel(f"Start position picker unavailable: {e}")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_label.setStyleSheet(
                "color: orange; font-size: 14px; padding: 20px;"
            )
            layout.addWidget(fallback_label)
            return widget, None

    def create_export_panel(self) -> tuple[QWidget, object | None]:
        """Create the export panel (NEW)."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        try:
            # Import our new ExportPanel
            from desktop.modern.presentation.components.export_panel.export_panel import (
                ExportPanel,
            )

            # Report progress if callback available
            if self.progress_callback:
                self.progress_callback(90, "Creating export panel...")

            export_panel = ExportPanel(
                container=self.container,
                parent=widget,
            )
            layout.addWidget(export_panel)

            if self.progress_callback:
                self.progress_callback(95, "Export panel created")

            return widget, export_panel

        except Exception as e:
            fallback_label = QLabel(f"Export panel unavailable: {e}")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_label.setStyleSheet("color: red; font-size: 14px; padding: 20px;")
            layout.addWidget(fallback_label)

            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create export panel: {e}", exc_info=True)

            return widget, None

    def create_option_picker_panel(self) -> tuple[QWidget, OptionPicker | None]:
        """Create the option picker panel."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        try:
            option_picker = OptionPicker(
                self.container,
                progress_callback=self.option_picker_progress,
                parent=widget,
            )
            option_picker.initialize()
            layout.addWidget(option_picker.widget)
            option_picker.make_widgets_visible()

            return widget, option_picker

        except Exception as e:
            print(f"❌ Failed to create option picker: {e}")
            fallback_label = QLabel("Option picker unavailable")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(fallback_label)
            return widget, None

    def option_picker_progress(self, message: str, progress: float) -> None:
        """Progress callback for option picker creation."""
        if self.progress_callback:
            # Simple progress callback - just call with progress and message
            self.progress_callback(int(progress), message)

    def create_graph_editor_panel(self) -> tuple[QWidget, object | None]:
        """Create the graph editor panel."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        try:
            from desktop.modern.presentation.components.graph_editor.graph_editor import (
                GraphEditor,
            )

            graph_editor = GraphEditor(
                graph_service=None,
                parent=None,
                workbench_width=800,
                workbench_height=300,
            )
            layout.addWidget(graph_editor)
            return widget, graph_editor

        except Exception as e:
            fallback_label = QLabel(f"Graph editor unavailable: {e}")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_label.setStyleSheet("color: red; font-size: 14px; padding: 20px;")
            layout.addWidget(fallback_label)

            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create graph editor: {e}", exc_info=True)

            return widget, None

    def create_generate_controls_panel(self) -> tuple[QWidget, object | None]:
        """Create the generate controls panel."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        try:
            from desktop.modern.presentation.components.generate_tab.generate_panel import (
                GeneratePanel,
            )

            generate_panel = GeneratePanel(parent=widget)
            layout.addWidget(generate_panel)
            return widget, generate_panel

        except Exception as e:
            fallback_label = QLabel(f"Generate controls unavailable: {e}")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_label.setStyleSheet(
                "color: orange; font-size: 14px; padding: 20px;"
            )
            layout.addWidget(fallback_label)

            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create generate controls: {e}", exc_info=True)

            return widget, None
