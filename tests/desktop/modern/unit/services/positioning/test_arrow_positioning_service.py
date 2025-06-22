"""
Comprehensive tests for ArrowPositioningService before refactoring.

These tests capture the existing behavior to ensure refactoring preserves functionality.
"""

from unittest.mock import Mock, patch

import pytest
from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from src.application.services.positioning.arrow_positioning_service import (
    ArrowPositioningService,
)
from src.domain.models.core_models import (
    Location,
    MotionData,
    MotionType,
    RotationDirection,
)
from src.domain.models.pictograph_models import ArrowData, PictographData


class TestArrowPositioningServiceBehavior:
    """Test existing behavior before refactoring."""

    @pytest.fixture
    def service(self):
        """Create service instance for testing."""
        return ArrowPositioningService()

    @pytest.fixture
    def sample_motion_data(self):
        """Create sample motion data for testing."""
        return MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            turns=1.0,
        )

    @pytest.fixture
    def sample_arrow_data(self, sample_motion_data):
        """Create sample arrow data for testing."""
        return ArrowData(color="blue", motion_data=sample_motion_data, is_visible=True)

    @pytest.fixture
    def sample_pictograph_data(self, sample_arrow_data):
        """Create sample pictograph data for testing."""
        return PictographData(
            letter="A",
            arrows={
                "blue": sample_arrow_data,
                "red": ArrowData(color="red", is_visible=False),
            },
        )

    def test_calculate_arrow_position_basic(
        self, service, sample_arrow_data, sample_pictograph_data
    ):
        """Test basic arrow position calculation."""
        x, y, rotation = service.calculate_arrow_position(
            sample_arrow_data, sample_pictograph_data
        )

        # Verify return types
        assert isinstance(x, float)
        assert isinstance(y, float)
        assert isinstance(rotation, float)

        # Verify reasonable coordinate ranges (within scene bounds)
        assert 0 <= x <= 950
        assert 0 <= y <= 950
        assert 0 <= rotation < 360

    def test_calculate_arrow_position_static_motion(
        self, service, sample_pictograph_data
    ):
        """Test static motion arrow positioning."""
        static_motion = MotionData(
            motion_type=MotionType.STATIC,
            start_loc=Location.NORTH,
            end_loc=Location.NORTH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
        )
        arrow_data = ArrowData(color="blue", motion_data=static_motion, is_visible=True)

        x, y, rotation = service.calculate_arrow_position(
            arrow_data, sample_pictograph_data
        )

        # Static arrows should use hand points
        expected_point = service.HAND_POINTS[Location.NORTH]
        # Note: Final position includes adjustments, so we test the pipeline works
        assert isinstance(x, float)
        assert isinstance(y, float)

    def test_calculate_arrow_position_pro_motion(self, service, sample_pictograph_data):
        """Test PRO motion arrow positioning."""
        pro_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            turns=1.0,
        )
        arrow_data = ArrowData(color="blue", motion_data=pro_motion, is_visible=True)

        x, y, rotation = service.calculate_arrow_position(
            arrow_data, sample_pictograph_data
        )

        # PRO arrows should use layer2 points and specific rotation
        assert isinstance(x, float)
        assert isinstance(y, float)
        assert rotation == 315.0  # Expected PRO rotation for NORTHEAST location, CW

    def test_calculate_arrow_position_anti_motion(
        self, service, sample_pictograph_data
    ):
        """Test ANTI motion arrow positioning."""
        anti_motion = MotionData(
            motion_type=MotionType.ANTI,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            turns=1.0,
        )
        arrow_data = ArrowData(color="blue", motion_data=anti_motion, is_visible=True)

        x, y, rotation = service.calculate_arrow_position(
            arrow_data, sample_pictograph_data
        )

        # ANTI arrows should use layer2 points and specific rotation
        assert isinstance(x, float)
        assert isinstance(y, float)
        assert rotation == 270.0  # Expected ANTI rotation for NORTHEAST location, CW

    def test_calculate_arrow_position_dash_motion(
        self, service, sample_pictograph_data
    ):
        """Test DASH motion arrow positioning."""
        dash_motion = MotionData(
            motion_type=MotionType.DASH,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            prop_rot_dir=RotationDirection.NO_ROTATION,
        )
        arrow_data = ArrowData(color="blue", motion_data=dash_motion, is_visible=True)

        x, y, rotation = service.calculate_arrow_position(
            arrow_data, sample_pictograph_data
        )

        # DASH arrows should use hand points and specific rotation
        assert isinstance(x, float)
        assert isinstance(y, float)
        assert rotation == 90.0  # Expected DASH rotation for N->S, NO_ROTATION

    def test_calculate_arrow_position_no_motion_data(
        self, service, sample_pictograph_data
    ):
        """Test arrow positioning with no motion data."""
        arrow_data = ArrowData(color="blue", motion_data=None, is_visible=True)

        x, y, rotation = service.calculate_arrow_position(
            arrow_data, sample_pictograph_data
        )

        # Should return center position
        assert x == service.CENTER_X
        assert y == service.CENTER_Y
        assert rotation == 0.0

    def test_calculate_all_arrow_positions(self, service, sample_pictograph_data):
        """Test calculating positions for all arrows in pictograph."""
        result = service.calculate_all_arrow_positions(sample_pictograph_data)

        # Should return updated pictograph data
        assert isinstance(result, PictographData)
        assert result.letter == sample_pictograph_data.letter

        # Blue arrow should have position data
        blue_arrow = result.blue_arrow
        assert blue_arrow.position_x is not None
        assert blue_arrow.position_y is not None
        assert blue_arrow.rotation_angle is not None

    def test_should_mirror_arrow_anti_clockwise(self, service):
        """Test mirror determination for ANTI motion with clockwise rotation."""
        motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
        )
        arrow_data = ArrowData(color="blue", motion_data=motion)

        should_mirror = service.should_mirror_arrow(arrow_data)
        assert should_mirror is True

    def test_should_mirror_arrow_anti_counter_clockwise(self, service):
        """Test mirror determination for ANTI motion with counter-clockwise rotation."""
        motion = MotionData(
            motion_type=MotionType.ANTI,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
        )
        arrow_data = ArrowData(color="blue", motion_data=motion)

        should_mirror = service.should_mirror_arrow(arrow_data)
        assert should_mirror is False

    def test_should_mirror_arrow_pro_clockwise(self, service):
        """Test mirror determination for PRO motion with clockwise rotation."""
        motion = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.EAST,
        )
        arrow_data = ArrowData(color="blue", motion_data=motion)

        should_mirror = service.should_mirror_arrow(arrow_data)
        assert should_mirror is False

    def test_should_mirror_arrow_no_motion_data(self, service):
        """Test mirror determination with no motion data."""
        arrow_data = ArrowData(color="blue", motion_data=None)

        should_mirror = service.should_mirror_arrow(arrow_data)
        assert should_mirror is False

    @patch("PyQt6.QtSvgWidgets.QGraphicsSvgItem")
    def test_apply_mirror_transform_true(self, mock_svg_item, service):
        """Test applying mirror transform when should_mirror is True."""
        mock_item = Mock(spec=QGraphicsSvgItem)
        mock_rect = Mock()
        mock_rect.center.return_value = QPointF(100, 100)
        mock_item.boundingRect.return_value = mock_rect

        service.apply_mirror_transform(mock_item, True)

        # Verify transform was applied
        mock_item.setTransform.assert_called_once()

    @patch("PyQt6.QtSvgWidgets.QGraphicsSvgItem")
    def test_apply_mirror_transform_false(self, mock_svg_item, service):
        """Test applying mirror transform when should_mirror is False."""
        mock_item = Mock(spec=QGraphicsSvgItem)
        mock_rect = Mock()
        mock_rect.center.return_value = QPointF(100, 100)
        mock_item.boundingRect.return_value = mock_rect

        service.apply_mirror_transform(mock_item, False)

        # Verify transform was applied (even for False, identity transform is applied)
        mock_item.setTransform.assert_called_once()

    def test_coordinate_system_constants(self, service):
        """Test that coordinate system constants are properly defined."""
        assert service.SCENE_SIZE == 950
        assert service.CENTER_X == 475.0
        assert service.CENTER_Y == 475.0

        # Test hand points are defined for all locations
        expected_locations = [
            Location.NORTH,
            Location.EAST,
            Location.SOUTH,
            Location.WEST,
            Location.NORTHEAST,
            Location.SOUTHEAST,
            Location.SOUTHWEST,
            Location.NORTHWEST,
        ]
        for location in expected_locations:
            assert location in service.HAND_POINTS
            assert location in service.LAYER2_POINTS

            # Verify points are QPointF instances
            assert isinstance(service.HAND_POINTS[location], QPointF)
            assert isinstance(service.LAYER2_POINTS[location], QPointF)
