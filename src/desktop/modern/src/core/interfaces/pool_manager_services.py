"""
Pool Manager Service Interfaces

Interface definitions for object pool management services following TKA's clean architecture.
These interfaces handle efficient object pooling for performance optimization.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set, TypeVar, Generic


T = TypeVar('T')


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
        pass

    @abstractmethod
    def return_object(self, obj: T) -> None:
        """
        Return object to pool.

        Args:
            obj: Object to return to pool

        Note:
            Web implementation: Resets DOM element properties
        """
        pass

    @abstractmethod
    def get_pool_size(self) -> int:
        """
        Get current pool size.

        Returns:
            Number of objects in pool

        Note:
            Web implementation: Returns cached DOM element count
        """
        pass

    @abstractmethod
    def get_active_count(self) -> int:
        """
        Get number of active (checked out) objects.

        Returns:
            Number of active objects

        Note:
            Web implementation: Returns in-use DOM element count
        """
        pass

    @abstractmethod
    def clear_pool(self) -> None:
        """
        Clear all objects from pool.

        Note:
            Web implementation: Removes cached DOM elements
        """
        pass

    @abstractmethod
    def set_max_pool_size(self, max_size: int) -> None:
        """
        Set maximum pool size.

        Args:
            max_size: Maximum number of objects to pool

        Note:
            Web implementation: Limits DOM element caching
        """
        pass

    @abstractmethod
    def get_pool_statistics(self) -> Dict[str, Any]:
        """
        Get pool performance statistics.

        Returns:
            Dictionary with pool metrics

        Note:
            Web implementation: Returns memory usage and performance data
        """
        pass


class IArrowItemPoolManager(ABC):
    """Interface for arrow item pool management operations."""

    @abstractmethod
    def get_arrow_item(self, arrow_type: str) -> Any:
        """
        Get arrow item from pool.

        Args:
            arrow_type: Type of arrow item needed

        Returns:
            Arrow item object

        Note:
            Web implementation: Returns SVG element or Canvas object
        """
        pass

    @abstractmethod
    def return_arrow_item(self, arrow_item: Any) -> None:
        """
        Return arrow item to pool.

        Args:
            arrow_item: Arrow item to return

        Note:
            Web implementation: Resets SVG properties and caches element
        """
        pass

    @abstractmethod
    def preload_arrows(self, arrow_types: List[str], count: int) -> None:
        """
        Preload arrow items into pool.

        Args:
            arrow_types: List of arrow types to preload
            count: Number of each type to preload

        Note:
            Web implementation: Pre-creates SVG elements for performance
        """
        pass

    @abstractmethod
    def get_arrow_count_by_type(self, arrow_type: str) -> int:
        """
        Get count of specific arrow type in pool.

        Args:
            arrow_type: Arrow type to count

        Returns:
            Number of arrow items of specified type

        Note:
            Web implementation: Returns cached SVG element count
        """
        pass

    @abstractmethod
    def clear_arrow_type(self, arrow_type: str) -> None:
        """
        Clear specific arrow type from pool.

        Args:
            arrow_type: Arrow type to clear

        Note:
            Web implementation: Removes SVG elements of specified type
        """
        pass

    @abstractmethod
    def reset_arrow_item(self, arrow_item: Any) -> None:
        """
        Reset arrow item to default state.

        Args:
            arrow_item: Arrow item to reset

        Note:
            Web implementation: Resets SVG attributes to defaults
        """
        pass

    @abstractmethod
    def configure_arrow_item(
        self, 
        arrow_item: Any, 
        config: Dict[str, Any]
    ) -> None:
        """
        Configure arrow item with properties.

        Args:
            arrow_item: Arrow item to configure
            config: Configuration dictionary

        Note:
            Web implementation: Sets SVG attributes and styles
        """
        pass


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
        pass

    @abstractmethod
    def return_pictograph(self, pictograph: Any) -> None:
        """
        Return pictograph to pool.

        Args:
            pictograph: Pictograph to return

        Note:
            Web implementation: Clears Canvas or resets SVG container
        """
        pass

    @abstractmethod
    def preload_pictographs(
        self, 
        pictograph_types: List[str], 
        count: int
    ) -> None:
        """
        Preload pictographs into pool.

        Args:
            pictograph_types: List of pictograph types to preload
            count: Number of each type to preload

        Note:
            Web implementation: Pre-creates Canvas/SVG elements
        """
        pass

    @abstractmethod
    def get_pictograph_count_by_type(self, pictograph_type: str) -> int:
        """
        Get count of specific pictograph type in pool.

        Args:
            pictograph_type: Pictograph type to count

        Returns:
            Number of pictographs of specified type

        Note:
            Web implementation: Returns cached element count
        """
        pass

    @abstractmethod
    def clear_pictograph_type(self, pictograph_type: str) -> None:
        """
        Clear specific pictograph type from pool.

        Args:
            pictograph_type: Pictograph type to clear

        Note:
            Web implementation: Removes elements of specified type
        """
        pass

    @abstractmethod
    def reset_pictograph(self, pictograph: Any) -> None:
        """
        Reset pictograph to default state.

        Args:
            pictograph: Pictograph to reset

        Note:
            Web implementation: Clears Canvas or resets SVG content
        """
        pass

    @abstractmethod
    def configure_pictograph(
        self, 
        pictograph: Any, 
        config: Dict[str, Any]
    ) -> None:
        """
        Configure pictograph with properties.

        Args:
            pictograph: Pictograph to configure
            config: Configuration dictionary

        Note:
            Web implementation: Sets Canvas properties or SVG attributes
        """
        pass

    @abstractmethod
    def capture_pictograph_state(self, pictograph: Any) -> Dict[str, Any]:
        """
        Capture current pictograph state.

        Args:
            pictograph: Pictograph to capture state from

        Returns:
            State dictionary

        Note:
            Web implementation: Captures Canvas ImageData or SVG state
        """
        pass

    @abstractmethod
    def restore_pictograph_state(
        self, 
        pictograph: Any, 
        state: Dict[str, Any]
    ) -> None:
        """
        Restore pictograph state.

        Args:
            pictograph: Pictograph to restore state to
            state: State dictionary to restore

        Note:
            Web implementation: Restores Canvas ImageData or SVG state
        """
        pass


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
        pass

    @abstractmethod
    def return_frame(self, frame: Any) -> None:
        """
        Return frame to pool.

        Args:
            frame: Frame to return

        Note:
            Web implementation: Resets DOM element and caches
        """
        pass

    @abstractmethod
    def preload_frames(self, frame_types: List[str], count: int) -> None:
        """
        Preload frames into pool.

        Args:
            frame_types: List of frame types to preload
            count: Number of each type to preload

        Note:
            Web implementation: Pre-creates DOM elements or components
        """
        pass

    @abstractmethod
    def configure_frame(self, frame: Any, config: Dict[str, Any]) -> None:
        """
        Configure frame with properties.

        Args:
            frame: Frame to configure
            config: Configuration dictionary

        Note:
            Web implementation: Sets DOM attributes and styles
        """
        pass

    @abstractmethod
    def get_frame_template(self, frame_type: str) -> Dict[str, Any]:
        """
        Get template configuration for frame type.

        Args:
            frame_type: Frame type to get template for

        Returns:
            Template configuration dictionary

        Note:
            Web implementation: Returns DOM template or component props
        """
        pass


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
        pass

    @abstractmethod
    def return_option(self, option: Any) -> None:
        """
        Return option to pool.

        Args:
            option: Option to return

        Note:
            Web implementation: Resets and caches option element
        """
        pass

    @abstractmethod
    def preload_options(self, option_types: List[str], count: int) -> None:
        """
        Preload options into pool.

        Args:
            option_types: List of option types to preload
            count: Number of each type to preload

        Note:
            Web implementation: Pre-creates option elements or data
        """
        pass

    @abstractmethod
    def get_available_option_types(self) -> List[str]:
        """
        Get list of available option types.

        Returns:
            List of option type identifiers

        Note:
            Web implementation: Returns supported option configurations
        """
        pass

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
        pass
