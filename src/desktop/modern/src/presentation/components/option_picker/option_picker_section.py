"""DEPRECATED: Use option_picker.components.sections.section_widget instead"""
import warnings
warnings.warn("Use option_picker.components.sections.section_widget instead", DeprecationWarning, stacklevel=2)
from .components.sections.section_widget import OptionPickerSection
__all__ = ['OptionPickerSection']
