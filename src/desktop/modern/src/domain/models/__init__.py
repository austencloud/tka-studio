# Modern Domain Models Module

# Export core models first (most important)
from .core_models import (
    # Enums
    MotionType,
    HandMotionType,
    HandPath,
    RotationDirection,
    Orientation,
    Location,
    GridPosition,
    VTGMode,
    ElementalType,
    LetterType,
    ArrowColor,
    GridMode,
    
    # Data classes
    MotionData,
    GlyphData,
    BeatData,
    SequenceData,
)

from .pictograph_models import (
    # Export pictograph models
    ArrowData,
    PropData,
    GridData,
    PictographData,
    PropType,
    ArrowType,
)

from .positioning_models import (
    # Export positioning models
    ArrowPositionResult,
    PropPositionResult,
)

from .letter_type_classifier import (
    # Export letter type classifier
    LetterTypeClassifier,
)

# Import generation and settings models with error handling
try:
    from .generation_models import (
        GenerationConfig,
        GenerationResult,
        GenerationState,
    )
    _GENERATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Generation models not available: {e}")
    _GENERATION_AVAILABLE = False

try:
    from .settings_models import (
        UserProfileData,
        VisibilitySettingsData,
        BeatLayoutData,
        ImageExportSettingsData,
        CodexExportSettingsData,
        GlobalSettingsData,
        SettingsData,
        DEFAULT_SETTINGS,
        BackgroundType,
    )
    _SETTINGS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Settings models not available: {e}")
    _SETTINGS_AVAILABLE = False

# Core exports (always available)
__all__ = [
    # Core models - Enums (most critical)
    'MotionType',
    'HandMotionType', 
    'HandPath',
    'RotationDirection',
    'Orientation',
    'Location',
    'GridPosition',
    'VTGMode',
    'ElementalType',
    'LetterType',
    'ArrowColor',
    'GridMode',
    
    # Core models - Data classes
    'MotionData',
    'GlyphData', 
    'BeatData',
    'SequenceData',
    
    # Pictograph models
    'ArrowData',
    'PropData',
    'GridData',
    'PictographData',
    'PropType',
    'ArrowType',
    
    # Positioning models
    'ArrowPositionResult',
    'PropPositionResult',
    
    # Utilities
    'LetterTypeClassifier',
]

# Add optional exports if available
if _GENERATION_AVAILABLE:
    __all__.extend([
        'GenerationConfig',
        'GenerationResult', 
        'GenerationState',
    ])

if _SETTINGS_AVAILABLE:
    __all__.extend([
        'UserProfileData',
        'VisibilitySettingsData',
        'BeatLayoutData',
        'ImageExportSettingsData',
        'CodexExportSettingsData',
        'GlobalSettingsData',
        'SettingsData',
        'DEFAULT_SETTINGS',
        'BackgroundType',
    ])
