"""
Interface definitions for option picker services.

These interfaces define the contracts for services that handle option picker
functionality, following TKA's clean architecture principles.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData


class IOptionServiceSignals(ABC):
    """Interface for option service signal emission."""

    @abstractmethod
    def emit_options_loaded(self, options: list[PictographData]) -> None:
        """
        Emit signal when options are loaded.

        Args:
            options: List of loaded pictograph options
        """

    @abstractmethod
    def emit_options_cleared(self) -> None:
        """Emit signal when options are cleared."""


class IOptionProvider(ABC):
    """Interface for pictograph option management."""

    @abstractmethod
    def load_options_from_sequence(
        self, sequence_data: list[dict[str, Any]]
    ) -> list[PictographData]:
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
    ) -> list[PictographData]:
        """
        Load pictograph options based on modern sequence data.

        Args:
            sequence: Modern SequenceData object

        Returns:
            List of pictograph options
        """

    @abstractmethod
    def get_current_options(self) -> list[PictographData]:
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
    def filter_options_by_letter(self, letter: str) -> list[PictographData]:
        """
        Filter current options by letter.

        Args:
            letter: Letter to filter by

        Returns:
            List of options matching the letter
        """

    @abstractmethod
    def get_available_letters(self) -> list[str]:
        """
        Get list of available letters in current options.

        Returns:
            Sorted list of unique letters
        """
