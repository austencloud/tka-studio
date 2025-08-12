"""
ConstructTabLayoutManager - Refactored

Manages the UI layout and panel creation for the construct tab.
Now uses specialized components for different responsibilities.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QHBoxLayout, QStackedWidget, QVBoxLayout, QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.animation_core_interfaces import (
    IAnimationOrchestrator,
)
from desktop.modern.presentation.components.construct.component_connector import (
    ComponentConnector,
)
from desktop.modern.presentation.components.construct.panel_factory import PanelFactory
from desktop.modern.presentation.components.construct.transition_animator import (
    TransitionAnimator,
)
from desktop.modern.presentation.components.right_panel_tabs.right_panel_tab_widget import (
    RightPanelTabWidget,
)
from desktop.modern.presentation.controllers.construct.orchestrators.layout_orchestrator import (
    LayoutOrchestrator,
)
from desktop.modern.presentation.controllers.construct.orchestrators.progress_reporter import (
    ProgressReporter,
)


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
        progress_callback: Callable[[int, str], None] | None = None,
        option_picker_ready_callback: Callable[[object], None] | None = None,
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

        # UI components - Updated to include export panel
        self.workbench = None
        self.picker_stack = None
        self.tab_widget = None
        self.start_position_picker = None
        self.option_picker = None
        self.graph_editor = None
        self.generate_panel = None
        self.export_panel = None  # NEW: Export panel

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

        # Create picker panel with 4 tabs
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
        """Create the picker panel with stacked widgets for 4 panels."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create tab widget with 4 tabs
        self.tab_widget = RightPanelTabWidget()
        layout.addWidget(self.tab_widget)

        # Create stacked widget
        self.picker_stack = QStackedWidget()

        # Create all panels including Export
        self._create_all_panels()

        self.picker_stack.setCurrentIndex(0)
        layout.addWidget(self.picker_stack)

        # Connect tab widget signals
        self._connect_tab_signals()

        # Update tab state
        self._update_tab_active_state(0)

        return panel

    def _connect_tab_signals(self):
        """Connect tab widget signals to transition methods."""
        if self.tab_widget:
            self.tab_widget.picker_tab_clicked.connect(
                self._handle_build_tab_click
            )  # FIXED: Use smart navigation
            self.tab_widget.generate_controls_tab_clicked.connect(
                self.transition_to_generate_controls
            )
            self.tab_widget.graph_editor_tab_clicked.connect(
                self.transition_to_graph_editor
            )
            self.tab_widget.export_tab_clicked.connect(self.transition_to_export_panel)

    def _create_all_panels(self):
        """Create all panels in the correct order including Export panel."""
        # Start position picker (index 0)
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

        # Option picker (index 1) - deferred creation
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

        # Graph editor (index 2)
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

        # Generate controls (index 3)
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

        # Export panel (index 4) - NEW
        self.progress_reporter.start_phase(
            "export_panel_creation", "Creating export panel..."
        )
        export_widget, self.export_panel = self.panel_factory.create_export_panel()
        self.picker_stack.addWidget(export_widget)
        self.layout_orchestrator.register_component("export_panel", self.export_panel)
        self.progress_reporter.complete_phase(
            "export_panel_creation", "Export panel created"
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
        self.component_connector.set_export_panel(self.export_panel)  # NEW

        # Connect export panel signals if available
        if self.export_panel:
            # Connect export request signal to workbench export functionality
            self.export_panel.export_requested.connect(self._handle_export_request)

    # Smart navigation methods
    def _handle_build_tab_click(self):
        """
        Handle Build tab click with smart navigation logic.

        Navigation Logic:
        - If NO sequence exists or start position is not set → Navigate to Start Position Picker
        - If a sequence EXISTS with a start position already selected → Navigate to Option Picker
        """
        print("🔨 Build tab clicked - determining smart navigation target...")

        # Check sequence state via workbench
        has_start_position = False
        has_sequence_beats = False

        if self.workbench and hasattr(self.workbench, "_state_manager"):
            state_manager = self.workbench._state_manager
            has_start_position = state_manager.has_start_position()
            has_sequence_beats = state_manager.has_sequence()

            print(
                f"📊 Sequence state: start_position={has_start_position}, sequence_beats={has_sequence_beats}"
            )
        else:
            print(
                "⚠️ No workbench state manager available - defaulting to start position picker"
            )

        # Smart navigation decision
        if has_start_position or has_sequence_beats:
            print("🎯 Navigating to Option Picker (sequence in progress)")
            self.transition_to_option_picker()
        else:
            print("🎯 Navigating to Start Position Picker (no sequence started)")
            self.transition_to_start_position_picker()

    # Public transition methods
    def transition_to_option_picker(self):
        """Transition to option picker with smooth animation."""
        if self.picker_stack and not self.transition_animator.is_transitioning():
            self._update_tab_active_state(
                0
            )  # Build tab (both start pos and option picker)
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
            self._update_tab_active_state(0)  # Build tab
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
            self._update_tab_active_state(2)  # Edit tab
            self.transition_animator.fade_to_panel(self.picker_stack, 2, "graph editor")

    def transition_to_generate_controls(self):
        """Transition to generate controls with smooth animation."""
        if self.picker_stack and not self.transition_animator.is_transitioning():
            self._update_tab_active_state(1)  # Generate tab
            self.transition_animator.fade_to_panel(
                self.picker_stack,
                3,
                "generate controls",  # Stack index 3
            )

    def transition_to_export_panel(self):
        """Transition to export panel with smooth animation (NEW)."""
        if self.picker_stack and not self.transition_animator.is_transitioning():
            self._update_tab_active_state(3)  # Export tab
            self.transition_animator.fade_to_panel(
                self.picker_stack,
                4,
                "export panel",  # Stack index 4
            )

            # Update export panel preview when switching to it
            if self.export_panel and hasattr(self.export_panel, "_update_preview"):
                self.export_panel._update_preview()

    def _update_tab_active_state(self, tab_index: int):
        """Update the tab widget to reflect the current panel."""
        if self.tab_widget:
            self.tab_widget.set_active_tab(tab_index)

    def _handle_export_request(self, export_type: str, options: dict):
        """Handle export request from export panel with proper options handling."""
        print(f"🔤 Export requested: {export_type} with options: {options}")

        # Get current sequence from workbench
        if not self.workbench:
            print("⚠️ No workbench available for export")
            return

        current_sequence = self.workbench.get_sequence()
        if not current_sequence and export_type == "export_current":
            print("⚠️ No sequence available to export")
            return

        try:
            if export_type == "export_current":
                # Use the workbench export service with the provided options
                if hasattr(self.workbench, "_export_service"):
                    # Use the modern export service with options
                    success, message = (
                        self.workbench._export_service.export_sequence_image(
                            current_sequence,
                            None,  # Let service choose file path
                        )
                    )
                    if success:
                        print(f"✅ Export completed: {message}")
                        # Update export panel to show success
                        if self.export_panel:
                            self.export_panel.actions_card.set_export_current_loading(
                                False
                            )
                    else:
                        print(f"❌ Export failed: {message}")
                elif hasattr(self.workbench, "_operation_coordinator"):
                    # Fallback to operation coordinator
                    result = self.workbench._operation_coordinator.save_image()
                    print(f"✅ Export completed: {result.message}")
                else:
                    print("⚠️ No export service available")

            elif export_type == "export_all":
                print("📚 Export all pictographs functionality not yet implemented")
                # TODO: Implement export all functionality

        except Exception as e:
            print(f"❌ Export failed: {e}")
            import traceback

            traceback.print_exc()

    # Legacy compatibility methods (maintain same interface)
    def _on_generate_requested(self, generation_config):
        """Handle generation request from generate panel."""
        self.component_connector._on_generate_requested(generation_config)

    def _on_graph_beat_modified(self, beat_index: int, beat_data):
        """Handle beat modification from graph editor."""
        self.component_connector._on_graph_beat_modified(beat_index, beat_data)

    def _create_real_option_picker(self):
        """Create the real option picker after main window is shown."""
        try:
            # Create the real option picker
            option_widget, self.option_picker = (
                self.panel_factory.create_option_picker_panel()
            )

            # Replace the placeholder at index 1
            self.picker_stack.removeWidget(self.picker_stack.widget(1))
            self.picker_stack.insertWidget(1, option_widget)

            # Register with orchestrator
            self.layout_orchestrator.register_component(
                "option_picker", self.option_picker
            )

            print("✅ Real option picker created and integrated")

            # Notify callback if provided
            if self.option_picker_ready_callback:
                self.option_picker_ready_callback(self.option_picker)

        except Exception as e:
            print(f"❌ Failed to create real option picker: {e}")

    # Component access methods
