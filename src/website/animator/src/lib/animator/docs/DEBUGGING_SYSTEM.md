# Sequence Interpretation Debugging System

## Overview

The Sequence Interpretation Debugging System is a comprehensive tool for analyzing, validating, and debugging the pictograph sequence interpretation logic in the SvelteKit Sequence Animator. It provides hands-on control and verification of how sequence data translates into staff animations.

## Architecture

### Core Components

1. **SequenceDebugger** (`src/lib/animator/core/debug/sequence-debugger.ts`)

   - Main debugging engine
   - Handles beat-by-beat analysis
   - Manages validation and session tracking
   - Provides event-driven architecture

2. **SequenceDebugModal** (`src/lib/animator/components/debug/SequenceDebugModal.svelte`)

   - Main modal interface
   - Tabbed navigation system
   - Keyboard shortcuts support
   - Responsive design

3. **Debug Components**
   - `DebugOverview.svelte` - Summary and table view
   - `BeatEditor.svelte` - Manual override system
   - `ValidationPanel.svelte` - Issue tracking
   - `ConfigurationPanel.svelte` - Settings management
   - `ExportPanel.svelte` - Data export functionality

### Data Flow

```
Sequence Data → SequenceDebugger → Analysis Engine → Validation → UI Components
                      ↓
              Beat-by-Beat Processing → PropDebugInfo → Validation Results
                      ↓
              Override System → Modified Attributes → Re-analysis
```

## Features

### 1. Beat-by-Beat Analysis

The system analyzes each beat of the sequence and provides:

- **Prop State Calculation**: Current coordinates, rotation angles, center path angles
- **Interpretation Analysis**: Motion type processing, rotation calculations, orientation tracking
- **Validation Results**: Continuity checks, turn count accuracy, error detection

### 2. Interactive Debugging Interface

#### Overview Tab

- Summary statistics (total beats, validation results, motion type breakdown)
- Filterable and sortable beat table
- Issue highlighting and navigation
- Real-time analysis progress

#### Beat Editor Tab

- Manual override system for individual beats
- Attribute modification (motion type, orientations, turns, locations)
- Live preview and comparison modes
- Validation feedback for changes

#### Validation Tab

- Comprehensive issue tracking
- Categorized warnings and errors
- Detailed validation breakdowns
- Orientation continuity analysis
- Turn count accuracy verification

#### Configuration Tab

- Debug system settings
- Capture mode configuration
- Validation level adjustment
- History management options

#### Export Tab

- Multiple export formats (JSON, CSV, Report)
- Configurable data filtering
- Validation summary inclusion
- Session metadata export

### 3. Validation System

The debugging system performs comprehensive validation:

#### Orientation Continuity

- Verifies that each beat's end orientation matches the next beat's start orientation
- Detects discontinuities that cause visual jumps
- Provides angle difference calculations

#### Turn Count Accuracy

- Compares expected turns (from sequence data) with calculated rotations
- Identifies discrepancies in rotation interpretation
- Supports tolerance-based validation

#### Motion Type Validation

- Validates motion type-specific calculations
- Checks for undefined or invalid attributes
- Provides motion-specific error messages

### 4. Override System

The beat editor allows manual overrides for testing:

- **Attribute Overrides**: Modify motion type, orientations, turns, locations
- **Live Preview**: See changes immediately in the animation
- **Comparison Mode**: Side-by-side view of original vs modified
- **Batch Application**: Apply overrides to multiple beats

## Usage

### Basic Usage

1. **Open Debug Modal**: Click the debug button or press `Shift+F12`
2. **Analyze Sequence**: The system automatically analyzes all beats
3. **Review Results**: Use the Overview tab to see summary and issues
4. **Edit Beats**: Use the Beat Editor to modify problematic beats
5. **Validate Changes**: Check the Validation tab for improvements
6. **Export Data**: Use the Export tab to save debugging session

### Advanced Features

#### Keyboard Shortcuts

- `Escape`: Close modal
- `Ctrl+1-5`: Switch between tabs
- `Shift+F12`: Toggle debug modal

#### Configuration Options

- **Capture Mode**: Real-time, manual, or step-by-step analysis
- **Validation Level**: Basic, detailed, or comprehensive checks
- **History Management**: Control data retention and memory usage

#### Export Formats

