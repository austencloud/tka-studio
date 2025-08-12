"""
Modern Core Interfaces Module

Exports all interface definitions for dependency injection and service contracts.
"""

# Background interfaces
from __future__ import annotations

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

# Layout service interfaces
from .layout_services import (
    IBeatLayoutCalculator,
    IBeatResizer,
    IComponentPositionCalculator,
    IComponentSizer,
    IDimensionCalculator,
    IResponsiveScalingCalculator,
)

# Motion service interfaces
from .motion_services import (
    IOrientationCalculator,
    ITurnIntensityManager,
    ITurnIntensityManagerFactory,
)

# Option picker interfaces
from .option_picker_interfaces import *

# Organization service interfaces
from .organization_services import *

# Pictograph service interfaces
from .pictograph_services import (
    IPictographValidator,
    RenderingContext,
)

# Positioning service interfaces
from .positioning_services import *

# Session service interfaces
from .session_services import *

# Settings service interfaces
from .settings_services import (
    IBackgroundSettingsManager,
    IBeatLayoutSettingsManager,
    IImageExportSettingsManager,
    IPropTypeSettingsManager,
    IUserProfileSettingsManager,
    IVisibilitySettingsManager,
)

# Tab settings interfaces
from .tab_settings_interfaces import (
    IBeatLayoutService,
    IImageExporter,
    IPropTypeSettingsManager,
    IUserProfileService,
    IVisibilityService,
    IVisibilitySettingsManager,
)
from .workbench_export_services import (
    IWorkbenchClipboardService,
    IWorkbenchExportService,
)

# Workbench service interfaces
from .workbench_services import *


__all__ = [
    "IArrowManagementService",
    # Settings services
    "IBackgroundSettingsManager",
    # Layout services
    "IBeatLayoutCalculator",
    "IBeatLayoutService",
    "IBeatLayoutSettingsManager",
    "IBeatResizer",
    "IComponentPositionCalculator",
    "IComponentSizer",
    "IDimensionCalculator",
    "IImageExportSettingsManager",
    "IImageExporter",
    # Core services
    "ILayoutService",
    "IObjectPoolManager",
    "IObjectPoolService",
    # Motion services
    "IOrientationCalculator",
    "IPictographBorderManager",
    "IPictographContextDetector",
    "IPictographManager",
    # Pictograph services
    "IPictographValidator",
    "IPropTypeSettingsManager",
    "IPropTypeSettingsManager",
    "IResponsiveScalingCalculator",
    "ISequenceDataService",
    "ISequenceManager",
    "ISettingsCoordinator",
    "ITurnIntensityManager",
    "ITurnIntensityManagerFactory",
    "IUIStateManagementService",
    "IUIStateManager",
    # Tab settings
    "IUserProfileService",
    "IUserProfileSettingsManager",
    "IValidationService",
    "IVisibilityService",
    "IVisibilitySettingsManager",
    "IVisibilitySettingsManager",
    "IWorkbenchClipboardService",
    # Workbench services
    "IWorkbenchExportService",
    "RenderingContext",
]
