"""
Event Handler Helper - Simple extraction from SequenceWorkbench

Extracted event handler methods without any changes to functionality.
Just moves the code to reduce the main file size.
"""

from __future__ import annotations

from shared.application.services.workbench.workbench_operation_coordinator import (
    OperationResult,
    OperationType,
)


class EventHandlerHelper:
    """Helper class for workbench event handlers - simple extraction."""

    def __init__(self, workbench):
        self.workbench = workbench

    def execute_operation(self, operation_type: OperationType):
        """Execute operation via operation coordinator."""

        # Handle copy JSON specially to pass the current sequence
        if operation_type == OperationType.COPY_JSON:
            current_sequence = self.workbench._state_manager.get_current_sequence()
            operation_method = lambda: self.workbench._operation_coordinator.copy_json(
                current_sequence
            )
        else:
            # Get the operation method from coordinator
            operation_methods = {
                OperationType.ADD_TO_DICTIONARY: self.workbench._operation_coordinator.add_to_dictionary,
                OperationType.VIEW_FULLSCREEN: self.workbench._operation_coordinator.view_fullscreen,
                OperationType.MIRROR_SEQUENCE: self.workbench._operation_coordinator.mirror_sequence,
                OperationType.SWAP_COLORS: self.workbench._operation_coordinator.swap_colors,
                OperationType.ROTATE_SEQUENCE: self.workbench._operation_coordinator.rotate_sequence,
            }

            operation_method = operation_methods.get(operation_type)
            if not operation_method:
                print(f"❌ [WORKBENCH] Unknown operation type: {operation_type}")
                return

        # Execute operation
        result: OperationResult = operation_method()
        self.workbench._handle_operation_result(result)

    def handle_delete_beat(self):
        """Handle delete beat operation."""
        selected_index = None
        if self.workbench._beat_frame_section:
            selected_index = (
                self.workbench._beat_frame_section.get_selected_beat_index()
            )

        result = self.workbench._operation_coordinator.delete_beat(selected_index)
        print(
            f"📊 [WORKBENCH] Operation result: success={result.success}, message='{result.message}'"
        )
        self.workbench._handle_operation_result(result)

    def handle_clear(self):
        """Handle clear sequence operation."""
        print("🧹 [WORKBENCH] Clear sequence requested")

        # Clear the sequence via state manager
        result = self.workbench._state_manager.set_sequence(None)

        if result.changed:
            print("🧹 [WORKBENCH] Sequence cleared, updating UI...")
            # Update UI to reflect the cleared sequence
            self.workbench._update_ui_from_state()

            # IMPORTANT: Clear the start position data from state manager
            # so that when a new start position is selected, it will be detected as a change
            print("🧹 [WORKBENCH] Clearing start position data from state manager...")
            self.workbench._state_manager.set_start_position(None)

            # Reset start position to text-only mode (no pictograph)
            if self.workbench._beat_frame_section:
                print("🧹 [WORKBENCH] Initializing cleared start position view...")
                self.workbench._beat_frame_section.initialize_cleared_start_position()

        # Also emit the signal for any parent handlers
        self.workbench.clear_sequence_requested.emit()

        # Reset button panel to picker mode
        if self.workbench._beat_frame_section and hasattr(
            self.workbench._beat_frame_section, "reset_to_picker_mode"
        ):
            self.workbench._beat_frame_section.reset_to_picker_mode()

    def handle_picker_mode_request(self):
        """Handle picker mode request with smart switching."""
        current_sequence = self.workbench._state_manager.get_current_sequence()
        start_position = self.workbench._state_manager.get_start_position()

        # Smart switching logic
        if not current_sequence and not start_position:
            print(
                "⚡ [WORKBENCH] No sequence or start position - switching to start position picker"
            )
        elif start_position and not current_sequence:
            print(
                "⚡ [WORKBENCH] Has start position but no sequence - switching to option picker"
            )
        elif current_sequence:
            print("⚡ [WORKBENCH] Has sequence - staying in option picker")

        # Emit signal to parent to handle layout transition
        self.workbench.picker_mode_requested.emit()

    def handle_graph_editor_request(self):
        """Handle graph editor mode request."""
        print("📊 [WORKBENCH] Graph editor mode requested")
        self.workbench.graph_editor_requested.emit()

    def handle_generate_request(self):
        """Handle generate controls mode request."""
        print("🤖 [WORKBENCH] Generate controls mode requested")
        self.workbench.generate_requested.emit()
