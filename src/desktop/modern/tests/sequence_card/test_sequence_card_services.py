"""
Comprehensive Test Suite for Sequence Card Services

Tests all sequence card services in isolation and integration.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import List

# Import the services and interfaces we're testing
from core.interfaces.sequence_card_services import (
    ISequenceCardDataService,
    ISequenceCardCacheService,
    ISequenceCardLayoutService,
    ISequenceCardDisplayService,
    ISequenceCardExportService,
    ISequenceCardSettingsService,
    SequenceCardData,
    CacheStats,
    GridDimensions,
    DisplayState,
    CacheLevel,
)

from application.services.sequence_card.sequence_data_service import (
    SequenceCardDataService,
)
from application.services.sequence_card.sequence_cache_service import (
    SequenceCardCacheService,
)
from application.services.sequence_card.sequence_layout_service import (
    SequenceCardLayoutService,
)
from application.services.sequence_card.sequence_display_service import (
    SequenceCardDisplayService,
)
from application.services.sequence_card.sequence_export_service import (
    SequenceCardExportService,
)
from application.services.sequence_card.sequence_settings_service import (
    SequenceCardSettingsService,
)


class TestSequenceCardDataService:
    """Test suite for SequenceCardDataService."""

    @pytest.fixture
    def service(self):
        """Create service instance for testing."""
        return SequenceCardDataService()

    @pytest.fixture
    def temp_dict_structure(self):
        """Create temporary dictionary structure for testing."""
        temp_dir = tempfile.mkdtemp()

        # Create word directories with sample images
        test_data = [
            ("hello", [("hello_16_1.png", 16), ("hello_8_1.png", 8)]),
            ("world", [("world_16_1.png", 16), ("world_4_1.png", 4)]),
            ("test", [("test_12_1.png", 12), ("test_2_1.png", 2)]),
        ]

        for word, files in test_data:
            word_dir = Path(temp_dir) / word
            word_dir.mkdir()

            for filename, length in files:
                image_file = word_dir / filename
                # Create fake PNG with minimal structure
                png_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
                image_file.write_bytes(png_data)

        yield Path(temp_dir)

        # Cleanup
        import shutil

        shutil.rmtree(temp_dir)

    def test_get_all_sequences(self, service, temp_dict_structure):
        """Test getting all sequences from dictionary."""
        sequences = service.get_all_sequences(temp_dict_structure)

        # Should find 6 sequences (2 per word × 3 words)
        assert len(sequences) == 6

        # Check sequence data structure
        for seq in sequences:
            assert isinstance(seq, SequenceCardData)
            assert seq.word in ["hello", "world", "test"]
            assert seq.path.exists()
            assert seq.length > 0

    def test_get_sequences_by_length(self, service, temp_dict_structure):
        """Test filtering sequences by length."""
        # Test specific length filtering
        length_16_sequences = service.get_sequences_by_length(temp_dict_structure, 16)
        assert len(length_16_sequences) == 2  # hello and world have length 16

        length_8_sequences = service.get_sequences_by_length(temp_dict_structure, 8)
        assert len(length_8_sequences) == 1  # only hello has length 8

        # Verify all sequences have correct length
        for seq in length_16_sequences:
            assert seq.length == 16
        for seq in length_8_sequences:
            assert seq.length == 8

    def test_get_sequences_by_length_all(self, service, temp_dict_structure):
        """Test getting all sequences (length <= 0)."""
        all_sequences = service.get_sequences_by_length(temp_dict_structure, 0)
        assert len(all_sequences) == 6  # All sequences

        all_sequences_negative = service.get_sequences_by_length(
            temp_dict_structure, -1
        )
        assert len(all_sequences_negative) == 6  # All sequences

    def test_extract_mock_metadata(self, service):
        """Test mock metadata extraction."""
        # Test filename pattern recognition
        test_cases = [
            (Path("hello_16_1.png"), 16),
            (Path("world_8_2.png"), 8),
            (Path("test_4_3.png"), 4),
            (Path("sequence_length_12.png"), 12),
            (Path("unknown_pattern.png"), 16),  # Default
        ]

        for path, expected_length in test_cases:
            metadata = service._extract_mock_metadata(path)
            assert metadata["sequence_length"] == expected_length
            assert metadata["is_favorite"] == False
            assert metadata["tags"] == []

    def test_validate_sequence_data(self, service, temp_dict_structure):
        """Test sequence data validation."""
        # Create valid sequence data
        valid_seq = SequenceCardData(
            path=temp_dict_structure / "hello" / "hello_16_1.png",
            word="hello",
            length=16,
            metadata={},
        )

        is_valid, errors = service.validate_sequence_data(valid_seq)
        assert is_valid
        assert len(errors) == 0

        # Test invalid sequence data - missing file
        invalid_seq = SequenceCardData(
            path=temp_dict_structure / "nonexistent.png",
            word="test",
            length=16,
            metadata={},
        )

        is_valid, errors = service.validate_sequence_data(invalid_seq)
        assert not is_valid
        assert len(errors) > 0
        assert "does not exist" in errors[0]

        # Test invalid sequence data - empty word
        invalid_seq2 = SequenceCardData(
            path=temp_dict_structure / "hello" / "hello_16_1.png",
            word="",
            length=16,
            metadata={},
        )

        is_valid, errors = service.validate_sequence_data(invalid_seq2)
        assert not is_valid
        assert any("Word is required" in error for error in errors)


class TestSequenceCardCacheService:
    """Test suite for SequenceCardCacheService."""

    @pytest.fixture
    def service(self):
        """Create cache service with small limits for testing."""
        return SequenceCardCacheService(max_raw_cache_size=3, max_scaled_cache_size=5)

    @pytest.fixture
    def sample_image_data(self):
        """Create sample image data for testing."""
        return b"\x89PNG\r\n\x1a\n" + b"test_image_data" * 100

    def test_cache_and_retrieve_raw_image(self, service, sample_image_data):
        """Test caching and retrieving raw images."""
        test_path = Path("test_image.png")

        # Initially should be empty
        cached_data = service.get_cached_image(test_path, 1.0)
        assert cached_data is None
        assert service.stats.raw_cache_misses == 1

        # Cache the image
        service.cache_image(test_path, sample_image_data, 1.0)

        # Should now retrieve from cache
        cached_data = service.get_cached_image(test_path, 1.0)
        assert cached_data == sample_image_data
        assert service.stats.raw_cache_hits == 1

    def test_cache_and_retrieve_scaled_image(self, service, sample_image_data):
        """Test caching and retrieving scaled images."""
        test_path = Path("test_image.png")
        scale = 0.5

        # Initially should be empty
        cached_data = service.get_cached_image(test_path, scale)
        assert cached_data is None
        assert service.stats.scaled_cache_misses == 1

        # Cache the scaled image
        service.cache_image(test_path, sample_image_data, scale)

        # Should now retrieve from cache
        cached_data = service.get_cached_image(test_path, scale)
        assert cached_data == sample_image_data
        assert service.stats.scaled_cache_hits == 1

    def test_lru_eviction(self, service, sample_image_data):
        """Test LRU cache eviction policy."""
        # Fill cache beyond capacity (3 raw images)
        paths = [Path(f"image_{i}.png") for i in range(5)]

        # Cache 5 images (should evict 2 oldest)
        for i, path in enumerate(paths):
            service.cache_image(path, sample_image_data + str(i).encode(), 1.0)

        # First two should be evicted
        assert service.get_cached_image(paths[0], 1.0) is None
        assert service.get_cached_image(paths[1], 1.0) is None

        # Last three should still be cached
        assert service.get_cached_image(paths[2], 1.0) is not None
        assert service.get_cached_image(paths[3], 1.0) is not None
        assert service.get_cached_image(paths[4], 1.0) is not None

    def test_clear_cache(self, service, sample_image_data):
        """Test cache clearing functionality."""
        test_path = Path("test_image.png")

        # Cache some data
        service.cache_image(test_path, sample_image_data, 1.0)
        service.cache_image(test_path, sample_image_data, 0.5)

        # Clear all caches
        service.clear_cache()

        # Should be empty
        assert service.get_cached_image(test_path, 1.0) is None
        assert service.get_cached_image(test_path, 0.5) is None

        # Stats should be reset
        assert service.stats.raw_cache_hits == 0
        assert service.stats.scaled_cache_hits == 0

    def test_clear_specific_cache_level(self, service, sample_image_data):
        """Test clearing specific cache levels."""
        test_path = Path("test_image.png")

        # Cache data at both levels
        service.cache_image(test_path, sample_image_data, 1.0)
        service.cache_image(test_path, sample_image_data, 0.5)

        # Clear only raw cache
        service.clear_cache(CacheLevel.RAW_IMAGE)

        assert service.get_cached_image(test_path, 1.0) is None
        assert service.get_cached_image(test_path, 0.5) is not None

        # Clear scaled cache
        service.clear_cache(CacheLevel.SCALED_IMAGE)
        assert service.get_cached_image(test_path, 0.5) is None

    def test_cache_stats(self, service, sample_image_data):
        """Test cache statistics calculation."""
        test_path = Path("test_image.png")

        # Generate some hits and misses
        service.get_cached_image(test_path, 1.0)  # miss
        service.cache_image(test_path, sample_image_data, 1.0)
        service.get_cached_image(test_path, 1.0)  # hit
        service.get_cached_image(test_path, 0.5)  # miss (scaled)

        stats = service.get_cache_stats()
        assert stats.raw_cache_hits == 1
        assert stats.raw_cache_misses == 1
        assert stats.scaled_cache_misses == 1
        assert abs(stats.hit_ratio - 0.333) < 0.01  # 1 hit out of 3 total requests


class TestSequenceCardLayoutService:
    """Test suite for SequenceCardLayoutService."""

    @pytest.fixture
    def service(self):
        return SequenceCardLayoutService()

    def test_grid_dimensions_mapping(self, service):
        """Test grid dimensions mapping for known sequence lengths."""
        # Test all known mappings from legacy system
        expected_mappings = {
            2: (3, 2, 6),  # cols, rows, total
            3: (3, 2, 6),
            4: (10, 2, 20),
            5: (2, 3, 6),
            6: (2, 3, 6),
            8: (5, 2, 10),
            10: (4, 3, 12),
            12: (4, 3, 12),
            16: (3, 2, 6),
        }

        for length, (
            expected_cols,
            expected_rows,
            expected_total,
        ) in expected_mappings.items():
            grid_dims = service.calculate_grid_dimensions(length)
            assert grid_dims.columns == expected_cols
            assert grid_dims.rows == expected_rows
            assert grid_dims.total_positions == expected_total

    def test_unknown_sequence_length(self, service):
        """Test handling of unknown sequence lengths."""
        grid_dims = service.calculate_grid_dimensions(99)

        # Should return default fallback
        assert grid_dims.columns == 4
        assert grid_dims.rows == 4
        assert grid_dims.total_positions == 16

    def test_calculate_page_size(self, service):
        """Test page size calculation."""
        available_width = 1000
        column_count = 3

        page_width, page_height = service.calculate_page_size(
            available_width, column_count
        )

        # Should account for margins and spacing
        expected_width = (1000 - 40 - 20) // 3  # margin=20, spacing=10*(3-1)=20
        expected_height = int(expected_width * 0.7)

        assert page_width == expected_width
        assert page_height == expected_height

        # Test minimum width
        page_width_small, _ = service.calculate_page_size(100, 2)
        assert page_width_small >= 200  # Should enforce minimum

    def test_calculate_scale_factor(self, service):
        """Test scale factor calculation."""
        # Test normal scaling
        scale = service.calculate_scale_factor((200, 150), (100, 75))
        assert scale == 0.5

        # Test aspect ratio preservation (should use smaller scale)
        scale = service.calculate_scale_factor((200, 200), (100, 50))
        assert scale == 0.25  # Limited by height

        # Test edge cases
        scale = service.calculate_scale_factor((0, 100), (50, 50))
        assert scale == 1.0  # Should handle zero width

        scale = service.calculate_scale_factor((100, 100), (1000, 1000))
        assert scale == 5.0  # Should cap at maximum


class TestSequenceCardSettingsService:
    """Test suite for SequenceCardSettingsService."""

    @pytest.fixture
    def mock_settings_service(self):
        """Create mock settings service."""
        mock_service = Mock()
        mock_service.get_setting.return_value = None
        return mock_service

    @pytest.fixture
    def service_with_mock(self, mock_settings_service):
        return SequenceCardSettingsService(mock_settings_service)

    @pytest.fixture
    def service_without_backend(self):
        return SequenceCardSettingsService(None)

    def test_get_last_selected_length_with_backend(
        self, service_with_mock, mock_settings_service
    ):
        """Test getting last selected length with settings backend."""
        # Mock return value
        mock_settings_service.get_setting.return_value = 8

        length = service_with_mock.get_last_selected_length()
        assert length == 8

        # Verify correct call
        mock_settings_service.get_setting.assert_called_with(
            "sequence_card_tab", "last_length", 16
        )

    def test_get_last_selected_length_default(
        self, service_with_mock, mock_settings_service
    ):
        """Test default value when no setting exists."""
        # Mock returns default
        mock_settings_service.get_setting.return_value = 16

        length = service_with_mock.get_last_selected_length()
        assert length == 16

    def test_save_selected_length_with_backend(
        self, service_with_mock, mock_settings_service
    ):
        """Test saving selected length with settings backend."""
        service_with_mock.save_selected_length(12)

        mock_settings_service.set_setting.assert_called_with(
            "sequence_card_tab", "last_length", 12
        )

    def test_internal_storage_fallback(self, service_without_backend):
        """Test internal storage when no backend is available."""
        # Should use internal storage
        service_without_backend.save_selected_length(8)
        length = service_without_backend.get_last_selected_length()
        assert length == 8

        # Test column count too
        service_without_backend.save_column_count(4)
        columns = service_without_backend.get_column_count()
        assert columns == 4


class TestSequenceCardExportService:
    """Test suite for SequenceCardExportService."""

    @pytest.fixture
    def service(self):
        return SequenceCardExportService()

    def test_export_all_sequences_mock(self, service):
        """Test export all sequences with mock implementation."""
        # Mock the worker to avoid threading in tests
        with patch(
            "application.services.sequence_card.sequence_export_service.ExportWorker"
        ) as mock_worker_class:
            mock_worker = Mock()
            mock_worker.isRunning.return_value = False
            mock_worker_class.return_value = mock_worker

            result = service.export_all_sequences()

            assert result == True
            mock_worker.start.assert_called_once()

    def test_export_prevents_concurrent_operations(self, service):
        """Test that export prevents concurrent operations."""
        # Mock a running worker
        mock_worker = Mock()
        mock_worker.isRunning.return_value = True
        service._current_worker = mock_worker

        result = service.export_all_sequences()
        assert result == False

    def test_regenerate_all_images_mock(self, service):
        """Test regenerate all images with mock implementation."""
        with patch(
            "application.services.sequence_card.sequence_export_service.ExportWorker"
        ) as mock_worker_class:
            mock_worker = Mock()
            mock_worker.isRunning.return_value = False
            mock_worker_class.return_value = mock_worker

            result = service.regenerate_all_images()

            assert result == True
            # Should create worker with "regenerate" type
            mock_worker_class.assert_called_with("regenerate")


@pytest.fixture
def sample_sequences():
    """Create sample sequence data for testing."""
    return [
        SequenceCardData(
            path=Path(f"test_{i}.png"),
            word=f"word_{i}",
            length=16,
            metadata={"sequence_length": 16},
        )
        for i in range(10)
    ]


class TestSequenceCardDisplayService:
    """Test suite for SequenceCardDisplayService."""

    @pytest.fixture
    def mock_services(self):
        """Create mock services for testing display service."""
        data_service = Mock(spec=ISequenceCardDataService)
        cache_service = Mock(spec=ISequenceCardCacheService)
        layout_service = Mock(spec=ISequenceCardLayoutService)

        # Setup default returns
        cache_service.get_cache_stats.return_value = CacheStats()

        return data_service, cache_service, layout_service

    @pytest.fixture
    def display_service(self, mock_services):
        """Create display service with mocked dependencies."""
        data_service, cache_service, layout_service = mock_services
        return SequenceCardDisplayService(
            data_service,
            cache_service,
            layout_service,
            dictionary_path=Path("test_dict"),
        )

    def test_display_sequences_calls_data_service(
        self, display_service, mock_services, sample_sequences
    ):
        """Test that display_sequences calls the data service correctly."""
        data_service, cache_service, layout_service = mock_services
        data_service.get_sequences_by_length.return_value = sample_sequences

        display_service.display_sequences(16, 2)

        data_service.get_sequences_by_length.assert_called_with(Path("test_dict"), 16)

    def test_display_state_tracking(self, display_service, mock_services):
        """Test display state tracking."""
        data_service, cache_service, layout_service = mock_services
        data_service.get_sequences_by_length.return_value = []

        # Initial state
        state = display_service.get_display_state()
        assert not state.is_loading
        assert state.current_length == 16

        # Start display operation
        display_service.display_sequences(8, 3)

        # Should update state
        assert display_service.display_state.current_length == 8
        assert display_service.display_state.current_column_count == 3

    def test_cancel_operation(self, display_service):
        """Test cancelling display operation."""
        display_service._cancel_requested = False
        display_service.cancel_current_operation()

        assert display_service._cancel_requested == True
        assert not display_service.display_state.is_loading


# Integration test
class TestSequenceCardServiceIntegration:
    """Integration tests for sequence card services."""

    @pytest.fixture
    def integrated_services(self, temp_dict_structure):
        """Create integrated services for testing."""
        data_service = SequenceCardDataService()
        cache_service = SequenceCardCacheService()
        layout_service = SequenceCardLayoutService()
        settings_service = SequenceCardSettingsService()
        display_service = SequenceCardDisplayService(
            data_service, cache_service, layout_service, temp_dict_structure
        )
        export_service = SequenceCardExportService()

        return {
            "data": data_service,
            "cache": cache_service,
            "layout": layout_service,
            "settings": settings_service,
            "display": display_service,
            "export": export_service,
        }

    @pytest.fixture
    def temp_dict_structure(self):
        """Create temporary dictionary structure for integration testing."""
        temp_dir = tempfile.mkdtemp()

        # Create more comprehensive test data
        test_data = [
            (
                "hello",
                [("hello_16_1.png", 16), ("hello_8_1.png", 8), ("hello_4_1.png", 4)],
            ),
            ("world", [("world_16_1.png", 16), ("world_12_1.png", 12)]),
            ("test", [("test_10_1.png", 10), ("test_2_1.png", 2)]),
        ]

        for word, files in test_data:
            word_dir = Path(temp_dir) / word
            word_dir.mkdir()

            for filename, length in files:
                image_file = word_dir / filename
                # Create fake PNG with minimal structure
                png_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
                image_file.write_bytes(png_data)

        yield Path(temp_dir)

        # Cleanup
        import shutil

        shutil.rmtree(temp_dir)

    def test_data_to_cache_integration(self, integrated_services):
        """Test integration between data service and cache service."""
        data_service = integrated_services["data"]
        cache_service = integrated_services["cache"]

        # Load sequences
        sequences = data_service.get_all_sequences(Path("test_dict"))

        # Simulate caching images for sequences
        for seq in sequences:
            if seq.path.exists():
                with open(seq.path, "rb") as f:
                    image_data = f.read()
                cache_service.cache_image(seq.path, image_data)

        # Verify caching worked
        stats = cache_service.get_cache_stats()
        assert stats.raw_cache_hits == 0  # No hits yet

        # Try to retrieve cached data
        if sequences:
            cached_data = cache_service.get_cached_image(sequences[0].path)
            assert cached_data is not None

    def test_layout_service_with_real_data(self, integrated_services):
        """Test layout service with real sequence data."""
        data_service = integrated_services["data"]
        layout_service = integrated_services["layout"]

        sequences = data_service.get_all_sequences(Path("test_dict"))

        # Test layout calculations for different lengths found in data
        for seq in sequences:
            grid_dims = layout_service.calculate_grid_dimensions(seq.length)
            assert grid_dims.columns > 0
            assert grid_dims.rows > 0
            assert grid_dims.total_positions > 0

    def test_settings_persistence(self, integrated_services):
        """Test settings persistence across service calls."""
        settings_service = integrated_services["settings"]

        # Test length persistence
        settings_service.save_selected_length(8)
        assert settings_service.get_last_selected_length() == 8

        # Test column count persistence
        settings_service.save_column_count(4)
        assert settings_service.get_column_count() == 4


# Add performance markers to existing tests
import pytest

# Add performance markers to sequence card services tests
# Note: Performance tests are marked with @pytest.mark.performance
# and can be run with: pytest -m performance


# Add this section to existing test classes
@pytest.mark.performance
class TestSequenceCardCacheServicePerformance:
    """Performance-specific tests for cache service."""

    @pytest.fixture
    def large_cache_service(self):
        """Create cache service with larger limits for performance testing."""
        return SequenceCardCacheService(
            max_raw_cache_size=1000, max_scaled_cache_size=2000
        )

    @pytest.mark.performance
    def test_cache_performance_under_load(self, large_cache_service):
        """Test cache performance under heavy load."""
        import time

        # Create test data
        test_data = b"x" * 10240  # 10KB per image

        # Measure cache write performance
        start_time = time.time()

        for i in range(500):  # Cache 500 images
            path = Path(f"perf_test_{i}.png")
            large_cache_service.cache_image(path, test_data, 1.0)

        write_time = time.time() - start_time

        # Measure cache read performance
        start_time = time.time()

        hit_count = 0
        for i in range(500):
            path = Path(f"perf_test_{i}.png")
            cached_data = large_cache_service.get_cached_image(path, 1.0)
            if cached_data is not None:
                hit_count += 1

        read_time = time.time() - start_time

        # Performance assertions
        assert write_time < 5.0  # Should cache 500 images in under 5 seconds
        assert read_time < 2.0  # Should read 500 images in under 2 seconds
        assert hit_count >= 400  # Should have at least 80% hit rate (LRU eviction)

        print(f"Cache write performance: {write_time:.2f}s for 500 images")
        print(f"Cache read performance: {read_time:.2f}s for 500 images")
        print(f"Cache hit rate: {hit_count/500*100:.1f}%")


@pytest.mark.performance
class TestSequenceCardDataServicePerformance:
    """Performance-specific tests for data service."""

    @pytest.fixture
    def large_dictionary(self, tmp_path):
        """Create large dictionary for performance testing."""
        dict_path = tmp_path / "large_dict"
        dict_path.mkdir()

        # Create 200 words with multiple sequences each
        for i in range(200):
            word_dir = dict_path / f"word_{i:03d}"
            word_dir.mkdir()

            # Each word has sequences of different lengths
            for length in [2, 4, 8, 16]:
                for variant in range(3):  # 3 variants per length
                    filename = f"word_{i:03d}_length_{length}_variant_{variant}.png"
                    image_file = word_dir / filename
                    # Create realistic PNG data
                    png_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 1000
                    image_file.write_bytes(png_data)

        return dict_path

    @pytest.mark.performance
    def test_large_dictionary_scan_performance(self, large_dictionary):
        """Test performance scanning large dictionary."""
        service = SequenceCardDataService()

        import time

        start_time = time.time()

        # Scan entire dictionary
        all_sequences = service.get_all_sequences(large_dictionary)

        scan_time = time.time() - start_time

        # Should find 200 words × 4 lengths × 3 variants = 2400 sequences
        expected_sequences = 200 * 4 * 3
        assert len(all_sequences) == expected_sequences
        assert scan_time < 10.0  # Should scan 2400 files in under 10 seconds

        print(
            f"Dictionary scan performance: {scan_time:.2f}s for {len(all_sequences)} sequences"
        )
        print(f"Scan rate: {len(all_sequences)/scan_time:.1f} sequences/second")

    @pytest.mark.performance
    def test_filtered_search_performance(self, large_dictionary):
        """Test performance of filtered sequence searches."""
        service = SequenceCardDataService()

        import time

        # Test different length filters
        for length in [2, 4, 8, 16]:
            start_time = time.time()

            filtered_sequences = service.get_sequences_by_length(
                large_dictionary, length
            )

            filter_time = time.time() - start_time

            # Should find 200 words × 3 variants = 600 sequences per length
            expected_count = 200 * 3
            assert len(filtered_sequences) == expected_count
            assert filter_time < 3.0  # Should filter in under 3 seconds

            print(
                f"Length {length} filter performance: {filter_time:.2f}s for {len(filtered_sequences)} sequences"
            )
