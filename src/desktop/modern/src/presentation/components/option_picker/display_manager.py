"""DEPRECATED: Use option_picker.services.layout.display_service instead"""
import warnings
warnings.warn("Use option_picker.services.layout.display_service instead", DeprecationWarning, stacklevel=2)
from .services.layout.display_service import OptionPickerDisplayManager
__all__ = ['OptionPickerDisplayManager']
