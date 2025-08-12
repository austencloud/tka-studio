"""
Performance monitoring microservice for pictograph rendering.

This service handles:
- Render operation timing
- Cache hit/miss tracking
- Memory usage monitoring
- Performance reporting and analytics
- Optimization recommendations
"""

import logging
import time
import uuid
from typing import Any

from desktop.modern.core.interfaces.pictograph_rendering_services import (
    IPictographPerformanceMonitor,
)

logger = logging.getLogger(__name__)


class PictographPerformanceMonitor(IPictographPerformanceMonitor):
    """
    Microservice for monitoring pictograph rendering performance.

    Provides:
    - Render operation timing with detailed breakdowns
    - Cache performance tracking
    - Memory usage monitoring
    - Performance analytics and reporting
    - Optimization recommendations
    """

    def __init__(self):
        """Initialize the performance monitor."""
        # Active timers
        self._active_timers: dict[str, dict[str, Any]] = {}

        # Completed operation history
        self._operation_history: list[dict[str, Any]] = []

        # Cache performance tracking
        self._cache_stats: dict[str, dict[str, int]] = {
            "grid": {"hits": 0, "misses": 0},
            "prop": {"hits": 0, "misses": 0},
            "glyph": {"hits": 0, "misses": 0},
            "arrow": {"hits": 0, "misses": 0},
            "svg_data": {"hits": 0, "misses": 0},
        }

        # Performance thresholds (in milliseconds)
        self._thresholds = {
            "grid_render": 50.0,
            "prop_render": 100.0,
            "glyph_render": 75.0,
            "arrow_render": 150.0,
            "svg_load": 25.0,
            "color_transform": 10.0,
        }

        # System performance tracking
        self._system_stats = {
            "total_operations": 0,
            "slow_operations": 0,
            "memory_warnings": 0,
            "error_count": 0,
        }

    def start_render_timer(self, operation: str) -> str:
        """Start timing a render operation. Returns timer ID."""
        timer_id = str(uuid.uuid4())

        self._active_timers[timer_id] = {
            "operation": operation,
            "start_time": time.perf_counter(),
            "start_timestamp": time.time(),
        }

        logger.debug(
            f"⏱️ [PERFORMANCE_MONITOR] Started timer for {operation}: {timer_id}"
        )
        return timer_id

    def end_render_timer(self, timer_id: str) -> float:
        """End timing and return duration in milliseconds."""
        if timer_id not in self._active_timers:
            logger.warning(f"⚠️ [PERFORMANCE_MONITOR] Timer not found: {timer_id}")
            return 0.0

        timer_data = self._active_timers.pop(timer_id)
        end_time = time.perf_counter()
        duration_ms = (end_time - timer_data["start_time"]) * 1000

        # Record the completed operation
        operation_record = {
            "operation": timer_data["operation"],
            "duration_ms": duration_ms,
            "timestamp": timer_data["start_timestamp"],
            "timer_id": timer_id,
        }

        self._operation_history.append(operation_record)
        self._system_stats["total_operations"] += 1

        # Check if operation was slow
        threshold = self._thresholds.get(timer_data["operation"], 100.0)
        if duration_ms > threshold:
            self._system_stats["slow_operations"] += 1
            logger.warning(
                f"🐌 [PERFORMANCE_MONITOR] Slow operation detected: {timer_data['operation']} "
                f"took {duration_ms:.1f}ms (threshold: {threshold}ms)"
            )

        # Keep history manageable (last 1000 operations)
        if len(self._operation_history) > 1000:
            self._operation_history = self._operation_history[-1000:]

        logger.debug(
            f"⏱️ [PERFORMANCE_MONITOR] Completed {timer_data['operation']}: {duration_ms:.1f}ms"
        )
        return duration_ms

    def record_cache_hit(self, cache_type: str) -> None:
        """Record a cache hit."""
        if cache_type in self._cache_stats:
            self._cache_stats[cache_type]["hits"] += 1
        else:
            logger.warning(f"⚠️ [PERFORMANCE_MONITOR] Unknown cache type: {cache_type}")

    def record_cache_miss(self, cache_type: str) -> None:
        """Record a cache miss."""
        if cache_type in self._cache_stats:
            self._cache_stats[cache_type]["misses"] += 1
        else:
            logger.warning(f"⚠️ [PERFORMANCE_MONITOR] Unknown cache type: {cache_type}")

    def record_memory_warning(self) -> None:
        """Record a memory usage warning."""
        self._system_stats["memory_warnings"] += 1
        logger.warning("🧠 [PERFORMANCE_MONITOR] Memory usage warning recorded")

    def record_error(self, operation: str, error_message: str) -> None:
        """Record an error during rendering operations."""
        self._system_stats["error_count"] += 1
        logger.error(f"❌ [PERFORMANCE_MONITOR] Error in {operation}: {error_message}")

    def get_performance_report(self) -> dict[str, Any]:
        """Get comprehensive performance report."""
        # Calculate cache hit rates
        cache_performance = {}
        for cache_type, stats in self._cache_stats.items():
            total = stats["hits"] + stats["misses"]
            hit_rate = (stats["hits"] / total * 100) if total > 0 else 0
            cache_performance[cache_type] = {
                "hits": stats["hits"],
                "misses": stats["misses"],
                "hit_rate_percent": round(hit_rate, 2),
            }

        # Calculate operation performance
        operation_performance = self._analyze_operation_performance()

        # Calculate system health metrics
        total_ops = self._system_stats["total_operations"]
        slow_rate = (
            (self._system_stats["slow_operations"] / total_ops * 100)
            if total_ops > 0
            else 0
        )

        return {
            "cache_performance": cache_performance,
            "operation_performance": operation_performance,
            "system_health": {
                "total_operations": total_ops,
                "slow_operations": self._system_stats["slow_operations"],
                "slow_operation_rate_percent": round(slow_rate, 2),
                "memory_warnings": self._system_stats["memory_warnings"],
                "error_count": self._system_stats["error_count"],
            },
            "active_timers": len(self._active_timers),
            "history_size": len(self._operation_history),
            "recommendations": self._generate_recommendations(),
        }

    def _analyze_operation_performance(self) -> dict[str, Any]:
        """Analyze performance of different operation types."""
        if not self._operation_history:
            return {}

        # Group operations by type
        operation_groups: dict[str, list[float]] = {}
        for record in self._operation_history:
            op_type = record["operation"]
            if op_type not in operation_groups:
                operation_groups[op_type] = []
            operation_groups[op_type].append(record["duration_ms"])

        # Calculate statistics for each operation type
        performance_data = {}
        for op_type, durations in operation_groups.items():
            if durations:
                performance_data[op_type] = {
                    "count": len(durations),
                    "avg_duration_ms": round(sum(durations) / len(durations), 2),
                    "min_duration_ms": round(min(durations), 2),
                    "max_duration_ms": round(max(durations), 2),
                    "threshold_ms": self._thresholds.get(op_type, 100.0),
                }

        return performance_data

    def _generate_recommendations(self) -> list[str]:
        """Generate performance optimization recommendations."""
        recommendations = []

        # Check cache hit rates
        for cache_type, stats in self._cache_stats.items():
            total = stats["hits"] + stats["misses"]
            if total > 10:  # Only recommend if we have enough data
                hit_rate = stats["hits"] / total * 100
                if hit_rate < 70:
                    recommendations.append(
                        f"Low {cache_type} cache hit rate ({hit_rate:.1f}%). "
                        f"Consider increasing cache size or reviewing cache keys."
                    )

        # Check slow operations
        total_ops = self._system_stats["total_operations"]
        if total_ops > 0:
            slow_rate = self._system_stats["slow_operations"] / total_ops * 100
            if slow_rate > 20:
                recommendations.append(
                    f"High slow operation rate ({slow_rate:.1f}%). "
                    f"Consider optimizing rendering pipeline or increasing cache sizes."
                )

        # Check memory warnings
        if self._system_stats["memory_warnings"] > 5:
            recommendations.append(
                "Multiple memory warnings detected. "
                "Consider reducing cache sizes or implementing more aggressive eviction."
            )

        # Check error rate
        if self._system_stats["error_count"] > 0:
            error_rate = (
                (self._system_stats["error_count"] / total_ops * 100)
                if total_ops > 0
                else 0
            )
            if error_rate > 5:
                recommendations.append(
                    f"High error rate ({error_rate:.1f}%). "
                    f"Review error logs and consider adding fallback mechanisms."
                )

        return recommendations

    def reset_statistics(self) -> None:
        """Reset all performance statistics."""
        self._active_timers.clear()
        self._operation_history.clear()

        # Reset cache stats
        for cache_type in self._cache_stats:
            self._cache_stats[cache_type] = {"hits": 0, "misses": 0}

        # Reset system stats
        self._system_stats = {
            "total_operations": 0,
            "slow_operations": 0,
            "memory_warnings": 0,
            "error_count": 0,
        }

        logger.info("🔄 [PERFORMANCE_MONITOR] Reset all performance statistics")

    def get_recent_operations(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get the most recent operations for debugging."""
        return self._operation_history[-limit:] if self._operation_history else []

    def set_threshold(self, operation: str, threshold_ms: float) -> None:
        """Set performance threshold for an operation type."""
        self._thresholds[operation] = threshold_ms
        logger.info(
            f"📊 [PERFORMANCE_MONITOR] Set threshold for {operation}: {threshold_ms}ms"
        )
