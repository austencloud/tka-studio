"""
TKA Application Startup Components

This package contains focused, single-responsibility components for application startup:

- ApplicationBootstrapper: Handles initialization sequence and startup coordination
- ConfigurationManager: Manages configuration loading and validation
- QtApplicationManager: Handles Qt-specific application lifecycle

These components were extracted from main.py to improve maintainability and testability.
"""

from .application_bootstrapper import ApplicationBootstrapper
from .configuration_manager import ApplicationConfiguration, ConfigurationManager
from .qt_application_manager import QtApplicationManager

__all__ = [
    "ApplicationBootstrapper",
    "ApplicationConfiguration",
    "ConfigurationManager",
    "QtApplicationManager",
]
