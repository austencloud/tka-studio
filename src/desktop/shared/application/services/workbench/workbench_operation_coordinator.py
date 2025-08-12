"""
Workbench Operation Coordinator - Framework-Agnostic Business Logic

Coordinates workbench operations across multiple services without Qt dependencies.
Handles operation execution, result coordination, and error management.

Following established patterns:
- Framework-agnostic (no Qt dependencies)
- Single responsibility (operation coordination only)
- Delegates to existing services
- Returns structured results
"""

import logging
from enum import Enum
from typing import NamedTuple, Optional

from desktop.modern.domain.models.sequence_data import SequenceData

logger = logging.getLogger(__name__)


class OperationType(Enum):
    """Types of workbench operations."""

    ADD_TO_DICTIONARY = "add_to_dictionary"
    SAVE_IMAGE = "save_image"
    VIEW_FULLSCREEN = "view_fullscreen"
    MIRROR_SEQUENCE = "mirror_sequence"
    SWAP_COLORS = "swap_colors"
    ROTATE_SEQUENCE = "rotate_sequence"
    COPY_JSON = "copy_json"
    DELETE_BEAT = "delete_beat"
    CLEAR_SEQUENCE = "clear_sequence"


class OperationResult(NamedTuple):
    """Result of a workbench operation."""

    success: bool
    operation_type: OperationType
    message: str
    updated_sequence: SequenceData | None = None
    error_details: str | None = None

    @classmethod
    def success_result(
        cls,
        operation_type: OperationType,
        message: str,
        updated_sequence: SequenceData | None = None,
    ):
        """Create a successful operation result."""
        return cls(True, operation_type, message, updated_sequence, None)

    @classmethod
    def failure_result(
        cls,
        operation_type: OperationType,
        message: str,
        error_details: str | None = None,
    ):
        """Create a failed operation result."""
        return cls(False, operation_type, message, None, error_details)


