"""
Qt Graph Editor Data Flow Manager Adapter

This adapter wraps the pure GraphEditorDataFlowService and provides Qt signal coordination.
This maintains the separation between platform-agnostic services and Qt-specific presentation logic.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.application.services.graph_editor.graph_editor_data_flow_service import (
    GraphEditorDataFlowService,
)
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


class QtGraphEditorDataFlowManagerAdapter(QObject):
    """
    Qt adapter for the GraphEditorDataFlowService that provides signal coordination.

    This class handles Qt-specific signal emissions while delegating actual
    data flow management logic to the platform-agnostic service.
    """

    # Qt signals for UI coordination
    beat_data_updated = pyqtSignal(
        object, int, object
    )  # BeatData, position, SequenceData
    sequence_modified = pyqtSignal(object)  # SequenceData

    def __init__(
        self,
        graph_editor_getter: Callable[[], object] | None = None,
    ):
        super().__init__()

        # Create the pure service
        self._service = GraphEditorDataFlowService(
            graph_editor_getter=graph_editor_getter,
        )

        # Connect service callbacks to Qt signals
        self._service.add_beat_data_updated_callback(self._on_beat_data_updated)
        self._service.add_sequence_modified_callback(self._on_sequence_modified)

    def _on_beat_data_updated(
        self, beat_data: BeatData, position: int, sequence_data: SequenceData
    ):
        """Convert service callback to Qt signal."""
        self.beat_data_updated.emit(beat_data, position, sequence_data)

    def _on_sequence_modified(self, sequence_data: SequenceData):
        """Convert service callback to Qt signal."""
        self.sequence_modified.emit(sequence_data)

    # Delegate all service methods to the pure service
    def update_beat_data(
        self,
        beat_data: BeatData,
        position: int,
        sequence_data: SequenceData,
        source: str = "graph_editor",
    ) -> SequenceData:
        """Update beat data from graph editor modifications."""
        return self._service.update_beat_data(
            beat_data, position, sequence_data, source
        )

    def modify_sequence(
        self,
        sequence_data: SequenceData,
        modification_type: str,
        details: dict[str, Any],
    ) -> SequenceData:
        """Modify sequence based on graph editor changes."""
        return self._service.modify_sequence(sequence_data, modification_type, details)

    def sync_data_from_graph_editor(self, sequence_data: SequenceData) -> SequenceData:
        """Synchronize data from graph editor to sequence."""
        return self._service.sync_data_from_graph_editor(sequence_data)

    def sync_data_to_graph_editor(self, sequence_data: SequenceData):
        """Synchronize data from sequence to graph editor."""
        return self._service.sync_data_to_graph_editor(sequence_data)

    def validate_data_consistency(self, sequence_data: SequenceData) -> bool:
        """Validate data consistency between graph editor and sequence."""
        return self._service.validate_data_consistency(sequence_data)
