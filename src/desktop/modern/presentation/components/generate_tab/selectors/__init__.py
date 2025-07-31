"""
Generation Tab Selectors Package

This package contains all the selector components used in the generation tab
for configuring sequence generation parameters.

Each selector follows the GenerationControlBase pattern and provides:
- Consistent styling and layout
- Type-safe value emission via pyqtSignal
- Appropriate tooltips and labels
- Modern UI appearance matching the overall design
"""

from .cap_type_selector import CAPTypeSelector
from .generation_mode_toggle import GenerationModeToggle
from .grid_mode_selector import ModernGridModeSelector
from .length_selector import LengthSelector
from .letter_type_selector import LetterTypeSelector
from .level_selector import LevelSelector
from .prop_continuity_toggle import PropContinuityToggle
from .slice_size_selector import SliceSizeSelector
from .turn_intensity_selector import TurnIntensitySelector

__all__ = [
    "CAPTypeSelector",
    "GenerationModeToggle",
    "ModernGridModeSelector",
    "LengthSelector",
    "LetterTypeSelector",
    "LevelSelector",
    "PropContinuityToggle",
    "SliceSizeSelector",
    "TurnIntensitySelector",
]
