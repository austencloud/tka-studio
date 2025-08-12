# Application services package


QT_SERVICES_AVAILABLE = False  # Set to False to avoid Qt dependencies in tests

from .core.object_pool_manager import ObjectPoolManager
from .motion.orientation_calculator import IOrientationCalculator, OrientationCalculator

# Core services

__all__ = [
    "OrientationCalculator",
    "IOrientationCalculator",
    "ObjectPoolManager",
]
