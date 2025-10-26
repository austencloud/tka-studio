# Animation Architecture: Position vs Rotation

## 🎯 Core Concept: Two Independent Coordinate Systems

The animation system uses **TWO SEPARATE** angle measurements that work together## 🔄 Motion Type Examples

### **STATIC Motion** (N-IN → N-IN, 0 turns)
```
Position: N (π/2) → N (π/2)         (STAYS at same location!)
Rotation: IN (3π/2) → IN (3π/2)     (orientation ALSO stays same with 0 turns)

centerPathAngle:    1.57 → 1.57     (NO position change)
staffRotationAngle: 4.71 → 4.71     (NO rotation with 0 turns!)
```

**CRITICAL STATIC RULES:**
- Position NEVER changes (N → N, E → E, etc.)
- End orientation is CALCULATED from turns:
  - **0 or 2 turns:** Orientation STAYS SAME (IN → IN, OUT → OUT)
  - **1 or 3 turns:** Orientation FLIPS (IN → OUT, OUT → IN)
- 0 turns = literally does NOTHING (stays completely still)
- STATIC is **never** N→E or N→W, always same location!

### **STATIC Motion** (N-IN → N-OUT, 1 turn)
```
Position: N (π/2) → N (π/2)         (position stays)
Rotation: 1 full turn flips orientation

centerPathAngle:    1.57 → 1.57     (NO position change)
staffRotationAngle: 4.71 → 4.71+2π  (1 turn, ends at OUT)letely different purposes:

### 1. **Center Path Angle** (`centerPathAngle`)
**What it controls:** WHERE the prop's center point is located on the circular grid
- **Range:** 0 to 2π radians (0° to 360°)
- **Reference:** Measured from the grid center
- **Maps to:** Grid locations (N, NE, E, SE, S, SW, W, NW)
- **Used for:** Calculating prop position (x, y coordinates)

```
         N (π/2)
         ↑
    NW ⟋   ⟍ NE
W ← ●────┼────● → E (0 or 2π)
    SW ⟍   ⟋ SE
         ↓
         S (3π/2)
```

### 2. **Staff Rotation Angle** (`staffRotationAngle`)
**What it controls:** HOW the staff is rotated at that location
- **Range:** 0 to 2π radians (0° to 360°)
- **Reference:** Absolute rotation of the staff itself
- **Maps to:** Orientations (IN, OUT, CLOCK, COUNTER)
- **Used for:** Rotating the staff image on canvas

```
Staff at location with different rotations:
  IN ↓    OUT ↑    CLOCK →    COUNTER ←
  ──●     ──●      ──●         ──●
    │       │        /           \
