"""
Interface definitions for option picker services.

These interfaces define the contracts for services that handle option picker
functionality, following TKA's clean architecture principles.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple

from core.dependency_injection.di_container import DIContainer
from domain.models.beat_data import BeatData
from domain.models.pictograph_models import PictographData
from domain.models.sequence_models import SequenceData


class IOptionServiceSignals(ABC):
    """Interface for option service signal emission."""

    @abstractmethod
    def emit_options_loaded(self, options: List[PictographData]) -> None:
        """
        Emit signal when options are loaded.

        Args:
            options: List of loaded pictograph options
        """

    @abstractmethod
    def emit_options_cleared(self) -> None:
        """Emit signal when options are cleared."""


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
    """Interface for option picker data management. Works exclusively with PictographData."""

    @abstractmethod
    def load_pictograph_options(self) -> List[PictographData]:
        """
        Load initial pictograph options.

        Returns:
            List of available pictograph data options
        """

    @abstractmethod
    def refresh_pictograph_options(self) -> List[PictographData]:
        """
        Refresh pictograph options.

        Returns:
            Updated list of pictograph data options
        """

    @abstractmethod
    def refresh_pictographs_from_sequence_data(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[PictographData]:
        """
        Refresh options based on legacy sequence data.

        Args:
            sequence_data: Legacy sequence data format

        Returns:
            Updated list of pictograph data options
        """

    @abstractmethod
    def refresh_pictographs_from_sequence(
        self, sequence: SequenceData
    ) -> List[PictographData]:
        """
        Refresh options based on modern sequence data.

        Args:
            sequence: Modern sequence data

        Returns:
            Updated list of pictograph data options
        """

    @abstractmethod
    def get_pictograph_for_option(self, option_id: str) -> Optional[PictographData]:
        """
        Get pictograph data for a specific option ID.

        Args:
            option_id: Option identifier (e.g., 'option_0', 'option_J')

        Returns:
            PictographData if found, None otherwise
        """

    @abstractmethod
    def get_current_pictographs(self) -> List[PictographData]:
        """
        Get currently loaded pictograph options.

        Returns:
            Current list of pictograph data options
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
    def update_pictograph_display(
        self, pictograph_options: List[PictographData]
    ) -> None:
        """
        Update the display with new pictograph options.

        Args:
            pictograph_options: List of pictograph data to display
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
        option_click_handler: Callable[[str], None],
        pictograph_click_handler: Callable[[PictographData], None],
        filter_change_handler: Callable[[str], None],
    ) -> None:
        """
        Setup event handlers for option picker interactions.

        Args:
            pool_manager: Pictograph pool manager
            filter_widget: Filter widget
            option_click_handler: Handler for option clicks
            pictograph_click_handler: Handler for pictograph data clicks
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


class IOptionService(ABC):
    """Interface for pictograph option management."""

    @abstractmethod
    def load_options_from_sequence(
        self, sequence_data: List[Dict[str, Any]]
    ) -> List[PictographData]:
        """
        Load pictograph options based on legacy sequence data.

        Args:
            sequence_data: Legacy sequence data format

        Returns:
            List of pictograph options
        """

    @abstractmethod
    def load_options_from_modern_sequence(
        self, sequence: SequenceData
    ) -> List[PictographData]:
        """
        Load pictograph options based on modern sequence data.

        Args:
            sequence: Modern SequenceData object

        Returns:
            List of pictograph options
        """

    @abstractmethod
    def get_current_options(self) -> List[PictographData]:
        """
        Get the currently loaded pictograph options.

        Returns:
            Copy of current pictograph options
        """

    @abstractmethod
    def clear_options(self) -> None:
        """Clear all loaded options."""

    @abstractmethod
    def get_option_count(self) -> int:
        """
        Get the number of currently loaded options.

        Returns:
            Count of loaded options
        """

    @abstractmethod
    def get_option_by_index(self, index: int) -> Optional[PictographData]:
        """
        Get option by index.

        Args:
            index: Index of the option to retrieve

        Returns:
            PictographData if found, None otherwise
        """

    @abstractmethod
    def filter_options_by_letter(self, letter: str) -> List[PictographData]:
        """
        Filter current options by letter.

        Args:
            letter: Letter to filter by

        Returns:
            List of options matching the letter
        """

    @abstractmethod
    def get_available_letters(self) -> List[str]:
        """
        Get list of available letters in current options.

        Returns:
            Sorted list of unique letters
        """


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
    def get_pictograph_for_option(self, option_id: str) -> Optional[PictographData]:
        """
        Get pictograph data for a specific option ID.

        Args:
            option_id: Option identifier

        Returns:
            PictographData if found, None otherwise
        """

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up option picker resources."""
