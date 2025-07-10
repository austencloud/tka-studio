"""
Modern Option Picker Package - Hierarchical Structure

This package contains the Modern option picker implementation with
improved hierarchical organization for better maintainability.

Architecture follows clean separation:
- core/ - Main orchestration and widget coordination
- components/ - Reusable UI widgets organized by purpose
- services/ - Business logic separated by domain (data/layout)
- types/ - Type definitions and constants

All domain/application/presentation absolute imports are preserved.
"""

# Core components (primary public API)
from .core.option_picker import OptionPicker
from .core.option_picker_widget import OptionPickerWidget

# Services (for advanced usage)
from .services.data.option_service import OptionService
from .services.data.pool_manager import PictographPoolManager
from .services.layout.display_service import OptionPickerDisplayManager

# Types
from .types.letter_types import LetterType

# Backward compatibility exports (maintain old interface)
__all__ = [
    "OptionPicker",
    "OptionPickerWidget",
    "OptionService",
    "OptionPickerDisplayManager",
    "PictographPoolManager",
    "LetterType",
]

__version__ = "2.0.0"
__restructured__ = True
