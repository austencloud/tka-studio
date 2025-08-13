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

from __future__ import annotations

from desktop.modern.application.services.option_picker.option_provider import (
    OptionProvider,
)

# Core components (primary public API)
from .components.option_picker import OptionPicker
from .components.option_picker_widget import OptionPickerWidget

# Types
from .types.letter_types import LetterType


# Services (for advanced usage)
# Note: PictographPoolManager has been moved to application.services.option_picker.data.pool_manager
# Import it directly from there to avoid circular imports
# from desktop.modern.application.services.option_picker.data.pool_manager import PictographPoolManager


# Backward compatibility exports (maintain old interface)
__all__ = [
    # "PictographPoolManager", # Moved to application.services.option_picker.data.pool_manager
    "LetterType",
    "OptionPicker",
    "OptionPickerWidget",
    "OptionProvider",
]

__version__ = "2.0.0"
__restructured__ = True
