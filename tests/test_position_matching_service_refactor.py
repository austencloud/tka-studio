"""
Test suite for the refactored PositionMatchingService.

This test suite verifies that the PositionMatchingService correctly:
1. Returns PictographData instead of BeatData
2. Uses GlyphDataService for glyph generation
3. Maintains all existing functionality
4. Properly converts dictionary data to PictographData
"""

import pytest
from unittest.mock import Mock, patch
from typing import List, Dict, Any

from domain.models import (
    PictographData,
    GlyphData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)
from domain.models.pictograph_models import ArrowData, GridData, GridMode
from application.services.positioning.arrows.utilities.position_matching_service import (
    PositionMatchingService,
)


class TestPositionMatchingServiceRefactor:
    """Test suite for the refactored PositionMatchingService."""

    @pytest.fixture
    def mock_dataset(self) -> Dict[str, List[Dict[str, Any]]]:
        """Create a mock dataset for testing."""
        return {
            "A": [
                {
                    "letter": "A",
                    "start_pos": "alpha1",
                    "end_pos": "beta1",
                    "blue_attributes": {
                        "motion_type": "pro",
                        "prop_rot_dir": "cw",
                        "start_loc": "n",
                        "end_loc": "s",
                        "start_ori": "in",
                        "end_ori": "out",
                        "turns": 1.0,
                    },
                    "red_attributes": {
                        "motion_type": "anti",
                        "prop_rot_dir": "ccw",
                        "start_loc": "s",
                        "end_loc": "n",
                        "start_ori": "out",
                        "end_ori": "in",
                        "turns": 1.0,
                    },
                }
            ],
            "B": [
                {
                    "letter": "B",
                    "start_pos": "beta1",
                    "end_pos": "alpha2",
                    "blue_attributes": {
                        "motion_type": "static",
                        "prop_rot_dir": "no_rot",
                        "start_loc": "e",
                        "end_loc": "e",
                        "start_ori": "in",
                        "end_ori": "in",
                        "turns": 0.0,
                    },
                    "red_attributes": {
                        "motion_type": "dash",
                        "prop_rot_dir": "no_rot",
                        "start_loc": "w",
                        "end_loc": "w",
                        "start_ori": "out",
                        "end_ori": "out",
                        "turns": 0.0,
                    },
                }
            ],
        }

    @pytest.fixture
    def service_with_mock_dataset(self, mock_dataset):
        """Create a PositionMatchingService with mocked dataset."""
        service = PositionMatchingService()
        service.pictograph_dataset = mock_dataset
        return service

    def test_get_next_options_returns_pictograph_data(self, service_with_mock_dataset):
        """Test that get_next_options returns List[PictographData]."""
        options = service_with_mock_dataset.get_next_options("alpha1")
        
        assert isinstance(options, list)
        assert len(options) == 1
        assert isinstance(options[0], PictographData)

    def test_pictograph_data_structure(self, service_with_mock_dataset):
        """Test that returned PictographData has correct structure."""
        options = service_with_mock_dataset.get_next_options("alpha1")
        pictograph = options[0]
        
        # Check basic fields
        assert pictograph.letter == "A"
        assert pictograph.start_position == "alpha1"
        assert pictograph.end_position == "beta1"
        
        # Check arrows
        assert "blue" in pictograph.arrows
        assert "red" in pictograph.arrows
        
        # Check arrow motion data
        blue_arrow = pictograph.arrows["blue"]
        assert isinstance(blue_arrow, ArrowData)
        assert blue_arrow.motion_data.motion_type == MotionType.PRO
        assert blue_arrow.motion_data.start_loc == Location.NORTH
        assert blue_arrow.motion_data.end_loc == Location.SOUTH
        
        red_arrow = pictograph.arrows["red"]
        assert isinstance(red_arrow, ArrowData)
        assert red_arrow.motion_data.motion_type == MotionType.ANTI
        assert red_arrow.motion_data.start_loc == Location.SOUTH
        assert red_arrow.motion_data.end_loc == Location.NORTH

    def test_glyph_data_generation(self, service_with_mock_dataset):
        """Test that glyph data is properly generated using GlyphDataService."""
        with patch('application.services.data.glyph_data_service.GlyphDataService') as mock_glyph_service:
            mock_glyph_instance = Mock()
            mock_glyph_data = GlyphData(
                vtg_mode=None,
                elemental_type=None,
                letter_type=None,
                has_dash=False,
                turns_data=None,
                start_position="alpha1",
                end_position="beta1",
                show_elemental=True,
                show_vtg=True,
                show_tka=True,
                show_positions=True,
            )
            mock_glyph_instance.determine_glyph_data.return_value = mock_glyph_data
            mock_glyph_service.return_value = mock_glyph_instance
            
            options = service_with_mock_dataset.get_next_options("alpha1")
            pictograph = options[0]
            
            # Verify glyph service was called
            mock_glyph_service.assert_called_once()
            mock_glyph_instance.determine_glyph_data.assert_called_once()
            
            # Verify glyph data is attached
            assert pictograph.glyph_data is not None

    def test_position_matching_algorithm(self, service_with_mock_dataset):
        """Test that the position matching algorithm works correctly."""
        # Test alpha1 -> should find A
        alpha1_options = service_with_mock_dataset.get_next_options("alpha1")
        assert len(alpha1_options) == 1
        assert alpha1_options[0].letter == "A"
        
        # Test beta1 -> should find B
        beta1_options = service_with_mock_dataset.get_next_options("beta1")
        assert len(beta1_options) == 1
        assert beta1_options[0].letter == "B"
        
        # Test non-existent position -> should return empty list
        empty_options = service_with_mock_dataset.get_next_options("gamma1")
        assert len(empty_options) == 0

    def test_get_alpha1_options_convenience_method(self, service_with_mock_dataset):
        """Test the get_alpha1_options convenience method."""
        options = service_with_mock_dataset.get_alpha1_options()
        
        assert isinstance(options, list)
        assert len(options) == 1
        assert isinstance(options[0], PictographData)
        assert options[0].letter == "A"

    def test_motion_type_parsing(self, service_with_mock_dataset):
        """Test that motion types are correctly parsed."""
        service = service_with_mock_dataset
        
        assert service._parse_motion_type("pro") == MotionType.PRO
        assert service._parse_motion_type("anti") == MotionType.ANTI
        assert service._parse_motion_type("static") == MotionType.STATIC
        assert service._parse_motion_type("dash") == MotionType.DASH
        assert service._parse_motion_type("unknown") == MotionType.STATIC

    def test_rotation_direction_parsing(self, service_with_mock_dataset):
        """Test that rotation directions are correctly parsed."""
        service = service_with_mock_dataset
        
        assert service._parse_rotation_direction("cw") == RotationDirection.CLOCKWISE
        assert service._parse_rotation_direction("ccw") == RotationDirection.COUNTER_CLOCKWISE
        assert service._parse_rotation_direction("no_rot") == RotationDirection.NO_ROTATION
        assert service._parse_rotation_direction("unknown") == RotationDirection.NO_ROTATION

    def test_location_parsing(self, service_with_mock_dataset):
        """Test that locations are correctly parsed."""
        service = service_with_mock_dataset
        
        assert service._parse_location("n") == Location.NORTH
        assert service._parse_location("s") == Location.SOUTH
        assert service._parse_location("e") == Location.EAST
        assert service._parse_location("w") == Location.WEST
        assert service._parse_location("unknown") == Location.SOUTH

    def test_empty_dataset_handling(self):
        """Test that service handles empty dataset gracefully."""
        service = PositionMatchingService()
        service.pictograph_dataset = {}
        
        options = service.get_next_options("alpha1")
        assert options == []

    def test_none_dataset_handling(self):
        """Test that service handles None dataset gracefully."""
        service = PositionMatchingService()
        service.pictograph_dataset = None
        
        options = service.get_next_options("alpha1")
        assert options == []

    def test_grid_data_creation(self, service_with_mock_dataset):
        """Test that grid data is properly created."""
        options = service_with_mock_dataset.get_next_options("alpha1")
        pictograph = options[0]
        
        assert isinstance(pictograph.grid_data, GridData)
        assert pictograph.grid_data.grid_mode == GridMode.DIAMOND
        assert pictograph.grid_data.center_x == 200.0
        assert pictograph.grid_data.center_y == 200.0
        assert pictograph.grid_data.radius == 100.0

    def test_metadata_preservation(self, service_with_mock_dataset):
        """Test that metadata is properly preserved."""
        options = service_with_mock_dataset.get_next_options("alpha1")
        pictograph = options[0]
        
        assert "source" in pictograph.metadata
        assert pictograph.metadata["source"] == "position_matching_service"
        assert "original_data" in pictograph.metadata
