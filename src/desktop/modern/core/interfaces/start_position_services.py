"""
Interface definitions for start position services.

These interfaces define the contracts for start position services
that follow TKA's clean architecture principles.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from desktop.modern.core.commands.start_position_commands import SetStartPositionCommand
from desktop.modern.core.types import Size
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData


class IStartPositionDataService(ABC):
    """Interface for start position data retrieval and caching."""

    @abstractmethod
    def get_position_data(
        self, position_key: str, grid_mode: str = "diamond"
    ) -> PictographData | None:
        """
        Get pictograph data for a start position.

        Args:
            position_key: Position key like "alpha1_alpha1"
            grid_mode: Grid mode ("diamond" or "box")

        Returns:
            PictographData if found, None otherwise
        """

    @abstractmethod
    def get_available_positions(self, grid_mode: str = "diamond") -> list[str]:
        """
        Get all available start positions for a grid mode.

        Args:
            grid_mode: Grid mode ("diamond" or "box")

        Returns:
            List of available position keys
        """

    @abstractmethod
    def get_position_beat_data(
        self, position_key: str, grid_mode: str = "diamond"
    ) -> BeatData | None:
        """
        Get complete beat data for a start position.

        Args:
            position_key: Position key like "alpha1_alpha1"
            grid_mode: Grid mode ("diamond" or "box")

        Returns:
            BeatData with embedded pictograph if found, None otherwise
        """


class IStartPositionSelectionService(ABC):
    """Interface for start position selection business logic."""

    @abstractmethod
    def validate_selection(self, position_key: str) -> bool:
        """
        Validate if a position key is selectable.

        Args:
            position_key: Position key to validate

        Returns:
            True if valid for selection, False otherwise
        """

    @abstractmethod
    def create_selection_command(self, position_key: str) -> SetStartPositionCommand:
        """
        Create a command for setting start position.

        Args:
            position_key: Position key to set

        Returns:
            SetStartPositionCommand ready for execution
        """

    @abstractmethod
    def extract_end_position_from_key(self, position_key: str) -> str:
        """
        Extract the end position from a position key.

        Args:
            position_key: Position key like "alpha1_alpha1"

        Returns:
            End position part (e.g., "alpha1")
        """


class IStartPositionUIService(ABC):
    """Interface for start position UI state and layout management."""

    @abstractmethod
    def calculate_option_size(
        self, container_width: int, is_advanced: bool = False
    ) -> int:
        """
        Calculate the appropriate size for start position options.

        Args:
            container_width: Width of the container
            is_advanced: True for advanced picker, False for basic

        Returns:
            Size in pixels for the option components
        """

    @abstractmethod
    def get_grid_layout_config(
        self, grid_mode: str, is_advanced: bool = False
    ) -> dict[str, Any]:
        """
        Get grid layout configuration for positioning options.

        Args:
            grid_mode: Grid mode ("diamond" or "box")
            is_advanced: True for advanced picker, False for basic

        Returns:
            Dictionary with layout configuration
        """

    @abstractmethod
    def get_positions_for_mode(
        self, grid_mode: str, is_advanced: bool = False
    ) -> list[str]:
        """
        Get the list of positions to display for a given mode.

        Args:
            grid_mode: Grid mode ("diamond" or "box")
            is_advanced: True for 16 positions, False for 3 positions

        Returns:
            List of position keys to display
        """


class IStartPositionOrchestrator(ABC):
    """Interface for orchestrating start position operations."""

    @abstractmethod
    def handle_position_selection(self, position_key: str) -> bool:
        """
        Handle the complete workflow of position selection.

        Args:
            position_key: Position key selected by user

        Returns:
            True if selection was successful, False otherwise
        """

    @abstractmethod
    def get_position_data_for_display(
        self, position_key: str, grid_mode: str
    ) -> PictographData | None:
        """
        Get position data optimized for display in the UI.

        Args:
            position_key: Position key to get data for
            grid_mode: Grid mode ("diamond" or "box")

        Returns:
            PictographData optimized for display, None if not available
        """

    @abstractmethod
    def calculate_responsive_layout(
        self, container_size: Size, position_count: int
    ) -> dict[str, Any]:
        """
        Calculate responsive layout parameters for position options.

        Args:
            container_size: Size of the container widget
            position_count: Number of positions to display

        Returns:
            Dictionary with layout parameters (rows, cols, spacing, etc.)
        """
