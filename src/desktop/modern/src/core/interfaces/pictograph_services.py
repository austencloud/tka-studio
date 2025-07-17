"""
Pictograph Service Interfaces

Interface definitions for pictograph-related services following TKA's clean architecture.
These interfaces define contracts for validation, scaling, and pictograph manipulation services.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from domain.models.pictograph_data import PictographData
from PyQt6.QtCore import QSize


class ScalingContext(Enum):
    """Different contexts where pictographs are displayed, each with specific scaling needs."""

    OPTION_VIEW = "option_view"
    START_POS_PICKER = "start_pos_picker"
    ADVANCED_START_POS = "advanced_start_pos"
    CODEX_VIEW = "codex_view"
    BEAT_VIEW = "beat_view"
    GRAPH_EDITOR_VIEW = "graph_editor_view"
    DEFAULT = "default"


class RenderingContext(Enum):
    """Different contexts where pictographs are rendered, affecting arrow behavior."""

    GRAPH_EDITOR = "graph_editor"
    BEAT_FRAME = "beat_frame"
    OPTION_PICKER = "option_picker"
    PREVIEW = "preview"
    SEQUENCE_VIEWER = "sequence_viewer"
    UNKNOWN = "unknown"


class IPictographValidator(ABC):
    """
    Interface for pictograph validation and condition checking.

    Provides methods to validate pictograph properties, orientation conditions,
    layer configurations, and letter conditions following TKA's validation rules.
    """

    @abstractmethod
    def validate_dependencies(self) -> bool:
        """
        Validate that all required dependencies are available.

        Returns:
            bool: True if dependencies are valid, False otherwise
        """

    @abstractmethod
    def ends_with_beta(self) -> bool:
        """
        Check if pictograph ends with beta position.

        Returns:
            bool: True if pictograph ends with beta position
        """

    @abstractmethod
    def ends_with_alpha(self) -> bool:
        """
        Check if pictograph ends with alpha position.

        Returns:
            bool: True if pictograph ends with alpha position
        """

    @abstractmethod
    def ends_with_gamma(self) -> bool:
        """
        Check if pictograph ends with gamma position.

        Returns:
            bool: True if pictograph ends with gamma position
        """

    @abstractmethod
    def ends_with_layer3(self) -> bool:
        """
        Check if pictograph ends with layer3 configuration.

        Returns:
            bool: True if pictograph has layer3 configuration
        """

    @abstractmethod
    def ends_with_radial_ori(self) -> bool:
        """
        Check if pictograph has radial orientation properties.

        Returns:
            bool: True if all props are radial (IN/OUT orientations)
        """

    @abstractmethod
    def ends_with_layer1(self) -> bool:
        """
        Check if pictograph ends with layer1 configuration.

        Returns:
            bool: True if both props have same radial/nonradial orientation
        """

    @abstractmethod
    def ends_with_layer2(self) -> bool:
        """
        Check if pictograph ends with layer2 configuration.

        Returns:
            bool: True if both props are nonradial
        """

    @abstractmethod
    def ends_with_nonradial_ori(self) -> bool:
        """
        Check if pictograph has non-radial orientation properties.

        Returns:
            bool: True if all props are nonradial (CLOCK/COUNTER orientations)
        """


class IScalingService(ABC):
    """
    Interface for context-aware pictograph scaling calculations.

    Provides methods to calculate appropriate scaling factors for pictographs
    in different display contexts, maintaining visual consistency across the application.
    """

    @abstractmethod
    def calculate_scale(
        self,
        context: ScalingContext,
        container_size: QSize,
        scene_size: QSize,
        **context_params,
    ) -> Tuple[float, float]:
        """
        Calculate scale factors for a pictograph in a specific context.

        Args:
            context: The scaling context (enum)
            container_size: Size of the container widget
            scene_size: Size of the pictograph scene
            **context_params: Additional context-specific parameters

        Returns:
            Tuple of (scale_x, scale_y) factors
        """

    @abstractmethod
    def get_responsive_border_width(self, target_size: int) -> int:
        """
        Calculate responsive border width based on target size.

        Args:
            target_size: Target size for the pictograph

        Returns:
            int: Calculated border width
        """

    @abstractmethod
    def validate_scaling_context(self, context: ScalingContext) -> bool:
        """
        Validate that the scaling context is supported.

        Args:
            context: The scaling context to validate

        Returns:
            bool: True if context is supported, False otherwise
        """

    @abstractmethod
    def get_minimum_size_for_context(self, context: ScalingContext) -> int:
        """
        Get the minimum size for a specific context.

        Args:
            context: The scaling context

        Returns:
            int: Minimum size for the context
        """


class AnalysisType(Enum):
    """Analysis type enumeration."""

    STRUCTURE = "structure"
    SIMILARITY = "similarity"
    COMPLEXITY = "complexity"
    FREQUENCY = "frequency"


class IAnalyzer(ABC):
    """Interface for pictograph analyzer operations."""

    @abstractmethod
    def analyze_pictograph(
        self, pictograph_data: Dict[str, Any], analysis_type: AnalysisType
    ) -> Dict[str, Any]:
        """
        Analyze pictograph data.

        Args:
            pictograph_data: Pictograph data to analyze
            analysis_type: Type of analysis to perform

        Returns:
            Analysis results dictionary

        Note:
            Web implementation: Same analysis logic across platforms
        """
        pass

    @abstractmethod
    def compare_pictographs(
        self, pictograph1: Dict[str, Any], pictograph2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compare two pictographs.

        Args:
            pictograph1: First pictograph data
            pictograph2: Second pictograph data

        Returns:
            Comparison results dictionary

        Note:
            Web implementation: Same comparison logic across platforms
        """
        pass

    @abstractmethod
    def get_analysis_metrics(self, pictograph_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Get analysis metrics for pictograph.

        Args:
            pictograph_data: Pictograph data to analyze

        Returns:
            Dictionary of metric names to values

        Note:
            Web implementation: Same metrics calculation across platforms
        """
        pass


class IPictographContextProvider(ABC):
    """Interface for pictograph context provider operations."""

    @abstractmethod
    def get_context(self, pictograph_id: str) -> Optional[Dict[str, Any]]:
        """
        Get context for a pictograph.

        Args:
            pictograph_id: ID of pictograph to get context for

        Returns:
            Context dictionary or None if not found

        Note:
            Web implementation: Retrieved from browser storage or server
        """
        pass


class IPictographVisibilityManager(ABC):
    """Interface for pictograph visibility manager operations."""

    @abstractmethod
    def set_pictograph_visibility(self, pictograph_id: str, visible: bool) -> None:
        """
        Set visibility for a pictograph.

        Args:
            pictograph_id: ID of pictograph to set visibility for
            visible: Visibility state

        Note:
            Web implementation: Updates CSS display/visibility properties
        """
        pass

    @abstractmethod
    def get_pictograph_visibility(self, pictograph_id: str) -> bool:
        """
        Get visibility state for a pictograph.

        Args:
            pictograph_id: ID of pictograph to check

        Returns:
            True if visible, False otherwise

        Note:
            Web implementation: Checks CSS display/visibility properties
        """
        pass

    @abstractmethod
    def toggle_pictograph_visibility(self, pictograph_id: str) -> bool:
        """
        Toggle visibility for a pictograph.

        Args:
            pictograph_id: ID of pictograph to toggle

        Returns:
            New visibility state

        Note:
            Web implementation: Toggles CSS display/visibility properties
        """
        pass

    @abstractmethod
    def set_category_visibility(self, category: str, visible: bool) -> None:
        """
        Set visibility for all pictographs in a category.

        Args:
            category: Category name
            visible: Visibility state

        Note:
            Web implementation: Updates CSS for all pictographs in category
        """
        pass

    @abstractmethod
    def get_category_visibility(self, category: str) -> bool:
        """
        Get visibility state for a category.

        Args:
            category: Category name

        Returns:
            True if category is visible, False otherwise
        """
        pass

    @abstractmethod
    def get_all_visibility_states(self) -> Dict[str, bool]:
        """
        Get visibility states for all pictographs.

        Returns:
            Dictionary mapping pictograph IDs to visibility states

        Note:
            Web implementation: Retrieved from DOM or state management
        """
        pass

    @abstractmethod
    def save_visibility_configuration(self, config_name: str) -> bool:
        """
        Save current visibility configuration.

        Args:
            config_name: Name for saved configuration

        Returns:
            True if saved successfully, False otherwise

        Note:
            Web implementation: Saves to browser storage
        """
        pass

    @abstractmethod
    def load_visibility_configuration(self, config_name: str) -> bool:
        """
        Load a saved visibility configuration.

        Args:
            config_name: Name of configuration to load

        Returns:
            True if loaded successfully, False otherwise

        Note:
            Web implementation: Loads from browser storage
        """
        pass

    @abstractmethod
    def get_visibility_configurations(self) -> List[str]:
        """
        Get list of saved visibility configurations.

        Returns:
            List of configuration names

        Note:
            Web implementation: Retrieved from browser storage
        """
        pass

    @abstractmethod
    def reset_visibility_to_defaults(self) -> None:
        """
        Reset all visibility states to defaults.

        Note:
            Web implementation: Resets CSS and state to default values
        """
        pass


class IPictographPositionMatcher(ABC):
    """Interface for pictograph position matcher operations."""

    @abstractmethod
    def match_position(
        self, pictograph_data: Dict[str, Any], position_criteria: Dict[str, Any]
    ) -> Optional[str]:
        """
        Match pictograph position to criteria.

        Args:
            pictograph_data: Pictograph data to match
            position_criteria: Position matching criteria

        Returns:
            Position ID or None if no match

        Note:
            Web implementation: Same matching logic across platforms
        """
        pass

    @abstractmethod
    def get_matching_positions(self, pictograph_data: Dict[str, Any]) -> List[str]:
        """
        Get all positions matching pictograph data.

        Args:
            pictograph_data: Pictograph data to match

        Returns:
            List of matching position IDs

        Note:
            Web implementation: Same matching logic across platforms
        """
        pass

    @abstractmethod
    def get_position_compatibility(
        self, pictograph_data: Dict[str, Any], position_id: str
    ) -> float:
        """
        Get compatibility score between pictograph and position.

        Args:
            pictograph_data: Pictograph data
            position_id: Position ID to check compatibility with

        Returns:
            Compatibility score (0.0 to 1.0)

        Note:
            Web implementation: Same compatibility calculation across platforms
        """
        pass

    @abstractmethod
    def update_position_mappings(self, mappings: Dict[str, List[str]]) -> bool:
        """
        Update position mappings.

        Args:
            mappings: Dictionary mapping pictograph IDs to position IDs

        Returns:
            True if updated successfully, False otherwise

        Note:
            Web implementation: Updates in browser storage or server
        """
        pass

    @abstractmethod
    def get_position_mappings(self) -> Dict[str, List[str]]:
        """
        Get current position mappings.

        Returns:
            Dictionary mapping pictograph IDs to position IDs

        Note:
            Web implementation: Retrieved from browser storage or server
        """
        pass


class IPictographFactory(ABC):
    """Interface for pictograph factory operations."""

    @abstractmethod
    def create_pictograph(
        self, pictograph_type: str, parameters: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new pictograph.

        Args:
            pictograph_type: Type of pictograph to create
            parameters: Creation parameters

        Returns:
            Created pictograph data or None if failed

        Note:
            Web implementation: Same creation logic across platforms
        """
        pass

    @abstractmethod
    def clone_pictograph(self, pictograph_id: str) -> Optional[Dict[str, Any]]:
        """
        Clone an existing pictograph.

        Args:
            pictograph_id: ID of pictograph to clone

        Returns:
            Cloned pictograph data or None if failed

        Note:
            Web implementation: Same cloning logic across platforms
        """
        pass

    @abstractmethod
    def get_supported_types(self) -> List[str]:
        """
        Get list of supported pictograph types.

        Returns:
            List of supported types
        """
        pass

    @abstractmethod
    def validate_parameters(
        self, pictograph_type: str, parameters: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        Validate creation parameters.

        Args:
            pictograph_type: Type of pictograph
            parameters: Parameters to validate

        Returns:
            Tuple of (is_valid, error_messages)

        Note:
            Web implementation: Same validation logic across platforms
        """
        pass


class IPictographPoolManager(ABC):
    """Interface for pictograph pool manager operations."""

    @abstractmethod
    def get_pictograph_from_pool(self, pictograph_id: str) -> Optional[Dict[str, Any]]:
        """
        Get pictograph from pool.

        Args:
            pictograph_id: ID of pictograph to get

        Returns:
            Pictograph data or None if not in pool

        Note:
            Web implementation: Retrieved from memory pool or cache
        """
        pass

    @abstractmethod
    def add_pictograph_to_pool(
        self, pictograph_id: str, pictograph_data: Dict[str, Any]
    ) -> bool:
        """
        Add pictograph to pool.

        Args:
            pictograph_id: ID of pictograph to add
            pictograph_data: Pictograph data to add

        Returns:
            True if added successfully, False otherwise

        Note:
            Web implementation: Adds to memory pool or cache
        """
        pass

    @abstractmethod
    def remove_pictograph_from_pool(self, pictograph_id: str) -> bool:
        """
        Remove pictograph from pool.

        Args:
            pictograph_id: ID of pictograph to remove

        Returns:
            True if removed successfully, False otherwise

        Note:
            Web implementation: Removes from memory pool or cache
        """
        pass

    @abstractmethod
    def clear_pool(self) -> bool:
        """
        Clear all pictographs from pool.

        Returns:
            True if cleared successfully, False otherwise

        Note:
            Web implementation: Clears memory pool or cache
        """
        pass

    @abstractmethod
    def get_pool_size(self) -> int:
        """
        Get current pool size.

        Returns:
            Number of pictographs in pool
        """
        pass

    @abstractmethod
    def get_pool_statistics(self) -> Dict[str, Any]:
        """
        Get pool statistics.

        Returns:
            Dictionary of pool statistics

        Note:
            Web implementation: May include memory usage metrics
        """
        pass


class IPictographDataManager(ABC):
    """Interface for pictograph data operations."""

    @abstractmethod
    def create_pictograph(self, grid_mode: Any = None) -> Any:
        """Create a new blank pictograph."""

    @abstractmethod
    def create_from_beat(self, beat_data: Any) -> Any:
        """Create pictograph from beat data."""

    @abstractmethod
    def update_pictograph_arrows(self, pictograph: Any, arrows: Dict[str, Any]) -> Any:
        """Update arrows in pictograph."""

    @abstractmethod
    def search_dataset(self, query: Dict[str, Any]) -> List[Any]:
        """Search pictograph dataset with query."""

    @abstractmethod
    def get_dataset_categories(self) -> List[str]:
        """Get all available dataset categories."""

    @abstractmethod
    def add_to_dataset(self, pictograph: Any, category: str = "user_created") -> str:
        """Add pictograph to dataset."""
