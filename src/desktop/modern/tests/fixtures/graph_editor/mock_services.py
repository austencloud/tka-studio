#!/usr/bin/env python3
"""
Mock Services for Graph Editor Testing
=====================================

Provides comprehensive mock services for testing graph editor components
following TKA architecture patterns and testing protocols.
"""
from __future__ import annotations

from pathlib import Path
import sys
from typing import Any
from unittest.mock import Mock


# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))

from domain.models import BeatData, SequenceData


class MockGraphEditorService:
    """
    Mock implementation of IGraphEditorService for testing.

    Provides predictable behavior for testing graph editor components
    without requiring full service infrastructure.
    """

    def __init__(self):
        self._selected_beat: BeatData | None = None
        self._selected_beat_index: int | None = None
        self._current_sequence: SequenceData | None = None
        self._selected_arrow_id: str | None = None

        # Track method calls for verification
        self.method_calls: list[dict[str, Any]] = []

    def get_selected_beat(self) -> BeatData | None:
        """Get the currently selected beat."""
        self._record_call("get_selected_beat")
        return self._selected_beat

    def set_selected_beat(self, beat_data: BeatData, beat_index: int) -> None:
        """Set the selected beat."""
        self._record_call(
            "set_selected_beat", beat_data=beat_data, beat_index=beat_index
        )
        self._selected_beat = beat_data
        self._selected_beat_index = beat_index

    def get_current_sequence(self) -> SequenceData | None:
        """Get the current sequence."""
        self._record_call("get_current_sequence")
        return self._current_sequence

    def update_graph_display(self, sequence_data: SequenceData) -> None:
        """Update the graph display with sequence data."""
        self._record_call("update_graph_display", sequence_data=sequence_data)
        self._current_sequence = sequence_data

    def apply_turn_adjustment(
        self, beat_data: BeatData, arrow_color: str, new_turns: float
    ) -> bool:
        """Apply turn adjustment to beat data."""
        self._record_call(
            "apply_turn_adjustment",
            beat_data=beat_data,
            arrow_color=arrow_color,
            new_turns=new_turns,
        )
        return True

    def apply_orientation_adjustment(
        self, beat_data: BeatData, arrow_color: str, orientation: str
    ) -> bool:
        """Apply orientation adjustment to beat data."""
        self._record_call(
            "apply_orientation_adjustment",
            beat_data=beat_data,
            arrow_color=arrow_color,
            orientation=orientation,
        )
        return True

    def set_arrow_selection(self, arrow_id: str) -> None:
        """Set the selected arrow."""
        self._record_call("set_arrow_selection", arrow_id=arrow_id)
        self._selected_arrow_id = arrow_id

    def get_selected_arrow_id(self) -> str | None:
        """Get the selected arrow ID."""
        self._record_call("get_selected_arrow_id")
        return self._selected_arrow_id

    def _record_call(self, method_name: str, **kwargs) -> None:
        """Record method call for verification."""
        self.method_calls.append(
            {
                "method": method_name,
                "args": kwargs,
                "call_count": len(
                    [c for c in self.method_calls if c["method"] == method_name]
                )
                + 1,
            }
        )

    def reset_calls(self) -> None:
        """Reset method call tracking."""
        self.method_calls.clear()

    def get_call_count(self, method_name: str) -> int:
        """Get the number of times a method was called."""
        return len([c for c in self.method_calls if c["method"] == method_name])

    def was_called_with(self, method_name: str, **expected_kwargs) -> bool:
        """Check if method was called with specific arguments."""
        for call in self.method_calls:
            if call["method"] == method_name:
                if all(call["args"].get(k) == v for k, v in expected_kwargs.items()):
                    return True
        return False


class MockDataFlowService:
    """Mock data flow service for testing signal coordination."""

    def __init__(self):
        # Create mock signals
        self.beat_data_updated = Mock()
        self.pictograph_refresh_needed = Mock()
        self.sequence_modified = Mock()
        self.panel_mode_changed = Mock()

        self._current_sequence: SequenceData | None = None
        self._selected_beat_index: int | None = None

    def set_context(self, sequence_data: SequenceData, beat_index: int) -> None:
        """Set the current context."""
        self._current_sequence = sequence_data
        self._selected_beat_index = beat_index

    def process_turn_change(
        self, beat_data: BeatData, arrow_color: str, new_turns: float
    ) -> BeatData:
        """Process turn change and return updated beat."""
        # Create updated beat data
        if arrow_color == "blue" and beat_data.blue_motion:
            updated_motion = beat_data.blue_motion.update(turns=new_turns)
            updated_beat = beat_data.update(blue_motion=updated_motion)
        elif arrow_color == "red" and beat_data.red_motion:
            updated_motion = beat_data.red_motion.update(turns=new_turns)
            updated_beat = beat_data.update(red_motion=updated_motion)
        else:
            updated_beat = beat_data

        # Emit signals
        self.beat_data_updated.emit(updated_beat, self._selected_beat_index or 0)
        self.pictograph_refresh_needed.emit(updated_beat)
        self.sequence_modified.emit()

        return updated_beat

    def process_orientation_change(
        self, beat_data: BeatData, arrow_color: str, orientation: str
    ) -> BeatData:
        """Process orientation change and return updated beat."""
        # Simple mock implementation
        self.beat_data_updated.emit(beat_data, self._selected_beat_index or 0)
        return beat_data

    def determine_panel_mode(self, beat_data: BeatData | None) -> str:
        """Determine panel mode based on beat data."""
        if beat_data is None:
            return "orientation"
        if hasattr(beat_data, "metadata") and beat_data.metadata.get(
            "is_start_position"
        ):
            return "orientation"
        return "turns"


class MockHotkeyService:
    """Mock hotkey service for testing keyboard interactions."""

    def __init__(self):
        # Create mock signals
        self.arrow_moved = Mock()
        self.rotation_override_requested = Mock()
        self.special_placement_removal_requested = Mock()
        self.prop_placement_override_requested = Mock()

        self.graph_service = MockGraphEditorService()

    def handle_key_event(self, key_event) -> bool:
        """Handle key event and return whether it was handled."""
        # Mock implementation that always returns True
        return True

    def set_selected_arrow(self, arrow_id: str) -> None:
        """Set the selected arrow for hotkey operations."""
        pass


def create_mock_graph_editor_service() -> MockGraphEditorService:
    """Factory function to create mock graph editor service."""
    return MockGraphEditorService()


def create_mock_data_flow_service() -> MockDataFlowService:
    """Factory function to create mock data flow service."""
    return MockDataFlowService()


def create_mock_hotkey_service() -> MockHotkeyService:
    """Factory function to create mock hotkey service."""
    return MockHotkeyService()


# Convenience function for creating all mock services
def create_all_mock_services() -> dict[str, Any]:
    """Create all mock services needed for graph editor testing."""
    return {
        "graph_service": create_mock_graph_editor_service(),
        "data_flow_service": create_mock_data_flow_service(),
        "hotkey_service": create_mock_hotkey_service(),
    }