```

---

## 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      DOMAIN DATA                             │
│  MotionData { startLocation, endLocation,                   │
│               startOrientation, endOrientation,              │
│               motionType, turns, rotationDirection }         │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│              ENDPOINT CALCULATION LAYER                      │
│  EndpointCalculator.calculateMotionEndpoints()              │
│                                                               │
│  Converts domain data into angles:                          │
│  ┌─────────────────────────────────────────┐                │
│  │ startCenterAngle    ← GridLocation      │                │
│  │ targetCenterAngle   ← GridLocation      │                │
│  │ startStaffAngle     ← Orientation       │                │
│  │ targetStaffAngle    ← Motion rules      │                │
│  └─────────────────────────────────────────┘                │
│                                                               │
│  Uses: AngleCalculator, MotionCalculator                    │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│              INTERPOLATION LAYER                             │
│  PropInterpolator.interpolatePropAngles()                   │
│                                                               │
│  Calculates current frame values:                           │
│  ┌─────────────────────────────────────────┐                │
│  │ centerPathAngle    = lerp(start, end)   │ ← Position     │
│  │ staffRotationAngle = lerp(start, end)   │ ← Rotation     │
│  │ (x, y)            = dash calculation    │ ← Optional     │
│  └─────────────────────────────────────────┘                │
│                                                               │
│  Special case: DASH motions use Cartesian x,y              │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                   PROP STATE                                 │
│  PropState {                                                 │
│    centerPathAngle: number    ← WHERE on grid               │
│    staffRotationAngle: number ← HOW rotated                 │
│    x?: number                 ← Optional (DASH only)        │
│    y?: number                 ← Optional (DASH only)        │
│  }                                                           │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│              RENDERING LAYER                                 │
│  CanvasRenderer.drawStaff()                                 │
│                                                               │
│  Step 1: Calculate prop CENTER position                     │
│  ┌─────────────────────────────────────────┐                │
│  │ if (x, y provided):                      │                │
│  │   Use x, y directly (DASH motion)       │                │
│  │ else:                                    │                │
│  │   x = cos(centerPathAngle) * radius     │ ← FROM ANGLE   │
│  │   y = sin(centerPathAngle) * radius     │                │
│  └─────────────────────────────────────────┘                │
│                                                               │
│  Step 2: Rotate staff around that center                    │
│  ┌─────────────────────────────────────────┐                │
│  │ ctx.translate(x, y)                      │                │
│  │ ctx.rotate(staffRotationAngle)          │ ← APPLY ROTATION│
│  │ ctx.drawImage(staffImage)                │                │
│  └─────────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 Key Services & Their Responsibilities

### **EndpointCalculator**
🎯 **Purpose:** Convert domain locations → angles
```typescript
calculateMotionEndpoints(motionData: MotionData): MotionEndpoints {
  // POSITION angles (WHERE)
  startCenterAngle   = mapPositionToAngle(startLocation)
  targetCenterAngle  = mapPositionToAngle(endLocation)

  // ROTATION angles (HOW)
  startStaffAngle    = mapOrientationToAngle(startOrientation, startCenterAngle)
  targetStaffAngle   = calculateByMotionType(motionType, ...)
}
```

### **PropInterpolator**
🎯 **Purpose:** Interpolate between start/end angles for current frame
```typescript
interpolatePropAngles(beatData, progress): InterpolationResult {
  // Interpolate POSITION angle
  centerPathAngle = lerpAngle(startCenterAngle, targetCenterAngle, progress)

  // Interpolate ROTATION angle (INDEPENDENT!)
  staffRotationAngle = lerpAngle(startStaffAngle, targetStaffAngle, progress)
}
```

### **AngleCalculator**
🎯 **Purpose:** Core angle utilities (mapping, normalization, interpolation)
```typescript
// Convert location → angle (POSITION)
mapPositionToAngle(GridLocation): number

// Convert orientation → angle (ROTATION)
mapOrientationToAngle(Orientation, centerPathAngle): number

// Interpolate with wraparound
lerpAngle(start, end, progress): number
```

### **MotionCalculator**
🎯 **Purpose:** Calculate target staff angles based on motion physics
```typescript
// Different motion types have different ROTATION rules
calculateProTargetAngle(...)        // Pro: turns with center motion
calculateAntispinTargetAngle(...)   // Anti: turns against center motion
calculateStaticStaffAngle(...)      // Static: orientation change only
calculateDashTargetAngle(...)       // Dash: straight-line motion
calculateFloatStaffAngle(...)       // Float: staff stays same
```

### **CanvasRenderer**
🎯 **Purpose:** Convert angles → screen coordinates and render
```typescript
drawStaff(propState: PropState) {
  // Step 1: POSITION (WHERE to place prop center)
  if (propState.x && propState.y) {
    // Dash: use Cartesian coordinates
    x = propState.x * radius
    y = propState.y * radius
  } else {
    // Regular: convert angle to coordinates
    x = cos(propState.centerPathAngle) * radius
    y = sin(propState.centerPathAngle) * radius
  }

  // Step 2: ROTATION (HOW to rotate staff at that position)
  ctx.translate(x, y)
  ctx.rotate(propState.staffRotationAngle)
  ctx.drawImage(staffImage)
}
```

---

## 🔄 Motion Type Examples

### **STATIC Motion** (N-IN → N-OUT, 0 turns)
```
Position: N (π/2) → N (π/2)         (STAYS at same location!)
Rotation: IN (3π/2) → OUT (π/2)     (orientation changes)

centerPathAngle:    1.57 → 1.57     (NO position change)
staffRotationAngle: 4.71 → 1.57     (rotates from pointing in to out)
```

**Note:** STATIC means position NEVER changes. Only orientation can change.
- N-IN → N-IN (0 turns): Literally does nothing, stays completely still
- N-IN → N-OUT: Position stays at N, staff rotates from IN to OUT orientation
- STATIC is **never** N→E or N→W, always same location!

```

