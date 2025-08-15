"""
Option Picker Interfaces

Defines interfaces for option selection and management services.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from desktop.modern.src.domain.models.pictograph_data import PictographData
    from desktop.modern.src.domain.models.sequence_data import SequenceData


class IOptionPickerWidget(ABC):
    """Interface for option picker widgets."""

    @abstractmethod
    def set_options(self, options: list[Any]) -> None:
        """Set available options."""
        pass

    @abstractmethod
    def get_selected_option(self) -> Any:
        """Get the currently selected option."""
        pass

    @abstractmethod
    def set_selected_option(self, option: Any) -> None:
        """Set the selected option."""
        pass

    @abstractmethod
    def clear_selection(self) -> None:
        """Clear the current selection."""
        pass


class IAdvancedOptionPicker(IOptionPickerWidget):
    """Interface for advanced option picker with filtering and search."""

    @abstractmethod
    def set_filter(self, filter_text: str) -> None:
        """Set filter text."""
        pass

    @abstractmethod
    def get_filtered_options(self) -> list[Any]:
        """Get options after applying filter."""
        pass

    @abstractmethod
    def set_search_enabled(self, enabled: bool) -> None:
        """Enable or disable search functionality."""
        pass


class IOptionPickerService(ABC):
    """Interface for option picker management service."""

    @abstractmethod
    def create_option_picker(self, options: list[Any]) -> IOptionPickerWidget:
        """Create a new option picker widget."""
        pass

    @abstractmethod
    def register_option_picker(
        self, picker_id: str, picker: IOptionPickerWidget
    ) -> None:
        """Register an option picker."""
        pass

    @abstractmethod
    def get_option_picker(self, picker_id: str) -> IOptionPickerWidget | None:
        """Get a registered option picker."""
        pass


class IOptionProvider(ABC):
    """Interface for option provider services."""

    @abstractmethod
    def load_options_from_sequence(
        self, sequence_data: list[dict[str, Any]]
    ) -> list[PictographData]:
        """Load pictograph options based on legacy sequence data."""
        pass

    @abstractmethod
    def load_options_from_modern_sequence(
        self, sequence: SequenceData
    ) -> list[PictographData]:
        """Load pictograph options based on modern sequence data."""
        pass

    @abstractmethod
    def get_current_options(self) -> list[PictographData]:
        """Get the currently loaded pictograph options."""
        pass

    @abstractmethod
    def clear_options(self) -> None:
        """Clear all loaded options."""
        pass

    @abstractmethod
    def get_option_count(self) -> int:
        """Get the number of currently loaded options."""
        pass

    @abstractmethod
    def get_option_by_index(self, index: int) -> PictographData | None:
        """Get option by index."""
        pass

    @abstractmethod
    def filter_options_by_letter(self, letter: str) -> list[PictographData]:
        """Filter current options by letter."""
        pass

    @abstractmethod
    def get_available_letters(self) -> list[str]:
        """Get list of available letters in current options."""
        pass


class IOptionServiceSignals(ABC):
    """Interface for option service signal emission."""

    @abstractmethod
    def emit_options_loaded(self, options: list[PictographData]) -> None:
        """Emit signal when options are loaded."""
        pass

    @abstractmethod
    def emit_options_cleared(self) -> None:
        """Emit signal when options are cleared."""
        pass

    @abstractmethod
    def set_signal_emitter(self, signal_emitter: IOptionServiceSignals) -> None:
        """Set the signal emitter for this service."""
        pass


class IOptionPickerDisplayService(ABC):
    """Interface for option picker display management."""

    @abstractmethod
    def show_options(self, options: list[PictographData]) -> None:
        """Display the given options in the picker."""
        pass

    @abstractmethod
    def hide_options(self) -> None:
        """Hide all options in the picker."""
        pass

    @abstractmethod
    def clear_selection(self) -> None:
        """Clear any selected options."""
        pass

    @abstractmethod
    def set_selected_option(self, option: PictographData) -> None:
        """Set the selected option."""
        pass

    @abstractmethod
    def get_selected_option(self) -> PictographData | None:
        """Get the currently selected option."""
        pass

    @abstractmethod
    def refresh_display(self) -> None:
        """Refresh the display of options."""
        pass

    @abstractmethod
    def set_filter(self, filter_text: str) -> None:
        """Apply a filter to the displayed options."""
        pass

    @abstractmethod
    def get_display_count(self) -> int:
        """Get the number of currently displayed options."""
        pass
