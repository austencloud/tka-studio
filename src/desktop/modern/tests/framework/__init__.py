"""
TKA Modern Image Export Testing Framework
========================================

Comprehensive testing framework for the Modern image export system that can detect:
- Visual regressions (font sizing, positioning, missing elements)
- Service registration failures
- UI workflow inconsistencies

Framework Components:
- ui_automation/: UI interaction automation and validation
- visual_regression/: Image comparison and visual element detection
- service_validation/: Service container and registration validation
- test_data/: Test data generators and fixtures
"""

from .ui_automation import (
    PickerNavigator,
    BeatFrameValidator,
    WorkbenchController,
)

from .visual_regression import (
    ImageComparator,
    FontSizeValidator,
    VisualElementDetector,
)

from .service_validation import (
    ContainerInspector,
    ServiceRegistrationValidator,
)

__all__ = [
    # UI Automation
    "PickerNavigator",
    "BeatFrameValidator", 
    "WorkbenchController",
    
    # Visual Regression
    "ImageComparator",
    "FontSizeValidator",
    "VisualElementDetector",
    
    # Service Validation
    "ContainerInspector",
    "ServiceRegistrationValidator",
]
