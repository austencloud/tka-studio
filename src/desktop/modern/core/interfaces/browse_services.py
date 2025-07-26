"""
Browse Service Interfaces

Interfaces for browse-related services following clean architecture patterns.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from desktop.modern.domain.models.sequence_data import SequenceData
from PyQt6.QtWidgets import QWidget


class ISequenceDeletionService(ABC):
    """Interface for sequence deletion service."""

    @abstractmethod
    def delete_variation(
        self,
        word: str,
        thumbnails: List[str],
        variation_index: int,
        parent_widget: Optional[QWidget] = None,
    ) -> bool:
        """
        Delete a specific variation of a sequence.

        Args:
            word: The sequence word/name
            thumbnails: List of thumbnail file paths
            variation_index: Index of variation to delete
            parent_widget: Parent widget for dialogs

        Returns:
            True if deletion was successful, False if cancelled or failed
        """

    @abstractmethod
    def delete_entire_sequence(
        self, word: str, parent_widget: Optional[QWidget] = None
    ) -> bool:
        """
        Delete an entire sequence (all variations).

        Args:
            word: The sequence word/name to delete
            parent_widget: Parent widget for dialogs

        Returns:
            True if deletion was successful, False if cancelled or failed
        """


class IThumbnailFactory(ABC):
    """Interface for creating sequence thumbnail widgets."""

    @abstractmethod
    def create_thumbnail(
        self, sequence: SequenceData, thumbnail_width: int, sort_method: str
    ) -> QWidget:
        """
        Create a thumbnail widget for a sequence.

        Args:
            sequence: The sequence data
            thumbnail_width: Width for the thumbnail
            sort_method: Current sort method for display optimization

        Returns:
            QWidget containing the sequence thumbnail
        """


class ILayoutManager(ABC):
    """Interface for managing grid layout and sections."""

    @abstractmethod
    def clear_grid(self) -> None:
        """Clear all items from the grid layout."""

    @abstractmethod
    def add_section_header(self, section_name: str, current_row: int) -> int:
        """
        Add a section header to the grid.

        Args:
            section_name: Name of the section
            current_row: Current row position

        Returns:
            Updated row position after adding header
        """

    @abstractmethod
    def add_thumbnail_to_grid(self, thumbnail: QWidget, row: int, col: int) -> None:
        """
        Add a thumbnail widget to the grid at specified position.

        Args:
            thumbnail: The thumbnail widget
            row: Grid row position
            col: Grid column position
        """

    @abstractmethod
    def set_row_stretch(self, row: int, stretch: int) -> None:
        """Set stretch factor for a grid row."""

    @abstractmethod
    def get_row_count(self) -> int:
        """Get the current number of rows in the grid."""


class ILoadingStateManager(ABC):
    """Interface for managing loading states and progress."""

    @abstractmethod
    def show_loading_state(self) -> None:
        """Show loading UI and hide main content."""

    @abstractmethod
    def hide_loading_state(self) -> None:
        """Hide loading UI and show main content."""

    @abstractmethod
    def update_progress(self, current: int, total: int, message: str = "") -> None:
        """
        Update loading progress.

        Args:
            current: Current progress value
            total: Total progress value
            message: Optional status message
        """

    @abstractmethod
    def show_empty_state(self) -> None:
        """Show empty state when no sequences are found."""


class ISequenceSorter(ABC):
    """Interface for sorting sequences."""

    @abstractmethod
    def sort_sequences(
        self, sequences: List[SequenceData], sort_method: str
    ) -> List[SequenceData]:
        """
        Sort sequences based on the selected method.

        Args:
            sequences: List of sequences to sort
            sort_method: Sort method ('alphabetical', 'length', 'level', 'date_added')

        Returns:
            Sorted list of sequences
        """

    @abstractmethod
    def group_sequences_into_sections(
        self, sequences: List[SequenceData], sort_method: str
    ) -> Dict[str, List[SequenceData]]:
        """
        Group sequences into sections based on sort method.

        Args:
            sequences: List of sequences to group
            sort_method: Sort method to determine grouping

        Returns:
            Dictionary mapping section names to sequence lists
        """

    @abstractmethod
    def get_section_key(self, sequence: SequenceData, sort_method: str) -> str:
        """
        Get the section key for a sequence based on sort method.

        Args:
            sequence: The sequence data
            sort_method: Current sort method

        Returns:
            Section key string
        """


class INavigationHandler(ABC):
    """Interface for handling navigation and scrolling."""

    @abstractmethod
    def scroll_to_section(self, section_name: str) -> None:
        """
        Scroll to a specific section in the grid.

        Args:
            section_name: Name of the section to scroll to
        """

    @abstractmethod
    def update_navigation_sections(
        self, section_names: List[str], sort_method: str
    ) -> None:
        """
        Update the navigation sidebar with new sections.

        Args:
            section_names: List of section names
            sort_method: Current sort method
        """
