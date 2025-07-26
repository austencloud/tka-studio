"""
Comprehensive Tests for LetterIPositioningService

Tests the Letter I positioning service with PRO/ANTI coordination logic.
"""

import pytest

from desktop.modern.domain.models import MotionData, MotionType, Orientation
from desktop.modern.domain.models.enums import Location

from shared.application.services.positioning.props.specialization.letter_i_positioning_service import (
    LetterIPositioningService,
)
from shared.application.services.positioning.props.calculation.direction_calculation_service import (
    SeparationDirection,
)


class TestLetterIPositioningService:
    """Comprehensive test suite for LetterIPositioningService."""

    @pytest.fixture
    def service(self):
        """Create service instance for testing."""
        return LetterIPositioningService()

    @pytest.fixture
    def pro_motion(self):
        """Create PRO motion data for testing."""
        return MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            turns=1.0,
        )

    @pytest.fixture
    def anti_motion(self):
        """Create ANTI motion data for testing."""
        return MotionData(
            motion_type=MotionType.ANTI,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            start_ori=Orientation.OUT,
            end_ori=Orientation.IN,
            turns=1.0,
        )

    def test_initialization(self, service):
        """Test that service initializes correctly."""
        assert service is not None

    @pytest.mark.parametrize("direction,expected_opposite", [
        (SeparationDirection.LEFT, SeparationDirection.RIGHT),
        (SeparationDirection.RIGHT, SeparationDirection.LEFT),
        (SeparationDirection.UP, SeparationDirection.DOWN),
        (SeparationDirection.DOWN, SeparationDirection.UP),
        (SeparationDirection.UPLEFT, SeparationDirection.DOWNRIGHT),
        (SeparationDirection.UPRIGHT, SeparationDirection.DOWNLEFT),
        (SeparationDirection.DOWNLEFT, SeparationDirection.UPRIGHT),
        (SeparationDirection.DOWNRIGHT, SeparationDirection.UPLEFT),
    ])
    def test_get_opposite_direction(self, service, direction, expected_opposite):
        """Test that opposite directions are calculated correctly."""
        result = service.get_opposite_direction(direction)
        assert result == expected_opposite

    def test_get_opposite_direction_unknown(self, service):
        """Test that unknown directions return themselves."""
        class UnknownDirection:
            pass
        
        unknown = UnknownDirection()
        result = service.get_opposite_direction(unknown)
        assert result == unknown

    def test_calculate_standard_direction_diamond_radial(self, service):
        """Test standard direction calculation for diamond grid with radial orientation."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=0.0,
        )
        
        # Test diamond grid locations with radial orientation
        blue_direction = service.calculate_standard_direction(motion, "blue")
        red_direction = service.calculate_standard_direction(motion, "red")
        
        # For NORTH location: blue=LEFT, red=RIGHT
        assert blue_direction == SeparationDirection.LEFT
        assert red_direction == SeparationDirection.RIGHT

    def test_calculate_standard_direction_diamond_nonradial(self, service):
        """Test standard direction calculation for diamond grid with nonradial orientation."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            start_ori=Orientation.CLOCK,
            end_ori=Orientation.CLOCK,
            turns=0.0,
        )
        
        # Test diamond grid locations with nonradial orientation
        blue_direction = service.calculate_standard_direction(motion, "blue")
        red_direction = service.calculate_standard_direction(motion, "red")
        
        # For NORTH location nonradial: blue=DOWN, red=UP
        assert blue_direction == SeparationDirection.DOWN
        assert red_direction == SeparationDirection.UP

    def test_calculate_standard_direction_box_radial(self, service):
        """Test standard direction calculation for box grid with radial orientation."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTHEAST,
            end_loc=Location.NORTHEAST,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN,
            turns=0.0,
        )
        
        # Test box grid locations with radial orientation
        blue_direction = service.calculate_standard_direction(motion, "blue")
        red_direction = service.calculate_standard_direction(motion, "red")
        
        # For NORTHEAST location radial: blue=UPLEFT, red=DOWNRIGHT
        assert blue_direction == SeparationDirection.UPLEFT
        assert red_direction == SeparationDirection.DOWNRIGHT

    def test_calculate_standard_direction_box_nonradial(self, service):
        """Test standard direction calculation for box grid with nonradial orientation."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTHEAST,
            end_loc=Location.NORTHEAST,
            start_ori=Orientation.CLOCK,
            end_ori=Orientation.CLOCK,
            turns=0.0,
        )
        
        # Test box grid locations with nonradial orientation
        blue_direction = service.calculate_standard_direction(motion, "blue")
        red_direction = service.calculate_standard_direction(motion, "red")
        
        # For NORTHEAST location nonradial: blue=DOWNLEFT, red=UPRIGHT
        assert blue_direction == SeparationDirection.DOWNLEFT
        assert red_direction == SeparationDirection.UPRIGHT

    def test_calculate_letter_i_directions_red_pro(self, service, pro_motion, anti_motion):
        """Test Letter I direction calculation when red is PRO."""
        # Red is PRO, blue is ANTI
        red_pro = pro_motion
        blue_anti = anti_motion
        
        blue_direction, red_direction = service.calculate_letter_i_directions(blue_anti, red_pro)
        
        # PRO and ANTI should get opposite directions
        assert blue_direction != red_direction
        assert service.get_opposite_direction(red_direction) == blue_direction

    def test_calculate_letter_i_directions_blue_pro(self, service, pro_motion, anti_motion):
        """Test Letter I direction calculation when blue is PRO."""
        # Blue is PRO, red is ANTI
        blue_pro = pro_motion
        red_anti = anti_motion
        
        blue_direction, red_direction = service.calculate_letter_i_directions(blue_pro, red_anti)
        
        # PRO and ANTI should get opposite directions
        assert blue_direction != red_direction
        assert service.get_opposite_direction(blue_direction) == red_direction

    def test_calculate_letter_i_directions_neither_pro(self, service):
        """Test Letter I direction calculation when neither motion is PRO."""
        static_motion = MotionData(
            motion_type=MotionType.STATIC,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            turns=1.0,
        )
        dash_motion = MotionData(
            motion_type=MotionType.DASH,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            start_ori=Orientation.OUT,
            end_ori=Orientation.IN,
            turns=1.0,
        )
        
        blue_direction, red_direction = service.calculate_letter_i_directions(static_motion, dash_motion)
        
        # Should fall back to standard directions
        expected_blue = service.calculate_standard_direction(static_motion, "blue")
        expected_red = service.calculate_standard_direction(dash_motion, "red")
        
        assert blue_direction == expected_blue
        assert red_direction == expected_red

    def test_calculate_letter_i_directions_both_pro(self, service, pro_motion):
        """Test Letter I direction calculation when both motions are PRO (edge case)."""
        # This shouldn't happen in normal Letter I, but test the behavior
        blue_direction, red_direction = service.calculate_letter_i_directions(pro_motion, pro_motion)
        
        # Should use the first PRO found (red in this case)
        assert blue_direction != red_direction
        assert service.get_opposite_direction(red_direction) == blue_direction

    def test_letter_i_coordination_consistency(self, service):
        """Test that Letter I coordination is consistent across multiple calls."""
        pro_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            turns=1.0,
        )
        anti_motion = MotionData(
            motion_type=MotionType.ANTI,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            start_ori=Orientation.OUT,
            end_ori=Orientation.IN,
            turns=1.0,
        )
        
        # Multiple calls should return consistent results
        result1 = service.calculate_letter_i_directions(pro_motion, anti_motion)
        result2 = service.calculate_letter_i_directions(pro_motion, anti_motion)
        result3 = service.calculate_letter_i_directions(pro_motion, anti_motion)
        
        assert result1 == result2 == result3

    def test_letter_i_symmetry(self, service):
        """Test that Letter I positioning maintains symmetry."""
        pro_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            turns=1.0,
        )
        anti_motion = MotionData(
            motion_type=MotionType.ANTI,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            start_ori=Orientation.OUT,
            end_ori=Orientation.IN,
            turns=1.0,
        )
        
        # Test both orders
        blue_dir1, red_dir1 = service.calculate_letter_i_directions(pro_motion, anti_motion)
        blue_dir2, red_dir2 = service.calculate_letter_i_directions(anti_motion, pro_motion)
        
        # The PRO motion should always get the same direction regardless of color
        # The ANTI motion should always get the opposite
        if pro_motion.motion_type == MotionType.PRO:
            # In first call: blue=PRO, red=ANTI
            # In second call: blue=ANTI, red=PRO
            assert service.get_opposite_direction(blue_dir1) == red_dir1
            assert service.get_opposite_direction(red_dir2) == blue_dir2

    def test_performance_with_many_calculations(self, service, pro_motion, anti_motion):
        """Test performance with many repeated calculations."""
        import time
        
        start_time = time.time()
        for _ in range(1000):
            service.calculate_letter_i_directions(pro_motion, anti_motion)
        end_time = time.time()
        
        # Should complete 1,000 calculations in under 1 second
        assert (end_time - start_time) < 1.0

    def test_all_location_combinations(self, service):
        """Test Letter I positioning for all location combinations."""
        locations = [Location.NORTH, Location.SOUTH, Location.EAST, Location.WEST,
                    Location.NORTHEAST, Location.NORTHWEST, Location.SOUTHEAST, Location.SOUTHWEST]
        
        for loc1 in locations:
            for loc2 in locations:
                pro_motion = MotionData(
                    motion_type=MotionType.PRO,
                    start_loc=loc1,
                    end_loc=loc1,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.IN,
                    turns=0.0,
                )
                anti_motion = MotionData(
                    motion_type=MotionType.ANTI,
                    start_loc=loc2,
                    end_loc=loc2,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.IN,
                    turns=0.0,
                )
                
                blue_dir, red_dir = service.calculate_letter_i_directions(pro_motion, anti_motion)
                
                # Should always return valid directions
                assert isinstance(blue_dir, SeparationDirection)
                assert isinstance(red_dir, SeparationDirection)
                
                # PRO and ANTI should be opposite
                assert service.get_opposite_direction(blue_dir) == red_dir
