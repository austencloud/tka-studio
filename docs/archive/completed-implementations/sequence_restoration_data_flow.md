# TKA Sequence Restoration Data Flow Documentation

## Overview
This document explains how sequence data flows from creation through session saving to restoration and beat frame display in TKA Modern.

## Data Structures Involved

### 1. SequenceData (Domain Model)
```python
@dataclass(frozen=True)
class SequenceData:
    id: str
    name: str
    beats: List[BeatData]
    # Other metadata...
```

### 2. BeatData (Domain Model)
```python
@dataclass(frozen=True)
class BeatData:
    beat_number: int
    letter: str
    duration: float
    blue_motion: Optional[MotionData] = None
    red_motion: Optional[MotionData] = None
    start_position: Optional[StartPositionData] = None
    # Motion data contains arrows, props, orientations
```

### 3. MotionData (Contains Visual Elements)
```python
@dataclass(frozen=True)
class MotionData:
    motion_type: MotionType
    arrow: Optional[ArrowData] = None
    prop: Optional[PropData] = None
    # Arrow and prop data contain visual rendering information
```

### 4. StartPositionData (Contains Orientation)
```python
@dataclass(frozen=True)
class StartPositionData:
    orientation: Orientation  # NORTH, SOUTH, EAST, WEST
    # Contains visual orientation for start position
```

## Complete Data Flow

### Phase 1: Sequence Creation
```
User Creates Sequence
    ↓
SequenceWorkbenchService.create_sequence()
    ↓
Creates SequenceData with empty beats
    ↓
User adds beats with motions/arrows/props
    ↓
BeatData objects created with:
    - motion_type (e.g., STATIC, SHIFT, DASH)
    - arrow data (direction, color)
    - prop data (type, position)
    - start_position (orientation)
```

### Phase 2: Session Saving
```
Sequence Modified
    ↓
SessionStateService.update_current_sequence()
    ↓
SequenceData → Dict conversion via to_dict()
    ↓
BeatData.to_dict() should preserve:
    - blue_motion.to_dict() (arrows, props)
    - red_motion.to_dict() (arrows, props)
    - start_position.to_dict() (orientation)
    ↓
Serialized to session_state.json
```

### Phase 3: Application Restart & Session Loading
```
TKA Startup
    ↓
ApplicationLifecycleManager.initialize_application()
    ↓
SessionStateService.load_session_state()
    ↓
Dict → SequenceData conversion
    ↓
CRITICAL: Dict beats → BeatData.from_dict()
    Must reconstruct:
    - MotionData objects from dicts
    - ArrowData objects from dicts
    - PropData objects from dicts
    - StartPositionData from dicts
```

### Phase 4: UI Restoration
```
ApplicationOrchestrator triggers deferred restoration
    ↓
ApplicationLifecycleManager._apply_restored_session_to_ui()
    ↓
Publishes UIEvent with restored SequenceData
    ↓
SequenceWorkbench._on_sequence_restored()
    ↓
SequenceWorkbench.set_sequence()
    ↓
BeatFrameSection.set_sequence()
    ↓
SequenceBeatFrame.set_sequence()
    ↓
SequenceBeatFrame._update_display()
    ↓
For each beat: BeatView.set_beat_data()
    ↓
CRITICAL: BeatView must render:
    - Arrows from motion data
    - Props from motion data
    - Start position orientation
```

## Critical Points Where Data Can Be Lost

### 1. **Serialization (to_dict)**
- BeatData.to_dict() must include all motion data
- MotionData.to_dict() must preserve arrow/prop details
- StartPositionData.to_dict() must preserve orientation

### 2. **Deserialization (from_dict)**
- BeatData.from_dict() must reconstruct motion objects
- Must handle nested object reconstruction
- Must preserve all visual element data

### 3. **Beat View Rendering**
- BeatView.set_beat_data() must trigger visual updates
- Must render arrows based on motion data
- Must render props based on motion data
- Must set start position orientation

## Expected Session File Structure

```json
{
  "current_sequence": {
    "sequence_id": "seq_123",
    "sequence_data": {
      "id": "seq_123",
      "name": "My Sequence",
      "beats": [
        {
          "beat_number": 1,
          "letter": "A",
          "duration": 1.0,
          "blue_motion": {
            "motion_type": "STATIC",
            "arrow": {
              "direction": "NORTH",
              "color": "BLUE"
            },
            "prop": null
          },
          "red_motion": {
            "motion_type": "SHIFT",
            "arrow": {
              "direction": "SOUTH", 
              "color": "RED"
            },
            "prop": {
              "type": "STAFF",
              "position": "CENTER"
            }
          },
          "start_position": {
            "orientation": "NORTH"
          }
        }
      ]
    }
  }
}
```

## Debugging Checklist

### 1. **Verify Session File Content**
- Check if motion data is present in session_state.json
- Verify arrow and prop data is serialized
- Confirm start position orientation is saved

### 2. **Verify Deserialization**
- Check if BeatData.from_dict() reconstructs motion objects
- Verify MotionData objects contain arrow/prop data
- Confirm StartPositionData contains orientation

### 3. **Verify UI Rendering**
- Check if BeatView.set_beat_data() is called
- Verify beat views render arrows and props
- Confirm start position shows orientation

### 4. **Compare with Working Implementation**
- Check legacy version's serialization format
- Compare motion data structures
- Verify rendering pipeline differences

## Success Criteria

A fully working restoration should:
1. **Save complete motion data** to session file
2. **Load complete motion data** from session file  
3. **Render all visual elements** in beat frame:
   - Arrows pointing in correct directions
   - Props in correct positions
   - Start position with correct orientation
   - Beat numbers and letters
4. **Preserve exact sequence state** across restarts
5. **Handle any sequence length** (not always 3 beats)
