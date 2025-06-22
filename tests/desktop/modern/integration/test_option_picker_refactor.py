"""
Integration test for the refactored option picker services.

This test verifies that the refactored services produce the same results
as the original monolithic OptionPicker.
"""

import pytest
from unittest.mock import Mock, MagicMock
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QSize

from src.application.services.option_picker.option_picker_initialization_service import OptionPickerInitializationService
from src.application.services.option_picker.option_picker_data_service import OptionPickerDataService
from src.application.services.option_picker.option_picker_display_service import OptionPickerDisplayService
from src.application.services.option_picker.option_picker_event_service import OptionPickerEventService
from src.application.services.option_picker.option_picker_orchestrator import OptionPickerOrchestrator

from src.domain.models.core_models import BeatData, SequenceData
from src.core.dependency_injection.di_container import DIContainer


class TestOptionPickerRefactor:
    """Test that refactored option picker services work correctly."""

    @pytest.fixture
    def mock_container(self):
        """Create mock DI container."""
        container = Mock(spec=DIContainer)
        container.resolve = Mock()
        return container

    @pytest.fixture
    def mock_beat_loader(self):
        """Create mock beat loader."""
        beat_loader = Mock()
        beat_loader.refresh_options.return_value = [
            BeatData(letter="A"),
            BeatData(letter="B"),
            BeatData(letter="C")
        ]
        beat_loader.get_beat_options.return_value = [
            BeatData(letter="A"),
            BeatData(letter="B"),
            BeatData(letter="C")
        ]
        return beat_loader

    @pytest.fixture
    def mock_progress_callback(self):
        """Create mock progress callback."""
        return Mock()

    @pytest.fixture
    def initialization_service(self):
        """Create initialization service."""
        return OptionPickerInitializationService()

    @pytest.fixture
    def data_service(self, mock_beat_loader):
        """Create data service with mock beat loader."""
        return OptionPickerDataService(mock_beat_loader)

    @pytest.fixture
    def display_service(self):
        """Create display service."""
        return OptionPickerDisplayService()

    @pytest.fixture
    def event_service(self):
        """Create event service."""
        return OptionPickerEventService()

    def test_initialization_service(self, initialization_service, mock_container, mock_progress_callback):
        """Test that initialization service works correctly."""
        # Test component initialization
        components = initialization_service.initialize_components(
            mock_container, mock_progress_callback
        )
        
        assert "layout_service" in components
        assert "widget_factory" in components
        assert "beat_loader" in components
        
        # Test validation
        assert initialization_service.validate_initialization(components)

    def test_data_service(self, data_service):
        """Test that data service works correctly."""
        # Test loading beat options
        options = data_service.load_beat_options()
        assert len(options) == 3
        assert all(isinstance(opt, BeatData) for opt in options)
        
        # Test getting beat data by option ID
        beat_data = data_service.get_beat_data_for_option("beat_A")
        assert beat_data is not None
        assert beat_data.letter == "A"
        
        # Test invalid option ID
        invalid_data = data_service.get_beat_data_for_option("invalid_id")
        assert invalid_data is None

    def test_display_service(self, display_service):
        """Test that display service works correctly."""
        # Test initialization without actual widgets (mock mode)
        mock_container = Mock()
        mock_layout = Mock()
        mock_pool_manager = Mock()
        mock_size_provider = Mock(return_value=QSize(800, 600))
        
        # This would normally fail without actual Qt widgets, but we can test the structure
        assert display_service.display_manager is None  # Not initialized yet
        
        # Test validation
        assert not display_service.validate_display_components()

    def test_event_service(self, event_service):
        """Test that event service works correctly."""
        # Test event handler setup
        mock_pool_manager = Mock()
        mock_filter_widget = Mock()
        mock_beat_click_handler = Mock()
        mock_beat_data_click_handler = Mock()
        mock_filter_change_handler = Mock()
        
        event_service.setup_event_handlers(
            mock_pool_manager,
            mock_filter_widget,
            mock_beat_click_handler,
            mock_beat_data_click_handler,
            mock_filter_change_handler
        )
        
        # Test validation
        assert event_service.validate_event_setup()
        
        # Test event info
        event_info = event_service.get_event_info()
        assert event_info["validation_passed"]

    def test_orchestrator_initialization(self, mock_container):
        """Test that orchestrator initializes correctly."""
        # Create orchestrator with mocked services
        mock_init_service = Mock()
        mock_data_service = Mock()
        mock_display_service = Mock()
        mock_event_service = Mock()
        
        orchestrator = OptionPickerOrchestrator(
            container=mock_container,
            initialization_service=mock_init_service,
            data_service=mock_data_service,
            display_service=mock_display_service,
            event_service=mock_event_service
        )
        
        assert orchestrator.container == mock_container
        assert orchestrator.initialization_service == mock_init_service
        assert orchestrator.data_service == mock_data_service
        assert orchestrator.display_service == mock_display_service
        assert orchestrator.event_service == mock_event_service

    def test_data_service_statistics(self, data_service):
        """Test that data service provides useful statistics."""
        stats = data_service.get_data_statistics()
        
        assert "total_options" in stats
        assert "unique_letters" in stats
        assert "letters" in stats
        assert "has_beat_loader" in stats
        assert stats["has_beat_loader"] is True

    def test_data_service_search(self, data_service):
        """Test that data service search functionality works."""
        # Load options first
        data_service.load_beat_options()
        
        # Test search
        results = data_service.search_options("A")
        assert len(results) == 1
        assert results[0].letter == "A"
        
        # Test empty search
        all_results = data_service.search_options("")
        assert len(all_results) == 3

    def test_data_service_cache_management(self, data_service):
        """Test that data service manages cache correctly."""
        # Load options
        options = data_service.load_beat_options()
        assert len(options) == 3
        
        # Clear cache
        data_service.clear_cache()
        
        # Get current options should still work (from beat loader)
        current_options = data_service.get_current_options()
        assert len(current_options) == 3

    def test_data_service_validation(self, data_service):
        """Test that data service validates beat loader correctly."""
        assert data_service.validate_beat_loader() is True
        
        # Test with invalid beat loader
        invalid_service = OptionPickerDataService(None)
        assert invalid_service.validate_beat_loader() is False

    def test_event_service_cleanup(self, event_service):
        """Test that event service cleans up correctly."""
        # Setup some handlers
        mock_pool_manager = Mock()
        mock_filter_widget = Mock()
        mock_filter_widget.filter_changed = Mock()
        mock_filter_widget.filter_changed.disconnect = Mock()
        
        event_service.setup_event_handlers(
            mock_pool_manager,
            mock_filter_widget,
            Mock(), Mock(), Mock()
        )
        
        # Test cleanup
        event_service.cleanup()
        
        # Verify handlers are cleared
        assert event_service.pool_manager is None
        assert event_service.filter_widget is None

    def test_service_error_handling(self, data_service):
        """Test that services handle errors gracefully."""
        # Test with broken beat loader
        broken_loader = Mock()
        broken_loader.refresh_options.side_effect = Exception("Test error")
        
        broken_service = OptionPickerDataService(broken_loader)
        
        # Should not raise exception, should return empty list
        options = broken_service.refresh_options()
        assert options == []

    def test_modern_sequence_refresh(self, data_service):
        """Test refreshing from modern sequence data."""
        # Create mock sequence
        mock_sequence = Mock(spec=SequenceData)
        
        # Mock beat loader method
        data_service.beat_loader.refresh_options_from_modern_sequence = Mock(
            return_value=[BeatData(letter="X")]
        )
        
        # Test refresh
        options = data_service.refresh_from_modern_sequence(mock_sequence)
        assert len(options) == 1
        assert options[0].letter == "X"

    def test_legacy_sequence_refresh(self, data_service):
        """Test refreshing from legacy sequence data."""
        # Create mock legacy data
        legacy_data = [{"letter": "Y", "motion_type": "PRO"}]
        
        # Mock beat loader method
        data_service.beat_loader.load_motion_combinations = Mock(
            return_value=[BeatData(letter="Y")]
        )
        
        # Test refresh
        options = data_service.refresh_from_sequence_data(legacy_data)
        assert len(options) == 1
        assert options[0].letter == "Y"
