# Manual Rotation System

This document describes the new manual rotation input system that allows you to directly specify staff rotation values instead of relying on dynamic calculations.

## Overview

The manual rotation system extends the existing `PropAttributes` interface with optional fields that override the dynamic rotation calculations. When manual rotation values are present, they take precedence over the motion type calculations.

## Key Files and Locations

### 1. Type Definitions

**File:** `src/lib/animator/types/core.ts`

- Extended `PropAttributes` interface with manual rotation fields:
  - `manual_start_rotation?: number` (in radians)
  - `manual_end_rotation?: number` (in radians)
  - `manual_rotation_direction?: 'cw' | 'ccw' | 'shortest'`

### 2. Core Manual Rotation Utilities

**File:** `src/lib/animator/utils/manual-rotation.ts`

- `setManualRotationDegrees()` - Set rotation values in degrees
- `setManualRotationRadians()` - Set rotation values in radians
- `calculateManualStaffRotation()` - Calculate rotation at time t
- `hasManualRotation()` - Check if manual rotation is set
- `clearManualRotation()` - Remove manual rotation values
- `validateManualRotation()` - Validate manual rotation inputs

### 3. Animation Engine Integration

**File:** `src/lib/animator/core/engine/animation-engine.ts`

- Modified `calculateStaffRotation()` method to check for manual rotation first
- Falls back to dynamic calculations only if manual rotation is not specified

### 4. Preset Utilities

**File:** `src/lib/animator/utils/rotation-presets.ts`

- Common rotation presets (quarter turns, half turns, full turns, etc.)
- Motion type specific presets (pro isolation, float, static)
- Batch application utilities for multiple steps

### 5. Validation Integration

**File:** `src/lib/animator/utils/validation/input-validator.ts`

- Added manual rotation validation to `validatePropAttributes()`

## Usage Examples

### Basic Manual Rotation

```typescript
import { setManualRotationDegrees } from "./utils/manual-rotation.js";

// Set blue prop to rotate from 0° to 90° clockwise
step.blue_attributes = setManualRotationDegrees(
  step.blue_attributes,
  0, // start degrees
  90, // end degrees
  "cw", // direction
);
```

### Using Presets

```typescript
import { MOTION_TYPE_PRESETS } from "./utils/rotation-presets.js";

// Apply pro isolation preset (90° rotation)
step.blue_attributes = MOTION_TYPE_PRESETS.pro_isolation_cw(
  step.blue_attributes,
);

// Apply float preset (no rotation)
step.red_attributes = MOTION_TYPE_PRESETS.float_no_rotation(
  step.red_attributes,
);
```

### Batch Application

```typescript
import { applyManualRotationsToSteps } from "./utils/rotation-presets.js";

const rotationMap = {
  1: {
    blue: { start: 0, end: 90, direction: "cw" },
    red: { start: 0, end: -90, direction: "ccw" },
  },
  2: {
    blue: { start: 90, end: 450, direction: "cw" }, // 1 full turn + 90°
    red: { start: -90, end: -90, direction: "shortest" },
  },
};

const updatedSteps = applyManualRotationsToSteps(steps, rotationMap);
```

## How It Works

1. **Priority System**: Manual rotation values take precedence over dynamic calculations
2. **Interpolation**: Rotation is interpolated between start and end values based on time `t`
3. **Direction Control**: You can force clockwise, counter-clockwise, or shortest path rotation
4. **Validation**: Input validation ensures rotation values are valid numbers
5. **Fallback**: If no manual rotation is specified, the system falls back to the original dynamic calculations

## Advantages

1. **Direct Control**: Specify exact rotation values without complex motion type logic
2. **Predictable Results**: Know exactly what rotation will occur
3. **Easy Testing**: Set specific values to test and verify behavior
4. **Clean Data**: Once you confirm the manual values work correctly, you can later algorithmically generate them

## Migration Path

1. **Phase 1** (Current): Use manual rotation system to input and test exact values
2. **Phase 2** (Future): Once you have clean, confirmed data, create algorithms to generate these manual values programmatically
3. **Phase 3** (Optional): Replace dynamic calculations with the new algorithmic approach

## Testing

Run the test suite to verify the manual rotation system:

```bash
npm test src/lib/animator/manual-rotation.test.ts
```

## Example Files

- `examples/manual-rotation-usage.ts` - Comprehensive usage examples
- `src/lib/animator/manual-rotation.test.ts` - Test suite

## Next Steps

1. Use the manual rotation system to input your desired rotation values
2. Test and verify the behavior matches your expectations
3. Once you have a complete set of clean data, we can create algorithms to generate these values programmatically
4. Eventually replace the dynamic calculation system with your new algorithmic approach

This system gives you complete control over staff rotations while maintaining backward compatibility with the existing motion type system.
