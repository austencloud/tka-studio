"""
Option Picker Display Service

Pure business service for option picker display logic and coordination.
This service contains all the business rules for how beats should be organized,
displayed, and managed without any UI dependencies.

This service handles:
- Beat organization and classification
- Display strategy calculation
- Section requirements determination
- Pictograph assignment coordination
- Display state management

No UI dependencies - completely testable in isolation.
"""

import logging
from typing import Any, Callable, Dict, List, Tuple

from core.interfaces.option_picker_services import IOptionPickerDisplayService
from domain.models.letter_type_classifier import LetterType, LetterTypeClassifier
from domain.models.pictograph_models import PictographData

logger = logging.getLogger(__name__)


class OptionPickerDisplayManager(IOptionPickerDisplayService):
    """
    Pure business service for option picker display logic.

    Contains all business rules for pictograph organization, display strategy,
    and section requirements without any UI dependencies.
    """

    def __init__(self):
        """Initialize the display service with business configuration."""
        self._section_strategy = self._get_default_section_strategy()
        self._current_pictographs: List[PictographData] = []
        self._current_display_strategy: Dict = {}
        self._display_state = {
            "initialized": False,
            "sections_created": False,
            "pictographs_assigned": False,
        }

    def _get_default_section_strategy(self) -> Dict[str, any]:
        """
        Get the default section creation strategy.

        Business rules for section organization:
        - Sections 1-3: Individual sections with natural content-based sizing
        - Sections 4-6: Horizontal layout in shared bottom row
        - Maximum 8 columns per section
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
            "bottom_row_shared": True,
            "natural_sizing": True,
        }

    def initialize_display_strategy(
        self, configuration: Dict[str, any] = None
    ) -> Dict[str, any]:
        """
        Initialize the display service with configuration.

        Args:
            configuration: Optional display configuration override

        Returns:
            Dict with initialization results and display strategy
        """
        try:
            if configuration:
                self._section_strategy.update(configuration)

            self._display_state["initialized"] = True

            # Return initialization configuration for UI layer
            return {
                "success": True,
                "section_strategy": self._section_strategy.copy(),
                "display_state": self._display_state.copy(),
                "sections_to_create": self.get_section_creation_order(),
            }

        except Exception as e:
            logger.error(f"Error initializing display service: {e}")
            return {"success": False, "error": str(e)}

    def create_sections(self) -> Dict[str, any]:
        """
        Calculate section creation requirements.

        Returns:
            Dict with section creation specifications
        """
        try:
            if not self._display_state["initialized"]:
                raise ValueError("Display service not initialized")

            section_specs = {}
            strategy = self._section_strategy

            # Individual sections (1-3)
            for letter_type in strategy["individual_sections"]:
                section_specs[letter_type] = {
                    "type": letter_type,
                    "layout_type": "individual",
                    "natural_sizing": True,
                    "shared_width": False,
                    "creation_order": strategy["individual_sections"].index(
                        letter_type
                    ),
                }

            # Bottom row sections (4-6)
            for letter_type in strategy["bottom_row_sections"]:
                section_specs[letter_type] = {
                    "type": letter_type,
                    "layout_type": "bottom_row",
                    "natural_sizing": False,
                    "shared_width": True,
                    "creation_order": len(strategy["individual_sections"])
                    + strategy["bottom_row_sections"].index(letter_type),
                }

            self._display_state["sections_created"] = True

            return {
                "success": True,
                "section_specifications": section_specs,
                "bottom_row_configuration": {
                    "sections": strategy["bottom_row_sections"],
                    "shared_container": True,
                    "equal_width_distribution": True,
                },
            }

        except Exception as e:
            logger.error(f"Error creating sections: {e}")
            return {"success": False, "error": str(e)}

    def update_pictograph_display(
        self, pictograph_options: List[PictographData]
    ) -> Dict[str, any]:
        """
        Calculate display update requirements for new pictograph options.

        Args:
            pictograph_options: List of pictograph data to display

        Returns:
            Dict with complete display update specifications
        """
        try:
            if not self._display_state["sections_created"]:
                logger.warning("Sections not created yet, creating them first")
                section_result = self.create_sections()
                if not section_result["success"]:
                    return section_result

            # Store current pictographs
            self._current_pictographs = pictograph_options.copy()

            # Organize pictographs by letter type
            organized_pictographs = self._organize_pictographs_by_letter_type(
                pictograph_options
            )

            # Calculate section requirements
            section_requirements = self._calculate_section_requirements(
                organized_pictographs
            )

            # Create complete display strategy
            display_strategy = {
                "organized_pictographs": organized_pictographs,
                "section_requirements": section_requirements,
                "section_strategy": self._section_strategy,
                "total_pictographs": len(pictograph_options),
                "sections_needed": len(
                    [
                        req
                        for req in section_requirements.values()
                        if req["beat_count"] > 0
                    ]
                ),
                "pictograph_assignments": self._calculate_pictograph_assignments(
                    organized_pictographs
                ),
            }

            self._current_display_strategy = display_strategy
            self._display_state["pictographs_assigned"] = True

            return {
                "success": True,
                "display_strategy": display_strategy,
                "update_requirements": self._generate_update_requirements(
                    display_strategy
                ),
            }

        except Exception as e:
            logger.error(f"Error updating beat display: {e}")
            return {"success": False, "error": str(e)}

    def _organize_pictographs_by_letter_type(
        self, pictographs: List[PictographData]
    ) -> Dict[str, List[Tuple[int, PictographData]]]:
        """
        Organize pictographs by their letter types with pool indices.

        Args:
            pictographs: List of pictograph data to organize

        Returns:
            Dict mapping letter types to lists of (pool_index, pictograph_data) tuples
        """
        organized_pictographs = {}
        pool_index = 0

        for pictograph in pictographs:
            if pictograph and pictograph.letter:
                letter_type = LetterTypeClassifier.get_letter_type(pictograph.letter)

                if letter_type not in organized_pictographs:
                    organized_pictographs[letter_type] = []

                organized_pictographs[letter_type].append((pool_index, pictograph))
                pool_index += 1

        return organized_pictographs

    def _calculate_section_requirements(
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
                "beats": organized_beats.get(letter_type, []),
            }

        return section_requirements

    def _calculate_pictograph_assignments(
        self, organized_beats: Dict[str, List]
    ) -> Dict[str, List[Dict]]:
        """
        Calculate pictograph frame assignments for each section.

        Args:
            organized_beats: Beats organized by letter type

        Returns:
            Dict mapping section types to pictograph assignment specifications
        """
        assignments = {}

        for letter_type, beats in organized_beats.items():
            section_assignments = []

            for pool_index, beat in beats:
                assignment = {
                    "pool_index": pool_index,
                    "beat_data": beat,
                    "letter": beat.letter,
                    "letter_type": letter_type,
                    "pictograph_key": f"{beat.letter}_{pool_index}",
                    "metadata": {
                        "end_pos": getattr(beat, "end_pos", None),
                        "beat_number": getattr(beat, "beat_number", None),
                    },
                }
                section_assignments.append(assignment)

            assignments[letter_type] = section_assignments

        return assignments

    def _generate_update_requirements(self, display_strategy: Dict) -> Dict[str, any]:
        """
        Generate specific update requirements for UI implementation.

        Args:
            display_strategy: Complete display strategy

        Returns:
            Dict with specific update requirements
        """
        return {
            "sections_to_update": list(display_strategy["section_requirements"].keys()),
            "total_pictographs_needed": display_strategy["total_pictographs"],
            "pool_reset_required": True,
            "assignment_specifications": display_strategy["pictograph_assignments"],
            "layout_updates_needed": {
                "bottom_row": any(
                    req["is_bottom_row"]
                    for req in display_strategy["section_requirements"].values()
                ),
                "individual_sections": any(
                    not req["is_bottom_row"]
                    for req in display_strategy["section_requirements"].values()
                ),
            },
        }

    def get_section_creation_order(self) -> List[str]:
        """
        Get the order in which sections should be created.

        Returns:
            List of letter types in creation order
        """
        strategy = self._section_strategy
        return strategy["individual_sections"] + strategy["bottom_row_sections"]

    def calculate_layout_dimensions(
        self, container_width: int, container_height: int
    ) -> Dict[str, Dict]:
        """
        Calculate layout dimensions for all sections.

        Args:
            container_width: Available container width
            container_height: Available container height

        Returns:
            Dict with dimension calculations for each section
        """
        dimensions = {}
        strategy = self._section_strategy

        # Calculate dimensions for individual sections (natural sizing)
        for letter_type in strategy["individual_sections"]:
            dimensions[letter_type] = {
                "width": "natural",  # Let content determine width
                "height": "natural",  # Let content determine height
                "sizing_mode": "content_based",
            }

        # Calculate dimensions for bottom row sections (shared width)
        margins = 20  # Business rule: standard margins
        available_width = container_width - margins
        section_width = (
            available_width // 3
        )  # Business rule: 3 sections share bottom row

        for letter_type in strategy["bottom_row_sections"]:
            dimensions[letter_type] = {
                "width": section_width,
                "height": "natural",
                "sizing_mode": "fixed_width_natural_height",
            }

        return dimensions

    def get_current_display_state(self) -> Dict[str, any]:
        """Get the current display state and strategy."""
        return {
            "display_state": self._display_state.copy(),
            "current_strategy": self._current_display_strategy.copy(),
            "beat_count": len(self._current_beats),
            "configuration": self._section_strategy.copy(),
        }

    def reset_display(self) -> Dict[str, any]:
        """Reset the display service to initial state."""
        self._current_beats.clear()
        self._current_display_strategy.clear()
        self._display_state.update({"sections_created": False, "beats_assigned": False})

        return {
            "success": True,
            "reset_complete": True,
            "display_state": self._display_state.copy(),
        }

    # Interface compliance methods - delegate to existing business logic
    def initialize_display(
        self,
        sections_container: Any,
        sections_layout: Any,
        pool_manager: Any,
        option_picker_size_provider: Callable,
    ) -> None:
        """Initialize the display components (interface compliance)."""
        # Store references for UI coordination
        self._sections_container = sections_container
        self._sections_layout = sections_layout
        self._pool_manager = pool_manager
        self._size_provider = option_picker_size_provider

        # Initialize using existing business logic
        result = self.initialize_display_strategy({})
        if not result.get("success", False):
            logger.warning(f"Display initialization had issues: {result}")

    def ensure_sections_visible(self) -> None:
        """Ensure all sections are visible after updates (interface compliance)."""
        # This is a UI concern - log for now, implement if needed
        logger.debug("ensure_sections_visible called - UI implementation needed")

    def resize_sections(self) -> None:
        """Resize sections to fit current container (interface compliance)."""
        # This is a UI concern - log for now, implement if needed
        logger.debug("resize_sections called - UI implementation needed")

    def get_sections(self) -> Dict[str, Any]:
        """Get current display sections (interface compliance)."""
        # Return section information from current strategy
        if not self._current_display_strategy:
            return {}

        sections = {}
        section_reqs = self._current_display_strategy.get("section_requirements", {})
        for letter_type, req in section_reqs.items():
            sections[letter_type] = {
                "letter_type": letter_type,
                "beat_count": len(req.get("beats", [])),
                "requirements": req,
            }
        return sections

    def cleanup(self) -> None:
        """Clean up display resources (interface compliance)."""
        self.reset_display()
        # Clear any stored UI references
        self._sections_container = None
        self._sections_layout = None
        self._pool_manager = None
        self._size_provider = None
        logger.info("Display service cleaned up")
