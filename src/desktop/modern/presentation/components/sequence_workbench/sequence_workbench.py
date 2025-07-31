"""
Modern Sequence Workbench - Simplified Qt Presentation Layer

Thin Qt adapter that uses framework-agnostic business services.
Follows established architectural patterns with clean separation of concerns.

SIMPLIFIED RESPONSIBILITIES:
- Qt widget setup and signal handling
- Service coordination via dependency injection
- UI state updates based on business state changes
- Event propagation to parent components

BUSINESS LOGIC DELEGATED TO:
- WorkbenchStateManager: State management
- WorkbenchOperationCoordinator: Operation execution
- WorkbenchSessionManager: Session restoration
- BeatSelectionService: Beat selection logic
"""

from typing import TYPE_CHECKING, Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.core_services import ILayoutService
from desktop.modern.domain.models import BeatData, SequenceData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.components.component_base import ViewableComponentBase

# Event bus removed - using Qt signals instead
EVENT_BUS_AVAILABLE = False
from shared.application.services.workbench.workbench_operation_coordinator import (
    OperationResult,
    OperationType,
    WorkbenchOperationCoordinator,
)
from shared.application.services.workbench.workbench_session_manager import (
    WorkbenchSessionManager,
)
from shared.application.services.workbench.workbench_state_manager import (
    WorkbenchStateManager,
)

from .beat_frame_section import WorkbenchBeatFrameSection
from .button_interface import WorkbenchButtonInterfaceAdapter
from .event_handler_helper import EventHandlerHelper
from .indicator_section import WorkbenchIndicatorSection
from .signal_connection_helper import SignalConnectionHelper
from .ui_setup_helper import UISetupHelper

if TYPE_CHECKING:
    from shared.application.services.workbench.beat_selection_service import (
        BeatSelectionService,
    )


