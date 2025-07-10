"""
Display Coordination Service

Pure business service for coordinating display operations without UI dependencies.
This service contains the business logic for how pictographs should be organized
and displayed, while delegating actual UI operations to adapters.

This service handles:
- Beat organization by letter types
- Section creation strategy and rules
- Pictograph assignment logic
- Display update coordination

No UI dependencies - completely testable in isolation.
"""

from typing import Dict, List, Tuple

from domain.models.beat_data import BeatData
from presentation.components.option_picker.types.letter_types import LetterType


class DisplayCoordinationService:
    """
    Pure business service for display coordination.

    Contains business rules for how beats should be organized and displayed,
    without any UI-specific implementation details.
    """

    def __init__(self):
        self._section_strategy = self._get_default_section_strategy()

    def _get_default_section_strategy(self) -> Dict[str, dict]:
        """
        Get the default section creation strategy.

        This defines the business rules for how sections should be organized:
        - Sections 1-3: Individual sections with natural content-based sizing
        - Sections 4-6: Horizontal layout in shared bottom row
        """
        return {
            "individual_sections": [
                LetterType.TYPE1,
                LetterType.TYPE2,
                LetterType.TYPE3,
            ],
            "bottom_row_sections": [
                LetterType.TYPE4,
                LetterType.TYPE5,
                LetterType.TYPE6,
            ],
            "total_sections": 6,
            "max_columns_per_section": 8,
        }

    def organize_beats_by_letter_type(
        self, beats: List[BeatData]
    ) -> Dict[str, List[Tuple[int, BeatData]]]:
        """
        Organize beats by their letter types with pool indices.

        Args:
            beats: List of beat data to organize

        Returns:
            Dict mapping letter types to lists of (pool_index, beat_data) tuples
        """
        from domain.models.letter_type_classifier import LetterTypeClassifier

        organized_beats = {}
        pool_index = 0

        for beat in beats:
            if beat and beat.letter:
                letter_type = LetterTypeClassifier.get_letter_type(beat.letter)

                if letter_type not in organized_beats:
                    organized_beats[letter_type] = []

                organized_beats[letter_type].append((pool_index, beat))
                pool_index += 1

        return organized_beats

    def calculate_section_requirements(
        self, organized_beats: Dict[str, List]
    ) -> Dict[str, dict]:
        """
        Calculate requirements for each section based on organized beats.

        Args:
            organized_beats: Beats organized by letter type

        Returns:
            Dict with section requirements including counts and layout needs
        """
        section_requirements = {}
        strategy = self._section_strategy

        for letter_type in (
            strategy["individual_sections"] + strategy["bottom_row_sections"]
        ):
            beat_count = len(organized_beats.get(letter_type, []))

            # Calculate rows needed (business rule: 8 columns max per section)
            columns = min(beat_count, strategy["max_columns_per_section"])
            rows = (beat_count + strategy["max_columns_per_section"] - 1) // strategy[
                "max_columns_per_section"
            ]

            section_requirements[letter_type] = {
                "beat_count": beat_count,
                "columns": columns,
                "rows": rows,
                "is_bottom_row": letter_type in strategy["bottom_row_sections"],
                "needs_shared_width": letter_type in strategy["bottom_row_sections"],
            }

        return section_requirements

    def determine_display_strategy(self, beats: List[BeatData]) -> Dict:
        """
        Determine the complete display strategy for the given beats.

        Args:
            beats: List of beats to display

        Returns:
            Dict with complete display strategy including organization and requirements
        """
        organized_beats = self.organize_beats_by_letter_type(beats)
        section_requirements = self.calculate_section_requirements(organized_beats)

        return {
            "organized_beats": organized_beats,
            "section_requirements": section_requirements,
            "section_strategy": self._section_strategy,
            "total_beats": len(beats),
            "sections_needed": len(
                [req for req in section_requirements.values() if req["beat_count"] > 0]
            ),
        }

    def get_section_creation_order(self) -> List[str]:
        """
        Get the order in which sections should be created.

        Returns:
            List of letter types in creation order
        """
        strategy = self._section_strategy
        return strategy["individual_sections"] + strategy["bottom_row_sections"]

    def should_use_shared_layout(self, letter_type: str) -> bool:
        """
        Determine if a letter type should use shared layout.

        Args:
            letter_type: The letter type to check

        Returns:
            True if the letter type should be in shared bottom row layout
        """
        return letter_type in self._section_strategy["bottom_row_sections"]

    def calculate_bottom_row_width_distribution(
        self, total_width: int, margins: int = 20
    ) -> Dict[str, int]:
        """
        Calculate width distribution for bottom row sections.

        Args:
            total_width: Total available width
            margins: Total margins to account for

        Returns:
            Dict mapping letter types to their calculated widths
        """
        available_width = total_width - margins
        section_width = (
            available_width // 3
        )  # Business rule: 3 sections share bottom row

        return {
            LetterType.TYPE4: section_width,
            LetterType.TYPE5: section_width,
            LetterType.TYPE6: section_width,
        }

    def validate_display_strategy(self, strategy: Dict) -> bool:
        """
        Validate that a display strategy is complete and valid.

        Args:
            strategy: Display strategy to validate

        Returns:
            True if strategy is valid
        """
        required_keys = [
            "organized_beats",
            "section_requirements",
            "section_strategy",
            "total_beats",
        ]

        if not all(key in strategy for key in required_keys):
            return False

        # Validate that all beats are accounted for
        total_organized = sum(
            len(beats) for beats in strategy["organized_beats"].values()
        )
        if total_organized != strategy["total_beats"]:
            return False

        return True

    def get_configuration(self) -> Dict:
        """Get the current display coordination configuration."""
        return {
            "section_strategy": self._section_strategy.copy(),
            "service_name": "DisplayCoordinationService",
            "version": "1.0",
        }
