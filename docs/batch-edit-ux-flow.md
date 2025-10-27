# Batch Edit UX Flow - Complete Design
## The Kinetic Alphabet - Multi-Select User Experience

**Status:** Design Proposal
**Created:** January 2025
**Purpose:** Define complete user flow for batch editing beats

---

## Complete User Flow

### Step 1: Activation - Long Press

**User Action:** Long-press any beat (500ms hold)

**System Response:**
- Haptic feedback at 500ms
- Beat highlights with glow
- Mode selection panel slides up from bottom

```
┌─────────────────────────────────────┐
│                                     │
│     [Beat Grid - Normal View]       │
│                                     │
│         👇 User long-presses         │
│         [Beat highlighted]          │
│                                     │
└─────────────────────────────────────┘
                 ↓
        [Haptic vibration]
                 ↓
┌─────────────────────────────────────┐
│ ══════ Selection Mode               │ ← Slides up
├─────────────────────────────────────┤
│                                     │
│  📍 Multi-Select                    │
│     Tap individual beats to select  │
│                                     │
│  ↔️  Select Row                     │
│     Select entire horizontal row    │
│                                     │
│  ↕️  Select Column                  │
│     Select entire vertical column   │
│                                     │
│                      [Cancel]       │
└─────────────────────────────────────┘
```

**Design Notes:**
- Panel is 40% screen height
- Large touch targets (60px min)
- Icons make options scannable
- Descriptions clarify each mode
- Cancel button always visible

---

### Step 2A: Multi-Select Mode

**User Action:** Taps "Multi-Select"

**System Response:**
- Panel shrinks to toolbar at bottom
- Initial beat gets checkbox (checked)
- Instruction hint appears briefly
- Selection counter shows "1 beat selected"

```
┌─────────────────────────────────────┐
│                                     │
│     [Beat Grid]                     │
│                                     │
│   ☑️ Beat 1    ☐ Beat 2    ☐ Beat 3 │ ← Checkboxes appear
│                                     │
│   ☐ Beat 4    ☐ Beat 5    ☐ Beat 6 │
│                                     │
└─────────────────────────────────────┘
                 ↓
      "Tap beats to select more" (hint)
                 ↓
┌─────────────────────────────────────┐
│ [✕] 1 beat selected    [Edit] [⋮]  │ ← Toolbar
└─────────────────────────────────────┘
```

**User continues tapping:**
- Each tap toggles checkbox
- Counter updates in real-time
- [Edit] button stays enabled
- Grid remains fully visible (no overlay)

**User taps Edit button:**
- Validation check (start position + beats)
- If valid → Open batch edit panel
- If invalid → Show error toast

---

### Step 2B: Select Row Mode

**User Action:** Taps "Select Row"

**System Response:**
- Panel shows instruction: "Tap any beat in the row"
- Initial beat highlights
- User taps beat → Entire row selects
- Toolbar appears with selection

```
Step 1: Choose row
┌─────────────────────────────────────┐
│ Tap any beat in the row to select  │ ← Instruction
├─────────────────────────────────────┤
│                                     │
│   💡 Beat 1    Beat 2    Beat 3     │
│   ↑ Tap here to select this row     │
│   Beat 4    Beat 5    Beat 6        │
│                                     │
└─────────────────────────────────────┘

Step 2: Row selected
┌─────────────────────────────────────┐
│                                     │
│   ☑️ Beat 1   ☑️ Beat 2   ☑️ Beat 3 │ ← Entire row checked
│                                     │
│   ☐ Beat 4    ☐ Beat 5    ☐ Beat 6 │
│                                     │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ [✕] Row 1 (3 beats)    [Edit] [⋮]  │ ← Shows "Row 1"
└─────────────────────────────────────┘
```

**Advanced Option:**
- User can tap MORE rows to add them
- Counter updates: "2 rows, 6 beats selected"
- Or tap [⋮] → "Select only this row" to deselect others

