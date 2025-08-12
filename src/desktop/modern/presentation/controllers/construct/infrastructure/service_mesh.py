"""
Service Mesh Implementation for ConstructTab Components

Implements service mesh pattern using existing event bus infrastructure.
Provides communication layer, circuit breaking, and observability.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
import logging
import time
from typing import Any, TypeVar

from desktop.modern.core.events.domain_events import UIStateChangedEvent
from desktop.modern.core.events.event_bus import IEventBus, get_event_bus


logger = logging.getLogger(__name__)
T = TypeVar("T")


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Circuit is open, failing fast
    HALF_OPEN = "half_open"  # Testing if service is back


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""

    failure_threshold: int = 5
    timeout_duration: float = 30.0  # seconds
    recovery_timeout: float = 60.0  # seconds
    success_threshold: int = 3  # successes needed to close circuit


@dataclass
class ServiceHealth:
    """Health status of a service."""

    is_healthy: bool = True
    last_check: float = field(default_factory=time.time)
    failure_count: int = 0
    success_count: int = 0
    error_message: str | None = None


class CircuitBreaker:
    """Circuit breaker for service fault tolerance."""

    def __init__(self, config: CircuitBreakerConfig, service_name: str):
        self.config = config
        self.service_name = service_name
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0.0
        self.logger = logging.getLogger(f"{__name__}.{service_name}")

    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                self.logger.info(
                    f"Circuit breaker for {self.service_name} is half-open"
                )
            else:
                raise CircuitBreakerOpenError(
                    f"Circuit breaker is open for {self.service_name}"
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise

    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit."""
        return time.time() - self.last_failure_time >= self.config.recovery_timeout

    def _on_success(self):
        """Handle successful operation."""
        self.failure_count = 0

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
                self.logger.info(f"Circuit breaker for {self.service_name} is closed")

    def _on_failure(self):
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            self.logger.warning(
                f"Circuit breaker for {self.service_name} is open after "
                f"{self.failure_count} failures"
            )


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open."""


class ServiceProxy:
    """Proxy that wraps service calls with service mesh features."""

    def __init__(self, target_service: Any, service_name: str, event_bus: IEventBus):
        self.target_service = target_service
        self.service_name = service_name
        self.event_bus = event_bus
        self.circuit_breaker = CircuitBreaker(CircuitBreakerConfig(), service_name)
        self.health = ServiceHealth()
        self.call_count = 0
        self.error_count = 0

    def __getattr__(self, name: str) -> Any:
        """Intercept method calls to add service mesh features."""
        if hasattr(self.target_service, name):
            original_method = getattr(self.target_service, name)

            if callable(original_method):
                return self._wrap_method(original_method, name)
            return original_method

        raise AttributeError(f"'{self.service_name}' has no attribute '{name}'")

    def _wrap_method(self, method: Callable, method_name: str) -> Callable:
        """Wrap method with service mesh features."""

        @wraps(method)
        def wrapper(*args, **kwargs):
            self.call_count += 1
            start_time = time.time()

            try:
                # Execute with circuit breaker protection
                result = self.circuit_breaker.call(method, *args, **kwargs)

                # Update health status
                self.health.is_healthy = True
                self.health.last_check = time.time()

                # Publish success metrics
                duration = time.time() - start_time
                self._publish_metrics_event(method_name, duration, success=True)

                return result

            except CircuitBreakerOpenError:
                # Circuit breaker is open, return fallback or raise
                self._publish_circuit_breaker_event("open")
                raise

            except Exception as e:
                self.error_count += 1
                self.health.is_healthy = False
                self.health.error_message = str(e)
                self.health.last_check = time.time()

                # Publish error metrics
                duration = time.time() - start_time
                self._publish_metrics_event(
                    method_name, duration, success=False, error=str(e)
                )

                raise

        return wrapper

    def _publish_metrics_event(
        self,
        method_name: str,
        duration: float,
        success: bool,
        error: str | None = None,
    ):
        """Publish service metrics through event bus."""
        event = UIStateChangedEvent(
            component=f"service_mesh.{self.service_name}",
            state_key="method_call_metrics",
            old_value=None,
            new_value={
                "method": method_name,
                "duration_ms": duration * 1000,
                "success": success,
                "error": error,
                "total_calls": self.call_count,
                "total_errors": self.error_count,
                "circuit_breaker_state": self.circuit_breaker.state.value,
            },
            source="service_mesh",
        )
        self.event_bus.publish(event)

    def _publish_circuit_breaker_event(self, state: str):
        """Publish circuit breaker state change."""
        event = UIStateChangedEvent(
            component=f"service_mesh.{self.service_name}",
            state_key="circuit_breaker_state",
            old_value=None,
            new_value=state,
            source="service_mesh",
        )
        self.event_bus.publish(event)

    def get_health(self) -> ServiceHealth:
        """Get current health status."""
        return self.health


class ServiceRegistry:
    """Registry for service discovery."""

    def __init__(self, event_bus: IEventBus):
        self.services: dict[str, ServiceProxy] = {}
        self.event_bus = event_bus

    def register(self, service_name: str, service_instance: Any) -> ServiceProxy:
        """Register a service and return wrapped proxy."""
        proxy = ServiceProxy(service_instance, service_name, self.event_bus)
        self.services[service_name] = proxy

        logger.info(f"Registered service: {service_name}")

        # Publish service registration event
        event = UIStateChangedEvent(
            component="service_mesh.registry",
            state_key="service_registered",
            old_value=None,
            new_value=service_name,
            source="service_mesh",
        )
        self.event_bus.publish(event)

        return proxy

    def get(self, service_name: str) -> ServiceProxy | None:
        """Get service proxy by name."""
        return self.services.get(service_name)

    def list_services(self) -> list[str]:
        """List all registered service names."""
        return list(self.services.keys())

    def get_health_status(self) -> dict[str, ServiceHealth]:
        """Get health status of all services."""
        return {name: proxy.get_health() for name, proxy in self.services.items()}


class ComponentServiceMesh:
    """
    Service mesh for ConstructTab component communication.

    Provides:
    - Service registration and discovery
    - Circuit breaker fault tolerance
    - Observability and metrics
    - Event-driven communication
    """

    def __init__(self, event_bus: IEventBus | None = None):
        self.event_bus = event_bus or get_event_bus()
        self.registry = ServiceRegistry(self.event_bus)
        self.logger = logging.getLogger(__name__)

    def register_component(self, component: Any, service_name: str) -> ServiceProxy:
        """Register component as a service and return mesh-enabled proxy."""
        try:
            proxy = self.registry.register(service_name, component)
            self.logger.info(f"Component {service_name} registered in service mesh")
            return proxy
        except Exception as e:
            self.logger.exception(f"Failed to register component {service_name}: {e}")
            # Return original component as fallback
            return component

    def setup_mesh_for_construct_tab(
        self, components: dict[str, Any]
    ) -> dict[str, ServiceProxy]:
        """Setup service mesh for all ConstructTab components."""
        proxied_components = {}

        component_configs = [
            ("workbench", components.get("workbench")),
            ("layout_manager", components.get("layout_manager")),
            ("option_picker", components.get("option_picker")),
            ("start_position_picker", components.get("start_position_picker")),
            ("graph_editor", components.get("graph_editor")),
            ("generate_panel", components.get("generate_panel")),
        ]

        for service_name, component in component_configs:
            if component is not None:
                proxy = self.register_component(component, service_name)
                proxied_components[service_name] = proxy

        self.logger.info(
            f"Service mesh setup complete with {len(proxied_components)} components"
        )
        return proxied_components

    def get_mesh_status(self) -> dict[str, Any]:
        """Get overall mesh status and health."""
        health_status = self.registry.get_health_status()

        return {
            "total_services": len(self.registry.services),
            "healthy_services": sum(1 for h in health_status.values() if h.is_healthy),
            "service_health": health_status,
            "service_names": self.registry.list_services(),
        }


# Factory function for easy integration
def create_construct_tab_service_mesh(
    components: dict[str, Any],
) -> ComponentServiceMesh:
    """Factory function to create and setup service mesh for ConstructTab."""
    mesh = ComponentServiceMesh()
    mesh.setup_mesh_for_construct_tab(components)
    return mesh
