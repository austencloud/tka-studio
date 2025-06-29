"""DEPRECATED: Use option_picker.services.layout.dimension_calculator instead"""
import warnings
warnings.warn("Use option_picker.services.layout.dimension_calculator instead", DeprecationWarning, stacklevel=2)
from .services.layout.dimension_calculator import DimensionCalculator
__all__ = ['DimensionCalculator']
