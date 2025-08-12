"""
Performance Framework Integration

Integration points for the TKA performance framework with existing codebase components.
Provides seamless integration with DI container, Qt components, and monitoring systems.
"""

import logging
from functools import wraps
from typing import Any, Callable, Dict, Optional

from .config import get_performance_config
from .memory_tracker import get_memory_tracker

# Result pattern removed - using simple exceptions
from .profiler import get_profiler, profile
from .qt_profiler import get_qt_profiler

logger = logging.getLogger(__name__)


class PerformanceIntegration:
    """
    Central integration point for performance framework.

    Provides seamless integration with existing TKA components including:
    - DI container service resolution monitoring
    - Qt component performance tracking
    - Arrow renderer optimization monitoring
    - Memory management integration
    """

    def __init__(self):
        self.config = get_performance_config()
        self.profiler = get_profiler()
        self.qt_profiler = get_qt_profiler()
        self.memory_tracker = get_memory_tracker()
        self._integration_active = False

    def initialize(self) -> bool:
        """
        Initialize performance framework integration.

        Returns:
            True if successful
            
        Raises:
            RuntimeError: If initialization fails
        """
        if not self.config.profiling.enabled:
            logger.info("Performance profiling disabled in configuration")
            return True

        try:
            # Initialize components
            if self.config.monitoring.memory_tracking:
                try:
                    self.memory_tracker.start_tracking()
                except Exception as e:
                    logger.warning(f"Failed to start memory tracking: {e}")

            if self.config.monitoring.qt_metrics:
                try:
                    self.qt_profiler.start_profiling()
                except Exception as e:
                    logger.warning(f"Failed to start Qt profiling: {e}")

            # Integrate with existing systems
            self._integrate_with_di_container()
            self._integrate_with_arrow_renderer()
            self._integrate_with_qt_components()

            self._integration_active = True
            logger.info("Performance framework integration initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize performance integration: {e}")
            raise RuntimeError(f"Failed to initialize performance integration: {e}") from e

    def shutdown(self) -> bool:
        """
        Shutdown performance framework integration.

        Returns:
            True if successful
            
        Raises:
            RuntimeError: If shutdown fails
        """
        try:
            if not self._integration_active:
                return True

            # Stop profiling if active
            if self.profiler.is_profiling:
                self.profiler.stop_session()

            # Stop Qt profiling
            if hasattr(self.qt_profiler, "stop_profiling"):
                self.qt_profiler.stop_profiling()

            # Stop memory tracking
            if hasattr(self.memory_tracker, "stop_tracking"):
                self.memory_tracker.stop_tracking()

            self._integration_active = False
            logger.info("Performance framework integration shutdown successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to shutdown performance integration: {e}")
            raise RuntimeError(f"Failed to shutdown performance integration: {e}") from e

    def _integrate_with_di_container(self):
        """Integrate with DI container for service resolution monitoring."""
        try:
            from desktop.modern.core.dependency_injection.di_container import DIContainer

            # Monkey patch the resolve method to add profiling
            original_resolve = DIContainer.resolve

            @profile
            def profiled_resolve(self, service_type, *args, **kwargs):
                """Profiled version of DI container resolve method."""
                return original_resolve(self, service_type, *args, **kwargs)

            DIContainer.resolve = profiled_resolve
            logger.info("Integrated performance monitoring with DI container")

        except ImportError:
            logger.debug("DI container not available for integration")
        except Exception as e:
            logger.warning(f"Failed to integrate with DI container: {e}")

    def _integrate_with_arrow_renderer(self):
        """Integrate with arrow renderer for rendering performance monitoring."""
        try:
            # Try to integrate with existing arrow renderer
            from presentation.pictograph.components.arrow_renderer import ArrowRenderer

            # Monkey patch key methods
            if hasattr(ArrowRenderer, "_load_svg_file_cached"):
                original_load_svg = ArrowRenderer._load_svg_file_cached

                @profile
                def profiled_load_svg(self, *args, **kwargs):
                    """Profiled version of SVG loading."""
                    return original_load_svg(self, *args, **kwargs)

                ArrowRenderer._load_svg_file_cached = profiled_load_svg
                logger.info(
                    "Integrated performance monitoring with arrow renderer SVG loading"
                )

            if hasattr(ArrowRenderer, "render"):
                original_render = ArrowRenderer.render

                @profile
                def profiled_render(self, *args, **kwargs):
                    """Profiled version of arrow rendering."""
                    return original_render(self, *args, **kwargs)

                ArrowRenderer.render = profiled_render
                logger.info("Integrated performance monitoring with arrow rendering")

        except ImportError:
            logger.debug("Arrow renderer not available for integration")
        except Exception as e:
            logger.warning(f"Failed to integrate with arrow renderer: {e}")

    def _integrate_with_qt_components(self):
        """Integrate with Qt components for UI performance monitoring."""
        try:
            # Integration with Qt components would go here
            # This is a placeholder for Qt-specific integrations
            logger.info("Qt component integration placeholder")

        except Exception as e:
            logger.warning(f"Failed to integrate with Qt components: {e}")

    def profile_critical_path(self, path_name: str):
        """
        Decorator for profiling critical code paths.

        Args:
            path_name: Name of the critical path

        Returns:
            Decorator function
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self._integration_active:
                    return func(*args, **kwargs)

                with self.profiler.profile_block(f"critical_path_{path_name}"):
                    return func(*args, **kwargs)

            return wrapper

        return decorator

    def monitor_memory_intensive_operation(self, operation_name: str):
        """
        Decorator for monitoring memory-intensive operations.

        Args:
            operation_name: Name of the operation

        Returns:
            Decorator function
        """

        de(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self._integration_active:
                    return func(*args, **kwargs)

                # Take memory snapshot before
                memory_before = self.memory_tracker.get_current_usage()

                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    # Check memory usage after
                    memory_after = self.memory_tracker.get_current_usage()
                    memory_delta = memory_after - memory_before

                    if memory_delta > self.config.profiling.memory_threshold_mb:
                        logger.warning(
                            f"Memory-intensive operation '{operation_name}' used "
                            f"{memory_delta:.1f}MB (threshold: {self.config.profiling.memory_threshold_mb}MB)"
                        )

            return wrapper

        return decorator

    def get_performance_status(self) -> Dict[str, Any]:
        """
        Get current performance monitoring status.

        Returns:
            Dictionary containing performance status information
        """
        return {
            "integration_active": self._integration_active,
            "profiling_active": self.profiler.is_profiling,
            "qt_profiling_active": getattr(self.qt_profiler, "is_profiling", False),
            "memory_tracking_active": getattr(
                self.memory_tracker, "is_tracking", False
            ),
            "configuration": {
                "profiling_enabled": self.config.profiling.enabled,
                "monitoring_enabled": self.config.monitoring.enabled,
                "qt_metrics_enabled": self.config.monitoring.qt_metrics,
                "memory_tracking_enabled": self.config.monitoring.memory_tracking,
            },
            "current_session": {
                "session_id": (
                    self.profiler.current_session.session_id
                    if self.profiler.current_session
                    else None
                ),
                "start_time": (
                    self.profiler.current_session.start_time.isoformat()
                    if self.profiler.current_session
                    else None
                ),
                "function_count": len(self.profiler._function_stats),
            },
        }

    def start_performance_session(
        self, session_name: Optional[str] = None
    ) -> Result[str, AppError]:
        """
        Start a comprehensive performance monitoring session.

        Args:
            session_name: Optional name for the session

        Returns:
            Result containing session ID or error
        """
        if not self._integration_active:
            return failure(
                app_error(
                    ErrorType.CONFIGURATION_ERROR, "Performance integration not active"
                )
            )

        # Start profiling session
        result = self.profiler.start_session(session_name)
        if result.is_failure():
            return result

        session_id = result.value

        # Start Qt profiling if enabled
        if self.config.monitoring.qt_metrics and hasattr(
            self.qt_profiler, "start_profiling"
        ):
            qt_result = self.qt_profiler.start_profiling()
            if qt_result.is_failure():
                logger.warning(f"Failed to start Qt profiling: {qt_result.error}")

        # Start memory tracking if enabled
        if self.config.monitoring.memory_tracking and hasattr(
            self.memory_tracker, "start_tracking"
        ):
            memory_result = self.memory_tracker.start_tracking()
            if memory_result.is_failure():
                logger.warning(
                    f"Failed to start memory tracking: {memory_result.error}"
                )

        logger.info(f"Started comprehensive performance session: {session_id}")
        return success(session_id)

    def stop_performance_session(self) -> Result[Optional[Dict[str, Any]], AppError]:
        """
        Stop the current performance monitoring session.

        Returns:
            Result containing session data or error
        """
        if not self._integration_active:
            return failure(
                app_error(
                    ErrorType.CONFIGURATION_ERROR, "Performance integration not active"
                )
            )

        # Stop profiling session
        result = self.profiler.stop_session()
        if result.is_failure():
            return result

        session_data = result.value

        # Stop Qt profiling
        if hasattr(self.qt_profiler, "stop_profiling"):
            qt_result = self.qt_profiler.stop_profiling()
            if qt_result.is_failure():
                logger.warning(f"Failed to stop Qt profiling: {qt_result.error}")

        # Stop memory tracking
        if hasattr(self.memory_tracker, "stop_tracking"):
            memory_result = self.memory_tracker.stop_tracking()
            if memory_result.is_failure():
                logger.warning(f"Failed to stop memory tracking: {memory_result.error}")

        if session_data:
            # Enhance session data with additional information
            enhanced_data = {
                "session": session_data,
                "qt_performance": (
                    self.qt_profiler.get_qt_performance_summary()
                    if hasattr(self.qt_profiler, "get_qt_performance_summary")
                    else {}
                ),
                "memory_summary": (
                    self.memory_tracker.get_memory_summary()
                    if hasattr(self.memory_tracker, "get_memory_summary")
                    else {}
                ),
                "performance_recommendations": self._generate_session_recommendations(
                    session_data
                ),
            }

            logger.info(
                f"Stopped comprehensive performance session: {session_data.session_id}"
            )
            return success(enhanced_data)

        return success(None)

    def _generate_session_recommendations(self, session_data) -> list:
        """Generate recommendations based on session data."""
        recommendations = []

        try:
            # Analyze function performance
            for func_name, metrics in session_data.function_metrics.items():
                if metrics.avg_time > 0.1:  # 100ms threshold
                    recommendations.append(
                        {
                            "type": "performance",
                            "priority": "high" if metrics.avg_time > 0.5 else "medium",
                            "function": func_name,
                            "issue": f"High execution time ({metrics.avg_time*1000:.1f}ms average)",
                            "recommendation": "Consider optimization, caching, or background processing",
                        }
                    )

                if metrics.memory_avg > 50:  # 50MB threshold
                    recommendations.append(
                        {
                            "type": "memory",
                            "priority": "medium",
                            "function": func_name,
                            "issue": f"High memory usage ({metrics.memory_avg:.1f}MB average)",
                            "recommendation": "Consider memory optimization or object pooling",
                        }
                    )

        except Exception as e:
            logger.warning(f"Failed to generate session recommendations: {e}")

        return recommendations


# Global integration instance
_global_integration: Optional[PerformanceIntegration] = None


def get_performance_integration() -> PerformanceIntegration:
    """Get the global performance integration instance."""
    global _global_integration
    if _global_integration is None:
        _global_integration = PerformanceIntegration()
    return _global_integration


def initialize_performance_framework() -> Result[bool, AppError]:
    """Initialize the performance framework integration."""
    integration = get_performance_integration()
    return integration.initialize()


def shutdown_performance_framework() -> Result[bool, AppError]:
    """Shutdown the performance framework integration."""
    integration = get_performance_integration()
    return integration.shutdown()


# Convenience decorators for common use cases
def profile_critical_path(path_name: str):
    """Decorator for profiling critical code paths."""
    integration = get_performance_integration()
    return integration.profile_critical_path(path_name)


def monitor_memory_intensive(operation_name: str):
    """Decorator for monitoring memory-intensive operations."""
    integration = get_performance_integration()
    return integration.monitor_memory_intensive_operation(operation_name)


def reset_performance_integration():
    """Reset the global integration instance (mainly for testing)."""
    global _global_integration
    _global_integration = None
