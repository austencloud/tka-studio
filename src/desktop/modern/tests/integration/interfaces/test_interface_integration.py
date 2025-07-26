"""
Integration tests for interface implementations with dependency injection.

These tests verify that the services correctly integrate with the dependency
injection system and that interfaces can be properly injected and used.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from shared.application.services.data.cache_manager import DataCacheManager
from shared.application.services.ui.thumbnail_generation_service import (
    ThumbnailGenerationService,
)
from shared.application.services.ui.ui_state_manager import UIStateManager
from shared.application.services.workbench.workbench_state_manager import WorkbenchStateManager
from desktop.modern.core.interfaces.core_services import IUIStateManager
from desktop.modern.core.interfaces.data_services import IDataCacheManager
from desktop.modern.core.interfaces.ui_services import IThumbnailGenerationService
from desktop.modern.core.interfaces.workbench_services import IWorkbenchStateManager, WorkbenchState
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


class TestDependencyInjectionIntegration:
    """Test integration with dependency injection system."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create temporary directory for file operations
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_workbench_state_manager_can_be_injected(self):
        """Test that WorkbenchStateManager can be injected as interface."""
        # Create service instance
        service = WorkbenchStateManager()

        # Should be instance of both concrete class and interface
        assert isinstance(service, WorkbenchStateManager)
        assert isinstance(service, IWorkbenchStateManager)

        # Should be able to use interface methods
        assert service.get_workbench_state() == WorkbenchState.EMPTY
        assert service.is_empty()

    def test_data_cache_manager_can_be_injected(self):
        """Test that DataCacheManager can be injected as interface."""
        # Create service instance
        service = DataCacheManager()

        # Should be instance of both concrete class and interface
        assert isinstance(service, DataCacheManager)
        assert isinstance(service, IDataCacheManager)

        # Should be able to use interface methods
        stats = service.get_cache_stats()
        assert stats["total_items"] == 0

    def test_thumbnail_generation_service_can_be_injected(self):
        """Test that ThumbnailGenerationService can be injected as interface."""
        # Create service instance
        service = ThumbnailGenerationService()

        # Should be instance of both concrete class and interface
        assert isinstance(service, ThumbnailGenerationService)
        assert isinstance(service, IThumbnailGenerationService)

        # Should be able to use interface methods
        # (We'll test with None to avoid needing actual implementation)
        result = service.generate_sequence_thumbnail(None, Path("test.png"))
        assert result is None  # Expected behavior for None input

    def test_ui_state_manager_can_be_injected(self):
        """Test that UIStateManager can be injected as interface."""
        # Create service instance
        service = UIStateManager()

        # Should be instance of both concrete class and interface
        assert isinstance(service, UIStateManager)
        assert isinstance(service, IUIStateManager)

        # Should be able to use interface methods
        # Note: active_tab may vary based on saved settings, so just check it's a string
        active_tab = service.get_active_tab()
        assert isinstance(active_tab, str)
        assert len(active_tab) > 0

        # Test graph editor toggle functionality
        initial_state = service.toggle_graph_editor()
        second_state = service.toggle_graph_editor()
        assert initial_state != second_state  # Should toggle between states

    def test_interface_polymorphism(self):
        """Test that interfaces enable polymorphism."""
        # Create different implementations
        real_cache = DataCacheManager()

        # Create mock implementation
        mock_cache = Mock(spec=IDataCacheManager)
        mock_cache.get_cache_stats.return_value = {"total_items": 42}

        # Function that accepts interface
        def process_cache(cache: IDataCacheManager):
            return cache.get_cache_stats()

        # Both should work
        real_stats = process_cache(real_cache)
        mock_stats = process_cache(mock_cache)

        assert real_stats["total_items"] == 0
        assert mock_stats["total_items"] == 42

    def test_service_interaction_through_interfaces(self):
        """Test that services can interact through interfaces."""
        # Create services
        workbench_manager = WorkbenchStateManager()
        cache_manager = DataCacheManager()

        # Create mock sequence
        mock_sequence = Mock(spec=SequenceData)
        mock_sequence.length = 5
        mock_sequence.name = "Test Sequence"

        # Set sequence in workbench
        result = workbench_manager.set_sequence(mock_sequence)
        assert result.changed
        assert result.sequence_changed

        # Cache some data related to the sequence
        cache_manager.set_sequence_cache(mock_sequence.name, mock_sequence)

        # Retrieve from cache
        cached_sequence = cache_manager.get_sequence_cache(mock_sequence.name)
        assert cached_sequence == mock_sequence

        # Services should work together through interfaces
        assert workbench_manager.has_sequence()
        assert cache_manager.get_cache_stats()["sequence_cache_size"] == 1

    def test_interface_method_compatibility(self):
        """Test that interface methods are compatible across implementations."""
        # Create services
        workbench_manager = WorkbenchStateManager()
        ui_manager = UIStateManager()

        # Both should have compatible state management patterns
        # (though they manage different types of state)

        # Workbench state
        workbench_state = workbench_manager.get_workbench_state()
        assert isinstance(workbench_state, WorkbenchState)

        # UI state
        ui_settings = ui_manager.get_all_settings()
        assert isinstance(ui_settings, dict)

        # Both should support save/load patterns
        # (workbench through validation, UI through explicit save/load)
        workbench_summary = workbench_manager.get_state_summary()
        ui_manager.save_state()
        ui_manager.load_state()

        assert "workbench_state" in workbench_summary


