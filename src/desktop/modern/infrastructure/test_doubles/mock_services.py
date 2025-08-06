"""
Mock service implementations for testing.

These services provide the same interface as production services
but use in-memory storage and simplified logic for fast testing.
"""

from __future__ import annotations

from typing import Any, Optional

# Import service interfaces
from desktop.modern.core.interfaces.core_services import (
    IArrowManagementService,
    ILayoutService,
    IPictographManager,
    ISequenceDataService,
    ISequenceManager,
    ISettingsCoordinator,
    IUIStateManager,
    IValidationService,
)

# Import types
from desktop.modern.core.types import Size


class InMemorySequenceDataService(ISequenceDataService):
    """In-memory sequence data service for testing."""

    def __init__(self):
        self.sequences: dict[str, dict[str, Any]] = {}
        self._id_counter = 0

    def get_all_sequences(self) -> list[dict[str, Any]]:
        """Get all sequences from memory."""
        return list(self.sequences.values())

    def get_sequence_by_id(self, sequence_id: str) -> Optional[dict[str, Any]]:
        """Get sequence by ID."""
        return self.sequences.get(sequence_id)

    def save_sequence(self, sequence_data: dict[str, Any]) -> bool:
        """Save sequence to memory."""
        if "id" not in sequence_data:
            sequence_data["id"] = f"seq_{self._id_counter}"
            self._id_counter += 1

        self.sequences[sequence_data["id"]] = sequence_data
        return True

    def delete_sequence(self, sequence_id: str) -> bool:
        """Delete sequence from memory."""
        if sequence_id in self.sequences:
            del self.sequences[sequence_id]
            return True
        return False

    def create_new_sequence(self, name: str) -> dict[str, Any]:
        """Create new empty sequence."""
        sequence = {
            "id": f"seq_{self._id_counter}",
            "name": name,
            "beats": [],
            "length": 16,
            "created_at": "2024-01-01T00:00:00",
        }
        self._id_counter += 1
        self.sequences[sequence["id"]] = sequence
        return sequence