---

### Step 2C: Select Column Mode

**User Action:** Taps "Select Column"

**System Response:**
- Panel shows instruction: "Tap any beat in the column"
- Initial beat highlights
- User taps beat → Entire column selects
- Toolbar appears with selection

```
Step 1: Choose column
┌─────────────────────────────────────┐
│ Tap any beat in the column         │ ← Instruction
├─────────────────────────────────────┤
│                                     │
│   Beat 1    💡 Beat 2    Beat 3     │
│             ↑ Tap here              │
│   Beat 4    Beat 5       Beat 6     │
│             ↑ Selects entire column │
│                                     │
└─────────────────────────────────────┘

Step 2: Column selected
┌─────────────────────────────────────┐
│                                     │
│   ☐ Beat 1   ☑️ Beat 2   ☐ Beat 3   │
│                ↓                    │
│   ☐ Beat 4   ☑️ Beat 5   ☐ Beat 6   │ ← Entire column
│                ↓                    │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ [✕] Column 2 (2 beats)  [Edit] [⋮] │ ← Shows "Column 2"
└─────────────────────────────────────┘
```

---

### Step 3: Batch Edit Panel Opens

**User Action:** Taps [Edit] button from toolbar

**System Response:**
1. **Validation Check:**
   - Ensure no start position + beats mix
   - If mixed → Show error, don't open panel

2. **Mixed Value Analysis:**
   - Scan all selected beats
   - Detect which properties have same/different values
   - Prepare UI accordingly

3. **Panel Slides Up:**

```
┌─────────────────────────────────────┐
│ ══════ Editing 5 Beats              │
├─────────────────────────────────────┤
│                                     │
│ Selected Pictographs:               │
│ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐     │ ← Thumbnails
│ │🎭│ │🎭│ │🎭│ │🎭│ │🎭│     │   (max 5, then "...")
│ └───┘ └───┘ └───┘ └───┘ └───┘     │
│                                     │
├─────────────────────────────────────┤
│ Turn Controls                       │
├─────────────────────────────────────┤
│                                     │
│ Left Hand Turn:                     │
│  Current: [Mixed] 1, 2, 3           │ ← Shows all values
│  ┌───────────────────────────────┐ │
│  │ [Mixed values] ▼              │ │ ← Dropdown
│  └───────────────────────────────┘ │
│                                     │
│ Right Hand Turn:                    │
│  Current: All set to 2              │ ← All same
│  ┌───────────────────────────────┐ │
│  │         2        ▼            │ │ ← Shows value
│  └───────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│ ⚠️  Info                            │
│ • Mixed values will be replaced     │
│ • Unchanged fields keep current     │
│   values                            │
│ • Changes apply to all 5 beats      │
├─────────────────────────────────────┤
│                                     │
│ [Cancel]          [Apply to All]   │
│                                     │
└─────────────────────────────────────┘
```

---

### Step 4: Mixed Value Dropdown Interaction

**User Action:** Taps dropdown for "Left Hand Turn: [Mixed]"

**System Response:**

```
┌───────────────────────────────────┐
│ Left Hand Turn                    │
├───────────────────────────────────┤
│ ● Keep as-is                      │ ← Don't change
│   (beats keep their current       │
│    values: 1, 2, 3)               │
├───────────────────────────────────┤
│ Set all to:                       │
│                                   │
│   ○ 0 turns                       │
│   ○ 1 turn    (1 beat has this)  │ ← Shows count
│   ○ 2 turns   (2 beats have this)│
│   ○ 3 turns   (2 beats have this)│
├───────────────────────────────────┤
│ 🎯 Custom value...                │ ← Opens picker
│                                   │
└───────────────────────────────────┘
```

**User selects "Set all to: 2 turns":**
- Dropdown closes
- Value updates to show "2"
- Field label becomes **bold** (edited indicator)
- Apply button becomes more prominent

