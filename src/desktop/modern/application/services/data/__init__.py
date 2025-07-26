# Data services module - exports only local data services
# External service dependencies should not be exposed at module level

from .dataset_manager import DatasetManager
from .legacy_to_modern_converter import LegacyToModernConverter
from .modern_to_legacy_converter import ModernToLegacyConverter

__all__ = [
    "DatasetManager",
    "LegacyToModernConverter",
    "ModernToLegacyConverter",
]