### **PRO Motion with 1 turn** (N-IN → E-IN, CW)
```
Position: N (π/2) → E (0)           (moves 90° around circle)
Rotation: 1 full turn + follows path

centerPathAngle:    1.57 → 0.00     (moves right 90°)
staffRotationAngle: 4.71 → 4.71+2π-π/2  (1 turn CW + follows path motion)
```

**PRO RULES:**
- Position CHANGES (moves around grid)
- Rotation = (turns × 2π) - path movement
- Odd turns (1, 3): Orientation FLIPS
- Even turns (0, 2): Orientation STAYS SAME

### **DASH Motion** (N → S, through center)
```
Position: N (π/2) → S (3π/2)        (straight line through CENTER!)
Uses x,y coordinates for straight-line movement

centerPathAngle:    1.57 → 4.71     (opposite side)
staffRotationAngle: calculated      (staff rotation)
x: 0.0 → 0.0                        (stays on vertical axis)
y: 1.0 → -1.0                       (top to bottom)
```

**CRITICAL DASH RULES:**
- DASH **ONLY** goes to **opposite** side through center
- Valid: N↔S, E↔W, NE↔SW, NW↔SE
- Invalid: N→E, N→W, E→S (these are PRO, ANTI, or FLOAT)
- Orientation calculation (like ANTI):
  - **Even turns (0, 2):** Orientation FLIPS
  - **Odd turns (1, 3):** Orientation STAYS SAME

### **FLOAT Motion** (N-IN → E-IN)
```
Position: N (π/2) → E (0)           (moves around circle)
Rotation: Staff angle STAYS THE SAME (floats)

centerPathAngle:    1.57 → 0.00     (moves right)
staffRotationAngle: 4.71 → 4.71     (NO rotation, just "floats")
```

**FLOAT RULES:**
- Position CHANGES
- Rotation NEVER changes
- Staff maintains absolute angle regardless of path motion

---

## 🧩 Why Two Separate Angles?

### **Independence of Concerns**

The prop can be at **any location** with **any rotation**:

- Staff pointing IN at North ≠ Staff pointing OUT at North
- Same position, different rotation
- This is **impossible** with a single angle!

### **Motion Physics**

Different motion types have different rotation rules:

- **STATIC:** Position NEVER changes. Orientation from turns (even=same, odd=flip)
- **PRO:** Position changes. Rotation = turns - path. Orientation from turns (even=same, odd=flip)
- **ANTI:** Position changes. Rotation = turns + path. Orientation from turns (even=flip, odd=same)
- **FLOAT:** Position changes. Rotation stays same. Orientation from handpath direction
- **DASH:** Straight through center to opposite. Orientation like ANTI (even=flip, odd=same)
```
Position: N (π/2) → E (0)           (moves around circle)
Rotation: 1 full turn + follows path

centerPathAngle:    1.57 → 0.00     (moves right 90°)
staffRotationAngle: 4.71 → 2π+0     (1 turn + follows to new position)
```

### **DASH Motion** (N → S, through center)
```
Position: N (π/2) → S (3π/2)        (straight line through CENTER!)
Uses x,y coordinates for straight-line movement

centerPathAngle:    1.57 → 4.71     (opposite side)
staffRotationAngle: calculated      (staff rotation)
x: 0.0 → 0.0                        (stays on vertical axis)
y: 1.0 → -1.0                       (top to bottom)
```

**Note:** DASH only goes to **opposite** side through center:
- Valid: N↔S, E↔W, NE↔SW, NW↔SE
- Invalid: N→E, N→W, E→S (these are PRO, ANTI, or FLOAT)

### **FLOAT Motion** (N-IN → E-IN)
```
Position: N (π/2) → E (0)           (moves around circle)
Rotation: Staff angle STAYS THE SAME (floats)

centerPathAngle:    1.57 → 0.00     (moves right)
staffRotationAngle: 4.71 → 4.71     (NO rotation, just "floats")
```

---

## 🧩 Why Two Separate Angles?

### **Independence of Concerns**
The prop can be at **any location** with **any rotation**:
- Staff pointing IN at North ≠ Staff pointing OUT at North
- Same position, different rotation
- This is **impossible** with a single angle!

