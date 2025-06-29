"""
Mock service implementations for testing.

These services provide the same interface as production services
but use in-memory storage and simplified logic for fast testing.
"""

from typing import List, Optional, Dict, Any, Tuple

# Import service interfaces
from core.interfaces.core_services import (
    ILayoutService,
    ISettingsService,
    ISequenceDataService,
    IValidationService,
    IArrowManagementService,
    ISequenceManagementService,
    IPictographManagementService,
    IUIStateManagementService,
)

# Import types
from core.types import Size


class InMemorySequenceDataService(ISequenceDataService):
    """In-memory sequence data service for testing."""

    def __init__(self):
        self.sequences: Dict[str, Dict[str, Any]] = {}
        self._id_counter = 0

    def get_all_sequences(self) -> List[Dict[str, Any]]:
        """Get all sequences from memory."""
        return list(self.sequences.values())

    def get_sequence_by_id(self, sequence_id: str) -> Optional[Dict[str, Any]]:
        """Get sequence by ID."""
        return self.sequences.get(sequence_id)

    def save_sequence(self, sequence_data: Dict[str, Any]) -> bool:
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

    def create_new_sequence(self, name: str) -> Dict[str, Any]:
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
        pass

    def calculate_component_size(self, component_type: str, parent_size: Size) -> Size:
        """Calculate component size with simple logic."""
        if component_type == "beat_frame":
            return Size(200, 200)
        elif component_type == "pictograph":
            return Size(150, 150)
        else:
            return Size(parent_size.width // 2, parent_size.height // 2)

    def calculate_beat_frame_layout(
        self, sequence: Any, container_size: Tuple[int, int]
    ) -> Dict[str, Any]:
        """Mock beat frame layout calculation."""
        return {
            "grid_size": (4, 4),
            "frame_size": (200, 200),
            "spacing": 10,
            "total_frames": 16,
        }

    def calculate_responsive_scaling(
        self, content_size: Tuple[int, int], container_size: Tuple[int, int]
    ) -> float:
        """Mock responsive scaling."""
        return 1.0

    def get_optimal_grid_layout(
        self, item_count: int, container_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Mock grid layout calculation."""
        cols = min(4, item_count)
        rows = (item_count + cols - 1) // cols
        return (rows, cols)

    def calculate_component_positions(
        self, layout_config: Dict[str, Any]
    ) -> Dict[str, Tuple[int, int]]:
        """Mock component position calculation."""
        return {"component_1": (0, 0), "component_2": (200, 0), "component_3": (0, 200)}


class InMemorySettingsService(ISettingsService):
    """In-memory settings service for testing."""

    def __init__(self):
        self.settings: Dict[str, Any] = {
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
        pass

    def load_settings(self) -> None:
        """Mock load settings (no-op)."""
        pass


class MockValidationService(IValidationService):
    """Mock validation service that always passes."""

    def validate_sequence(self, sequence_data: Dict[str, Any]) -> bool:
        """Mock sequence validation."""
        return "name" in sequence_data and "beats" in sequence_data

    def validate_beat(self, beat_data: Dict[str, Any]) -> bool:
        """Mock beat validation."""
        return True

    def validate_motion(self, motion_data: Dict[str, Any]) -> bool:
        """Mock motion validation."""
        return True

    def get_validation_errors(self, data: Dict[str, Any]) -> List[str]:
        """Mock validation errors."""
        return []


class MockArrowManagementService(IArrowManagementService):
    """Mock arrow management service."""

    def calculate_arrow_position(
        self, arrow_data: Any, pictograph_data: Any
    ) -> Tuple[float, float, float]:
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


class MockSequenceManagementService(ISequenceManagementService):
    """Mock sequence management service."""

    def __init__(self):
        self.sequences: Dict[str, Any] = {}
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


class MockPictographManagementService(IPictographManagementService):
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

    def search_dataset(self, query: Dict[str, Any]) -> List[Any]:
        """Mock dataset search."""
        # Return some mock results
        return [
            self.create_pictograph(),
            self.create_pictograph(),
        ]

    def get_pictographs_by_letter(self, letter: str) -> List[Any]:
        """Mock get pictographs by letter."""
        # Return some mock pictographs for any letter
        return [
            self.create_pictograph(),
            self.create_pictograph(),
        ]


class MockUIStateManagementService(IUIStateManagementService):
    """Mock UI state management service."""

    def __init__(self):
        self.settings: Dict[str, Any] = {}
        self.tab_states: Dict[str, Dict[str, Any]] = {}
        self.graph_editor_visible = False

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get UI setting."""
        return self.settings.get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set UI setting."""
        self.settings[key] = value

    def get_tab_state(self, tab_name: str) -> Dict[str, Any]:
        """Get tab state."""
        return self.tab_states.get(tab_name, {})

    def toggle_graph_editor(self) -> bool:
        """Toggle graph editor visibility."""
        self.graph_editor_visible = not self.graph_editor_visible
        return self.graph_editor_visible
