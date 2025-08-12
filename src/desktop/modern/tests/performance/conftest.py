"""
Performance Test Configuration

Pytest configuration and fixtures for performance testing.
Provides test setup, teardown, and common utilities for performance tests.
"""

import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator
from unittest.mock import Mock, patch

import pytest
from core.performance.config import PerformanceConfig, reset_performance_config
from core.performance.memory_tracker import reset_memory_tracker
from core.performance.profiler import reset_profiler
from core.performance.qt_profiler import reset_qt_profiler
from infrastructure.performance.storage import reset_performance_storage


@pytest.fixture(scope="function")
def performance_config() -> Generator[PerformanceConfig, None, None]:
    """Provide a test performance configuration."""
    # Create test configuration
    config = PerformanceConfig.create_default()

    # Override with test-specific settings
    config.profiling.enabled = True
    config.profiling.overhead_threshold_percent = 5.0  # More lenient for tests
    config.monitoring.enabled = True
    config.monitoring.interval_ms = 100  # Faster updates for tests
    config.storage.retention_days = 1  # Short retention for tests

    yield config

    # Cleanup
    reset_performance_config()


@pytest.fixture(scope="function")
def temp_performance_storage() -> Generator[Path, None, None]:
    """Provide temporary storage for performance data."""
    temp_dir = Path(tempfile.mkdtemp(prefix="tka_perf_test_"))

    try:
        yield temp_dir
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="function")
def isolated_profiler(performance_config, temp_performance_storage):
    """Provide an isolated profiler instance for testing."""
    # Update config to use temp storage (create new config with updated storage)
    from core.performance.config import PerformanceConfig
    from core.performance.profiler import AdvancedProfiler

    updated_storage = performance_config.storage.with_database_path(
        str(temp_performance_storage / "test_performance.db")
    )
    performance_config = PerformanceConfig(
        profiling=performance_config.profiling,
        monitoring=performance_config.monitoring,
        regression=performance_config.regression,
        storage=updated_storage,
        environment=performance_config.environment,
    )

    # Create isolated profiler
    profiler = AdvancedProfiler(performance_config)

    yield profiler

    # Cleanup
    if profiler.is_profiling:
        profiler.stop_session()
    reset_profiler()


@pytest.fixture(scope="function")
def mock_qt_environment():
    """Mock Qt environment for testing without requiring PyQt6."""
    with patch("core.performance.qt_profiler.QT_AVAILABLE", True):
        # Mock Qt classes
        mock_qobject = Mock()
        mock_qevent = Mock()
        mock_qapplication = Mock()

        with (
            patch("core.performance.qt_profiler.QObject", mock_qobject),
            patch("core.performance.qt_profiler.QEvent", mock_qevent),
            patch("core.performance.qt_profiler.QApplication", mock_qapplication),
        ):
            yield {
                "QObject": mock_qobject,
                "QEvent": mock_qevent,
                "QApplication": mock_qapplication,
            }


@pytest.fixture(scope="function")
def performance_test_data() -> Dict[str, Any]:
    """Provide test data for performance tests."""
    return {
        "test_functions": [
            {"name": "fast_function", "execution_time": 0.001, "memory_usage": 1.0},
            {"name": "medium_function", "execution_time": 0.01, "memory_usage": 10.0},
            {"name": "slow_function", "execution_time": 0.1, "memory_usage": 100.0},
        ],
        "test_sessions": [
            {
                "session_id": "test_session_1",
                "duration_minutes": 5,
                "function_count": 10,
            },
            {
                "session_id": "test_session_2",
                "duration_minutes": 15,
                "function_count": 25,
            },
        ],
        "performance_thresholds": {
            "profiler_overhead_percent": 1.0,
            "service_resolution_ms": 1.0,
            "arrow_rendering_ms": 5.0,
            "memory_tracking_overhead_percent": 5.0,
        },
    }


@pytest.fixture(scope="function")
def mock_system_resources():
    """Mock system resource monitoring for consistent testing."""
    with patch("psutil.Process") as mock_process:
        # Mock memory info
        mock_memory_info = Mock()
        mock_memory_info.rss = 100 * 1024 * 1024  # 100MB
        mock_memory_info.vms = 200 * 1024 * 1024  # 200MB

        mock_process_instance = Mock()
        mock_process_instance.memory_info.return_value = mock_memory_info
        mock_process_instance.memory_percent.return_value = 10.0
        mock_process_instance.pid = 12345

        mock_process.return_value = mock_process_instance

        # Mock virtual memory
        with patch("psutil.virtual_memory") as mock_virtual_memory:
            mock_vm = Mock()
            mock_vm.available = 8 * 1024 * 1024 * 1024  # 8GB available
            mock_virtual_memory.return_value = mock_vm

            yield {
                "process": mock_process_instance,
                "memory_info": mock_memory_info,
                "virtual_memory": mock_vm,
            }


@pytest.fixture(scope="session", autouse=True)
def performance_test_session_setup():
    """Session-wide setup for performance tests."""
    # Set test environment variables
    import os

    os.environ["TKA_ENV"] = "test"
    os.environ["TKA_PROFILING_ENABLED"] = "true"
    os.environ["TKA_MONITORING_ENABLED"] = "true"

    yield

    # Session cleanup
    # Reset all global instances
    reset_performance_config()
    reset_profiler()
    reset_qt_profiler()
    reset_memory_tracker()
    reset_performance_storage()