```
Left Hand Turn:
  Current: Mixed (1, 2, 3)
  Change to: 2             ✓ Edited  ← Bold, checkmark
```

---

### Step 5: Apply Changes

**User Action:** Taps "Apply to All"

**System Response:**

**5A: Applying Animation**
```
┌─────────────────────────────────────┐
│ Applying changes...                 │
│                                     │
│ ████████████░░░░░░░░  65%          │ ← Progress
│                                     │
│ Updating beat 3 of 5...             │
└─────────────────────────────────────┘
```

**5B: Success Feedback**
```
┌─────────────────────────────────────┐
│ ✅ Updated 5 beats successfully     │
│                                     │
│ Changes:                            │
│ • Left hand turn: Set to 2          │
│                                     │
│        [View] [Undo] [Done]         │
└─────────────────────────────────────┘

After 2 seconds (or user taps Done):
- Success message slides down
- Selection toolbar appears again
- Beats remain selected
- User can:
  - Make more edits
  - Change selection
  - Or tap [✕] to exit multi-select
```

**5C: Partial Failure**
```
┌─────────────────────────────────────┐
│ ⚠️  Updated 4 of 5 beats            │
│                                     │
│ Beat 3 could not be updated:        │
│ Invalid turn configuration          │
│                                     │
│ [View Failed] [Retry] [Done]        │
└─────────────────────────────────────┘
```

---

## Edge Cases & Validation

### Case 1: Start Position + Beats Mixed Selection

**Scenario:** User has beats 1, 2 selected, tries to add start position

**Prevention:**
```typescript
function validateSelection(selection: Set<number>): ValidationResult {
  const hasStart = selection.has(0);
  const hasBeats = Array.from(selection).some(n => n > 0);

  if (hasStart && hasBeats) {
    return {
      valid: false,
      errorType: 'MIXED_TYPES',
      message: 'Cannot select start position and beats together',
      suggestion: 'Start position has different properties. Clear selection to choose start position.'
    };
  }

  return { valid: true };
}
```

**UI Response:**
```
User tries to select start position while beats selected:

┌─────────────────────────────────────┐
│ ⚠️  Cannot mix types                │
│                                     │
│ Start position and beats have       │
│ different editable properties.      │
│                                     │
│ [Keep beats]  [Clear & select start]│
└─────────────────────────────────────┘

OR (less intrusive):

Toast message at bottom:
┌──────────────────────────────────┐
│ ⚠️  Can't mix start position with│
│    beats. Clear selection first. │
└──────────────────────────────────┘
```

### Case 2: No Beats Selected

