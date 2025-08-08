# Application services package
from __future__ import annotations


QT_SERVICES_AVAILABLE = False  # Set to False to avoid Qt dependencies in tests

from shared.application.services.motion.orientation_calculator import (
    IOrientationCalculator,
    OrientationCalculator,
)


# Core services

__all__ = [
    "IOrientationCalculator",
    "OrientationCalculator",
]
