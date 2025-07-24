"""
Visual Regression Detection Framework
====================================

Provides comprehensive visual regression detection capabilities for the Modern
image export system, including pixel-perfect comparison, font size validation,
and visual element detection.

Components:
- ImageComparator: Pixel-perfect Legacy vs Modern comparison
- FontSizeValidator: Specific font size regression prevention
- VisualElementDetector: Detection of grids, props, arrows, and other elements
"""

from .font_size_validator import (
    FontComparisonReport,
    FontMeasurements,
    FontSizeValidator,
)
from .image_comparator import ComparisonResult, ImageComparator
from .visual_element_detector import (
    ElementDetectionResult,
    VisualElementDetector,
    VisualElementReport,
)

__all__ = [
    "ImageComparator",
    "ComparisonResult",
    "FontSizeValidator",
    "FontMeasurements",
    "FontComparisonReport",
    "VisualElementDetector",
    "VisualElementReport",
    "ElementDetectionResult",
]
