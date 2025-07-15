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

from typing import TYPE_CHECKING, List, Optional

from application.services.workbench.workbench_operation_coordinator import (
    OperationResult,
    OperationType,
    WorkbenchOperationCoordinator,
)
from application.services.workbench.workbench_session_manager import (
    WorkbenchSessionManager,
)
from application.services.workbench.workbench_state_manager import WorkbenchStateManager
from core.dependency_injection.di_container import DIContainer
from core.interfaces.core_services import ILayoutService
from domain.models import BeatData, SequenceData
from domain.models.pictograph_data import PictographData
from presentation.components.component_base import ViewableComponentBase
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from .beat_frame_section import WorkbenchBeatFrameSection
from .button_interface import WorkbenchButtonInterfaceAdapter
from .indicator_section import WorkbenchIndicatorSection

if TYPE_CHECKING:
    from application.services.workbench.beat_selection_service import (
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
        self._subscription_ids: List[str] = []

    def _safe_resolve(self, service_key: str):
        """Safely resolve a service, returning None if not available."""
        try:
            return self.container.resolve(service_key)
        except Exception:
            return None

    def initialize(self) -> None:
        """Initialize the workbench component."""
        try:
            self._setup_session_subscriptions()
            self._setup_ui()
            self._connect_signals()
            self._setup_button_interface()

            # Mark as initialized
            self._initialized = True
            self.component_ready.emit()

        except Exception as e:
            self.emit_error(f"Failed to initialize workbench: {e}", e)
            raise

    def get_widget(self) -> QWidget:
        """Get the main widget for this component."""
        if not self._widget:
            raise RuntimeError(
                "SequenceWorkbench not initialized - call initialize() first"
            )
        return self._widget

    # UI Setup
    def _setup_ui(self):
        """Setup UI layout using existing components."""
        # Create main widget
        self._widget = QWidget(self.parent())
        main_layout = QVBoxLayout(self._widget)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # Create sections using existing components
        self._indicator_section = WorkbenchIndicatorSection(
            dictionary_service=self._safe_resolve("SequenceDictionaryService"),
            parent=self._widget,
        )
        main_layout.addWidget(self._indicator_section, 0)

        self._beat_frame_section = WorkbenchBeatFrameSection(
            layout_service=self._layout_service,
            beat_selection_service=self._beat_selection_service,
            parent=self._widget,
        )
        main_layout.addWidget(self._beat_frame_section, 1)

    def _connect_signals(self):
        """Connect component signals to business logic."""
        if self._beat_frame_section:
            # Beat frame signals -> business logic
            self._beat_frame_section.beat_selected.connect(self._on_beat_selected)
            self._beat_frame_section.beat_modified.connect(self._on_beat_modified)
            self._beat_frame_section.sequence_modified.connect(
                self._on_sequence_modified
            )

            # Operation signals -> operation coordinator
            self._beat_frame_section.add_to_dictionary_requested.connect(
                lambda: self._execute_operation(OperationType.ADD_TO_DICTIONARY)
            )
            self._beat_frame_section.save_image_requested.connect(
                lambda: self._execute_operation(OperationType.SAVE_IMAGE)
            )
            self._beat_frame_section.view_fullscreen_requested.connect(
                lambda: self._execute_operation(OperationType.VIEW_FULLSCREEN)
            )
            self._beat_frame_section.mirror_sequence_requested.connect(
                lambda: self._execute_operation(OperationType.MIRROR_SEQUENCE)
            )
            self._beat_frame_section.swap_colors_requested.connect(
                lambda: self._execute_operation(OperationType.SWAP_COLORS)
            )
            self._beat_frame_section.rotate_sequence_requested.connect(
                lambda: self._execute_operation(OperationType.ROTATE_SEQUENCE)
            )
            self._beat_frame_section.copy_json_requested.connect(
                lambda: self._execute_operation(OperationType.COPY_JSON)
            )
            self._beat_frame_section.delete_beat_requested.connect(
                self._handle_delete_beat
            )
            self._beat_frame_section.clear_sequence_requested.connect(
                self._handle_clear
            )

    def _setup_button_interface(self):
        """Setup button interface adapter."""
        self._button_interface = WorkbenchButtonInterfaceAdapter(self._widget)
        if self._button_interface.signals:
            self._button_interface.signals.sequence_modified.connect(
                self.sequence_modified
            )
            self._button_interface.signals.operation_completed.connect(
                self.operation_completed
            )
            self._button_interface.signals.operation_failed.connect(self.error_occurred)

    def _setup_session_subscriptions(self):
        """Setup session restoration event subscriptions."""
        try:
            self._subscription_ids = self._session_manager.setup_event_subscriptions()
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
            print(f"🎯 [WORKBENCH] Updating UI from state...")
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
                            f"   Beat {i+1}: {beat.letter if hasattr(beat, 'letter') else 'Unknown'}"
                        )
        else:
            print(f"🎯 [WORKBENCH] No change detected, UI not updated")

    def get_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence from state manager."""
        return self._state_manager.get_current_sequence()

    def set_start_position(
        self,
        start_position_data: BeatData,
        pictograph_data: Optional["PictographData"] = None,
    ):
        """Set the start position via state manager."""
        print(
            f"🎯 [WORKBENCH] set_start_position called with: {start_position_data.letter if hasattr(start_position_data, 'letter') else 'BeatData'}"
        )
        print(f"🎯 [WORKBENCH] pictograph_data provided: {pictograph_data is not None}")

        result = self._state_manager.set_start_position(start_position_data)

        print(f"🎯 [WORKBENCH] Start position state result: changed={result.changed}")

        if result.changed:
            print(f"🎯 [WORKBENCH] Updating beat frame with start position...")
            # Update beat frame section
            if self._beat_frame_section:
                self._beat_frame_section.set_start_position(
                    start_position_data, pictograph_data
                )

            # Update button panel sequence state for smart picker button
            self._update_button_panel_sequence_state()

            # Emit sequence_modified if not in restoration mode
            if not self._state_manager.should_prevent_auto_save():
                complete_sequence = (
                    self._state_manager.get_complete_sequence_with_start_position()
                )
                if complete_sequence:
                    self.sequence_modified.emit(complete_sequence)
        else:
            print(f"🎯 [WORKBENCH] Start position unchanged, no UI update needed")

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
        # Get operation method from coordinator
        operation_methods = {
            OperationType.ADD_TO_DICTIONARY: self._operation_coordinator.add_to_dictionary,
            OperationType.SAVE_IMAGE: self._operation_coordinator.save_image,
            OperationType.VIEW_FULLSCREEN: self._operation_coordinator.view_fullscreen,
            OperationType.MIRROR_SEQUENCE: self._operation_coordinator.mirror_sequence,
            OperationType.SWAP_COLORS: self._operation_coordinator.swap_colors,
            OperationType.ROTATE_SEQUENCE: self._operation_coordinator.rotate_sequence,
            OperationType.COPY_JSON: self._operation_coordinator.copy_json,
        }

        operation_method = operation_methods.get(operation_type)
        if not operation_method:
            self.error_occurred.emit(f"Unknown operation: {operation_type}")
            return

        # Execute operation
        result: OperationResult = operation_method()
        self._handle_operation_result(result)

    def _handle_delete_beat(self):
        """Handle delete beat operation."""
        print("🗑️ [WORKBENCH] Delete beat operation requested")
        print(f"🔍 [WORKBENCH] Workbench state manager: {self._state_manager}")
        print(f"🔍 [WORKBENCH] Workbench state manager ID: {id(self._state_manager)}")
        print(f"🔍 [WORKBENCH] Operation coordinator: {self._operation_coordinator}")

        selected_index = None
        if self._beat_frame_section:
            selected_index = self._beat_frame_section.get_selected_beat_index()
            print(f"📊 [WORKBENCH] Selected beat index: {selected_index}")

        print("🔄 [WORKBENCH] Calling operation coordinator...")
        result = self._operation_coordinator.delete_beat(selected_index)
        print(
            f"📊 [WORKBENCH] Operation result: success={result.success}, message='{result.message}'"
        )
        self._handle_operation_result(result)

    def _handle_clear(self):
        """Handle clear sequence operation."""
        print(f"🧹 [WORKBENCH] Clear sequence requested")

        # Clear the sequence via state manager
        result = self._state_manager.set_sequence(None)

        if result.changed:
            print(f"🧹 [WORKBENCH] Sequence cleared, updating UI...")
            # Update UI to reflect the cleared sequence
            self._update_ui_from_state()

            # IMPORTANT: Clear the start position data from state manager
            # so that when a new start position is selected, it will be detected as a change
            print(f"🧹 [WORKBENCH] Clearing start position data from state manager...")
            self._state_manager.set_start_position(None)

            # Reset start position to text-only mode (no pictograph)
            if self._beat_frame_section:
                print(f"🧹 [WORKBENCH] Initializing cleared start position view...")
                self._beat_frame_section.initialize_cleared_start_position()

            # Update button panel state after clearing
            self._update_button_panel_sequence_state()

        # Also emit the signal for any parent handlers
        self.clear_sequence_requested.emit()

        # Reset button panel to picker mode
        if self._beat_frame_section and hasattr(
            self._beat_frame_section, "reset_to_picker_mode"
        ):
            self._beat_frame_section.reset_to_picker_mode()

    def _handle_operation_result(self, result: OperationResult):
        """Handle operation result from coordinator."""
        print(f"📊 [WORKBENCH] Handling operation result: success={result.success}")
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

        # Update indicator section
        if self._indicator_section:
            self._indicator_section.update_sequence(sequence)

        # Update beat frame section
        if self._beat_frame_section:
            self._beat_frame_section.set_sequence(sequence)

        # Update button panel state
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

            print(
                f"🔧 [WORKBENCH] Beat {beat_index + 1} modified: {beat_data.letter if hasattr(beat_data, 'letter') else 'Unknown'}"
            )
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

    # New panel mode handlers
    def _handle_picker_mode_request(self):
        """Handle picker mode request with smart switching."""
        current_sequence = self._state_manager.get_current_sequence()
        start_position = self._state_manager.get_start_position()

        # Smart switching logic
        if not start_position:
            print(
                "📍 [WORKBENCH] No start position - transitioning to start position picker"
            )
        elif not current_sequence or len(current_sequence.beats) == 0:
            print(
                "⚡ [WORKBENCH] Has start position but no sequence - transitioning to option picker"
            )
        else:
            print("⚡ [WORKBENCH] Has sequence - staying in option picker")

        # Emit signal to parent to handle layout transition
        self.picker_mode_requested.emit()

    def _handle_graph_editor_request(self):
        """Handle graph editor mode request."""
        print("📊 [WORKBENCH] Graph editor mode requested")
        self.graph_editor_requested.emit()

    def _handle_generate_request(self):
        """Handle generate controls mode request."""
        print("🤖 [WORKBENCH] Generate controls mode requested")
        self.generate_requested.emit()

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
