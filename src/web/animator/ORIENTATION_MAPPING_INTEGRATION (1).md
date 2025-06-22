# Orientation Mapping Integration

This document describes the successful integration of the finalized staff orientation mappings into the pictograph animator system.

## Overview

The orientation mapping system replaces dynamic orientation calculations with precise, manually-validated rotation angles. This ensures consistent and predictable staff orientations across all animations.

## Finalized Orientation Data

The following rotation angles (in degrees) were systematically tested and validated:

```json
{
  "n_hand": { "in": 90, "out": 270, "clockwise": 90, "counter": 180 },
  "e_hand": { "in": 180, "out": 0, "clockwise": 90, "counter": 270 },
  "s_hand": { "in": 270, "out": 90, "clockwise": 180, "counter": 270 },
  "w_hand": { "in": 0, "out": 180, "clockwise": 270, "counter": 90 },
  "ne": { "in": 135, "out": 315, "clockwise": 45, "counter": 225 },
  "se": { "in": 225, "out": 45, "clockwise": 135, "counter": 315 },
  "sw": { "in": 315, "out": 135, "clockwise": 225, "counter": 45 },
  "nw": { "in": 45, "out": 225, "clockwise": 315, "counter": 135 }
}
```

## Integration Architecture

### 1. Core Files Modified

**`src/lib/animator/utils/orientation-mapping.ts`**

- Updated with finalized orientation mappings
- Provides `getOrientationAngle()` and `getOrientationAngleRadians()` functions
- Replaces placeholder data with validated test results

**`src/lib/animator/core/engine/animation-engine.ts`**

- Modified `calculateStaffRotation()` method
- Added orientation mapping lookup before falling back to dynamic calculations
- Maintains backward compatibility with existing motion types

**`src/lib/animator/utils/sequence-orientation-processor.ts`** (New)

- Processes complete sequences to use orientation mappings
- Validates sequence orientation integrity
- Generates processing reports

### 2. Priority System

The animation engine now uses a three-tier priority system for staff rotation:

1. **Manual Rotation Override** (Highest Priority)

   - If `manual_start_rotation` and `manual_end_rotation` are set
   - Used for precise control and testing

2. **Orientation Mapping** (Medium Priority)

   - If `start_ori` and `end_ori` are available
   - Uses finalized orientation mappings for consistent results

3. **Dynamic Calculations** (Fallback)
   - Original motion type calculations (pro, anti, static, dash, fl)
   - Used when orientation data is missing

### 3. Key Functions

**Orientation Lookup:**

```typescript
import {
  getOrientationAngle,
  getOrientationAngleRadians,
} from "./utils/orientation-mapping.js";

// Get angle in degrees
const angle = getOrientationAngle("n_hand", "in"); // Returns 90

// Get angle in radians for calculations
const radians = getOrientationAngleRadians("n_hand", "in"); // Returns π/2
```

**Sequence Processing:**

```typescript
import { processSequenceWithOrientationMappings } from "./utils/sequence-orientation-processor.js";

// Process entire sequence to use orientation mappings
const processedSequence =
  processSequenceWithOrientationMappings(originalSequence);
```

**Validation:**

```typescript
import { validateSequenceOrientationIntegrity } from "./utils/sequence-orientation-processor.js";

// Validate orientation continuity
const validation = validateSequenceOrientationIntegrity(sequenceData);
if (!validation.isValid) {
  console.error("Orientation continuity errors:", validation.errors);
}
```

## Data Integrity Requirements

### Orientation Continuity

The system assumes that `end_ori` of beat N always matches `start_ori` of beat N+1:

```
Beat 1: start_ori='in', end_ori='out'
Beat 2: start_ori='out', end_ori='clockwise'  ✓ Valid
Beat 3: start_ori='in', end_ori='counter'     ✗ Invalid (should start with 'clockwise')
```

### Validation Function

Use `validateSequenceOrientationIntegrity()` to check for:

- Missing orientation data
- Broken orientation continuity between beats
- Invalid orientation values

## Migration Guide

### For Existing Sequences

1. **Automatic Integration**: The animation engine automatically uses orientation mappings when available
2. **Backward Compatibility**: Sequences without orientation data continue to use dynamic calculations
3. **Gradual Migration**: Add `start_ori` and `end_ori` to sequence steps to enable orientation mapping

### For New Sequences

1. **Always Include Orientations**: Set `start_ori` and `end_ori` for all sequence steps
2. **Validate Continuity**: Use validation functions to ensure orientation continuity
3. **Test Thoroughly**: Verify that orientation mappings produce expected visual results

## Benefits

### 1. Consistency

- **Predictable Results**: Same orientation always produces same rotation angle
- **Visual Consistency**: Staff orientations look identical across different sequences
- **No Motion Type Dependencies**: Orientation is independent of motion type

### 2. Precision

- **Manually Validated**: Every angle was tested and validated through the test interface
- **Exact Control**: Precise rotation angles instead of calculated approximations
- **Visual Accuracy**: Orientations match exactly what was defined in the test interface

### 3. Maintainability

- **Clear Data**: Orientation mappings are easy to understand and modify
- **Centralized Control**: All orientation logic in one place
- **Easy Testing**: Simple lookup functions for unit testing

## Testing

### Unit Tests

```typescript
import { getOrientationAngle } from "./utils/orientation-mapping.js";

// Test specific orientation mappings
expect(getOrientationAngle("n_hand", "in")).toBe(90);
expect(getOrientationAngle("e_hand", "out")).toBe(0);
```

### Integration Tests

```typescript
import { processSequenceWithOrientationMappings } from "./utils/sequence-orientation-processor.js";

// Test sequence processing
const processed = processSequenceWithOrientationMappings(testSequence);
expect(processed[1].blue_attributes.manual_start_rotation).toBeDefined();
```

### Visual Testing

Use the staff orientation test interface (`staff-orientation-test.html`) to:

- Verify orientation mappings visually
- Test new orientation combinations
- Validate changes before integration

## Future Enhancements

### 1. Center Position

- Add center position orientation mappings when needed
- Extend test interface to include center position

### 2. Custom Orientations

- Support for additional orientation types beyond the current 4
- Dynamic orientation mapping updates

### 3. Animation Transitions

- Smooth transition algorithms between orientation mappings
- Advanced interpolation for complex orientation changes

## Troubleshooting

### Common Issues

1. **Missing Orientation Data**

   - Error: `Failed to get orientation mapping`
   - Solution: Ensure `start_ori` and `end_ori` are set in sequence data

2. **Orientation Continuity Errors**

   - Error: Validation reports continuity mismatches
   - Solution: Fix sequence data so end_ori matches next start_ori

3. **Unexpected Rotation Angles**
   - Issue: Staff doesn't rotate as expected
   - Solution: Verify orientation mappings in test interface

### Debug Tools

- **Console Logging**: Animation engine logs orientation mapping usage
- **Validation Reports**: Use validation functions to identify issues
- **Test Interface**: Visual verification of orientation mappings

This integration successfully replaces dynamic orientation calculations with precise, manually-validated rotation angles, providing consistent and predictable staff orientations throughout the animation system.
