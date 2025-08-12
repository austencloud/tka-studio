"""
Debugging Tools - Dependency Injection Debugging and Analysis

Provides:
- Dependency graph generation
- Service registration analysis
- Resolution path tracing
- Performance metrics
- Diagnostic information
"""

from __future__ import annotations

from datetime import datetime
import inspect
import logging
from typing import Any, get_type_hints


logger = logging.getLogger(__name__)


class DebuggingTools:
    """
    Comprehensive debugging and analysis tools for the DI container.

    Provides detailed insights into service registrations, dependency graphs,
    and resolution patterns for troubleshooting and optimization.
    """

    def __init__(self):
        self._resolution_history: list[dict[str, Any]] = []
        self._performance_metrics: dict[str, Any] = {}

    def get_dependency_graph(self, registry: Any) -> dict[str, list[str]]:
        """
        Generate dependency graph for debugging.

        Returns:
            Dictionary mapping service names to their dependencies
        """
        graph = {}
        all_registrations = registry.get_all_registrations()

        # Analyze singleton services
        for interface, implementation in all_registrations.items():
            if registry.has_service_registration(interface):
                dependencies = self._get_service_dependencies(implementation)
                graph[f"{interface.__name__} -> {implementation.__name__}"] = [
                    dep.__name__ for dep in dependencies
                ]

        # Analyze transient services
        for interface in all_registrations:
            if registry.has_factory_registration(interface):
                implementation = registry.get_factory_or_implementation(interface)
                if inspect.isclass(implementation):
                    dependencies = self._get_service_dependencies(implementation)
                    graph[
                        f"{interface.__name__} -> {implementation.__name__} (transient)"
                    ] = [dep.__name__ for dep in dependencies]

        return graph

    def _get_service_dependencies(self, implementation: type) -> list[type]:
        """Get list of dependencies for a service implementation."""
        dependencies = []

        try:
            signature = inspect.signature(implementation.__init__)
            type_hints = get_type_hints(implementation.__init__)

            for param_name, param in signature.parameters.items():
                if param_name == "self":
                    continue

                param_type = type_hints.get(param_name, param.annotation)

                # Skip primitive types, optional parameters, and special parameters
                if (
                    param_type == inspect.Parameter.empty
                    or param_type == inspect._empty
                    or str(param_type) == "_empty"
                    or self._is_primitive_type(param_type)
                    or param.default != inspect.Parameter.empty
                    or param.kind
                    in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
                ):
                    continue

                dependencies.append(param_type)

        except Exception:
            # If we can't analyze dependencies, return empty list
            pass

        return dependencies

    def _is_primitive_type(self, param_type: type) -> bool:
        """Check if a type is a primitive type."""
        from datetime import datetime, timedelta
        from pathlib import Path
        from typing import Union

        primitive_types = {
            str,
            int,
            float,
            bool,
            bytes,
            type(None),
            list,
            dict,
            tuple,
            set,
            frozenset,
            Path,
            datetime,
            timedelta,
        }

        if hasattr(param_type, "__origin__"):
            origin = param_type.__origin__
            if origin is Union:
                args = getattr(param_type, "__args__", ())
                if len(args) == 2 and type(None) in args:
                    non_none_type = next(arg for arg in args if arg is not type(None))
                    return self._is_primitive_type(non_none_type)
                return all(arg in primitive_types for arg in args)
            if origin in primitive_types:
                return True

        if hasattr(param_type, "__module__") and param_type.__module__ == "builtins":
            return True

        return param_type in primitive_types

    def analyze_service_registrations(self, registry: Any) -> dict[str, Any]:
        """Analyze service registrations and provide detailed statistics."""
        all_registrations = registry.get_all_registrations()

        analysis = {
            "total_services": len(all_registrations),
            "singleton_services": 0,
            "transient_services": 0,
            "instance_services": 0,
            "services_by_module": {},
            "dependency_counts": {},
            "circular_dependencies": [],
            "orphaned_services": [],
        }

        # Count service types
        for interface in all_registrations:
            if registry.has_service_registration(interface):
                analysis["singleton_services"] += 1
            elif registry.has_factory_registration(interface):
                analysis["transient_services"] += 1
            elif registry.has_singleton_instance(interface):
                analysis["instance_services"] += 1

        # Analyze by module
        for interface, implementation in all_registrations.items():
            module_name = getattr(implementation, "__module__", "unknown")
            if module_name not in analysis["services_by_module"]:
                analysis["services_by_module"][module_name] = 0
            analysis["services_by_module"][module_name] += 1

        # Analyze dependency counts
        for interface, implementation in all_registrations.items():
            if inspect.isclass(implementation):
                deps = self._get_service_dependencies(implementation)
                analysis["dependency_counts"][interface.__name__] = len(deps)

        return analysis

    def trace_resolution_path(self, service_type: type, registry: Any) -> list[str]:
        """Trace the resolution path for a service type."""
        path = []
        visited = set()

        def _trace_recursive(current_type: type, depth: int = 0):
            if current_type in visited:
                path.append(f"{'  ' * depth}CIRCULAR: {current_type.__name__}")
                return

            visited.add(current_type)
            path.append(f"{'  ' * depth}{current_type.__name__}")

            implementation = registry.get_service_implementation(current_type)
            if implementation and inspect.isclass(implementation):
                dependencies = self._get_service_dependencies(implementation)
                for dep in dependencies:
                    _trace_recursive(dep, depth + 1)

        _trace_recursive(service_type)
        return path

    def record_resolution(
        self, service_type: type, resolution_time: float, success: bool
    ) -> None:
        """Record a service resolution for performance analysis."""
        self._resolution_history.append(
            {
                "service_type": service_type.__name__,
                "resolution_time": resolution_time,
                "success": success,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Keep only last 1000 resolutions
        if len(self._resolution_history) > 1000:
            self._resolution_history = self._resolution_history[-1000:]

    def get_performance_metrics(self) -> dict[str, Any]:
        """Get performance metrics for service resolution."""
        if not self._resolution_history:
            return {"message": "No resolution history available"}

        successful_resolutions = [r for r in self._resolution_history if r["success"]]
        failed_resolutions = [r for r in self._resolution_history if not r["success"]]

        if successful_resolutions:
            resolution_times = [r["resolution_time"] for r in successful_resolutions]
            avg_time = sum(resolution_times) / len(resolution_times)
            max_time = max(resolution_times)
            min_time = min(resolution_times)
        else:
            avg_time = max_time = min_time = 0

        return {
            "total_resolutions": len(self._resolution_history),
            "successful_resolutions": len(successful_resolutions),
            "failed_resolutions": len(failed_resolutions),
            "success_rate": len(successful_resolutions)
            / len(self._resolution_history)
            * 100,
            "average_resolution_time": avg_time,
            "max_resolution_time": max_time,
            "min_resolution_time": min_time,
            "most_resolved_services": self._get_most_resolved_services(),
        }

    def _get_most_resolved_services(self) -> list[dict[str, Any]]:
        """Get the most frequently resolved services."""
        service_counts = {}
        for resolution in self._resolution_history:
            service_name = resolution["service_type"]
            service_counts[service_name] = service_counts.get(service_name, 0) + 1

        # Sort by count and return top 10
        sorted_services = sorted(
            service_counts.items(), key=lambda x: x[1], reverse=True
        )
        return [
            {"service": name, "count": count} for name, count in sorted_services[:10]
        ]

    def find_potential_issues(self, registry: Any) -> list[dict[str, Any]]:
        """Find potential issues in the DI configuration."""
        issues = []
        all_registrations = registry.get_all_registrations()

        # Check for services with many dependencies
        for interface, implementation in all_registrations.items():
            if inspect.isclass(implementation):
                deps = self._get_service_dependencies(implementation)
                if len(deps) > 10:
                    issues.append(
                        {
                            "type": "high_dependency_count",
                            "service": interface.__name__,
                            "dependency_count": len(deps),
                            "message": f"Service {interface.__name__} has {len(deps)} dependencies",
                        }
                    )

        # Check for unused services (services that are registered but never used as dependencies)
        used_services = set()
        for interface, implementation in all_registrations.items():
            if inspect.isclass(implementation):
                deps = self._get_service_dependencies(implementation)
                used_services.update(deps)

        for interface in all_registrations:
            if interface not in used_services:
                issues.append(
                    {
                        "type": "potentially_unused",
                        "service": interface.__name__,
                        "message": f"Service {interface.__name__} is registered but not used as a dependency",
                    }
                )

        return issues

    def generate_diagnostic_report(
        self, registry: Any, lifecycle_manager: Any = None
    ) -> str:
        """Generate a comprehensive diagnostic report."""
        analysis = self.analyze_service_registrations(registry)
        performance = self.get_performance_metrics()
        issues = self.find_potential_issues(registry)

        report = []
        report.append("=== DI Container Diagnostic Report ===")
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")

        # Service registration summary
        report.append("Service Registration Summary:")
        report.append(f"  Total Services: {analysis['total_services']}")
        report.append(f"  Singleton Services: {analysis['singleton_services']}")
        report.append(f"  Transient Services: {analysis['transient_services']}")
        report.append(f"  Instance Services: {analysis['instance_services']}")
        report.append("")

        # Performance metrics
        if isinstance(performance, dict) and "total_resolutions" in performance:
            report.append("Performance Metrics:")
            report.append(f"  Total Resolutions: {performance['total_resolutions']}")
            report.append(f"  Success Rate: {performance['success_rate']:.1f}%")
            report.append(
                f"  Average Resolution Time: {performance['average_resolution_time']:.4f}s"
            )
            report.append("")

        # Lifecycle information
        if lifecycle_manager:
            stats = lifecycle_manager.get_lifecycle_stats()
            report.append("Lifecycle Information:")
            report.append(f"  Cleanup Handlers: {stats['cleanup_handlers']}")
            report.append(f"  Initialized Services: {stats['initialized_services']}")
            report.append(f"  Active Scopes: {stats['active_scopes']}")
            report.append("")

        # Issues
        if issues:
            report.append("Potential Issues:")
            for issue in issues[:10]:  # Show top 10 issues
                report.append(f"  - {issue['message']}")
            report.append("")

        return "\n".join(report)

    def clear_history(self) -> None:
        """Clear resolution history and metrics."""
        self._resolution_history.clear()
        self._performance_metrics.clear()
        logger.debug("Debugging history cleared")
