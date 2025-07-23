"""
Pytest Configuration for Sequence Card Tests

Provides common fixtures and configuration for all sequence card tests.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock
import sys

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent.parent / "src"
sys.path.insert(0, str(src_dir))

# Qt Application fixture
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication for testing."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # Don't quit the app as it may be needed by other tests


@pytest.fixture
def temp_dictionary_structure():
    """
    Create temporary dictionary structure for testing.

    Creates a realistic dictionary structure with:
    - Multiple words (hello, world, test, example)
    - Multiple sequence lengths per word
    - Proper PNG file structure
    """
    temp_dir = tempfile.mkdtemp()

    # Comprehensive test data
    test_data = [
        (
            "hello",
            [
                ("hello_length_16_001.png", 16),
                ("hello_length_8_001.png", 8),
                ("hello_length_4_001.png", 4),
                ("hello_sequence_2.png", 2),
            ],
        ),
        (
            "world",
            [
                ("world_16_beat_001.png", 16),
                ("world_12_sequence_001.png", 12),
                ("world_6_001.png", 6),
            ],
        ),
        (
            "test",
            [
                ("test_length_10_001.png", 10),
                ("test_5_beat.png", 5),
                ("test_3_sequence.png", 3),
            ],
        ),
        ("example", [("example_16_001.png", 16), ("example_8_001.png", 8)]),
    ]

    for word, files in test_data:
        word_dir = Path(temp_dir) / word
        word_dir.mkdir()

        for filename, length in files:
            image_file = word_dir / filename
            # Create realistic PNG structure
            png_header = (
                b"\x89PNG\r\n\x1a\n"  # PNG signature
                b"\x00\x00\x00\rIHDR"  # IHDR chunk
                b"\x00\x00\x00d"  # Width: 100px
                b"\x00\x00\x00d"  # Height: 100px
                b"\x08\x02\x00\x00\x00"  # Bit depth, color type, etc.
            )

            # Add some metadata that might indicate sequence length
            metadata = f"sequence_length:{length}".encode()
            png_data = png_header + b"\x00" * 500 + metadata + b"\x00" * 500

            image_file.write_bytes(png_data)

    yield Path(temp_dir)

    # Cleanup
    import shutil

    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_metadata_extractor():
    """Create mock metadata extractor for testing."""
    extractor = Mock()

    def extract_metadata(path):
        """Extract metadata based on filename patterns."""
        filename = Path(path).stem

        # Extract length from filename patterns
        for length in [2, 3, 4, 5, 6, 8, 10, 12, 16]:
            if f"_{length}_" in filename or f"length_{length}" in filename:
                return {
                    "sequence_length": length,
                    "is_favorite": False,
                    "tags": [],
                    "sequence": f"test_sequence_{length}",
                    "word": filename.split("_")[0],
                }

        # Default metadata
        return {
            "sequence_length": 16,
            "is_favorite": False,
            "tags": [],
            "sequence": "unknown_sequence",
            "word": "unknown",
        }

    extractor.extract_metadata_from_image.side_effect = extract_metadata
    return extractor


@pytest.fixture
def mock_settings_backend():
    """Create mock settings backend for testing."""
    backend = Mock()
    storage = {}  # In-memory storage for testing

    def get_setting(section, key, default=None):
        return storage.get(f"{section}.{key}", default)

    def set_setting(section, key, value):
        storage[f"{section}.{key}"] = value

    backend.get_setting.side_effect = get_setting
    backend.set_setting.side_effect = set_setting

    return backend


@pytest.fixture
def sample_sequence_data():
    """Create sample sequence data for testing."""
    from core.interfaces.sequence_card_services import SequenceCardData

    return [
        SequenceCardData(
            path=Path(f"test_{i}.png"),
            word=f"word_{i}",
            length=16 if i % 2 == 0 else 8,
            metadata={
                "sequence_length": 16 if i % 2 == 0 else 8,
                "is_favorite": i < 3,
                "tags": [f"tag_{i}"] if i % 3 == 0 else [],
            },
        )
        for i in range(10)
    ]


@pytest.fixture
def mock_di_container():
    """Create mock DI container for testing."""
    from core.dependency_injection.di_container import DIContainer

    return DIContainer()


# Performance testing fixtures
@pytest.fixture
def performance_timer():
    """Timer fixture for performance testing."""
    import time

    class PerformanceTimer:
        def __init__(self):
            self.start_time = None
            self.end_time = None

        def start(self):
            self.start_time = time.time()

        def stop(self):
            self.end_time = time.time()

        @property
        def elapsed(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return 0

    return PerformanceTimer()


# Memory testing fixtures
@pytest.fixture
def memory_monitor():
    """Memory monitoring fixture."""
    try:
        import psutil

        class MemoryMonitor:
            def __init__(self):
                self.process = psutil.Process()
                self.initial_memory = None

            def start(self):
                self.initial_memory = self.process.memory_info().rss

            def current_usage_mb(self):
                return self.process.memory_info().rss / 1024 / 1024

            def memory_increase_mb(self):
                if self.initial_memory:
                    current = self.process.memory_info().rss
                    return (current - self.initial_memory) / 1024 / 1024
                return 0

        return MemoryMonitor()
    except ImportError:
        # Fallback if psutil not available
        class MockMemoryMonitor:
            def start(self):
                pass

            def current_usage_mb(self):
                return 100

            def memory_increase_mb(self):
                return 0

        return MockMemoryMonitor()


# Test data generators
@pytest.fixture
def large_sequence_dataset():
    """Generate large sequence dataset for performance testing."""
    from core.interfaces.sequence_card_services import SequenceCardData

    def generate_sequences(count=1000):
        sequences = []
        for i in range(count):
            word = f"word_{i:04d}"
            length = [2, 3, 4, 5, 6, 8, 10, 12, 16][i % 9]

            sequence = SequenceCardData(
                path=Path(f"test_{word}_{length}.png"),
                word=word,
                length=length,
                metadata={
                    "sequence_length": length,
                    "is_favorite": i % 10 == 0,
                    "tags": [f"tag_{i % 5}"] if i % 3 == 0 else [],
                },
            )
            sequences.append(sequence)

        return sequences

    return generate_sequences


# Qt testing helpers
@pytest.fixture
def qt_signal_waiter():
    """Helper for waiting on Qt signals in tests."""
    from PyQt6.QtCore import QTimer
    from PyQt6.QtTest import QTest, QSignalSpy

    class SignalWaiter:
        @staticmethod
        def wait_for_signal(signal, timeout=1000):
            """Wait for a signal to be emitted."""
            spy = QSignalSpy(signal)

            # Wait for signal or timeout
            start_time = QTimer()
            start_time.start()

            while len(spy) == 0 and start_time.elapsed() < timeout:
                QApplication.processEvents()
                QTest.qWait(10)

            return len(spy) > 0

    return SignalWaiter()


# Test markers for categorization
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "ui: mark test as a UI test (requires Qt)")
    config.addinivalue_line("markers", "performance: mark test as a performance test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "visual: mark test as visual regression test")


# Test collection customization
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add automatic markers."""
    for item in items:
        # Auto-mark tests based on path
        if "test_sequence_card_services.py" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "test_sequence_card_ui.py" in str(item.fspath):
            item.add_marker(pytest.mark.ui)
        elif "test_sequence_card_integration.py" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

        # Mark slow tests
        if "performance" in item.name.lower() or "large_data" in item.name.lower():
            item.add_marker(pytest.mark.slow)

        # Mark visual tests
        if "visual" in item.name.lower():
            item.add_marker(pytest.mark.visual)


# Cleanup fixture
@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Automatically cleanup after each test."""
    yield

    # Process any pending Qt events
    try:
        from PyQt6.QtWidgets import QApplication

        app = QApplication.instance()
        if app:
            app.processEvents()
    except ImportError:
        pass

    # Force garbage collection
    import gc

    gc.collect()
