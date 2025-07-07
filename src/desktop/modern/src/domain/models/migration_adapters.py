"""
Migration Adapters for Gradual Transition to Pydantic Models

This module provides adapters to convert between:
1. Old dataclass models (current desktop implementation)
2. New Pydantic models (with camelCase JSON serialization)

Key Features:
- Bidirectional conversion (old ↔ new)
- Backward compatibility during migration
- Type-safe conversions with validation
- Gradual migration support
"""

from typing import Dict, Any, Optional, List
from dataclasses import asdict

# Import old models (current desktop implementation)
try:
    from ..core_models import (
        MotionData as OldMotionData,
        BeatData as OldBeatData,
        SequenceData as OldSequenceData,
        MotionType as OldMotionType,
        RotationDirection as OldRotationDirection,
        Location as OldLocation,
        Orientation as OldOrientation,
    )
    OLD_MODELS_AVAILABLE = True
except ImportError:
    # Old models not available yet, create placeholder types
    OLD_MODELS_AVAILABLE = False
    OldMotionData = None
    OldBeatData = None
    OldSequenceData = None

# Import new Pydantic models
from .pydantic_models import (
    MotionData as NewMotionData,
    BeatData as NewBeatData,
    SequenceData as NewSequenceData,
    create_default_motion_data,
    create_default_beat_data,
    create_default_sequence_data,
)


class ModelMigrationAdapter:
    """Adapter for converting between old and new domain models."""
    
    @staticmethod
    def enum_to_string(enum_value) -> str:
        """Convert old enum values to string literals."""
        if hasattr(enum_value, 'value'):
            return enum_value.value.lower()
        return str(enum_value).lower()
    
    @staticmethod
    def string_to_enum(string_value: str, enum_class):
        """Convert string literals to old enum values."""
        if not OLD_MODELS_AVAILABLE:
            return string_value
        
        # Try to find matching enum value
        for enum_item in enum_class:
            if enum_item.value.lower() == string_value.lower():
                return enum_item
        
        # Fallback: return first enum value
        return list(enum_class)[0]
    
    @classmethod
    def old_motion_to_new(cls, old_motion: 'OldMotionData') -> NewMotionData:
        """Convert old MotionData to new Pydantic MotionData."""
        if not OLD_MODELS_AVAILABLE:
            raise RuntimeError("Old models not available for conversion")
        
        return NewMotionData(
            motion_type=cls.enum_to_string(old_motion.motion_type),
            prop_rot_dir=cls.enum_to_string(old_motion.prop_rot_dir),
            start_loc=cls.enum_to_string(old_motion.start_loc),
            end_loc=cls.enum_to_string(old_motion.end_loc),
            turns=old_motion.turns,
            start_ori=cls.enum_to_string(old_motion.start_ori),
            end_ori=cls.enum_to_string(old_motion.end_ori),
        )
    
    @classmethod
    def new_motion_to_old(cls, new_motion: NewMotionData) -> 'OldMotionData':
        """Convert new Pydantic MotionData to old MotionData."""
        if not OLD_MODELS_AVAILABLE:
            raise RuntimeError("Old models not available for conversion")
        
        return OldMotionData(
            motion_type=cls.string_to_enum(new_motion.motion_type, OldMotionType),
            prop_rot_dir=cls.string_to_enum(new_motion.prop_rot_dir, OldRotationDirection),
            start_loc=cls.string_to_enum(new_motion.start_loc, OldLocation),
            end_loc=cls.string_to_enum(new_motion.end_loc, OldLocation),
            turns=new_motion.turns,
            start_ori=cls.string_to_enum(new_motion.start_ori, OldOrientation),
            end_ori=cls.string_to_enum(new_motion.end_ori, OldOrientation),
        )
    
    @classmethod
    def old_beat_to_new(cls, old_beat: 'OldBeatData') -> NewBeatData:
        """Convert old BeatData to new Pydantic BeatData."""
        if not OLD_MODELS_AVAILABLE:
            raise RuntimeError("Old models not available for conversion")
        
        return NewBeatData(
            beat_number=old_beat.beat_number,
            letter=old_beat.letter,
            duration=getattr(old_beat, 'duration', 1.0),
            blue_motion=cls.old_motion_to_new(old_beat.blue_motion),
            red_motion=cls.old_motion_to_new(old_beat.red_motion),
            blue_reversal=getattr(old_beat, 'blue_reversal', False),
            red_reversal=getattr(old_beat, 'red_reversal', False),
            filled=getattr(old_beat, 'filled', False),
            tags=getattr(old_beat, 'tags', []),
            glyph_data=getattr(old_beat, 'glyph_data', None),
        )
    
    @classmethod
    def new_beat_to_old(cls, new_beat: NewBeatData) -> 'OldBeatData':
        """Convert new Pydantic BeatData to old BeatData."""
        if not OLD_MODELS_AVAILABLE:
            raise RuntimeError("Old models not available for conversion")
        
        return OldBeatData(
            beat_number=new_beat.beat_number,
            letter=new_beat.letter,
            blue_motion=cls.new_motion_to_old(new_beat.blue_motion),
            red_motion=cls.new_motion_to_old(new_beat.red_motion),
            # Note: Old model might not have all new properties
        )
    
    @classmethod
    def old_sequence_to_new(cls, old_sequence: 'OldSequenceData') -> NewSequenceData:
        """Convert old SequenceData to new Pydantic SequenceData."""
        if not OLD_MODELS_AVAILABLE:
            raise RuntimeError("Old models not available for conversion")
        
        new_beats = [cls.old_beat_to_new(beat) for beat in old_sequence.beats]
        
        return NewSequenceData(
            name=old_sequence.name,
            beats=new_beats,
            length=getattr(old_sequence, 'length', len(new_beats)),
            created_at=getattr(old_sequence, 'created_at', None),
            updated_at=getattr(old_sequence, 'updated_at', None),
            version=getattr(old_sequence, 'version', '1.0'),
            difficulty=getattr(old_sequence, 'difficulty', None),
            tags=getattr(old_sequence, 'tags', []),
        )
    
    @classmethod
    def new_sequence_to_old(cls, new_sequence: NewSequenceData) -> 'OldSequenceData':
        """Convert new Pydantic SequenceData to old SequenceData."""
        if not OLD_MODELS_AVAILABLE:
            raise RuntimeError("Old models not available for conversion")
        
        old_beats = [cls.new_beat_to_old(beat) for beat in new_sequence.beats]
        
        return OldSequenceData(
            name=new_sequence.name,
            beats=old_beats,
        )


