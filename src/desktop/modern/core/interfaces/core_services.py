"""
Core service interfaces for Kinetic Constructor.

These interfaces define the contracts for core services, replacing tightly-coupled dependencies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from desktop.modern.core.types import Size


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer


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
        self, sequence: Any, container_size: tuple[int, int]
    ) -> dict[str, Any]:
        """Calculate layout for beat frames in a sequence."""

    @abstractmethod
    def calculate_responsive_scaling(
        self, content_size: tuple[int, int], container_size: tuple[int, int]
    ) -> float:
        """Calculate responsive scaling factor."""

    @abstractmethod
    def get_optimal_grid_layout(
        self, item_count: int, container_size: tuple[int, int]
    ) -> tuple[int, int]:
        """Get optimal grid layout (rows, cols) for items."""

    @abstractmethod
    def calculate_component_positions(
        self, layout_config: dict[str, Any]
    ) -> dict[str, tuple[int, int]]:
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
    def update_setting(self, key: str, value: Any) -> None:
        """Update a setting value (alias for set_setting for UI compatibility)."""

    @abstractmethod
    def add_change_listener(self, listener: Callable[[str, Any], None]) -> None:
        """Add a listener for setting changes."""

    @abstractmethod
    def remove_change_listener(self, listener: Callable[[str, Any], None]) -> None:
        """Remove a listener for setting changes."""

    @abstractmethod
    def get_all_settings(self) -> dict[str, Any]:
        """Get all settings."""

    @abstractmethod
    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""

    @abstractmethod
    def save_settings(self) -> bool:
        """Save settings to persistent storage."""

    @abstractmethod
    def load_settings(self) -> bool:
        """Load settings from persistent storage."""


class ISequenceDataService(ABC):
    """Interface for sequence data management."""

    @abstractmethod
    def get_all_sequences(self) -> list[dict[str, Any]]:
        """Get all available sequences."""

    @abstractmethod
    def get_sequence_by_id(self, sequence_id: str) -> dict[str, Any] | None:
        """Get a specific sequence by ID."""

    @abstractmethod
    def save_sequence(self, sequence_data: dict[str, Any]) -> bool:
        """Save sequence data."""

    @abstractmethod
    def delete_sequence(self, sequence_id: str) -> bool:
        """Delete a sequence."""

    @abstractmethod
    def create_new_sequence(self, name: str) -> dict[str, Any]:
        """Create a new empty sequence."""


class IValidationService(ABC):
    """Interface for validation services."""

    @abstractmethod
    def validate_sequence(self, sequence_data: dict[str, Any]) -> bool:
        """Validate a sequence."""

    @abstractmethod
    def validate_beat(self, beat_data: dict[str, Any]) -> bool:
        """Validate a beat."""

    @abstractmethod
    def validate_motion(self, motion_data: dict[str, Any]) -> bool:
        """Validate a motion."""

    @abstractmethod
    def get_validation_errors(self, data: dict[str, Any]) -> list[str]:
        """Get validation errors for data."""


class IArrowManagementService(ABC):
    """Interface for unified arrow management operations."""

    @abstractmethod
    def calculate_arrow_position(
        self, arrow_data: Any, pictograph_data: Any
    ) -> tuple[float, float, float]:
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
    def search_dataset(self, query: dict[str, Any]) -> list[Any]:
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
    def get_tab_state(self, tab_name: str) -> dict[str, Any]:
        """Get state for a specific tab."""

    @abstractmethod
    def get_all_settings(self) -> dict[str, Any]:
        """Get all settings."""

    @abstractmethod
    def clear_settings(self) -> None:
        """Clear all settings."""

    @abstractmethod
    def save_state(self) -> None:
        """Save current state to persistent storage."""

    @abstractmethod
    def load_state(self) -> None:
        """Load state from persistent storage."""

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
    def get_current_colors(self) -> tuple[str, str]:
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


class IObjectPoolService(ABC):
    """Alias for IObjectPoolManager for backward compatibility."""

    @abstractmethod
    def initialize_pool(
        self,
        pool_name: str,
        max_objects: int,
        object_factory: Callable[[], Any],
        progress_callback: Callable | None = None,
    ) -> None:
        """Initialize object pool with progress tracking."""

    @abstractmethod
    def get_pooled_object(self, pool_name: str, index: int) -> Any | None:
        """Get object from pool by index."""


class IUIStateManagementService(ABC):
    """Interface for UI state management operations."""

    @abstractmethod
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""

    @abstractmethod
    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""

    @abstractmethod
    def get_tab_state(self, tab_name: str) -> dict[str, Any]:
        """Get state for a specific tab."""

    @abstractmethod
    def set_tab_state(self, tab_name: str, state: dict[str, Any]) -> None:
        """Set state for a specific tab."""

    @abstractmethod
    def toggle_graph_editor(self) -> bool:
        """Toggle graph editor visibility."""

    @abstractmethod
    def save_state(self) -> None:
        """Save current UI state to persistent storage."""

    @abstractmethod
    def load_state(self) -> None:
        """Load UI state from persistent storage."""


class IDataServiceRegistrar(ABC):
    """
    Interface for data service registrars.

    Handles registration of data management services following microservices architecture.
    """

    @abstractmethod
    def register_services(self, container: DIContainer) -> None:
        """Register all data services in the DI container."""

    @abstractmethod
    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""

    @abstractmethod
    def get_registered_services(self) -> list[str]:
        """Get list of service names registered by this registrar."""

    @abstractmethod
    def is_critical(self) -> bool:
        """Return True if this registrar's services are critical for application startup."""

    @abstractmethod
    def get_service_availability(self) -> dict[str, bool]:
        """Get availability status of services in this domain."""


