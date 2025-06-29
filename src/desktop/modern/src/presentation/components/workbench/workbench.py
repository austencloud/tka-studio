from typing import TYPE_CHECKING, Optional

from core.interfaces.core_services import ILayoutService
from core.interfaces.workbench_services import (
    IBeatDeletionService,
    IDictionaryService,
    IFullScreenService,
    IGraphEditorService,
    ISequenceWorkbenchService,
)
from domain.models.core_models import BeatData, SequenceData
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from .beat_frame_section import WorkbenchBeatFrameSection
from .button_interface import WorkbenchButtonInterfaceAdapter
from .event_controller import WorkbenchEventController

from .indicator_section import WorkbenchIndicatorSection

if TYPE_CHECKING:
    pass


class SequenceWorkbench(QWidget):
    """Modern sequence workbench component following modern architecture patterns"""

    # Signals for communication with other components
    sequence_modified = pyqtSignal(object)  # SequenceData object
    operation_completed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    edit_construct_toggle_requested = pyqtSignal(
        bool
    )  # True for Edit mode, False for Construct mode

    def __init__(
        self,
        layout_service: ILayoutService,
        workbench_service: ISequenceWorkbenchService,
        fullscreen_service: IFullScreenService,
        deletion_service: IBeatDeletionService,
        graph_service: IGraphEditorService,
        dictionary_service: IDictionaryService,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        # Store injected dependencies
        self._layout_service = layout_service
        self._graph_service = graph_service
        self._dictionary_service = dictionary_service

        # Current state
        self._current_sequence: Optional[SequenceData] = None
        self._start_position_data: Optional[BeatData] = None

        # Components
        self._indicator_section: Optional[WorkbenchIndicatorSection] = None
        self._beat_frame_section: Optional[WorkbenchBeatFrameSection] = None

        self._event_controller: Optional[WorkbenchEventController] = None
        self._button_interface: Optional[WorkbenchButtonInterfaceAdapter] = None

        # Initialize components and setup
        self._create_event_controller(
            workbench_service, fullscreen_service, deletion_service, dictionary_service
        )
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

        # Top section: Indicator section (fixed size)
        self._indicator_section = WorkbenchIndicatorSection(
            dictionary_service=self._dictionary_service, parent=self
        )
        main_layout.addWidget(self._indicator_section, 0)  # No stretch

        # Middle section: Beat frame section (takes remaining space)
        self._beat_frame_section = WorkbenchBeatFrameSection(
            layout_service=self._layout_service, parent=self
        )
        main_layout.addWidget(self._beat_frame_section, 1)  # Takes remaining space

    def _connect_signals(self):
        """Connect component signals"""
        if self._beat_frame_section:
            # Beat frame events
            self._beat_frame_section.beat_selected.connect(self._on_beat_selected)
            self._beat_frame_section.beat_modified.connect(self._on_beat_modified)
            self._beat_frame_section.sequence_modified.connect(
                self._on_sequence_modified
            )
            self._beat_frame_section.layout_changed.connect(self._on_layout_changed)

        # Connect beat frame button events (always connect these)
        if self._beat_frame_section:
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
            print(
                "🔧 DEBUG: Connected clear_sequence_requested signal to _handle_clear"
            )

        if self._event_controller:
            # Event controller signals
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

    # Public API methods
    def set_sequence(self, sequence: SequenceData):
        """Set the current sequence to display/edit"""
        self._current_sequence = sequence
        self._update_all_components()

        # CRITICAL FIX: Emit sequence_modified signal to notify external listeners
        # This enables dynamic option picker updates when sequence changes
        self.sequence_modified.emit(sequence)

    def get_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence"""
        return self._current_sequence

    def set_start_position(self, start_position_data: BeatData):
        """Set the start position"""
        self._start_position_data = start_position_data
        if self._beat_frame_section:
            self._beat_frame_section.set_start_position(start_position_data)

    def clear_start_position(self):
        """Clear the start position data (V1 clear behavior)"""
        self._start_position_data = None
        if self._beat_frame_section and hasattr(
            self._beat_frame_section, "_beat_frame"
        ):
            beat_frame = self._beat_frame_section._beat_frame
            if hasattr(beat_frame, "_start_position_view"):
                # Clear start position view to show only START text
                beat_frame._start_position_view.clear_position_data()

    def get_start_position(self) -> Optional[BeatData]:
        """Get the current start position"""
        return self._start_position_data

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

    # Event handlers using the event controller
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
        print("🧹 DEBUG: Clear sequence button clicked!")

        if not self._event_controller:
            print("❌ DEBUG: No event controller available")
            return

        success, message, updated_sequence = self._event_controller.handle_clear()
        print(
            f"🧹 DEBUG: Event controller result - success: {success}, message: {message}"
        )

        if success and updated_sequence:
            print(
                f"🧹 DEBUG: Clearing sequence - old length: {self._current_sequence.length if self._current_sequence else 0}"
            )
            self._current_sequence = updated_sequence
            print(f"🧹 DEBUG: New sequence length: {updated_sequence.length}")

            # Clear start position data and show cleared state (legacy behavior)
            self.clear_start_position()
            print("🧹 DEBUG: Start position cleared")

            self._update_all_components()
            print("🧹 DEBUG: All components updated")

            self.sequence_modified.emit(updated_sequence)
            print("🧹 DEBUG: Sequence modified signal emitted")

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

    # Component signal handlers
    def _on_beat_selected(self, beat_index: int):
        """Handle beat selection from beat frame and update graph editor"""
        # Enable delete button
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
        # Store layout parameters for potential future use
        _ = rows
        _ = columns

    def _on_graph_editor_beat_changed(self, beat_data: BeatData, beat_index: int):
        """Handle beat changes from graph editor and update beat frame"""
        if hasattr(self, "_beat_frame_section") and self._beat_frame_section:
            # Update the specific beat in beat frame
            if hasattr(self._beat_frame_section, "update_beat_at_index"):
                self._beat_frame_section.update_beat_at_index(beat_index, beat_data)

            # Refresh beat frame display
            if hasattr(self._beat_frame_section, "refresh_display"):
                self._beat_frame_section.refresh_display()

            # Update current sequence
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

        if self._beat_frame_section:
            self._beat_frame_section.update_button_sizes(self.height())
