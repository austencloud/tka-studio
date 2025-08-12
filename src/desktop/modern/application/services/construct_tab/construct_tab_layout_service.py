"""
Construct Tab Layout Service

Manages layout and UI transitions for the construct tab.
Extracted from the large LayoutManager to provide focused responsibility.
"""

from __future__ import annotations

from typing import Any, Callable

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QHBoxLayout, QStackedWidget, QVBoxLayout, QWidget

from desktop.modern.application.services.construct_tab.construct_tab_component_factory import (
    ConstructTabComponentFactory,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.construct_tab_services import (
    IConstructTabLayoutService,
)
from desktop.modern.presentation.components.right_panel_tabs.right_panel_tab_widget import (
    RightPanelTabWidget,
)


class ConstructTabLayoutService(IConstructTabLayoutService):
    """
    Service for managing construct tab layout and transitions.

    Responsibilities:
    - Layout setup and management
    - Component placement
    - UI transitions
    - Tab management
    """

    def __init__(
        self,
        container: DIContainer,
        component_factory: ConstructTabComponentFactory,
        progress_callback: Callable[[int, str], None] | None = None,
    ):
        self._container = container
        self._component_factory = component_factory
        self._progress_callback = progress_callback

        # Layout components
        self._main_widget: QWidget | None = None
        self._workbench_widget: QWidget | None = None
        self._picker_widget: QWidget | None = None
        self._picker_stack: QStackedWidget | None = None
        self._tab_widget: RightPanelTabWidget | None = None

        # Component references
        self._components: dict[str, Any] = {}
        self._is_transitioning = False

    def setup_layout(self, parent_widget: QWidget) -> None:
        """Set up the main UI layout."""
        self._report_progress(10, "Setting up layout...")

        # Create main horizontal layout
        main_layout = QHBoxLayout(parent_widget)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(4, 4, 4, 4)

        # Create workbench panel
        self._report_progress(20, "Creating workbench...")
        self._workbench_widget, workbench_component = (
            self._component_factory.create_workbench()
        )
        main_layout.addWidget(self._workbench_widget, 1)
        self._components["workbench"] = workbench_component

        # Create picker panel
        self._report_progress(50, "Creating picker panel...")
        self._picker_widget = self._create_picker_panel()
        main_layout.addWidget(self._picker_widget, 1)

        # Connect tab signals
        self._connect_tab_signals()

        # Set initial state
        self._update_tab_active_state(0)
        self._report_progress(100, "Layout complete")

    def _create_picker_panel(self) -> QWidget:
        """Create the picker panel with stacked widgets."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create tab widget
        self._tab_widget = RightPanelTabWidget()
        layout.addWidget(self._tab_widget)

        # Create stacked widget
        self._picker_stack = QStackedWidget()
        layout.addWidget(self._picker_stack)

        # Create all panels
        self._create_all_panels()

        # Set initial panel
        self._picker_stack.setCurrentIndex(0)

        return panel

    def _create_all_panels(self):
        """Create all panels in the correct order."""
        # Start position picker (index 0)
        start_pos_widget, start_pos_component = (
            self._component_factory.create_start_position_picker()
        )
        self._picker_stack.addWidget(start_pos_widget)
        self._components["start_position_picker"] = start_pos_component

        # Option picker (index 1) - create placeholder first, then real component
        option_placeholder = self._component_factory.create_placeholder_widget(
            "Loading option picker..."
        )
        self._picker_stack.addWidget(option_placeholder)
        self._components["option_picker"] = None  # Will be set later

        # Schedule deferred option picker creation
        QTimer.singleShot(500, self._create_real_option_picker)

        # Graph editor (index 2)
        graph_widget, graph_component = self._component_factory.create_graph_editor()
        self._picker_stack.addWidget(graph_widget)
        self._components["graph_editor"] = graph_component

        # Generate panel (index 3)
        generate_widget, generate_component = (
            self._component_factory.create_generate_panel()
        )
        self._picker_stack.addWidget(generate_widget)
        self._components["generate_panel"] = generate_component

        # Export panel (index 4)
        export_widget, export_component = self._component_factory.create_export_panel()
        self._picker_stack.addWidget(export_widget)
        self._components["export_panel"] = export_component

    def _create_real_option_picker(self):
        """Create the real option picker component (deferred)."""
        try:
            option_widget, option_component = (
                self._component_factory.create_option_picker()
            )

            # Replace placeholder with real component
            self._picker_stack.removeWidget(self._picker_stack.widget(1))
            self._picker_stack.insertWidget(1, option_widget)
            self._components["option_picker"] = option_component

        except Exception as e:
            print(f"❌ Failed to create option picker: {e}")

    def _connect_tab_signals(self):
        """Connect tab widget signals to transition methods."""
        if self._tab_widget:
            self._tab_widget.picker_tab_clicked.connect(
                self.transition_to_start_position_picker
            )
            self._tab_widget.option_picker_tab_clicked.connect(
                self.transition_to_option_picker
            )
            self._tab_widget.graph_editor_tab_clicked.connect(
                self.transition_to_graph_editor
            )
            self._tab_widget.generate_tab_clicked.connect(
                self.transition_to_generate_controls
            )
            self._tab_widget.export_tab_clicked.connect(self.transition_to_export_panel)

    # Transition methods
    def transition_to_start_position_picker(self) -> None:
        """Transition to start position picker."""
        self._transition_to_panel(0)

    def transition_to_option_picker(self) -> None:
        """Transition to option picker."""
        self._transition_to_panel(1)

    def transition_to_graph_editor(self) -> None:
        """Transition to graph editor."""
        self._transition_to_panel(2)

    def transition_to_generate_controls(self) -> None:
        """Transition to generate controls."""
        self._transition_to_panel(3)

    def transition_to_export_panel(self) -> None:
        """Transition to export panel."""
        self._transition_to_panel(4)

    def _transition_to_panel(self, index: int):
        """Transition to the specified panel index."""
        if self._is_transitioning or not self._picker_stack:
            return

        self._is_transitioning = True
        try:
            self._picker_stack.setCurrentIndex(index)
            self._update_tab_active_state(index)
        finally:
            self._is_transitioning = False

    def _update_tab_active_state(self, active_index: int):
        """Update tab active state."""
        if self._tab_widget:
            self._tab_widget.set_active_tab(active_index)

    # Getters
    def get_workbench_widget(self) -> QWidget:
        """Get the workbench widget."""
        if not self._workbench_widget:
            raise RuntimeError("Layout not initialized")
        return self._workbench_widget

    def get_picker_widget(self) -> QWidget:
        """Get the picker panel widget."""
        if not self._picker_widget:
            raise RuntimeError("Layout not initialized")
        return self._picker_widget

    def get_component(self, name: str) -> Any:
        """Get a component by name."""
        return self._components.get(name)

    def _report_progress(self, progress: int, message: str):
        """Report progress if callback is available."""
        if self._progress_callback:
            self._progress_callback(progress, message)