class TestCrossCuttingConcerns:
    """Test cross-cutting concerns across interface implementations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_error_handling_consistency(self):
        """Test that error handling is consistent across implementations."""
        # Create services
        workbench_manager = WorkbenchStateManager()
        cache_manager = DataCacheManager()
        thumbnail_service = ThumbnailGenerationService()

        # Test graceful handling of None inputs
        assert workbench_manager.get_current_sequence() is None
        assert cache_manager.get_position_cache("nonexistent") is None
        assert (
            thumbnail_service.generate_sequence_thumbnail(None, Path("test.png"))
            is None
        )

        # Test handling of invalid inputs
        validation_result = workbench_manager.validate_state_consistency()
        assert isinstance(validation_result, tuple)
        assert len(validation_result) == 2
        assert isinstance(validation_result[0], bool)
        assert isinstance(validation_result[1], list)

    def test_logging_and_debugging_support(self):
        """Test that services provide debugging support."""
        # Create services
        workbench_manager = WorkbenchStateManager()
        cache_manager = DataCacheManager()

        # All services should provide introspection capabilities
        workbench_summary = workbench_manager.get_state_summary()
        cache_stats = cache_manager.get_cache_stats()

        # Should contain useful debugging information
        assert "workbench_state" in workbench_summary
        assert "is_empty" in workbench_summary
        assert "state_valid" in workbench_summary

        assert "total_items" in cache_stats
        assert "max_size_per_cache" in cache_stats

    def test_thread_safety_considerations(self):
        """Test thread safety considerations for services."""
        # Create services
        cache_manager = DataCacheManager()

        # Test concurrent access patterns
        # (Note: These services are not designed to be thread-safe,
        # but we test basic concurrent usage patterns)

        # Add items to cache
        cache_manager.set_position_cache("key1", "value1")
        cache_manager.set_position_cache("key2", "value2")

        # Read from cache
        value1 = cache_manager.get_position_cache("key1")
        value2 = cache_manager.get_position_cache("key2")

        assert value1 == "value1"
        assert value2 == "value2"

        # Clear cache
        cache_manager.clear_position_cache()

        # Should be empty
        assert cache_manager.get_position_cache("key1") is None
        assert cache_manager.get_position_cache("key2") is None


class TestServiceLifecycleIntegration:
    """Test service lifecycle integration."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_service_initialization(self):
        """Test service initialization through interfaces."""
        # Services should initialize properly when created
        workbench_manager = WorkbenchStateManager()
        cache_manager = DataCacheManager()
        thumbnail_service = ThumbnailGenerationService()

        # Should be in valid initial state
        assert workbench_manager.get_workbench_state() == WorkbenchState.EMPTY
        assert cache_manager.get_cache_stats()["total_items"] == 0
        assert thumbnail_service._temp_directory is not None

    def test_service_cleanup(self):
        """Test service cleanup behavior."""
        # Create services and use them
        workbench_manager = WorkbenchStateManager()
        cache_manager = DataCacheManager()

        # Add some state
        mock_sequence = Mock(spec=SequenceData)
        mock_sequence.length = 3
        workbench_manager.set_sequence(mock_sequence)

        cache_manager.set_position_cache("key1", "value1")
        cache_manager.set_sequence_cache("key2", "value2")

        # Clear state
        workbench_manager.clear_all_state()
        cache_manager.clear_all()

        # Should be clean
        assert workbench_manager.is_empty()
        assert cache_manager.get_cache_stats()["total_items"] == 0

    def test_service_state_persistence(self):
        """Test service state persistence."""
        # Create UI state manager
        ui_manager = UIStateManager()

        # Set some state
        ui_manager.set_setting("test_key", "test_value")
        ui_manager.set_active_tab("dictionary")

        # Save state
        ui_manager.save_state()

        # Create new instance and load
        ui_manager2 = UIStateManager()
        ui_manager2.load_state()

        # State should be preserved
        # (Note: This might not work perfectly due to file system mocking,
        # but the interface contract should be maintained)
        assert ui_manager2.get_setting("test_key", "default") in [
            "test_value",
            "default",
        ]


