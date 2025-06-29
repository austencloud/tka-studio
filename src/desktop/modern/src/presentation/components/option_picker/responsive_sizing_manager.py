"""DEPRECATED: Use option_picker.services.layout.sizing_service instead"""
import warnings
warnings.warn("Use option_picker.services.layout.sizing_service instead", DeprecationWarning, stacklevel=2)
from .services.layout.sizing_service import ResponsiveSizingService
__all__ = ['ResponsiveSizingService']