class IAssetManager(ABC):
    """
    Interface for asset management operations.

    Manages SVG assets, file paths, and color transformations for pictograph rendering.
    """

    @abstractmethod
    def get_arrow_svg_path(self, motion_data: Any, color: str) -> str:
        """Generate SVG file path for arrow assets based on motion type and color."""

    @abstractmethod
    def get_fallback_arrow_svg_path(self, motion_data: Any) -> str:
        """Generate fallback SVG file path for original (non-colored) arrow assets."""

    @abstractmethod
    def get_prop_asset_path(self, prop_type: str, color: str | None = None) -> str:
        """Get asset path for prop (hand) assets."""

    @abstractmethod
    def svg_path_exists(self, path: str) -> bool:
        """Check if SVG file exists at the given path."""

    @abstractmethod
    def apply_color_transformation(self, svg_data: str, color: str) -> str:
        """Apply color transformation to SVG data."""

    @abstractmethod
    def load_and_cache_asset(self, path: str) -> str:
        """Load and cache SVG asset with proper error handling."""

    @abstractmethod
    def get_cache_stats(self) -> dict[str, int]:
        """Get cache statistics for monitoring."""

    @abstractmethod
    def clear_cache(self) -> None:
        """Clear the SVG asset cache."""

    @abstractmethod
    def get_cache_info(self) -> str:
        """Get comprehensive cache information."""


class ISessionRestorationCoordinator(ABC):
    """Interface for session restoration coordination."""

    @abstractmethod
    def load_and_prepare_session(self, session_service) -> Any | None:
        """Load and prepare session data for restoration."""

    @abstractmethod
    def trigger_deferred_restoration(self, session_data: Any) -> None:
        """Trigger deferred session restoration after UI components are ready."""

    @abstractmethod
    def trigger_deferred_restoration_if_pending(self) -> None:
        """Trigger deferred session restoration if there's pending data."""


class IBeatResizer(ABC):
    """Interface for beat resizing operations."""

    @abstractmethod
    def resize_beat(self, beat_data: Any, new_size: tuple[int, int]) -> Any:
        """Resize beat to new dimensions."""

    @abstractmethod
    def calculate_optimal_size(
        self, beat_data: Any, container_size: tuple[int, int]
    ) -> tuple[int, int]:
        """Calculate optimal size for beat within container."""

    @abstractmethod
    def validate_size_constraints(self, size: tuple[int, int]) -> bool:
        """Validate size constraints."""


class IComponentSizer(ABC):
    """Interface for component sizing operations."""

    @abstractmethod
    def calculate_component_size(
        self, component_type: str, content_size: tuple[int, int]
    ) -> tuple[int, int]:
        """Calculate component size based on content."""

    @abstractmethod
    def get_size_constraints(self, component_type: str) -> dict[str, Any]:
        """Get size constraints for component type."""

    @abstractmethod
    def apply_responsive_sizing(
        self, base_size: tuple[int, int], viewport_size: tuple[int, int]
    ) -> tuple[int, int]:
        """Apply responsive sizing rules."""


class IDimensionCalculator(ABC):
    """Interface for dimension calculation operations."""

    @abstractmethod
    def calculate_dimensions(
        self, content: Any, constraints: dict[str, Any]
    ) -> tuple[int, int]:
        """Calculate dimensions for content with constraints."""

    @abstractmethod
    def get_aspect_ratio(self, dimensions: tuple[int, int]) -> float:
        """Get aspect ratio from dimensions."""

    @abstractmethod
    def scale_dimensions(
        self, dimensions: tuple[int, int], scale_factor: float
    ) -> tuple[int, int]:
        """Scale dimensions by factor."""


class IFramePoolService(ABC):
    """Interface for frame pool service operations."""

    @abstractmethod
    def initialize_pool(self, pool_size: int) -> None:
        """Initialize frame pool with specified size."""

    @abstractmethod
    def get_frame(self, index: int) -> Any | None:
        """Get frame from pool by index."""

    @abstractmethod
    def return_frame(self, frame: Any) -> None:
        """Return frame to pool."""

    @abstractmethod
    def get_pool_size(self) -> int:
        """Get current pool size."""

    @abstractmethod
    def is_initialized(self) -> bool:
        """Check if pool is initialized."""
