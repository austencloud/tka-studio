"""
Unit tests for ArrowPositioningOrchestrator

Tests the complete arrow positioning pipeline using focused services.
Validates that refactoring maintains positioning accuracy.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

# Add modern/src to path for imports
modern_src_path = Path(__file__).parent.parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)
from domain.models.pictograph_models import ArrowData
from domain.models.pictograph_models import PictographData
from domain.models.positioning_models import ArrowPositionResult
from application.services.positioning.arrow_positioning_orchestrator import (
    ArrowPositioningOrchestrator,
    IArrowPositioningService,
)


class TestArrowPositioningOrchestrator:
    """Test suite for ArrowPositioningOrchestrator."""

    def setup_method(self):
        """Set up test fixtures."""
        # Mock the focused services to test orchestration
        self.mock_location_calculator = Mock()
        self.mock_rotation_calculator = Mock()
        self.mock_adjustment_service = Mock()

        self.orchestrator = ArrowPositioningOrchestrator(
            location_calculator=self.mock_location_calculator,
            rotation_calculator=self.mock_rotation_calculator,
            adjustment_service=self.mock_adjustment_service,
        )

    def test_calculate_position_complete_pipeline(self):
        """Test complete positioning pipeline orchestration."""
        # Setup test data
        motion = MotionData(
            motion_type=MotionType.STATIC,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
        )

        arrow_data = ArrowData(
            color="red",
            motion_data=motion,
            is_visible=True,
        )

        pictograph_data = PictographData(letter="A")

        # Mock service responses
        self.mock_location_calculator.calculate_location.return_value = Location.NORTH
        self.mock_rotation_calculator.calculate_rotation.return_value = 180.0
        self.mock_adjustment_service.calculate_adjustment.return_value = Mock(
            x=lambda: 10.0, y=lambda: 5.0
        )

        # Execute
        result = self.orchestrator.calculate_position(arrow_data, pictograph_data)

        # Verify orchestration
        self.mock_location_calculator.calculate_location.assert_called_once_with(
            motion, pictograph_data
        )
        self.mock_rotation_calculator.calculate_rotation.assert_called_once_with(
            motion, Location.NORTH
        )
        self.mock_adjustment_service.calculate_adjustment.assert_called_once_with(
            arrow_data, pictograph_data
        )

        # Verify result
        assert isinstance(result, ArrowPositionResult)
        assert result.rotation == 180.0
        assert result.location == "NORTH"

    def test_calculate_position_no_motion_data(self):
        """Test positioning with no motion data returns center position."""
        arrow_data = ArrowData(
            color="red",
            motion_data=None,
            is_visible=True,
        )

        result = self.orchestrator.calculate_position(arrow_data)

        assert result.x == 475.0
        assert result.y == 475.0
        assert result.rotation == 0.0

    def test_calculate_all_positions(self):
        """Test calculating positions for all arrows in pictograph."""
        # Setup pictograph with multiple arrows
        motion1 = MotionData(
            motion_type=MotionType.STATIC,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
        )

        motion2 = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            prop_rot_dir=RotationDirection.CLOCKWISE,
        )

        arrows = {
            "red": ArrowData(color="red", motion_data=motion1, is_visible=True),
            "blue": ArrowData(color="blue", motion_data=motion2, is_visible=True),
            "hidden": ArrowData(color="green", motion_data=motion1, is_visible=False),
        }

        pictograph_data = PictographData(letter="A", arrows=arrows)

        # Mock service responses
        self.mock_location_calculator.calculate_location.return_value = Location.NORTH
        self.mock_rotation_calculator.calculate_rotation.return_value = 90.0
        self.mock_adjustment_service.calculate_adjustment.return_value = Mock(
            x=lambda: 0.0, y=lambda: 0.0
        )

        # Execute
        results = self.orchestrator.calculate_all_positions(pictograph_data)

        # Verify only visible arrows are processed
        assert len(results) == 2
        assert "red" in results
        assert "blue" in results
        assert "hidden" not in results

        # Verify all results are ArrowPositionResult instances
        for result in results.values():
            assert isinstance(result, ArrowPositionResult)

    def test_interface_compliance(self):
        """Test that ArrowPositioningOrchestrator implements the interface correctly."""
        assert isinstance(self.orchestrator, IArrowPositioningService)

    def test_layer2_vs_hand_point_positioning(self):
        """Test that different motion types use correct coordinate systems."""
        # Test PRO motion uses layer2 points
        motion_pro = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            prop_rot_dir=RotationDirection.CLOCKWISE,
        )

        # Test STATIC motion uses hand points
        motion_static = MotionData(
            motion_type=MotionType.STATIC,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
        )

        # Mock location calculator to return NORTH for both
        self.mock_location_calculator.calculate_location.return_value = Location.NORTH
        self.mock_rotation_calculator.calculate_rotation.return_value = 0.0
        self.mock_adjustment_service.calculate_adjustment.return_value = Mock(
            x=lambda: 0.0, y=lambda: 0.0
        )

        # Test PRO motion
        arrow_pro = ArrowData(color="red", motion_data=motion_pro, is_visible=True)
        result_pro = self.orchestrator.calculate_position(arrow_pro)

        # Test STATIC motion
        arrow_static = ArrowData(
            color="blue", motion_data=motion_static, is_visible=True
        )
        result_static = self.orchestrator.calculate_position(arrow_static)

        # PRO should use layer2 coordinates (618.1, 331.9 for NORTH)
        # STATIC should use hand point coordinates (475.0, 331.9 for NORTH)
        assert result_pro.x != result_static.x  # Different coordinate systems


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
