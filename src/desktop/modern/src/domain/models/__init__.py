# Modern Domain Models Module
"""
TKA Domain Models

Clean, immutable dataclass models with JSON serialization support.
Supports both snake_case (Python) and camelCase (JSON/TypeScript) conventions.
"""

# Import serialization utilities

from ..serialization import (
    dataclass_to_camel_dict,
    dict_from_camel_case,
    domain_model_from_json,
    domain_model_to_json,
)
from .arrow_data import ArrowData, ArrowType  # Export pictograph models
from .beat_data import BeatData

# Export core models from their new organized locations
# Import enums from their new location
from .enums import (
    ArrowColor,
    Direction,
    ElementalType,
    GridMode,
    GridPosition,
    HandMotionType,
    HandPath,
    LetterType,
    Location,
    MotionType,
    Orientation,
    RotationDirection,
    Timing,
    VTGMode,
)
from .glyph_models import GlyphData
from .grid_data import GridData
from .letter_type_classifier import (  # Export letter type classifier
    LetterTypeClassifier,
)
from .motion_models import MotionData
from .pictograph_data import PictographData
from .positioning_models import (  # Export positioning models
    ArrowPositionResult,
    PropPositionResult,
)
from .prop_data import PropData, PropType
from .sequence_data import SequenceData

# Import serialization utilities
try:
    from ..serialization import (
        dataclass_to_camel_dict,
        dict_from_camel_case,
        domain_model_from_json,
        domain_model_to_json,
    )
except ImportError:
    # Fallback if serialization module not available
    domain_model_to_json = None
    domain_model_from_json = None
    dataclass_to_camel_dict = None
    dict_from_camel_case = None

# Import generation and settings models with error handling
try:
    _GENERATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Generation models not available: {e}")
    _GENERATION_AVAILABLE = False

try:
    _SETTINGS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Settings models not available: {e}")
    _SETTINGS_AVAILABLE = False

# Core exports (always available)
__all__ = [
    # Core models - Enums (most critical)
    "MotionType",
    "HandMotionType",
    "HandPath",
    "RotationDirection",
    "Orientation",
    "Location",
    "GridPosition",
    "VTGMode",
    "ElementalType",
    "LetterType",
    "ArrowColor",
    "GridMode",
    # Core models - Data classes
    "MotionData",
    "GlyphData",
    "BeatData",
    "SequenceData",
    # Pictograph models
    "ArrowData",
    "PropData",
    "GridData",
    "PictographData",
    "PropType",
    "ArrowType",
    # Positioning models
    "ArrowPositionResult",
    "PropPositionResult",
    # Utilities
    "LetterTypeClassifier",
    # Serialization utilities
    "domain_model_to_json",
    "domain_model_from_json",
    "dataclass_to_camel_dict",
    "dict_from_camel_case",
]

# Add optional exports if available
if _GENERATION_AVAILABLE:
    __all__.extend(
        [
            "GenerationConfig",
            "GenerationResult",
            "GenerationState",
        ]
    )

if _SETTINGS_AVAILABLE:
    __all__.extend(
        [
            "UserProfileData",
            "VisibilitySettingsData",
            "BeatLayoutData",
            "ImageExportSettingsData",
            "CodexExportSettingsData",
            "GlobalSettingsData",
            "SettingsData",
            "DEFAULT_SETTINGS",
            "BackgroundType",
        ]
    )