### **Motion Physics**
Different motion types have different rotation rules:
- **PRO:** Staff rotates WITH the path motion + extra turns
- **ANTI:** Staff rotates AGAINST the path motion
- **STATIC:** Only rotation changes, position stays or moves
- **FLOAT:** Position changes, rotation stays same
- **DASH:** Both change, but position follows straight line

### **Orientation Mapping**
Grid orientations are **relative to position**:
```typescript
// IN: points toward center (centerPathAngle + π)
// OUT: points away from center (centerPathAngle)
// CLOCK: perpendicular CW (centerPathAngle + π/2)
// COUNTER: perpendicular CCW (centerPathAngle - π/2)
```

This means orientation depends on BOTH the position angle AND the orientation type!

---

## 📐 Mathematical Foundation

### **Polar Coordinates** (Regular Motions)
```
Position:  (r, θ) where θ = centerPathAngle
Cartesian: x = r × cos(θ)
           y = r × sin(θ)
Rotation:  Applied AFTER translation
```

### **Cartesian Coordinates** (DASH Motions)
```
Position:  (x, y) directly specified
No angle:  Don't use centerPathAngle for position
Rotation:  Still uses staffRotationAngle
```

---

## 🎨 Visual Mental Model

```
    POSITION (centerPathAngle)           ROTATION (staffRotationAngle)
    WHERE is the prop center?            HOW is the staff rotated?

         ●                                      |
        ╱│╲                                    ╱
       ╱ │ ╲                                  ●
      ╱  │  ╲                                  ╲
     ╱   ●   ╲                                  |
    ╱  ╱   ╲  ╲
   ╱  ╱     ╲  ╲                         All 4 rotations
  ●──●───●───●──●                        possible at any
     ╲       ╱                            single position!
      ╲     ╱
       ╲   ╱
        ╲ ╱
         ●

  8 positions on grid              ×    4 orientations at each
  = centerPathAngle                     = staffRotationAngle
```

---

## 🚀 Performance Implications

### **Why Separate?**
1. **Clarity:** Each angle has ONE job
2. **Flexibility:** Can interpolate independently
3. **Efficiency:** Don't recalculate position from rotation
4. **Correctness:** Motion physics require independent control

### **Optimization:**
- DASH motions pre-calculate x,y to avoid angle → coordinate conversion
- Other motions calculate coordinates on-the-fly from angle (cheaper)

---

## 📝 Summary

| Aspect | Center Path Angle | Staff Rotation Angle |
|--------|-------------------|----------------------|
| **Controls** | Prop center position | Staff visual rotation |
| **Domain** | GridLocation (N, E, S, W) | Orientation (IN, OUT, CLOCK, COUNTER) |
| **Calculation** | Direct mapping from location | Depends on motion type + turns |
| **Interpolation** | Linear angle interpolation | Linear angle interpolation |
| **Rendering** | → (x, y) coordinates | → canvas rotation |
| **Independence** | Can change alone | Can change alone |
| **Dependencies** | → Used to calculate staff angle | None (absolute rotation) |

**The key insight:** These are **two orthogonal dimensions** of prop state, like position (x,y) and rotation in 2D graphics!

---

## 📊 Orientation Calculation Rules (by OrientationCalculator)

**CRITICAL:** End orientation is NOT arbitrary—it's calculated from motion type and turns!

### Orientation Flip Rules

| Motion Type | 0 Turns | 1 Turn | 2 Turns | 3 Turns |
|-------------|---------|---------|---------|---------|
| **STATIC** | Same | **Flip** | Same | **Flip** |
| **PRO** | Same | **Flip** | Same | **Flip** |
| **ANTI** | **Flip** | Same | **Flip** | Same |
| **DASH** | **Flip** | Same | **Flip** | Same |
| **FLOAT** | _Calculated from handpath_ | N/A | N/A | N/A |

**"Same"** = IN→IN, OUT→OUT, CLOCK→CLOCK, COUNTER→COUNTER

**"Flip"** = IN→OUT, OUT→IN, CLOCK→COUNTER, COUNTER→CLOCK

### Code Location

The **source of truth** for orientation calculation is:
```
src/lib/shared/pictograph/prop/services/implementations/OrientationCalculator.ts
```

This service implements the `calculateEndOrientation()` method that enforces these rules during sequence generation.

**Animation services** receive already-calculated orientations from domain data and simply interpolate between them.
