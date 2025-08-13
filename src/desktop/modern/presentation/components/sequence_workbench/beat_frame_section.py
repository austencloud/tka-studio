from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from desktop.modern.core.interfaces.core_services import ILayoutService
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData

from .button_panel import SequenceWorkbenchButtonPanel
from .sequence_beat_frame.sequence_beat_frame import SequenceBeatFrame


if TYPE_CHECKING:
    from desktop.modern.application.services.workbench.beat_selection_service import (
        BeatSelectionService,
    )


class WorkbenchBeatFrameSection(QWidget):
    """Beat frame section component combining beat frame and button panel"""

    # Signals for parent workbench
    beat_selected = pyqtSignal(int)
    beat_modified = pyqtSignal(int, object)
    sequence_modified = pyqtSignal(object)  # SequenceData object
    layout_changed = pyqtSignal(int, int)

    # Button panel signals
    add_to_dictionary_requested = pyqtSignal()
    # save_image_requested = pyqtSignal()  # REMOVED - functionality moved to Export tab
    view_fullscreen_requested = pyqtSignal()
    mirror_sequence_requested = pyqtSignal()
    swap_colors_requested = pyqtSignal()
    rotate_sequence_requested = pyqtSignal()
    copy_json_requested = pyqtSignal()
    delete_beat_requested = pyqtSignal()
    clear_sequence_requested = pyqtSignal()
    edit_construct_toggle_requested = pyqtSignal(bool)

    def __init__(
        self,
        layout_service: ILayoutService,
        beat_selection_service: BeatSelectionService,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self._layout_service = layout_service
        self._beat_selection_service = beat_selection_service
        self._current_sequence: SequenceData | None = None
        self._start_position_data: BeatData | None = None

        # Components
        self._beat_frame: SequenceBeatFrame | None = None
        self._button_panel: SequenceWorkbenchButtonPanel | None = None

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Setup beat frame + button panel layout matching Legacy's structure"""
        layout = QHBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create beat frame (left side)
        self._beat_frame = SequenceBeatFrame(
            layout_service=self._layout_service,
            beat_selection_service=self._beat_selection_service,
            parent=self,
        )
        self._beat_frame.setMinimumHeight(400)

        # CRITICAL FIX: Ensure beat frame is visible
        self._beat_frame.show()
        self._beat_frame.setVisible(True)

        # Create button panel (right side)
        self._button_panel = SequenceWorkbenchButtonPanel(self)

        # Add with proper proportions (10:1 ratio like Legacy)
        layout.addWidget(self._beat_frame, 10)
        layout.addWidget(self._button_panel, 1)

        # CRITICAL FIX: Ensure the beat frame section itself is visible
        self.show()
        self.setVisible(True)

    def _connect_signals(self):
        """Connect internal component signals"""
        if self._beat_frame:
            self._beat_frame.beat_selected.connect(self.beat_selected)
            self._beat_frame.beat_modified.connect(self.beat_modified)
            self._beat_frame.sequence_modified.connect(self.sequence_modified)
            self._beat_frame.layout_changed.connect(self.layout_changed)

        if self._button_panel:
            # Dictionary & Export operations
            self._button_panel.add_to_dictionary_requested.connect(
                self.add_to_dictionary_requested
            )
            # save_image_requested signal removed - functionality moved to Export tab
            self._button_panel.view_fullscreen_requested.connect(
                self.view_fullscreen_requested
            )

            # Transform operations
            self._button_panel.mirror_sequence_requested.connect(
                self.mirror_sequence_requested
            )
            self._button_panel.swap_colors_requested.connect(self.swap_colors_requested)
            self._button_panel.rotate_sequence_requested.connect(
                self.rotate_sequence_requested
            )

            # Sequence management operations
            self._button_panel.copy_json_requested.connect(self.copy_json_requested)
            self._button_panel.delete_beat_requested.connect(
                self._handle_delete_beat_request
            )
            self._button_panel.clear_sequence_requested.connect(
                self._handle_clear_sequence_request
            )

    def _handle_delete_beat_request(self):
        """Handle delete beat request from button panel"""
        print("🗑️ [BEAT_FRAME_SECTION] Delete beat requested from button panel")
        print(
            f"📊 [BEAT_FRAME_SECTION] Current selected beat index: {self.get_selected_beat_index()}"
        )
        self.delete_beat_requested.emit()

    def _handle_clear_sequence_request(self):
        """Handle clear sequence request from button panel"""

        # Reset button panel to Construct mode when clearing sequence
        if self._button_panel and hasattr(
            self._button_panel, "reset_to_construct_mode"
        ):
            self._button_panel.reset_to_construct_mode()

        self.clear_sequence_requested.emit()

    def set_sequence(self, sequence: SequenceData | None):
        """Set the current sequence"""

        self._current_sequence = sequence
        if self._beat_frame:
            self._beat_frame.set_sequence(sequence)
        else:
            print("⚠️ [BEAT_FRAME_SECTION] No beat frame available")

        # Initialize cleared start position for empty sequences
        if not sequence or sequence.length == 0:
            self.initialize_cleared_start_position()

        self._update_button_states()

    def set_start_position(
        self,
        start_position_data: BeatData,
        pictograph_data: PictographData | None = None,
    ):
        """
        Set the start position with optional separate pictograph data.

        Args:
            start_position_data: Beat context data (beat number, duration, metadata)
            pictograph_data: Optional pictograph data for direct rendering.
                           If None, will be reconstructed from beat_data (legacy mode)
        """
        self._start_position_data = start_position_data
        if self._beat_frame:
            self._beat_frame.set_start_position(start_position_data, pictograph_data)

    def initialize_cleared_start_position(self):
        """Initialize start position view in cleared state (shows START text only)"""
        self.show()
        self.setVisible(True)

        # Debug parent visibility
        self.parent()

        self._start_position_data = None
        if self._beat_frame:
            self._beat_frame.initialize_cleared_start_position()
        else:
            print("❌ [BEAT_FRAME_SECTION] No beat frame available!")

    def get_selected_beat_index(self) -> int | None:
        """Get selected beat index from beat frame"""
        return self._beat_frame.get_selected_beat_index() if self._beat_frame else None

    def set_button_enabled(self, button_name: str, enabled: bool):
        """Enable/disable specific button"""
        if self._button_panel:
            self._button_panel.set_button_enabled(button_name, enabled)

    def show_button_message(self, button_name: str, message: str, duration: int = 2000):
        """Show message tooltip on button"""
        if self._button_panel:
            self._button_panel.show_message_tooltip(button_name, message, duration)

    def _update_button_states(self):
        """Update button enabled states based on current sequence"""
        if not self._button_panel:
            return

        has_sequence = (
            self._current_sequence is not None and self._current_sequence.length > 0
        )

        # Buttons that require a sequence
        sequence_dependent_buttons = [
            "save_image",
            "mirror_sequence",
            "swap_colors",
            "rotate_sequence",
            "copy_json",
            "add_to_dictionary",
        ]

        for button_name in sequence_dependent_buttons:
            self._button_panel.set_button_enabled(button_name, has_sequence)

        # Clear button is always enabled
        self._button_panel.set_button_enabled("clear_sequence", True)

        # Delete beat requires selection
        # This will be updated when beat selection changes
        self._button_panel.set_button_enabled("delete_beat", False)

    def update_button_sizes(self, container_height: int):
        """Update button sizes for responsive design"""
        if self._button_panel:
            self._button_panel.update_button_sizes(container_height)
