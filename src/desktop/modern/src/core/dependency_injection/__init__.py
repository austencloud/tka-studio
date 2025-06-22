"""
Dependency injection system for TKA.

REFACTORED ARCHITECTURE: The DI system has been broken down into focused modules:
- ServiceRegistry: Handles all service registrations
- ServiceResolvers: Strategy pattern for service resolution
- LifecycleManager: Service lifecycle and cleanup management
- ValidationEngine: Comprehensive dependency validation
- DebuggingTools: Debugging and analysis capabilities
- DIContainer: Main coordinator that uses all modules

This provides better maintainability, testability, and separation of concerns.
"""

from .di_container import DIContainer, get_container, reset_container
from .service_registry import ServiceRegistry, ServiceScope, ServiceDescriptor
from .service_resolvers import ResolverChain, LazyProxy, IServiceResolver
from .lifecycle_manager import LifecycleManager
from .validation_engine import ValidationEngine
from .debugging_tools import DebuggingTools

__all__ = [
    # Main container
    "DIContainer",
    "get_container",
    "reset_container",
    # Focused modules
    "ServiceRegistry",
    "ServiceScope",
    "ServiceDescriptor",
    "ResolverChain",
    "LazyProxy",
    "IServiceResolver",
    "LifecycleManager",
    "ValidationEngine",
    "DebuggingTools",
]
