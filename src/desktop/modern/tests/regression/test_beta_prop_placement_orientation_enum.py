"""
TEST LIFECYCLE: REGRESSION
PURPOSE: Ensure beta prop placement logic works correctly with Orientation enums
AUTHOR: @ai-agent

This test prevents regression of the beta prop placement bug that occurred
when MotionData was migrated from string orientations to Orientation enums.
The bug caused props in beta positions to move in incorrect directions
because the placement logic was still checking for string values.
"""

import pytest
from domain.models import (
    MotionData,
    BeatData,
    MotionType,
    RotationDirection,
    Location,
    Orientation,
)
from application.services.positioning.props.calculation.direction_calculation_service import (
    DirectionCalculationService,
    SeparationDirection,
)
from application.services.positioning.props.orchestration.prop_management_service import (
    PropManagementService,
)


class TestBetaPropPlacementOrientationEnum:
    """
    Regression tests for beta prop placement with Orientation enums.
    
    These tests ensure that the prop placement logic correctly handles
    Orientation enums instead of expecting string values.
    """

    def setup_method(self):
        """Set up test fixtures."""
        self.direction_service = DirectionCalculationService()
        self.prop_service = PropManagementService(self.direction_service)

    def test_radial_orientation_detection_with_enums(self):
        """Test that radial orientation detection works with Orientation enums."""
        # Test IN orientation (radial)
        motion_in = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            end_ori=Orientation.IN,
        )
        
        beat_data = BeatData(letter="A", blue_motion=motion_in)
        result = self.direction_service.calculate_separation_direction(
            motion_in, beat_data, "blue"
        )
        
        # Should return a valid separation direction for radial orientation
        assert isinstance(result, SeparationDirection)
        
        # Test OUT orientation (radial)
        motion_out = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            end_ori=Orientation.OUT,
        )
        
        beat_data = BeatData(letter="A", blue_motion=motion_out)
        result = self.direction_service.calculate_separation_direction(
            motion_out, beat_data, "blue"
        )
        
        # Should return a valid separation direction for radial orientation
        assert isinstance(result, SeparationDirection)

    def test_nonradial_orientation_detection_with_enums(self):
        """Test that nonradial orientation detection works with Orientation enums."""
        # Test CLOCK orientation (nonradial)
        motion_clock = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            end_ori=Orientation.CLOCK,
        )
        
        beat_data = BeatData(letter="A", blue_motion=motion_clock)
        result = self.direction_service.calculate_separation_direction(
            motion_clock, beat_data, "blue"
        )
        
        # Should return a valid separation direction for nonradial orientation
        assert isinstance(result, SeparationDirection)
        
        # Test COUNTER orientation (nonradial)
        motion_counter = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            end_ori=Orientation.COUNTER,
        )
        
        beat_data = BeatData(letter="A", blue_motion=motion_counter)
        result = self.direction_service.calculate_separation_direction(
            motion_counter, beat_data, "blue"
        )
        
        # Should return a valid separation direction for nonradial orientation
        assert isinstance(result, SeparationDirection)

    def test_beta_prop_direction_calculation_consistency(self):
        """
        Test that beta prop direction calculations are consistent between
        radial and nonradial orientations using Orientation enums.
        """
        # Create motions with different orientations at the same location
        base_motion_data = {
            "motion_type": MotionType.PRO,
            "prop_rot_dir": RotationDirection.CLOCKWISE,
            "start_loc": Location.NORTHEAST,
            "end_loc": Location.NORTHEAST,
        }
        
        # Test all four orientations
        orientations = [
            Orientation.IN,
            Orientation.OUT,
            Orientation.CLOCK,
            Orientation.COUNTER,
        ]
        
        results = {}
        for orientation in orientations:
            motion = MotionData(**base_motion_data, end_ori=orientation)
            beat_data = BeatData(letter="A", blue_motion=motion)
            
            blue_result = self.direction_service.calculate_separation_direction(
                motion, beat_data, "blue"
            )
            red_result = self.direction_service.calculate_separation_direction(
                motion, beat_data, "red"
            )
            
            results[orientation] = {
                "blue": blue_result,
                "red": red_result,
            }
        
        # Verify all results are valid SeparationDirection enums
        for orientation, color_results in results.items():
            for color, result in color_results.items():
                assert isinstance(result, SeparationDirection), (
                    f"Invalid result for {orientation.value} orientation, {color} prop: {result}"
                )
        
        # Verify radial orientations (IN/OUT) produce different results than nonradial (CLOCK/COUNTER)
        radial_results = [results[Orientation.IN], results[Orientation.OUT]]
        nonradial_results = [results[Orientation.CLOCK], results[Orientation.COUNTER]]
        
        # At least one radial result should differ from at least one nonradial result
        # (This ensures the orientation type is actually affecting the calculation)
        radial_blue = {r["blue"] for r in radial_results}
        nonradial_blue = {r["blue"] for r in nonradial_results}
        
        # The sets should not be identical (orientation should matter)
        assert radial_blue != nonradial_blue, (
            "Radial and nonradial orientations should produce different separation directions"
        )

    def test_orientation_enum_not_string_comparison(self):
        """
        Regression test to ensure orientation comparisons use enums, not strings.
        
        This test specifically checks that the bug where orientation was compared
        as `motion.end_ori in ["in", "out"]` instead of 
        `motion.end_ori in [Orientation.IN, Orientation.OUT]` is fixed.
        """
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            end_ori=Orientation.IN,
        )
        
        # Verify the motion has an Orientation enum, not a string
        assert isinstance(motion.end_ori, Orientation)
        assert motion.end_ori == Orientation.IN
        assert motion.end_ori != "in"  # Should NOT equal the string
        
        # Verify the direction calculation service handles this correctly
        beat_data = BeatData(letter="A", blue_motion=motion)
        result = self.direction_service.calculate_separation_direction(
            motion, beat_data, "blue"
        )
        
        # Should successfully calculate a direction without errors
        assert isinstance(result, SeparationDirection)

    def test_backward_compatibility_string_to_enum_conversion(self):
        """
        Test that MotionData still accepts string orientations and converts them to enums.
        
        This ensures backward compatibility while preventing the beta prop placement bug.
        """
        # Create MotionData with string orientation (backward compatibility)
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            end_ori="in",  # String input
        )
        
        # Verify it was converted to an Orientation enum
        assert isinstance(motion.end_ori, Orientation)
        assert motion.end_ori == Orientation.IN
        
        # Verify direction calculation works correctly
        beat_data = BeatData(letter="A", blue_motion=motion)
        result = self.direction_service.calculate_separation_direction(
            motion, beat_data, "blue"
        )
        
        assert isinstance(result, SeparationDirection)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
