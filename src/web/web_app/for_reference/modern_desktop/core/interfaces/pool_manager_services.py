"""
Pool Manager Service Interfaces

Interface definitions for object pool management services following TKA's clean architecture.
These interfaces handle efficient object pooling for performance optimization.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar


T = TypeVar("T")


class IPoolManager(ABC, Generic[T]):
    """Generic interface for object pool management operations."""

    @abstractmethod
    def get_object(self) -> T:
        """
        Get object from pool.

        Returns:
            Object from pool (new if pool empty)

        Note:
            Web implementation: May use object recycling for DOM elements
        """

    @abstractmethod
    def return_object(self, obj: T) -> None:
        """
        Return object to pool.

        Args:
            obj: Object to return to pool

        Note:
            Web implementation: Resets DOM element properties
        """

    @abstractmethod
    def get_pool_size(self) -> int:
        """
        Get current pool size.

        Returns:
            Number of objects in pool

        Note:
            Web implementation: Returns cached DOM element count
        """

    @abstractmethod
    def get_active_count(self) -> int:
        """
        Get number of active (checked out) objects.

        Returns:
            Number of active objects

        Note:
            Web implementation: Returns in-use DOM element count
        """

    @abstractmethod
    def clear_pool(self) -> None:
        """
        Clear all objects from pool.

        Note:
            Web implementation: Removes cached DOM elements
        """

    @abstractmethod
    def set_max_pool_size(self, max_size: int) -> None:
        """
        Set maximum pool size.

        Args:
            max_size: Maximum number of objects to pool

        Note:
            Web implementation: Limits DOM element caching
        """

    @abstractmethod
    def get_pool_statistics(self) -> dict[str, Any]:
        """
        Get pool performance statistics.

        Returns:
            Dictionary with pool metrics

        Note:
            Web implementation: Returns memory usage and performance data
        """


# IArrowItemPoolManager removed - using legacy direct arrow creation approach


class IPictographPoolManager(ABC):
    """Interface for pictograph pool management operations."""

    @abstractmethod
    def get_pictograph(self, pictograph_type: str) -> Any:
        """
        Get pictograph from pool.

        Args:
            pictograph_type: Type of pictograph needed

        Returns:
            Pictograph object

        Note:
            Web implementation: Returns Canvas context or SVG container
        """

    @abstractmethod
    def return_pictograph(self, pictograph: Any) -> None:
        """
        Return pictograph to pool.

        Args:
            pictograph: Pictograph to return

        Note:
            Web implementation: Clears Canvas or resets SVG container
        """

    @abstractmethod
    def preload_pictographs(self, pictograph_types: list[str], count: int) -> None:
        """
        Preload pictographs into pool.

        Args:
            pictograph_types: List of pictograph types to preload
            count: Number of each type to preload

        Note:
            Web implementation: Pre-creates Canvas/SVG elements
        """

    @abstractmethod
    def reset_pictograph(self, pictograph: Any) -> None:
        """
        Reset pictograph to default state.

        Args:
            pictograph: Pictograph to reset

        Note:
            Web implementation: Clears Canvas or resets SVG content
        """

    @abstractmethod
    def configure_pictograph(self, pictograph: Any, config: dict[str, Any]) -> None:
        """
        Configure pictograph with properties.

        Args:
            pictograph: Pictograph to configure
            config: Configuration dictionary

        Note:
            Web implementation: Sets Canvas properties or SVG attributes
        """


class IFramePoolService(ABC):
    """Interface for frame pool service operations."""

    @abstractmethod
    def get_frame(self, frame_type: str) -> Any:
        """
        Get frame from pool.

        Args:
            frame_type: Type of frame needed

        Returns:
            Frame object

        Note:
            Web implementation: Returns DOM element or component instance
        """

    @abstractmethod
    def return_frame(self, frame: Any) -> None:
        """
        Return frame to pool.

        Args:
            frame: Frame to return

        Note:
            Web implementation: Resets DOM element and caches
        """

    @abstractmethod
    def preload_frames(self, frame_types: list[str], count: int) -> None:
        """
        Preload frames into pool.

        Args:
            frame_types: List of frame types to preload
            count: Number of each type to preload

        Note:
            Web implementation: Pre-creates DOM elements or components
        """

    @abstractmethod
    def configure_frame(self, frame: Any, config: dict[str, Any]) -> None:
        """
        Configure frame with properties.

        Args:
            frame: Frame to configure
            config: Configuration dictionary

        Note:
            Web implementation: Sets DOM attributes and styles
        """

    @abstractmethod
    def get_frame_template(self, frame_type: str) -> dict[str, Any]:
        """
        Get template configuration for frame type.

        Args:
            frame_type: Frame type to get template for

        Returns:
            Template configuration dictionary

        Note:
            Web implementation: Returns DOM template or component props
        """


class IOptionPoolService(ABC):
    """Interface for option pool service operations."""

    @abstractmethod
    def get_option(self, option_type: str) -> Any:
        """
        Get option from pool.

        Args:
            option_type: Type of option needed

        Returns:
            Option object

        Note:
            Web implementation: Returns DOM element or data object
        """

    @abstractmethod
    def return_option(self, option: Any) -> None:
        """
        Return option to pool.

        Args:
            option: Option to return

        Note:
            Web implementation: Resets and caches option element
        """

    @abstractmethod
    def preload_options(self, option_types: list[str], count: int) -> None:
        """
        Preload options into pool.

        Args:
            option_types: List of option types to preload
            count: Number of each type to preload

        Note:
            Web implementation: Pre-creates option elements or data
        """

    @abstractmethod
    def get_available_option_types(self) -> list[str]:
        """
        Get list of available option types.

        Returns:
            List of option type identifiers

        Note:
            Web implementation: Returns supported option configurations
        """

    @abstractmethod
    def validate_option(self, option: Any) -> bool:
        """
        Validate option object.

        Args:
            option: Option to validate

        Returns:
            True if option is valid

        Note:
            Web implementation: Validates option data structure
        """
