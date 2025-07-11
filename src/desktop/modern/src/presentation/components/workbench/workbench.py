from typing import TYPE_CHECKING, List, Optional

from core.interfaces.core_services import ILayoutService
from core.interfaces.workbench_services import (
    IBeatDeletionService,
    IDictionaryService,
    IFullScreenService,
    IGraphEditorService,
    ISequenceWorkbenchService,
)
from domain.models import BeatData, SequenceData
from domain.models.pictograph_models import PictographData
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget

# Import event system for session restoration
try:
    from core.events.event_bus import EventPriority, get_event_bus

    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    EVENT_SYSTEM_AVAILABLE = False

from .beat_frame_section import WorkbenchBeatFrameSection
from .button_interface import WorkbenchButtonInterfaceAdapter
from .event_controller import WorkbenchEventController
from .indicator_section import WorkbenchIndicatorSection

if TYPE_CHECKING:
    from application.services.workbench.beat_selection_service import (
        BeatSelectionService,
    )


class SequenceWorkbench(QWidget):
    """Modern sequence workbench component following modern architecture patterns"""

    sequence_modified = pyqtSignal(object)
    operation_completed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    edit_construct_toggle_requested = pyqtSignal(bool)

    def __init__(
        self,
        layout_service: ILayoutService,
        beat_selection_service: "BeatSelectionService",
        workbench_service: ISequenceWorkbenchService,
        fullscreen_service: IFullScreenService,
        deletion_service: IBeatDeletionService,
        graph_service: IGraphEditorService,
        dictionary_service: IDictionaryService,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self._layout_service = layout_service
        self._beat_selection_service = beat_selection_service
        self._graph_service = graph_service
        self._dictionary_service = dictionary_service
        self._current_sequence: Optional[SequenceData] = None
        self._start_position_data: Optional[BeatData] = None
        self._indicator_section: Optional[WorkbenchIndicatorSection] = None
        self._beat_frame_section: Optional[WorkbenchBeatFrameSection] = None
        self._event_controller: Optional[WorkbenchEventController] = None
        self._button_interface: Optional[WorkbenchButtonInterfaceAdapter] = None

        # Event bus integration for session restoration
        self.event_bus = get_event_bus() if EVENT_SYSTEM_AVAILABLE else None
        self._subscription_ids: List[str] = []

        self._create_event_controller(
            workbench_service, fullscreen_service, deletion_service, dictionary_service
        )

        # Setup event subscriptions IMMEDIATELY to catch restoration events
        # This must happen before UI setup completes to receive restoration events
        self._setup_event_subscriptions()

        self._setup_ui()
        self._connect_signals()
        self._setup_button_interface()

    def _create_event_controller(
        self,
        workbench_service: ISequenceWorkbenchService,
        fullscreen_service: IFullScreenService,
        deletion_service: IBeatDeletionService,
        dictionary_service: IDictionaryService,
    ):
        """Create centralized event controller"""
        self._event_controller = WorkbenchEventController(
            workbench_service=workbench_service,
            fullscreen_service=fullscreen_service,
            deletion_service=deletion_service,
            dictionary_service=dictionary_service,
        )

    def _setup_ui(self):
        """Setup the UI layout with proper constraints"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)
        self._indicator_section = WorkbenchIndicatorSection(
            dictionary_service=self._dictionary_service, parent=self
        )
        main_layout.addWidget(self._indicator_section, 0)
        self._beat_frame_section = WorkbenchBeatFrameSection(
            layout_service=self._layout_service,
            beat_selection_service=self._beat_selection_service,
            parent=self,
        )
        main_layout.addWidget(self._beat_frame_section, 1)

    def _connect_signals(self):
        """Connect component signals"""
        if self._beat_frame_section:
            self._beat_frame_section.beat_selected.connect(self._on_beat_selected)
            self._beat_frame_section.beat_modified.connect(self._on_beat_modified)
            self._beat_frame_section.sequence_modified.connect(
                self._on_sequence_modified
            )
            self._beat_frame_section.layout_changed.connect(self._on_layout_changed)
            self._beat_frame_section.add_to_dictionary_requested.connect(
                self._handle_add_to_dictionary
            )
            self._beat_frame_section.save_image_requested.connect(
                self._handle_save_image
            )
            self._beat_frame_section.view_fullscreen_requested.connect(
                self._handle_fullscreen
            )
            self._beat_frame_section.mirror_sequence_requested.connect(
                self._handle_reflection
            )
            self._beat_frame_section.swap_colors_requested.connect(
                self._handle_color_swap
            )
            self._beat_frame_section.rotate_sequence_requested.connect(
                self._handle_rotation
            )
            self._beat_frame_section.copy_json_requested.connect(self._handle_copy_json)
            self._beat_frame_section.delete_beat_requested.connect(
                self._handle_delete_beat
            )
            self._beat_frame_section.clear_sequence_requested.connect(
                self._handle_clear
            )
            self._beat_frame_section.edit_construct_toggle_requested.connect(
                self.edit_construct_toggle_requested
            )
        if self._event_controller:
            self._event_controller.sequence_modified.connect(self.sequence_modified)
            self._event_controller.operation_completed.connect(self.operation_completed)
            self._event_controller.error_occurred.connect(self.error_occurred)

    def _setup_button_interface(self):
        """Setup button interface adapter for Sprint 2 integration"""
        self._button_interface = WorkbenchButtonInterfaceAdapter(self)
        self._button_interface.signals.sequence_modified.connect(self.sequence_modified)
        self._button_interface.signals.operation_completed.connect(
            self.operation_completed
        )
        self._button_interface.signals.operation_failed.connect(self.error_occurred)

    def set_sequence(self, sequence: SequenceData):
        """Set the current sequence to display/edit"""
        self._current_sequence = sequence
        self._update_all_components()

        # Only emit sequence_modified if we're not in restoration mode
        # This prevents auto-save loops during sequence restoration
        if not getattr(self, "_restoring_sequence", False):
            # Include start position in the sequence data when emitting
            complete_sequence = self._get_complete_sequence_with_start_position()
            self.sequence_modified.emit(complete_sequence)

    def get_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence"""
        return self._current_sequence

    def set_start_position(
        self,
        start_position_data: BeatData,
        pictograph_data: Optional["PictographData"] = None,
    ):
        """
        Set the start position with optional separate pictograph data.

        Args:
            start_position_data: Beat context data (beat number, duration, metadata)
            pictograph_data: Optional pictograph data for direct rendering.
                           If None, will be reconstructed from beat_data (legacy mode)
        """
        self._start_position_data = start_position_data
        if self._beat_frame_section:
            self._beat_frame_section.set_start_position(
                start_position_data, pictograph_data
            )

        # Emit sequence_modified with updated start position (unless restoring)
        if not getattr(self, "_restoring_sequence", False) and self._current_sequence:
            complete_sequence = self._get_complete_sequence_with_start_position()
            self.sequence_modified.emit(complete_sequence)

    def clear_start_position(self):
        """Clear the start position data (V1 clear behavior)"""
        self._start_position_data = None
        if self._beat_frame_section and hasattr(
            self._beat_frame_section, "_beat_frame"
        ):
            beat_frame = self._beat_frame_section._beat_frame
            if hasattr(beat_frame, "_start_position_view"):
                beat_frame._start_position_view.clear_position_data()

    def get_start_position(self) -> Optional[BeatData]:
        """Get the current start position"""
        return self._start_position_data

    def _get_complete_sequence_with_start_position(self) -> SequenceData:
        """Get the current sequence with start position data included."""
        if not self._current_sequence:
            return self._current_sequence

        # If we have start position data, include it in the sequence
        if self._start_position_data:
            return self._current_sequence.update(
                start_position=self._start_position_data
            )

        return self._current_sequence

    def get_button_interface(self) -> Optional[WorkbenchButtonInterfaceAdapter]:
        """Get the button interface adapter for Sprint 2 integration"""
        return self._button_interface

    def _update_all_components(self):
        """Update all components with current sequence"""
        if self._event_controller:
            self._event_controller.set_sequence(self._current_sequence)
        if self._indicator_section:
            self._indicator_section.update_sequence(self._current_sequence)
        if self._beat_frame_section:
            self._beat_frame_section.set_sequence(self._current_sequence)

    def _handle_add_to_dictionary(self):
        """Handle add to dictionary operation"""
        if not self._event_controller:
            return
        success, message = self._event_controller.handle_add_to_dictionary()
        self._show_operation_result("add_to_dictionary", success, message)

    def _handle_save_image(self):
        """Handle save image operation"""
        if not self._event_controller:
            return
        success, message = self._event_controller.handle_save_image()
        self._show_operation_result("save_image", success, message)

    def _handle_delete_beat(self):
        """Handle delete beat operation"""
        if not self._event_controller or not self._beat_frame_section:
            return
        selected_index = self._beat_frame_section.get_selected_beat_index()
        success, message, updated_sequence = self._event_controller.handle_delete_beat(
            selected_index
        )
        if success and updated_sequence:
            self._current_sequence = updated_sequence
            self._update_all_components()
            self.sequence_modified.emit(updated_sequence)
        self._show_operation_result("delete_beat", success, message)

    def _handle_color_swap(self):
        """Handle color swap operation"""
        if not self._event_controller:
            return
        success, message, updated_sequence = self._event_controller.handle_color_swap()
        if success and updated_sequence:
            self._current_sequence = updated_sequence
            self._update_all_components()
            self.sequence_modified.emit(updated_sequence)
        self._show_operation_result("swap_colors", success, message)

    def _handle_reflection(self):
        """Handle reflection operation"""
        if not self._event_controller:
            return
        success, message, updated_sequence = self._event_controller.handle_reflection()
        if success and updated_sequence:
            self._current_sequence = updated_sequence
            self._update_all_components()
            self.sequence_modified.emit(updated_sequence)
        self._show_operation_result("mirror_sequence", success, message)

    def _handle_rotation(self):
        """Handle rotation operation"""
        if not self._event_controller:
            return
        success, message, updated_sequence = self._event_controller.handle_rotation()
        if success and updated_sequence:
            self._current_sequence = updated_sequence
            self._update_all_components()
            self.sequence_modified.emit(updated_sequence)
        self._show_operation_result("rotate_sequence", success, message)

    def _handle_clear(self):
        """Handle clear sequence operation"""
        if not self._event_controller:
            return
        success, message, updated_sequence = self._event_controller.handle_clear()
        if success and updated_sequence:
            self._current_sequence = updated_sequence
            self.clear_start_position()
            self._update_all_components()
            self._graph_service.toggle_graph_visibility()
            print(
                f"🔄 [WORKBENCH] Emitting sequence_modified signal after clear: seq_length={updated_sequence.length}"
            )
            self.sequence_modified.emit(updated_sequence)
        self._show_operation_result("clear_sequence", success, message)

    def _handle_fullscreen(self):
        """Handle full screen view operation"""
        if not self._event_controller:
            return
        success, message = self._event_controller.handle_fullscreen()
        self._show_operation_result("view_fullscreen", success, message)

    def _handle_copy_json(self):
        """Handle copy JSON operation"""
        if not self._event_controller:
            return
        success, message = self._event_controller.handle_copy_json()
        self._show_operation_result("copy_json", success, message)

    def _show_operation_result(self, button_name: str, success: bool, message: str):
        """Show operation result with appropriate feedback"""
        if success:
            self.operation_completed.emit(message)
            if self._beat_frame_section:
                self._beat_frame_section.show_button_message(button_name, message, 2000)
        else:
            self.error_occurred.emit(message)
            if self._beat_frame_section:
                self._beat_frame_section.show_button_message(
                    button_name, f"❌ {message}", 3000
                )

    def _on_beat_selected(self, beat_index: int):
        """Handle beat selection from beat frame and update graph editor"""
        if self._beat_frame_section:
            self._beat_frame_section.set_button_enabled(
                "delete_beat", beat_index is not None
            )

    def _on_beat_modified(self, beat_index: int, beat_data):
        """Handle beat modification from beat frame"""
        if not self._current_sequence:
            return
        new_beats = list(self._current_sequence.beats)
        if beat_index < len(new_beats):
            new_beats[beat_index] = beat_data
            self._current_sequence = self._current_sequence.update(beats=new_beats)
            self.sequence_modified.emit(self._current_sequence)

    def _on_sequence_modified(self, sequence):
        """Handle sequence modification from beat frame"""
        self._current_sequence = sequence
        self._update_all_components()

    def _on_layout_changed(self, rows: int, columns: int):
        """Handle layout change from beat frame"""
        _ = rows
        _ = columns

    def _on_graph_editor_beat_changed(self, beat_data: BeatData, beat_index: int):
        """Handle beat changes from graph editor and update beat frame"""
        if hasattr(self, "_beat_frame_section") and self._beat_frame_section:
            if hasattr(self._beat_frame_section, "update_beat_at_index"):
                self._beat_frame_section.update_beat_at_index(beat_index, beat_data)
            if hasattr(self._beat_frame_section, "refresh_display"):
                self._beat_frame_section.refresh_display()
            if self._current_sequence and beat_index < len(
                self._current_sequence.beats
            ):
                beats = list(self._current_sequence.beats)
                beats[beat_index] = beat_data
                self._current_sequence = self._current_sequence.update(beats=beats)
                self.sequence_modified.emit(self._current_sequence)

    def resizeEvent(self, event):
        """Handle resize events for responsive design"""
        super().resizeEvent(event)
        # Beat frame section handles its own resize events automatically
        # No manual intervention needed - Qt will call resizeEvent on child widgets

    def _setup_event_subscriptions(self):
        """Setup event subscriptions for session restoration."""
        try:
            if not EVENT_SYSTEM_AVAILABLE:
                print(
                    "⚠️ [WORKBENCH] Event system not available - skipping session restoration subscription"
                )
                return

            if not self.event_bus:
                print(
                    "⚠️ [WORKBENCH] Event bus not available - skipping session restoration subscription"
                )
                return

            print(
                "🔍 [WORKBENCH] Setting up session restoration event subscriptions..."
            )

            # Subscribe to session restoration events
            # UIEvent.event_type returns "ui.{component}.{action}"
            sub_id = self.event_bus.subscribe(
                "ui.session_restoration.sequence_restored",
                self._on_sequence_restored,
                priority=EventPriority.HIGH,
            )

            if sub_id:
                self._subscription_ids.append(sub_id)
                print(
                    f"✅ [WORKBENCH] Subscribed to session restoration events (ID: {sub_id})"
                )
            else:
                print("⚠️ [WORKBENCH] Failed to subscribe to session restoration events")

        except Exception as e:
            print(f"⚠️ [WORKBENCH] Error setting up event subscriptions: {e}")
            # Don't let event subscription errors block workbench creation

    def _on_sequence_restored(self, event):
        """Handle sequence restoration from session."""
        try:
            state_data = event.state_data
            sequence_data = state_data.get("sequence_data")
            start_position_data = state_data.get("start_position_data")

            # Extract start position from sequence data if it exists
            sequence_start_position = None
            if (
                hasattr(sequence_data, "start_position")
                and sequence_data.start_position
            ):
                sequence_start_position = sequence_data.start_position
            elif isinstance(sequence_data, dict) and sequence_data.get(
                "start_position"
            ):
                sequence_start_position = sequence_data["start_position"]

            # Set the sequence using the existing method (this will trigger auto-save)
            # Temporarily disable auto-save during restoration to avoid loops
            self._restoring_sequence = True
            self.set_sequence(sequence_data)
            self._restoring_sequence = False

            # Restore start position from event data or sequence data
            start_pos_to_restore = start_position_data or sequence_start_position
            if start_pos_to_restore:
                # Convert dict to BeatData if needed
                if isinstance(start_pos_to_restore, dict):
                    start_pos_to_restore = BeatData.from_dict(start_pos_to_restore)

                self.set_start_position(start_pos_to_restore)
            else:
                # CRITICAL FIX: Always initialize start position view, even when cleared
                # This ensures the "START" text overlay is visible after restoration
                print(
                    "🔧 [WORKBENCH] No start position data - initializing cleared start position view"
                )
                if self._beat_frame_section:
                    self._beat_frame_section.initialize_cleared_start_position()

        except Exception as e:
            print(f"❌ [WORKBENCH] Failed to restore sequence: {e}")
            import traceback

            traceback.print_exc()

    def cleanup(self):
        """Clean up event subscriptions when component is destroyed."""
        if self.event_bus:
            for sub_id in self._subscription_ids:
                self.event_bus.unsubscribe(sub_id)
            self._subscription_ids.clear()
            print("🧹 [WORKBENCH] Event subscriptions cleaned up")
