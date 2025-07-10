"""
Core service interfaces for Kinetic Constructor.

These interfaces define the contracts for core services, replacing tightly-coupled dependencies.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple

from core.types import Size


class ILayoutService(ABC):
    """
    Unified interface for all layout management operations.

    Consolidates both basic UI layout and advanced layout calculations
    into a single cohesive interface to reduce complexity.
    """

    # Basic UI Layout Methods (formerly ILayoutService)
    @abstractmethod
    def get_main_window_size(self) -> Size:
        """Get the main window size."""

    @abstractmethod
    def get_workbench_size(self) -> Size:
        """Get the workbench area size."""

    @abstractmethod
    def get_picker_size(self) -> Size:
        """Get the option picker size."""

    @abstractmethod
    def get_layout_ratio(self) -> tuple[int, int]:
        """Get the layout ratio (workbench:picker)."""

    @abstractmethod
    def set_layout_ratio(self, ratio: tuple[int, int]) -> None:
        """Set the layout ratio."""

    @abstractmethod
    def calculate_component_size(self, component_type: str, parent_size: Size) -> Size:
        """Calculate component size based on parent and type."""

    # Advanced Layout Methods (formerly ILayoutManagementService)
    @abstractmethod
    def calculate_beat_frame_layout(
        self, sequence: Any, container_size: Tuple[int, int]
    ) -> Dict[str, Any]:
        """Calculate layout for beat frames in a sequence."""

    @abstractmethod
    def calculate_responsive_scaling(
        self, content_size: Tuple[int, int], container_size: Tuple[int, int]
    ) -> float:
        """Calculate responsive scaling factor."""

    @abstractmethod
    def get_optimal_grid_layout(
        self, item_count: int, container_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Get optimal grid layout (rows, cols) for items."""

    @abstractmethod
    def calculate_component_positions(
        self, layout_config: Dict[str, Any]
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate positions for UI components."""


class ISettingsCoordinator(ABC):
    """Interface for settings management."""

    @abstractmethod
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""

    @abstractmethod
    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""

    @abstractmethod
    def save_settings(self) -> None:
        """Save settings to persistent storage."""

    @abstractmethod
    def load_settings(self) -> None:
        """Load settings from persistent storage."""


class ISequenceDataService(ABC):
    """Interface for sequence data management."""

    @abstractmethod
    def get_all_sequences(self) -> List[Dict[str, Any]]:
        """Get all available sequences."""

    @abstractmethod
    def get_sequence_by_id(self, sequence_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific sequence by ID."""

    @abstractmethod
    def save_sequence(self, sequence_data: Dict[str, Any]) -> bool:
        """Save sequence data."""

    @abstractmethod
    def delete_sequence(self, sequence_id: str) -> bool:
        """Delete a sequence."""

    @abstractmethod
    def create_new_sequence(self, name: str) -> Dict[str, Any]:
        """Create a new empty sequence."""


class IValidationService(ABC):
    """Interface for validation services."""

    @abstractmethod
    def validate_sequence(self, sequence_data: Dict[str, Any]) -> bool:
        """Validate a sequence."""

    @abstractmethod
    def validate_beat(self, beat_data: Dict[str, Any]) -> bool:
        """Validate a beat."""

    @abstractmethod
    def validate_motion(self, motion_data: Dict[str, Any]) -> bool:
        """Validate a motion."""

    @abstractmethod
    def get_validation_errors(self, data: Dict[str, Any]) -> List[str]:
        """Get validation errors for data."""


class IArrowManagementService(ABC):
    """Interface for unified arrow management operations."""

    @abstractmethod
    def calculate_arrow_position(
        self, arrow_data: Any, pictograph_data: Any
    ) -> Tuple[float, float, float]:
        """Calculate complete arrow position and rotation."""

    @abstractmethod
    def should_mirror_arrow(self, arrow_data: Any) -> bool:
        """Determine if arrow should be mirrored based on motion type."""

    @abstractmethod
    def apply_beta_positioning(self, beat_data: Any) -> Any:
        """Apply beta prop positioning if needed."""

    @abstractmethod
    def calculate_all_arrow_positions(self, pictograph_data: Any) -> Any:
        """Calculate positions for all arrows in pictograph."""


# IMotionManagementService removed - bridge service eliminated
# Consumers should use focused services directly:
# - IMotionGenerationService for generation
# - IMotionOrientationService for orientation


class ISequenceManager(ABC):
    """Interface for unified sequence management operations."""

    @abstractmethod
    def create_sequence(self, name: str, length: int = 16) -> Any:
        """Create a new sequence with specified length."""

    @abstractmethod
    def add_beat(self, sequence: Any, beat: Any, position: int) -> Any:
        """Add beat to sequence at specified position."""

    @abstractmethod
    def remove_beat(self, sequence: Any, position: int) -> Any:
        """Remove beat from sequence at specified position."""

    @abstractmethod
    def generate_sequence(self, sequence_type: str, length: int, **kwargs) -> Any:
        """Generate sequence using specified algorithm."""

    @abstractmethod
    def apply_workbench_operation(self, sequence: Any, operation: str, **kwargs) -> Any:
        """Apply workbench transformation to sequence."""


class IPictographManager(ABC):
    """Interface for unified pictograph management operations."""

    @abstractmethod
    def create_pictograph(self, grid_mode: Any = None) -> Any:
        """Create a new blank pictograph."""

    @abstractmethod
    def create_from_beat(self, beat_data: Any) -> Any:
        """Create pictograph from beat data."""

    @abstractmethod
    def search_dataset(self, query: Dict[str, Any]) -> List[Any]:
        """Search pictograph dataset with query."""


class IUIStateManager(ABC):
    """Interface for unified UI state management operations."""

    @abstractmethod
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""

    @abstractmethod
    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""

    @abstractmethod
    def get_tab_state(self, tab_name: str) -> Dict[str, Any]:
        """Get state for a specific tab."""

    @abstractmethod
    def toggle_graph_editor(self) -> bool:
        """Toggle graph editor visibility."""


class IPictographContextDetector(ABC):
    """Interface for pictograph context detection and management."""

    @abstractmethod
    def register_context_provider(self, component_id: str, context: Any) -> None:
        """Register a component with its explicit context."""

    @abstractmethod
    def get_context_for_component(self, component_id: str) -> Any:
        """Get the rendering context for a specific component."""

    @abstractmethod
    def determine_context_from_provider(self, provider: Any) -> Any:
        """Determine context from a context provider component."""

    @abstractmethod
    def determine_context_from_scene(self, scene: Any) -> Any:
        """Determine context from a pictograph scene."""


class IPictographBorderManager(ABC):
    """Interface for pictograph border management operations."""

    @abstractmethod
    def calculate_border_width(self, size: int) -> int:
        """Calculate border width based on size using the standard formula."""

    @abstractmethod
    def get_border_adjusted_size(self, original_size: int) -> int:
        """Get size adjusted for border width."""

    @abstractmethod
    def calculate_floating_dimensions(self, view_width: int) -> Any:
        """Calculate floating-point border dimensions for precise drawing."""

    @abstractmethod
    def apply_letter_type_colors(self, letter_type: Any) -> Any:
        """Apply border colors based on letter type."""

    @abstractmethod
    def apply_gold_colors(self) -> Any:
        """Apply gold colors (typically used for hover states)."""

    @abstractmethod
    def apply_custom_colors(self, primary: str, secondary: str) -> Any:
        """Apply custom border colors."""

    @abstractmethod
    def reset_to_original_colors(self) -> Any:
        """Reset border colors to original values."""

    @abstractmethod
    def get_current_colors(self) -> Tuple[str, str]:
        """Get current border colors as (primary, secondary) tuple."""

    @abstractmethod
    def get_current_configuration(self) -> Any:
        """Get current border configuration."""

    @abstractmethod
    def enable_borders(self) -> Any:
        """Enable border rendering."""

    @abstractmethod
    def disable_borders(self) -> Any:
        """Disable border rendering."""

    @abstractmethod
    def set_border_width_percentage(self, percentage: float) -> Any:
        """Set the border width percentage."""

    @abstractmethod
    def validate_configuration(self) -> bool:
        """Validate current border configuration."""


# ILayoutManagementService has been consolidated into ILayoutService above
# This removes the duplicate interface definition to reduce complexity


# Note: IBeatLoadingService was removed during SRP refactoring
# Its functionality was split into focused microservices:
# - OptionPickerDataService for option loading
# - PositionMatchingService for position-based filtering
# - Various specialized services for specific beat operations


class IObjectPoolManager(ABC):
    """Interface for object pool management."""

    @abstractmethod
    def initialize_pool(
        self,
        pool_name: str,
        max_objects: int,
        object_factory: Callable[[], Any],
        progress_callback: Optional[Callable] = None,
    ) -> None:
        """Initialize object pool with progress tracking."""

    @abstractmethod
    def get_pooled_object(self, pool_name: str, index: int) -> Optional[Any]:
        """Get object from pool by index."""

    @abstractmethod
    def reset_pool(self, pool_name: str) -> None:
        """Reset pool state."""
