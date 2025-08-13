"""
Enhanced Workbench Operation Coordinator - Framework-Agnostic Business Logic

Coordinates workbench operations across multiple services without Qt dependencies.
Handles operation execution, result coordination, and error management.

ENHANCEMENTS:
- Added export service integration for image and JSON exports
- Added clipboard service integration for copy operations
- Enhanced error handling and result reporting
- Improved operation validation and precondition checking
- Added comprehensive diagnostics and status reporting

Following established patterns:
- Framework-agnostic (no Qt dependencies)
- Single responsibility (operation coordination only)
- Delegates to existing services
- Returns structured results
"""

import logging
from enum import Enum
from typing import NamedTuple

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
    additional_data: dict | None = None

    @classmethod
    def success_result(
        cls,
        operation_type: OperationType,
        message: str,
        updated_sequence: SequenceData | None = None,
        additional_data: dict | None = None,
    ):
        """Create a successful operation result."""
        return cls(
            True, operation_type, message, updated_sequence, None, additional_data
        )

    @classmethod
    def failure_result(
        cls,
        operation_type: OperationType,
        message: str,
        error_details: str | None = None,
        additional_data: dict | None = None,
    ):
        """Create a failed operation result."""
        return cls(False, operation_type, message, None, error_details, additional_data)


