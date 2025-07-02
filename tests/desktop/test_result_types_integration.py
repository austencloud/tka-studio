"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Ensure Result types and error handling architecture work correctly
PERMANENT: Result types are core to TKA's error handling architecture
AUTHOR: @ai-agent
"""

import pytest
from pathlib import Path
import tempfile
import pandas as pd
from core.testing.ai_agent_helpers import TKAAITestHelper

from core.types.result import (
    Result,
    Success,
    Failure,
    AppError,
    ErrorType,
    success,
    failure,
    app_error,
)
from core.types.coordinates import (
    PositionResult,
    qpoint_to_point,
    point_to_qpoint,
    get_default_point,
)
from core.types.geometry import Point
from core.config.data_config import DataConfig, create_data_config
from core.config.app_config import AppConfig, PositioningConfig, create_app_config
from application.services.data.data_service import DataService


@pytest.mark.specification
@pytest.mark.critical
class TestResultTypesContract:
    """PERMANENT: Result type behavioral contracts - NEVER DELETE"""

    def test_success_result(self):
        """Test Success result behavior."""
        result = success("test_value")

        assert result.is_success()
        assert not result.is_failure()
        assert result.unwrap() == "test_value"
        assert result.unwrap_or("default") == "test_value"

    def test_failure_result(self):
        """Test Failure result behavior."""
        error = app_error(ErrorType.VALIDATION_ERROR, "Test error")
        result = failure(error)

        assert not result.is_success()
        assert result.is_failure()
        assert result.unwrap_or("default") == "default"

        with pytest.raises(RuntimeError, match="Called unwrap\\(\\) on Failure"):
            result.unwrap()

    def test_app_error_formatting(self):
        """Test AppError string formatting."""
        error = app_error(
            ErrorType.POSITIONING_ERROR, "Test positioning error", {"x": 10, "y": 20}
        )

        error_str = str(error)
        assert "positioning_error" in error_str
        assert "Test positioning error" in error_str
        assert "x=10" in error_str
        assert "y=20" in error_str


@pytest.mark.specification
class TestCoordinateTypesContract:
    """PERMANENT: Coordinate type conversion contracts - NEVER DELETE"""

    def test_point_qpoint_conversion(self):
        """Test conversion between Point and QPointF."""
        # Test Point to QPointF
        point = Point(10.5, 20.7)
        qpoint = point_to_qpoint(point)

        assert qpoint.x() == 10.5
        assert qpoint.y() == 20.7

        # Test QPointF to Point
        converted_point = qpoint_to_point(qpoint)
        assert converted_point.x == 10.5
        assert converted_point.y == 20.7

    def test_safe_conversions(self):
        """Test safe conversion functions with error handling."""
        from core.types.coordinates import safe_qpoint_to_point, safe_point_to_qpoint

        # Test successful conversion
        point = Point(5.0, 15.0)
        qpoint_result = safe_point_to_qpoint(point)
        assert qpoint_result.is_success()
        assert qpoint_result.value.x() == 5.0

        # Test None handling
        none_result = safe_point_to_qpoint(None)
        assert none_result.is_failure()
        assert none_result.error.error_type == ErrorType.VALIDATION_ERROR


class TestDataConfiguration:
    """Test data configuration with Result types."""

    def test_data_config_creation_success(self):
        """Test successful data configuration creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test CSV files
            diamond_csv = temp_path / "DiamondPictographDataframe.csv"
            box_csv = temp_path / "BoxPictographDataframe.csv"

            # Create minimal CSV content
            test_data = pd.DataFrame({"letter": ["A", "B"], "value": [1, 2]})
            test_data.to_csv(diamond_csv, index=False)
            test_data.to_csv(box_csv, index=False)

            # Test configuration creation
            result = create_data_config(temp_path)
            assert result.is_success()

            config = result.value
            assert config.data_dir == temp_path
            assert config.diamond_csv_path == diamond_csv
            assert config.box_csv_path == box_csv

    def test_data_config_validation_failure(self):
        """Test data configuration validation with missing files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Don't create CSV files - should fail validation
            result = create_data_config(temp_path)
            assert result.is_failure()
            assert result.error.error_type == ErrorType.DATA_ERROR
            assert "Diamond CSV not found" in result.error.message


class TestDataService:
    """Test DataService with Result types."""

    def test_data_service_load_success(self):
        """Test successful data loading."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test CSV file
            diamond_csv = temp_path / "DiamondPictographDataframe.csv"
            test_data = pd.DataFrame(
                {
                    "letter": ["A", "B", "C"],
                    "motion_type": ["Pro", "Anti", "Static"],
                    "value": [1, 2, 3],
                }
            )
            test_data.to_csv(diamond_csv, index=False)

            # Create configuration and service
            config = DataConfig(
                temp_path, diamond_csv, temp_path / "BoxPictographDataframe.csv"
            )
            service = DataService(config)

            # Test loading
            result = service.load_diamond_dataset()
            assert result.is_success()

            df = result.value
            assert len(df) == 3
            assert "letter" in df.columns
            assert df.iloc[0]["letter"] == "A"

    def test_data_service_load_failure(self):
        """Test data loading failure handling."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create configuration with non-existent file
            config = DataConfig(
                temp_path,
                temp_path / "nonexistent.csv",
                temp_path / "BoxPictographDataframe.csv",
            )
            service = DataService(config)

            # Test loading failure
            result = service.load_diamond_dataset()
            assert result.is_failure()
            assert result.error.error_type == ErrorType.FILE_SYSTEM_ERROR
            assert "not found" in result.error.message


class TestAppConfiguration:
    """Test application configuration."""

    def test_app_config_creation(self):
        """Test application configuration creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test CSV files
            diamond_csv = temp_path / "DiamondPictographDataframe.csv"
            test_data = pd.DataFrame({"letter": ["A"], "value": [1]})
            test_data.to_csv(diamond_csv, index=False)

            # Create data config
            data_config = DataConfig(
                temp_path, diamond_csv, temp_path / "BoxPictographDataframe.csv"
            )

            # Create app config
            result = create_app_config(data_config=data_config)
            assert result.is_success()

            app_config = result.value
            assert app_config.data_config == data_config
            assert app_config.positioning.default_grid_mode == "diamond"
            assert app_config.ui.default_screen == "secondary"

    def test_positioning_config_validation(self):
        """Test positioning configuration validation."""
        from core.config.app_config import PositioningConfig

        # Test valid configuration
        valid_config = PositioningConfig(default_grid_mode="diamond")
        result = valid_config.validate()
        assert result.is_success()

        # Test invalid configuration
        invalid_config = PositioningConfig(default_grid_mode="invalid_mode")
        result = invalid_config.validate()
        assert result.is_failure()
        assert result.error.error_type == ErrorType.CONFIG_ERROR
        assert "Invalid grid mode" in result.error.message


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
