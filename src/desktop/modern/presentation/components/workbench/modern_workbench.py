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
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.core_services import ILayoutService
from desktop.modern.domain.models import BeatData, SequenceData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.components.component_base import ViewableComponentBase
from desktop.modern.presentation.components.sequence_workbench.button_interface import (
    WorkbenchButtonInterfaceAdapter,
)
from desktop.modern.presentation.components.sequence_workbench.indicator_section import (
    WorkbenchIndicatorSection,
)
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
    operation_completed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
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

            # CRITICAL FIX: Ensure workbench widget is visible
            self._widget.show()
            self._widget.setVisible(True)
            print(
                f"🔧 [WORKBENCH] Workbench widget made visible: {self._widget.isVisible()}"
            )

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
            # save_image_requested signal removed - functionality moved to Export tab
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
            self._beat_frame_section.edit_construct_toggle_requested.connect(
                self.edit_construct_toggle_requested
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
        selected_index = None
        if self._beat_frame_section:
            selected_index = self._beat_frame_section.get_selected_beat_index()

        result = self._operation_coordinator.delete_beat(selected_index)
        self._handle_operation_result(result)

    def _handle_clear(self):
        """Handle clear sequence operation."""
        print("🧹 [WORKBENCH] Clear sequence requested")

        # Clear the sequence via state manager
        result = self._state_manager.set_sequence(None)

        if result.changed:
            print("🧹 [WORKBENCH] Sequence cleared, updating UI...")
            # Update UI to reflect the cleared sequence
            self._update_ui_from_state()

            # IMPORTANT: Clear the start position data from state manager
            # so that when a new start position is selected, it will be detected as a change
            print("🧹 [WORKBENCH] Clearing start position data from state manager...")
            self._state_manager.set_start_position(None)

            # Reset start position to text-only mode (no pictograph)
            if self._beat_frame_section:
                print("🧹 [WORKBENCH] Initializing cleared start position view...")
                self._beat_frame_section.initialize_cleared_start_position()

        # Also emit the signal for any parent handlers
        self.clear_sequence_requested.emit()

    def _handle_operation_result(self, result: OperationResult):
        """Handle operation result from coordinator."""
        if result.success:
            self.operation_completed.emit(result.message)

            # Update state if sequence was modified
            if result.updated_sequence:
                state_result = self._state_manager.set_sequence(result.updated_sequence)
                if state_result.changed:
                    self._update_ui_from_state()
                    self.sequence_modified.emit(result.updated_sequence)

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
