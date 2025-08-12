"""
TKA Performance Framework

Core performance monitoring and profiling infrastructure for TKA Desktop.
Provides comprehensive function-level profiling, real-time monitoring,
and performance regression detection.

COMPONENTS:
- profiler: Advanced profiling engine with minimal overhead
- metrics: Performance metrics collection and analysis
- config: Performance configuration management
- decorators: Performance monitoring decorators

INTEGRATION:
- Extends existing core/monitoring.py for backward compatibility
- Integrates with DI container and Qt integration layers
- Provides foundation for advanced performance analysis

USAGE:
    from desktop.modern.core.performance import profile, profile_block, get_profiler

    # Decorator usage
    @profile
    def my_function():
        pass

    # Context manager usage
    with profile_block("operation_name"):
        # Code to profile
        pass

    # Advanced profiler
    profiler = get_profiler()
    session_id = profiler.start_session("my_session")
    # ... operations ...
    results = profiler.stop_session()
"""
from __future__ import annotations

from .config import PerformanceConfig, get_performance_config
from .integration import (
    PerformanceIntegration,
    get_performance_integration,
    initialize_performance_framework,
    monitor_memory_intensive,
    profile_critical_path,
    shutdown_performance_framework,
)
from .memory_tracker import MemoryTracker, get_memory_tracker
from .metrics import FunctionMetrics, PerformanceMetrics, QtEventMetrics, SystemMetrics
from .profiler import AdvancedProfiler, get_profiler, profile, profile_block
from .qt_profiler import QtProfiler, get_qt_profiler


__all__ = [
    # Core profiling
    "AdvancedProfiler",
    "FunctionMetrics",
    # Memory tracking
    "MemoryTracker",
    # Configuration
    "PerformanceConfig",
    # Integration
    "PerformanceIntegration",
    # Metrics
    "PerformanceMetrics",
    "QtEventMetrics",
    # Qt profiling
    "QtProfiler",
    "SystemMetrics",
    "get_memory_tracker",
    "get_performance_config",
    "get_performance_integration",
    "get_profiler",
    "get_qt_profiler",
    "initialize_performance_framework",
    "monitor_memory_intensive",
    "profile",
    "profile_block",
    "profile_critical_path",
    "shutdown_performance_framework",
]
