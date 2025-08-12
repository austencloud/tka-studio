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

from .profiler import AdvancedProfiler, get_profiler, profile, profile_block
from .metrics import PerformanceMetrics, FunctionMetrics, SystemMetrics, QtEventMetrics
from .config import PerformanceConfig, get_performance_config
from .qt_profiler import QtProfiler, get_qt_profiler
from .memory_tracker import MemoryTracker, get_memory_tracker
from .integration import (
    PerformanceIntegration,
    get_performance_integration,
    initialize_performance_framework,
    shutdown_performance_framework,
    profile_critical_path,
    monitor_memory_intensive,
)

__all__ = [
    # Core profiling
    "AdvancedProfiler",
    "get_profiler",
    "profile",
    "profile_block",
    # Metrics
    "PerformanceMetrics",
    "FunctionMetrics",
    "SystemMetrics",
    "QtEventMetrics",
    # Qt profiling
    "QtProfiler",
    "get_qt_profiler",
    # Memory tracking
    "MemoryTracker",
    "get_memory_tracker",
    # Configuration
    "PerformanceConfig",
    "get_performance_config",
    # Integration
    "PerformanceIntegration",
    "get_performance_integration",
    "initialize_performance_framework",
    "shutdown_performance_framework",
    "profile_critical_path",
    "monitor_memory_intensive",
]