class WorkbenchOperationCoordinator:
    """
    Framework-agnostic coordinator for workbench operations.

    Responsibilities:
    - Coordinate operations across multiple services
    - Validate operation preconditions
    - Handle operation execution and error management
    - Return structured results for presentation layer
    - Delegate to appropriate business services
    """

    def __init__(
        self,
        workbench_state_manager=None,
        beat_operations=None,
        dictionary_service=None,
        fullscreen_service=None,
        sequence_transformer=None,
        sequence_persister=None,
        export_service=None,
    ):
        """
        Initialize operation coordinator with injected dependencies.

        Args:
            workbench_state_manager: WorkbenchStateManager for state access
            beat_operations: SequenceBeatOperations for beat manipulation
            dictionary_service: SequenceDictionaryService for dictionary operations
            fullscreen_service: IFullScreenViewer for fullscreen operations
            sequence_transformer: SequenceTransformer for transform operations
            sequence_persister: SequencePersister for persistence operations
            export_service: WorkbenchExportService for export operations
        """
        self._state_manager = workbench_state_manager
        self._beat_operations = beat_operations
        self._dictionary_service = dictionary_service
        self._fullscreen_service = fullscreen_service
        self._sequence_transformer = sequence_transformer
        self._sequence_persister = sequence_persister
        self._export_service = export_service

        logger.debug("WorkbenchOperationCoordinator initialized")

    # Dictionary Operations
    def add_to_dictionary(self) -> OperationResult:
        """
        Add current sequence to dictionary.

        Returns:
            OperationResult with operation details
        """
        try:
            # Check preconditions
            if not self._state_manager or not self._state_manager.has_sequence():
                return OperationResult.failure_result(
                    OperationType.ADD_TO_DICTIONARY, "No sequence to add to dictionary"
                )

            if not self._dictionary_service:
                return OperationResult.failure_result(
                    OperationType.ADD_TO_DICTIONARY, "Dictionary service not available"
                )

            sequence = self._state_manager.get_current_sequence()

            # Execute operation
            result = self._dictionary_service.add_sequence_to_dictionary(sequence, "")

            if result:
                return OperationResult.success_result(
                    OperationType.ADD_TO_DICTIONARY, "Added to dictionary!"
                )
            else:
                return OperationResult.failure_result(
                    OperationType.ADD_TO_DICTIONARY, "Sequence already in dictionary"
                )

        except Exception as e:
            logger.error(f"Failed to add to dictionary: {e}")
            return OperationResult.failure_result(
                OperationType.ADD_TO_DICTIONARY, "Failed to add to dictionary", str(e)
            )

    # Export Operations
    def save_image(self) -> OperationResult:
        """
        Save current sequence as image using export service.

        Returns:
            OperationResult with operation details
        """
        try:
            # Check preconditions
            logger.debug(f"Save image: state_manager={self._state_manager}")
            if not self._state_manager:
                logger.error("Save image failed: No state manager")
                return OperationResult.failure_result(
                    OperationType.SAVE_IMAGE, "No state manager available"
                )

            has_sequence = self._state_manager.has_sequence()
            logger.debug(f"Save image: has_sequence={has_sequence}")
            if not has_sequence:
                logger.error("Save image failed: No sequence to export")
                return OperationResult.failure_result(
                    OperationType.SAVE_IMAGE, "No sequence to export"
                )

            logger.debug(f"Save image: export_service={self._export_service}")
            if not self._export_service:
                logger.error("Save image failed: Export service not available")
                return OperationResult.failure_result(
                    OperationType.SAVE_IMAGE, "Export service not available"
                )

            sequence = self._state_manager.get_current_sequence()
            logger.debug(
                f"Save image: sequence={sequence}, length={sequence.length if sequence else 'None'}"
            )

            # Use export service to save image
            logger.debug("Save image: Calling export service...")
            success, result_message = self._export_service.export_sequence_image(
                sequence
            )
            logger.debug(
                f"Save image: Export result: success={success}, message='{result_message}'"
            )

            if success:
                # result_message contains the file path
                return OperationResult.success_result(
                    OperationType.SAVE_IMAGE,
                    f"Image saved successfully to: {result_message}",
                )
            else:
                return OperationResult.failure_result(
                    OperationType.SAVE_IMAGE, f"Image export failed: {result_message}"
                )

        except Exception as e:
            logger.error(f"Failed to save image: {e}")
            return OperationResult.failure_result(
                OperationType.SAVE_IMAGE, "Image export failed", str(e)
            )

    def copy_json(self, sequence: Optional["SequenceData"] = None) -> OperationResult:
        """
        Copy sequence JSON to clipboard.

        Returns:
            OperationResult with operation details
        """
        try:
            # Use passed sequence or get from state manager
            if sequence is None:
                # Check preconditions
                if not self._state_manager or not self._state_manager.has_sequence():
                    return OperationResult.failure_result(
                        OperationType.COPY_JSON, "No sequence to copy"
                    )
                sequence = self._state_manager.get_current_sequence()

            # Final check that we have a sequence
            if not sequence:
                return OperationResult.failure_result(
                    OperationType.COPY_JSON, "No sequence to copy"
                )

            # Check if export service is available
            if not self._export_service:
                return OperationResult.failure_result(
                    OperationType.COPY_JSON, "Export service not available"
                )

            # Export sequence to JSON
            success, json_data = self._export_service.export_sequence_json(sequence)

            if not success:
                return OperationResult.failure_result(
                    OperationType.COPY_JSON, f"JSON export failed: {json_data}"
                )

            # Copy to clipboard using Qt clipboard
            try:
                from PyQt6.QtWidgets import QApplication

                clipboard = QApplication.clipboard()
                clipboard.setText(json_data)

                logger.info(
                    f"Sequence JSON copied to clipboard: {len(json_data)} characters"
                )
                return OperationResult.success_result(
                    OperationType.COPY_JSON,
                    f"JSON copied to clipboard! ({len(json_data)} characters)",
                )

            except Exception as clipboard_error:
                logger.error(f"Failed to copy to clipboard: {clipboard_error}")
                return OperationResult.failure_result(
                    OperationType.COPY_JSON,
                    f"Clipboard operation failed: {clipboard_error}",
                )

        except Exception as e:
            logger.error(f"Failed to copy JSON: {e}")
            return OperationResult.failure_result(
                OperationType.COPY_JSON, "JSON export failed", str(e)
            )

    # View Operations
    def view_fullscreen(self) -> OperationResult:
        """
        View current sequence in fullscreen.

        Returns:
            OperationResult with operation details
        """
        try:
            # Check preconditions
            if not self._state_manager or not self._state_manager.has_sequence():
                return OperationResult.failure_result(
                    OperationType.VIEW_FULLSCREEN, "No sequence to view"
                )

            if not self._fullscreen_service:
                return OperationResult.failure_result(
                    OperationType.VIEW_FULLSCREEN, "Fullscreen service not available"
                )

            sequence = self._state_manager.get_current_sequence()

            # Execute operation
            self._fullscreen_service.show_full_screen_view(sequence)

            return OperationResult.success_result(
                OperationType.VIEW_FULLSCREEN, "Opening full screen view..."
            )

        except Exception as e:
            logger.error(f"Failed to show fullscreen: {e}")
            return OperationResult.failure_result(
                OperationType.VIEW_FULLSCREEN, "Full screen view failed", str(e)
            )

    # Transform Operations
    def mirror_sequence(self) -> OperationResult:
        """
        Mirror/reflect current sequence.

        Returns:
            OperationResult with operation details and updated sequence
        """
        try:
            # Check preconditions
            if not self._state_manager or not self._state_manager.has_sequence():
                return OperationResult.failure_result(
                    OperationType.MIRROR_SEQUENCE, "No sequence to mirror"
                )

            if not self._sequence_transformer:
                return OperationResult.failure_result(
                    OperationType.MIRROR_SEQUENCE, "Sequence transformer not available"
                )

            sequence = self._state_manager.get_current_sequence()

            # Execute operation
            mirrored_sequence = self._sequence_transformer.reflect_sequence(sequence)

            return OperationResult.success_result(
                OperationType.MIRROR_SEQUENCE, "Sequence mirrored!", mirrored_sequence
            )

        except Exception as e:
            logger.error(f"Failed to mirror sequence: {e}")
            return OperationResult.failure_result(
                OperationType.MIRROR_SEQUENCE, "Mirror operation failed", str(e)
            )

    def swap_colors(self) -> OperationResult:
        """
        Swap colors in current sequence.

        Returns:
            OperationResult with operation details and updated sequence
        """
        try:
            # Check preconditions
            if not self._state_manager or not self._state_manager.has_sequence():
                return OperationResult.failure_result(
                    OperationType.SWAP_COLORS, "No sequence to swap colors"
                )

            if not self._sequence_transformer:
                return OperationResult.failure_result(
                    OperationType.SWAP_COLORS, "Sequence transformer not available"
                )

            sequence = self._state_manager.get_current_sequence()

            # Execute operation
            swapped_sequence = self._sequence_transformer.swap_colors(sequence)

            return OperationResult.success_result(
                OperationType.SWAP_COLORS, "Colors swapped!", swapped_sequence
            )

        except Exception as e:
            logger.error(f"Failed to swap colors: {e}")
            return OperationResult.failure_result(
                OperationType.SWAP_COLORS, "Color swap failed", str(e)
            )

    def rotate_sequence(self) -> OperationResult:
        """
        Rotate current sequence.

        Returns:
            OperationResult with operation details and updated sequence
        """
        try:
            # Check preconditions
            if not self._state_manager or not self._state_manager.has_sequence():
                return OperationResult.failure_result(
                    OperationType.ROTATE_SEQUENCE, "No sequence to rotate"
                )

            if not self._sequence_transformer:
                return OperationResult.failure_result(
                    OperationType.ROTATE_SEQUENCE, "Sequence transformer not available"
                )

            sequence = self._state_manager.get_current_sequence()

            # Execute operation
            rotated_sequence = self._sequence_transformer.rotate_sequence(sequence)

            return OperationResult.success_result(
                OperationType.ROTATE_SEQUENCE, "Sequence rotated!", rotated_sequence
            )

        except Exception as e:
            logger.error(f"Failed to rotate sequence: {e}")
            return OperationResult.failure_result(
                OperationType.ROTATE_SEQUENCE, "Rotation failed", str(e)
            )

    # Beat Operations
    def delete_beat(self, beat_index: int | None) -> OperationResult:
        """
        Delete beat at specified index (legacy behavior: delete beat and all following).

        Args:
            beat_index: Index of beat to delete, or -1 for start position (delete all beats)

        Returns:
            OperationResult with operation details and updated sequence
        """
        print(
            f"🗑️ [OPERATION_COORDINATOR] delete_beat called with beat_index={beat_index}"
        )

        try:
            # Check preconditions
            print(f"🔍 [OPERATION_COORDINATOR] State manager: {self._state_manager}")
            print(
                f"🔍 [OPERATION_COORDINATOR] State manager ID: {id(self._state_manager)}"
            )
            if self._state_manager:
                has_sequence = self._state_manager.has_sequence()
                print(f"🔍 [OPERATION_COORDINATOR] Has sequence: {has_sequence}")
                if has_sequence:
                    current_seq = self._state_manager.get_current_sequence()
                    print(f"🔍 [OPERATION_COORDINATOR] Current sequence: {current_seq}")
                    if current_seq:
                        print(
                            f"🔍 [OPERATION_COORDINATOR] Sequence beats: {len(current_seq.beats)}"
                        )

            if not self._state_manager or not self._state_manager.has_sequence():
                print("❌ [OPERATION_COORDINATOR] No state manager or sequence")
                return OperationResult.failure_result(
                    OperationType.DELETE_BEAT, "No beats to delete"
                )

            if beat_index is None:
                print("❌ [OPERATION_COORDINATOR] No beat selected")
                return OperationResult.failure_result(
                    OperationType.DELETE_BEAT, "No beat selected"
                )

            if not self._beat_operations:
                print("❌ [OPERATION_COORDINATOR] No beat operations service")
                return OperationResult.failure_result(
                    OperationType.DELETE_BEAT, "Beat operations service not available"
                )

            sequence = self._state_manager.get_current_sequence()
            print(
                f"📊 [OPERATION_COORDINATOR] Current sequence has {len(sequence.beats)} beats"
            )

            # Handle start position deletion (delete all beats)
            if beat_index == -1:
                print(
                    "🗑️ [OPERATION_COORDINATOR] Start position deletion - deleting all beats"
                )
                # Start position selected - delete all beats (legacy behavior)
                updated_sequence = sequence.update(beats=[])
                print(
                    f"✅ [OPERATION_COORDINATOR] All beats deleted, sequence now has {len(updated_sequence.beats)} beats"
                )
                return OperationResult.success_result(
                    OperationType.DELETE_BEAT, "All beats deleted!", updated_sequence
                )

            # Execute normal beat deletion (delete beat and following)
            print(
                f"🗑️ [OPERATION_COORDINATOR] Deleting beat at index {beat_index} and following"
            )
            updated_sequence = self._beat_operations.delete_beat(sequence, beat_index)
            print(
                f"✅ [OPERATION_COORDINATOR] Beat deletion complete, sequence now has {len(updated_sequence.beats)} beats"
            )

            return OperationResult.success_result(
                OperationType.DELETE_BEAT, "Beat deleted!", updated_sequence
            )

        except Exception as e:
            logger.error(f"Failed to delete beat: {e}")
            return OperationResult.failure_result(
                OperationType.DELETE_BEAT, "Delete failed", str(e)
            )

    # Sequence Management Operations
    def clear_sequence(self) -> OperationResult:
        """
        Clear current sequence and start position.

        Returns:
            OperationResult with operation details
        """
        try:
            print("🧹 [OPERATION_COORDINATOR] Starting clear sequence operation...")

            # CRITICAL FIX: Use state manager's set_sequence(None) instead of clear_all_state()
            # This ensures proper UI update notifications are sent
            if self._state_manager:
                print(
                    "🧹 [OPERATION_COORDINATOR] Setting sequence to None via state manager..."
                )
                sequence_result = self._state_manager.set_sequence(None)
                print(
                    f"🧹 [OPERATION_COORDINATOR] Sequence clear result: {sequence_result}"
                )

                print(
                    "🧹 [OPERATION_COORDINATOR] Setting start position to None via state manager..."
                )
                start_pos_result = self._state_manager.set_start_position(None)
                print(
                    f"🧹 [OPERATION_COORDINATOR] Start position clear result: {start_pos_result}"
                )

                # Verify the state is actually cleared
                current_sequence = self._state_manager.get_current_sequence()
                print(
                    f"🧹 [OPERATION_COORDINATOR] Current sequence after clear: {current_sequence}"
                )
            else:
                print("❌ [OPERATION_COORDINATOR] No state manager available!")
                return OperationResult.failure_result(
                    OperationType.CLEAR_SEQUENCE,
                    "Clear failed",
                    "No state manager available",
                )

            # Execute persistence clearing if available
            if self._sequence_persister:
                print("🧹 [OPERATION_COORDINATOR] Clearing sequence persistence...")
                self._sequence_persister.clear_current_sequence()
            else:
                print(
                    "⚠️ [OPERATION_COORDINATOR] No sequence persister available - skipping persistence clear"
                )

            print(
                "✅ [OPERATION_COORDINATOR] Clear sequence operation completed successfully"
            )
            return OperationResult.success_result(
                OperationType.CLEAR_SEQUENCE, "Sequence cleared!"
            )

        except Exception as e:
            print(f"❌ [OPERATION_COORDINATOR] Failed to clear sequence: {e}")
            logger.error(f"Failed to clear sequence: {e}")
            return OperationResult.failure_result(
                OperationType.CLEAR_SEQUENCE, "Clear failed", str(e)
            )

    # Operation Validation
    def can_execute_operation(self, operation_type: OperationType) -> tuple[bool, str]:
        """
        Check if operation can be executed.

        Args:
            operation_type: Type of operation to check

        Returns:
            Tuple of (can_execute, reason_if_not)
        """
        if not self._state_manager:
            return False, "State manager not available"

        # Operations that require a sequence
        sequence_required_ops = {
            OperationType.ADD_TO_DICTIONARY,
            OperationType.SAVE_IMAGE,
            OperationType.VIEW_FULLSCREEN,
            OperationType.MIRROR_SEQUENCE,
            OperationType.SWAP_COLORS,
            OperationType.ROTATE_SEQUENCE,
            OperationType.COPY_JSON,
            OperationType.DELETE_BEAT,
        }

        if operation_type in sequence_required_ops:
            if not self._state_manager.has_sequence():
                return False, "No sequence loaded"

        # Clear operation can always be executed
        if operation_type == OperationType.CLEAR_SEQUENCE:
            return True, ""

        # Check service availability
        service_requirements = {
            OperationType.ADD_TO_DICTIONARY: self._dictionary_service,
            OperationType.VIEW_FULLSCREEN: self._fullscreen_service,
            OperationType.MIRROR_SEQUENCE: self._sequence_transformer,
            OperationType.SWAP_COLORS: self._sequence_transformer,
            OperationType.ROTATE_SEQUENCE: self._sequence_transformer,
            OperationType.DELETE_BEAT: self._beat_operations,
        }

        required_service = service_requirements.get(operation_type)
        if required_service is None:
            return False, f"Required service for {operation_type.value} not available"

        return True, ""

    # Diagnostics
    def get_operation_status_summary(self) -> dict:
        """Get summary of operation availability for debugging."""
        operations_status = {}

        for op_type in OperationType:
            can_execute, reason = self.can_execute_operation(op_type)
            operations_status[op_type.value] = {
                "can_execute": can_execute,
                "reason": reason if not can_execute else "Available",
            }

        return {
            "state_manager_available": self._state_manager is not None,
            "has_sequence": (
                self._state_manager.has_sequence() if self._state_manager else False
            ),
            "operations": operations_status,
        }
