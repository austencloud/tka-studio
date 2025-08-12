"""
Performance Infrastructure

Infrastructure components for the TKA performance framework including
data storage, API endpoints, dashboard, and external integrations.

COMPONENTS:
- storage: Performance data persistence and retrieval
- api: REST API endpoints for performance data
- dashboard: Web-based performance monitoring interface
- exporters: Data export in various formats

INTEGRATION:
- Follows existing infrastructure patterns
- Uses Result types for error handling
- Integrates with existing configuration system
- Provides foundation for external monitoring tools
"""
from __future__ import annotations

from .api import PerformanceAPI
from .storage import PerformanceStorage, get_performance_storage


__all__ = [
    # API
    "PerformanceAPI",
    # Storage
    "PerformanceStorage",
    "get_performance_storage",
]
