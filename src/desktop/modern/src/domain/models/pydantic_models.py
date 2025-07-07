"""
Pydantic-based Domain Models with camelCase JSON Serialization

This module provides Pydantic models that:
1. Use snake_case in Python code (Pythonic)
2. Serialize to camelCase JSON (Web standards)
3. Are compatible with @tka/domain TypeScript schemas
4. Support both naming conventions during migration

Key Features:
- alias_generator=to_camel for automatic camelCase JSON
- populate_by_name=True for backward compatibility
- frozen=True for immutability (like current dataclasses)
- Full type safety and validation
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from enum import Enum


# Base configuration for all TKA domain models
class TKABaseModel(BaseModel):
    """Base model for all TKA domain objects with camelCase JSON serialization."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,  # Accepts both snake_case and camelCase
        frozen=True,  # Immutable like current dataclasses
        extra='forbid',  # Strict validation
        str_strip_whitespace=True,  # Clean string inputs
        validate_assignment=True,  # Validate on assignment
    )

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Override to use aliases by default (camelCase output)."""
        kwargs.setdefault('by_alias', True)
        return super().model_dump(**kwargs)

    def model_dump_json(self, **kwargs) -> str:
        """Override to use aliases by default (camelCase output)."""
        kwargs.setdefault('by_alias', True)
        return super().model_dump_json(**kwargs)


# Motion Types (matching schema exactly)
MotionType = Literal['pro', 'anti', 'float', 'dash', 'static']
PropRotDir = Literal['cw', 'ccw', 'no_rot']
Location = Literal['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw']
Orientation = Literal['in', 'out', 'clock', 'counter']


class MotionData(TKABaseModel):
    """
    Motion data with automatic camelCase JSON serialization.
    
    Python usage (snake_case):
        motion = MotionData(motion_type='pro', prop_rot_dir='cw', start_loc='n')
    
    JSON output (camelCase):
        {"motionType": "pro", "propRotDir": "cw", "startLoc": "n"}
    """
    motion_type: MotionType
    prop_rot_dir: PropRotDir
    start_loc: Location
    end_loc: Location
    turns: float = 0.0
    start_ori: Orientation
    end_ori: Orientation


# Pictograph Types
GridMode = Literal['diamond', 'box']
StartEndPos = Literal[
    'alpha1', 'alpha2', 'alpha3', 'alpha4', 'alpha5', 'alpha6', 'alpha7', 'alpha8',
    'beta1', 'beta2', 'beta3', 'beta4', 'beta5', 'beta6', 'beta7', 'beta8',
    'gamma1', 'gamma2', 'gamma3', 'gamma4', 'gamma5', 'gamma6', 'gamma7', 'gamma8'
]
Timing = Literal['together', 'split']
Direction = Literal['same', 'opp']


class PictographData(TKABaseModel):
    """
    Pictograph data with automatic camelCase JSON serialization.
    
    Matches the pictograph-data.json schema exactly.
    """
    grid_mode: GridMode
    grid: str
    letter: Optional[str] = None
    start_pos: Optional[StartEndPos] = None
    end_pos: Optional[StartEndPos] = None
    timing: Optional[Timing] = None
    direction: Optional[Direction] = None
    is_start_position: Optional[bool] = None
    
    # Grid data as flat properties (matching schema)
    grid_data: Optional[Dict[str, Any]] = None


class BeatData(TKABaseModel):
    """
    Beat data with automatic camelCase JSON serialization.
    
    Combines current desktop BeatData with schema compatibility.
    """
    beat_number: int = Field(ge=0)
    letter: str
    duration: float = Field(gt=0, default=1.0)
    
    # Motion data
    blue_motion: MotionData
    red_motion: MotionData
    
    # Pictograph data
    pictograph_data: Optional[PictographData] = None
    
    # Beat properties
    blue_reversal: bool = False
    red_reversal: bool = False
    filled: bool = False
    tags: List[str] = Field(default_factory=list)
    
    # Desktop-specific properties (not in schema yet)
    glyph_data: Optional[Dict[str, Any]] = None


class SequenceData(TKABaseModel):
    """
    Sequence data with automatic camelCase JSON serialization.
    
    Matches the sequence-data.json schema.
    """
    name: str
    beats: List[BeatData] = Field(default_factory=list)
    
    # Metadata
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    version: str = "1.0"
    
    # Sequence properties
    length: int = Field(ge=1, default=8)
    difficulty: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    
    def add_beat(self, beat: BeatData) -> 'SequenceData':
        """Add a beat and return a new sequence (immutable)."""
        new_beats = self.beats + [beat]
        return self.model_copy(update={'beats': new_beats})
    
    def update_beat(self, index: int, beat: BeatData) -> 'SequenceData':
        """Update a beat and return a new sequence (immutable)."""
        new_beats = self.beats.copy()
        new_beats[index] = beat
        return self.model_copy(update={'beats': new_beats})


# Factory functions for easy creation
def create_default_motion_data(
    motion_type: MotionType = 'pro',
    prop_rot_dir: PropRotDir = 'cw',
    start_loc: Location = 'n',
    end_loc: Location = 'e',
    start_ori: Orientation = 'in',
    end_ori: Orientation = 'in'
) -> MotionData:
    """Create a default motion data object."""
    return MotionData(
        motion_type=motion_type,
        prop_rot_dir=prop_rot_dir,
        start_loc=start_loc,
        end_loc=end_loc,
        turns=0.0,
        start_ori=start_ori,
        end_ori=end_ori
    )


def create_default_beat_data(
    beat_number: int,
    letter: str,
    blue_motion: Optional[MotionData] = None,
    red_motion: Optional[MotionData] = None
) -> BeatData:
    """Create a default beat data object."""
    return BeatData(
        beat_number=beat_number,
        letter=letter,
        duration=1.0,
        blue_motion=blue_motion or create_default_motion_data(),
        red_motion=red_motion or create_default_motion_data()
    )


def create_default_sequence_data(name: str, length: int = 8) -> SequenceData:
    """Create a default sequence with empty beats."""
    return SequenceData(
        name=name,
        length=length,
        beats=[]
    )