class EnhancedWorkbenchOperationCoordinator:
    """
    Enhanced framework-agnostic coordinator for workbench operations.

    NEW CAPABILITIES:
    - Export service integration for image and JSON exports
    - Clipboard service integration for copy operations
    - Enhanced error handling and diagnostics
    - Improved operation validation

    RESPONSIBILITIES:
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
        export_service=None,  # NEW: Export service
        clipboard_service=None,  # NEW: Clipboard service
    ):
        """
        Initialize enhanced operation coordinator with injected dependencies.

        Args:
            workbench_state_manager: WorkbenchStateManager for state access
            beat_operations: SequenceBeatOperations for beat manipulation
            dictionary_service: SequenceDictionaryService for dictionary operations
            fullscreen_service: IFullScreenViewer for fullscreen operations
            sequence_transformer: SequenceTransformer for transform operations
            sequence_persister: SequencePersister for persistence operations
            export_service: WorkbenchExportService for export operations (NEW)
            clipboard_service: WorkbenchClipboardService for clipboard operations (NEW)
        """
        # Existing services
        self._state_manager = workbench_state_manager
        self._beat_operations = beat_operations
        self._dictionary_service = dictionary_service
        self._fullscreen_service = fullscreen_service
        self._sequence_transformer = sequence_transformer
        self._sequence_persister = sequence_persister

        # NEW: Enhanced services
        self._export_service = export_service
        self._clipboard_service = clipboard_service

        logger.debug(
            "EnhancedWorkbenchOperationCoordinator initialized with new export and clipboard services"
        )

    # Dictionary Operations (unchanged)
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

    # ENHANCED: Export Operations
    def save_image(self) -> OperationResult:
        """
        Save current sequence as image using export service.

        Returns:
            OperationResult with operation details and file path
        """
        try:
            # Check preconditions
            if not self._state_manager or not self._state_manager.has_sequence():
                return OperationResult.failure_result(
                    OperationType.SAVE_IMAGE, "No sequence to export"
                )

            if not self._export_service:
                return OperationResult.failure_result(
                    OperationType.SAVE_IMAGE, "Export service not available"
                )

            sequence = self._state_manager.get_current_sequence()

            # Execute export operation
            success, result_message = self._export_service.export_sequence_image(
                sequence
            )

            if success:
                # result_message contains the file path
                additional_data = {"file_path": result_message, "export_type": "image"}
                return OperationResult.success_result(
                    OperationType.SAVE_IMAGE,
                    "Image saved successfully!",
                    additional_data=additional_data,
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

    def copy_json(self) -> OperationResult:
        """
        Copy sequence JSON to clipboard using export and clipboard services.

        Returns:
            OperationResult with operation details
        """
        try:
            # Check preconditions
            if not self._state_manager or not self._state_manager.has_sequence():
                return OperationResult.failure_result(
                    OperationType.COPY_JSON, "No sequence to copy"
                )

            if not self._export_service:
                return OperationResult.failure_result(
                    OperationType.COPY_JSON, "Export service not available"
                )

            if not self._clipboard_service:
                return OperationResult.failure_result(
                    OperationType.COPY_JSON, "Clipboard service not available"
                )

            sequence = self._state_manager.get_current_sequence()

            # Step 1: Export sequence as JSON
            json_success, json_result = self._export_service.export_sequence_json(
                sequence
            )

            if not json_success:
                return OperationResult.failure_result(
                    OperationType.COPY_JSON, f"JSON export failed: {json_result}"
                )

            # Step 2: Copy JSON to clipboard
            clipboard_success, clipboard_message = (
                self._clipboard_service.copy_text_to_clipboard(json_result)
            )

            if clipboard_success:
                additional_data = {
                    "json_length": len(json_result),
                    "sequence_length": sequence.length,
                }
                return OperationResult.success_result(
                    OperationType.COPY_JSON,
                    "JSON copied to clipboard!",
                    additional_data=additional_data,
                )
            else:
                return OperationResult.failure_result(
                    OperationType.COPY_JSON,
                    f"Clipboard operation failed: {clipboard_message}",
                )

        except Exception as e:
            logger.error(f"Failed to copy JSON: {e}")
            return OperationResult.failure_result(
                OperationType.COPY_JSON, "JSON copy failed", str(e)
            )

    # View Operations (unchanged)
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

    # Transform Operations (unchanged but with enhanced error reporting)
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

            additional_data = {
                "original_length": sequence.length,
                "mirrored_length": mirrored_sequence.length,
            }

            return OperationResult.success_result(
                OperationType.MIRROR_SEQUENCE,
                "Sequence mirrored!",
                mirrored_sequence,
                additional_data,
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

            additional_data = {
                "original_length": sequence.length,
                "swapped_length": swapped_sequence.length,
            }

            return OperationResult.success_result(
                OperationType.SWAP_COLORS,
                "Colors swapped!",
                swapped_sequence,
                additional_data,
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

            additional_data = {
                "original_length": sequence.length,
                "rotated_length": rotated_sequence.length,
            }

            return OperationResult.success_result(
                OperationType.ROTATE_SEQUENCE,
                "Sequence rotated!",
                rotated_sequence,
                additional_data,
            )

        except Exception as e:
            logger.error(f"Failed to rotate sequence: {e}")
            return OperationResult.failure_result(
                OperationType.ROTATE_SEQUENCE, "Rotation failed", str(e)
            )

    # Beat Operations (unchanged but with enhanced logging)
    def delete_beat(self, beat_index: int | None) -> OperationResult:
        """
        Delete beat at specified index.

        Args:
            beat_index: Index of beat to delete, or -1 for start position (delete all beats)

        Returns:
            OperationResult with operation details and updated sequence
        """
        print(
            f"🗑️ [ENHANCED_COORDINATOR] delete_beat called with beat_index={beat_index}"
        )

        try:
            # Check preconditions
            if not self._state_manager or not self._state_manager.has_sequence():
                print("❌ [ENHANCED_COORDINATOR] No state manager or sequence")
                return OperationResult.failure_result(
                    OperationType.DELETE_BEAT, "No beats to delete"
                )

            if beat_index is None:
                print("❌ [ENHANCED_COORDINATOR] No beat selected")
                return OperationResult.failure_result(
                    OperationType.DELETE_BEAT, "No beat selected"
                )

            if not self._beat_operations:
                print("❌ [ENHANCED_COORDINATOR] No beat operations service")
                return OperationResult.failure_result(
                    OperationType.DELETE_BEAT, "Beat operations service not available"
                )

            sequence = self._state_manager.get_current_sequence()
            original_length = sequence.length
            print(
                f"📊 [ENHANCED_COORDINATOR] Current sequence has {original_length} beats"
            )

            # Handle start position deletion (delete all beats)
            if beat_index == -1:
                print(
                    "🗑️ [ENHANCED_COORDINATOR] Start position deletion - deleting all beats"
                )
                updated_sequence = sequence.update(beats=[])
                additional_data = {
                    "deletion_type": "all_beats",
                    "original_length": original_length,
                    "new_length": 0,
                }
                print("✅ [ENHANCED_COORDINATOR] All beats deleted")
                return OperationResult.success_result(
                    OperationType.DELETE_BEAT,
                    "All beats deleted!",
                    updated_sequence,
                    additional_data,
                )

            # Execute normal beat deletion
            print(f"🗑️ [ENHANCED_COORDINATOR] Deleting beat at index {beat_index}")
            updated_sequence = self._beat_operations.delete_beat(sequence, beat_index)
            new_length = updated_sequence.length

            additional_data = {
                "deletion_type": "single_beat",
                "deleted_index": beat_index,
                "original_length": original_length,
                "new_length": new_length,
            }

            print(
                f"✅ [ENHANCED_COORDINATOR] Beat deletion complete, sequence now has {new_length} beats"
            )

            return OperationResult.success_result(
                OperationType.DELETE_BEAT,
                "Beat deleted!",
                updated_sequence,
                additional_data,
            )

        except Exception as e:
            logger.error(f"Failed to delete beat: {e}")
            return OperationResult.failure_result(
                OperationType.DELETE_BEAT, "Delete failed", str(e)
            )

    # Sequence Management Operations (unchanged)
    def clear_sequence(self) -> OperationResult:
        """
        Clear current sequence and start position.

        Returns:
            OperationResult with operation details
        """
        try:
            # Execute operation
            if self._sequence_persister:
                self._sequence_persister.clear_current_sequence()

            if self._state_manager:
                self._state_manager.clear_all_state()

            return OperationResult.success_result(
                OperationType.CLEAR_SEQUENCE, "Sequence cleared!"
            )

        except Exception as e:
            logger.error(f"Failed to clear sequence: {e}")
            return OperationResult.failure_result(
                OperationType.CLEAR_SEQUENCE, "Clear failed", str(e)
            )

    # ENHANCED: Operation Validation
    def can_execute_operation(self, operation_type: OperationType) -> tuple[bool, str]:
        """
        Check if operation can be executed with enhanced validation.

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

        # ENHANCED: Check service availability with detailed validation
        service_requirements = {
            OperationType.ADD_TO_DICTIONARY: (
                self._dictionary_service,
                "Dictionary service",
            ),
            OperationType.VIEW_FULLSCREEN: (
                self._fullscreen_service,
                "Fullscreen service",
            ),
            OperationType.MIRROR_SEQUENCE: (
                self._sequence_transformer,
                "Sequence transformer",
            ),
            OperationType.SWAP_COLORS: (
                self._sequence_transformer,
                "Sequence transformer",
            ),
            OperationType.ROTATE_SEQUENCE: (
                self._sequence_transformer,
                "Sequence transformer",
            ),
            OperationType.DELETE_BEAT: (
                self._beat_operations,
                "Beat operations service",
            ),
            OperationType.SAVE_IMAGE: (self._export_service, "Export service"),
            OperationType.COPY_JSON: (
                self._export_service,
                "Export service (for JSON)",
            ),
        }

        # Special validation for COPY_JSON (requires both export and clipboard)
        if operation_type == OperationType.COPY_JSON:
            if not self._export_service:
                return False, "Export service not available for JSON generation"
            if not self._clipboard_service:
                return False, "Clipboard service not available for copying"
            if not self._clipboard_service.is_clipboard_available():
                return False, "System clipboard not available"

        requirement = service_requirements.get(operation_type)
        if requirement:
            service, service_name = requirement
            if service is None:
                return False, f"{service_name} not available"

        return True, ""

    # ENHANCED: Diagnostics and Status Reporting
    def get_operation_status_summary(self) -> dict:
        """Get comprehensive summary of operation availability for debugging."""
        operations_status = {}

        for op_type in OperationType:
            can_execute, reason = self.can_execute_operation(op_type)
            operations_status[op_type.value] = {
                "can_execute": can_execute,
                "reason": reason if not can_execute else "Available",
            }

        # Enhanced service status
        service_status = {
            "state_manager": self._state_manager is not None,
            "beat_operations": self._beat_operations is not None,
            "dictionary_service": self._dictionary_service is not None,
            "fullscreen_service": self._fullscreen_service is not None,
            "sequence_transformer": self._sequence_transformer is not None,
            "sequence_persister": self._sequence_persister is not None,
            "export_service": self._export_service is not None,  # NEW
            "clipboard_service": self._clipboard_service is not None,  # NEW
        }

        # Enhanced state information
        state_info = {
            "has_sequence": (
                self._state_manager.has_sequence() if self._state_manager else False
            ),
            "sequence_length": (
                self._state_manager.get_current_sequence().length
                if self._state_manager and self._state_manager.has_sequence()
                else 0
            ),
        }

        # NEW: Enhanced service diagnostics
        enhanced_diagnostics = {}

        if self._export_service:
            enhanced_diagnostics["export_service"] = {
                "directory_valid": self._export_service.validate_export_directory(),
                "export_stats": self._export_service.get_export_stats(),
            }

        if self._clipboard_service:
            enhanced_diagnostics["clipboard_service"] = (
                self._clipboard_service.get_clipboard_stats()
            )

        return {
            "services": service_status,
            "state": state_info,
            "operations": operations_status,
            "diagnostics": enhanced_diagnostics,  # NEW
        }

    def get_service_health_report(self) -> dict:
        """NEW: Get detailed health report of all services."""
        try:
            health_report = {
                "timestamp": logger.handlers[0].baseFilename
                if logger.handlers
                else "unknown",
                "overall_health": "healthy",
                "critical_services": [],
                "warnings": [],
                "service_details": {},
            }

            # Check critical services
            critical_services = [
                ("state_manager", self._state_manager),
                ("beat_operations", self._beat_operations),
            ]

            for service_name, service in critical_services:
                if service is None:
                    health_report["critical_services"].append(service_name)
                    health_report["overall_health"] = "degraded"

            # Check optional services
            optional_services = [
                ("dictionary_service", self._dictionary_service),
                ("fullscreen_service", self._fullscreen_service),
                ("sequence_transformer", self._sequence_transformer),
                ("sequence_persister", self._sequence_persister),
                ("export_service", self._export_service),
                ("clipboard_service", self._clipboard_service),
            ]

            for service_name, service in optional_services:
                if service is None:
                    health_report["warnings"].append(f"{service_name} not available")

            # Detailed service information
            if self._export_service:
                health_report["service_details"]["export_service"] = {
                    "available": True,
                    "directory_valid": self._export_service.validate_export_directory(),
                    "directory": self._export_service.get_export_directory(),
                }

            if self._clipboard_service:
                health_report["service_details"]["clipboard_service"] = {
                    "available": True,
                    "clipboard_available": self._clipboard_service.is_clipboard_available(),
                }

            if health_report["critical_services"]:
                health_report["overall_health"] = "critical"

            return health_report

        except Exception as e:
            return {
                "timestamp": "unknown",
                "overall_health": "error",
                "error": str(e),
                "critical_services": ["health_check_failed"],
                "warnings": [],
                "service_details": {},
            }
