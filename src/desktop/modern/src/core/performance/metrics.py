"""
Performance Metrics Collection and Analysis

Provides comprehensive metrics collection, statistical analysis,
and performance trend detection for the TKA performance framework.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import statistics
from typing import Any

import numpy as np


logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of performance metrics."""
    EXECUTION_TIME = "execution_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    IO_OPERATIONS = "io_operations"
    CACHE_PERFORMANCE = "cache_performance"
    QT_EVENTS = "qt_events"


@dataclass
class FunctionMetrics:
    """Comprehensive metrics for a single function."""
    name: str
    call_count: int = 0
    total_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    avg_time: float = 0.0
    std_dev: float = 0.0
    percentile_95: float = 0.0
    percentile_99: float = 0.0

    # Memory metrics
    memory_total: float = 0.0
    memory_avg: float = 0.0
    memory_peak: float = 0.0

    # Cache metrics
    cache_hits: int = 0
    cache_misses: int = 0

    # Historical data for trend analysis
    execution_times: list[float] = field(default_factory=list)
    memory_usages: list[float] = field(default_factory=list)

    def update_statistics(self):
        """Update calculated statistics from raw data."""
        if self.execution_times:
            self.avg_time = statistics.mean(self.execution_times)
            if len(self.execution_times) > 1:
                self.std_dev = statistics.stdev(self.execution_times)

            # Use numpy for percentile calculations if available
            try:
                self.percentile_95 = np.percentile(self.execution_times, 95)
                self.percentile_99 = np.percentile(self.execution_times, 99)
            except ImportError:
                # Fallback if numpy not available
                sorted_times = sorted(self.execution_times)
                n = len(sorted_times)
                self.percentile_95 = sorted_times[int(0.95 * n)] if n > 0 else 0
                self.percentile_99 = sorted_times[int(0.99 * n)] if n > 0 else 0

    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate percentage."""
        total_requests = self.cache_hits + self.cache_misses
        return (self.cache_hits / total_requests * 100) if total_requests > 0 else 0.0

    @property
    def efficiency_score(self) -> float:
        """Calculate efficiency score (0-100) based on multiple factors."""
        # Combine execution time, memory usage, and cache performance
        time_score = max(0, 100 - (self.avg_time * 1000))  # Penalize slow functions
        memory_score = max(0, 100 - (self.memory_avg / 1024))  # Penalize memory-heavy functions
        cache_score = self.cache_hit_rate if self.cache_hits + self.cache_misses > 0 else 100

        return (time_score * 0.4 + memory_score * 0.3 + cache_score * 0.3)


@dataclass
class SystemMetrics:
    """System-level performance metrics."""
    timestamp: datetime
    cpu_percent: float
    memory_mb: float
    memory_percent: float
    disk_io_read: int = 0
    disk_io_write: int = 0
    network_bytes_sent: int = 0
    network_bytes_recv: int = 0
    thread_count: int = 0
    open_files: int = 0


@dataclass
class QtEventMetrics:
    """Metrics for Qt events."""
    event_type: str
    count: int = 0
    total_time: float = 0.0
    avg_time: float = 0.0
    max_time: float = 0.0


class PerformanceMetrics:
    """
    Central metrics collection and analysis engine.

    Provides comprehensive performance data collection, statistical analysis,
    and performance trend detection capabilities.
    """

    def __init__(self):
        self.function_metrics: dict[str, FunctionMetrics] = {}
        self.system_metrics: list[SystemMetrics] = []
        self.qt_event_metrics: dict[str, QtEventMetrics] = {}
        self.performance_baselines: dict[str, float] = {}

    def record_function_execution(self, function_name: str, execution_time: float,
                                memory_usage: float = 0.0):
        """Record a function execution with timing and memory data."""
        if function_name not in self.function_metrics:
            self.function_metrics[function_name] = FunctionMetrics(name=function_name)

        metrics = self.function_metrics[function_name]
        metrics.call_count += 1
        metrics.total_time += execution_time
        metrics.min_time = min(metrics.min_time, execution_time)
        metrics.max_time = max(metrics.max_time, execution_time)

        # Add to historical data
        metrics.execution_times.append(execution_time)
        if memory_usage > 0:
            metrics.memory_usages.append(memory_usage)
            metrics.memory_total += memory_usage
            metrics.memory_peak = max(metrics.memory_peak, memory_usage)

        # Update calculated statistics
        metrics.update_statistics()

    def record_cache_event(self, function_name: str, hit: bool):
        """Record cache hit or miss for a function."""
        if function_name not in self.function_metrics:
            self.function_metrics[function_name] = FunctionMetrics(name=function_name)

        metrics = self.function_metrics[function_name]
        if hit:
            metrics.cache_hits += 1
        else:
            metrics.cache_misses += 1

    def record_system_metrics(self, metrics: SystemMetrics):
        """Record system-level performance metrics."""
        self.system_metrics.append(metrics)

        # Keep only last 1000 entries to prevent memory bloat
        if len(self.system_metrics) > 1000:
            self.system_metrics = self.system_metrics[-1000:]

    def record_qt_event(self, event_type: str, execution_time: float):
        """Record Qt event execution time."""
        if event_type not in self.qt_event_metrics:
            self.qt_event_metrics[event_type] = QtEventMetrics(event_type=event_type)

        metrics = self.qt_event_metrics[event_type]
        metrics.count += 1
        metrics.total_time += execution_time
        metrics.avg_time = metrics.total_time / metrics.count
        metrics.max_time = max(metrics.max_time, execution_time)

    def get_performance_summary(self) -> dict[str, Any]:
        """Generate comprehensive performance summary."""
        if not self.function_metrics:
            return {"error": "No performance data available"}

        # Top bottlenecks by total time
        top_by_time = sorted(
            self.function_metrics.values(),
            key=lambda x: x.total_time,
            reverse=True
        )[:10]

        # Top memory consumers
        top_by_memory = sorted(
            self.function_metrics.values(),
            key=lambda x: x.memory_total,
            reverse=True
        )[:10]

        # Functions with poor cache performance
        poor_cache_performance = [
            m for m in self.function_metrics.values()
            if (m.cache_hits + m.cache_misses) > 0 and m.cache_hit_rate < 80
        ]

        # Calculate overall statistics
        total_execution_time = sum(m.total_time for m in self.function_metrics.values())
        total_function_calls = sum(m.call_count for m in self.function_metrics.values())
        avg_execution_time = total_execution_time / total_function_calls if total_function_calls > 0 else 0

        return {
            "summary": {
                "total_functions_profiled": len(self.function_metrics),
                "total_execution_time": total_execution_time,
                "total_function_calls": total_function_calls,
                "average_execution_time": avg_execution_time,
                "data_collection_period": self._get_collection_period()
            },
            "top_bottlenecks": [
                {
                    "function": m.name,
                    "total_time": m.total_time,
                    "call_count": m.call_count,
                    "avg_time": m.avg_time,
                    "efficiency_score": m.efficiency_score
                }
                for m in top_by_time
            ],
            "memory_hotspots": [
                {
                    "function": m.name,
                    "total_memory": m.memory_total,
                    "avg_memory": m.memory_avg,
                    "peak_memory": m.memory_peak
                }
                for m in top_by_memory if m.memory_total > 0
            ],
            "cache_performance_issues": [
                {
                    "function": m.name,
                    "hit_rate": m.cache_hit_rate,
                    "total_requests": m.cache_hits + m.cache_misses
                }
                for m in poor_cache_performance
            ],
            "qt_events": [
                {
                    "event_type": m.event_type,
                    "count": m.count,
                    "avg_time": m.avg_time,
                    "max_time": m.max_time
                }
                for m in self.qt_event_metrics.values()
            ],
            "optimization_recommendations": self._generate_optimization_recommendations()
        }

    def _get_collection_period(self) -> dict[str, Any]:
        """Get the time period over which data was collected."""
        if not self.system_metrics:
            return {"error": "No system metrics available"}

        start_time = min(m.timestamp for m in self.system_metrics)
        end_time = max(m.timestamp for m in self.system_metrics)

        return {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": (end_time - start_time).total_seconds()
        }

    def _generate_optimization_recommendations(self) -> list[dict[str, str]]:
        """Generate AI-powered optimization recommendations."""
        recommendations = []

        # Analyze function metrics for optimization opportunities
        for func_name, metrics in self.function_metrics.items():
            # High execution time recommendations
            if metrics.avg_time > 0.1:  # 100ms threshold
                recommendations.append({
                    "type": "performance",
                    "function": func_name,
                    "issue": "High execution time",
                    "recommendation": f"Function averages {metrics.avg_time*1000:.1f}ms. Consider caching, algorithm optimization, or background processing.",
                    "priority": "high" if metrics.avg_time > 0.5 else "medium"
                })

            # Memory usage recommendations
            if metrics.memory_avg > 50:  # 50MB threshold
                recommendations.append({
                    "type": "memory",
                    "function": func_name,
                    "issue": "High memory usage",
                    "recommendation": f"Function uses {metrics.memory_avg:.1f}MB on average. Consider object pooling or data structure optimization.",
                    "priority": "medium"
                })

            # Cache performance recommendations
            if (metrics.cache_hits + metrics.cache_misses) > 0 and metrics.cache_hit_rate < 80:
                recommendations.append({
                    "type": "cache",
                    "function": func_name,
                    "issue": "Poor cache performance",
                    "recommendation": f"Cache hit rate is {metrics.cache_hit_rate:.1f}%. Review cache size, eviction policy, or caching strategy.",
                    "priority": "medium"
                })

        return recommendations

    def detect_performance_regressions(self, baseline_metrics: dict[str, FunctionMetrics],
                                     threshold_percent: float = 5.0) -> list[dict[str, Any]]:
        """Detect performance regressions compared to baseline metrics."""
        regressions = []

        for func_name, current_metrics in self.function_metrics.items():
            if func_name not in baseline_metrics:
                continue

            baseline = baseline_metrics[func_name]

            # Check execution time regression
            if baseline.avg_time > 0:
                time_increase = ((current_metrics.avg_time - baseline.avg_time) / baseline.avg_time) * 100
                if time_increase > threshold_percent:
                    regressions.append({
                        "function": func_name,
                        "type": "execution_time",
                        "baseline": baseline.avg_time,
                        "current": current_metrics.avg_time,
                        "regression_percent": time_increase,
                        "severity": "critical" if time_increase > 20 else "warning"
                    })

            # Check memory regression
            if baseline.memory_avg > 0:
                memory_increase = ((current_metrics.memory_avg - baseline.memory_avg) / baseline.memory_avg) * 100
                if memory_increase > threshold_percent:
                    regressions.append({
                        "function": func_name,
                        "type": "memory_usage",
                        "baseline": baseline.memory_avg,
                        "current": current_metrics.memory_avg,
                        "regression_percent": memory_increase,
                        "severity": "warning"
                    })

        return regressions
