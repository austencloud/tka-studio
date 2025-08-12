"""
PyQt6-Specific Performance Profiler

Specialized profiler for PyQt6 applications that monitors:
- Event loop performance
- Signal/slot overhead
- Paint operations
- Graphics scene performance
- QObject lifecycle

Integrates with existing Qt integration layer and follows TKA patterns.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import logging
import time
from typing import Any
import weakref


try:
    from PyQt6.QtCore import QEvent, QObject, pyqtSignal
    from PyQt6.QtWidgets import QApplication

    QT_AVAILABLE = True
except ImportError:
    # Fallback for environments without PyQt6
    QT_AVAILABLE = False
    QObject = object
    QEvent = object
    def pyqtSignal():
        return None

from .config import PerformanceConfig, get_performance_config

# Result pattern removed - using simple exceptions
from .metrics import QtEventMetrics


logger = logging.getLogger(__name__)


@dataclass
class QtObjectMetrics:
    """Metrics for Qt object lifecycle."""

    object_type: str
    created_count: int = 0
    destroyed_count: int = 0
    active_count: int = 0
    peak_count: int = 0
    creation_times: list[float] = field(default_factory=list)


@dataclass
class SignalSlotMetrics:
    """Metrics for signal/slot connections."""

    signal_name: str
    slot_name: str
    call_count: int = 0
    total_time: float = 0.0
    avg_time: float = 0.0


class QtProfiler(QObject if QT_AVAILABLE else object):
    """
    Advanced Qt-specific profiler for monitoring PyQt6 performance.

    Monitors:
    - Event loop processing times
    - Paint operations and graphics performance
    - Signal/slot emission and connection overhead
    - QObject creation/destruction patterns
    - Memory usage of Qt objects

    Integrates with existing Qt integration layer for seamless operation.
    """

    def __init__(
        self,
        parent: QObject | None = None,
        config: PerformanceConfig | None = None,
    ):
        if QT_AVAILABLE:
            super().__init__(parent)

        self.config = config or get_performance_config()
        self.is_profiling = False

        # Metrics storage
        self.event_metrics: dict[str, QtEventMetrics] = {}
        self.signal_slot_metrics: dict[str, SignalSlotMetrics] = {}
        self.paint_metrics: dict[str, dict[str, Any]] = {}
        self.object_metrics: dict[str, QtObjectMetrics] = {}

        # Qt object tracking
        self.tracked_objects: set[weakref.ref] = set()
        self.object_creation_times: dict[int, float] = {}

        # Event filtering
        self.original_event_filter: Any | None = None
        self._event_filter_installed = False

        # Integration with existing Qt integration
        self._integrate_with_qt_layer()

    def _integrate_with_qt_layer(self):
        """Integrate with existing Qt integration layer."""
        try:
            from presentation.qt_integration import qt_resources

            # Hook into existing resource management if available
            if hasattr(qt_resources(), "_creation_stats"):
                logger.info("Integrated with existing Qt resource management")
        except ImportError:
            logger.debug("Qt integration layer not available")

    def start_profiling(self) -> Result[bool, AppError]:
        """
        Start Qt-specific profiling.

        Returns:
            Result indicating success or failure
        """
        if not QT_AVAILABLE:
            return failure(
                app_error(
                    ErrorType.CONFIG_ERROR, "PyQt6 not available for Qt profiling"
                )
            )

        if not self.config.monitoring.qt_metrics:
            return failure(
                app_error(
                    ErrorType.CONFIG_ERROR, "Qt metrics disabled in configuration"
                )
            )

        if self.is_profiling:
            return success(True)

        try:
            self.is_profiling = True

            # Install global event filter
            app = QApplication.instance()
            if app and not self._event_filter_installed:
                app.installEventFilter(self)
                self._event_filter_installed = True

            # Start object tracking
            self._start_object_tracking()

            logger.info("Started Qt-specific profiling")
            return success(True)

        except Exception as e:
            return failure(
                app_error(
                    ErrorType.PROFILING_ERROR,
                    f"Failed to start Qt profiling: {e}",
                    cause=e,
                )
            )

    def stop_profiling(self) -> Result[bool, AppError]:
        """
        Stop Qt-specific profiling.

        Returns:
            Result indicating success or failure
        """
        if not self.is_profiling:
            return success(True)

        try:
            self.is_profiling = False

            # Remove event filter
            app = QApplication.instance()
            if app and self._event_filter_installed:
                app.removeEventFilter(self)
                self._event_filter_installed = False

            # Clean up hooks
            self._cleanup_hooks()

            logger.info("Stopped Qt-specific profiling")
            return success(True)

        except Exception as e:
            return failure(
                app_error(
                    ErrorType.PROFILING_ERROR,
                    f"Failed to stop Qt profiling: {e}",
                    cause=e,
                )
            )

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """Global event filter to monitor all Qt events."""
        if not self.is_profiling or not QT_AVAILABLE:
            return False

        event_type_name = self._get_event_type_name(event.type())
        start_time = time.perf_counter()

        # Process the event normally
        result = (
            super().eventFilter(obj, event)
            if hasattr(super(), "eventFilter")
            else False
        )

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        # Record metrics
        self._record_event_metrics(event_type_name, execution_time)

        # Special handling for paint events
        if hasattr(event, "type") and "Paint" in event_type_name:
            self._record_paint_metrics(obj, execution_time)

        return result

    def _get_event_type_name(self, event_type) -> str:
        """Get human-readable event type name."""
        if not QT_AVAILABLE:
            return "Unknown"

        try:
            # Try to get the name from QEvent.Type enum
            return event_type.name if hasattr(event_type, "name") else str(event_type)
        except Exception:
            return str(event_type)

    def _record_event_metrics(self, event_type: str, execution_time: float):
        """Record metrics for Qt events."""
        if event_type not in self.event_metrics:
            self.event_metrics[event_type] = QtEventMetrics(event_type=event_type)

        metrics = self.event_metrics[event_type]
        metrics.count += 1
        metrics.total_time += execution_time
        metrics.avg_time = metrics.total_time / metrics.count
        metrics.max_time = max(metrics.max_time, execution_time)

    def _record_paint_metrics(self, obj: QObject, execution_time: float):
        """Record metrics for paint operations."""
        class_name = obj.__class__.__name__

        if class_name not in self.paint_metrics:
            self.paint_metrics[class_name] = {
                "count": 0,
                "total_time": 0.0,
                "avg_time": 0.0,
                "max_time": 0.0,
            }

        metrics = self.paint_metrics[class_name]
        metrics["count"] += 1
        metrics["total_time"] += execution_time
        metrics["avg_time"] = metrics["total_time"] / metrics["count"]
        metrics["max_time"] = max(metrics["max_time"], execution_time)

    def _start_object_tracking(self):
        """Start tracking QObject creation and destruction."""
        if not QT_AVAILABLE:
            return

        # This would require more advanced Qt integration
        # For now, we'll track basic object metrics
        logger.debug("Started Qt object tracking")

    def _cleanup_hooks(self):
        """Clean up all installed hooks."""
        # Clean up any installed hooks
        self.tracked_objects.clear()
        self.object_creation_times.clear()

    def get_qt_performance_summary(self) -> dict[str, Any]:
        """Get comprehensive Qt performance summary."""
        return {
            "event_performance": {
                event_type: {
                    "count": metrics.count,
                    "total_time": metrics.total_time,
                    "avg_time": metrics.avg_time,
                    "max_time": metrics.max_time,
                }
                for event_type, metrics in self.event_metrics.items()
            },
            "paint_performance": {
                class_name: {
                    "count": metrics["count"],
                    "total_time": metrics["total_time"],
                    "avg_time": metrics["avg_time"],
                    "max_time": metrics["max_time"],
                }
                for class_name, metrics in self.paint_metrics.items()
            },
            "signal_slot_performance": {
                f"{metrics.signal_name}->{metrics.slot_name}": {
                    "call_count": metrics.call_count,
                    "total_time": metrics.total_time,
                    "avg_time": metrics.avg_time,
                }
                for metrics in self.signal_slot_metrics.values()
            },
            "object_lifecycle": {
                obj_type: {
                    "created": metrics.created_count,
                    "destroyed": metrics.destroyed_count,
                    "active": metrics.active_count,
                    "peak": metrics.peak_count,
                }
                for obj_type, metrics in self.object_metrics.items()
            },
            "recommendations": self._generate_qt_recommendations(),
        }

    def _generate_qt_recommendations(self) -> list[dict[str, str]]:
        """Generate Qt-specific optimization recommendations."""
        recommendations = []

        # Analyze event performance
        for event_type, metrics in self.event_metrics.items():
            if metrics.avg_time > 0.016:  # 16ms (60fps threshold)
                recommendations.append(
                    {
                        "type": "qt_event",
                        "issue": f"Slow {event_type} events",
                        "recommendation": f"Average {event_type} processing takes {metrics.avg_time*1000:.1f}ms. Consider optimizing event handlers.",
                        "priority": "high" if metrics.avg_time > 0.033 else "medium",
                    }
                )

        # Analyze paint performance
        for class_name, metrics in self.paint_metrics.items():
            if metrics["avg_time"] > 0.016:  # 16ms threshold
                recommendations.append(
                    {
                        "type": "qt_paint",
                        "issue": f"Slow paint operations in {class_name}",
                        "recommendation": f"Paint operations average {metrics['avg_time']*1000:.1f}ms. Consider caching, reducing complexity, or using QPixmapCache.",
                        "priority": "high",
                    }
                )

        return recommendations


# Global Qt profiler instance
_global_qt_profiler: QtProfiler | None = None


def get_qt_profiler() -> QtProfiler:
    """Get the global Qt profiler instance."""
    global _global_qt_profiler
    if _global_qt_profiler is None:
        _global_qt_profiler = QtProfiler()
    return _global_qt_profiler


def reset_qt_profiler():
    """Reset the global Qt profiler instance (mainly for testing)."""
    global _global_qt_profiler
    _global_qt_profiler = None
