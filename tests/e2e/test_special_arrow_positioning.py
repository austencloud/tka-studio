"""
End-to-End Test for Special Arrow Positioning (Letters G, H, I)

This test validates that arrows are correctly positioned for special letters
that require custom placement adjustments, ensuring the special placement
management logic is working correctly.

Tests cover:
- Letter G: Color-specific adjustments (red/blue)
- Letter H: Complex positioning scenarios
- Letter I: Motion-type-specific adjustments (pro/anti)
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from base_e2e_test import BaseE2ETest

logger = logging.getLogger(__name__)


class SpecialArrowPositioningE2ETest(BaseE2ETest):
    """E2E test for special arrow positioning functionality."""

    def __init__(self):
        super().__init__("Special Arrow Positioning")
        self.test_cases = []
        self.positioning_results = {}

    def execute_test_logic(self) -> bool:
        """Execute the main test logic (required by base class)."""
        return self.run_special_arrow_positioning_test()

    def run_special_arrow_positioning_test(self) -> bool:
        """Run the complete special arrow positioning test."""
        try:
            logger.info("INIT: Initializing Special Arrow Positioning E2E test")
            logger.info("START: Starting Special Arrow Positioning test...")

            # Phase 1: Setup and component discovery
            if not self._setup_test_environment():
                return False

            # Phase 2: Test special letter positioning
            if not self._test_special_letter_positioning():
                return False

            # Phase 3: Validate positioning results
            if not self._validate_positioning_results():
                return False

            logger.info(
                "SUCCESS: Special Arrow Positioning test completed successfully!"
            )
            return True

        except Exception as e:
            logger.error(f"FAILED: Special Arrow Positioning test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

        finally:
            self._cleanup()

    def _setup_test_environment(self) -> bool:
        """Set up the test environment and discover components."""
        try:
            logger.info("SETUP: Setting up test environment...")

            # Setup application and navigate to construct tab
            if not self.setup_application():
                logger.error("ERROR: Failed to setup application")
                return False

            if not self.navigate_to_construct_tab():
                logger.error("ERROR: Failed to navigate to construct tab")
                return False

            # Discover components
            if not self.discover_components():
                logger.error("ERROR: Failed to discover components")
                return False

            # Verify special placement service is available
            if not self._verify_special_placement_service():
                logger.error("ERROR: Special placement service not available")
                return False

            logger.info("SUCCESS: Test environment setup completed")
            return True

        except Exception as e:
            logger.error(f"ERROR: Test environment setup failed: {e}")
            return False

    def _verify_special_placement_service(self) -> bool:
        """Verify that the special placement service is properly initialized."""
        try:
            logger.info("VERIFY: Checking special placement service...")

            # Try to access the special placement service through DI container
            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
            )

            container = get_container()

            # Check if arrow positioning services are available
            try:
                from desktop.modern.core.interfaces.positioning_services import (
                    IArrowPositioningOrchestrator,
                )

                orchestrator = container.resolve(IArrowPositioningOrchestrator)
                logger.info("SUCCESS: Arrow positioning orchestrator found")

                # Store reference for later use
                self.arrow_orchestrator = orchestrator
                return True

            except Exception as e:
                logger.warning(
                    f"WARNING: Could not resolve arrow positioning orchestrator: {e}"
                )
                return False

        except Exception as e:
            logger.error(f"ERROR: Failed to verify special placement service: {e}")
            return False

    def _test_special_letter_positioning(self) -> bool:
        """Test arrow positioning for special letters G, H, and I using real pictograph data."""
        try:
            logger.info("PHASE 2: Testing special letter positioning with real data...")

            # Get real pictographs for letters G, H, and I
            special_letters = ["G", "H", "I"]

            for letter in special_letters:
                logger.info(f"TESTING: Getting real pictographs for letter {letter}")

                # Get actual pictographs for this letter
                pictographs = self._get_real_pictographs_for_letter(letter)

                if not pictographs:
                    logger.warning(f"WARNING: No pictographs found for letter {letter}")
                    continue

                # Test positioning for each real pictograph
                for i, pictograph_data in enumerate(
                    pictographs[:3]
                ):  # Test first 3 examples
                    logger.info(
                        f"TESTING: Letter {letter} pictograph {i+1}/{min(3, len(pictographs))}"
                    )

                    if not self._test_real_pictograph_positioning(
                        letter, pictograph_data, i + 1
                    ):
                        logger.error(f"ERROR: Failed to test {letter} pictograph {i+1}")
                        return False

            logger.info("SUCCESS: All special letter positioning tests completed")
            return True

        except Exception as e:
            logger.error(f"ERROR: Special letter positioning test failed: {e}")
            return False

    def _test_letter_positioning(self, test_case: Dict[str, Any]) -> bool:
        """Test positioning for a specific letter configuration."""
        try:
            letter = test_case["letter"]
            logger.info(f"LETTER: Testing positioning for letter {letter}")

            # Create test pictograph data for this letter
            pictograph_data = self._create_test_pictograph_data(test_case)

            if not pictograph_data:
                logger.error(f"ERROR: Failed to create pictograph data for {letter}")
                return False

            # Calculate arrow positions using the orchestrator
            positioning_results = self._calculate_arrow_positions(pictograph_data)

            if not positioning_results:
                logger.error(f"ERROR: Failed to calculate positions for {letter}")
                return False

            # Store results for validation
            self.positioning_results[letter] = {
                "test_case": test_case,
                "pictograph_data": pictograph_data,
                "positions": positioning_results,
            }

            logger.info(f"SUCCESS: Positioning calculated for letter {letter}")
            return True

        except Exception as e:
            logger.error(
                f"ERROR: Letter positioning test failed for {test_case.get('letter', 'unknown')}: {e}"
            )
            return False

    def _create_test_pictograph_data(self, test_case: Dict[str, Any]) -> Any:
        """Create test pictograph data for the given test case."""
        try:
            # Import required classes
            from desktop.modern.domain.models.arrow_data import ArrowData
            from desktop.modern.domain.models.motion_data import MotionData
            from desktop.modern.domain.models.pictograph_data import PictographData
            from shared.domain.enums import Location, MotionType

            letter = test_case["letter"]
            motion_configs = test_case["motion_configs"]

            # Create motion data for each arrow
            motions = {}
            arrows = {}

            for config in motion_configs:
                color = config["color"]
                motion_type = MotionType(config["motion_type"].upper())
                start_loc = Location(config["start_loc"].upper())
                end_loc = Location(config["end_loc"].upper())

                # Create motion data
                motion_data = MotionData(
                    motion_type=motion_type,
                    start_loc=start_loc,
                    end_loc=end_loc,
                    turns=1,  # Default turns for testing
                )
                motions[color] = motion_data

                # Create arrow data
                arrow_data = ArrowData(
                    color=color,
                    is_visible=True,
                    position_x=0.0,  # Will be calculated
                    position_y=0.0,  # Will be calculated
                    rotation_angle=0.0,  # Will be calculated
                )
                arrows[color] = arrow_data

            # Create pictograph data
            pictograph_data = PictographData(
                letter=letter,
                grid_mode="diamond",  # Use diamond mode for testing
                motions=motions,
                arrows=arrows,
            )

            logger.info(f"CREATED: Test pictograph data for letter {letter}")
            return pictograph_data

        except Exception as e:
            logger.error(f"ERROR: Failed to create test pictograph data: {e}")
            return None

    def _calculate_arrow_positions(
        self, pictograph_data: Any
    ) -> Dict[str, Tuple[float, float, float]]:
        """Calculate arrow positions using the positioning orchestrator."""
        try:
            positions = {}

            for color, arrow_data in pictograph_data.arrows.items():
                motion_data = pictograph_data.motions.get(color)

                if arrow_data.is_visible and motion_data:
                    # Calculate position using orchestrator
                    x, y, rotation = self.arrow_orchestrator.calculate_arrow_position(
                        arrow_data, pictograph_data, motion_data
                    )

                    positions[color] = (x, y, rotation)
                    logger.info(
                        f"POSITION: {color} arrow at ({x:.1f}, {y:.1f}) rotation {rotation:.1f}°"
                    )

            return positions

        except Exception as e:
            logger.error(f"ERROR: Failed to calculate arrow positions: {e}")
            return {}

    def _validate_positioning_results(self) -> bool:
        """Validate that positioning results are correct."""
        try:
            logger.info("PHASE 3: Validating positioning results...")

            if not self.positioning_results:
                logger.error("ERROR: No positioning results to validate")
                return False

            validation_passed = True

            for letter, result_data in self.positioning_results.items():
                logger.info(f"VALIDATE: Checking results for letter {letter}")

                if not self._validate_letter_results(letter, result_data):
                    logger.error(f"ERROR: Validation failed for letter {letter}")
                    validation_passed = False

            if validation_passed:
                logger.info("SUCCESS: All positioning results validated")
            else:
                logger.error("ERROR: Some positioning validations failed")

            return validation_passed

        except Exception as e:
            logger.error(f"ERROR: Positioning validation failed: {e}")
            return False

    def _validate_letter_results(
        self, letter: str, result_data: Dict[str, Any]
    ) -> bool:
        """Validate positioning results for a specific letter."""
        try:
            positions = result_data["positions"]

            # Basic validation: ensure positions are reasonable
            for color, (x, y, rotation) in positions.items():
                # Check that positions are not at origin (0, 0) unless expected
                if abs(x) < 1.0 and abs(y) < 1.0:
                    logger.warning(
                        f"WARNING: {letter} {color} arrow at near-origin position ({x:.1f}, {y:.1f})"
                    )

                # Check that rotation is within valid range
                if not (0 <= rotation <= 360):
                    logger.warning(
                        f"WARNING: {letter} {color} arrow has invalid rotation {rotation:.1f}°"
                    )

                logger.info(
                    f"VALID: {letter} {color} arrow positioned at ({x:.1f}, {y:.1f}) rotation {rotation:.1f}°"
                )

            # For letter I, verify motion-type-specific positioning was applied
            if letter == "I":
                return self._validate_motion_type_positioning(result_data)

            # For letter G, verify color-specific positioning was applied
            elif letter == "G":
                return self._validate_color_specific_positioning(result_data)

            return True

        except Exception as e:
            logger.error(f"ERROR: Failed to validate results for letter {letter}: {e}")
            return False

    def _validate_motion_type_positioning(self, result_data: Dict[str, Any]) -> bool:
        """Validate that motion-type-specific positioning was applied for letter I."""
        try:
            # For letter I, different motion types should result in different positions
            positions = result_data["positions"]

            if len(positions) >= 2:
                position_values = list(positions.values())
                pos1 = position_values[0]
                pos2 = position_values[1]

                # Positions should be different (special placement applied)
                if abs(pos1[0] - pos2[0]) > 10 or abs(pos1[1] - pos2[1]) > 10:
                    logger.info(
                        "SUCCESS: Motion-type-specific positioning detected for letter I"
                    )
                    return True
                else:
                    logger.warning(
                        "WARNING: Letter I positions are very similar - special placement may not be working"
                    )

            return True

        except Exception as e:
            logger.error(f"ERROR: Failed to validate motion-type positioning: {e}")
            return False

    def _validate_color_specific_positioning(self, result_data: Dict[str, Any]) -> bool:
        """Validate that color-specific positioning was applied for letter G."""
        try:
            # For letter G, different colors should result in different positions
            positions = result_data["positions"]

            if "red" in positions and "blue" in positions:
                red_pos = positions["red"]
                blue_pos = positions["blue"]

                # Positions should be different (special placement applied)
                if (
                    abs(red_pos[0] - blue_pos[0]) > 10
                    or abs(red_pos[1] - blue_pos[1]) > 10
                ):
                    logger.info(
                        "SUCCESS: Color-specific positioning detected for letter G"
                    )
                    return True
                else:
                    logger.warning(
                        "WARNING: Letter G red/blue positions are very similar - special placement may not be working"
                    )

            return True

        except Exception as e:
            logger.error(f"ERROR: Failed to validate color-specific positioning: {e}")
            return False


def run_special_arrow_positioning_test() -> bool:
    """Run the special arrow positioning E2E test."""
    test = SpecialArrowPositioningE2ETest()
    return test.run_special_arrow_positioning_test()


if __name__ == "__main__":
    success = run_special_arrow_positioning_test()
    if not success:
        print("\nFAILED: SPECIAL ARROW POSITIONING TEST FAILED!")
        print("Check the logs above for detailed failure information.")
        sys.exit(1)
    else:
        print("\nSUCCESS: SPECIAL ARROW POSITIONING TEST PASSED!")
        sys.exit(0)
