# Edit Panel Deselection Fix

## Problem

When the edit panel was open with a pictograph selected, clicking outside the panel (not on another pictograph) would close the panel but **fail to deselect the pictograph**. This caused subsequent pictograph selection attempts to fail.

## Root Cause

The edit panel's backdrop had `pointer-events: none` set in [Drawer.svelte:178-184](src/lib/shared/foundation/ui/Drawer.svelte#L178-L184), which meant clicks went through the backdrop instead of being detected by the `handleBackdropClick` handler.

**Before:**

```css
:global(.drawer-overlay.edit-panel-backdrop) {
  background: transparent !important;
  backdrop-filter: none !important;
  pointer-events: none !important; /* ❌ Clicks ignored */
}
```

This caused:

1. User clicks outside panel (empty workspace area)
2. Click goes through transparent backdrop
3. Backdrop click handler never fires
4. Panel might close via other means (Escape key, gestures)
5. `clearSelection()` never called
6. Pictograph stays selected

## Solution

### 1. Fixed Backdrop Pointer Events

Changed `pointer-events: none` to `pointer-events: auto` in [Drawer.svelte:183](src/lib/shared/foundation/ui/Drawer.svelte#L183):

```css
:global(.drawer-overlay.edit-panel-backdrop) {
  background: transparent !important;
  backdrop-filter: none !important;
  pointer-events: auto !important; /* ✅ Clicks detected */
}
```

### 2. Enhanced Backdrop Click Detection

Updated `handleBackdropClick` in [EditSlidePanel.svelte:127-159](src/lib/modules/create/edit/components/EditSlidePanel.svelte#L127-L159) to detect elements beneath the backdrop:

```typescript
function handleBackdropClick(event: MouseEvent): boolean {
  // Get the element at the click coordinates (beneath the backdrop)
  const backdrop = event.target as HTMLElement;
  backdrop.style.pointerEvents = "none";
  const elementBeneath = document.elementFromPoint(
    event.clientX,
    event.clientY
  );
  backdrop.style.pointerEvents = "auto";

  // Check if the element beneath is a beat cell
  const isBeatClick = elementBeneath?.closest(".beat-cell, .start-tile, ...");

  if (isBeatClick) {
    // Trigger click on the beat and keep panel open
    if (elementBeneath instanceof HTMLElement) {
      elementBeneath.click();
    }
    return false;
  }

  // Close panel for non-beat clicks
  return true;
}
```

**Why this approach?**

- The backdrop overlay intercepts all clicks (since it covers the viewport)
- `event.target` is the backdrop itself, not the element underneath
- Using `document.elementFromPoint()` with temporarily disabled pointer-events reveals the actual clicked element
- If it's a beat, we forward the click and keep the panel open
- If it's empty space, we close the panel

### 3. Synchronized Local UI State

Added effect in [WorkspacePanel.svelte:76-86](src/lib/modules/create/workspace-panel/core/WorkspacePanel.svelte#L76-L86) to sync visual selection state:

```typescript
// Effect: Sync local selection with sequenceState selection
$effect(() => {
  if (!sequenceState) return;

  const globalSelection = sequenceState.selectedBeatNumber;
  if (animatingBeatNumber === null) {
    localSelectedBeatNumber = globalSelection;
  }
});
```

**Why was this needed?**

- `WorkspacePanel` has its own `localSelectedBeatNumber` for rendering the selection UI
- When `sequenceState.clearSelection()` was called, it only cleared the global state
- The local UI state wasn't updating, so the gold border remained
- This effect keeps them in sync, ensuring the visual state updates when selection is cleared

### 4. Cleaned Up Old CSS

Removed outdated BottomSheet CSS references in [EditSlidePanel.svelte:264-276](src/lib/modules/create/edit/components/EditSlidePanel.svelte#L264-L276) that were targeting the wrong component classes.

## Fix Verification

### Code Flow (After Fix)

1. User clicks outside panel (not on a beat)
2. Click hits transparent backdrop (pointer-events enabled)
3. `Drawer.handleBackdropClick` called with event
4. `EditSlidePanel.handleBackdropClick` checks if click is on a beat:
   - Uses `target.closest('.beat-cell, .start-tile, ...')`
   - Returns `false` if beat clicked (keep panel open)
   - Returns `true` if non-beat clicked (close panel)
5. If returning `true`, `Drawer` calls `emitClose("backdrop")` and sets `isOpen = false`
6. `emitClose` calls the `onclose` callback
7. `EditSlidePanel.handleClose` is invoked
8. Calls `onClose()` which is `EditCoordinator.handleClosePanel`
9. `EditCoordinator.handleClosePanel` [lines 156-179](src/lib/modules/create/shared/components/coordinators/EditCoordinator.svelte#L156-L179):
   - Calls `panelState.closeEditPanel()` to close panel
   - Calls `CreateModuleState.sequenceState.clearSelection()` to **deselect pictograph** ✅
   - Exits multi-select mode if active

### Files Changed

1. [src/lib/shared/foundation/ui/Drawer.svelte](src/lib/shared/foundation/ui/Drawer.svelte)
   - Line 183: Changed `pointer-events: none` → `pointer-events: auto` for edit panel backdrop

2. [src/lib/modules/create/edit/components/EditSlidePanel.svelte](src/lib/modules/create/edit/components/EditSlidePanel.svelte)
   - Lines 127-159: Enhanced `handleBackdropClick` to detect elements beneath backdrop
   - Lines 264-276: Cleaned up old BottomSheet CSS

3. [src/lib/modules/create/workspace-panel/core/WorkspacePanel.svelte](src/lib/modules/create/workspace-panel/core/WorkspacePanel.svelte)
   - Lines 76-86: Added effect to sync `localSelectedBeatNumber` with `sequenceState.selectedBeatNumber`

## Manual Test Procedure

### Test 1: Outside Click Deselection

1. Navigate to Build > Construct
2. Select a start position (if required)
3. Click an option tile to add a beat to the sequence
4. Click on the beat cell in the workspace
5. **Verify**: Edit panel opens, beat has gold "selected" border
6. Click on an empty area of the workspace (not on the beat, not on the panel)
7. **Expected**:
   - ✅ Edit panel closes
   - ✅ Beat's gold "selected" border disappears (deselected)
8. Click on the beat again
9. **Expected**:
   - ✅ Edit panel opens successfully
   - ✅ Beat is selected again (subsequent selections work)

### Test 2: Beat-to-Beat Selection Switching

1. Navigate to Build > Construct
2. Add at least 2 beats to the sequence
3. Click first beat
4. **Verify**: First beat selected (gold border), edit panel open
5. Click second beat (while panel still open)
6. **Expected**:
   - ✅ Second beat now selected (gold border)
   - ✅ First beat no longer selected (no border)
   - ✅ Edit panel remains open, showing second beat's data

### Test 3: Escape Key Deselection

1. Select a beat to open edit panel
2. Press `Escape` key
3. **Expected**:
   - ✅ Edit panel closes
   - ✅ Beat is deselected

## Technical Details

### Related Components

- **Drawer.svelte**: Generic drawer/sheet component with backdrop click handling
- **EditSlidePanel.svelte**: Edit panel wrapper with custom backdrop click logic
- **EditCoordinator.svelte**: Handles edit panel events and selection state
- **SequenceSelectionState.svelte.ts**: Manages beat selection state
- **AutoEditPanelManager.svelte.ts**: Opens panel when beats are selected

### Selection State Management

The selection state uses Svelte 5 runes:

- `selectedBeatNumber`: Stores currently selected beat (null = nothing selected)
- `clearSelection()`: Sets `selectedBeatNumber = null`

The AutoEditPanelManager effect only opens the panel when `selectedBeatNumber !== null`, so clearing selection won't trigger re-opening.

## Automated Test

An automated test has been created at [tests/e2e/edit-panel-deselection.spec.ts](tests/e2e/edit-panel-deselection.spec.ts) but requires additional test infrastructure setup to run properly.

---

**Status**: ✅ Fixed and ready for manual testing
**Date**: 2025-11-06
