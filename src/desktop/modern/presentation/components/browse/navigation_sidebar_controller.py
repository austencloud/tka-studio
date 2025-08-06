"""
Navigation Sidebar Controller

Controls the navigation sidebar for the sequence browser panel.
Manages section navigation, scrolling, and progressive updates.
"""

from __future__ import annotations

from collections.abc import Callable
import logging

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QScrollArea

from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.components.browse.modern_navigation_sidebar import (
    ModernNavigationSidebar as NavigationSidebar,
)


logger = logging.getLogger(__name__)


class NavigationSidebarController:
    """
    Controller for managing navigation sidebar operations.

    Handles:
    - Section navigation and scrolling
    - Progressive section updates
    - Section selection events
    - Scroll position management
    """

    def __init__(
        self,
        navigation_sidebar: NavigationSidebar | None = None,
        scroll_area: QScrollArea | None = None,
    ):
        """
        Initialize the navigation sidebar controller.

        Args:
            navigation_sidebar: The navigation sidebar widget
            scroll_area: The main scroll area for content
        """
        self.navigation_sidebar = navigation_sidebar
        self.scroll_area = scroll_area

        # Section tracking
        self.current_sections: dict[str, int] = {}  # section_name -> sequence_count
        self.section_positions: dict[str, int] = {}  # section_name -> scroll_position

        # Progressive update timer
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self._perform_navigation_update)

        # Callbacks
        self.section_selected_callback: Callable[[str], None] | None = None

        self._connect_signals()

    def _connect_signals(self) -> None:
        """Connect navigation sidebar signals."""
        if self.navigation_sidebar:
            self.navigation_sidebar.section_selected.connect(self._on_section_selected)

    def set_section_selected_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for section selection events."""
        self.section_selected_callback = callback

    def update_navigation_sections(
        self, sequences: list[SequenceData], sort_method: str
    ) -> None:
        """
        Update navigation sections based on loaded sequences.

        Args:
            sequences: List of loaded sequences
            sort_method: Current sort method for grouping
        """
        logger.info(f"🧭 [NAVIGATION] Updating sections for {len(sequences)} sequences")

        # Group sequences by section
        sections = self._group_sequences_by_section(sequences, sort_method)

        # Update section counts
        self.current_sections = {
            section_name: len(section_sequences)
            for section_name, section_sequences in sections.items()
        }

        # Update navigation sidebar
        if self.navigation_sidebar:
            self.navigation_sidebar.update_sections(self.current_sections)

    def update_navigation_progressively(self) -> None:
        """Schedule a progressive navigation update with debouncing."""
        # Use timer to debounce rapid updates during progressive loading
        self.update_timer.start(100)  # 100ms delay

    def _perform_navigation_update(self) -> None:
        """Perform the actual navigation update."""
        if self.navigation_sidebar:
            self.navigation_sidebar.update_sections(self.current_sections)

    def scroll_to_section(self, section_name: str) -> None:
        """
        Scroll to a specific section.

        Args:
            section_name: Name of the section to scroll to
        """
        logger.info(f"📍 [NAVIGATION] Scrolling to section: {section_name}")

        if not self.scroll_area:
            logger.warning("⚠️ [NAVIGATION] No scroll area available for scrolling")
            return

        # Get section position if available
        if section_name in self.section_positions:
            position = self.section_positions[section_name]
            vertical_scrollbar = self.scroll_area.verticalScrollBar()
            if vertical_scrollbar:
                vertical_scrollbar.setValue(position)
                logger.info(f"📍 [NAVIGATION] Scrolled to position {position}")
        else:
            logger.warning(
                f"⚠️ [NAVIGATION] Section '{section_name}' position not found"
            )

    def update_section_position(self, section_name: str, position: int) -> None:
        """
        Update the scroll position for a section.

        Args:
            section_name: Name of the section
            position: Scroll position for the section
        """
        self.section_positions[section_name] = position

    def add_section_progressively(self, section_name: str, sequence_count: int) -> None:
        """
        Add or update a section during progressive loading.

        Args:
            section_name: Name of the section
            sequence_count: Number of sequences in the section
        """
        if section_name in self.current_sections:
            self.current_sections[section_name] += sequence_count
        else:
            self.current_sections[section_name] = sequence_count

        # Schedule progressive update
        self.update_navigation_progressively()

    def _on_section_selected(self, section_name: str) -> None:
        """Handle section selection from navigation sidebar."""
        logger.info(f"🎯 [NAVIGATION] Section selected: {section_name}")

        # Scroll to section
        self.scroll_to_section(section_name)

        # Call callback if set
        if self.section_selected_callback:
            self.section_selected_callback(section_name)

    def _group_sequences_by_section(
        self, sequences: list[SequenceData], sort_method: str
    ) -> dict[str, list[SequenceData]]:
        """
        Group sequences by section based on sort method.

        Args:
            sequences: List of sequences to group
            sort_method: Method for grouping

        Returns:
            Dictionary mapping section names to sequence lists
        """
        sections: dict[str, list[SequenceData]] = {}

        for sequence in sequences:
            section_name = self._get_section_name(sequence, sort_method)

            if section_name not in sections:
                sections[section_name] = []

            sections[section_name].append(sequence)

        return sections

    def _get_section_name(self, sequence: SequenceData, sort_method: str) -> str:
        """
        Get the section name for a sequence based on sort method.

        Args:
            sequence: The sequence to categorize
            sort_method: The sorting method

        Returns:
            Section name for the sequence
        """
        if sort_method == "difficulty":
            return sequence.difficulty or "Unknown Difficulty"
        if sort_method == "length":
            return f"Length {sequence.length or 'Unknown'}"
        if sort_method == "alphabetical":
            if sequence.word:
                first_letter = sequence.word[0].upper()
                return f"Starting with {first_letter}"
            return "Unknown"
        return "All Sequences"

    def clear_sections(self) -> None:
        """Clear all sections from navigation."""
        logger.info("🧹 [NAVIGATION] Clearing all sections")

        self.current_sections.clear()
        self.section_positions.clear()

        if self.navigation_sidebar:
            self.navigation_sidebar.clear_sections()

    def get_current_sections(self) -> dict[str, int]:
        """Get the current sections and their counts."""
        return self.current_sections.copy()

    def set_widgets(
        self,
        navigation_sidebar: NavigationSidebar | None = None,
        scroll_area: QScrollArea | None = None,
    ) -> None:
        """
        Update widget references.

        Args:
            navigation_sidebar: The navigation sidebar widget
            scroll_area: The main scroll area for content
        """
        if navigation_sidebar is not None:
            # Disconnect old signals
            if self.navigation_sidebar:
                self.navigation_sidebar.section_selected.disconnect()

            self.navigation_sidebar = navigation_sidebar
            self._connect_signals()

        if scroll_area is not None:
            self.scroll_area = scroll_area
