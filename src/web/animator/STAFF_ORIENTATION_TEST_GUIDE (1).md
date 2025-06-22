# Staff Orientation Test Interface Guide

This guide explains how to use the comprehensive staff orientation test system to systematically define and validate staff orientations at different hand positions.

## Overview

The staff orientation test system consists of:

1. **Interactive Test Interface** (`staff-orientation-test.html`) - Visual tool for defining orientations
2. **Orientation Mapping System** (`orientation-mapping.ts`) - Data management and validation
3. **Integration Utilities** (`orientation-integration.ts`) - Connect test data with animation system
4. **Manual Rotation System** - Apply exact rotation values to sequences

## Getting Started

### 1. Open the Test Interface

Open `staff-orientation-test.html` in your web browser. You'll see:

- **Position Grid**: Visual representation of all hand positions
- **Detail Panel**: Controls for setting orientation angles
- **Export/Import Tools**: Save and load your test data

### 2. Systematic Testing Process

#### Step 1: Select a Position

- Click on any position in the grid (e.g., 'n', 's', 'e', 'w', 'ne', etc.)
- The position will be highlighted and the detail panel will update

#### Step 2: Define Orientations

For the selected position, you'll see 6 orientation controls:

- **'in'**: Staff pointing toward center
- **'out'**: Staff pointing away from center
- **'n'**: Staff pointing north (up)
- **'e'**: Staff pointing east (right)
- **'s'**: Staff pointing south (down)
- **'w'**: Staff pointing west (left)

#### Step 3: Set Rotation Angles

- Enter the desired rotation angle (in degrees) for each orientation
- Watch the visual preview update in real-time
- 0° = horizontal pointing right
- 90° = vertical pointing up
- 180° = horizontal pointing left
- 270° = vertical pointing down

#### Step 4: Validate Visually

- Use the comparison mode to see all orientations side-by-side
- Verify that the staff angles match your expectations
- Adjust angles as needed

### 3. Recommended Testing Workflow

#### Phase 1: Cardinal Positions

Start with the main positions and establish baseline orientations:

1. **Position 'n' (North)**

   - 'in' should point toward center (down) = 270°
   - 'out' should point away from center (up) = 90°
   - 'n', 'e', 's', 'w' should point in their respective directions

2. **Position 's' (South)**

   - 'in' should point toward center (up) = 90°
   - 'out' should point away from center (down) = 270°
   - Continue with directional orientations

3. **Position 'e' (East)**

   - 'in' should point toward center (left) = 180°
   - 'out' should point away from center (right) = 0°

4. **Position 'w' (West)**
   - 'in' should point toward center (right) = 0°
   - 'out' should point away from center (left) = 180°

#### Phase 2: Hand Positions

Test the hand positions (n_hand, e_hand, s_hand, w_hand) which may have different orientation behaviors.

#### Phase 3: Diagonal Positions

Test diagonal positions (ne, se, sw, nw) where 'in' and 'out' orientations point at 45-degree angles.

### 4. Data Management

#### Saving Your Work

- Data is automatically saved to browser localStorage
- Use "Export All Data" to save a JSON file backup
- Use "Export Position" to save data for a specific position

#### Loading Previous Work

- Use "Import Data" to load a previously exported JSON file
- Data will merge with existing data (overwrites duplicates)

#### Resetting Data

- Use "Reset All Data" to clear everything and start over
- This action cannot be undone

## Integration with Animation System

### 1. Export Test Data

Once you've defined all orientations:

```javascript
// Export from test interface
const orientationData = exportAllData(); // Downloads JSON file
```

### 2. Load into Animation System

```typescript
import { loadOrientationMappingsFromJSON } from "./utils/orientation-mapping.js";
import { applyOrientationBasedRotationsToSequence } from "./utils/orientation-integration.js";

// Load your test data
const success = loadOrientationMappingsFromJSON(jsonData);

// Apply to a sequence
const updatedSequence =
  applyOrientationBasedRotationsToSequence(originalSequence);
```

### 3. Use in Sequence Creation

```typescript
import { createPropAttributesWithOrientation } from "./utils/orientation-integration.js";

// Create prop attributes with automatic orientation-based rotation
const blueAttributes = createPropAttributesWithOrientation(
  "s", // start location
  "w", // end location
  "in", // start orientation
  "out", // end orientation
  "pro", // motion type
  "cw", // rotation direction
  0, // turns
);
```

## Advanced Features

### Comparison Mode

- Toggle comparison mode to see all orientations for a position side-by-side
- Useful for ensuring consistency and spotting errors
- Helps visualize the relationship between different orientations

### Validation and Statistics

```typescript
import {
  getOrientationMappingStats,
  validateOrientationMappings,
} from "./utils/orientation-mapping.js";

// Get completion statistics
const stats = getOrientationMappingStats();
console.log(
  `Completed ${stats.completedPositions}/${stats.totalPositions} positions`,
);

// Validate data integrity
const validation = validateOrientationMappings(orientationData);
if (!validation.isValid) {
  console.error("Validation errors:", validation.errors);
}
```

### Export Formats

The system can export data in multiple formats:

```typescript
import { OrientationMappingExporter } from "./utils/orientation-mapping.js";

// JSON for programmatic use
const json = OrientationMappingExporter.toJSON();

// TypeScript constant for code integration
const typescript = OrientationMappingExporter.toTypeScript();

// CSV for spreadsheet analysis
const csv = OrientationMappingExporter.toCSV();

// Markdown table for documentation
const markdown = OrientationMappingExporter.toMarkdown();
```

## Best Practices

### 1. Consistency

- Establish clear rules for 'in' and 'out' orientations
- 'in' should always point toward the center of the grid
- 'out' should always point away from the center
- Directional orientations ('n', 'e', 's', 'w') should be consistent across all positions

### 2. Visual Validation

- Always check the visual preview before moving to the next orientation
- Use comparison mode to spot inconsistencies
- Test edge cases (diagonal positions, center position)

### 3. Documentation

- Export your data regularly as backup
- Document any special rules or exceptions
- Keep notes about your decision-making process

### 4. Iterative Refinement

- Start with rough approximations
- Refine angles based on visual testing
- Test with actual animation sequences to validate

## Troubleshooting

### Common Issues

1. **Angles not updating visually**

   - Check that you're entering valid numbers (0-359)
   - Refresh the page if previews stop updating

2. **Data not saving**

   - Check browser localStorage permissions
   - Export data manually as backup

3. **Import/Export not working**
   - Ensure JSON file format is correct
   - Check browser file access permissions

### Getting Help

If you encounter issues:

1. Check the browser console for error messages
2. Verify your JSON data format matches the expected structure
3. Try resetting data and starting with a clean slate

## Next Steps

After completing your orientation mapping:

1. **Validate with Real Sequences**: Test your mappings with actual animation sequences
2. **Algorithmic Generation**: Create algorithms to generate these mappings programmatically
3. **Integration**: Replace dynamic calculations with your orientation-based system
4. **Documentation**: Create comprehensive documentation of your orientation rules

This systematic approach will give you complete control over staff orientations and provide a solid foundation for programmatic generation of rotation values.
