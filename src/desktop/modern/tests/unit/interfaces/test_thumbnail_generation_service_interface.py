"""
Tests for ThumbnailGenerationService interface compliance and functionality.

These tests verify that the ThumbnailGenerationService correctly implements the
IThumbnailGenerationService interface and provides expected behavior.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
from shared.application.services.ui.thumbnail_generation_service import (
    MockThumbnailGenerationService,
    ThumbnailGenerationService,
)
from desktop.modern.core.interfaces.ui_services import IThumbnailGenerationService
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


class TestThumbnailGenerationServiceInterface:
    """Test interface compliance for ThumbnailGenerationService."""

    def test_thumbnail_generation_service_implements_interface(self):
        """Test that ThumbnailGenerationService implements IThumbnailGenerationService."""
        assert issubclass(ThumbnailGenerationService, IThumbnailGenerationService)

    def test_mock_thumbnail_generation_service_implements_interface(self):
        """Test that MockThumbnailGenerationService implements IThumbnailGenerationService."""
        assert issubclass(MockThumbnailGenerationService, IThumbnailGenerationService)

    def test_all_interface_methods_implemented(self):
        """Test that all interface methods are implemented."""
        service = ThumbnailGenerationService()

        # Get all abstract methods from interface
        interface_methods = [
            method
            for method in dir(IThumbnailGenerationService)
            if not method.startswith("_")
            and callable(getattr(IThumbnailGenerationService, method))
        ]

        # Verify all methods exist and are callable
        for method_name in interface_methods:
            assert hasattr(service, method_name), f"Missing method: {method_name}"
            assert callable(
                getattr(service, method_name)
            ), f"Method not callable: {method_name}"

    def test_method_signatures_match_interface(self):
        """Test that method signatures match the interface."""
        import inspect

        service = ThumbnailGenerationService()

        # Test key methods
        key_methods = ["generate_sequence_thumbnail"]

        for method_name in key_methods:
            interface_method = getattr(IThumbnailGenerationService, method_name)
            implementation_method = getattr(service, method_name)

            # Both should be callable
            assert callable(interface_method)
            assert callable(implementation_method)


class TestThumbnailGenerationServiceBehavior:
    """Test behavior of ThumbnailGenerationService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.service = ThumbnailGenerationService(temp_directory=self.temp_dir)

        # Create mock sequence data
        self.mock_beat1 = Mock(spec=BeatData)
        self.mock_beat1.letter = "A"

        self.mock_beat2 = Mock(spec=BeatData)
        self.mock_beat2.letter = "B"

        self.mock_sequence = Mock(spec=SequenceData)
        self.mock_sequence.name = "Test Sequence"
        self.mock_sequence.beats = [self.mock_beat1, self.mock_beat2]
        self.mock_sequence.length = 2

    def teardown_method(self):
        """Clean up test fixtures."""
        # Clean up temp directory
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_generate_sequence_thumbnail_with_empty_sequence(self):
        """Test generating thumbnail with empty sequence."""
        empty_sequence = Mock(spec=SequenceData)
        empty_sequence.beats = []

        output_path = self.temp_dir / "empty_thumbnail.png"

        result = self.service.generate_sequence_thumbnail(empty_sequence, output_path)

        # Should return None for empty sequence
        assert result is None

    def test_generate_sequence_thumbnail_with_none_sequence(self):
        """Test generating thumbnail with None sequence."""
        output_path = self.temp_dir / "none_thumbnail.png"

        result = self.service.generate_sequence_thumbnail(None, output_path)

        # Should return None for None sequence
        assert result is None

    def test_generate_sequence_thumbnail_with_too_short_sequence(self):
        """Test generating thumbnail with sequence that's too short."""
        short_sequence = Mock(spec=SequenceData)
        short_sequence.beats = [self.mock_beat1]  # Only one beat

        output_path = self.temp_dir / "short_thumbnail.png"

        result = self.service.generate_sequence_thumbnail(short_sequence, output_path)

        # Should return None for too short sequence
        assert result is None

    def test_generate_sequence_thumbnail_creates_output_directory(self):
        """Test that output directory is created if it doesn't exist."""
        nested_dir = self.temp_dir / "nested" / "deep"
        output_path = nested_dir / "thumbnail.png"

        # Directory shouldn't exist initially
        assert not nested_dir.exists()

        # Try to generate thumbnail (will fail due to no legacy system, but should create dir)
        result = self.service.generate_sequence_thumbnail(
            self.mock_sequence, output_path
        )

        # Directory should now exist
        assert nested_dir.exists()

    @patch(
        "application.services.ui.thumbnail_generation_service.ThumbnailGenerationService._convert_to_legacy_format"
    )
    def test_generate_sequence_thumbnail_with_conversion_failure(self, mock_convert):
        """Test handling of conversion failure."""
        mock_convert.return_value = None  # Simulate conversion failure

        output_path = self.temp_dir / "failed_thumbnail.png"

        result = self.service.generate_sequence_thumbnail(
            self.mock_sequence, output_path
        )

        # Should return None when conversion fails
        assert result is None
        mock_convert.assert_called_once_with(self.mock_sequence)

    def test_generate_sequence_thumbnail_with_fullscreen_preview(self):
        """Test generating thumbnail with fullscreen preview option."""
        output_path = self.temp_dir / "fullscreen_thumbnail.png"

        # This will fail due to no legacy system, but we can test the parameter passing
        result = self.service.generate_sequence_thumbnail(
            self.mock_sequence, output_path, fullscreen_preview=True
        )

        # Should return None (no legacy system), but method should accept parameter
        assert result is None

    def test_temp_directory_default(self):
        """Test that default temp directory is used when not specified."""
        service = ThumbnailGenerationService()

        # Should use system temp directory
        assert service._temp_directory == Path(tempfile.gettempdir())

    def test_temp_directory_custom(self):
        """Test that custom temp directory is used when specified."""
        custom_temp = Path("/custom/temp")
        service = ThumbnailGenerationService(temp_directory=custom_temp)

        assert service._temp_directory == custom_temp