class MockLayoutService(ILayoutService):
    """Mock layout service with fixed dimensions."""

    def get_main_window_size(self) -> Size:
        """Return fixed window size for tests."""
        return Size(1920, 1080)

    def get_workbench_size(self) -> Size:
        """Return fixed workbench size."""
        return Size(1440, 1080)

    def get_picker_size(self) -> Size:
        """Return fixed picker size."""
        return Size(480, 1080)

    def get_layout_ratio(self) -> tuple[int, int]:
        """Return fixed layout ratio."""
        return (3, 1)

    def set_layout_ratio(self, ratio: tuple[int, int]) -> None:
        """Mock set layout ratio."""

    def calculate_component_size(self, component_type: str, parent_size: Size) -> Size:
        """Calculate component size with simple logic."""
        if component_type == "beat_frame":
            return Size(200, 200)
        if component_type == "pictograph":
            return Size(150, 150)
        return Size(parent_size.width // 2, parent_size.height // 2)

    def calculate_beat_frame_layout(
        self, sequence: Any, container_size: tuple[int, int]
    ) -> dict[str, Any]:
        """Mock beat frame layout calculation."""
        return {
            "grid_size": (4, 4),
            "frame_size": (200, 200),
            "spacing": 10,
            "total_frames": 16,
        }

    def calculate_responsive_scaling(
        self, content_size: tuple[int, int], container_size: tuple[int, int]
    ) -> float:
        """Mock responsive scaling."""
        return 1.0

    def get_optimal_grid_layout(
        self, item_count: int, container_size: tuple[int, int]
    ) -> tuple[int, int]:
        """Mock grid layout calculation."""
        cols = min(4, item_count)
        rows = (item_count + cols - 1) // cols
        return (rows, cols)

    def calculate_component_positions(
        self, layout_config: dict[str, Any]
    ) -> dict[str, tuple[int, int]]:
        """Mock component position calculation."""
        return {"component_1": (0, 0), "component_2": (200, 0), "component_3": (0, 200)}


class InMemorySettingsService(ISettingsCoordinator):
    """In-memory settings service for testing."""

    def __init__(self):
        self.settings: dict[str, Any] = {
            "window_width": 1920,
            "window_height": 1080,
            "layout_ratio": [3, 1],
            "theme": "default",
            "auto_save": True,
        }

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get setting value."""
        return self.settings.get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set setting value."""
        self.settings[key] = value

    def save_settings(self) -> None:
        """Mock save settings (no-op)."""

    def load_settings(self) -> None:
        """Mock load settings (no-op)."""


class MockValidationService(IValidationService):
    """Mock validation service that always passes."""

    def validate_sequence(self, sequence_data: dict[str, Any]) -> bool:
        """Mock sequence validation."""
        return "name" in sequence_data and "beats" in sequence_data

    def validate_beat(self, beat_data: dict[str, Any]) -> bool:
        """Mock beat validation."""
        return True

    def validate_motion(self, motion_data: dict[str, Any]) -> bool:
        """Mock motion validation."""
        return True

    def get_validation_errors(self, data: dict[str, Any]) -> list[str]:
        """Mock validation errors."""
        return []


class MockArrowManagementService(IArrowManagementService):
    """Mock arrow management service."""

    def calculate_arrow_position(
        self, arrow_data: Any, pictograph_data: Any
    ) -> tuple[float, float, float]:
        """Mock arrow position calculation."""
        return (100.0, 100.0, 0.0)

    def should_mirror_arrow(self, arrow_data: Any) -> bool:
        """Mock arrow mirroring logic."""
        return False

    def apply_beta_positioning(self, beat_data: Any) -> Any:
        """Mock beta positioning."""
        return beat_data

    def calculate_all_arrow_positions(self, pictograph_data: Any) -> Any:
        """Mock all arrow positions."""
        return pictograph_data


class MockSequenceManager(ISequenceManager):
    """Mock sequence management service."""

    def __init__(self):
        self.sequences: dict[str, Any] = {}
        self._id_counter = 0

    def create_sequence(self, name: str, length: int = 16) -> Any:
        """Create mock sequence."""
        sequence = {
            "id": f"seq_{self._id_counter}",
            "name": name,
            "length": length,
            "beats": [],
        }
        self._id_counter += 1
        self.sequences[sequence["id"]] = sequence
        return sequence

    def add_beat(self, sequence: Any, beat: Any, position: int) -> Any:
        """Add beat to sequence."""
        if "beats" not in sequence:
            sequence["beats"] = []

        # Extend beats list if necessary
        while len(sequence["beats"]) <= position:
            sequence["beats"].append(None)

        sequence["beats"][position] = beat
        return sequence

    def remove_beat(self, sequence: Any, position: int) -> Any:
        """Remove beat from sequence."""
        if "beats" in sequence and 0 <= position < len(sequence["beats"]):
            sequence["beats"][position] = None
        return sequence

    def generate_sequence(self, sequence_type: str, length: int, **kwargs) -> Any:
        """Generate mock sequence."""
        return self.create_sequence(f"Generated_{sequence_type}", length)

    def apply_workbench_operation(self, sequence: Any, operation: str, **kwargs) -> Any:
        """Apply mock workbench operation."""
        # Mock operation - just return sequence unchanged
        return sequence


class MockPictographManagementService(IPictographManager):
    """Mock pictograph management service."""

    def __init__(self):
        self._id_counter = 0

    def create_pictograph(self, grid_mode: Any = None) -> Any:
        """Create mock pictograph."""
        pictograph = {
            "id": f"picto_{self._id_counter}",
            "grid_mode": grid_mode or "diamond",
            "arrows": [],
            "positions": {},
        }
        self._id_counter += 1
        return pictograph

    def create_from_beat(self, beat_data: Any) -> Any:
        """Create pictograph from beat data."""
        return self.create_pictograph()

    def search_dataset(self, query: dict[str, Any]) -> list[Any]:
        """Mock dataset search."""
        # Return some mock results
        return [
            self.create_pictograph(),
            self.create_pictograph(),
        ]

    def get_pictographs_by_letter(self, letter: str) -> list[Any]:
        """Mock get pictographs by letter."""
        # Return some mock pictographs for any letter
        return [
            self.create_pictograph(),
            self.create_pictograph(),
        ]


class MockUIStateManagementService(IUIStateManager):
    """Mock UI state management service."""

    def __init__(self):
        self.settings: dict[str, Any] = {}
        self.tab_states: dict[str, dict[str, Any]] = {}
        self.graph_editor_visible = False
        self._session_service = None

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get UI setting."""
        return self.settings.get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set UI setting."""
        self.settings[key] = value

    def get_tab_state(self, tab_name: str) -> dict[str, Any]:
        """Get tab state."""
        return self.tab_states.get(tab_name, {})

    def toggle_graph_editor(self) -> bool:
        """Toggle graph editor visibility."""
        self.graph_editor_visible = not self.graph_editor_visible
        return self.graph_editor_visible

    def set_session_service(self, session_service) -> None:
        """Set the session service for integration."""
        self._session_service = session_service

    def update_current_sequence_with_session(
        self, sequence_data, sequence_id: str
    ) -> None:
        """Update current sequence and save to session."""
        self.settings["current_sequence_id"] = sequence_id
        if self._session_service:
            self._session_service.update_current_sequence(sequence_data, sequence_id)

    def update_workbench_selection_with_session(
        self, beat_index, beat_data, start_position
    ) -> None:
        """Update workbench selection and save to session."""
        if beat_index is not None:
            self.settings["selected_beat_index"] = beat_index
        if self._session_service:
            self._session_service.update_workbench_state(
                beat_index, beat_data, start_position
            )

    def set_active_tab(self, tab_name: str) -> None:
        """Set the active tab."""
        self.settings["active_tab"] = tab_name
        if self._session_service:
            self._session_service.update_ui_state(tab_name)

    def get_active_tab(self) -> str:
        """Get the active tab."""
        return self.settings.get("active_tab", "sequence_builder")

    def restore_session_on_startup(self) -> bool:
        """Restore session state on application startup."""
        if not self._session_service:
            return False

        try:
            restore_result = self._session_service.load_session_state()
            if (
                restore_result.success
                and restore_result.session_restored
                and restore_result.session_data
            ):
                session_data = restore_result.session_data

                # Restore UI state from session
                if session_data.active_tab:
                    self.settings["active_tab"] = session_data.active_tab

                return True
            return False
        except Exception:
            return False
