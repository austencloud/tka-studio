"""
Modern Core Interfaces Module

Exports all interface definitions for dependency injection and service contracts.
"""

# Background interfaces
from .background_interfaces import *

# Core service interfaces
from .core_services import (
    IArrowManagementService,
    ILayoutService,
    IObjectPoolService,
    IPictographBorderManager,
    IPictographContextDetector,
    IPictographManager,
    ISequenceDataService,
    ISequenceManager,
    ISettingsCoordinator,
    IUIStateManagementService,
    IUIStateManager,
    IValidationService,
)

# Generation service interfaces
from .generation_services import *

# Option picker interfaces
from .option_picker_interfaces import *

# Organization service interfaces
from .organization_services import *

# Positioning service interfaces
from .positioning_services import *

# Session service interfaces
from .session_services import *

# Settings interfaces
from .settings_interfaces import *

# Tab settings interfaces
from .tab_settings_interfaces import (
    IBeatLayoutService,
    IImageExporter,
    IPropTypeSettingsManager,
    IUserProfileService,
    IVisibilityService,
    IVisibilitySettingsManager,
)

# Workbench service interfaces
from .workbench_services import *

__all__ = [
    # Core services
    "ILayoutService",
    "ISettingsCoordinator",
    "ISequenceDataService",
    "IValidationService",
    "IArrowManagementService",
    "ISequenceManager",
    "IPictographManager",
    "IUIStateManager",
    "IUIStateManagementService",
    "IPictographContextDetector",
    "IPictographBorderManager",
    "IObjectPoolManager",
    "IObjectPoolService",
    # Tab settings
    "IUserProfileService",
    "IPropTypeSettingsManager",
    "IVisibilityService",
    "IVisibilitySettingsManager",
    "IBeatLayoutService",
    "IImageExporter",
]