**Scenario:** User taps Edit with 0 beats selected (shouldn't happen, but defensive)

**Prevention:**
- [Edit] button is **disabled** when selection count = 0
- Button style: Grayed out, no hover effect

### Case 3: All Same Values (No Mixed State)

**Scenario:** User selects 5 beats, all have identical properties

**UI Response:**
```
┌─────────────────────────────────────┐
│ ══════ Editing 5 Beats              │
├─────────────────────────────────────┤
│                                     │
│ Left Hand Turn:                     │
│  Current: All set to 2              │ ← No "Mixed"
│  ┌───────────────────────────────┐ │
│  │         2        ▼            │ │ ← Value shown
│  └───────────────────────────────┘ │
│                                     │
│ Right Hand Turn:                    │
│  Current: All set to 1              │
│  ┌───────────────────────────────┐ │
│  │         1        ▼            │ │
│  └───────────────────────────────┘ │
│                                     │
│ ℹ️  All selected beats have the     │
│    same values                      │
└─────────────────────────────────────┘
```

### Case 4: Single Beat in Multi-Select Mode

**Scenario:** User enters multi-select but only selects 1 beat

**Options:**

**Option A: Allow it (Recommended)**
- Treat as batch edit of 1 item
- Same UI, just says "Editing 1 beat"
- Consistent behavior

**Option B: Suggest single-edit**
```
┌─────────────────────────────────────┐
│ 💡 Tip                              │
│ Only 1 beat selected.               │
│ Use quick edit instead?             │
│                                     │
│ [Stay in multi-select] [Quick edit] │
└─────────────────────────────────────┘
```

### Case 5: Empty Selection State

**Scenario:** User enters multi-select, then deselects all beats

**Behavior:**
- Toolbar shows "0 beats selected"
- [Edit] button becomes **disabled**
- After 2 seconds of 0 selection, auto-exit multi-select mode (optional)
- Or keep in mode but show hint: "Tap beats to select"

---

## Graph Editor Integration

### Challenge: Displaying Multiple Pictographs with Turn Editor

**Problem:** Graph editor currently shows single pictograph + turn graph. With multiple pictographs, what to display?

### Solution: Adaptive Layout

**Layout A: Single Pictograph Selected**
```
┌─────────────────────────────────┐
│      ┌───────────┐              │
│      │           │              │ ← Large pictograph
│      │   🎭      │              │
│      │           │              │
│      └───────────┘              │
│                                 │
│      Turn Graph                 │
│      (interactive)              │
│   ┌─────────────────────┐      │
│   │     /\    /\         │      │
│   │    /  \  /  \        │      │
│   └─────────────────────┘      │
└─────────────────────────────────┘
```

**Layout B: Multiple Pictographs Selected (New)**
```
┌─────────────────────────────────┐
│ 5 Beats Selected                │
│ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ │ ← Thumbnails
│ │🎭│ │🎭│ │🎭│ │🎭│ │🎭│ │   (scrollable)
│ └───┘ └───┘ └───┘ └───┘ └───┘ │
│                                 │
│ Turn Controls (Batch Mode)      │
│                                 │
│ Left Turn:  [Mixed ▼] ──────●  │ ← Slider + dropdown
│                                 │
│ Right Turn: [  2   ▼] ──────●  │
│                                 │
│ ⚠️  Changes apply to all        │
│                                 │
│ [Visual Preview] ←──────────────┤ ← Button
└─────────────────────────────────┘

Visual Preview shows:
┌─────────────────────────────────┐
│ Beat 1 Preview  Beat 2 Preview  │ ← Side-by-side
│   🎭              🎭            │   before/after
│ Before: L2 R1   Before: L1 R1   │
│ After:  L2 R2   After:  L2 R2   │
└─────────────────────────────────┘
```

**Recommendation for Graph Editor:**

**Don't show graph in batch mode** - it becomes meaningless with mixed values. Instead:

1. **Show thumbnails** of all selected pictographs (max 5 visible, scroll for more)
2. **Simple controls** - Dropdowns/sliders without graph visualization
3. **Preview button** - Opens modal showing before/after for each beat
4. **Batch indicator** - Clear banner: "Batch editing 5 beats"

**Updated EditSlidePanel behavior:**

```typescript
// In EditSlidePanel.svelte

const isBatchMode = $derived(
  selectedBeatNumbers && selectedBeatNumbers.size > 1
);

// Render different layout based on mode
{#if isBatchMode}
  <BatchEditLayout
    selectedBeats={selectedBeatData}
    onApply={handleBatchApply}
  />
{:else}
  <EditPanelLayout
    selectedBeatData={selectedBeatData}
    onOrientationChanged={onOrientationChanged}
    onTurnAmountChanged={onTurnAmountChanged}
  />
{/if}
```

---

## Component Architecture

### New Components Needed

```
src/lib/modules/build/edit/components/
├── EditSlidePanel.svelte              (existing - modify)
├── EditPanelLayout.svelte             (existing - single edit)
├── BatchEditLayout.svelte             (NEW - batch edit)
├── MixedValueDropdown.svelte          (NEW)
├── PictographThumbnailGrid.svelte     (NEW)
└── BatchEditToolbar.svelte            (NEW)

src/lib/modules/build/workspace-panel/
├── SelectionModePanel.svelte          (NEW - mode chooser)
├── SelectionToolbar.svelte            (NEW - bottom toolbar)
└── BeatCellCheckbox.svelte            (NEW - overlay checkbox)
```

### State Extensions

```typescript
// In SequenceSelectionState

interface SelectionState {
  // Mode
  mode: 'single' | 'multi-select' | 'row-select' | 'column-select';

  // Selection
  selectedBeatNumbers: Set<number>;
  selectionAnchor: number | null;

  // Grid context (for row/column)
  gridRows: number;
  gridColumns: number;

  // Validation
  hasStartPosition: boolean;
  preventMixedTypes: boolean;
}

// Methods
enterMultiSelectMode(initialBeat: number): void
enterRowSelectMode(rowIndex: number): void
enterColumnSelectMode(colIndex: number): void
exitSelectionMode(): void
toggleBeat(beatNumber: number): ValidationResult
selectRow(rowIndex: number): void
selectColumn(colIndex: number): void
validateSelection(): ValidationResult
```

---

## Implementation Checklist

### Phase 1: Mode Selection Panel
- [ ] Create SelectionModePanel component
- [ ] Add long-press detection to BeatCell
- [ ] Implement mode selection UI
- [ ] Add animations (slide up/down)
- [ ] Haptic feedback on long-press

### Phase 2: Multi-Select Mode
- [ ] Add checkbox overlay to BeatCell
- [ ] Implement toggle selection
- [ ] Create SelectionToolbar component
- [ ] Add selection counter
- [ ] Implement cancel/exit

### Phase 3: Row/Column Selection
- [ ] Add grid layout awareness to state
- [ ] Implement row selection logic
- [ ] Implement column selection logic
- [ ] Add visual feedback for row/column

### Phase 4: Validation
- [ ] Add start position + beats validation
- [ ] Implement error toasts
- [ ] Disable invalid selections
- [ ] Add helpful error messages

### Phase 5: Batch Edit UI
- [ ] Create BatchEditLayout component
- [ ] Implement MixedValueDropdown
- [ ] Add pictograph thumbnail grid
- [ ] Detect mixed values
- [ ] Track edited fields

### Phase 6: Apply Changes
- [ ] Implement batch update logic
- [ ] Add progress indicator
- [ ] Success/error feedback
- [ ] Undo support
- [ ] Partial failure handling

### Phase 7: Graph Editor Integration
- [ ] Detect batch mode in EditSlidePanel
- [ ] Create simplified batch controls
- [ ] Remove graph visualization in batch mode
- [ ] Add preview modal
- [ ] Update turn controls for mixed values

---

## Open Questions

1. **Grid Layout:**
   - How is grid structure defined? (3x5, 4x4, etc.)
   - Is it fixed or dynamic?
   - How do we map beat numbers to grid positions?

2. **Row/Column Definition:**
   - Are rows/columns based on visual layout?
   - Or based on sequence structure?
   - What if sequences have different lengths?

3. **Undo Granularity:**
   - Is batch edit ONE undo action?
   - Or individual undos per beat?
   - What if user wants to undo just one beat's change?

4. **Performance:**
   - How many beats is the max for batch edit?
   - Should we limit selection size?
   - Performance implications of updating 50+ beats?

5. **Visual Preview:**
   - Should preview be modal or inline?
   - Show all beats or paginated?
   - Real-time preview or on-demand?

---

## Next Steps

1. **Answer open questions** about grid layout
2. **Create prototypes** of mode selection panel
3. **Design mixed value dropdown** interaction
4. **User test** with 5 users (mode selection flow)
5. **Implement Phase 1** (mode selection panel)
6. **Iterate** based on feedback

---

**Document Version:** 1.0
**Last Updated:** January 2025
**Status:** Design Proposal - Awaiting Review
