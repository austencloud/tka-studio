"""
Performance Framework Tests

Comprehensive test suite for the TKA performance framework including
profiler functionality, metrics collection, Qt integration, and regression detection.
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Any, Dict
from unittest.mock import MagicMock, Mock, patch

import pytest
from core.performance import (
    AdvancedProfiler,
    FunctionMetrics,
    MemoryTracker,
    PerformanceMetrics,
    QtProfiler,
    get_profiler,
    profile,
    profile_block,
)
from core.performance.config import PerformanceConfig, get_performance_config
from infrastructure.performance.storage import PerformanceStorage


class TestAdvancedProfiler:
    """Test the advanced profiler functionality."""

    def setup_method(self):
        """Setup test environment."""
        self.config = PerformanceConfig.create_default()
        self.profiler = AdvancedProfiler(self.config)

    def test_profiler_initialization(self):
        """Test profiler initialization."""
        assert self.profiler.config == self.config
        assert not self.profiler.is_profiling
        assert self.profiler.current_session is None
        assert len(self.profiler._function_stats) == 0

    def test_session_lifecycle(self):
        """Test profiling session start/stop lifecycle."""
        # Start session
        result = self.profiler.start_session("test_session")
        assert result.is_success()
        assert self.profiler.is_profiling
        assert self.profiler.current_session is not None
        assert self.profiler.current_session.session_id == "test_session"

        # Stop session
        result = self.profiler.stop_session()
        assert result.is_success()
        assert not self.profiler.is_profiling
        session_data = result.value
        assert session_data is not None
        assert session_data.session_id == "test_session"
        assert session_data.end_time is not None

    def test_function_profiling_decorator(self):
        """Test function profiling with decorator."""

        @self.profiler.profile_function
        def test_function():
            time.sleep(0.01)  # 10ms
            return "test_result"

        # Start profiling
        self.profiler.start_session("decorator_test")

        # Call function
        result = test_function()
        assert result == "test_result"

        # Check metrics
        function_name = f"{test_function.__module__}.{test_function.__qualname__}"
        assert function_name in self.profiler._function_stats

        stats = self.profiler._function_stats[function_name]
        assert stats.call_count == 1
        assert stats.total_time > 0.008  # Should be at least 8ms
        assert stats.avg_time > 0.008

    def test_profile_block_context_manager(self):
        """Test profiling with context manager."""
        self.profiler.start_session("context_test")

        with self.profiler.profile_block("test_block"):
            time.sleep(0.01)  # 10ms

        # Check metrics
        assert "test_block" in self.profiler._function_stats
        stats = self.profiler._function_stats["test_block"]
        assert stats.call_count == 1
        assert stats.total_time > 0.008

    def test_performance_bottleneck_detection(self):
        """Test bottleneck detection."""
        self.profiler.start_session("bottleneck_test")

        # Create functions with different performance characteristics
        @self.profiler.profile_function
        def fast_function():
            time.sleep(0.001)  # 1ms

        @self.profiler.profile_function
        def slow_function():
            time.sleep(0.05)  # 50ms - should trigger bottleneck alert

        # Call functions
        fast_function()
        slow_function()

        # Get bottlenecks
        bottlenecks = self.profiler.get_top_bottlenecks(5)
        assert len(bottlenecks) == 2

        # Slow function should be first
        slowest = bottlenecks[0]
        assert "slow_function" in slowest.name
        assert slowest.total_time > 0.04

    def test_memory_tracking_integration(self):
        """Test memory tracking integration."""
        self.profiler.start_session("memory_test")

        @self.profiler.profile_function
        def memory_intensive_function():
            # Allocate some memory
            data = [i for i in range(10000)]
            return len(data)

        result = memory_intensive_function()
        assert result == 10000

        # Check memory metrics
        function_name = f"{memory_intensive_function.__module__}.{memory_intensive_function.__qualname__}"
        stats = self.profiler._function_stats[function_name]
        assert stats.memory_total >= 0  # Should track memory delta

    def test_thread_safety(self):
        """Test thread safety of profiler."""
        self.profiler.start_session("thread_test")
        results = []

        @self.profiler.profile_function
        def threaded_function(thread_id):
            time.sleep(0.01)
            return thread_id

        def worker(thread_id):
            result = threaded_function(thread_id)
            results.append(result)

        # Start multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        # Check results
        assert len(results) == 5
        assert set(results) == {0, 1, 2, 3, 4}

        # Check profiling data
        function_name = (
            f"{threaded_function.__module__}.{threaded_function.__qualname__}"
        )
        stats = self.profiler._function_stats[function_name]
        assert stats.call_count == 5


class TestPerformanceMetrics:
    """Test performance metrics collection and analysis."""

    def setup_method(self):
        """Setup test environment."""
        self.metrics = PerformanceMetrics()

    def test_function_metrics_recording(self):
        """Test recording function execution metrics."""
        # Record some function executions
        self.metrics.record_function_execution("test_function", 0.1, 50.0)
        self.metrics.record_function_execution("test_function", 0.2, 30.0)
        self.metrics.record_function_execution("test_function", 0.15, 40.0)

        # Check metrics
        assert "test_function" in self.metrics.function_metrics
        func_metrics = self.metrics.function_metrics["test_function"]

        assert func_metrics.call_count == 3
        assert abs(func_metrics.total_time - 0.45) < 1e-10
        assert func_metrics.min_time == 0.1
        assert func_metrics.max_time == 0.2
        assert func_metrics.memory_total == 120.0

    def test_cache_performance_tracking(self):
        """Test cache hit/miss tracking."""
        # Record cache events
        self.metrics.record_cache_event("cached_function", True)  # Hit
        self.metrics.record_cache_event("cached_function", True)  # Hit
        self.metrics.record_cache_event("cached_function", False)  # Miss
        self.metrics.record_cache_event("cached_function", True)  # Hit

        # Check cache metrics
        func_metrics = self.metrics.function_metrics["cached_function"]
        assert func_metrics.cache_hits == 3
        assert func_metrics.cache_misses == 1
        assert func_metrics.cache_hit_rate == 75.0

    def test_performance_summary_generation(self):
        """Test performance summary generation."""
        # Add some test data
        self.metrics.record_function_execution("slow_function", 0.5, 100.0)
        self.metrics.record_function_execution("fast_function", 0.01, 10.0)
        self.metrics.record_cache_event(
            "cached_function", False
        )  # Poor cache performance

        summary = self.metrics.get_performance_summary()

        assert "summary" in summary
        assert "top_bottlenecks" in summary
        assert "memory_hotspots" in summary
        assert "cache_performance_issues" in summary
        assert "optimization_recommendations" in summary

        # Check bottlenecks
        bottlenecks = summary["top_bottlenecks"]
        assert len(bottlenecks) >= 1
        assert bottlenecks[0]["function"] == "slow_function"

    def test_regression_detection(self):
        """Test performance regression detection."""
        # Create baseline metrics
        baseline_metrics = {
            "test_function": FunctionMetrics(
                name="test_function",
                call_count=10,
                total_time=1.0,
                avg_time=0.1,
                memory_total=100.0,
                memory_avg=10.0,
            )
        }

        # Record current metrics (with regression)
        for _ in range(10):
            self.metrics.record_function_execution(
                "test_function", 0.15, 15.0
            )  # 50% slower, 50% more memory

        # Detect regressions
        regressions = self.metrics.detect_performance_regressions(
            baseline_metrics, threshold_percent=10.0
        )

        assert len(regressions) >= 1

        # Check execution time regression
        time_regression = next(
            (r for r in regressions if r["type"] == "execution_time"), None
        )
        assert time_regression is not None
        assert time_regression["function"] == "test_function"
        assert (
            time_regression["regression_percent"] > 40
        )  # Should detect ~50% regression


class TestQtProfiler:
    """Test Qt-specific profiling functionality."""

    def setup_method(self):
        """Setup test environment."""
        self.qt_profiler = QtProfiler()

    def test_qt_profiler_initialization(self):
        """Test Qt profiler initialization."""
        assert not self.qt_profiler.is_profiling
        assert len(self.qt_profiler.event_metrics) == 0
        assert len(self.qt_profiler.paint_metrics) == 0

    @pytest.mark.skipif(
        not hasattr(QtProfiler, "start_profiling"), reason="Qt profiling not available"
    )
    def test_qt_profiling_lifecycle(self):
        """Test Qt profiling start/stop lifecycle."""
        # Start profiling
        result = self.qt_profiler.start_profiling()
        if result.is_success():
            assert self.qt_profiler.is_profiling

            # Stop profiling
            result = self.qt_profiler.stop_profiling()
            assert result.is_success()
            assert not self.qt_profiler.is_profiling

    def test_qt_performance_summary(self):
        """Test Qt performance summary generation."""
        summary = self.qt_profiler.get_qt_performance_summary()

        assert "event_performance" in summary
        assert "paint_performance" in summary
        assert "signal_slot_performance" in summary
        assert "object_lifecycle" in summary
        assert "recommendations" in summary


class TestMemoryTracker:
    """Test memory tracking functionality."""

    def setup_method(self):
        """Setup test environment."""
        self.memory_tracker = MemoryTracker()

    def test_memory_tracker_initialization(self):
        """Test memory tracker initialization."""
        assert not self.memory_tracker.is_tracking
        assert len(self.memory_tracker.snapshots) == 0

    def test_memory_usage_tracking(self):
        """Test memory usage tracking."""
        current_usage = self.memory_tracker.get_current_usage()
        assert current_usage >= 0  # Should return valid memory usage

    def test_memory_summary_generation(self):
        """Test memory summary generation."""
        # Start tracking to get some data
        result = self.memory_tracker.start_tracking()
        if result.is_success():
            time.sleep(0.1)  # Let it collect some data

            summary = self.memory_tracker.get_memory_summary()

            if "error" not in summary:
                assert "current" in summary
                assert "statistics" in summary
                assert "tracking" in summary
                assert "recommendations" in summary


class TestPerformanceStorage:
    """Test performance data storage functionality."""

    def setup_method(self):
        """Setup test environment."""
        # Use temporary database for testing
        import os
        import tempfile

        config = PerformanceConfig.create_default()

        # Create temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()

        updated_storage = config.storage.with_database_path(self.temp_db.name)
        test_config = PerformanceConfig(
            profiling=config.profiling,
            monitoring=config.monitoring,
            regression=config.regression,
            storage=updated_storage,
            environment=config.environment,
        )
        self.storage = PerformanceStorage(test_config)

    def teardown_method(self):
        """Clean up test environment."""
        import os

        try:
            os.unlink(self.temp_db.name)
        except OSError:
            pass

    def test_storage_initialization(self):
        """Test storage initialization."""
        # Database should be initialized
        assert str(self.storage.db_path) == self.temp_db.name

    def test_session_storage_and_retrieval(self):
        """Test storing and retrieving session data."""
        from core.performance.profiler import ProfilerSession

        # Create test session
        session = ProfilerSession(
            session_id="test_session",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(minutes=5),
            metadata={"test": "data"},
        )

        # Add some function metrics
        session.function_metrics["test_function"] = FunctionMetrics(
            name="test_function",
            call_count=5,
            total_time=0.5,
            avg_time=0.1,
            min_time=0.05,
            max_time=0.15,
            memory_total=50.0,
            memory_avg=10.0,
        )

        # Save session
        result = self.storage.save_session(session)
        assert result.is_success()

        # Retrieve session
        result = self.storage.get_session("test_session")
        assert result.is_success()

        retrieved_session = result.value
        assert retrieved_session is not None
        assert retrieved_session["session_id"] == "test_session"
        assert len(retrieved_session["function_metrics"]) == 1

    def test_recent_sessions_retrieval(self):
        """Test retrieving recent sessions."""
        result = self.storage.get_recent_sessions(10)
        assert result.is_success()

        sessions = result.value
        assert isinstance(sessions, list)


class TestPerformanceIntegration:
    """Integration tests for the complete performance framework."""

    def test_end_to_end_profiling_workflow(self):
        """Test complete profiling workflow."""
        # Get profiler
        profiler = get_profiler()

        # Start session
        result = profiler.start_session("integration_test")
        assert result.is_success()
        session_id = result.value

        # Profile some functions
        @profile
        def test_function_1():
            time.sleep(0.01)
            return "result1"

        @profile
        def test_function_2():
            time.sleep(0.02)
            return "result2"

        # Execute functions
        result1 = test_function_1()
        result2 = test_function_2()

        assert result1 == "result1"
        assert result2 == "result2"

        # Use profile block
        with profile_block("integration_block"):
            time.sleep(0.01)

        # Stop session
        result = profiler.stop_session()
        assert result.is_success()

        session_data = result.value
        assert session_data is not None
        assert len(session_data.function_metrics) >= 3  # 2 functions + 1 block

    def test_configuration_integration(self):
        """Test configuration system integration."""
        config = get_performance_config()

        assert config.profiling.enabled is not None
        assert config.monitoring.enabled is not None
        assert config.storage.database_path is not None

        # Validate configuration
        validation_result = config.validate()
        assert validation_result.is_success()

    def test_global_instances(self):
        """Test global instance management."""
        # Test that global instances are properly managed
        profiler1 = get_profiler()
        profiler2 = get_profiler()

        assert profiler1 is profiler2  # Should be same instance

        # Test reset functionality
        from core.performance.profiler import reset_profiler

        reset_profiler()

        profiler3 = get_profiler()
        assert profiler3 is not profiler1  # Should be new instance
