"""
Graph Editor Service Implementation

Provides graph editor functionality for the modern TKA desktop application.
Manages graph editor state, beat selection, and UI interactions.
"""

from typing import Optional

from desktop.modern.core.interfaces.core_services import IUIStateManager
from desktop.modern.core.interfaces.workbench_services import IGraphEditorService
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.enums import MotionType
from desktop.modern.domain.models.sequence_data import SequenceData


class GraphEditorCoordinator(IGraphEditorService):
    """Modern graph editor coordinator implementation"""

    def __init__(self, ui_state_service: Optional[IUIStateManager] = None):
        self.ui_state_service = ui_state_service
        self._current_sequence: Optional[SequenceData] = None
        self._selected_beat: Optional[BeatData] = None
        self._selected_beat_index: Optional[int] = None
        self._selected_arrow_id: Optional[str] = None
        self._is_visible: bool = False

        # Graph editor settings with proven ratios
        self._graph_height_ratio = 3.5  # parent_height // 3.5
        self._max_width_ratio = 4  # parent_width // 4

    def update_graph_display(self, sequence: Optional[SequenceData]) -> None:
        """Update the graph editor display with sequence data"""
        self._current_sequence = sequence

        # Clear selections when sequence changes
        if sequence != self._current_sequence:
            self._selected_beat = None
            self._selected_beat_index = None
            self._selected_arrow_id = None

        # Notify UI state service if available (save only basic info, not the full sequence object)
        if self.ui_state_service:
            sequence_info = {
                "beat_count": len(sequence.beats) if sequence and sequence.beats else 0,
                "sequence_id": sequence.id if sequence else None,
            }
            self.ui_state_service.set_setting(
                "graph_editor_sequence_info", sequence_info
            )

    def toggle_graph_visibility(self) -> bool:
        """Toggle graph editor visibility, return new visibility state"""
        self._is_visible = not self._is_visible

        # Notify UI state service if available
        if self.ui_state_service:
            self.ui_state_service.set_setting("graph_editor_visible", self._is_visible)

        return self._is_visible

    def set_selected_beat(
        self, beat_data: Optional[BeatData], beat_index: Optional[int] = None
    ) -> None:
        """Set the currently selected beat for editing"""
        self._selected_beat = beat_data
        self._selected_beat_index = beat_index

        # Clear arrow selection when beat changes
        self._selected_arrow_id = None

        # Notify UI state service if available
        if self.ui_state_service:
            self.ui_state_service.set_setting(
                "graph_editor_selected_beat_index", beat_index
            )

    def get_selected_beat(self) -> Optional[BeatData]:
        """Get the currently selected beat"""
        return self._selected_beat

    def get_selected_beat_index(self) -> Optional[int]:
        """Get the currently selected beat index"""
        return self._selected_beat_index

    def is_visible(self) -> bool:
        """Check if graph editor is currently visible"""
        return self._is_visible

    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence being displayed"""
        return self._current_sequence

    def update_beat_adjustments(self, beat_data: BeatData) -> BeatData:
        """Apply adjustment panel modifications to beat data"""
        # In a full implementation, this would apply any pending adjustments
        # from the adjustment panel to the beat data
        return beat_data

    def set_arrow_selection(self, arrow_id: Optional[str]) -> None:
        """Set selected arrow for detailed editing"""
        self._selected_arrow_id = arrow_id

        # Notify UI state service if available
        if self.ui_state_service:
            self.ui_state_service.set_setting("graph_editor_selected_arrow", arrow_id)

    def get_available_turns(self, arrow_color: str) -> list[float]:
        """Get available turn values for specified arrow color"""
        # Standard turn values - these are common turn increments
        return [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0]

    def get_available_orientations(self, arrow_color: str) -> list[str]:
        """Get available orientation values for specified arrow color"""
        # Standard orientations based on motion types
        return ["pro", "anti", "float", "dash", "static"]

    def apply_turn_adjustment(self, arrow_color: str, turn_value: float) -> bool:
        """Apply turn adjustment to selected arrow"""
        if not self._selected_beat:
            return False

        try:
            # Update actual beat data
            updated = False
            if arrow_color == "blue" and self._selected_beat.blue_motion:
                # Create updated motion data with new turns value
                updated_motion = self._selected_beat.blue_motion.update(
                    turns=turn_value
                )
                # Update the beat with the new motion data
                self._selected_beat = self._selected_beat.update(
                    blue_motion=updated_motion
                )
                updated = True
            elif arrow_color == "red" and self._selected_beat.red_motion:
                # Create updated motion data with new turns value
                updated_motion = self._selected_beat.red_motion.update(turns=turn_value)
                # Update the beat with the new motion data
                self._selected_beat = self._selected_beat.update(
                    red_motion=updated_motion
                )
                updated = True

            if updated:
                # Persist changes (connect to existing persistence layer)
                self._persist_beat_changes(self._selected_beat)

                # Notify UI components of changes
                self._notify_beat_changed(self._selected_beat)

            return updated

        except Exception as e:
            print(f"⚠️ Turn adjustment failed: {e}")
            return False

    def apply_orientation_adjustment(self, arrow_color: str, orientation: str) -> bool:
        """Apply orientation adjustment to selected arrow"""
        if not self._selected_beat:
            return False

        try:
            # Update actual beat data
            updated = False
            if arrow_color == "blue" and self._selected_beat.blue_motion:
                # Create updated motion data with new motion type
                updated_motion = self._selected_beat.blue_motion.update(
                    motion_type=MotionType(orientation)
                )
                # Update the beat with the new motion data
                self._selected_beat = self._selected_beat.update(
                    blue_motion=updated_motion
                )
                updated = True
            elif arrow_color == "red" and self._selected_beat.red_motion:
                # Create updated motion data with new motion type
                updated_motion = self._selected_beat.red_motion.update(
                    motion_type=MotionType(orientation)
                )
                # Update the beat with the new motion data
                self._selected_beat = self._selected_beat.update(
                    red_motion=updated_motion
                )
                updated = True

            if updated:
                # Persist changes (connect to existing persistence layer)
                self._persist_beat_changes(self._selected_beat)

                # Notify UI components of changes
                self._notify_beat_changed(self._selected_beat)

            return updated

        except Exception as e:
            print(f"⚠️ Orientation adjustment failed: {e}")
            return False

    def get_graph_editor_size_ratio(self) -> tuple[float, float]:
        """Get the size ratios for graph editor dimensions"""
        return (self._graph_height_ratio, self._max_width_ratio)

    def _persist_beat_changes(self, beat_data: BeatData) -> None:
        """Persist beat changes to JSON repository"""
        # TODO: Connect to existing beat persistence mechanism
        # This should trigger JSON file updates and sequence state changes
        # For now, update the sequence in memory if we have context
        if self._current_sequence and self._selected_beat_index is not None:
            beats = list(self._current_sequence.beats)
            if self._selected_beat_index < len(beats):
                beats[self._selected_beat_index] = beat_data
                self._current_sequence = self._current_sequence.update(beats=beats)

    def _notify_beat_changed(self, beat_data: BeatData) -> None:
        """Notify all UI components that beat data has changed"""
        # TODO: Implement signal emission for UI synchronization
        # This should emit signals that the graph editor and other components can listen to

    def cleanup(self) -> None:
        """Clean up resources and state"""
        self._current_sequence = None
        self._selected_beat = None
        self._selected_beat_index = None
        self._selected_arrow_id = None
        self._is_visible = False

    # IGraphEditorService interface implementation
    def create_graph(self, sequence_data: any) -> any:
        """Create a graph from sequence data."""
        # For now, just store the sequence and return a simple graph representation
        self._current_sequence = sequence_data
        return {
            "id": f"graph_{sequence_data.id if sequence_data else 'unknown'}",
            "sequence": sequence_data,
            "created": True,
        }

    def update_graph(self, graph_id: str, updates: any) -> bool:
        """Update an existing graph."""
        # For now, just update the current sequence if it matches
        try:
            if updates and hasattr(updates, "id") and self._current_sequence:
                if self._current_sequence.id == updates.id:
                    self._current_sequence = updates
                    return True
            return False
        except Exception:
            return False

    def delete_graph(self, graph_id: str) -> bool:
        """Delete a graph."""
        # For now, just clear the current sequence if it matches
        try:
            if (
                self._current_sequence
                and f"graph_{self._current_sequence.id}" == graph_id
            ):
                self._current_sequence = None
                return True
            return False
        except Exception:
            return False

    def get_graph(self, graph_id: str) -> Optional[any]:
        """Get graph by ID."""
        # For now, return the current sequence if it matches
        try:
            if (
                self._current_sequence
                and f"graph_{self._current_sequence.id}" == graph_id
            ):
                return {"id": graph_id, "sequence": self._current_sequence}
            return None
        except Exception:
            return None

    def list_graphs(self) -> list[any]:
        """List all available graphs."""
        # For now, return the current sequence if available
        try:
            if self._current_sequence:
                return [
                    {
                        "id": f"graph_{self._current_sequence.id}",
                        "sequence": self._current_sequence,
                    }
                ]
            return []
        except Exception:
            return []
