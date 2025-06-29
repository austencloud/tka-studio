"""DEPRECATED: Use option_picker.services.data.pool_manager instead"""
import warnings
warnings.warn("Use option_picker.services.data.pool_manager instead", DeprecationWarning, stacklevel=2)
from .services.data.pool_manager import PictographPoolManager
__all__ = ['PictographPoolManager']
