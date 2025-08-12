# Modern Domain Models Module
"""
TKA Domain Models

Clean, immutable dataclass models with JSON serialization support.
Supports both snake_case (Python) and camelCase (JSON/TypeScript) conventions.
"""

# Import serialization utilities
from __future__ import annotations

from .arrow_data import ArrowData, ArrowType  # Export pictograph models
from .beat_data import BeatData

# Export core models from their new organized locations
# Import enums from their new location
from .enums import (
    ArrowColor,
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
    VTGMode,
)
from .grid_data import GridData
from .letter_type_classifier import (  # Export letter type classifier
    LetterTypeClassifier,
)
from .motion_data import MotionData
from .pictograph_data import PictographData
from .positioning_results import (  # Export positioning models
    ArrowPositionResult,
    PropPositionResult,
)
from .prop_data import PropData, PropType
from .sequence_data import SequenceData
from ..serialization import (
    dataclass_to_camel_dict,
    dict_from_camel_case,
    domain_model_from_json,
    domain_model_to_json,
)


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
    "ArrowColor",
    # Pictograph models
    "ArrowData",
    # Positioning models
    "ArrowPositionResult",
    "ArrowType",
    "BeatData",
    "ElementalType",
    "GridData",
    "GridMode",
    "GridPosition",
    "HandMotionType",
    "HandPath",
    "LetterType",
    # Utilities
    "LetterTypeClassifier",
    "Location",
    # Core models - Data classes
    "MotionData",
    # Core models - Enums (most critical)
    "MotionType",
    "Orientation",
    "PictographData",
    "PropData",
    "PropPositionResult",
    "PropType",
    "RotationDirection",
    "SequenceData",
    "VTGMode",
    "dataclass_to_camel_dict",
    "dict_from_camel_case",
    "domain_model_from_json",
    # Serialization utilities
    "domain_model_to_json",
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
            "DEFAULT_SETTINGS",
            "BackgroundType",
            "BeatLayoutData",
            "CodexExportSettingsData",
            "GlobalSettingsData",
            "ImageExportSettingsData",
            "SettingsData",
            "UserProfileData",
            "VisibilitySettingsData",
        ]
    )
