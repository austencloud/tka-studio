"""
ComponentConnector

Handles signal connections and inter-component communication for the construct tab.
"""

from __future__ import annotations

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
    generate_requested = pyqtSignal(object)  # generation_config (deprecated)
    sequence_generated = pyqtSignal(list)  # sequence_data (NEW: direct from controller)
    graph_beat_modified = pyqtSignal(int, object)  # beat_index, beat_data
    export_requested = pyqtSignal(str, dict)  # NEW: export_type, options

    def __init__(self, parent=None):
        super().__init__(parent)
        self.workbench = None
        self.graph_editor = None
        self.generate_panel = None
        self.start_position_picker = None
        self.export_panel = None  # NEW: Export panel reference

    def set_workbench(self, workbench):
        """Set the workbench and connect its signals."""
        self.workbench = workbench
        self._connect_beat_frame_signals()

        # CRITICAL: If export panel already exists, connect it to workbench
        if self.export_panel and hasattr(self.export_panel, "set_workbench_widget"):
            self.export_panel.set_workbench_widget(self.workbench)
            print(
                "🔗 [COMPONENT_CONNECTOR] Workbench connected to existing export panel"
            )
            self._connect_export_panel_updates()

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

        # Connect to the controller's generation_completed signal instead of generate_requested
        # This bypasses the old routing through SignalCoordinator
        controller = getattr(generate_panel, "_controller", None)
        if controller and hasattr(controller, "generation_completed"):
            controller.generation_completed.connect(self._on_generation_completed)
            print("🔗 [COMPONENT_CONNECTOR] Connected to GeneratePanel controller")
        # Fallback to old method if controller not available
        elif hasattr(generate_panel, "generate_requested"):
            generate_panel.generate_requested.connect(self._on_generate_requested)
            print(
                "⚠️ [COMPONENT_CONNECTOR] Using fallback generate_requested connection"
            )

    def set_start_position_picker(self, start_position_picker):
        """Set the start position picker for transition management."""
        self.start_position_picker = start_position_picker

    def set_export_panel(self, export_panel):
        """Set the export panel and connect its signals (NEW)."""
        self.export_panel = export_panel
        if export_panel and hasattr(export_panel, "export_requested"):
            export_panel.export_requested.connect(self._on_export_requested)
            print("🔤 [COMPONENT_CONNECTOR] Export panel connected")

        # CRITICAL: Connect workbench to export panel for sequence data access
        if self.workbench and export_panel:
            if hasattr(export_panel, "set_workbench_widget"):
                export_panel.set_workbench_widget(self.workbench)
                print("🔗 [COMPONENT_CONNECTOR] Workbench connected to export panel")

            self._connect_export_panel_updates()

    def _connect_export_panel_updates(self):
        """Connect workbench changes to export panel preview updates (NEW)."""
        if not (self.workbench and self.export_panel):
            return

        # Connect sequence modification signals to update export preview
        if hasattr(self.workbench, "sequence_modified"):
            self.workbench.sequence_modified.connect(
                self._on_sequence_changed_for_export
            )

    def _connect_beat_frame_signals(self):
        """Connect beat frame signals to graph editor."""
        if not self.workbench:
            return

        beat_frame_section = getattr(self.workbench, "_beat_frame_section", None)
        if not beat_frame_section:
            return

        beat_frame: SequenceBeatFrame = getattr(beat_frame_section, "_beat_frame", None)
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
            print("⚠️ No current sequence available")
            return

        if beat_index == -1:
            # Handle start position selection
            start_position_data = getattr(self.workbench, "_start_position_data", None)
            if start_position_data:
                self.graph_editor.set_selected_beat_data(-1, start_position_data)
            else:
                print("⚠️ No start position data available")
            return

        if 0 <= beat_index < len(current_sequence.beats):
            beat_data = current_sequence.beats[beat_index]
            self.graph_editor.set_selected_beat_data(beat_index, beat_data)
        else:
            print(
                f"⚠️ Invalid beat index: {beat_index} (sequence has {len(current_sequence.beats)} beats)"
            )

    def _on_generation_completed(self, result):
        """Handle generation completion from generate panel controller."""
        print(
            f"🎯 [COMPONENT_CONNECTOR] Generation completed: success={result.success}"
        )

        if result.success and result.sequence_data:
            print(
                f"🎯 [COMPONENT_CONNECTOR] Emitting sequence_generated with {len(result.sequence_data)} beats"
            )
            self.sequence_generated.emit(result.sequence_data)
        else:
            error_msg = result.error_message or "Unknown generation error"
            print(f"❌ [COMPONENT_CONNECTOR] Generation failed: {error_msg}")

    def _on_generate_requested(self, generation_config):
        """Handle generation request from generate panel (DEPRECATED)."""
        print(
            f"🤖 [COMPONENT_CONNECTOR] Generation requested with config: {generation_config}"
        )
        self.generate_requested.emit(generation_config)

    def _on_export_requested(self, export_type: str, options: dict):
        """Handle export request from export panel (NEW)."""
        print(
            f"🔤 [COMPONENT_CONNECTOR] Export requested: {export_type} with options: {options}"
        )
        self.export_requested.emit(export_type, options)

        # Trigger actual export based on type
        if export_type == "export_current" and self.workbench:
            self._handle_current_sequence_export(options)
        elif export_type == "export_all":
            self._handle_all_pictographs_export(options)

    def _handle_current_sequence_export(self, options: dict):
        """Handle current sequence export (replaces old save image button) (NEW)."""
        print("🔤 [COMPONENT_CONNECTOR] Export request delegated to export panel...")
        # The export panel now handles this directly with its workbench connection
        # No need to duplicate logic here

    def _handle_all_pictographs_export(self, options: dict):
        """Handle export all pictographs functionality (NEW)."""
        print("📚 [COMPONENT_CONNECTOR] Export all pictographs not yet implemented")
        # This would be implemented later as part of extended export functionality

    def _on_sequence_changed_for_export(self, sequence):
        """Handle sequence changes to update export panel preview (NEW)."""
        if self.export_panel and hasattr(self.export_panel, "_update_preview"):
            print(
                "🔄 [COMPONENT_CONNECTOR] Updating export panel preview after sequence change"
            )
            self.export_panel._update_preview()

    def _on_graph_beat_modified(self, beat_index: int, beat_data):
        """Handle beat modification from graph editor."""
        print(f"✅ Graph editor modified beat {beat_index}")
        self.graph_beat_modified.emit(beat_index, beat_data)

        # Update export panel preview if available
        if self.export_panel and hasattr(self.export_panel, "_update_preview"):
            self.export_panel._update_preview()

    def notify_generation_completed(self, success: bool, error_message: str):
        """Notify the generate panel that generation has completed."""
        print(
            f"🔔 [COMPONENT_CONNECTOR] Notifying generation completion: success={success}"
        )

        if self.generate_panel and hasattr(
            self.generate_panel, "set_generation_result"
        ):
            from desktop.modern.domain.models.generation_models import GenerationResult

            result = GenerationResult(
                success=success, error_message=error_message if not success else None
            )
            self.generate_panel.set_generation_result(result)
        else:
            print(
                "❌ [COMPONENT_CONNECTOR] No generate panel or set_generation_result method"
            )

    def prepare_for_transition(self, target_mode: str):
        """Prepare components for transition based on target mode."""
        if target_mode == "start_position" and self.start_position_picker:
            if hasattr(self.start_position_picker, "set_transition_mode"):
                self.start_position_picker.set_transition_mode(True)
        elif target_mode == "option_picker":
            # Prepare option picker for transition if needed
            pass
        elif target_mode == "export_panel" and self.export_panel:
            # Prepare export panel for transition
            if hasattr(self.export_panel, "_update_preview"):
                self.export_panel._update_preview()

    def finalize_transition(self, target_mode: str):
        """Finalize transition cleanup."""
        if target_mode == "start_position" and self.start_position_picker:
            if hasattr(self.start_position_picker, "set_transition_mode"):
                self.start_position_picker.set_transition_mode(False)
        elif target_mode == "export_panel" and self.export_panel:
            # Finalize export panel transition
            print("🔤 [COMPONENT_CONNECTOR] Export panel transition finalized")
