# 02 - TKA Domain Models Guide

## 🏗️ SOPHISTICATED IMMUTABLE DATA MODELS

TKA uses complex, immutable dataclasses with sophisticated validation and functional operations. AI agents must understand these patterns to work effectively.

## 📊 CORE DOMAIN MODELS

### `BeatData` - Fundamental Unit of Motion
**Location**: `domain/models/core_models.py`

```python
@dataclass(frozen=True)
class BeatData:
    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    beat_number: int = 1

    # Business data
    letter: Optional[str] = None
    duration: float = 1.0

    # Motion data (complex nested objects)
    blue_motion: Optional[MotionData] = None
    red_motion: Optional[MotionData] = None

    # Glyph data (visual representation)
    glyph_data: Optional[GlyphData] = None

    # State flags
    blue_reversal: bool = False
    red_reversal: bool = False
    is_blank: bool = False

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
```

**Key Operations**:
```python
# CORRECT: Immutable updates
beat = BeatData(beat_number=1, letter="A")
updated_beat = beat.update(duration=2.0)  # Returns new instance

# Validation
is_valid = beat.is_valid()  # Checks business rules

# Serialization
beat_dict = beat.to_dict()
restored_beat = BeatData.from_dict(beat_dict)
```

### `SequenceData` - Collection of Beats
**Location**: `domain/models/core_models.py`

```python
@dataclass(frozen=True)
class SequenceData:
    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    word: str = ""  # Generated word from sequence

    # Business data
    beats: List[BeatData] = field(default_factory=list)
    start_position: Optional[str] = None

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
```

**Sophisticated Operations**:
```python
# Functional operations (return new instances)
sequence = SequenceData(name="Test", beats=[])
new_sequence = sequence.add_beat(beat_data)      # Immutable add
updated_sequence = sequence.remove_beat(0)       # Immutable remove
modified_sequence = sequence.update_beat(1, letter="B")  # Immutable update

# Properties
length = sequence.length                         # Number of beats
duration = sequence.total_duration              # Sum of beat durations
is_valid = sequence.is_valid                    # Business rule validation
is_empty = sequence.is_empty                    # No beats check

# Access patterns
beat = sequence.get_beat(beat_number=1)         # Safe access
```

### `MotionData` - Complex Motion Definition
**Location**: `domain/models/core_models.py`

```python
@dataclass(frozen=True)
class MotionData:
    motion_type: MotionType                      # PRO, ANTI, STATIC, DASH, FLOAT
    prop_rot_dir: RotationDirection             # CLOCKWISE, COUNTER_CLOCKWISE
    start_loc: Location                         # NORTH, EAST, SOUTH, WEST, etc.
    end_loc: Location
    turns: float = 0.0
    start_ori: str = "in"
    end_ori: str = "in"
```

**Enums Used**:
```python
class MotionType(Enum):
    PRO = "pro"
    ANTI = "anti"
    FLOAT = "float"
    DASH = "dash"
    STATIC = "static"

class Location(Enum):
    NORTH = "n"
    EAST = "e"
    SOUTH = "s"
    WEST = "w"
    NORTHEAST = "ne"
    SOUTHEAST = "se"
    SOUTHWEST = "sw"
    NORTHWEST = "nw"
```

### `PictographData` - Visual Representation
**Location**: `domain/models/pictograph_models.py`

```python
@dataclass(frozen=True)
class PictographData:
    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # Grid configuration
    grid_data: GridData = field(default_factory=GridData)

    # Arrows and props (complex nested structures)
    arrows: Dict[str, ArrowData] = field(default_factory=dict)  # "blue", "red"
    props: Dict[str, PropData] = field(default_factory=dict)    # "blue", "red"

    # Letter and position data
    letter: Optional[str] = None
    start_position: Optional[str] = None
    end_position: Optional[str] = None

    # Visual state
    is_blank: bool = False
    is_mirrored: bool = False

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
```

**Access Properties**:
```python
# Convenient access to color-specific data
blue_arrow = pictograph.blue_arrow    # Returns ArrowData
red_arrow = pictograph.red_arrow      # Returns ArrowData
blue_prop = pictograph.blue_prop      # Returns PropData
red_prop = pictograph.red_prop        # Returns PropData

# Immutable updates
updated_pictograph = pictograph.update_arrow("blue", position=(100, 100))
modified_pictograph = pictograph.update_prop("red", orientation="out")
```

## 🎯 ADVANCED DOMAIN PATTERNS

### Glyph Data System
```python
@dataclass(frozen=True)
class GlyphData:
    # VTG glyph data
    vtg_mode: Optional[VTGMode] = None           # SPLIT_SAME, TOG_OPP, etc.

    # Elemental glyph data  
    elemental_type: Optional[ElementalType] = None  # WATER, FIRE, EARTH, AIR

    # TKA glyph data
    letter_type: Optional[LetterType] = None     # TYPE1, TYPE2, etc.
    has_dash: bool = False
    turns_data: Optional[str] = None

    # Position glyph data
    start_position: Optional[str] = None
    end_position: Optional[str] = None

    # Visibility flags
    show_elemental: bool = True
    show_vtg: bool = True
    show_tka: bool = True
    show_positions: bool = True
```

