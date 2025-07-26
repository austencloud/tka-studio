"""
ComponentConnector

Handles signal connections and inter-component communication for the construct tab.
"""

from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from desktop.modern.presentation.components.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )


class ComponentConnector(QObject):
    """
    Handles signal connections between components.

    Responsibilities:
    - Connecting beat frame to graph editor
    - Connecting generate panel signals
    - Handling beat selection events
    - Managing component communication
    """

    # Signals for external communication
    beat_selected_for_graph_editor = pyqtSignal(int)  # beat_index
    generate_requested = pyqtSignal(object)  # generation_config
    graph_beat_modified = pyqtSignal(int, object)  # beat_index, beat_data

    def __init__(self, parent=None):
        super().__init__(parent)
        self.workbench = None
        self.graph_editor = None
        self.generate_panel = None
        self.start_position_picker = None

    def set_workbench(self, workbench):
        """Set the workbench and connect its signals."""
        self.workbench = workbench
        self._connect_beat_frame_signals()

    def set_graph_editor(self, graph_editor):
        """Set the graph editor and connect its signals."""
        self.graph_editor = graph_editor
        if hasattr(graph_editor, "beat_modified"):
            graph_editor.beat_modified.connect(self._on_graph_beat_modified)

        # Connect to beat selection signal
        self.beat_selected_for_graph_editor.connect(
            self._on_beat_selected_for_graph_editor
        )

    def set_generate_panel(self, generate_panel):
        """Set the generate panel and connect its signals."""
        self.generate_panel = generate_panel
        if hasattr(generate_panel, "generate_requested"):
            generate_panel.generate_requested.connect(self._on_generate_requested)

    def set_start_position_picker(self, start_position_picker):
        """Set the start position picker for transition management."""
        self.start_position_picker = start_position_picker

    def _connect_beat_frame_signals(self):
        """Connect beat frame signals to graph editor."""
        if not self.workbench:
            return

        beat_frame_section = getattr(self.workbench, "_beat_frame_section", None)
        if not beat_frame_section:
            return

        beat_frame: "SequenceBeatFrame" = getattr(
            beat_frame_section, "_beat_frame", None
        )
        if not beat_frame:
            return

        beat_frame.beat_selected.connect(self._on_beat_selected)

    def _on_beat_selected(self, beat_index: int):
        """Handle beat selection from the beat frame."""
        self.beat_selected_for_graph_editor.emit(beat_index)

    def _on_beat_selected_for_graph_editor(self, beat_index: int):
        """Handle beat selection for graph editor update."""
        if not self.graph_editor or not self.workbench:
            print(
                f"⚠️ Missing components - graph_editor: {bool(self.graph_editor)}, workbench: {bool(self.workbench)}"
            )
            return

        current_sequence = self.workbench.get_sequence()
        if not current_sequence:
            print(f"⚠️ No current sequence available")
            return

        if beat_index == -1:
            # Handle start position selection
            start_position_data = getattr(self.workbench, "_start_position_data", None)
            if start_position_data:
                self.graph_editor.set_selected_beat_data(-1, start_position_data)
            else:
                print(f"⚠️ No start position data available")
            return

        if 0 <= beat_index < len(current_sequence.beats):
            beat_data = current_sequence.beats[beat_index]
            self.graph_editor.set_selected_beat_data(beat_index, beat_data)
        else:
            print(
                f"⚠️ Invalid beat index: {beat_index} (sequence has {len(current_sequence.beats)} beats)"
            )

    def _on_generate_requested(self, generation_config):
        """Handle generation request from generate panel."""
        print(
            f"🤖 [COMPONENT_CONNECTOR] Generation requested with config: {generation_config}"
        )
        self.generate_requested.emit(generation_config)

    def _on_graph_beat_modified(self, beat_index: int, beat_data):
        """Handle beat modification from graph editor."""
        print(f"✅ Graph editor modified beat {beat_index}")
        self.graph_beat_modified.emit(beat_index, beat_data)

    def prepare_for_transition(self, target_mode: str):
        """Prepare components for transition based on target mode."""
        if target_mode == "start_position" and self.start_position_picker:
            if hasattr(self.start_position_picker, "set_transition_mode"):
                self.start_position_picker.set_transition_mode(True)
        elif target_mode == "option_picker":
            # Prepare option picker for transition if needed
            pass

    def finalize_transition(self, target_mode: str):
        """Finalize transition cleanup."""
        if target_mode == "start_position" and self.start_position_picker:
            if hasattr(self.start_position_picker, "set_transition_mode"):
                self.start_position_picker.set_transition_mode(False)
