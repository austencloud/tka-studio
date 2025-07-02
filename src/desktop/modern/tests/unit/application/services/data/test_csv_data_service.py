"""
TEST LIFECYCLE: UNIT
PURPOSE: Test CSVDataService data loading and conversion functionality
AUTHOR: @ai-agent
"""

import pytest
from unittest.mock import Mock, patch
import pandas as pd

from domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)
from application.services.data.csv_data_service import (
    CSVDataService,
    ICSVDataService,
)


@pytest.mark.unit
class TestCSVDataService:
    """Test suite for CSVDataService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = CSVDataService()

    def test_interface_compliance(self):
        """Test that CSVDataService implements the interface correctly."""
        assert isinstance(self.service, ICSVDataService)

    @patch("pandas.read_csv")
    def test_load_csv_data_success(self, mock_read_csv):
        """Test successful CSV data loading."""
        # Mock DataFrame
        mock_df = pd.DataFrame(
            {
                "letter": ["A", "B"],
                "blue_motion_type": ["pro", "static"],
                "blue_start_loc": ["n", "e"],
                "blue_end_loc": ["s", "e"],
            }
        )
        mock_read_csv.return_value = mock_df

        # Test loading
        result = self.service.load_csv_data()

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        mock_read_csv.assert_called_once()

    @patch("pandas.read_csv")
    def test_load_csv_data_error_handling(self, mock_read_csv):
        """Test CSV loading error handling."""
        # Mock exception
        mock_read_csv.side_effect = FileNotFoundError("File not found")

        # Test error handling
        result = self.service.load_csv_data()

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0  # Empty DataFrame on error

    def test_convert_row_to_beat_data(self):
        """Test CSV row to BeatData conversion."""
        # Create test row
        row = pd.Series(
            {
                "letter": "A",
                "beat_number": 1,
                "blue_motion_type": "pro",
                "blue_prop_rot_dir": "cw",
                "blue_start_loc": "n",
                "blue_end_loc": "s",
                "red_motion_type": "anti",
                "red_prop_rot_dir": "ccw",
                "red_start_loc": "e",
                "red_end_loc": "w",
            }
        )

        # Convert to BeatData
        result = self.service.convert_row_to_beat_data(row)

        # Verify conversion
        assert isinstance(result, BeatData)
        assert result.letter == "A"
        assert result.beat_number == 1

        # Verify blue motion
        assert result.blue_motion is not None
        assert result.blue_motion.motion_type == MotionType.PRO
        assert result.blue_motion.prop_rot_dir == RotationDirection.CLOCKWISE
        assert result.blue_motion.start_loc == Location.NORTH
        assert result.blue_motion.end_loc == Location.SOUTH

        # Verify red motion
        assert result.red_motion is not None
        assert result.red_motion.motion_type == MotionType.ANTI
        assert result.red_motion.prop_rot_dir == RotationDirection.COUNTER_CLOCKWISE
        assert result.red_motion.start_loc == Location.EAST
        assert result.red_motion.end_loc == Location.WEST

    def test_convert_row_partial_data(self):
        """Test conversion with partial motion data."""
        # Create row with only blue motion
        row = pd.Series(
            {
                "letter": "B",
                "beat_number": 2,
                "blue_motion_type": "static",
                "blue_prop_rot_dir": "no_rot",
                "blue_start_loc": "n",
                "blue_end_loc": "n",
                "red_motion_type": "",  # Empty red motion
            }
        )

        result = self.service.convert_row_to_beat_data(row)

        assert result.letter == "B"
        assert result.blue_motion is not None
        assert result.blue_motion.motion_type == MotionType.STATIC
        assert result.red_motion is None

    @patch.object(CSVDataService, "_load_cached_data")
    def test_get_pictographs_by_letter(self, mock_load_data):
        """Test getting pictographs by letter."""
        # Mock DataFrame
        mock_df = pd.DataFrame(
            {
                "letter": ["A", "A", "B"],
                "blue_motion_type": ["pro", "static", "anti"],
                "blue_start_loc": ["n", "e", "s"],
                "blue_end_loc": ["s", "e", "n"],
            }
        )
        mock_load_data.return_value = mock_df

        # Test getting pictographs for letter 'A'
        results = self.service.get_pictographs_by_letter("A")

        assert len(results) == 2
        assert all(isinstance(beat, BeatData) for beat in results)
        assert all(beat.letter == "A" for beat in results)

    @patch.object(CSVDataService, "_load_cached_data")
    def test_get_specific_pictograph(self, mock_load_data):
        """Test getting specific pictograph by letter and index."""
        # Mock DataFrame
        mock_df = pd.DataFrame(
            {
                "letter": ["A", "A", "B"],
                "blue_motion_type": ["pro", "static", "anti"],
                "blue_start_loc": ["n", "e", "s"],
                "blue_end_loc": ["s", "e", "n"],
            }
        )
        mock_load_data.return_value = mock_df

        # Test getting first 'A' pictograph
        result = self.service.get_specific_pictograph("A", 0)
        assert result is not None
        assert result.letter == "A"
        assert result.blue_motion.motion_type == MotionType.PRO

        # Test getting second 'A' pictograph
        result = self.service.get_specific_pictograph("A", 1)
        assert result is not None
        assert result.letter == "A"
        assert result.blue_motion.motion_type == MotionType.STATIC

        # Test getting non-existent index
        result = self.service.get_specific_pictograph("A", 5)
        assert result is None

        # Test getting non-existent letter
        result = self.service.get_specific_pictograph("Z", 0)
        assert result is None

    def test_get_start_position_pictograph(self):
        """Test getting start position pictograph."""
        # Mock the get_pictographs_by_letter method
        with patch.object(self.service, "get_pictographs_by_letter") as mock_get:
            mock_beat = BeatData(letter="A", beat_number=1)
            mock_get.return_value = [mock_beat]

            # Test valid position key
            result = self.service.get_start_position_pictograph("alpha1_alpha1")
            assert result == mock_beat
            mock_get.assert_called_once_with("A")

            # Test invalid position key
            result = self.service.get_start_position_pictograph("invalid_key")
            assert result is None

    def test_clear_cache(self):
        """Test cache clearing functionality."""
        # Set some cached data
        self.service._csv_data = pd.DataFrame({"test": [1, 2, 3]})

        # Clear cache
        self.service.clear_cache()

        # Verify cache is cleared
        assert self.service._csv_data is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