### Arrow and Prop Data
```python
@dataclass(frozen=True)
class ArrowData:
    # Core identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    arrow_type: ArrowType = ArrowType.BLUE

    # Motion reference (complex relationship)
    motion_data: Optional[MotionData] = None

    # Visual properties
    color: str = "blue"
    turns: float = 0.0
    is_mirrored: bool = False

    # Position data (calculated by positioning system)
    location: Optional[str] = None
    position_x: float = 0.0
    position_y: float = 0.0
    rotation_angle: float = 0.0

    # State flags
    is_visible: bool = True
    is_selected: bool = False
```

## 🔄 IMMUTABLE OPERATIONS PATTERNS

### Update Patterns
```python
# Single field update
beat = beat.update(letter="B")
sequence = sequence.update(name="New Name")

# Multiple field update
beat = beat.update(letter="C", duration=1.5, blue_reversal=True)

# Nested object update
pictograph = pictograph.update_arrow("blue", 
    position_x=150.0, 
    position_y=200.0,
    rotation_angle=45.0
)
```

### Collection Operations
```python
# Adding to collections
sequence = sequence.add_beat(new_beat)
sequence = sequence.update(beats=sequence.beats + [additional_beat])

# Removing from collections  
sequence = sequence.remove_beat(beat_number=1)

# Transforming collections
new_beats = [beat.update(duration=2.0) for beat in sequence.beats]
sequence = sequence.update(beats=new_beats)
```

### Validation Patterns
```python
# Individual validation
if beat.is_valid():
    sequence = sequence.add_beat(beat)

# Sequence validation
if sequence.is_valid and sequence.length > 0:
    save_sequence(sequence)

# Custom validation
errors = []
if not sequence.name:
    errors.append("Sequence name required")
if sequence.length == 0:
    errors.append("Sequence must have beats")
```

## 🧪 TESTING WITH DOMAIN MODELS

### Fixture Usage
```python
# Use existing sophisticated fixtures
def test_beat_operations(sample_beat_data):
    """Test with real BeatData"""
    beat = sample_beat_data
    updated = beat.update(letter="B")
    assert beat.letter != updated.letter  # Original unchanged

def test_sequence_operations(sample_sequence_data):
    """Test with real SequenceData"""
    sequence = sample_sequence_data
    assert sequence.is_valid
    assert sequence.length > 0
```

### Creating Test Data
```python
# Create valid domain objects for testing
def create_test_beat(letter: str = "A") -> BeatData:
    blue_motion = MotionData(
        motion_type=MotionType.PRO,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.NORTH,
        end_loc=Location.EAST
    )
    
    return BeatData(
        beat_number=1,
        letter=letter,
        blue_motion=blue_motion,
        red_motion=blue_motion  # Simplified for testing
    )
```

## 🚨 COMMON MISTAKES TO AVOID

### DON'T:
```python
# ❌ Try to mutate frozen dataclasses
beat.letter = "B"  # Will raise exception

# ❌ Create incomplete domain objects
beat = BeatData()  # Missing required motion data

# ❌ Ignore validation
sequence.add_beat(invalid_beat)  # Could corrupt sequence

# ❌ Mix domain and UI concerns
beat.ui_color = "red"  # Domain models are UI-agnostic
```

### DO:
```python
# ✅ Use immutable updates
beat = beat.update(letter="B")

# ✅ Create complete domain objects
beat = BeatData(
    beat_number=1,
    letter="A",
    blue_motion=motion_data,
    red_motion=motion_data
)

# ✅ Validate before operations
if beat.is_valid():
    sequence = sequence.add_beat(beat)

# ✅ Keep domain models pure
# UI concerns handled in presentation layer
```

## 📊 SERIALIZATION PATTERNS

### Dictionary Conversion
```python
# To dictionary (for JSON, API, storage)
beat_dict = beat.to_dict()
sequence_dict = sequence.to_dict()
pictograph_dict = pictograph.to_dict()

# From dictionary (for loading, API responses)
beat = BeatData.from_dict(beat_dict)
sequence = SequenceData.from_dict(sequence_dict)
pictograph = PictographData.from_dict(pictograph_dict)
```

### Nested Object Handling
```python
# Nested objects are automatically handled
beat_dict = beat.to_dict()
# Contains: blue_motion as dict, red_motion as dict, glyph_data as dict

# Restoration maintains object integrity
restored_beat = BeatData.from_dict(beat_dict)
assert isinstance(restored_beat.blue_motion, MotionData)
```

## 🎯 KEY TAKEAWAYS FOR AI AGENTS

1. **Immutability is Fundamental**: All operations return new instances
2. **Complex Relationships**: Domain models have sophisticated nested structures
3. **Validation is Built-in**: Use `is_valid()` methods for business rule checking
4. **Serialization is Handled**: Use `to_dict()` and `from_dict()` for persistence
5. **Enums are Everywhere**: Understand the enum types used throughout
6. **Testing Fixtures Exist**: Use existing fixtures rather than creating mock objects

**Work with these sophisticated models correctly and they provide powerful, type-safe, validated business logic operations.**
