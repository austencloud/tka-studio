"""
Memory Tracking for TKA Performance Framework

Provides comprehensive memory usage tracking and leak detection
for the TKA desktop application. Integrates with existing Qt
resource management and monitoring infrastructure.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
import gc
import logging
import threading
from typing import Any

import psutil

# Result pattern removed - using simple exceptions
from .config import PerformanceConfig, get_performance_config


logger = logging.getLogger(__name__)


@dataclass
class MemorySnapshot:
    """Snapshot of memory usage at a point in time."""

    timestamp: datetime
    rss_mb: float  # Resident Set Size
    vms_mb: float  # Virtual Memory Size
    percent: float  # Memory percentage
    available_mb: float  # Available system memory
    gc_objects: int  # Number of objects tracked by GC
    gc_collections: dict[int, int] = field(
        default_factory=dict
    )  # GC collections by generation


@dataclass
class MemoryLeak:
    """Detected memory leak information."""

    object_type: str
    count_increase: int
    time_period: timedelta
    severity: str  # "low", "medium", "high"
    first_detected: datetime
    last_detected: datetime


class MemoryTracker:
    """
    Advanced memory tracking and leak detection.

    Features:
    - Real-time memory usage monitoring
    - Memory leak detection
    - Integration with Qt resource management
    - Garbage collection analysis
    - Memory usage profiling per function
    """

    def __init__(self, config: PerformanceConfig | None = None):
        self.config = config or get_performance_config()
        self.is_tracking = False

        # Memory snapshots
        self.snapshots: list[MemorySnapshot] = []
        self.max_snapshots = 1000

        # Leak detection
        self.object_counts: dict[str, list[int]] = {}
        self.detected_leaks: list[MemoryLeak] = []

        # Thread safety
        self._lock = threading.RLock()

        # Integration with existing systems
        self._integrate_with_existing_systems()

    def _integrate_with_existing_systems(self):
        """Integrate with existing Qt resource management."""
        try:
            from presentation.qt_integration.resource_management import qt_resources

            # Hook into existing resource tracking if available
            if hasattr(qt_resources(), "_creation_stats"):
                logger.info(
                    "Integrated with Qt resource management for memory tracking"
                )
        except ImportError:
            logger.debug("Qt resource management not available for integration")

    def start_tracking(self) -> Result[bool, AppError]:
        """
        Start memory tracking.

        Returns:
            Result indicating success or failure
        """
        if not self.config.monitoring.memory_tracking:
            return failure(
                app_error(
                    ErrorType.CONFIGURATION_ERROR,
                    "Memory tracking disabled in configuration",
                )
            )

        if self.is_tracking:
            return success(True)

        try:
            self.is_tracking = True

            # Take initial snapshot
            self._take_snapshot()

            logger.info("Started memory tracking")
            return success(True)

        except Exception as e:
            return failure(
                app_error(
                    ErrorType.PROFILING_ERROR,
                    f"Failed to start memory tracking: {e}",
                    cause=e,
                )
            )

    def stop_tracking(self) -> Result[bool, AppError]:
        """
        Stop memory tracking.

        Returns:
            Result indicating success or failure
        """
        if not self.is_tracking:
            return success(True)

        try:
            self.is_tracking = False

            # Take final snapshot
            self._take_snapshot()

            logger.info("Stopped memory tracking")
            return success(True)

        except Exception as e:
            return failure(
                app_error(
                    ErrorType.PROFILING_ERROR,
                    f"Failed to stop memory tracking: {e}",
                    cause=e,
                )
            )

    def get_current_usage(self) -> float:
        """
        Get current memory usage in MB.

        Returns:
            Current memory usage in megabytes
        """
        try:
            # Cache process instance to reduce overhead
            if not hasattr(self, "_cached_process"):
                self._cached_process = psutil.Process()
            return self._cached_process.memory_info().rss / 1024 / 1024
        except Exception as e:
            logger.warning(f"Failed to get current memory usage: {e}")
            return 0.0

    def _take_snapshot(self):
        """Take a memory usage snapshot."""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            system_memory = psutil.virtual_memory()

            # Get garbage collection stats
            gc_stats = {}
            for i in range(3):  # Python has 3 GC generations
                gc_stats[i] = gc.get_count()[i] if i < len(gc.get_count()) else 0

            snapshot = MemorySnapshot(
                timestamp=datetime.now(),
                rss_mb=memory_info.rss / 1024 / 1024,
                vms_mb=memory_info.vms / 1024 / 1024,
                percent=process.memory_percent(),
                available_mb=system_memory.available / 1024 / 1024,
                gc_objects=len(gc.get_objects()),
                gc_collections=gc_stats,
            )

            with self._lock:
                self.snapshots.append(snapshot)

                # Keep only recent snapshots
                if len(self.snapshots) > self.max_snapshots:
                    self.snapshots = self.snapshots[-self.max_snapshots :]

            # Check for memory threshold violations
            if snapshot.rss_mb > self.config.profiling.memory_threshold_mb:
                logger.warning(
                    f"Memory usage ({snapshot.rss_mb:.1f}MB) exceeds threshold "
                    f"({self.config.profiling.memory_threshold_mb}MB)"
                )

        except Exception as e:
            logger.exception(f"Failed to take memory snapshot: {e}")

    def detect_leaks(self) -> list[MemoryLeak]:
        """
        Detect potential memory leaks.

        Returns:
            List of detected memory leaks
        """
        if len(self.snapshots) < 10:  # Need enough data points
            return []

        detected_leaks = []

        try:
            # Analyze memory growth over time
            recent_snapshots = self.snapshots[-10:]
            first_snapshot = recent_snapshots[0]
            last_snapshot = recent_snapshots[-1]

            time_period = last_snapshot.timestamp - first_snapshot.timestamp
            memory_growth = last_snapshot.rss_mb - first_snapshot.rss_mb

            # Check for significant memory growth
            if memory_growth > 50:  # 50MB growth threshold
                severity = (
                    "high"
                    if memory_growth > 200
                    else "medium" if memory_growth > 100 else "low"
                )

                leak = MemoryLeak(
                    object_type="general",
                    count_increase=int(memory_growth),
                    time_period=time_period,
                    severity=severity,
                    first_detected=first_snapshot.timestamp,
                    last_detected=last_snapshot.timestamp,
                )
                detected_leaks.append(leak)

            # Analyze GC object growth
            gc_growth = last_snapshot.gc_objects - first_snapshot.gc_objects
            if gc_growth > 10000:  # 10k objects threshold
                severity = (
                    "high"
                    if gc_growth > 50000
                    else "medium" if gc_growth > 25000 else "low"
                )

                leak = MemoryLeak(
                    object_type="python_objects",
                    count_increase=gc_growth,
                    time_period=time_period,
                    severity=severity,
                    first_detected=first_snapshot.timestamp,
                    last_detected=last_snapshot.timestamp,
                )
                detected_leaks.append(leak)

        except Exception as e:
            logger.exception(f"Failed to detect memory leaks: {e}")

        return detected_leaks

    def get_memory_summary(self) -> dict[str, Any]:
        """
        Get comprehensive memory usage summary.

        Returns:
            Dictionary containing memory usage statistics
        """
        if not self.snapshots:
            return {"error": "No memory snapshots available"}

        try:
            with self._lock:
                current_snapshot = self.snapshots[-1]

                # Calculate statistics
                rss_values = [s.rss_mb for s in self.snapshots]
                gc_object_values = [s.gc_objects for s in self.snapshots]

                summary = {
                    "current": {
                        "rss_mb": current_snapshot.rss_mb,
                        "vms_mb": current_snapshot.vms_mb,
                        "percent": current_snapshot.percent,
                        "available_mb": current_snapshot.available_mb,
                        "gc_objects": current_snapshot.gc_objects,
                    },
                    "statistics": {
                        "min_rss_mb": min(rss_values),
                        "max_rss_mb": max(rss_values),
                        "avg_rss_mb": sum(rss_values) / len(rss_values),
                        "min_gc_objects": min(gc_object_values),
                        "max_gc_objects": max(gc_object_values),
                        "avg_gc_objects": sum(gc_object_values) / len(gc_object_values),
                    },
                    "tracking": {
                        "is_active": self.is_tracking,
                        "snapshot_count": len(self.snapshots),
                        "tracking_duration": (
                            (
                                current_snapshot.timestamp - self.snapshots[0].timestamp
                            ).total_seconds()
                            if len(self.snapshots) > 1
                            else 0
                        ),
                    },
                    "leaks": [
                        {
                            "object_type": leak.object_type,
                            "count_increase": leak.count_increase,
                            "severity": leak.severity,
                            "duration_seconds": leak.time_period.total_seconds(),
                        }
                        for leak in self.detect_leaks()
                    ],
                    "recommendations": self._generate_memory_recommendations(),
                }

                return summary

        except Exception as e:
            logger.exception(f"Failed to generate memory summary: {e}")
            return {"error": f"Failed to generate summary: {e}"}

    def _generate_memory_recommendations(self) -> list[dict[str, str]]:
        """Generate memory optimization recommendations."""
        recommendations = []

        if not self.snapshots:
            return recommendations

        try:
            current_snapshot = self.snapshots[-1]

            # High memory usage
            if current_snapshot.rss_mb > self.config.profiling.memory_threshold_mb:
                recommendations.append(
                    {
                        "type": "memory_usage",
                        "issue": "High memory usage",
                        "recommendation": f"Current usage ({current_snapshot.rss_mb:.1f}MB) exceeds threshold. Consider memory optimization.",
                        "priority": "high",
                    }
                )

            # High GC object count
            if current_snapshot.gc_objects > 100000:
                recommendations.append(
                    {
                        "type": "gc_objects",
                        "issue": "High object count",
                        "recommendation": f"High number of GC objects ({current_snapshot.gc_objects}). Consider object pooling or cleanup.",
                        "priority": "medium",
                    }
                )

            # Memory leaks
            leaks = self.detect_leaks()
            for leak in leaks:
                if leak.severity in ["high", "medium"]:
                    recommendations.append(
                        {
                            "type": "memory_leak",
                            "issue": f"Potential {leak.object_type} leak",
                            "recommendation": f"Detected {leak.severity} severity leak with {leak.count_increase} increase over {leak.time_period.total_seconds():.0f}s.",
                            "priority": leak.severity,
                        }
                    )

        except Exception as e:
            logger.exception(f"Failed to generate memory recommendations: {e}")

        return recommendations

    def force_gc(self) -> dict[str, int]:
        """
        Force garbage collection and return statistics.

        Returns:
            Dictionary with GC statistics
        """
        try:
            before_objects = len(gc.get_objects())
            collected = gc.collect()
            after_objects = len(gc.get_objects())

            return {
                "objects_before": before_objects,
                "objects_after": after_objects,
                "objects_collected": before_objects - after_objects,
                "gc_collected": collected,
            }
        except Exception as e:
            logger.exception(f"Failed to force garbage collection: {e}")
            return {"error": str(e)}


# Global memory tracker instance
_global_memory_tracker: MemoryTracker | None = None


def get_memory_tracker() -> MemoryTracker:
    """Get the global memory tracker instance."""
    global _global_memory_tracker
    if _global_memory_tracker is None:
        _global_memory_tracker = MemoryTracker()
    return _global_memory_tracker


def reset_memory_tracker():
    """Reset the global memory tracker instance (mainly for testing)."""
    global _global_memory_tracker
    _global_memory_tracker = None