- **JSON**: Complete structured data for programmatic analysis
- **CSV**: Spreadsheet-compatible format for data analysis
- **Report**: Human-readable text report for documentation

## Integration

### Adding to Components

```svelte
<script>
	import DebugButton from '$lib/animator/components/debug/DebugButton.svelte';

	let sequenceData = $state(null);
</script>

<DebugButton {sequenceData} position="bottom-right" />
```

### Programmatic Usage

```typescript
import { SequenceDebugger } from '$lib/animator/core/debug/sequence-debugger.js';

const debugger = new SequenceDebugger({
  enabled: true,
  captureMode: 'manual',
  validationLevel: 'comprehensive'
});

const session = debugger.startSession(sequenceData);
const beatInfo = debugger.analyzeBeat(1);
```

## Sequence Interpretation Pipeline Documentation

### Current Implementation Analysis

Based on the codebase analysis, here's the complete sequence interpretation pipeline:

#### 1. Data Flow

```
Raw Sequence JSON → Animation Engine → Prop Calculations → Canvas Rendering
```

#### 2. Key Components

**Animation Engine** (`animation-engine.ts`):

- Manages beat timing and interpolation
- Calculates prop states for each frame
- Handles start position vs animation frames

**Prop Calculations** (`prop-calculations.ts`):

- Motion type-specific rotation calculations
- Orientation angle conversions
- Center path angle computations

**Sequence Interpretation** (`sequence-interpretation.ts`):

- Turn-to-degrees mapping
- Orientation-to-angle mapping
- Rotation direction multipliers

#### 3. Motion Type Processing

**Pro Motion**:

- Float (0 turns): 90-degree rotation canceling center path
- Standard: Orientation change + turn rotation with direction

**Anti Motion**:

- Anti-spin calculation with center path consideration
- Turn rotation applied with direction multiplier

**Static Motion**:

- Staff maintains orientation relative to center
- No additional rotation beyond orientation alignment

**Dash Motion**:

- Linear interpolation between start and end orientations
- Shortest angular path calculation

#### 4. Known Issues Identified

**Turn Count Mismatch**:

- Animated rotations don't always match sequence "turns" values
- Float motion (0 turns) shows 90-degree rotation instead of 0

**Orientation Discontinuity**:

- End orientation of beat N doesn't match start orientation of beat N+1
- Causes visual jumps in staff orientation

**Center Point Flipping**:

- Staff orientation flips when passing through center during dash motions
- Inconsistent reference system between staff image and grid position

**Reference System Confusion**:

- Staff image orientation vs grid position calculations use different reference frames
- Rotation calculations may be applied in wrong coordinate system

## Troubleshooting

### Common Issues

1. **Modal Won't Open**

   - Check if sequence data is loaded
   - Verify debug button is not disabled
   - Try keyboard shortcut `Shift+F12`

2. **Analysis Fails**

   - Check browser console for errors
   - Verify sequence data format
   - Try with smaller sequence data

3. **Performance Issues**
   - Reduce max history size in configuration
   - Use manual capture mode instead of real-time
   - Filter data before export

### Debug Information

The system provides extensive debug information:

- Calculation methods used for each motion type
- Intermediate values in rotation calculations
- Validation failure reasons
- Performance metrics

## Future Enhancements

### Planned Features

1. **Graph Visualization**: Visual representation of rotation angles over time
2. **Timeline View**: Interactive timeline for beat navigation
3. **Automated Fixes**: Suggested corrections for common issues
4. **Batch Validation**: Validate multiple sequences simultaneously
5. **Plugin System**: Extensible validation rules

### API Extensions

1. **Custom Validators**: Register custom validation functions
2. **Export Plugins**: Custom export format support
3. **Integration Hooks**: Callbacks for external tools
4. **Real-time Monitoring**: Live validation during animation playback

## Contributing

When extending the debugging system:

1. Follow the existing component structure
2. Use TypeScript for type safety
3. Maintain responsive design patterns
4. Add comprehensive validation
5. Include export functionality
6. Document new features

## Performance Considerations

- Use `$derived` for computed values
- Implement virtual scrolling for large datasets
- Debounce validation checks
- Lazy load debug components
- Optimize export file sizes

## Security Notes

- Debug data may contain sensitive sequence information
- Export files should be handled securely
- Consider data retention policies
- Implement access controls if needed
