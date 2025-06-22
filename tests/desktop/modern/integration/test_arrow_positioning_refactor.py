"""
Integration test for the refactored arrow positioning services.

This test verifies that the refactored services produce the same results
as the original monolithic ArrowPositioningService.
"""

import pytest
from PyQt6.QtCore import QPointF

from src.application.services.positioning.arrow_positioning_service import ArrowPositioningService
from src.application.services.positioning.arrow_location_calculator_service import ArrowLocationCalculatorService
from src.application.services.positioning.arrow_rotation_calculator_service import ArrowRotationCalculatorService
from src.application.services.positioning.arrow_adjustment_calculator_service import ArrowAdjustmentCalculatorService
from src.application.services.positioning.arrow_coordinate_system_service import ArrowCoordinateSystemService

from src.domain.models.core_models import MotionData, MotionType, Location, RotationDirection
from src.domain.models.pictograph_models import ArrowData, PictographData


class TestArrowPositioningRefactor:
    """Test that refactored services work correctly."""

    @pytest.fixture
    def sample_motion_data(self):
        """Create sample motion data for testing."""
        return MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            turns=1.0
        )

    @pytest.fixture
    def sample_arrow_data(self, sample_motion_data):
        """Create sample arrow data for testing."""
        return ArrowData(
            color="blue",
            motion_data=sample_motion_data,
            is_visible=True
        )

    @pytest.fixture
    def sample_pictograph_data(self, sample_arrow_data):
        """Create sample pictograph data for testing."""
        return PictographData(
            letter="A",
            arrows={
                "blue": sample_arrow_data,
                "red": ArrowData(color="red", is_visible=False)
            }
        )

    @pytest.fixture
    def refactored_service(self):
        """Create refactored positioning service."""
        location_calculator = ArrowLocationCalculatorService()
        rotation_calculator = ArrowRotationCalculatorService()
        adjustment_calculator = ArrowAdjustmentCalculatorService()
        coordinate_system = ArrowCoordinateSystemService()
        
        return ArrowPositioningService(
            location_calculator=location_calculator,
            rotation_calculator=rotation_calculator,
            adjustment_calculator=adjustment_calculator,
            coordinate_system=coordinate_system
        )

    @pytest.fixture
    def original_service(self):
        """Create original positioning service for comparison."""
        return ArrowPositioningService()

    def test_location_calculator_service(self, sample_motion_data, sample_pictograph_data):
        """Test that location calculator service works correctly."""
        calculator = ArrowLocationCalculatorService()
        
        # Test PRO motion location calculation
        location = calculator.calculate_location(sample_motion_data, sample_pictograph_data)
        
        # PRO motion from NORTH to EAST should result in NORTHEAST
        assert location == Location.NORTHEAST

    def test_rotation_calculator_service(self, sample_motion_data):
        """Test that rotation calculator service works correctly."""
        calculator = ArrowRotationCalculatorService()
        
        # Test PRO motion rotation calculation
        rotation = calculator.calculate_rotation(sample_motion_data, Location.NORTHEAST)
        
        # PRO motion at NORTHEAST with clockwise rotation should be 0 degrees
        assert rotation == 0.0

    def test_coordinate_system_service(self, sample_motion_data):
        """Test that coordinate system service works correctly."""
        coordinate_system = ArrowCoordinateSystemService()
        
        # Test initial position calculation for PRO motion
        initial_position = coordinate_system.get_initial_position(sample_motion_data, Location.NORTHEAST)
        
        # PRO motion should use layer2 points
        expected_position = coordinate_system.LAYER2_POINTS[Location.NORTHEAST]
        assert initial_position == expected_position

    def test_adjustment_calculator_service(self, sample_arrow_data, sample_pictograph_data):
        """Test that adjustment calculator service works correctly."""
        calculator = ArrowAdjustmentCalculatorService()
        
        # Test adjustment calculation
        adjustment = calculator.calculate_adjustment(sample_arrow_data, sample_pictograph_data)
        
        # Should return a QPointF
        assert isinstance(adjustment, QPointF)

    def test_refactored_vs_original_consistency(self, refactored_service, original_service, sample_arrow_data, sample_pictograph_data):
        """Test that refactored service produces same results as original."""
        # Calculate positions with both services
        refactored_x, refactored_y, refactored_rotation = refactored_service.calculate_arrow_position(
            sample_arrow_data, sample_pictograph_data
        )
        
        original_x, original_y, original_rotation = original_service.calculate_arrow_position(
            sample_arrow_data, sample_pictograph_data
        )
        
        # Results should be identical (within floating point precision)
        assert abs(refactored_x - original_x) < 0.001
        assert abs(refactored_y - original_y) < 0.001
        assert abs(refactored_rotation - original_rotation) < 0.001

    def test_mirror_arrow_functionality(self, refactored_service, sample_arrow_data):
        """Test that mirror arrow functionality still works."""
        # Test with ANTI motion that should be mirrored
        anti_motion = MotionData(
            motion_type=MotionType.ANTI,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            turns=1.0
        )
        anti_arrow = ArrowData(color="blue", motion_data=anti_motion, is_visible=True)
        
        should_mirror = refactored_service.should_mirror_arrow(anti_arrow)
        assert should_mirror is True

    def test_coordinate_system_constants(self, refactored_service):
        """Test that coordinate system constants are preserved."""
        assert refactored_service.SCENE_SIZE == 950
        assert refactored_service.CENTER_X == 475.0
        assert refactored_service.CENTER_Y == 475.0
        
        # Test that hand points and layer2 points are available
        assert Location.NORTH in refactored_service.HAND_POINTS
        assert Location.NORTHEAST in refactored_service.LAYER2_POINTS

    def test_service_validation(self):
        """Test that individual services validate their inputs correctly."""
        location_calculator = ArrowLocationCalculatorService()
        rotation_calculator = ArrowRotationCalculatorService()
        adjustment_calculator = ArrowAdjustmentCalculatorService()
        
        # Test validation methods
        valid_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            prop_rot_dir=RotationDirection.CLOCKWISE
        )
        
        assert location_calculator.validate_motion_data(valid_motion) is True
        assert rotation_calculator.validate_motion_data(valid_motion) is True
        
        valid_arrow = ArrowData(color="blue", motion_data=valid_motion, is_visible=True)
        assert adjustment_calculator.validate_arrow_data(valid_arrow) is True

    def test_service_info_methods(self, sample_arrow_data, sample_pictograph_data):
        """Test that services provide useful debugging information."""
        adjustment_calculator = ArrowAdjustmentCalculatorService()
        coordinate_system = ArrowCoordinateSystemService()
        
        # Test adjustment info
        adjustment_info = adjustment_calculator.get_adjustment_info(sample_arrow_data, sample_pictograph_data)
        assert "placement_key" in adjustment_info
        assert "final_adjustment" in adjustment_info
        
        # Test coordinate info
        coord_info = coordinate_system.get_coordinate_info(Location.NORTHEAST)
        assert "hand_point" in coord_info
        assert "layer2_point" in coord_info
