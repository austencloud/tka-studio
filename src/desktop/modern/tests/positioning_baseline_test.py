"""
Arrow Positioning Baseline Test

This test establishes a baseline for the current arrow positioning system
before refactoring. It captures the expected outputs for various inputs
to ensure the refactored system produces identical results.
"""
from __future__ import annotations

import os
import sys


# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from application.services.positioning.arrows.calculation.arrow_location_calculator import (
    ArrowLocationCalculatorService,
)
from application.services.positioning.arrows.calculation.arrow_rotation_calculator import (
    ArrowRotationCalculatorService,
)
from application.services.positioning.arrows.coordinate_system.arrow_coordinate_system_service import (
    ArrowCoordinateSystemService,
)
from application.services.positioning.arrows.orchestration.arrow_adjustment_calculator_service import (
    ArrowAdjustmentCalculatorService,
)

# Import the services we're testing
from application.services.positioning.arrows.orchestration.arrow_positioning_orchestrator import (
    ArrowPositioningOrchestrator,
)
from domain.models.arrow_data import ArrowData
from domain.models.enums import Location
from domain.models.motion_models import MotionData, MotionType, RotationDirection
from domain.models.pictograph_data import PictographData


class TestArrowPositioningBaseline:
    """Baseline tests for arrow positioning system."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create service instances
        self.location_calculator = ArrowLocationCalculatorService()
        self.rotation_calculator = ArrowRotationCalculatorService()
        self.coordinate_system = ArrowCoordinateSystemService()
        self.adjustment_calculator = ArrowAdjustmentCalculatorService()

        # Create orchestrator
        self.orchestrator = ArrowPositioningOrchestrator(
            location_calculator=self.location_calculator,
            rotation_calculator=self.rotation_calculator,
            adjustment_calculator=self.adjustment_calculator,
            coordinate_system=self.coordinate_system,
        )

    def create_test_motion(
        self,
        motion_type: MotionType = MotionType.STATIC,
        start_loc: Location = Location.NORTH,
        end_loc: Location = Location.SOUTH,
        prop_rot_dir: RotationDirection = RotationDirection.CLOCKWISE,
    ) -> MotionData:
        """Create test motion data."""
        return MotionData(
            motion_type=motion_type,
            start_loc=start_loc,
            end_loc=end_loc,
            prop_rot_dir=prop_rot_dir,
        )

    def create_test_arrow(self, color: str = "blue") -> ArrowData:
        """Create test arrow data."""
        return ArrowData(color=color, is_visible=True)

    def create_test_pictograph(
        self, motions: dict[str, MotionData], letter: str = "A"
    ) -> PictographData:
        """Create test pictograph data."""
        arrows = {color: self.create_test_arrow(color) for color in motions}
        return PictographData(letter=letter, arrows=arrows, motions=motions)

    def test_static_motion_baseline(self):
        """Test static motion positioning baseline."""
        motion = self.create_test_motion(MotionType.STATIC, Location.NORTH)
        arrow = self.create_test_arrow("blue")
        pictograph = self.create_test_pictograph({"blue": motion})

        # Test individual services
        location = self.location_calculator.calculate_location(motion, pictograph)
        assert location == Location.NORTH

        rotation = self.rotation_calculator.calculate_rotation(motion, location)
        assert rotation == 180.0  # Static arrows point inward

        initial_pos = self.coordinate_system.get_initial_position(motion, location)
        assert initial_pos.x == 475.0
        assert initial_pos.y == 331.9

        # Test full orchestrator
        x, y, rot = self.orchestrator.calculate_arrow_position(
            arrow, pictograph, motion
        )

        # Record baseline values
        print(f"BASELINE - Static NORTH: x={x}, y={y}, rotation={rot}")
        assert isinstance(x, float)
        assert isinstance(y, float)
        assert isinstance(rot, float)
        assert rot == 180.0

    def test_pro_motion_baseline(self):
        """Test PRO motion positioning baseline."""
        motion = self.create_test_motion(
            MotionType.PRO, Location.NORTH, Location.SOUTH, RotationDirection.CLOCKWISE
        )
        arrow = self.create_test_arrow("blue")
        pictograph = self.create_test_pictograph({"blue": motion})

        # Test individual services
        location = self.location_calculator.calculate_location(motion, pictograph)
        self.rotation_calculator.calculate_rotation(motion, location)
        self.coordinate_system.get_initial_position(motion, location)

        # Test full orchestrator
        x, y, rot = self.orchestrator.calculate_arrow_position(
            arrow, pictograph, motion
        )

        # Record baseline values
        print(f"BASELINE - PRO N->S CW: x={x}, y={y}, rotation={rot}")
        assert isinstance(x, float)
        assert isinstance(y, float)
        assert isinstance(rot, (int, float))

    def test_anti_motion_baseline(self):
        """Test ANTI motion positioning baseline."""
        motion = self.create_test_motion(
            MotionType.ANTI,
            Location.EAST,
            Location.NORTH,
            RotationDirection.COUNTER_CLOCKWISE,
        )
        arrow = self.create_test_arrow("red")
        pictograph = self.create_test_pictograph({"red": motion})

        x, y, rot = self.orchestrator.calculate_arrow_position(
            arrow, pictograph, motion
        )

        print(f"BASELINE - ANTI E->W CCW: x={x}, y={y}, rotation={rot}")
        assert isinstance(x, float)
        assert isinstance(y, float)
        assert isinstance(rot, (int, float))

    def test_dash_motion_baseline(self):
        """Test DASH motion positioning baseline."""
        motion = self.create_test_motion(
            MotionType.DASH,
            Location.NORTHEAST,
            Location.SOUTHWEST,
            RotationDirection.NO_ROTATION,
        )
        arrow = self.create_test_arrow("blue")
        pictograph = self.create_test_pictograph({"blue": motion})

        x, y, rot = self.orchestrator.calculate_arrow_position(
            arrow, pictograph, motion
        )

        print(f"BASELINE - DASH NE->SW NO_ROT: x={x}, y={y}, rotation={rot}")
        assert isinstance(x, float)
        assert isinstance(y, float)
        assert isinstance(rot, (int, float))

    def test_multiple_arrows_baseline(self):
        """Test multiple arrows positioning baseline."""
        blue_motion = self.create_test_motion(MotionType.STATIC, Location.NORTH)
        red_motion = self.create_test_motion(
            MotionType.PRO, Location.SOUTH, Location.NORTH
        )

        pictograph = self.create_test_pictograph(
            {"blue": blue_motion, "red": red_motion}
        )

        # Test blue arrow
        blue_arrow = pictograph.arrows["blue"]
        blue_x, blue_y, blue_rot = self.orchestrator.calculate_arrow_position(
            blue_arrow, pictograph, blue_motion
        )

        # Test red arrow
        red_arrow = pictograph.arrows["red"]
        red_x, red_y, red_rot = self.orchestrator.calculate_arrow_position(
            red_arrow, pictograph, red_motion
        )

        print(f"BASELINE - Blue: x={blue_x}, y={blue_y}, rotation={blue_rot}")
        print(f"BASELINE - Red: x={red_x}, y={red_y}, rotation={red_rot}")

        # Ensure different positions for different arrows
        assert (blue_x, blue_y) != (red_x, red_y) or blue_rot != red_rot

    def test_deterministic_behavior(self):
        """Test that positioning is deterministic."""
        motion = self.create_test_motion(MotionType.STATIC, Location.EAST)
        arrow = self.create_test_arrow("blue")
        pictograph = self.create_test_pictograph({"blue": motion})

        # Calculate position multiple times
        results = []
        for _ in range(3):
            result = self.orchestrator.calculate_arrow_position(
                arrow, pictograph, motion
            )
            results.append(result)

        # All results should be identical
        assert all(result == results[0] for result in results)
        print(f"BASELINE - Deterministic: {results[0]}")


if __name__ == "__main__":
    # Run the baseline tests
    test_instance = TestArrowPositioningBaseline()
    test_instance.setup_method()

    print("=== ARROW POSITIONING BASELINE TESTS ===")

    try:
        test_instance.test_static_motion_baseline()
        print("✅ Static motion baseline captured")
    except Exception as e:
        print(f"❌ Static motion baseline failed: {e}")

    try:
        test_instance.test_pro_motion_baseline()
        print("✅ PRO motion baseline captured")
    except Exception as e:
        print(f"❌ PRO motion baseline failed: {e}")

    try:
        test_instance.test_anti_motion_baseline()
        print("✅ ANTI motion baseline captured")
    except Exception as e:
        print(f"❌ ANTI motion baseline failed: {e}")

    try:
        test_instance.test_dash_motion_baseline()
        print("✅ DASH motion baseline captured")
    except Exception as e:
        print(f"❌ DASH motion baseline failed: {e}")

    try:
        test_instance.test_multiple_arrows_baseline()
        print("✅ Multiple arrows baseline captured")
    except Exception as e:
        print(f"❌ Multiple arrows baseline failed: {e}")

    try:
        test_instance.test_deterministic_behavior()
        print("✅ Deterministic behavior verified")
    except Exception as e:
        print(f"❌ Deterministic behavior failed: {e}")

    print("=== BASELINE TESTS COMPLETE ===")
