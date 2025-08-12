"""
Modern Settings Services Package

This package provides modern state persistence services for the TKA application
following clean architecture principles and CQRS patterns.

Services included:
- ModernSettingsService: Main service with CQRS and Memento patterns
- BackgroundSettingsManager: Background type management
- VisibilitySettingsManager: UI element visibility control
- BeatLayoutSettingsManager: Sequence layout management
- PropTypeSettingsManager: Prop type selection and management
- UserProfileSettingsManager: Multi-user profile support
- ImageExportSettingsManager: Export format and quality settings

Usage:
    # Using dependency injection (recommended)
    from desktop.modern.core.dependency_injection.settings_service_registration import (
        create_configured_settings_container
    )

    container = create_configured_settings_container()
    settings_service = container.resolve(ModernSettingsService)

    # Direct instantiation (for testing)
    from desktop.modern.application.services.settings.modern_settings_service import ModernSettingsService
    from desktop.modern.application.services.core.session_state_tracker import SessionStateTracker

    session_tracker = SessionStateTracker(ui_state_manager, file_system_service)
    settings_service = ModernSettingsService(session_tracker)
"""

# Import main services for easy access
from __future__ import annotations

from .background_settings_manager import BackgroundSettingsManager
from .beat_layout_settings_manager import BeatLayoutSettingsManager
from .image_export_settings_manager import ImageExportSettingsManager
from .modern_settings_service import ApplicationStateMemento, ModernSettingsService
from .prop_type_settings_manager import PropTypeSettingsManager
from .user_profile_settings_manager import UserProfileSettingsManager
from .visibility_settings_manager import VisibilitySettingsManager


__all__ = [
    "ApplicationStateMemento",
    "BackgroundSettingsManager",
    "BeatLayoutSettingsManager",
    "ImageExportSettingsManager",
    "ModernSettingsService",
    "PropTypeSettingsManager",
    "UserProfileSettingsManager",
    "VisibilitySettingsManager",
]

__version__ = "1.0.0"
__author__ = "TKA Development Team"
__description__ = "Modern state persistence services with CQRS and clean architecture"