class SequenceWorkbench(ViewableComponentBase):
    """
    Modern sequence workbench - thin Qt adapter using business services.

    Dramatically simplified from 600+ lines to ~150 lines by extracting business logic
    into framework-agnostic services following established architectural patterns.
    """

    # Qt signals for parent coordination
    sequence_modified = pyqtSignal(object)
    sequence_modified_with_operation = pyqtSignal(
        object, str
    )  # sequence, operation_type
    operation_completed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    # 3-panel system signals
    picker_mode_requested = pyqtSignal()
    graph_editor_requested = pyqtSignal()
    generate_requested = pyqtSignal()
    edit_construct_toggle_requested = pyqtSignal(bool)
    clear_sequence_requested = pyqtSignal()

    def __init__(
        self,
        container: DIContainer,
        layout_service: ILayoutService,
        beat_selection_service: "BeatSelectionService",
        parent: Optional[QWidget] = None,
    ):
        """Initialize workbench with injected services."""
        super().__init__(container, parent)

        # Store direct Qt dependencies
        self._layout_service = layout_service
        self._beat_selection_service = beat_selection_service

        # Resolve business services from container
        self._state_manager: WorkbenchStateManager = container.resolve(
            WorkbenchStateManager
        )
        self._operation_coordinator: WorkbenchOperationCoordinator = container.resolve(
            WorkbenchOperationCoordinator
        )
        self._session_manager: WorkbenchSessionManager = container.resolve(
            WorkbenchSessionManager
        )

        # Qt components
        self._indicator_section: Optional[WorkbenchIndicatorSection] = None
        self._beat_frame_section: Optional[WorkbenchBeatFrameSection] = None
        self._button_interface: Optional[WorkbenchButtonInterfaceAdapter] = None

        # Session restoration tracking
        self._subscription_ids: list[str] = []

        # Helper instances for extracted functionality
        self._ui_setup = UISetupHelper(self)
        self._signal_connector = SignalConnectionHelper(self)
        self._event_handler = EventHandlerHelper(self)

    def _safe_resolve(self, service_key: str):
        """Safely resolve a service, returning None if not available."""
        try:
            return self.container.resolve(service_key)
        except Exception:
            return None

    def initialize(self) -> None:
        """Initialize the workbench component with optimized startup."""
        try:
            # PERFORMANCE OPTIMIZATION: Defer non-critical initialization
            self._ui_setup.setup_ui_minimal()  # Create minimal UI first

            # CRITICAL FIX: Ensure workbench widget is visible
            self._widget.show()
            self._widget.setVisible(True)

            # Mark as initialized early for faster startup
            self._initialized = True
            self.component_ready.emit()

            # DEFERRED: Complete initialization after main window is shown
            from PyQt6.QtCore import QTimer

            QTimer.singleShot(100, self._complete_initialization)

        except Exception as e:
            self.emit_error(f"Failed to initialize workbench: {e}", e)
            raise

    def _complete_initialization(self) -> None:
        """Complete workbench initialization after main window is shown."""
        try:
            print("🔧 [WORKBENCH] Starting deferred initialization...")
            self._setup_session_subscriptions()
            print("🔧 [WORKBENCH] Session subscriptions setup complete")

            self._ui_setup.complete_ui_setup()
            print("🔧 [WORKBENCH] UI setup complete")

            self._signal_connector.connect_signals()
            print("🔧 [WORKBENCH] Signals connected")

            self._ui_setup.setup_button_interface()
            print("🔧 [WORKBENCH] Button interface setup complete")

            self._setup_state_monitoring()  # CRITICAL FIX: Monitor state manager changes
            print("🔧 [WORKBENCH] State monitoring setup complete")

            self._setup_event_subscriptions()  # NEW: Subscribe to event bus events
            print("🔧 [WORKBENCH] Event subscriptions setup complete")

            print("✅ [WORKBENCH] Deferred initialization completed successfully")

        except Exception as e:
            print(f"❌ [WORKBENCH] Error in deferred initialization: {e}")
            import traceback

            traceback.print_exc()
            # Don't raise - allow application to continue with partial workbench

    def get_widget(self) -> QWidget:
        """Get the main widget for this component."""
        if not self._widget:
            raise RuntimeError(
                "SequenceWorkbench not initialized - call initialize() first"
            )
        return self._widget

    # UI Setup methods moved to UISetupHelper

    def _setup_state_monitoring(self):
        """Setup monitoring of state manager changes for automatic UI updates."""
        print("🔗 [WORKBENCH] Setting up state monitoring...")

        # Store the original state manager methods to intercept changes
        if hasattr(self._state_manager, "set_sequence"):
            original_set_sequence = self._state_manager.set_sequence

            def monitored_set_sequence(sequence, from_restoration=False):
                print(
                    f"🔍 [WORKBENCH] State manager set_sequence intercepted: {sequence}"
                )
                result = original_set_sequence(sequence, from_restoration)

                # If the state changed, update our UI
                if result.changed and result.sequence_changed:
                    print("🔄 [WORKBENCH] State changed externally, updating UI...")
                    self._update_ui_from_state()
                    self._update_button_panel_sequence_state()

                return result

            # Replace the method with our monitored version
            self._state_manager.set_sequence = monitored_set_sequence
            print("✅ [WORKBENCH] State monitoring setup complete")
        else:
            print("❌ [WORKBENCH] State manager has no set_sequence method!")

    def _setup_session_subscriptions(self):
        """Setup session restoration event subscriptions."""
        try:
            self._subscription_ids = self._session_manager.setup_event_subscriptions()

            # CRITICAL FIX: Set workbench callback for restoration UI updates
            self._session_manager.set_workbench_callback(self.set_start_position)

        except Exception as e:
            # Don't fail initialization due to session subscription errors
            self.emit_error(f"Failed to setup session subscriptions: {e}", e)

    # Public API - State Management
    def set_sequence(self, sequence: SequenceData):
        """Set the current sequence via state manager."""
        print(
            f"🎯 [WORKBENCH] set_sequence called with: {sequence.length if sequence else 0} beats"
        )

        result = self._state_manager.set_sequence(sequence)

        print(
            f"🎯 [WORKBENCH] State manager result: changed={result.changed}, seq_changed={result.sequence_changed}"
        )

        if result.changed:
            print("🎯 [WORKBENCH] Updating UI from state...")
            self._update_ui_from_state()

            # Update button panel sequence state for smart picker button
            self._update_button_panel_sequence_state()

            # Emit sequence_modified if not in restoration mode
            if not self._state_manager.should_prevent_auto_save():
                complete_sequence = (
                    self._state_manager.get_complete_sequence_with_start_position()
                )
                self.sequence_modified.emit(complete_sequence)

                # Debug output to track sequence updates
                print(
                    f"🔄 [WORKBENCH] Sequence updated: {sequence.length if sequence else 0} beats"
                )
                if sequence:
                    for i, beat in enumerate(sequence.beats):
                        print(
                            f"   Beat {i + 1}: {beat.letter if hasattr(beat, 'letter') else 'Unknown'}"
                        )
        else:
            print("🎯 [WORKBENCH] No change detected, UI not updated")

    def get_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence from state manager."""
        return self._state_manager.get_current_sequence()

    def get_start_position_data(self) -> Optional[BeatData]:
        """Get the current start position from state manager."""
        return self._state_manager.get_start_position()

    def set_start_position_data(
        self, start_position: BeatData, position_key: str
    ) -> None:
        """Set the start position via state manager."""
        print(f"🎯 [WORKBENCH] set_start_position_data called with: {position_key}")

        result = self._state_manager.set_start_position(start_position)

        if result.changed:
            print("🎯 [WORKBENCH] Start position changed, updating UI")
            self._update_ui_from_state()

            # Update button panel sequence state for smart picker button
            self._update_button_panel_sequence_state()

            # Emit signals if not in restoration mode
            if not self._state_manager.should_prevent_auto_save():
                # Emit appropriate signals for start position change
                complete_sequence = (
                    self._state_manager.get_complete_sequence_with_start_position()
                )
                if complete_sequence:
                    self.sequence_modified.emit(complete_sequence)

                print(f"🔄 [WORKBENCH] Start position updated: {position_key}")
        else:
            print("🎯 [WORKBENCH] No start position change detected")

    def set_start_position(
        self,
        start_position_data: BeatData,
        pictograph_data: Optional["PictographData"] = None,
        from_restoration: bool = False,
    ):
        """Set the start position via state manager."""
        print(
            f"🎯 [WORKBENCH] set_start_position called with: {start_position_data.letter if hasattr(start_position_data, 'letter') else 'BeatData'}"
        )
        print(f"🎯 [WORKBENCH] pictograph_data provided: {pictograph_data is not None}")
        print(f"🎯 [WORKBENCH] from_restoration: {from_restoration}")

        result = self._state_manager.set_start_position(
            start_position_data, from_restoration
        )

        print(f"🎯 [WORKBENCH] Start position state result: changed={result.changed}")

        # CRITICAL FIX: Always update UI when start position is set, regardless of state change
        # This ensures the start position view always reflects the current selection
        print(
            "🎯 [WORKBENCH] Updating beat frame with start position (always update UI)..."
        )

        # Update beat frame section - this should always happen for user selections
        if self._beat_frame_section:
            self._beat_frame_section.set_start_position(
                start_position_data, pictograph_data
            )

        # Update button panel sequence state for smart picker button
        self._update_button_panel_sequence_state()

        # Only emit sequence_modified if state actually changed and not in restoration mode
        if result.changed and not self._state_manager.should_prevent_auto_save():
            complete_sequence = (
                self._state_manager.get_complete_sequence_with_start_position()
            )
            if complete_sequence:
                self.sequence_modified.emit(complete_sequence)
                print("🎯 [WORKBENCH] Sequence modified signal emitted")
        else:
            print(
                f"🎯 [WORKBENCH] Skipping sequence modified signal (changed={result.changed}, auto_save_prevented={self._state_manager.should_prevent_auto_save()})"
            )

    def get_start_position(self) -> Optional[BeatData]:
        """Get the current start position from state manager."""
        return self._state_manager.get_start_position()

    def clear_start_position(self):
        """Clear the start position via state manager."""
        self._state_manager.set_start_position(None)
        if self._beat_frame_section:
            self._beat_frame_section.initialize_cleared_start_position()

    def get_button_interface(self) -> Optional[WorkbenchButtonInterfaceAdapter]:
        """Get the button interface adapter."""
        return self._button_interface

    # Event Handlers - Delegation to Business Logic
    def _execute_operation(self, operation_type: OperationType):
        """Execute operation via operation coordinator."""
        self._event_handler.execute_operation(operation_type)

    def _handle_delete_beat(self):
        """Handle delete beat operation."""
        self._event_handler.handle_delete_beat()

    def _handle_clear(self):
        """Handle clear sequence operation."""
        self._event_handler.handle_clear()

    def _handle_operation_result(self, result: OperationResult):
        """Handle operation result from coordinator."""
        print(f"📊 [WORKBENCH] Handling operation result: success={result.success}")
        if not result.success:
            print(f"❌ [WORKBENCH] Operation failed: {result.message}")
            if hasattr(result, "error_details") and result.error_details:
                print(f"🔍 [WORKBENCH] Error details: {result.error_details}")
        if result.success:
            print(f"✅ [WORKBENCH] Operation successful: {result.message}")
            self.operation_completed.emit(result.message)

            # Update state if sequence was modified
            if result.updated_sequence:
                print(
                    f"🔄 [WORKBENCH] Updating state with sequence: {len(result.updated_sequence.beats)} beats"
                )
                state_result = self._state_manager.set_sequence(result.updated_sequence)
                print(
                    f"📊 [WORKBENCH] State update result: changed={state_result.changed}"
                )
                if state_result.changed:
                    print("🔄 [WORKBENCH] Updating UI from state...")
                    self._update_ui_from_state()

                    # Emit both signals - new signal includes operation type
                    self.sequence_modified.emit(result.updated_sequence)
                    self.sequence_modified_with_operation.emit(
                        result.updated_sequence, result.operation_type.value
                    )

                    print(
                        f"✅ [WORKBENCH] UI updated and sequence_modified signals emitted (operation: {result.operation_type.value})"
                    )
            else:
                print("⚠️ [WORKBENCH] No updated sequence in result")

            # Show success message on button
            if self._beat_frame_section:
                self._beat_frame_section.show_button_message(
                    result.operation_type.value, result.message, 2000
                )
        else:
            self.error_occurred.emit(result.message)

            # Show error message on button
            if self._beat_frame_section:
                self._beat_frame_section.show_button_message(
                    result.operation_type.value, f"❌ {result.message}", 3000
                )

    # UI Update Methods
    def _update_ui_from_state(self):
        """Update UI components based on current business state."""
        sequence = self._state_manager.get_current_sequence()
        print(f"🔄 [WORKBENCH] Updating UI from state - sequence: {sequence}")
        print(
            f"🔄 [WORKBENCH] Sequence length: {sequence.length if sequence else 'None'}"
        )

        # Update indicator section
        if self._indicator_section:
            print("🔄 [WORKBENCH] Updating indicator section...")
            self._indicator_section.update_sequence(sequence)

        # Update beat frame section
        if self._beat_frame_section:
            print("🔄 [WORKBENCH] Updating beat frame section...")
            self._beat_frame_section.set_sequence(sequence)
        else:
            print("❌ [WORKBENCH] No beat frame section available!")

        # Update button panel state
        print("🔄 [WORKBENCH] Updating button panel state...")
        self._update_button_panel_sequence_state()

    def _on_beat_selected(self, beat_index: int):
        """Handle beat selection from UI."""
        # Update button states based on selection
        if self._beat_frame_section:
            self._beat_frame_section.set_button_enabled(
                "delete_beat", beat_index is not None
            )

    def _on_beat_modified(self, beat_index: int, beat_data):
        """Handle beat modification from UI."""
        # This would typically go through a command/operation instead of direct modification
        # For now, maintain existing behavior
        sequence = self._state_manager.get_current_sequence()
        if sequence and beat_index < len(sequence.beats):
            new_beats = list(sequence.beats)
            new_beats[beat_index] = beat_data
            updated_sequence = sequence.update(beats=new_beats)

            self.set_sequence(updated_sequence)

    def _on_sequence_modified(self, sequence):
        """Handle sequence modification from UI."""
        print(
            f"📝 [WORKBENCH] Sequence modified from UI: {sequence.length if sequence else 0} beats"
        )
        self.set_sequence(sequence)

    def _update_button_panel_sequence_state(self):
        """Update button panel with current sequence state for smart picker button."""
        if self._beat_frame_section and hasattr(
            self._beat_frame_section, "set_sequence_state"
        ):
            current_sequence = self._state_manager.get_current_sequence()
            start_position = self._state_manager.get_start_position()
            has_sequence = current_sequence and len(current_sequence.beats) > 0
            has_start_position = start_position is not None

            self._beat_frame_section.set_sequence_state(
                has_sequence, has_start_position
            )

    # Cleanup
    def cleanup(self) -> None:
        """Clean up workbench resources."""
        try:
            # Clean up session subscriptions
            if self._session_manager and self._subscription_ids:
                self._session_manager.cleanup_event_subscriptions(
                    self._subscription_ids
                )
                self._subscription_ids.clear()

            # Clean up button interface
            if self._button_interface:
                # Button interface cleanup if needed
                pass

            # Call parent cleanup
            super().cleanup()

        except Exception as e:
            self.emit_error(f"Error during cleanup: {e}", e)

    def _setup_event_subscriptions(self):
        """Setup event bus subscriptions."""
        if self.event_bus and EVENT_BUS_AVAILABLE:
            try:
                # Subscribe to start position selection events
                self.event_bus.subscribe(
                    "sequence.start_position_selected",
                    self._handle_start_position_selected_event,
                )
                print("📡 [WORKBENCH] Subscribed to start position events")
            except Exception as e:
                print(f"❌ [WORKBENCH] Failed to setup event subscriptions: {e}")
        else:
            print("⚠️ [WORKBENCH] Event bus not available, skipping subscriptions")

    def _handle_start_position_selected_event(self, event):
        """Handle start position selected event from event bus."""
        try:
            print(f"📡 [WORKBENCH] Received start position event: {event.position_key}")

            # Convert event data to beat data format
            if event.beat_data:
                # Create a simple beat data object from the event
                from desktop.modern.domain.models import BeatData

                beat_data = BeatData(
                    letter=event.beat_data.get("letter", event.position_key),
                    position_key=event.position_key,
                    # Add other required fields with defaults
                )

                # Set the start position using the state manager
                result = self._state_manager.set_start_position(beat_data)
                if result.changed:
                    print(
                        f"✅ [WORKBENCH] Start position set via event bus: {event.position_key}"
                    )
                    # Trigger UI update
                    self._update_ui_from_state()
                else:
                    print(
                        f"⚠️ [WORKBENCH] Start position unchanged: {event.position_key}"
                    )
            else:
                print("⚠️ [WORKBENCH] No beat data in start position event")

        except Exception as e:
            print(f"❌ [WORKBENCH] Error handling start position event: {e}")
            import traceback

            traceback.print_exc()

    # New panel mode handlers
    def _handle_picker_mode_request(self):
        """Handle picker mode request with smart switching."""
        self._event_handler.handle_picker_mode_request()

    def _handle_graph_editor_request(self):
        """Handle graph editor mode request."""
        self._event_handler.handle_graph_editor_request()

    def _handle_generate_request(self):
        """Handle generate controls mode request."""
        self._event_handler.handle_generate_request()

    def _handle_panel_mode_change(self, mode: str):
        """Handle panel mode change notification."""
        print(f"🔄 [WORKBENCH] Panel mode changed to: {mode}")
        # Update internal state if needed

        # Update button panel sequence state for smart picker button
        if self._beat_frame_section:
            current_sequence = self._state_manager.get_current_sequence()
            start_position = self._state_manager.get_start_position()
            has_sequence = current_sequence and len(current_sequence.beats) > 0
            has_start_position = start_position is not None

            if hasattr(self._beat_frame_section, "set_sequence_state"):
                self._beat_frame_section.set_sequence_state(
                    has_sequence, has_start_position
                )