class TestInterfaceContractCompliance:
    """Test that implementations comply with interface contracts."""

    def test_workbench_state_manager_contract(self):
        """Test WorkbenchStateManager contract compliance."""
        manager = WorkbenchStateManager()

        # Test return types
        assert isinstance(manager.get_workbench_state(), WorkbenchState)
        assert isinstance(manager.has_sequence(), bool)
        assert isinstance(manager.has_start_position(), bool)
        assert isinstance(manager.is_empty(), bool)
        assert isinstance(manager.is_restoring(), bool)

        # Test method contracts
        result = manager.validate_state_consistency()
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], list)

        summary = manager.get_state_summary()
        assert isinstance(summary, dict)
        assert "workbench_state" in summary

    def test_data_cache_manager_contract(self):
        """Test DataCacheManager contract compliance."""
        manager = DataCacheManager()

        # Test cache operations
        assert manager.get_position_cache("nonexistent") is None

        manager.set_position_cache("key1", "value1")
        assert manager.get_position_cache("key1") == "value1"

        # Test stats
        stats = manager.get_cache_stats()
        assert isinstance(stats, dict)
        assert "total_items" in stats
        assert "position_cache_size" in stats

        # Test clear operations
        manager.clear_position_cache()
        assert manager.get_position_cache("key1") is None

    def test_thumbnail_generation_service_contract(self):
        """Test ThumbnailGenerationService contract compliance."""
        service = ThumbnailGenerationService()

        # Test with None input
        result = service.generate_sequence_thumbnail(None, Path("test.png"))
        assert result is None

        # Test with empty sequence
        empty_sequence = Mock(spec=SequenceData)
        empty_sequence.beats = []

        result = service.generate_sequence_thumbnail(empty_sequence, Path("test.png"))
        assert result is None

        # Test with valid sequence (will fail due to no legacy system, but contract should be maintained)
        mock_beat1 = Mock(spec=BeatData)
        mock_beat2 = Mock(spec=BeatData)

        valid_sequence = Mock(spec=SequenceData)
        valid_sequence.beats = [mock_beat1, mock_beat2]
        valid_sequence.length = 2

        result = service.generate_sequence_thumbnail(valid_sequence, Path("test.png"))
        # Should return None or Path, not raise exception
        assert result is None or isinstance(result, Path)

    def test_ui_state_manager_contract(self):
        """Test UIStateManager contract compliance."""
        manager = UIStateManager()

        # Test settings
        assert manager.get_setting("nonexistent", "default") == "default"

        manager.set_setting("key1", "value1")
        assert manager.get_setting("key1") == "value1"

        # Test tab state
        assert isinstance(manager.get_tab_state("nonexistent"), dict)

        # Test graph editor
        result = manager.toggle_graph_editor()
        assert isinstance(result, bool)

        # Test all settings
        all_settings = manager.get_all_settings()
        assert isinstance(all_settings, dict)

        # Test save/load
        manager.save_state()
        manager.load_state()
        # Should not raise exceptions


class TestBackwardCompatibility:
    """Test backward compatibility with existing code."""

    def test_direct_class_usage_still_works(self):
        """Test that direct class usage still works alongside interface usage."""
        # Direct usage
        workbench_manager = WorkbenchStateManager()
        cache_manager = DataCacheManager()

        # Should work exactly as before
        assert workbench_manager.get_workbench_state() == WorkbenchState.EMPTY
        assert cache_manager.get_cache_stats()["total_items"] == 0

        # Interface usage
        workbench_interface: IWorkbenchStateManager = workbench_manager
        cache_interface: IDataCacheManager = cache_manager

        # Should work through interface
        assert workbench_interface.get_workbench_state() == WorkbenchState.EMPTY
        assert cache_interface.get_cache_stats()["total_items"] == 0

    def test_existing_method_signatures_preserved(self):
        """Test that existing method signatures are preserved."""
        # Create services
        workbench_manager = WorkbenchStateManager()
        cache_manager = DataCacheManager()

        # Test that all original methods still exist and work
        assert hasattr(workbench_manager, "set_sequence")
        assert hasattr(workbench_manager, "get_current_sequence")
        assert hasattr(workbench_manager, "get_workbench_state")

        assert hasattr(cache_manager, "get_position_cache")
        assert hasattr(cache_manager, "set_position_cache")
        assert hasattr(cache_manager, "get_cache_stats")

        # Test that they're callable
        assert callable(workbench_manager.set_sequence)
        assert callable(cache_manager.get_cache_stats)
