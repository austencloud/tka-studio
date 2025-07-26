"""
Test for Start Position Services

Basic tests to verify service structure and functionality.
"""

import pytest
from unittest.mock import Mock, patch

from desktop.modern.application.services.start_position import (
    StartPositionDataService,
    StartPositionSelectionService,
    StartPositionUIService,
    StartPositionOrchestrator
)
from desktop.modern.core.interfaces.start_position_services import (
    IStartPositionDataService,
    IStartPositionSelectionService,
    IStartPositionUIService,
    IStartPositionOrchestrator
)
from PyQt6.QtCore import QSize


class TestStartPositionDataService:
    """Test the StartPositionDataService implementation."""

    def test_service_implements_interface(self):
        """Test that the service implements the required interface."""
        service = StartPositionDataService()
        assert isinstance(service, IStartPositionDataService)

    def test_service_initialization(self):
        """Test that the service initializes correctly."""
        service = StartPositionDataService()
        assert service is not None
        assert hasattr(service, 'dataset_service')

    @patch('application.services.start_position.start_position_data_service.DatasetQuery')
    def test_get_position_data_calls_dataset_service(self, mock_dataset_query):
        """Test that get_position_data delegates to dataset service."""
        # Setup mock
        mock_dataset_instance = Mock()
        mock_dataset_query.return_value = mock_dataset_instance
        mock_dataset_instance.get_start_position_pictograph_data.return_value = Mock()

        # Create service and call method
        service = StartPositionDataService()
        result = service.get_position_data("alpha1_alpha1", "diamond")

        # Verify delegation
        mock_dataset_instance.get_start_position_pictograph_data.assert_called_once_with(
            "alpha1_alpha1", "diamond"
        )
        assert result is not None

    def test_get_available_positions_returns_list(self):
        """Test that get_available_positions returns a list."""
        service = StartPositionDataService()
        with patch.object(service.dataset_service, 'get_available_positions', return_value={"start_positions": ["alpha1", "beta5"]}):
            result = service.get_available_positions("diamond")
            assert isinstance(result, list)


class TestStartPositionSelectionService:
    """Test the StartPositionSelectionService implementation."""

    def test_service_implements_interface(self):
        """Test that the service implements the required interface."""
        service = StartPositionSelectionService()
        assert isinstance(service, IStartPositionSelectionService)

    def test_validate_selection_valid_position(self):
        """Test validation of valid position keys."""
        service = StartPositionSelectionService()
        
        # Test valid start position
        assert service.validate_selection("alpha1_alpha1") == True
        assert service.validate_selection("beta5_beta5") == True
        
    def test_validate_selection_invalid_position(self):
        """Test validation of invalid position keys."""
        service = StartPositionSelectionService()
        
        # Test invalid positions
        assert service.validate_selection("") == False
        assert service.validate_selection("invalid") == False
        assert service.validate_selection("alpha1_beta5_gamma11") == False

    def test_extract_end_position_from_key(self):
        """Test extraction of end position from position key."""
        service = StartPositionSelectionService()
        
        # Test valid extraction
        assert service.extract_end_position_from_key("alpha1_alpha1") == "alpha1"
        assert service.extract_end_position_from_key("beta5_gamma11") == "gamma11"
        
        # Test edge cases
        assert service.extract_end_position_from_key("singleposition") == "singleposition"
        assert service.extract_end_position_from_key("") == ""

    def test_normalize_position_key(self):
        """Test normalization of position keys."""
        service = StartPositionSelectionService()
        
        # Test normalization
        assert service.normalize_position_key("alpha1") == "alpha1_alpha1"
        assert service.normalize_position_key("alpha1_alpha1") == "alpha1_alpha1"
        assert service.normalize_position_key(" beta5 _ beta5 ") == "beta5_beta5"


