"""
Pure Graph Editor Data Flow Service - Platform Agnostic

This service handles graph editor data flow without any Qt dependencies.
Qt-specific signal coordination is handled by adapters in the presentation layer.
"""

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData

if TYPE_CHECKING:
    from desktop.modern.presentation.components.graph_editor.graph_editor import (
        GraphEditor,
    )

logger = logging.getLogger(__name__)


class GraphEditorDataFlowService:
    """
    Pure service for managing graph editor data flow.

    This service is platform-agnostic and does not depend on Qt.
    Signal coordination is handled by Qt adapters in the presentation layer.

    Responsibilities:
    - Managing beat data updates from graph editor
    - Coordinating sequence modifications
    - Handling data flow between graph editor and sequence
    """

    def __init__(
        self,
        graph_editor_getter: Callable[[], "GraphEditor"] | None = None,
    ):
        self.graph_editor_getter = graph_editor_getter

        # Platform-agnostic event callbacks
        self._beat_data_updated_callbacks: list[
            Callable[[BeatData, int, SequenceData], None]
        ] = []
        self._sequence_modified_callbacks: list[Callable[[SequenceData], None]] = []

    def add_beat_data_updated_callback(
        self, callback: Callable[[BeatData, int, SequenceData], None]
    ):
        """Add callback for when beat data is updated."""
        self._beat_data_updated_callbacks.append(callback)

    def add_sequence_modified_callback(self, callback: Callable[[SequenceData], None]):
        """Add callback for when sequence is modified."""
        self._sequence_modified_callbacks.append(callback)

    def update_beat_data(
        self,
        beat_data: BeatData,
        position: int,
        sequence_data: SequenceData,
        source: str = "graph_editor",
    ) -> SequenceData:
        """
        Update beat data from graph editor modifications.

        Args:
            beat_data: The updated beat data
            position: Position of the beat in the sequence
            sequence_data: Current sequence data
            source: Source of the update (for tracking)

        Returns:
            Updated sequence data
        """
        try:
            # Update the beat in the sequence
            updated_sequence = sequence_data.update_beat(position, beat_data)

            # Update graph editor if available
            if self.graph_editor_getter:
                try:
                    graph_editor = self.graph_editor_getter()
                    if graph_editor and hasattr(graph_editor, "update_beat_data"):
                        graph_editor.update_beat_data(beat_data, position)
                except Exception as e:
                    logger.warning(f"Could not update graph editor: {e}")

            # Notify callbacks instead of emitting Qt signals
            for callback in self._beat_data_updated_callbacks:
                callback(beat_data, position, updated_sequence)

            logger.info(f"Beat data updated at position {position} from {source}")
            return updated_sequence

        except Exception as e:
            logger.error(f"Failed to update beat data: {e}")
            raise

    def modify_sequence(
        self,
        sequence_data: SequenceData,
        modification_type: str,
        details: dict[str, Any],
    ) -> SequenceData:
        """
        Modify sequence based on graph editor changes.

        Args:
            sequence_data: Current sequence data
            modification_type: Type of modification (add, remove, update, etc.)
            details: Details about the modification

        Returns:
            Modified sequence data
        """
        try:
            modified_sequence = sequence_data

            if modification_type == "add_beat":
                position = details.get("position", len(sequence_data.beats))
                beat_data = details.get("beat_data")
                if beat_data:
                    modified_sequence = sequence_data.add_beat(beat_data, position)

            elif modification_type == "remove_beat":
                position = details.get("position")
                if position is not None:
                    modified_sequence = sequence_data.remove_beat(position)

            elif modification_type == "update_beat":
                position = details.get("position")
                beat_data = details.get("beat_data")
                if position is not None and beat_data:
                    modified_sequence = sequence_data.update_beat(position, beat_data)

            elif modification_type == "reorder_beats":
                old_position = details.get("old_position")
                new_position = details.get("new_position")
                if old_position is not None and new_position is not None:
                    modified_sequence = sequence_data.reorder_beat(
                        old_position, new_position
                    )

            else:
                logger.warning(f"Unknown modification type: {modification_type}")
                return sequence_data

            # Update graph editor if available
            if self.graph_editor_getter:
                try:
                    graph_editor = self.graph_editor_getter()
                    if graph_editor and hasattr(graph_editor, "update_sequence"):
                        graph_editor.update_sequence(modified_sequence)
                except Exception as e:
                    logger.warning(f"Could not update graph editor: {e}")

            # Notify callbacks instead of emitting Qt signals
            for callback in self._sequence_modified_callbacks:
                callback(modified_sequence)

            logger.info(f"Sequence modified: {modification_type}")
            return modified_sequence

        except Exception as e:
            logger.error(f"Failed to modify sequence: {e}")
            raise

    def sync_data_from_graph_editor(self, sequence_data: SequenceData) -> SequenceData:
        """
        Synchronize data from graph editor to sequence.

        Args:
            sequence_data: Current sequence data

        Returns:
            Synchronized sequence data
        """
        try:
            if not self.graph_editor_getter:
                return sequence_data

            graph_editor = self.graph_editor_getter()
            if not graph_editor:
                return sequence_data

            # Get current data from graph editor
            if hasattr(graph_editor, "get_current_data"):
                graph_data = graph_editor.get_current_data()
                if graph_data:
                    # Update sequence with graph editor data
                    updated_sequence = self._apply_graph_data_to_sequence(
                        sequence_data, graph_data
                    )
                    return updated_sequence

            return sequence_data

        except Exception as e:
            logger.error(f"Failed to sync data from graph editor: {e}")
            return sequence_data

    def sync_data_to_graph_editor(self, sequence_data: SequenceData):
        """
        Synchronize data from sequence to graph editor.

        Args:
            sequence_data: Current sequence data
        """
        try:
            if not self.graph_editor_getter:
                return

            graph_editor = self.graph_editor_getter()
            if not graph_editor:
                return

            # Update graph editor with sequence data
            if hasattr(graph_editor, "update_sequence"):
                graph_editor.update_sequence(sequence_data)

            logger.info("Data synchronized to graph editor")

        except Exception as e:
            logger.error(f"Failed to sync data to graph editor: {e}")

    def _apply_graph_data_to_sequence(
        self, sequence_data: SequenceData, graph_data: dict[str, Any]
    ) -> SequenceData:
        """
        Apply graph editor data to sequence data.

        Args:
            sequence_data: Current sequence data
            graph_data: Data from graph editor

        Returns:
            Updated sequence data
        """
        try:
            # This is a placeholder implementation
            # In a real implementation, you would parse the graph_data
            # and apply the changes to the sequence_data

            updated_sequence = sequence_data

            # Example: Update beats based on graph data
            beats = graph_data.get("beats", [])
            for i, beat_info in enumerate(beats):
                if i < len(sequence_data.beats):
                    # Update existing beat
                    current_beat = sequence_data.beats[i]
                    if "pictograph_data" in beat_info:
                        updated_beat = current_beat.update_pictograph(
                            beat_info["pictograph_data"]
                        )
                        updated_sequence = updated_sequence.update_beat(i, updated_beat)

            return updated_sequence

        except Exception as e:
            logger.error(f"Failed to apply graph data to sequence: {e}")
            return sequence_data

    def validate_data_consistency(self, sequence_data: SequenceData) -> bool:
        """
        Validate data consistency between graph editor and sequence.

        Args:
            sequence_data: Current sequence data

        Returns:
            True if data is consistent, False otherwise
        """
        try:
            if not self.graph_editor_getter:
                return True

            graph_editor = self.graph_editor_getter()
            if not graph_editor:
                return True

            # Get current data from graph editor
            if hasattr(graph_editor, "get_current_data"):
                graph_data = graph_editor.get_current_data()
                if graph_data:
                    # Compare graph data with sequence data
                    return self._compare_graph_and_sequence_data(
                        sequence_data, graph_data
                    )

            return True

        except Exception as e:
            logger.error(f"Failed to validate data consistency: {e}")
            return False

    def _compare_graph_and_sequence_data(
        self, sequence_data: SequenceData, graph_data: dict[str, Any]
    ) -> bool:
        """
        Compare graph editor data with sequence data.

        Args:
            sequence_data: Current sequence data
            graph_data: Data from graph editor

        Returns:
            True if data is consistent, False otherwise
        """
        try:
            # This is a placeholder implementation
            # In a real implementation, you would compare the data structures

            # Example: Check beat count
            graph_beats = graph_data.get("beats", [])
            if len(graph_beats) != len(sequence_data.beats):
                return False

            # Example: Check beat data
            for i, graph_beat in enumerate(graph_beats):
                if i < len(sequence_data.beats):
                    sequence_beat = sequence_data.beats[i]
                    # Compare beat data (simplified)
                    if graph_beat.get("letter") != sequence_beat.letter:
                        return False

            return True

        except Exception as e:
            logger.error(f"Failed to compare data: {e}")
            return False
