"""
Test Application Factory implementation.

Verifies that all application modes work correctly.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(src_path))

from core.application.application_factory import ApplicationFactory, ApplicationMode
from core.interfaces.core_services import (
    ISequenceDataService,
    ILayoutService,
    ISettingsService
)


class TestApplicationFactory:
    """Test the Application Factory functionality."""

    def test_create_test_app(self):
        """Test creating test application."""
        container = ApplicationFactory.create_test_app()

        # Verify container is created
        assert container is not None

        # Verify we can resolve test services
        sequence_service = container.resolve(ISequenceDataService)
        assert sequence_service is not None

        layout_service = container.resolve(ILayoutService)
        assert layout_service is not None

        settings_service = container.resolve(ISettingsService)
        assert settings_service is not None

    def test_create_headless_app(self):
        """Test creating headless application."""
        container = ApplicationFactory.create_headless_app()

        # Verify container is created
        assert container is not None

        # Verify we can resolve services
        layout_service = container.resolve(ILayoutService)
        assert layout_service is not None

    def test_create_app_with_mode(self):
        """Test creating app with specific mode."""
        test_container = ApplicationFactory.create_app(ApplicationMode.TEST)
        assert test_container is not None

        headless_container = ApplicationFactory.create_app(ApplicationMode.HEADLESS)
        assert headless_container is not None

    def test_create_app_from_args(self):
        """Test creating app from command line arguments."""
        # Test with test mode
        test_container = ApplicationFactory.create_app_from_args(["script.py", "--test"])
        assert test_container is not None

        # Test with headless mode
        headless_container = ApplicationFactory.create_app_from_args(["script.py", "--headless"])
        assert headless_container is not None

        # Test with no args (production mode)
        prod_container = ApplicationFactory.create_app_from_args(["script.py"])
        assert prod_container is not None


class TestMockServices:
    """Test that mock services work correctly."""

    def test_sequence_data_service(self):
        """Test in-memory sequence data service."""
        container = ApplicationFactory.create_test_app()
        service = container.resolve(ISequenceDataService)

        # Test creating a sequence
        sequence = service.create_new_sequence("Test Sequence")
        assert sequence['name'] == "Test Sequence"
        assert sequence['id'] is not None

        # Test saving and retrieving
        assert service.save_sequence(sequence) is True
        retrieved = service.get_sequence_by_id(sequence['id'])
        assert retrieved == sequence

        # Test getting all sequences
        all_sequences = service.get_all_sequences()
        assert len(all_sequences) == 1
        assert all_sequences[0] == sequence

    def test_layout_service(self):
        """Test mock layout service."""
        container = ApplicationFactory.create_test_app()
        service = container.resolve(ILayoutService)

        # Test basic layout methods
        window_size = service.get_main_window_size()
        assert window_size.width > 0
        assert window_size.height > 0

        workbench_size = service.get_workbench_size()
        assert workbench_size.width > 0
        assert workbench_size.height > 0

        # Test component size calculation
        component_size = service.calculate_component_size("beat_frame", window_size)
        assert component_size.width > 0
        assert component_size.height > 0

    def test_settings_service(self):
        """Test in-memory settings service."""
        container = ApplicationFactory.create_test_app()
        service = container.resolve(ISettingsService)

        # Test setting and getting values
        service.set_setting("test_key", "test_value")
        assert service.get_setting("test_key") == "test_value"

        # Test default values
        assert service.get_setting("nonexistent_key", "default") == "default"

        # Test save/load (should not crash)
        service.save_settings()
        service.load_settings()


if __name__ == "__main__":
    pytest.main([__file__])
