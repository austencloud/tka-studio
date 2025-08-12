"""
Accordion Filter Panel Component

Main accordion container that manages multiple collapsible filter sections.
Only one section can be expanded at a time.
"""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from application.services.browse.dictionary_data_manager import DictionaryDataManager
from desktop.modern.domain.models.browse_models import FilterType

from .accordion_section import AccordionSection
from .section_title import SectionTitle


class AccordionFilterPanel(QWidget):
    """Main accordion container with multiple collapsible filter sections."""

    filter_selected = pyqtSignal(FilterType, object)

    def __init__(
        self,
        dictionary_manager: DictionaryDataManager,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.dictionary_manager = dictionary_manager
        self.sections = []
        self.current_expanded_section = None
        self.all_buttons = {}
        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self) -> None:
        """Setup the accordion panel layout with centered, cohesive spacing."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)  # Add margins for centering
        layout.setSpacing(8)  # Consistent, moderate spacing

        # Section title
        title = SectionTitle("Browse by Category")
        title.setStyleSheet("color: rgba(255, 255, 255, 0.9); margin-bottom: 12px;")
        layout.addWidget(title)

        # Create accordion sections
        sections_config = [
            (
                "📝 Starting Letter",
                FilterType.STARTING_LETTER,
                self._get_starting_letter_options(),
            ),
            (
                "📏 Length",
                FilterType.LENGTH,
                self._get_length_options(),
            ),
            (
                "📊 Difficulty",
                FilterType.DIFFICULTY,
                [
                    ("🟢 Beginner", "beginner"),
                    ("🟡 Intermediate", "intermediate"),
                    ("🔴 Advanced", "advanced"),
                ],
            ),
            (
                "🎯 Start Position",
                FilterType.STARTING_POSITION,
                self._get_starting_position_options(),
            ),
            (
                "👤 Author",
                FilterType.AUTHOR,
                self._get_author_options(),
            ),
            (
                "🎨 Grid Style",
                FilterType.GRID_MODE,
                self._get_grid_mode_options(),
            ),
        ]

        for title_text, filter_type, options in sections_config:
            section = AccordionSection(title_text, filter_type, options)
            section.filter_selected.connect(self.filter_selected.emit)
            section.expansion_requested.connect(self._on_section_expansion_requested)

            self.sections.append(section)
            self.all_buttons.update(section.get_buttons())
            layout.addWidget(section)

        # Add single stretch at bottom to center content and allow expansion
        layout.addStretch(1)

        # Auto-open the Starting Letter section (most commonly used)
        if self.sections:
            starting_letter_section = self.sections[
                0
            ]  # First section is Starting Letter
            starting_letter_section.expand()
            self.current_expanded_section = starting_letter_section

    def _get_starting_letter_options(self) -> list[str]:
        """Get all individual starting letters that actually exist in the data."""
        try:
            # Get all sequences and extract unique starting letters (like legacy)
            sequences = self.dictionary_manager.get_all_sequences()
            letters = set()
            for seq in sequences:
                if seq.word and seq.word.strip():
                    # Extract first letter like legacy: handle W vs W- properly
                    word = seq.word.strip()
                    if len(word) > 1 and word[1] == "-":
                        # Handle cases like "W-", "Σ-", etc.
                        first_letter = word[:2]
                    else:
                        # Handle single letters like "W", "A", etc.
                        first_letter = word[0]
                    letters.add(first_letter)

            # Return sorted list of actual letters found
            return (
                sorted(letters)
                if letters
                else [chr(i) for i in range(ord("A"), ord("Z") + 1)]
            )
        except Exception as e:
            print(f"⚠️ [ACCORDION] Error getting starting letters: {e}")
            # Fallback to full alphabet
            return [chr(i) for i in range(ord("A"), ord("Z") + 1)]

    def _get_length_options(self) -> list[str]:
        """Get all available sequence lengths that actually exist in the data."""
        try:
            # Get all sequences and extract unique lengths
            sequences = self.dictionary_manager.get_all_sequences()
            lengths = set()
            for seq in sequences:
                if seq.sequence_length and seq.sequence_length > 0:
                    lengths.add(seq.sequence_length)

            # Return sorted list of actual lengths found as strings
            return (
                [str(length) for length in sorted(lengths)]
                if lengths
                else ["3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
            )
        except Exception as e:
            print(f"⚠️ [ACCORDION] Error getting sequence lengths: {e}")
            # Fallback to common lengths
            return ["3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

    def _get_author_options(self) -> list[str]:
        """Get all available authors from the actual data."""
        try:
            authors = self.dictionary_manager.get_distinct_authors()
            # Return all authors, not just top 3
            return (
                authors if authors else ["Demo Author", "Test User", "Sample Creator"]
            )
        except Exception as e:
            print(f"⚠️ [ACCORDION] Error getting authors: {e}")
            return ["Demo Author", "Test User", "Sample Creator"]

    def _get_starting_position_options(self) -> list[str]:
        """Get all available starting positions that actually exist in the data."""
        try:
            # Get all sequences and extract unique starting positions
            sequences = self.dictionary_manager.get_all_sequences()
            positions = set()
            for seq in sequences:
                if seq.starting_position and seq.starting_position.strip():
                    # Capitalize first letter for display
                    position = seq.starting_position.strip().capitalize()
                    positions.add(position)

            # Return sorted list of actual positions found
            return sorted(positions) if positions else ["Alpha", "Beta", "Gamma"]
        except Exception as e:
            print(f"⚠️ [ACCORDION] Error getting starting positions: {e}")
            # Fallback to common positions
            return ["Alpha", "Beta", "Gamma"]

    def _get_grid_mode_options(self) -> list[tuple[str, str]]:
        """Get all available grid modes that actually exist in the data."""
        try:
            # Get all sequences and extract unique grid modes
            sequences = self.dictionary_manager.get_all_sequences()
            modes = set()
            for seq in sequences:
                if seq.grid_mode and seq.grid_mode.strip():
                    modes.add(seq.grid_mode.strip().lower())

            # Map to display format with icons
            mode_mapping = {
                "diamond": ("💎 Diamond", "diamond"),
                "box": ("⬜ Box", "box"),
                "mixed": ("🎭 Mixed", "mixed"),
            }

            # Return tuples for modes that exist in data
            result = []
            for mode in sorted(modes):
                if mode in mode_mapping:
                    result.append(mode_mapping[mode])
                else:
                    # Handle unknown modes gracefully
                    result.append((f"🔹 {mode.capitalize()}", mode))

            return (
                result
                if result
                else [
                    ("💎 Diamond", "diamond"),
                    ("⬜ Box", "box"),
                    ("🎭 Mixed", "mixed"),
                ]
            )
        except Exception as e:
            print(f"⚠️ [ACCORDION] Error getting grid modes: {e}")
            # Fallback to common modes
            return [("💎 Diamond", "diamond"), ("⬜ Box", "box"), ("🎭 Mixed", "mixed")]

    def _on_section_expansion_requested(
        self, requested_section: AccordionSection
    ) -> None:
        """Handle section expansion request - ensure only one section is open."""
        print(f"🎛️ [ACCORDION PANEL] Expansion requested: {requested_section.title}")

        # If the requested section is already expanded, collapse it
        if self.current_expanded_section == requested_section:
            requested_section.collapse()
            self.current_expanded_section = None
            return

        # Collapse currently expanded section if any
        if self.current_expanded_section:
            self.current_expanded_section.collapse()

        # Expand the requested section
        requested_section.expand()
        self.current_expanded_section = requested_section

    def get_all_buttons(self) -> dict:
        """Get all buttons from all sections for external access."""
        return self.all_buttons.copy()

    def set_active_filter(
        self, filter_type: FilterType | None, filter_value=None
    ) -> None:
        """Set active filter state for visual feedback."""
        # This method maintains compatibility with the existing FilterSelectionPanel
        # For now, we'll just log the active filter
        # TODO: Later implement visual feedback for active filters
        if filter_type and filter_value:
            print(
                f"🎯 [ACCORDION PANEL] Active filter: {filter_type.value} = {filter_value}"
            )
        else:
            print("🎯 [ACCORDION PANEL] No active filter")

    def _apply_styling(self) -> None:
        """Apply glassmorphism styling to the accordion panel."""
        self.setStyleSheet(
            """
            AccordionFilterPanel {
                background: transparent;
                border: none;
                margin: 0px;
                padding: 0px;
            }
        """
        )
