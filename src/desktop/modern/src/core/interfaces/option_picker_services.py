"""
Interface definitions for option picker services.

These interfaces define the contracts for services that handle option picker
functionality, following TKA's clean architecture principles.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple

from core.dependency_injection.di_container import DIContainer
from domain.models.core_models import BeatData, SequenceData
from PyQt6.QtWidgets import QVBoxLayout, QWidget


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
        pass

    @abstractmethod
    def create_widget_hierarchy(
        self, container: DIContainer, resize_callback: Callable[[], None]
    ) -> Tuple[QWidget, QWidget, QVBoxLayout, QWidget]:
        """
        Create the widget hierarchy for option picker.

        Args:
            container: DI container for service resolution
            resize_callback: Callback for widget resize events

        Returns:
            Tuple of (main_widget, sections_container, sections_layout, filter_widget)
        """
        pass

    @abstractmethod
    def create_pool_manager(
        self,
        main_widget: QWidget,
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
        pass


class IOptionPickerDataService(ABC):
    """Interface for option picker data management."""

    @abstractmethod
    def load_beat_options(self) -> List[BeatData]:
        """
        Load initial beat options.

        Returns:
            List of available beat data options
        """
        pass

    @abstractmethod
    def refresh_options(self) -> List[BeatData]:
        """
        Refresh beat options.

        Returns:
            Updated list of beat data options
        """
        pass

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
        pass

    @abstractmethod
    def refresh_from_modern_sequence(self, sequence: SequenceData) -> List[BeatData]:
        """
        Refresh options based on modern sequence data.

        Args:
            sequence: Modern sequence data

        Returns:
            Updated list of beat data options
        """
        pass

    @abstractmethod
    def get_beat_data_for_option(self, option_id: str) -> Optional[BeatData]:
        """
        Get beat data for a specific option ID.

        Args:
            option_id: Option identifier (e.g., 'beat_J')

        Returns:
            BeatData if found, None otherwise
        """
        pass

    @abstractmethod
    def get_current_options(self) -> List[BeatData]:
        """
        Get currently loaded beat options.

        Returns:
            Current list of beat data options
        """
        pass

    @abstractmethod
    def clear_cache(self) -> None:
        """Clear cached options."""
        pass


class IOptionPickerDisplayService(ABC):
    """Interface for option picker display management."""

    @abstractmethod
    def initialize_display(
        self,
        sections_container: QWidget,
        sections_layout: QVBoxLayout,
        pool_manager: Any,
        size_provider: Callable,
    ) -> None:
        """
        Initialize the display components.

        Args:
            sections_container: Container for sections
            sections_layout: Layout for sections
            pool_manager: Pictograph pool manager
            size_provider: Function to provide size information
        """
        pass

    @abstractmethod
    def create_sections(self) -> None:
        """Create display sections for beat options."""
        pass

    @abstractmethod
    def update_beat_display(self, beat_options: List[BeatData]) -> None:
        """
        Update the display with new beat options.

        Args:
            beat_options: List of beat data to display
        """
        pass

    @abstractmethod
    def ensure_sections_visible(self) -> None:
        """Ensure all sections are visible after updates."""
        pass

    @abstractmethod
    def resize_sections(self) -> None:
        """Resize sections to fit current container."""
        pass

    @abstractmethod
    def get_sections(self) -> Dict[str, Any]:
        """
        Get current display sections.

        Returns:
            Dictionary of section name to section widget
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up display resources."""
        pass


class IOptionPickerEventService(ABC):
    """Interface for option picker event handling."""

    @abstractmethod
    def setup_event_handlers(
        self,
        pool_manager: Any,
        filter_widget: QWidget,
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
        pass

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
        pass

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
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up event service resources."""
        pass


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
        pass

    @abstractmethod
    def get_widget(self) -> QWidget:
        """
        Get the main widget for this component.

        Returns:
            Main option picker widget
        """
        pass

    @abstractmethod
    def load_motion_combinations(self, sequence_data: List[Dict[str, Any]]) -> None:
        """
        Load motion combinations from sequence data.

        Args:
            sequence_data: Sequence data to load combinations from
        """
        pass

    @abstractmethod
    def refresh_options(self) -> None:
        """Refresh the option picker with latest beat options."""
        pass

    @abstractmethod
    def refresh_from_modern_sequence(self, sequence: SequenceData) -> None:
        """
        Refresh options based on modern sequence data.

        Args:
            sequence: Modern sequence data
        """
        pass

    @abstractmethod
    def get_beat_data_for_option(self, option_id: str) -> Optional[BeatData]:
        """
        Get beat data for a specific option ID.

        Args:
            option_id: Option identifier

        Returns:
            BeatData if found, None otherwise
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up option picker resources."""
        pass
