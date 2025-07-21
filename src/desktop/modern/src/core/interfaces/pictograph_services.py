"""
Pictograph Service Interfaces

Interface definitions for pictograph-related services following TKA's clean architecture.
These interfaces define contracts for validation, scaling, and pictograph manipulation services.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Tuple

from core.types import Size


class ScalingContext(Enum):
    """Different contexts where pictographs are displayed, each with specific scaling needs."""

    OPTION_VIEW = "option_view"
    START_POS_PICKER = "start_pos_picker"
    ADVANCED_START_POS = "advanced_start_pos"
    CODEX_VIEW = "codex_view"
    BEAT_VIEW = "beat_view"
    GRAPH_EDITOR_VIEW = "graph_editor_view"
    LEARN_QUESTION = "learn_question"
    LEARN_ANSWER = "learn_answer"
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
        container_size: Size,
        scene_size: Size,
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
