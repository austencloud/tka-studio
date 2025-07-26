"""
Integration Tests for Sequence Card Tab

Tests the complete integration of services, UI components, and DI container.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Qt testing
pytest_plugins = ["pytest-qt"]
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt, QTimer

# DI Container and registration
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.sequence_card_service_registration import (
    register_sequence_card_services,
    validate_sequence_card_service_registration,
)

# Interfaces
from desktop.modern.core.interfaces.sequence_card_services import (
    ISequenceCardDataService,
    ISequenceCardCacheService,
    ISequenceCardLayoutService,
    ISequenceCardDisplayService,
    ISequenceCardExportService,
    ISequenceCardSettingsService,
)

# Tab implementation
from desktop.modern.presentation.tabs.sequence_card import SequenceCardTab


class TestSequenceCardServiceRegistration:
    """Test suite for service registration and DI container integration."""

    @pytest.fixture
    def container(self):
        """Create DI container for testing."""
        return DIContainer()

    def test_service_registration(self, container):
        """Test that all services can be registered."""
        # Should not raise any exceptions
        register_sequence_card_services(container)

        # Verify all interfaces are registered
        registrations = container.get_registrations()

        expected_interfaces = [
            ISequenceCardDataService,
            ISequenceCardCacheService,
            ISequenceCardLayoutService,
            ISequenceCardDisplayService,
            ISequenceCardExportService,
            ISequenceCardSettingsService,
        ]

        for interface in expected_interfaces:
            assert interface in registrations, f"{interface.__name__} not registered"

    def test_service_resolution(self, container):
        """Test that all services can be resolved."""
        register_sequence_card_services(container)

        # Test resolving each service
        data_service = container.resolve(ISequenceCardDataService)
        assert data_service is not None
        assert isinstance(data_service, ISequenceCardDataService)

        cache_service = container.resolve(ISequenceCardCacheService)
        assert cache_service is not None
        assert isinstance(cache_service, ISequenceCardCacheService)

        layout_service = container.resolve(ISequenceCardLayoutService)
        assert layout_service is not None
        assert isinstance(layout_service, ISequenceCardLayoutService)

        display_service = container.resolve(ISequenceCardDisplayService)
        assert display_service is not None
        assert isinstance(display_service, ISequenceCardDisplayService)

        export_service = container.resolve(ISequenceCardExportService)
        assert export_service is not None
        assert isinstance(export_service, ISequenceCardExportService)

        settings_service = container.resolve(ISequenceCardSettingsService)
        assert settings_service is not None
        assert isinstance(settings_service, ISequenceCardSettingsService)

    def test_singleton_behavior(self, container):
        """Test that singleton services return the same instance."""
        register_sequence_card_services(container)

        # Resolve same service twice
        data_service1 = container.resolve(ISequenceCardDataService)
        data_service2 = container.resolve(ISequenceCardDataService)

        # Should be the same instance (singleton)
        assert data_service1 is data_service2

    def test_service_dependencies(self, container):
        """Test that services with dependencies can be resolved."""
        register_sequence_card_services(container)

        # Display service depends on other services
        display_service = container.resolve(ISequenceCardDisplayService)

        # Should be able to resolve without issues
        assert display_service is not None

        # Test that it has the expected dependencies injected
        assert hasattr(display_service, "data_service")
        assert hasattr(display_service, "cache_service")
        assert hasattr(display_service, "layout_service")

    def test_validation_function(self, container):
        """Test service registration validation."""
        register_sequence_card_services(container)

        # Validation should pass with modern services
        is_valid = validate_sequence_card_service_registration(container)
        assert is_valid is True


class TestSequenceCardTabIntegration:
    """Integration tests for the complete sequence card tab."""

    @pytest.fixture
    def temp_dictionary(self):
        """Create temporary dictionary structure for testing."""
        temp_dir = tempfile.mkdtemp()

        # Create realistic test data structure
        test_data = [
            (
                "apple",
                [
                    ("apple_length_16.png", 16),
                    ("apple_length_8.png", 8),
                    ("apple_sequence_4.png", 4),
                ],
            ),
            ("banana", [("banana_16_beat.png", 16), ("banana_12_sequence.png", 12)]),
            ("cherry", [("cherry_length_10.png", 10), ("cherry_2.png", 2)]),
        ]

        for word, files in test_data:
            word_dir = Path(temp_dir) / word
            word_dir.mkdir()

            for filename, length in files:
                image_file = word_dir / filename
                # Create realistic fake PNG
                png_header = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00d\x08\x02\x00\x00\x00"
                png_data = png_header + b"\x00" * 1000  # Padding
                image_file.write_bytes(png_data)

        yield Path(temp_dir)

        # Cleanup
        import shutil

        shutil.rmtree(temp_dir)

    @pytest.fixture
    def container_with_services(self, temp_dictionary):
        """Create container with all sequence card services registered."""
        container = DIContainer()
        register_sequence_card_services(container)

        # Override dictionary path for testing
        data_service = container.resolve(ISequenceCardDataService)
        # Monkey patch the dictionary path for testing
        original_method = data_service.get_all_sequences
        data_service.get_all_sequences = lambda base_path=None: original_method(
            temp_dictionary
        )

        return container

    @pytest.fixture
    def integrated_tab(self, qtbot, container_with_services):
        """Create fully integrated sequence card tab."""
        container = container_with_services

        tab = container.resolve(SequenceCardTab)
        qtbot.addWidget(tab)

        return tab

    def test_tab_creation_with_di(self, integrated_tab):
        """Test tab creation through DI container."""
        assert integrated_tab is not None
        assert integrated_tab.header is not None
        assert integrated_tab.navigation is not None
        assert integrated_tab.content is not None

    def test_end_to_end_sequence_loading(self, qtbot, integrated_tab):
        """Test end-to-end sequence loading workflow."""
        # Show tab (triggers initialization)
        integrated_tab.show()
        qtbot.waitExposed(integrated_tab)

        # Wait for initialization
        QApplication.processEvents()

        # Should be initialized
        assert integrated_tab.initialized

        # Test selecting different lengths
        navigation = integrated_tab.navigation

        # Click length 16 button
        if 16 in navigation.length_buttons:
            length_16_button = navigation.length_buttons[16]
            qtbot.mouseClick(length_16_button, Qt.MouseButton.LeftButton)

            # Wait for processing
            QApplication.processEvents()

            # Should have updated display
            assert navigation.selected_length == 16

    def test_cache_integration(self, integrated_tab):
        """Test cache integration in full workflow."""
        cache_service = integrated_tab.cache_service

        # Initially cache should be empty
        stats = cache_service.get_cache_stats()
        initial_cache_size = stats.cache_size

        # Simulate loading sequences (would populate cache)
        integrated_tab._initialize_content(16, 2)

        # Process events to allow async operations
        QApplication.processEvents()

        # Cache stats should be available (even if cache is empty due to mock data)
        stats = cache_service.get_cache_stats()
        assert stats is not None
        assert hasattr(stats, "hit_ratio")

    def test_settings_persistence_integration(self, integrated_tab):
        """Test settings persistence integration."""
        settings_service = integrated_tab.settings_service

        # Change settings through UI
        integrated_tab._on_length_selected(8)
        integrated_tab._on_column_count_changed(4)

        # Settings should be persisted
        assert settings_service.get_last_selected_length() == 8
        assert settings_service.get_column_count() == 4

    def test_export_integration(self, qtbot, integrated_tab):
        """Test export integration."""
        export_service = integrated_tab.export_service

        # Mock the export to avoid actual file operations
        with patch.object(
            export_service, "export_all_sequences", return_value=True
        ) as mock_export:
            # Trigger export through UI
            header = integrated_tab.header
            qtbot.mouseClick(header.export_button, Qt.MouseButton.LeftButton)

            # Should have called export service
            mock_export.assert_called_once()

    def test_error_handling_integration(self, integrated_tab):
        """Test error handling in integrated environment."""
        # Simulate error in data service
        data_service = integrated_tab.data_service

        # Mock method to raise exception
        original_method = data_service.get_sequences_by_length
        data_service.get_sequences_by_length = Mock(side_effect=Exception("Test error"))

        # Should handle error gracefully
        try:
            integrated_tab._on_length_selected(16)
            # Should not raise exception - error should be handled
        except Exception as e:
            pytest.fail(f"Error not handled gracefully: {e}")
        finally:
            # Restore original method
            data_service.get_sequences_by_length = original_method

    def test_memory_management_integration(self, integrated_tab):
        """Test memory management in integrated environment."""
        cache_service = integrated_tab.cache_service

        # Test that memory optimization works
        cache_service.optimize_memory_usage()

        # Should not raise exceptions
        stats = cache_service.get_cache_stats()
        assert stats is not None

    def test_resize_handling_integration(self, qtbot, integrated_tab):
        """Test resize handling in integrated environment."""
        # Initialize tab
        integrated_tab.show()
        qtbot.waitExposed(integrated_tab)
        integrated_tab.initialized = True

        # Trigger resize
        integrated_tab.resize(800, 600)
        QApplication.processEvents()

        # Should handle resize without errors
        assert integrated_tab.width() == 800
        assert integrated_tab.height() == 600

    def test_cleanup_integration(self, integrated_tab):
        """Test cleanup in integrated environment."""
        # Initialize some state
        integrated_tab.initialized = True

        # Test cleanup
        integrated_tab.cleanup()

        # Should complete without errors
        # (Specific cleanup verification would depend on implementation details)


class TestSequenceCardRealWorldScenarios:
    """Test real-world usage scenarios."""

    @pytest.fixture
    def realistic_container(self, tmp_path):
        """Create container with realistic configuration."""
        container = DIContainer()

        # Create a test dictionary path to avoid legacy import issues
        test_dict_path = tmp_path / "test_dictionary"
        test_dict_path.mkdir()

        # Create some test sequence files
        for word in ["test", "example"]:
            word_dir = test_dict_path / word
            word_dir.mkdir()
            for length in [2, 4, 8, 16]:
                (word_dir / f"{word}_{length}.png").write_bytes(
                    b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
                )

        # Register services with explicit dictionary path
        register_sequence_card_services(container)

        # Override display service with explicit path to avoid legacy imports
        from shared.application.services.sequence_card.sequence_display_service import (
            SequenceCardDisplayService,
        )
        from desktop.modern.core.interfaces.sequence_card_services import (
            ISequenceCardDataService,
            ISequenceCardCacheService,
            ISequenceCardLayoutService,
        )

        container.register_singleton(
            ISequenceCardDisplayService,
            lambda c: SequenceCardDisplayService(
                data_service=c.resolve(ISequenceCardDataService),
                cache_service=c.resolve(ISequenceCardCacheService),
                layout_service=c.resolve(ISequenceCardLayoutService),
                dictionary_path=test_dict_path,
            ),
        )

        return container

    def test_multiple_tab_instances(self, realistic_container):
        """Test that multiple tab instances can coexist."""
        # Create multiple tabs
        tab1 = realistic_container.resolve(SequenceCardTab)
        tab2 = realistic_container.resolve(SequenceCardTab)

        # Should be different instances
        assert tab1 is not tab2

        # But should share singleton services
        assert tab1.data_service is tab2.data_service  # Singleton
        assert tab1.cache_service is tab2.cache_service  # Singleton

    def test_service_lifecycle_management(self, realistic_container):
        """Test service lifecycle management."""
        # Resolve services
        data_service = realistic_container.resolve(ISequenceCardDataService)
        cache_service = realistic_container.resolve(ISequenceCardCacheService)

        # Services should be properly initialized
        assert data_service is not None
        assert cache_service is not None

        # Test cleanup (if implemented)
        if hasattr(cache_service, "clear_cache"):
            cache_service.clear_cache()

        # Should handle cleanup without errors

    @patch("utils.path_helpers.get_dictionary_path")
    def test_with_real_dictionary_path(
        self, mock_get_path, realistic_container, tmp_path
    ):
        """Test with realistic dictionary path configuration."""
        # Setup mock dictionary path
        mock_dict_path = tmp_path / "dictionary"
        mock_dict_path.mkdir()
        mock_get_path.return_value = str(mock_dict_path)

        # Create some test dictionary content
        for word in ["test1", "test2"]:
            word_dir = mock_dict_path / word
            word_dir.mkdir()
            (word_dir / f"{word}_16.png").write_bytes(
                b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
            )

        # Test data service with real path
        data_service = realistic_container.resolve(ISequenceCardDataService)
        sequences = data_service.get_all_sequences(mock_dict_path)

        # Should find sequences
        assert len(sequences) >= 2

        # Should have realistic data
        for seq in sequences:
            assert seq.word in ["test1", "test2"]
            assert seq.path.exists()


class TestSequenceCardPerformanceIntegration:
    """Performance tests in integrated environment."""

    @pytest.fixture
    def performance_container(self):
        """Create container configured for performance testing."""
        container = DIContainer()
        register_sequence_card_services(container)
        return container

    def test_service_resolution_performance(self, performance_container):
        """Test service resolution performance."""
        import time

        # Measure time to resolve all services
        start_time = time.time()

        for _ in range(100):  # Resolve 100 times
            data_service = performance_container.resolve(ISequenceCardDataService)
            cache_service = performance_container.resolve(ISequenceCardCacheService)
            layout_service = performance_container.resolve(ISequenceCardLayoutService)

        end_time = time.time()
        resolution_time = end_time - start_time

        # Should resolve quickly (adjust threshold as needed)
        assert resolution_time < 1.0  # Less than 1 second for 300 resolutions

    def test_large_data_set_performance(self, performance_container, tmp_path):
        """Test performance with large data sets."""
        # Create large test dictionary
        dict_path = tmp_path / "large_dict"
        dict_path.mkdir()

        # Create many words with sequences
        for i in range(100):  # 100 words
            word_dir = dict_path / f"word_{i:03d}"
            word_dir.mkdir()

            # Each word has multiple sequences
            for length in [4, 8, 16]:
                image_file = word_dir / f"word_{i:03d}_length_{length}.png"
                image_file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

        # Test data loading performance
        data_service = performance_container.resolve(ISequenceCardDataService)

        import time

        start_time = time.time()

        sequences = data_service.get_all_sequences(dict_path)

        end_time = time.time()
        loading_time = end_time - start_time

        # Should load within reasonable time
        assert loading_time < 5.0  # Less than 5 seconds for 300 sequences
        assert len(sequences) == 300  # 100 words × 3 sequences each
