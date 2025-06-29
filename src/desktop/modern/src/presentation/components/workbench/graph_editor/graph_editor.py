from typing import Optional, TYPE_CHECKING
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QResizeEvent, QKeyEvent

from core.interfaces.workbench_services import IGraphEditorService
from domain.models.core_models import SequenceData, BeatData
from application.services.graph_editor_data_flow_service import (
    GraphEditorDataFlowService,
)
from application.services.graph_editor_hotkey_service import (
    GraphEditorHotkeyService,
)

# Import our specialized component classes
from .animation_controller import GraphEditorAnimationController
from .signal_coordinator import GraphEditorSignalCoordinator
from .layout_manager import GraphEditorLayoutManager
from .state_manager import GraphEditorStateManager

if TYPE_CHECKING:
    from presentation.components.workbench.workbench import (
        ModernSequenceWorkbench,
    )


class GraphEditor(QFrame):
    """
    Modern graph editor component following clean architecture patterns.

    Acts as a coordinator that delegates functionality to specialized components:
    - AnimationController: Handles sliding animations and height management
    - SignalCoordinator: Manages signal connections and communication
    - LayoutManager: Handles UI setup, styling, and component positioning
    - StateManager: Manages sequence, beat, arrow, and visibility state

    This refactored design improves maintainability, testability, and separation of concerns.
    """

    # Public signals for external communication
    beat_modified = pyqtSignal(BeatData)
    arrow_selected = pyqtSignal(str)  # arrow_id
    visibility_changed = pyqtSignal(bool)  # is_visible

    def __init__(
        self,
        graph_service: IGraphEditorService,
        parent: Optional["ModernSequenceWorkbench"] = None,
        workbench_width: int = 800,
        workbench_height: int = 600,
    ):
        super().__init__(parent)

        # Core dependencies
        self._graph_service = graph_service
        self._parent_workbench = parent

        # Initialize specialized component managers
        self.state_manager = GraphEditorStateManager(self)
        self._animation_controller = GraphEditorAnimationController(self)
        self._layout_manager = GraphEditorLayoutManager(self)
        self._signal_coordinator = GraphEditorSignalCoordinator(self)

        # Update animation controller with workbench dimensions
        self._animation_controller.update_workbench_size(
            workbench_width, workbench_height
        )

        # Initialize services
        self._data_flow_service = GraphEditorDataFlowService(self)
        self._hotkey_service = GraphEditorHotkeyService(graph_service, self)

        # Setup the UI and wire everything together
        self._initialize_components()

        # Synchronize width with workbench after initialization
        self.sync_width_with_workbench()

        # Start hidden like legacy
        self.hide()

    def _initialize_components(self) -> None:
        """Initialize all components and wire them together"""
        # Setup UI layout and components
        self._layout_manager.setup_ui()

        # Provide dependencies to signal coordinator
        self._signal_coordinator.set_dependencies(
            data_flow_service=self._data_flow_service,
            hotkey_service=self._hotkey_service,
            animation_controller=self._animation_controller,
            layout_manager=self._layout_manager,
            state_manager=self.state_manager,
        )

        # Connect external signals to our public API
        self._connect_external_signals()

        # Show toggle tab
        self._layout_manager.show_toggle_tab()

    def _connect_external_signals(self) -> None:
        """Connect internal signals to external public API"""
        # Forward signals from signal coordinator to our public API
        self._signal_coordinator.beat_modified.connect(self.beat_modified.emit)
        self._signal_coordinator.arrow_selected.connect(self.arrow_selected.emit)
        self._signal_coordinator.visibility_changed.connect(
            self.visibility_changed.emit
        )

        # Connect state manager visibility changes to animation controller
        self.state_manager.visibility_changed.connect(self._on_state_visibility_changed)

    def _on_state_visibility_changed(self, is_visible: bool) -> None:
        """Handle visibility state changes"""
        # This ensures state and animation stay in sync
        pass  # State change is handled by the animation system

    # ============================================================================
    # PUBLIC API METHODS (maintaining backward compatibility)
    # ============================================================================

    def set_sequence(self, sequence: Optional[SequenceData]) -> None:
        """Set the current sequence for display/editing"""
        self.state_manager.set_current_sequence(sequence)
        self._graph_service.update_graph_display(sequence)

        # Update all UI components through layout manager
        self._layout_manager.update_component_display(sequence_data=sequence)

    def set_selected_beat(
        self, beat_data: Optional[BeatData], beat_index: Optional[int] = None
    ) -> None:
        """Set the currently selected beat for editing"""
        # Update state
        self.state_manager.set_selected_beat(beat_data, beat_index)

        # Update service
        self._graph_service.set_selected_beat(beat_data, beat_index)

        # Update data flow service context
        self.state_manager.update_data_flow_context(self._data_flow_service)

        # Update UI components
        self._layout_manager.update_component_display(beat_data=beat_data)

    def toggle_visibility(self) -> None:
        """Toggle graph editor visibility with smooth sliding animation"""
        print("🔄 toggle_visibility() called")

        # Prevent multiple animations
        if self._animation_controller.is_animating():
            print("  ⚠️ Animation already in progress, skipping")
            return

        # Validate state synchronization before making decisions
        print("  🔍 Calling validate_state_synchronization()...")
        is_synchronized = self._animation_controller.validate_state_synchronization()
        print(f"  🔍 Validation result: {is_synchronized}")
        if not is_synchronized:
            print("  🔧 State desynchronization detected and corrected")

        current_visibility = self.state_manager.is_visible()
        current_height = self.height()
        print(
            f"  📊 Current visibility: {current_visibility}, height: {current_height}"
        )

        if current_visibility:
            # Hide: start animation (state will be updated when animation completes)
            print("  🔽 Calling slide_down()")
            self._animation_controller.slide_down()
        else:
            # Show: start animation (state will be updated when animation completes)
            print("  🔼 Calling slide_up()")
            self._animation_controller.slide_up()

    def is_visible(self) -> bool:
        """Check if graph editor is currently visible"""
        return self.state_manager.is_visible()

    def get_preferred_height(self) -> int:
        """Get the preferred height for the graph editor"""
        return self._animation_controller.get_preferred_height()

    def update_workbench_size(self, width: int, height: int) -> None:
        """Update workbench size reference when workbench resizes"""
        self._animation_controller.update_workbench_size(width, height)

        # Synchronize graph editor width with workbench width
        self.sync_width_with_workbench()

    def sync_width_with_workbench(self) -> None:
        """Synchronize graph editor width with parent workbench width"""
        # CRITICAL FIX: Don't sync width during animation to prevent interference
        if (
            hasattr(self, "_animation_controller")
            and self._animation_controller.is_animating()
        ):
            print("🚫 [WIDTH SYNC] Blocking width sync during animation")
            return

        if self._parent_workbench:
            workbench_width = self._parent_workbench.width()
            if workbench_width > 0:
                # CRITICAL FIX: Prevent width sync loops
                current_width = self.width()
                if abs(current_width - workbench_width) < 5:  # Less than 5px difference
                    return  # Skip micro-adjustments that cause loops

                # Set graph editor width to match workbench width
                self.setFixedWidth(workbench_width)
                print(
                    f"🔄 [WIDTH SYNC] Graph editor width synchronized: {current_width}px → {workbench_width}px"
                )

                # Notify pictograph container of width change
                if (
                    hasattr(self, "_pictograph_container")
                    and self._pictograph_container
                ):
                    self._pictograph_container.handle_width_change(workbench_width)

    def get_current_width(self) -> int:
        """Get the current graph editor width"""
        return self.width()

    def get_workbench_width(self) -> int:
        """Get the parent workbench width"""
        if self._parent_workbench:
            return self._parent_workbench.width()
        return 800  # Default fallback

    def _debug_setFixedHeight(self, height: int) -> None:
        """Debug wrapper for setFixedHeight to track all height changes"""
        current_height = self.height()
        is_visible = hasattr(self, "_state_manager") and self.state_manager.is_visible()

        print(
            f"🎯 [HEIGHT DEBUG] setFixedHeight called: {current_height}px -> {height}px (visible={is_visible})"
        )

        # CRITICAL: Track unwanted height changes when collapsed (for debugging)
        if not is_visible and height > 0:
            print(
                f"🚨 [HEIGHT DEBUG] CRITICAL: Setting height {height}px when graph editor should be collapsed!"
            )
            print(f"🚨 [HEIGHT DEBUG] This may indicate an issue - monitoring...")

            # Get some call stack info for debugging
            import traceback

            print("🚨 [HEIGHT DEBUG] Call stack:")
            for line in traceback.format_stack()[
                -5:
            ]:  # Last 5 stack frames for context
                print(f"    {line.strip()}")

            # Allow the height change but log it for analysis

        # Call the original method
        self._original_setFixedHeight(height)

    # ============================================================================
    # COMPONENT PROPERTY ACCESS (for backward compatibility)
    # ============================================================================

    @property
    def _pictograph_container(self):
        """Access to pictograph container for backward compatibility"""
        return self._layout_manager.pictograph_container

    @_pictograph_container.setter
    def _pictograph_container(self, value):
        """Setter for backward compatibility (managed by layout manager)"""
        pass  # Managed by layout manager

    @property
    def _left_adjustment_panel(self):
        """Access to left adjustment panel for backward compatibility"""
        return self._layout_manager.left_adjustment_panel

    @_left_adjustment_panel.setter
    def _left_adjustment_panel(self, value):
        """Setter for backward compatibility (managed by layout manager)"""
        pass  # Managed by layout manager

    @property
    def _right_adjustment_panel(self):
        """Access to right adjustment panel for backward compatibility"""
        return self._layout_manager.right_adjustment_panel

    @_right_adjustment_panel.setter
    def _right_adjustment_panel(self, value):
        """Setter for backward compatibility (managed by layout manager)"""
        pass  # Managed by layout manager

    @property
    def _adjustment_panel(self):
        """Access to adjustment panel for backward compatibility"""
        return self._layout_manager.right_adjustment_panel

    @_adjustment_panel.setter
    def _adjustment_panel(self, value):
        """Setter for backward compatibility (managed by layout manager)"""
        pass  # Managed by layout manager

    @property
    def _toggle_tab(self):
        """Access to toggle tab for backward compatibility"""
        return self._layout_manager.toggle_tab

    @_toggle_tab.setter
    def _toggle_tab(self, value):
        """Setter for backward compatibility (managed by layout manager)"""
        pass  # Managed by layout manager

    # ============================================================================
    # EVENT HANDLERS
    # ============================================================================

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize events - delegate to layout manager"""
        # print hte call stack
        import traceback

        print("🔍 [HEIGHT DEBUG] Graph editor resize event called")
        for line in traceback.format_stack()[-5:]:  # Last 5 stack frames for context
            print(f"    {line.strip()}")

        # Delegate to layout manager
        super().resizeEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle key press events for hotkeys"""
        # Only handle hotkeys when graph editor is visible and has focus
        if not self.state_manager.is_visible():
            super().keyPressEvent(event)
            return

        # Try hotkey service first
        if self._hotkey_service.handle_key_event(event):
            return  # Handled by hotkey service

        # Pass to parent if not handled
        super().keyPressEvent(event)

    # ============================================================================
    # COMPONENT ACCESS METHODS (for testing and advanced usage)
    # ============================================================================

    def get_state_manager(self) -> GraphEditorStateManager:
        """Get the state manager component"""
        return self.state_manager

    def get_animation_controller(self) -> GraphEditorAnimationController:
        """Get the animation controller component"""
        return self._animation_controller

    def get_layout_manager(self) -> GraphEditorLayoutManager:
        """Get the layout manager component"""
        return self._layout_manager

    def get_signal_coordinator(self) -> GraphEditorSignalCoordinator:
        """Get the signal coordinator component"""
        return self._signal_coordinator

    def get_data_flow_service(self) -> GraphEditorDataFlowService:
        """Get the data flow service"""
        return self._data_flow_service

    def get_hotkey_service(self) -> GraphEditorHotkeyService:
        """Get the hotkey service"""
        return self._hotkey_service

    # ============================================================================
    # DEBUG AND MAINTENANCE METHODS
    # ============================================================================

    def get_state_summary(self) -> dict:
        """Get a comprehensive summary of the current state (useful for debugging)"""
        return {
            "state_manager": self.state_manager.get_state_summary(),
            "animation_controller": {
                "is_animating": self._animation_controller.is_animating(),
                "preferred_height": self._animation_controller.get_preferred_height(),
            },
            "graph_editor": {
                "is_visible_widget": self.isVisible(),
                "height": self.height(),
                "width": self.width(),
            },
        }

    def force_state_validation(self) -> bool:
        """Force validation of all component states"""
        return self.state_manager.force_state_validation()

    def reconnect_signals(self) -> None:
        """Reconnect all signals (useful for debugging signal issues)"""
        self._signal_coordinator.reconnect_ui_component_signals()

    def reset_to_initial_state(self) -> None:
        """Reset the graph editor to its initial state"""
        self.state_manager.reset_all_state()
        self.hide()
