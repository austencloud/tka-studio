"""
TKA Application Startup Components

This package contains focused configuration management for application startup.
"""

from __future__ import annotations

from .configuration_manager import ApplicationConfiguration, ConfigurationManager


__all__ = [
    "ApplicationConfiguration",
    "ConfigurationManager",
]
