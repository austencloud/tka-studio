"""
Headless service implementations.

These services provide real business logic but without UI components.
Perfect for server-side processing or CI/CD environments.
"""

from typing import Any

from desktop.modern.core.interfaces.core_services import ILayoutService, IUIStateManager
from desktop.modern.core.types import Size


class HeadlessLayoutService(ILayoutService):
    """Headless layout service that calculates layouts without UI."""

    def __init__(self):
        self.window_size = Size(1920, 1080)
        self.layout_ratio = (3, 1)

    def get_main_window_size(self) -> Size:
        """Return configured window size."""
        return self.window_size

    def get_workbench_size(self) -> Size:
        """Calculate workbench size based on ratio."""
        total_parts = sum(self.layout_ratio)
        workbench_width = int(
            self.window_size.width * self.layout_ratio[0] / total_parts
        )
        return Size(workbench_width, self.window_size.height)

    def get_picker_size(self) -> Size:
        """Calculate picker size based on ratio."""
        total_parts = sum(self.layout_ratio)
        picker_width = int(self.window_size.width * self.layout_ratio[1] / total_parts)
        return Size(picker_width, self.window_size.height)

    def get_layout_ratio(self) -> tuple[int, int]:
        """Get current layout ratio."""
        return self.layout_ratio

    def set_layout_ratio(self, ratio: tuple[int, int]) -> None:
        """Set layout ratio."""
        self.layout_ratio = ratio

    def calculate_component_size(self, component_type: str, parent_size: Size) -> Size:
        """Calculate component size with real logic."""
        if component_type == "beat_frame":
            # Real calculation for beat frames
            grid_cols = 4
            grid_rows = 4
            available_width = parent_size.width - 40  # padding
            available_height = parent_size.height - 40

            frame_width = available_width // grid_cols - 10  # spacing
            frame_height = available_height // grid_rows - 10

            return Size(frame_width, frame_height)

        elif component_type == "pictograph":
            # Real calculation for pictographs
            return Size(150, 150)

        else:
            # Default calculation
            return Size(parent_size.width // 2, parent_size.height // 2)

    def calculate_beat_frame_layout(
        self, sequence: Any, container_size: tuple[int, int]
    ) -> dict[str, Any]:
        """Calculate real beat frame layout."""
        sequence_length = getattr(sequence, "length", 16)
        container_width, container_height = container_size

        # Calculate optimal grid
        cols = min(4, sequence_length)
        rows = (sequence_length + cols - 1) // cols

        # Calculate frame size
        available_width = container_width - 40  # padding
        available_height = container_height - 40

        frame_width = (available_width - (cols - 1) * 10) // cols  # spacing
        frame_height = (available_height - (rows - 1) * 10) // rows

        return {
            "grid_size": (rows, cols),
            "frame_size": (frame_width, frame_height),
            "spacing": 10,
            "total_frames": sequence_length,
            "container_size": container_size,
        }

    def calculate_responsive_scaling(
        self, content_size: tuple[int, int], container_size: tuple[int, int]
    ) -> float:
        """Calculate real responsive scaling."""
        content_width, content_height = content_size
        container_width, container_height = container_size

        # Calculate scale to fit both dimensions
        width_scale = container_width / content_width
        height_scale = container_height / content_height

        # Use the smaller scale to ensure content fits
        return min(width_scale, height_scale, 1.0)  # Don't scale up beyond 1.0

    def get_optimal_grid_layout(
        self, item_count: int, container_size: tuple[int, int]
    ) -> tuple[int, int]:
        """Calculate optimal grid layout."""
        if item_count <= 0:
            return (0, 0)

        container_width, container_height = container_size
        aspect_ratio = container_width / container_height

        # Try different column counts and find the best fit
        best_cols = 1
        best_efficiency = 0

        for cols in range(1, item_count + 1):
            rows = (item_count + cols - 1) // cols
            grid_ratio = cols / rows

            # Efficiency is how well the grid matches container aspect ratio
            efficiency = min(aspect_ratio / grid_ratio, grid_ratio / aspect_ratio)

            if efficiency > best_efficiency:
                best_efficiency = efficiency
                best_cols = cols

        best_rows = (item_count + best_cols - 1) // best_cols
        return (best_rows, best_cols)

    def calculate_component_positions(
        self, layout_config: dict[str, Any]
    ) -> dict[str, tuple[int, int]]:
        """Calculate real component positions."""
        positions = {}

        grid_size = layout_config.get("grid_size", (4, 4))
        frame_size = layout_config.get("frame_size", (200, 200))
        spacing = layout_config.get("spacing", 10)

        rows, cols = grid_size
        frame_width, frame_height = frame_size

        component_index = 0
        for row in range(rows):
            for col in range(cols):
                x = col * (frame_width + spacing)
                y = row * (frame_height + spacing)
                positions[f"component_{component_index}"] = (x, y)
                component_index += 1

        return positions


class HeadlessUIStateManagementService(IUIStateManager):
    """Headless UI state management without actual UI."""

    def __init__(self):
        self.settings: dict[str, Any] = {
            "theme": "default",
            "auto_save": True,
            "last_sequence": None,
        }
        self.tab_states: dict[str, dict[str, Any]] = {
            "sequence_builder": {"active": True, "scroll_position": 0},
            "pictograph_editor": {"active": False, "selected_pictograph": None},
            "animation_player": {"active": False, "playing": False},
        }
        self.graph_editor_visible = False

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get UI setting."""
        return self.settings.get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set UI setting."""
        self.settings[key] = value

    def get_tab_state(self, tab_name: str) -> dict[str, Any]:
        """Get tab state."""
        if tab_name not in self.tab_states:
            self.tab_states[tab_name] = {"active": False}
        return self.tab_states[tab_name].copy()

    def toggle_graph_editor(self) -> bool:
        """Toggle graph editor visibility."""
        self.graph_editor_visible = not self.graph_editor_visible
        return self.graph_editor_visible
