"""
ConstructTabLayoutManager - Refactored

Manages the UI layout and panel creation for the construct tab.
Now uses specialized components for different responsibilities.
"""

from typing import TYPE_CHECKING, Callable, Optional

from core.dependency_injection.di_container import DIContainer
from core.interfaces.animation_core_interfaces import IAnimationOrchestrator
from presentation.components.right_panel_tabs.right_panel_tab_widget import (
    RightPanelTabWidget,
)
from PyQt6.QtWidgets import QHBoxLayout, QStackedWidget, QVBoxLayout, QWidget

from .components.component_connector import ComponentConnector
from .components.panel_factory import PanelFactory
from .components.transition_animator import TransitionAnimator
from .orchestrators.layout_orchestrator import LayoutOrchestrator
from .orchestrators.progress_reporter import ProgressReporter

if TYPE_CHECKING:
    pass


class ConstructTabLayoutManager:
    """
    Refactored layout manager with separated responsibilities.

    Responsibilities:
    - Coordinating between specialized components
    - Managing the main layout structure
    - Providing public interface for transitions
    - Handling component lifecycle
    """

    def __init__(
        self,
        container: DIContainer,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        option_picker_ready_callback: Optional[Callable[[object], None]] = None,
    ):
        self.container = container
        self.option_picker_ready_callback = option_picker_ready_callback

        # Initialize orchestrators (Qt-agnostic)
        self.layout_orchestrator = LayoutOrchestrator()
        self.progress_reporter = ProgressReporter(progress_callback)

        # Initialize components (Qt-specific)
        self.panel_factory = PanelFactory(container, self._component_progress_callback)
        self.transition_animator = TransitionAnimator()
        self.component_connector = ComponentConnector()

        # UI components
        self.workbench = None
        self.picker_stack = None
        self.tab_widget = None
        self.start_position_picker = None
        self.option_picker = None
        self.graph_editor = None
        self.generate_panel = None

        # Animation orchestrator
        try:
            self.animation_orchestrator = container.resolve(IAnimationOrchestrator)
        except Exception:
            self.animation_orchestrator = None

        self._is_transitioning = False

    def _component_progress_callback(self, progress: int, message: str):
        """Progress callback for component creation."""
        if self.progress_reporter.progress_callback:
            self.progress_reporter.progress_callback(progress, message)

    def setup_ui(self, parent_widget: QWidget) -> None:
        """Set up the main UI layout."""
        self.progress_reporter.start_phase("layout_setup", "Setting up layout...")

        # Create main horizontal layout
        main_layout = QHBoxLayout(parent_widget)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(4, 4, 4, 4)

        # Create workbench panel
        self.progress_reporter.start_phase(
            "workbench_creation", "Creating workbench..."
        )
        workbench_panel, self.workbench = self.panel_factory.create_workbench_panel()
        main_layout.addWidget(workbench_panel, 1)
        self.layout_orchestrator.register_component("workbench", self.workbench)
        self.progress_reporter.complete_phase("workbench_creation", "Workbench created")

        # Create picker panel
        picker_panel = self._create_picker_panel()
        main_layout.addWidget(picker_panel, 1)

        # Connect components
        self.progress_reporter.start_phase(
            "signal_connection", "Connecting components..."
        )
        self._connect_components()
        self.progress_reporter.complete_phase(
            "signal_connection", "Components connected"
        )

        # Finalize
        self.progress_reporter.start_phase("finalization", "Finalizing layout...")
        self.progress_reporter.complete_phase("finalization", "Layout complete")

    def _create_picker_panel(self) -> QWidget:
        """Create the picker panel with stacked widgets."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create tab widget
        self.tab_widget = RightPanelTabWidget()
        layout.addWidget(self.tab_widget)

        # Create stacked widget
        self.picker_stack = QStackedWidget()

        # Create all panels
        self._create_all_panels()

        self.picker_stack.setCurrentIndex(0)
        layout.addWidget(self.picker_stack)

        # Update tab state
        self._update_tab_active_state(0)

        return panel

    def _create_all_panels(self):
        """Create all panels in the correct order."""
        # Start position picker
        self.progress_reporter.start_phase(
            "start_position_creation", "Loading start positions..."
        )
        start_pos_widget, self.start_position_picker = (
            self.panel_factory.create_start_position_panel()
        )
        self.picker_stack.addWidget(start_pos_widget)
        self.layout_orchestrator.register_component(
            "start_position_picker", self.start_position_picker
        )
        self.progress_reporter.complete_phase(
            "start_position_creation", "Start positions loaded"
        )

        # PERFORMANCE OPTIMIZATION: Defer option picker creation for faster startup
        self.progress_reporter.start_phase(
            "option_picker_creation", "Preparing option picker..."
        )
        # Create placeholder widget for now
        from PyQt6.QtWidgets import QLabel

        option_widget = QLabel("Loading option picker...")
        option_widget.setStyleSheet(
            "color: #888; font-size: 14px; padding: 20px; text-align: center;"
        )
        self.option_picker = None  # Will be created later
        self.picker_stack.addWidget(option_widget)
        self._option_placeholder = option_widget  # Store reference for replacement
        self.layout_orchestrator.register_component("option_picker", self.option_picker)
        self.progress_reporter.complete_phase(
            "option_picker_creation", "Option picker prepared"
        )

        # Schedule deferred option picker creation
        from PyQt6.QtCore import QTimer

        QTimer.singleShot(500, self._create_real_option_picker)

        # Graph editor
        self.progress_reporter.start_phase(
            "graph_editor_creation", "Creating graph editor..."
        )
        graph_editor_widget, self.graph_editor = (
            self.panel_factory.create_graph_editor_panel()
        )
        self.picker_stack.addWidget(graph_editor_widget)
        self.layout_orchestrator.register_component("graph_editor", self.graph_editor)
        self.progress_reporter.complete_phase(
            "graph_editor_creation", "Graph editor created"
        )

        # Generate controls
        self.progress_reporter.start_phase(
            "generate_controls_creation", "Creating generate controls..."
        )
        generate_widget, self.generate_panel = (
            self.panel_factory.create_generate_controls_panel()
        )
        self.picker_stack.addWidget(generate_widget)
        self.layout_orchestrator.register_component(
            "generate_controls", self.generate_panel
        )
        self.progress_reporter.complete_phase(
            "generate_controls_creation", "Generate controls created"
        )

    def _connect_components(self):
        """Connect all components through the component connector."""
        # Note: WorkbenchStateManager is framework-agnostic and doesn't need direct workbench reference
        # The workbench widget communicates with the state manager through method calls
        if self.workbench:
            pass  # Workbench available for component connections

        # Connect components through component connector
        self.component_connector.set_workbench(self.workbench)
        self.component_connector.set_graph_editor(self.graph_editor)
        self.component_connector.set_generate_panel(self.generate_panel)
        self.component_connector.set_start_position_picker(self.start_position_picker)

    # Public transition methods
    def transition_to_option_picker(self):
        """Transition to option picker with smooth animation."""
        if self.picker_stack and not self.transition_animator.is_transitioning():
            self._update_tab_active_state(1)
            self.component_connector.prepare_for_transition("option_picker")
            self.transition_animator.fade_to_panel(
                self.picker_stack,
                1,
                "option picker",
                lambda: self.component_connector.finalize_transition("option_picker"),
            )

    def transition_to_start_position_picker(self):
        """Transition to start position picker with smooth animation."""
        if self.picker_stack and not self.transition_animator.is_transitioning():
            self._update_tab_active_state(0)
            self.component_connector.prepare_for_transition("start_position")
            self.transition_animator.fade_to_panel(
                self.picker_stack,
                0,
                "start position picker",
                lambda: self.component_connector.finalize_transition("start_position"),
            )

    def transition_to_graph_editor(self):
        """Transition to graph editor with smooth animation."""
        if self.picker_stack and not self.transition_animator.is_transitioning():
            self._update_tab_active_state(2)
            self.transition_animator.fade_to_panel(self.picker_stack, 2, "graph editor")

    def transition_to_generate_controls(self):
        """Transition to generate controls with smooth animation."""
        if self.picker_stack and not self.transition_animator.is_transitioning():
            self._update_tab_active_state(3)
            self.transition_animator.fade_to_panel(
                self.picker_stack, 3, "generate controls"
            )

    def _update_tab_active_state(self, panel_index: int):
        """Update the tab widget to reflect the current panel."""
        if self.tab_widget:
            tab_index = self.layout_orchestrator.get_tab_for_panel(panel_index)
            self.tab_widget.set_active_tab(tab_index)

    # Legacy compatibility methods (maintain same interface)
    def _on_generate_requested(self, generation_config):
        """Handle generation request from generate panel."""
        self.component_connector._on_generate_requested(generation_config)

    def _on_graph_beat_modified(self, beat_index: int, beat_data):
        """Handle beat modification from graph editor."""
        self.component_connector._on_graph_beat_modified(beat_index, beat_data)

    def _connect_beat_frame_to_graph_editor(self):
        """Connect beat frame to graph editor (legacy compatibility)."""
        self.component_connector._connect_beat_frame_signals()

    # Component access methods
    def get_workbench(self):
        """Get the workbench component."""
        return self.workbench

    def get_option_picker(self):
        """Get the option picker component."""
        return self.option_picker

    def get_start_position_picker(self):
        """Get the start position picker component."""
        return self.start_position_picker

    def get_graph_editor(self):
        """Get the graph editor component."""
        return self.graph_editor

    def get_generate_panel(self):
        """Get the generate panel component."""
        return self.generate_panel

    def get_component_connector(self):
        """Get the component connector for signal access."""
        return self.component_connector

    def _create_real_option_picker(self):
        """Create the real option picker after main window is shown."""
        try:

            # Create the real option picker
            option_widget, self.option_picker = (
                self.panel_factory.create_option_picker_panel()
            )

            # Replace placeholder with real option picker
            if hasattr(self, "_option_placeholder"):
                placeholder_index = self.picker_stack.indexOf(self._option_placeholder)
                if placeholder_index >= 0:
                    self.picker_stack.removeWidget(self._option_placeholder)
                    self._option_placeholder.deleteLater()
                    self.picker_stack.insertWidget(placeholder_index, option_widget)

                    # Update orchestrator registration
                    self.layout_orchestrator.register_component(
                        "option_picker", self.option_picker
                    )

                    # Notify callback that option picker is ready
                    if self.option_picker_ready_callback:

                        self.option_picker_ready_callback(self.option_picker)

        except Exception as e:
            print(f"❌ [LAYOUT_MANAGER] Error creating deferred option picker: {e}")
            import traceback

            traceback.print_exc()
