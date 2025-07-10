"""
Interface definitions for option picker services.

These interfaces define the contracts for services that handle option picker
functionality, following TKA's clean architecture principles.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple

from core.dependency_injection.di_container import DIContainer
from domain.models.beat_data import BeatData
from domain.models.sequence_models import SequenceData


class IOptionPickerInitializationService(ABC):
    """Interface for option picker initialization logic."""

    @abstractmethod
    def initialize_components(
        self,
        container: DIContainer,
        progress_callback: Optional[Callable[[str, float], None]] = None,
    ) -> Dict[str, Any]:
        """
        Initialize all option picker components.

        Args:
            container: DI container for service resolution
            progress_callback: Optional progress reporting callback

        Returns:
            Dictionary containing initialized components
        """

    @abstractmethod
    def create_widget_hierarchy(
        self, container: DIContainer, resize_callback: Callable[[], None]
    ) -> Tuple[Any, Any, Any, Any]:
        """
        Create the widget hierarchy for option picker.

        Args:
            container: DI container for service resolution
            resize_callback: Callback for widget resize events

        Returns:
            Tuple of (main_widget, sections_container, sections_layout, filter_widget)
        """

    @abstractmethod
    def create_pool_manager(
        self,
        main_widget: Any,
        beat_click_handler: Callable[[str], None],
        beat_data_click_handler: Callable[[Any], None],
    ) -> Any:
        """
        Create and configure the pictograph pool manager.

        Args:
            main_widget: Main widget for pool manager
            beat_click_handler: Handler for beat clicks
            beat_data_click_handler: Handler for beat data clicks

        Returns:
            Configured pool manager
        """


class IOptionPickerDataService(ABC):
    """Interface for option picker data management."""

    @abstractmethod
    def load_beat_options(self) -> List[BeatData]:
        """
        Load initial beat options.

        Returns:
            List of available beat data options
        """

    @abstractmethod
    def refresh_options(self) -> List[BeatData]:
        """
        Refresh beat options.

        Returns:
            Updated list of beat data options
        """

    @abstractmethod
    def refresh_from_sequence_data(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[BeatData]:
        """
        Refresh options based on legacy sequence data.

        Args:
            sequence_data: Legacy sequence data format

        Returns:
            Updated list of beat data options
        """

    @abstractmethod
    def refresh_from_sequence(self, sequence: SequenceData) -> List[BeatData]:
        """
        Refresh options based on modern sequence data.

        Args:
            sequence: Modern sequence data

        Returns:
            Updated list of beat data options
        """

    @abstractmethod
    def get_beat_data_for_option(self, option_id: str) -> Optional[BeatData]:
        """
        Get beat data for a specific option ID.

        Args:
            option_id: Option identifier (e.g., 'beat_J')

        Returns:
            BeatData if found, None otherwise
        """

    @abstractmethod
    def get_current_options(self) -> List[BeatData]:
        """
        Get currently loaded beat options.

        Returns:
            Current list of beat data options
        """

    @abstractmethod
    def clear_cache(self) -> None:
        """Clear cached options."""


class IOptionPickerDisplayService(ABC):
    """Interface for option picker display management."""

    @abstractmethod
    def initialize_display(
        self,
        sections_container: Any,
        sections_layout: Any,
        pool_manager: Any,
        option_picker_size_provider: Callable,
    ) -> None:
        """
        Initialize the display components.

        Args:
            sections_container: Container for sections
            sections_layout: Layout for sections
            pool_manager: Pictograph pool manager
            size_provider: Function to provide size information
        """

    @abstractmethod
    def create_sections(self) -> None:
        """Create display sections for beat options."""

    @abstractmethod
    def update_beat_display(self, beat_options: List[BeatData]) -> None:
        """
        Update the display with new beat options.

        Args:
            beat_options: List of beat data to display
        """

    @abstractmethod
    def ensure_sections_visible(self) -> None:
        """Ensure all sections are visible after updates."""

    @abstractmethod
    def resize_sections(self) -> None:
        """Resize sections to fit current container."""

    @abstractmethod
    def get_sections(self) -> Dict[str, Any]:
        """
        Get current display sections.

        Returns:
            Dictionary of section name to section widget
        """

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up display resources."""


class IOptionPickerEventService(ABC):
    """Interface for option picker event handling."""

    @abstractmethod
    def setup_event_handlers(
        self,
        pool_manager: Any,
        filter_widget: Any,
        beat_click_handler: Callable[[str], None],
        beat_data_click_handler: Callable[[BeatData], None],
        filter_change_handler: Callable[[str], None],
    ) -> None:
        """
        Setup event handlers for option picker interactions.

        Args:
            pool_manager: Pictograph pool manager
            filter_widget: Filter widget
            beat_click_handler: Handler for beat clicks
            beat_data_click_handler: Handler for beat data clicks
            filter_change_handler: Handler for filter changes
        """

    @abstractmethod
    def handle_widget_resize(
        self, pool_manager: Any, display_service: IOptionPickerDisplayService
    ) -> None:
        """
        Handle widget resize events.

        Args:
            pool_manager: Pictograph pool manager
            display_service: Display service for section resizing
        """

    @abstractmethod
    def handle_filter_change(
        self,
        filter_text: str,
        data_service: IOptionPickerDataService,
        display_service: IOptionPickerDisplayService,
    ) -> None:
        """
        Handle filter text changes.

        Args:
            filter_text: New filter text
            data_service: Data service for getting options
            display_service: Display service for updating display
        """

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up event service resources."""


class IOptionPickerOrchestrator(ABC):
    """Interface for option picker orchestration."""

    @abstractmethod
    def initialize(
        self, progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> None:
        """
        Initialize the option picker with all components.

        Args:
            progress_callback: Optional progress reporting callback
        """

    @abstractmethod
    def get_widget(self) -> Any:
        """
        Get the main widget for this component.

        Returns:
            Main option picker widget
        """

    @abstractmethod
    def load_motion_combinations(self, sequence_data: List[Dict[str, Any]]) -> None:
        """
        Load motion combinations from sequence data.

        Args:
            sequence_data: Sequence data to load combinations from
        """

    @abstractmethod
    def refresh_options(self) -> None:
        """Refresh the option picker with latest beat options."""

    @abstractmethod
    def refresh_from_modern_sequence(self, sequence: SequenceData) -> None:
        """
        Refresh options based on modern sequence data.

        Args:
            sequence: Modern sequence data
        """

    @abstractmethod
    def get_beat_data_for_option(self, option_id: str) -> Optional[BeatData]:
        """
        Get beat data for a specific option ID.

        Args:
            option_id: Option identifier

        Returns:
            BeatData if found, None otherwise
        """

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up option picker resources."""