@pytest.fixture(scope="function", autouse=True)
def performance_test_cleanup():
    """Automatic cleanup after each performance test."""
    yield

    # Reset global instances after each test
    reset_profiler()
    reset_qt_profiler()
    reset_memory_tracker()


def pytest_configure(config):
    """Configure pytest for performance testing."""
    # Add custom markers
    config.addinivalue_line("markers", "performance: mark test as a performance test")
    config.addinivalue_line("markers", "benchmark: mark test as a benchmark test")
    config.addinivalue_line("markers", "regression: mark test as a regression test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")


def pytest_collection_modifyitems(config, items):
    """Modify test collection for performance tests."""
    # Add performance marker to all tests in performance directory
    for item in items:
        if "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)

        # Add specific markers based on test names
        if "benchmark" in item.name:
            item.add_marker(pytest.mark.benchmark)
        elif "regression" in item.name:
            item.add_marker(pytest.mark.regression)
        elif "integration" in item.name:
            item.add_marker(pytest.mark.integration)


@pytest.fixture
def performance_assertion_helper():
    """Helper for performance assertions."""

    class PerformanceAssertionHelper:
        @staticmethod
        def assert_execution_time_within_threshold(
            execution_time: float,
            threshold_ms: float,
            operation_name: str = "operation",
        ):
            """Assert that execution time is within threshold."""
            execution_time_ms = execution_time * 1000
            assert (
                execution_time_ms <= threshold_ms
            ), f"{operation_name} execution time ({execution_time_ms:.3f}ms) exceeds threshold ({threshold_ms}ms)"

        @staticmethod
        def assert_overhead_within_threshold(
            baseline_time: float,
            profiled_time: float,
            threshold_percent: float,
            operation_name: str = "operation",
        ):
            """Assert that profiling overhead is within threshold."""
            overhead_percent = ((profiled_time - baseline_time) / baseline_time) * 100
            assert (
                overhead_percent <= threshold_percent
            ), f"{operation_name} overhead ({overhead_percent:.2f}%) exceeds threshold ({threshold_percent}%)"

        @staticmethod
        def assert_memory_usage_reasonable(
            memory_mb: float, max_memory_mb: float, operation_name: str = "operation"
        ):
            """Assert that memory usage is reasonable."""
            assert (
                memory_mb <= max_memory_mb
            ), f"{operation_name} memory usage ({memory_mb:.1f}MB) exceeds limit ({max_memory_mb}MB)"

        @staticmethod
        def assert_regression_detected(
            regressions: list, function_name: str, expected_regression_percent: float
        ):
            """Assert that a performance regression was detected."""
            regression_functions = [r["function"] for r in regressions]
            assert (
                function_name in regression_functions
            ), f"Expected regression in {function_name} not detected"

            function_regression = next(
                r for r in regressions if r["function"] == function_name
            )
            assert (
                function_regression["regression_percent"] >= expected_regression_percent
            ), f"Detected regression ({function_regression['regression_percent']:.1f}%) is less than expected ({expected_regression_percent}%)"

    return PerformanceAssertionHelper()


@pytest.fixture
def performance_data_generator():
    """Generate test performance data."""
    import random
    from datetime import datetime, timedelta

    from core.performance.metrics import FunctionMetrics, SystemMetrics

    class PerformanceDataGenerator:
        @staticmethod
        def generate_function_metrics(
            name: str, call_count: int = 100, base_time: float = 0.01
        ) -> FunctionMetrics:
            """Generate realistic function metrics."""
            execution_times = [
                base_time + random.gauss(0, base_time * 0.1) for _ in range(call_count)
            ]
            execution_times = [
                max(0.001, t) for t in execution_times
            ]  # Ensure positive times

            total_time = sum(execution_times)
            avg_time = total_time / call_count
            min_time = min(execution_times)
            max_time = max(execution_times)

            memory_usages = [random.uniform(1.0, 50.0) for _ in range(call_count)]
            memory_total = sum(memory_usages)
            memory_avg = memory_total / call_count

            metrics = FunctionMetrics(
                name=name,
                call_count=call_count,
                total_time=total_time,
                avg_time=avg_time,
                min_time=min_time,
                max_time=max_time,
                memory_total=memory_total,
                memory_avg=memory_avg,
                execution_times=execution_times,
                memory_usages=memory_usages,
            )

            # Add some cache metrics
            metrics.cache_hits = random.randint(0, call_count)
            metrics.cache_misses = call_count - metrics.cache_hits

            return metrics

        @staticmethod
        def generate_system_metrics(count: int = 100) -> list:
            """Generate realistic system metrics."""
            metrics = []
            base_time = datetime.now()

            for i in range(count):
                metric = SystemMetrics(
                    timestamp=base_time + timedelta(seconds=i),
                    cpu_percent=random.uniform(10.0, 80.0),
                    memory_mb=random.uniform(100.0, 1000.0),
                    memory_percent=random.uniform(10.0, 60.0),
                    thread_count=random.randint(10, 50),
                    open_files=random.randint(50, 200),
                )
                metrics.append(metric)

            return metrics

    return PerformanceDataGenerator()
