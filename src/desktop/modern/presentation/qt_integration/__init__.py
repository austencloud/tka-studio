"""
TKA Desktop Qt Integration Module

A+ Enhancement: Comprehensive Qt integration with version detection,
automatic lifecycle management, resource pooling, and memory leak prevention.

ARCHITECTURE: Provides enterprise-grade Qt integration patterns including:
- Qt Version Detection and Compatibility Layer
- Automatic Object Lifecycle Management
- Qt Resource Pooling for Performance
- Smart Pointer Management for Qt Objects
- Memory Leak Detection and Prevention
- Threading Bridge for Async/Await Support

EXPORTS:
- QtCompatibilityManager: Qt version detection and adaptation
- AutoManagedWidget: Smart widget base with automatic cleanup
- QtResourceManager: Resource pooling for expensive Qt objects
- QtMemoryLeakDetector: Automatic memory leak detection
- SmartQtPointer: Smart pointer for Qt object management
- QtAsyncBridge: Threading bridge for async operations
"""

# Qt Compatibility Layer
# Automatic Lifecycle Management
from __future__ import annotations

from .lifecycle_management import (
    AutoManagedWidget,
    QtObjectFactory,
    qt_factory,
)

# Memory Management
from .memory_management import (
    LeakReport,
    MemorySnapshot,
    QtMemoryLeakDetector,
    SmartQtPointer,
    memory_detector,
)
from .qt_compatibility import (
    QtCompatibilityManager,
    QtEnvironment,
    QtVariant,
    QtVersion,
    qt_compat,
)

# Resource Management
from .resource_management import (
    PooledResource,
    QtResourceManager,
    ResourcePool,
    pooled_brush,
    pooled_font,
    pooled_pen,
    qt_resources,
)

# Threading Integration
from .threading_integration import (
    AsyncQtWidget,
    QtAsyncBridge,
    qt_async_bridge,
)


__all__ = [
    "AsyncQtWidget",
    # Lifecycle Management
    "AutoManagedWidget",
    "LeakReport",
    "MemorySnapshot",
    "PooledResource",
    # Threading Integration
    "QtAsyncBridge",
    # Compatibility
    "QtCompatibilityManager",
    "QtEnvironment",
    # Memory Management
    "QtMemoryLeakDetector",
    "QtObjectFactory",
    # Resource Management
    "QtResourceManager",
    "QtVariant",
    "QtVersion",
    "ResourcePool",
    "SmartQtPointer",
    "memory_detector",
    "pooled_brush",
    "pooled_font",
    "pooled_pen",
    "qt_async_bridge",
    "qt_compat",
    "qt_factory",
    "qt_resources",
]
