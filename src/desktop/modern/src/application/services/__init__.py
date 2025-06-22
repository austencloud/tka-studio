# Application services package

# Note: Qt-dependent services (arrow_management_service, prop_management_service)
# are not imported here to avoid DLL loading issues during testing.
# Import them directly when needed:
# from application.services.positioning.arrow_management_service import ArrowManagementService

QT_SERVICES_AVAILABLE = False  # Set to False to avoid Qt dependencies in tests

from .motion.motion_validation_service import (
    MotionValidationService,
    IMotionValidationService,
)
from .motion.motion_orientation_service import (
    MotionOrientationService,
    IMotionOrientationService,
)

# Layout services consolidated into LayoutManagementService (ILayoutService)
from .core.pictograph_management_service import PictographManagementService
from .core.sequence_management_service import SequenceManagementService

__all__ = [
    "MotionValidationService",
    "IMotionValidationService",
    "MotionOrientationService",
    "IMotionOrientationService",
    "PictographManagementService",
    "SequenceManagementService",
    # Note: Qt-dependent services excluded to avoid DLL issues:
    # "ArrowManagementService", "IArrowManagementService",
    # "PropManagementService", "IPropManagementService"
]
