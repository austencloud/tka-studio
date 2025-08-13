"""
Workbench Integration - Practical Generation Architecture

Simple workbench integration without over-engineered service layers.
Direct, focused integration - around 80 lines.
"""

from __future__ import annotations

import logging

from desktop.modern.domain.models.pictograph_data import PictographData


logger = logging.getLogger(__name__)


class WorkbenchIntegrator:
    """
    Simple workbench integration for generated sequences.

    Handles updating the workbench with generated beats without
    complex service layers or over-engineered abstractions.
    """

    def __init__(self, workbench_manager=None):
        self.workbench_manager = workbench_manager
        self._arrow_positioning_orchestrator = None
        self._initialize_arrow_positioning()

    def update_workbench_with_sequence(
        self, sequence: list[PictographData], clear_existing: bool = True
    ) -> bool:
        """
        Update workbench with a generated sequence.

        Args:
            sequence: Generated sequence to add to workbench
            clear_existing: Whether to clear existing beats first

        Returns:
            True if successful, False otherwise
        """
        if not self.workbench_manager:
            logger.warning("No workbench manager available")
            return False

        if not sequence:
            logger.warning("Empty sequence provided")
            return False

        try:
            logger.info(
                f"🎯 Generating sequence with {len(sequence)} beats (one-at-a-time approach)"
            )

            # Clear existing beats if requested
            if clear_existing:
                self._clear_workbench()

            # CRITICAL FIX: Establish start position BEFORE adding beats
            if sequence:
                self._establish_start_position(sequence[0])

            # LEGACY-STYLE APPROACH: Add beats one at a time with visual feedback
            success_count = 0
            for i, pictograph in enumerate(sequence):
                logger.info(
                    f"🔄 Processing beat {i + 1}/{len(sequence)}: {pictograph.letter}"
                )

                if self._add_beat_individually(pictograph, i + 1):
                    success_count += 1
                    logger.debug(f"✅ Beat {i + 1} added successfully")

                    # Process events for visual feedback (like legacy system)
                    self._process_events_for_visual_feedback()
                else:
                    logger.warning(f"❌ Failed to add beat {i + 1}")

            logger.info(
                f"✅ Sequence generation complete: {success_count}/{len(sequence)} beats added"
            )
            return success_count == len(sequence)

        except Exception as e:
            logger.exception(f"❌ Failed to update workbench: {e}")
            return False

    def _clear_workbench(self) -> None:
        """Clear existing beats from workbench."""
        try:
            if hasattr(self.workbench_manager, "clear_beats"):
                self.workbench_manager.clear_beats()
            elif hasattr(self.workbench_manager, "clear"):
                self.workbench_manager.clear()
            else:
                logger.debug("Workbench manager doesn't support clearing")
        except Exception as e:
            logger.exception(f"Failed to clear workbench: {e}")

    def _add_beat_individually(
        self, pictograph: PictographData, beat_number: int
    ) -> bool:
        """
        Add a single beat to the workbench using legacy-style individual processing.

        This follows the proven legacy pattern where each beat goes through the full
        construct pipeline individually, ensuring proper arrow positioning.
        """
        try:
            # Apply arrow positioning to this individual beat (like legacy system)
            positioned_pictograph = self._apply_arrow_positioning_to_beat(pictograph)

            # Use workbench manager's individual beat methods
            if hasattr(self.workbench_manager, "create_new_beat_and_add_to_sequence"):
                # This is the legacy-style method that ensures proper construct pipeline
                self.workbench_manager.create_new_beat_and_add_to_sequence(
                    positioned_pictograph,
                    override_grow_sequence=True,
                    update_image_export_preview=False,
                )
                return True
            if hasattr(self.workbench_manager, "add_beat"):
                self.workbench_manager.add_beat(positioned_pictograph)
                return True
            if hasattr(self.workbench_manager, "add_pictograph"):
                self.workbench_manager.add_pictograph(positioned_pictograph)
                return True
            if hasattr(self.workbench_manager, "update_beat"):
                self.workbench_manager.update_beat(beat_number, positioned_pictograph)
                return True
            logger.warning(
                "Workbench manager doesn't support individual beat operations"
            )
            return False
        except Exception as e:
            logger.exception(f"Failed to add beat {beat_number} individually: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _apply_arrow_positioning_to_beat(
        self, pictograph: PictographData
    ) -> PictographData:
        """Apply arrow positioning to a single beat (individual processing)."""
        if not self._arrow_positioning_orchestrator:
            logger.warning("⚠️ No arrow positioning orchestrator for individual beat")
            return pictograph

        try:
            positioned_pictograph = (
                self._arrow_positioning_orchestrator.calculate_all_arrow_positions(
                    pictograph
                )
            )
            logger.debug(
                f"✅ Applied arrow positioning to individual beat {pictograph.letter}"
            )
            return positioned_pictograph
        except Exception as e:
            logger.warning(
                f"⚠️ Failed to apply arrow positioning to beat {pictograph.letter}: {e}"
            )
            return pictograph

    def _process_events_for_visual_feedback(self) -> None:
        """Process events for visual feedback during generation (like legacy system)."""
        try:
            # Import QApplication here to avoid circular imports
            from PyQt6.QtWidgets import QApplication

            QApplication.processEvents()
            logger.debug("🔄 Processed events for visual feedback")
        except Exception as e:
            logger.debug(f"Could not process events: {e}")

    def _add_beat_to_workbench(self, pictograph: PictographData) -> bool:
        """Legacy method - now redirects to individual processing."""
        return self._add_beat_individually(
            pictograph, pictograph.beat if hasattr(pictograph, "beat") else 1
        )

    def _establish_start_position(self, first_beat: PictographData) -> None:
        """
        Establish start position before adding sequence beats.

        This creates the proper foundation for the generated sequence by setting
        the start position in the workbench's start position beat view.
        """
        try:
            # Create start position data from the first beat's start position
            if hasattr(first_beat, "start_position") and first_beat.start_position:
                start_position_key = first_beat.start_position
                logger.debug(f"🎯 Establishing start position: {start_position_key}")

                # Use workbench manager's start position methods
                if hasattr(self.workbench_manager, "set_start_position_data"):
                    # Create start position beat data from the first beat
                    start_position_beat = self._create_start_position_beat_data(
                        first_beat
                    )
                    self.workbench_manager.set_start_position_data(
                        start_position_beat, start_position_key
                    )
                    logger.info(f"✅ Start position established: {start_position_key}")
                elif hasattr(self.workbench_manager, "set_start_position"):
                    self.workbench_manager.set_start_position(start_position_key)
                    logger.info(f"✅ Start position set: {start_position_key}")
                else:
                    logger.warning(
                        "Workbench manager doesn't support start position operations"
                    )
            else:
                logger.warning("First beat has no start position data")
        except Exception as e:
            logger.exception(f"Failed to establish start position: {e}")
            import traceback

            traceback.print_exc()

    def _create_start_position_beat_data(self, first_beat: PictographData):
        """Create start position beat data from the first beat."""
        try:
            # Import BeatData here to avoid circular imports
            from desktop.modern.domain.models.beat_data import BeatData

            # Create start position beat data based on first beat's start position
            start_position_beat = BeatData(
                letter=first_beat.letter,
                start_position=first_beat.start_position,
                end_position=first_beat.start_position,  # Start position has same start/end
                pictograph_data=first_beat,
                is_filled=True,
            )

            return start_position_beat
        except Exception as e:
            logger.exception(f"Failed to create start position beat data: {e}")
            return None

    def set_workbench_manager(self, workbench_manager) -> None:
        """Set the workbench manager."""
        self.workbench_manager = workbench_manager
        logger.debug("Updated workbench manager")

    def get_workbench_status(self) -> dict:
        """Get workbench status information."""
        return {
            "has_workbench_manager": self.workbench_manager is not None,
            "workbench_type": (
                type(self.workbench_manager).__name__
                if self.workbench_manager
                else None
            ),
        }

    def _initialize_arrow_positioning(self) -> None:
        """Initialize arrow positioning orchestrator for proper arrow rendering."""
        try:
            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
            )
            from desktop.modern.core.interfaces.positioning_services import (
                IArrowPositioningOrchestrator,
            )

            container = get_container()
            self._arrow_positioning_orchestrator = container.resolve(
                IArrowPositioningOrchestrator
            )
            logger.debug(
                "✅ Arrow positioning orchestrator initialized from DI container"
            )
        except Exception as e:
            logger.warning(
                f"⚠️ Could not initialize arrow positioning from DI container: {e}"
            )
            # Try fallback initialization
            self._try_fallback_arrow_positioning()

    def _apply_arrow_positioning_to_sequence(
        self, sequence: list[PictographData]
    ) -> list[PictographData]:
        """
        Apply proper arrow positioning and rotation to all pictographs in sequence.

        This ensures that generated sequences have correctly positioned and rotated arrows,
        just like manually created sequences.
        """
        if not self._arrow_positioning_orchestrator:
            logger.warning(
                "⚠️ No arrow positioning orchestrator - arrows may not be positioned correctly"
            )
            return sequence

        processed_sequence = []
        for pictograph in sequence:
            try:
                # Apply arrow positioning calculations to the pictograph
                positioned_pictograph = (
                    self._arrow_positioning_orchestrator.calculate_all_arrow_positions(
                        pictograph
                    )
                )
                processed_sequence.append(positioned_pictograph)
                logger.debug(f"✅ Applied arrow positioning to beat {pictograph.beat}")
            except Exception as e:
                logger.warning(
                    f"⚠️ Failed to apply arrow positioning to beat {pictograph.beat}: {e}"
                )
                # Fall back to original pictograph if positioning fails
                processed_sequence.append(pictograph)

        logger.info(f"✅ Applied arrow positioning to {len(processed_sequence)} beats")
        return processed_sequence

    def _try_fallback_arrow_positioning(self) -> None:
        """Try to create arrow positioning orchestrator with fallback initialization."""
        try:
            # Import all required services
            from desktop.modern.application.services.positioning.arrows.calculation.arrow_location_calculator import (
                ArrowLocationCalculatorService,
            )
            from desktop.modern.application.services.positioning.arrows.calculation.arrow_rotation_calculator import (
                ArrowRotationCalculatorService,
            )
            from desktop.modern.application.services.positioning.arrows.coordinate_system.arrow_coordinate_system_service import (
                ArrowCoordinateSystemService,
            )
            from desktop.modern.application.services.positioning.arrows.orchestration.arrow_adjustment_calculator import (
                ArrowAdjustmentCalculator,
            )
            from desktop.modern.application.services.positioning.arrows.orchestration.arrow_positioning_orchestrator import (
                ArrowPositioningOrchestrator,
            )

            # Create services with default configurations
            location_calculator = ArrowLocationCalculatorService()
            rotation_calculator = ArrowRotationCalculatorService()
            adjustment_calculator = ArrowAdjustmentCalculator()
            coordinate_system = ArrowCoordinateSystemService()

            # Create orchestrator with all dependencies
            self._arrow_positioning_orchestrator = ArrowPositioningOrchestrator(
                location_calculator=location_calculator,
                rotation_calculator=rotation_calculator,
                adjustment_calculator=adjustment_calculator,
                coordinate_system=coordinate_system,
            )
            logger.debug(
                "✅ Arrow positioning orchestrator initialized with fallback method"
            )
        except Exception as e:
            logger.warning(f"⚠️ Fallback arrow positioning initialization failed: {e}")
            self._arrow_positioning_orchestrator = None
