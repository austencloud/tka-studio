"""
Modern Infrastructure Patterns for ConstructTab Microservices

This package implements 2024-2025 microservices infrastructure patterns:
- Event-Driven Architecture
- Service Mesh Pattern
- Saga Pattern
- Circuit Breaker Pattern
- Distributed Observability
"""

from .circuit_breaker import CircuitBreaker, CircuitBreakerConfig
from .event_bus import ConstructTabEventBus, DomainEvent
from .health_monitor import HealthMonitor
from .metrics_collector import MetricsCollector
from .service_mesh import ComponentServiceMesh, ServiceProxy

__all__ = [
    "ConstructTabEventBus",
    "DomainEvent",
    "ComponentServiceMesh",
    "ServiceProxy",
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "HealthMonitor",
    "MetricsCollector",
]