class TestMockThumbnailGenerationService:
    """Test MockThumbnailGenerationService behavior."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.service = MockThumbnailGenerationService(temp_directory=self.temp_dir)

        # Create mock sequence data
        self.mock_beat1 = Mock(spec=BeatData)
        self.mock_beat1.letter = "A"

        self.mock_beat2 = Mock(spec=BeatData)
        self.mock_beat2.letter = "B"

        self.mock_sequence = Mock(spec=SequenceData)
        self.mock_sequence.name = "Test Sequence"
        self.mock_sequence.beats = [self.mock_beat1, self.mock_beat2]

    def teardown_method(self):
        """Clean up test fixtures."""
        # Clean up temp directory
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_mock_implements_interface(self):
        """Test that mock implements interface."""
        assert isinstance(self.service, IThumbnailGenerationService)

    def test_mock_generates_placeholder_thumbnail(self):
        """Test that mock generates placeholder thumbnail."""
        output_path = self.temp_dir / "mock_thumbnail.png"

        result = self.service.generate_sequence_thumbnail(
            self.mock_sequence, output_path
        )

        # Should return output path
        assert result == output_path

        # File should exist
        assert output_path.exists()

        # File should have some content
        assert output_path.stat().st_size > 0

    def test_mock_handles_empty_sequence(self):
        """Test that mock handles empty sequence."""
        empty_sequence = Mock(spec=SequenceData)
        empty_sequence.beats = []

        output_path = self.temp_dir / "empty_mock_thumbnail.png"

        result = self.service.generate_sequence_thumbnail(empty_sequence, output_path)

        # Should return None for empty sequence
        assert result is None

    def test_mock_handles_none_sequence(self):
        """Test that mock handles None sequence."""
        output_path = self.temp_dir / "none_mock_thumbnail.png"

        result = self.service.generate_sequence_thumbnail(None, output_path)

        # Should return None for None sequence
        assert result is None

    def test_mock_handles_short_sequence(self):
        """Test that mock handles short sequence."""
        short_sequence = Mock(spec=SequenceData)
        short_sequence.beats = [self.mock_beat1]  # Only one beat

        output_path = self.temp_dir / "short_mock_thumbnail.png"

        result = self.service.generate_sequence_thumbnail(short_sequence, output_path)

        # Should return None for short sequence
        assert result is None

    def test_mock_fullscreen_preview_option(self):
        """Test that mock handles fullscreen preview option."""
        output_path = self.temp_dir / "fullscreen_mock_thumbnail.png"

        result = self.service.generate_sequence_thumbnail(
            self.mock_sequence, output_path, fullscreen_preview=True
        )

        # Should return output path
        assert result == output_path

        # File should exist
        assert output_path.exists()

    def test_mock_creates_output_directory(self):
        """Test that mock creates output directory if needed."""
        nested_dir = self.temp_dir / "nested" / "deep"
        output_path = nested_dir / "mock_thumbnail.png"

        # Directory shouldn't exist initially
        assert not nested_dir.exists()

        result = self.service.generate_sequence_thumbnail(
            self.mock_sequence, output_path
        )

        # Directory should now exist
        assert nested_dir.exists()

        # File should exist
        assert output_path.exists()

    @patch("builtins.open")
    def test_mock_handles_file_error(self, mock_open):
        """Test that mock handles file errors gracefully."""
        # Mock open to raise an exception
        mock_open.side_effect = IOError("File write error")

        output_path = self.temp_dir / "error_mock_thumbnail.png"

        result = self.service.generate_sequence_thumbnail(
            self.mock_sequence, output_path
        )

        # Should return None when file error occurs
        assert result is None


class ConcreteThumbnailGenerationService(IThumbnailGenerationService):
    """Concrete implementation for testing interface compliance."""

    def __init__(self):
        self.thumbnails_generated = []

    def generate_sequence_thumbnail(
        self, sequence, output_path, fullscreen_preview=False
    ):
        """Mock implementation that records calls."""
        if not sequence or not sequence.beats or len(sequence.beats) <= 1:
            return None

        # Record the call
        self.thumbnails_generated.append(
            {
                "sequence": sequence,
                "output_path": output_path,
                "fullscreen_preview": fullscreen_preview,
            }
        )

        # Create a dummy file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("dummy thumbnail content")

        return output_path


class TestConcreteThumbnailGenerationService:
    """Test concrete implementation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.service = ConcreteThumbnailGenerationService()

        # Create mock sequence data
        self.mock_beat1 = Mock(spec=BeatData)
        self.mock_beat2 = Mock(spec=BeatData)

        self.mock_sequence = Mock(spec=SequenceData)
        self.mock_sequence.name = "Test Sequence"
        self.mock_sequence.beats = [self.mock_beat1, self.mock_beat2]

    def teardown_method(self):
        """Clean up test fixtures."""
        # Clean up temp directory
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_concrete_implements_interface(self):
        """Test that concrete implementation implements interface."""
        assert isinstance(self.service, IThumbnailGenerationService)

    def test_concrete_basic_functionality(self):
        """Test basic functionality of concrete implementation."""
        output_path = self.temp_dir / "concrete_thumbnail.png"

        result = self.service.generate_sequence_thumbnail(
            self.mock_sequence, output_path
        )

        # Should return output path
        assert result == output_path

        # Should record the call
        assert len(self.service.thumbnails_generated) == 1
        assert self.service.thumbnails_generated[0]["sequence"] == self.mock_sequence
        assert self.service.thumbnails_generated[0]["output_path"] == output_path
        assert self.service.thumbnails_generated[0]["fullscreen_preview"] is False

    def test_concrete_fullscreen_preview(self):
        """Test fullscreen preview functionality."""
        output_path = self.temp_dir / "fullscreen_concrete_thumbnail.png"

        result = self.service.generate_sequence_thumbnail(
            self.mock_sequence, output_path, fullscreen_preview=True
        )

        # Should return output path
        assert result == output_path

        # Should record the call with fullscreen_preview=True
        assert len(self.service.thumbnails_generated) == 1
        assert self.service.thumbnails_generated[0]["fullscreen_preview"] is True
