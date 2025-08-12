"""
Freeform Generator - Practical Generation Architecture

Focused freeform sequence generation without over-engineering.
Integrates with real TKA data and workbench - around 180 lines.
"""

from __future__ import annotations

import logging
import random

from PyQt6.QtCore import QCoreApplication

from desktop.modern.core.interfaces.generation_services import PropContinuity
from desktop.modern.domain.models.enums import RotationDirection
from desktop.modern.domain.models.generation_models import GenerationConfig
from desktop.modern.domain.models.pictograph_data import PictographData

from .data_and_filtering import (
    CSVToPictographConverter,
    PictographDataManager,
    PictographFilter,
)
from .turn_applicator import TurnApplicator


logger = logging.getLogger(__name__)


class FreeformGenerator:
    """
    Practical freeform sequence generator.

    Handles the complete freeform generation process with real TKA data,
    proper filtering, and workbench integration. No over-engineering.
    """

    def __init__(self, workbench_manager=None):
        self.data_manager = PictographDataManager()
        self.filter = PictographFilter()
        self.converter = CSVToPictographConverter()
        self.turn_applicator = TurnApplicator()
        self.workbench_manager = workbench_manager

        # Generation state
        self.current_end_position: str | None = None
        self.grid_mode: str | None = None
        self.blue_rot_dir: RotationDirection | None = None
        self.red_rot_dir: RotationDirection | None = None

    def generate_sequence(self, config: GenerationConfig) -> list[PictographData]:
        """
        Generate a freeform sequence using real TKA data.

        Args:
            config: Generation configuration

        Returns:
            List of generated PictographData objects
        """
        # Simple validation
        if not self._validate_config(config):
            return []

        logger.info(
            f"🎯 Starting freeform generation: length={config.length}, level={config.level}"
        )

        # Reset state
        self._reset_generation_state()

        # CRITICAL: Establish start position before generating sequence
        if not self._establish_start_position(config):
            logger.error("Failed to establish start position for sequence")
            return []

        # Determine rotation directions for continuous mode
        if config.prop_continuity == PropContinuity.CONTINUOUS:
            self._set_rotation_directions()

        # FIXED: Allocate turns for entire sequence using REAL legacy logic
        blue_turns_list, red_turns_list = (
            self.turn_applicator.allocate_turns_for_sequence(
                sequence_length=config.length,
                level=config.level,
                turn_intensity=config.turn_intensity,
            )
        )

        # Generate sequence
        sequence = []
        available_data = self.data_manager.get_all_data()

        for beat_num in range(1, config.length + 1):
            try:
                # Generate next beat
                pictograph = self._generate_next_beat(available_data, config, beat_num)

                if pictograph:
                    # FIXED: Apply pre-allocated turns
                    if config.level >= 2 and beat_num <= len(blue_turns_list):
                        blue_turns = blue_turns_list[beat_num - 1]
                        red_turns = red_turns_list[beat_num - 1]
                        pictograph = self.turn_applicator.apply_turns_to_pictograph(
                            pictograph, blue_turns, red_turns
                        )

                    sequence.append(pictograph)
                    self._update_generation_state(pictograph)

                    # Update workbench if available
                    if self.workbench_manager:
                        self._update_workbench(pictograph)

                    # Process events for UI responsiveness
                    self._process_events()

                    logger.debug(f"✅ Generated beat {beat_num}: {pictograph.letter}")
                else:
                    logger.warning(f"⚠️ Failed to generate beat {beat_num}")
                    break

            except Exception as e:
                logger.exception(f"❌ Error generating beat {beat_num}: {e}")
                break

        logger.info(f"🎉 Generated freeform sequence with {len(sequence)} beats")
        return sequence

    def _validate_config(self, config: GenerationConfig) -> bool:
        """Simple, direct validation without over-engineered validators."""
        if config.length <= 0:
            logger.error("Sequence length must be positive")
            return False

        if config.length > 32:
            logger.error("Sequence length cannot exceed 32")
            return False

        if config.level < 1 or config.level > 6:
            logger.error("Level must be between 1 and 6")
            return False

        if not self.data_manager.get_all_data():
            logger.error("No pictograph data available")
            return False

        return True

    def _reset_generation_state(self) -> None:
        """Reset generation state for new sequence."""
        self.current_end_position = None
        self.grid_mode = None
        self.blue_rot_dir = None
        self.red_rot_dir = None

    def _establish_start_position(self, config: GenerationConfig) -> bool:
        """
        Establish a start position for the sequence.

        This is critical for positional continuity - without a start position,
        the sequence has no logical flow.
        """
        try:
            # TODO: In the future, get current start position from workbench
            # For now, create a random valid start position based on grid mode

            # Determine grid mode from config
            grid_mode = config.grid_mode.value if config.grid_mode else "diamond"

            # Get valid start positions for the grid mode
            if grid_mode == "diamond":
                start_positions = ["alpha1", "beta5", "gamma11"]
            else:  # box mode
                start_positions = ["alpha2", "beta6", "gamma12"]

            # Choose random start position
            chosen_start = random.choice(start_positions)

            # Set the current end position to this start position
            # This ensures the first beat will start from this position
            self.current_end_position = chosen_start
            self.grid_mode = grid_mode

            logger.info(
                f"✅ Established start position: {chosen_start} (grid: {grid_mode})"
            )
            return True

        except Exception as e:
            logger.exception(f"Failed to establish start position: {e}")
            return False

    def _set_rotation_directions(self) -> None:
        """Set rotation directions for continuous prop mode."""
        self.blue_rot_dir = random.choice(
            [RotationDirection.CLOCKWISE, RotationDirection.COUNTER_CLOCKWISE]
        )
        self.red_rot_dir = random.choice(
            [RotationDirection.CLOCKWISE, RotationDirection.COUNTER_CLOCKWISE]
        )
        logger.debug(
            f"Continuous mode: blue={self.blue_rot_dir.value}, red={self.red_rot_dir.value}"
        )

    def _generate_next_beat(
        self, available_data: list[dict], config: GenerationConfig, beat_num: int
    ) -> PictographData | None:
        """Generate the next beat in the sequence."""

        # Filter options
        filtered_options = self.filter.filter_options(
            available_data,
            letter_types=config.letter_types,
            current_end_position=self.current_end_position,
            grid_mode=self.grid_mode,
            prop_continuity=config.prop_continuity,
            blue_rot_dir=self.blue_rot_dir.value if self.blue_rot_dir else None,
            red_rot_dir=self.red_rot_dir.value if self.red_rot_dir else None,
        )

        if not filtered_options:
            logger.error(f"No valid options available for beat {beat_num}")
            return None

        # Select random option
        selected_csv = random.choice(filtered_options)
        logger.debug(
            f"Selected from {len(filtered_options)} options for beat {beat_num}"
        )

        # Convert to PictographData
        pictograph = self.converter.convert(selected_csv, beat_num)
        if not pictograph:
            logger.error(f"Failed to convert CSV data for beat {beat_num}")
            return None

        return pictograph

    def _update_generation_state(self, pictograph: PictographData) -> None:
        """Update generation state after adding a beat."""
        # Update end position for next beat's positional continuity
        self.current_end_position = pictograph.end_position

        # Set grid mode from first beat
        if not self.grid_mode:
            self.grid_mode = self.filter.determine_grid_mode(pictograph.start_position)
            if self.grid_mode:
                logger.debug(f"Grid mode set to: {self.grid_mode}")

    def _update_workbench(self, pictograph: PictographData) -> None:
        """Update workbench with new beat."""
        try:
            if hasattr(self.workbench_manager, "add_beat"):
                self.workbench_manager.add_beat(pictograph)
            elif hasattr(self.workbench_manager, "update_beat"):
                self.workbench_manager.update_beat(pictograph.beat, pictograph)
            else:
                logger.debug("Workbench manager doesn't support beat updates")
        except Exception as e:
            logger.exception(f"Failed to update workbench: {e}")

    def _process_events(self) -> None:
        """Process Qt events for UI responsiveness."""
        try:
            QCoreApplication.processEvents()
        except Exception:
            pass  # No Qt available or other error

    def get_generation_stats(self) -> dict:
        """Get statistics about the generator."""
        return {
            "total_pictographs": len(self.data_manager.get_all_data()),
            "diamond_pictographs": len(self.data_manager.get_diamond_data()),
            "box_pictographs": len(self.data_manager.get_box_data()),
            "current_end_position": self.current_end_position,
            "current_grid_mode": self.grid_mode,
            "has_workbench": self.workbench_manager is not None,
        }

    def set_workbench_manager(self, workbench_manager) -> None:
        """Set the workbench manager for UI integration."""
        self.workbench_manager = workbench_manager
        logger.debug("Updated workbench manager")

    def create_start_position_beat(self, start_position: str) -> PictographData | None:
        """
        Create a start position beat for the sequence.

        Args:
            start_position: The desired start position

        Returns:
            PictographData for start position or None if not found
        """
        try:
            # Find pictographs where start_pos == end_pos (true start positions)
            start_options = []
            for data in self.data_manager.get_all_data():
                if (
                    data.get("start_pos") == start_position
                    and data.get("end_pos") == start_position
                ):
                    start_options.append(data)

            if not start_options:
                logger.warning(f"No start position options found for {start_position}")
                return None

            # Select random start option
            selected = random.choice(start_options)
            pictograph = self.converter.convert(
                selected, 0
            )  # Beat 0 for start position

            if pictograph:
                # Update state
                self.current_end_position = pictograph.end_position
                self.grid_mode = self.filter.determine_grid_mode(
                    pictograph.start_position
                )
                logger.info(f"✅ Created start position: {start_position}")

            return pictograph

        except Exception as e:
            logger.exception(f"Failed to create start position beat: {e}")
            return None
