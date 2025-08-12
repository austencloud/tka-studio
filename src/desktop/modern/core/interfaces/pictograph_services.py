"""
Pictograph Service Interfaces

Interface definitions for pictograph-related services following TKA's clean architecture.
These interfaces define contracts for validation, scaling, and pictograph manipulation services.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


# ScalingContext removed - direct views handle their own scaling


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


# IScalingService removed - direct views handle their own scaling using Qt's built-in methods


class IPictographDataManager(ABC):
    """Interface for pictograph data operations."""

    @abstractmethod
    def create_pictograph(self, grid_mode: Any = None) -> Any:
        """Create a new blank pictograph."""

    @abstractmethod
    def create_from_beat(self, beat_data: Any) -> Any:
        """Create pictograph from beat data."""

    @abstractmethod
    def update_pictograph_arrows(self, pictograph: Any, arrows: dict[str, Any]) -> Any:
        """Update arrows in pictograph."""

    @abstractmethod
    def search_dataset(self, query: dict[str, Any]) -> list[Any]:
        """Search pictograph dataset with query."""

    @abstractmethod
    def get_dataset_categories(self) -> list[str]:
        """Get all available dataset categories."""

    @abstractmethod
    def get_pictograph_data(self, pictograph_id: str) -> Any | None:
        """
        Get pictograph data by ID.

        Args:
            pictograph_id: Unique identifier for pictograph

        Returns:
            Pictograph data or None if not found
        """

    @abstractmethod
    def get_pictograph_dataset(self) -> dict[str, list[dict[str, Any]]]:
        """
        Get the complete pictograph dataset for question generation.

        Returns:
            Dictionary mapping letters to lists of pictograph data dictionaries.
            Each pictograph data dictionary contains:
            - id: Unique identifier
            - letter: Associated letter
            - type: Type of pictograph ("real" or "mock")
            - data: PictographData object
            - beat_data: Optional BeatData object for real pictographs
        """

    @abstractmethod
    def add_to_dataset(self, pictograph: Any, category: str = "user_created") -> str:
        """Add pictograph to dataset."""