class JSONCompatibilityLayer:
    """Provides JSON compatibility between old and new formats."""
    
    @staticmethod
    def old_model_to_camel_case_json(old_model) -> str:
        """Convert old model to camelCase JSON (via new model)."""
        if isinstance(old_model, OldMotionData):
            new_model = ModelMigrationAdapter.old_motion_to_new(old_model)
        elif isinstance(old_model, OldBeatData):
            new_model = ModelMigrationAdapter.old_beat_to_new(old_model)
        elif isinstance(old_model, OldSequenceData):
            new_model = ModelMigrationAdapter.old_sequence_to_new(old_model)
        else:
            raise ValueError(f"Unsupported model type: {type(old_model)}")
        
        return new_model.model_dump_json()
    
    @staticmethod
    def camel_case_json_to_old_model(json_str: str, model_type: type):
        """Convert camelCase JSON to old model (via new model)."""
        import json
        data = json.loads(json_str)
        
        if model_type == OldMotionData:
            new_model = NewMotionData(**data)
            return ModelMigrationAdapter.new_motion_to_old(new_model)
        elif model_type == OldBeatData:
            new_model = NewBeatData(**data)
            return ModelMigrationAdapter.new_beat_to_old(new_model)
        elif model_type == OldSequenceData:
            new_model = NewSequenceData(**data)
            return ModelMigrationAdapter.new_sequence_to_old(new_model)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")


class GradualMigrationHelper:
    """Helper for gradual migration from old to new models."""
    
    def __init__(self, use_new_models: bool = False):
        """
        Initialize migration helper.
        
        Args:
            use_new_models: If True, use new Pydantic models. If False, use old models.
        """
        self.use_new_models = use_new_models
    
    def create_motion_data(self, **kwargs) -> 'MotionData':
        """Create motion data using current model preference."""
        if self.use_new_models:
            return create_default_motion_data(**kwargs)
        else:
            if not OLD_MODELS_AVAILABLE:
                # Fallback to new models if old not available
                return create_default_motion_data(**kwargs)
            # Convert kwargs to old enum format and create old model
            # This would need specific implementation based on old model structure
            return create_default_motion_data(**kwargs)  # Simplified for now
    
    def create_beat_data(self, **kwargs) -> 'BeatData':
        """Create beat data using current model preference."""
        if self.use_new_models:
            return create_default_beat_data(**kwargs)
        else:
            if not OLD_MODELS_AVAILABLE:
                return create_default_beat_data(**kwargs)
            return create_default_beat_data(**kwargs)  # Simplified for now
    
    def create_sequence_data(self, **kwargs) -> 'SequenceData':
        """Create sequence data using current model preference."""
        if self.use_new_models:
            return create_default_sequence_data(**kwargs)
        else:
            if not OLD_MODELS_AVAILABLE:
                return create_default_sequence_data(**kwargs)
            return create_default_sequence_data(**kwargs)  # Simplified for now
    
    def to_json(self, model) -> str:
        """Convert model to JSON using appropriate format."""
        if self.use_new_models or not OLD_MODELS_AVAILABLE:
            # Use camelCase JSON
            if hasattr(model, 'model_dump_json'):
                return model.model_dump_json()
            else:
                # Convert old model to camelCase JSON
                return JSONCompatibilityLayer.old_model_to_camel_case_json(model)
        else:
            # Use old JSON format (snake_case)
            import json
            if hasattr(model, 'model_dump'):
                # New model, but output snake_case for compatibility
                return model.model_dump_json(by_alias=False)
            else:
                # Old model
                return json.dumps(asdict(model))


# Global migration helper instance
migration_helper = GradualMigrationHelper(use_new_models=True)


def enable_new_models():
    """Enable new Pydantic models globally."""
    global migration_helper
    migration_helper.use_new_models = True


def enable_old_models():
    """Enable old dataclass models globally."""
    global migration_helper
    migration_helper.use_new_models = False
