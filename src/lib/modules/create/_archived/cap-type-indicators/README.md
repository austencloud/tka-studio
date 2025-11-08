# CAP Type Indicators Component

## Overview

This component displays visual indicators showing what type of CAP (Continuous Assembly Pattern) a **completed** sequence represents. It was originally implemented for the Create module's WorkspaceHeader but was removed due to visual noise concerns.

## Purpose

The CapTypeIndicators component provides **educational feedback** to users about the pattern type of their completed sequences:

- **Rotated CAP** (90°): Blue badge with `fa-rotate-right` icon
- **Mirrored CAP** (180°): Purple badge with `fa-left-right` icon
- **Rotated-Mirrored CAP**: Pink badge with `fa-arrows-rotate` icon
- **Static Loop CAP**: Green badge with `fa-circle-dot` icon

Each badge includes:

- Font Awesome icon
- Text label (e.g., "90° Rotated")
- Hover tooltip with educational description
- Color-coded gradient background
- Responsive design that hides labels on small screens

## Why It Was Removed from Create module

The component was removed from the Create module because:

1. **Visual Noise**: The colorful badges with educational tooltips added clutter to a productivity-focused interface
2. **Wrong Context**: Educational content belongs in the Learn tab, not in the creation workspace
3. **User Focus**: Create module users want to create sequences without constant educational interruptions
4. **Overwhelming**: Users reported feeling visually overwhelmed during the creative process

## Technical Implementation

### Dependencies

- `ISequenceAnalysisService.detectCompletedCapTypes()` - Analyzes all consecutive beat pairs in a sequence to determine actual CAP type
- Font Awesome icons (already available in the project)
- Svelte 5 with runes (`$state`, `$derived`, `$props`)

### Key Features

1. **Consecutive Beat Analysis**: Unlike simple start→end checks, this properly analyzes every beat transition to detect the actual completed pattern
2. **Responsive Design**: Labels automatically hide on screens < 500px width or height
3. **Tooltip System**: Custom hover tooltips with proper word-wrapping
4. **Accessible**: Includes ARIA labels and semantic HTML

### Usage Example

```svelte
<script lang="ts">
  import CapTypeIndicators from "./CapTypeIndicators.svelte";
  import type { ISequenceAnalysisService } from "$create/shared/services/contracts";
  import { resolve, TYPES } from "$shared/inversify";

  const sequenceAnalysisService = resolve<ISequenceAnalysisService>(
    TYPES.ISequenceAnalysisService
  );

  const capTypes = $derived(() => {
    if (!sequence) return [];
    return sequenceAnalysisService.detectCompletedCapTypes(sequence);
  });
</script>

<CapTypeIndicators capTypes={capTypes()} />
```

## Future Use Cases

This component could be valuable in:

### Learn Tab

- **Codex**: Show CAP types next to sequence examples
- **Quiz**: Educational feedback when users complete pattern exercises
- **Read**: Annotate textbook examples with CAP type badges

### Create module (Optional/Toggleable)

- As a minimal, opt-in feature in settings
- Only show icon (no label) for advanced users
- Collapsible educational panel

### Explore

- Show CAP types for saved sequences
- Filter sequences by CAP type
- Educational annotations on shared sequences

## Implementation Notes

### SequenceAnalysisService Integration

The component requires `detectCompletedCapTypes()` method which:

1. Checks if all beats are at same position → Static CAP
2. Builds consecutive pairs: `beat[i].endPosition → beat[i+1].startPosition`
3. Checks if all pairs show 90° rotation → Rotated CAP
4. Checks if all pairs show mirroring → Mirrored CAP
5. Returns empty array if sequence doesn't match a CAP pattern

### Styling Considerations

- Uses CSS custom properties for color theming
- Gradients auto-generated from base colors
- Animations on hover for polish
- Media queries for responsive text hiding

## Related Files

- `ISequenceAnalysisService.ts` - Interface definition with `detectCompletedCapTypes()` method
- `SequenceAnalysisService.ts` - Implementation of CAP detection algorithm (lines 244-328)
- Position transformation maps:
  - `QUARTERED_CAPS` - 90° rotation patterns
  - `HALVED_CAPS` - 180° mirroring patterns
  - `VERTICAL_MIRROR_POSITION_MAP` - Vertical mirror transformations
  - `SWAPPED_POSITION_MAP` - Position swapping patterns

## Design Philosophy

This component represents the tension between **education** and **productivity**:

- **Education**: Users benefit from understanding pattern theory
- **Productivity**: Users need focus and minimal distractions during creation

The key insight: **Context matters**. Educational features shine in learning contexts but create friction in creative workflows.

## Recommendation for Revival

If reintroducing this component:

1. **Start in Learn Tab**: Add to Quiz or Codex where education is the primary goal
2. **User Testing**: Get feedback on whether it enhances or distracts from learning
3. **Progressive Enhancement**: Only add to Create module if users explicitly request it
4. **Minimal Design**: If added to Build, make it extremely subtle (icon-only, no colors, no tooltips)

---

**Archived**: 2025-10-29
**Original Location**: `src/lib/modules/create/workspace-panel/sequence-display/components/CapTypeIndicators.svelte`
**Decision Maker**: User feedback - "visual noise" concerns