class TestStartPositionUIService:
    """Test the StartPositionUIService implementation."""

    def test_service_implements_interface(self):
        """Test that the service implements the required interface."""
        service = StartPositionUIService()
        assert isinstance(service, IStartPositionUIService)

    def test_calculate_option_size(self):
        """Test option size calculation."""
        service = StartPositionUIService()
        
        # Test basic sizing
        size = service.calculate_option_size(1000, is_advanced=False)
        assert isinstance(size, int)
        assert 80 <= size <= 200  # Within expected range
        
        # Test advanced sizing
        advanced_size = service.calculate_option_size(1000, is_advanced=True)
        assert isinstance(advanced_size, int)
        assert 70 <= advanced_size <= 150  # Within expected range
        assert advanced_size <= size  # Advanced should be smaller

    def test_get_positions_for_mode(self):
        """Test getting positions for different modes."""
        service = StartPositionUIService()
        
        # Test basic diamond
        positions = service.get_positions_for_mode("diamond", is_advanced=False)
        assert len(positions) == 3
        assert "alpha1_alpha1" in positions
        
        # Test advanced diamond
        advanced_positions = service.get_positions_for_mode("diamond", is_advanced=True)
        assert len(advanced_positions) == 16
        
        # Test box mode
        box_positions = service.get_positions_for_mode("box", is_advanced=False)
        assert len(box_positions) == 3
        assert "alpha2_alpha2" in box_positions

    def test_get_grid_layout_config(self):
        """Test grid layout configuration."""
        service = StartPositionUIService()
        
        # Test basic config
        config = service.get_grid_layout_config("diamond", is_advanced=False)
        assert isinstance(config, dict)
        assert "rows" in config
        assert "cols" in config
        assert config["position_count"] == 3
        
        # Test advanced config
        advanced_config = service.get_grid_layout_config("diamond", is_advanced=True)
        assert advanced_config["position_count"] == 16

    def test_calculate_responsive_layout(self):
        """Test responsive layout calculation."""
        service = StartPositionUIService()
        
        # Test layout calculation
        layout = service.calculate_responsive_layout(QSize(800, 600), 3)
        assert isinstance(layout, dict)
        assert "rows" in layout
        assert "cols" in layout
        assert "option_size" in layout
        assert layout["position_count"] == 3


class TestStartPositionOrchestrator:
    """Test the StartPositionOrchestrator implementation."""

    def test_service_implements_interface(self):
        """Test that the service implements the required interface."""
        # Create mock dependencies
        data_service = Mock(spec=IStartPositionDataService)
        selection_service = Mock(spec=IStartPositionSelectionService)
        ui_service = Mock(spec=IStartPositionUIService)
        
        orchestrator = StartPositionOrchestrator(data_service, selection_service, ui_service)
        assert isinstance(orchestrator, IStartPositionOrchestrator)

    def test_orchestrator_initialization(self):
        """Test that the orchestrator initializes with dependencies."""
        data_service = Mock(spec=IStartPositionDataService)
        selection_service = Mock(spec=IStartPositionSelectionService)
        ui_service = Mock(spec=IStartPositionUIService)
        
        orchestrator = StartPositionOrchestrator(data_service, selection_service, ui_service)
        
        assert orchestrator.data_service == data_service
        assert orchestrator.selection_service == selection_service
        assert orchestrator.ui_service == ui_service

    def test_get_position_data_for_display(self):
        """Test getting position data for display."""
        data_service = Mock(spec=IStartPositionDataService)
        selection_service = Mock(spec=IStartPositionSelectionService)
        ui_service = Mock(spec=IStartPositionUIService)
        
        # Setup mock return value
        mock_data = Mock()
        data_service.get_position_data.return_value = mock_data
        
        orchestrator = StartPositionOrchestrator(data_service, selection_service, ui_service)
        result = orchestrator.get_position_data_for_display("alpha1_alpha1", "diamond")
        
        # Verify delegation
        data_service.get_position_data.assert_called_once_with("alpha1_alpha1", "diamond")
        assert result == mock_data

    @patch('application.services.start_position.start_position_orchestrator.get_command_processor')
    def test_handle_position_selection_success(self, mock_get_processor):
        """Test successful position selection workflow."""
        # Setup mocks
        data_service = Mock(spec=IStartPositionDataService)
        selection_service = Mock(spec=IStartPositionSelectionService)
        ui_service = Mock(spec=IStartPositionUIService)
        
        # Mock validation and command creation
        selection_service.validate_selection.return_value = True
        mock_command = Mock()
        selection_service.create_selection_command.return_value = mock_command
        
        # Mock command processor
        mock_processor = Mock()
        mock_result = Mock()
        mock_result.success = True
        mock_processor.execute.return_value = mock_result
        mock_get_processor.return_value = mock_processor
        
        # Test
        orchestrator = StartPositionOrchestrator(data_service, selection_service, ui_service)
        result = orchestrator.handle_position_selection("alpha1_alpha1")
        
        # Verify workflow
        selection_service.validate_selection.assert_called_once_with("alpha1_alpha1")
        selection_service.create_selection_command.assert_called_once_with("alpha1_alpha1")
        mock_processor.execute.assert_called_once_with(mock_command)
        assert result == True

    def test_handle_position_selection_validation_failure(self):
        """Test position selection with validation failure."""
        data_service = Mock(spec=IStartPositionDataService)
        selection_service = Mock(spec=IStartPositionSelectionService)
        ui_service = Mock(spec=IStartPositionUIService)
        
        # Mock validation failure
        selection_service.validate_selection.return_value = False
        
        orchestrator = StartPositionOrchestrator(data_service, selection_service, ui_service)
        result = orchestrator.handle_position_selection("invalid_position")
        
        # Verify early exit on validation failure
        selection_service.validate_selection.assert_called_once_with("invalid_position")
        selection_service.create_selection_command.assert_not_called()
        assert result == False


if __name__ == "__main__":
    pytest.main([__file__])
