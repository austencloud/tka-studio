# Integrating CREATE Module Keyboard Shortcuts

## Overview

The CREATE module keyboard shortcuts have been registered and are ready to integrate with your existing functionality. This guide shows how to connect each shortcut to the appropriate service or state.

## Current Status

✅ **Shortcuts Registered**: All shortcuts are registered in the keyboard system
⏳ **Implementation Needed**: Action handlers need to be connected to CREATE module services

---

## Registered Shortcuts

### Animation Control

| Shortcut | Action | Status | Priority |
|----------|--------|--------|----------|
| `Space` | Play/Pause animation | Not implemented | HIGH |

### Beat Grid Navigation

| Shortcut | Action | Status | Priority |
|----------|--------|--------|----------|
| `↑` | Navigate up in grid | Not implemented | MEDIUM |
| `↓` | Navigate down in grid | Not implemented | MEDIUM |
| `←` | Navigate left in grid | Not implemented | MEDIUM |
| `→` | Navigate right in grid | Not implemented | MEDIUM |

### Edit Panel Navigation

| Shortcut | Action | Status | Priority |
|----------|--------|--------|----------|
| `←` (in edit panel) | Previous beat | Not implemented | HIGH |
| `→` (in edit panel) | Next beat | Not implemented | HIGH |
| `Enter` | Accept changes & close | Not implemented | HIGH |
| `[` | Decrease value | Not implemented | LOW |
| `]` | Increase value | Not implemented | LOW |

### Sequence Management

| Shortcut | Action | Status | Priority |
|----------|--------|--------|----------|
| `Ctrl+S` | Save sequence | Not implemented | HIGH |
| `+` | Add beat | Not implemented | MEDIUM |
| `Backspace` | Delete beat | Not implemented | MEDIUM |

---

## Integration Steps

### 1. Space - Play/Pause Animation

**Location**: [register-create-shortcuts.ts:28](../src/lib/shared/keyboard/utils/register-create-shortcuts.ts#L28)

**What needs to be done**:
- Update animation service to support pause (currently only plays)
- Add `togglePlayback()` method to animation service
- Connect shortcut to animation state

**Integration code**:

```typescript
// In register-create-shortcuts.ts
import { /* your animation state */ } from "$lib/modules/create/...";

action: () => {
  // Option A: If using a service
  const animService = resolve(TYPES.IAnimationService);
  animService.togglePlayback();

  // Option B: If using Svelte state
  animationState.togglePlayback();
}
```

**Notes from user**:
> "Love the idea of space for playing and pausing the animation right now we can't even stop the animation if we wanted to."

**Required changes**:
1. Add `isPlaying` state to animation system
2. Add `pause()` method alongside existing `play()`
3. Modify animation loop to respect `isPlaying` state

---

### 2. Arrow Keys - Beat Grid Navigation

**Location**: [register-create-shortcuts.ts:58-124](../src/lib/shared/keyboard/utils/register-create-shortcuts.ts#L58-L124)

**What needs to be done**:
- Add focus state to beat grid
- Track which beat is currently focused
- Add visual indicator for focused beat
- Navigate focus on arrow key press

**Integration code**:

```typescript
// In register-create-shortcuts.ts
import { beatGridState } from "$lib/modules/create/...";

action: () => {
  // Navigate based on arrow direction
  beatGridState.moveFocus("up"); // or "down", "left", "right"
}
```

**Implementation suggestions**:

1. **Add focus state** to beat grid display state:
```typescript
// In beat-grid-display-state.svelte.ts
let focusedBeatIndex = $state<number | null>(null);

function moveFocus(direction: "up" | "down" | "left" | "right") {
  // Calculate new index based on grid layout
  // Update focusedBeatIndex
}
```

2. **Add visual indicator** in BeatCell.svelte:
```svelte
<div
  class="beat-cell"
  class:focused={isFocused}
>
```

3. **Handle selection on Enter**:
```typescript
// When Enter is pressed on focused beat
if (focusedBeatIndex !== null) {
  selectBeat(focusedBeatIndex);
}
```

**Notes from user**:
> "I actually think up and down can navigate across the grid in the actual beat grid instead of be a direction option."

---

### 3. Arrow Keys in Edit Panel - Beat Navigation

**Location**: [register-create-shortcuts.ts:128-168](../src/lib/shared/keyboard/utils/register-create-shortcuts.ts#L128-L168)

**What needs to be done**:
- Detect when edit panel is open
- Navigate to previous/next beat
- Update edit panel to show new beat

**Condition check needed**:

```typescript
// You'll need to import or access edit panel state
import { isEditPanelOpen } from "$lib/modules/create/edit/...";

condition: () => {
  return state.settings.enableSingleKeyShortcuts && isEditPanelOpen();
},
```

**Integration code**:

```typescript
// In register-create-shortcuts.ts
import { editState } from "$lib/modules/create/edit/...";

// Previous beat
action: () => {
  const currentIndex = editState.selectedBeatIndex;
  if (currentIndex > 0) {
    editState.selectBeat(currentIndex - 1);
  }
}

// Next beat
action: () => {
  const currentIndex = editState.selectedBeatIndex;
  const maxIndex = sequence.beats.length - 1;
  if (currentIndex < maxIndex) {
    editState.selectBeat(currentIndex + 1);
  }
}
```

**Notes from user**:
> "Love the idea of using the arrow keys to navigate between beats and the when the edit panel is open."

---

### 4. Enter - Accept Changes

**Location**: [register-create-shortcuts.ts:171-184](../src/lib/shared/keyboard/utils/register-create-shortcuts.ts#L171-L184)

**What needs to be done**:
- Apply current changes in edit panel
- Close the edit panel
- Update sequence with changes

**Integration code**:

```typescript
// In register-create-shortcuts.ts
import { editState } from "$lib/modules/create/edit/...";

action: () => {
  // Apply changes (this should already exist in your edit panel)
  editState.applyChanges();

  // Close panel
  editState.closePanel();
}
```

**Notes from user**:
> "I like the idea of Enter accepting the changes and closing the panel too."

---

### 5. Ctrl+S - Save Sequence

**Location**: [register-create-shortcuts.ts:188-201](../src/lib/shared/keyboard/utils/register-create-shortcuts.ts#L188-L201)

**What needs to be done**:
- Implement sequence persistence
- Save to user's profile
- Show save confirmation

**Integration code**:

```typescript
// In register-create-shortcuts.ts
import { sequenceService } from "$lib/modules/create/...";

action: async () => {
  const currentSequence = getCurrentSequence();

  try {
    await sequenceService.saveSequence(currentSequence);
    // Show success toast
    console.log("✅ Sequence saved!");
  } catch (error) {
    console.error("Failed to save sequence:", error);
    // Show error toast
  }
}
```

**Notes from user**:
> "I think control S should probably mean save the sequence, which is functionality that we have not yet implemented but I look forward to doing very soon."

---

### 6. + / Backspace - Add/Delete Beats

**Location**: [register-create-shortcuts.ts:204-235](../src/lib/shared/keyboard/utils/register-create-shortcuts.ts#L204-L235)

**What needs to be done**:
- Determine which prop color to add (blue/red)
- Add beat to sequence
- Delete focused/selected beat

**Challenge identified by user**:
> "We're going to have to think of a way to make it easy for the user to use keyboards to add or subtract to both the blue and red beat without using a confusing keyboard pattern."

**Suggested approach**:

**Option A: Modal selection**
- Press `+` opens a small dialog: "Add Blue or Red beat?"
- Press `B` for blue, `R` for red

**Option B: Based on focus**
- Add beat of same color as currently focused beat
- If no focus, add to last beat's color

**Option C: Modifier keys**
- `+` alone = add blue beat
- `Shift + +` = add red beat

**Integration code**:

```typescript
// Option B implementation (based on focus)
action: () => {
  const focusedBeat = beatGridState.getFocusedBeat();
  const colorToAdd = focusedBeat?.propColor || "blue";

  sequenceOperations.addBeat(colorToAdd);
}
```

---

### 7. [ and ] - Adjust Values in Edit Panel

**Location**: [register-create-shortcuts.ts:239-277](../src/lib/shared/keyboard/utils/register-create-shortcuts.ts#L239-L277)

**What needs to be done**:
- Determine which control is focused in edit panel
- Increment/decrement that control's value
- Update the visual display

**Integration code**:

```typescript
// In register-create-shortcuts.ts
import { editState } from "$lib/modules/create/edit/...";

// Decrease value
action: () => {
  const currentControl = editState.focusedControl;
  if (currentControl) {
    editState.adjustValue(currentControl, -1); // Decrease by 1 step
  }
}

// Increase value
action: () => {
  const currentControl = editState.focusedControl;
  if (currentControl) {
    editState.adjustValue(currentControl, 1); // Increase by 1 step
  }
}
```

---

## Context Management

The shortcuts need to know which context they're in. Update the shortcut service context when:

1. **User switches to CREATE module**:
```typescript
shortcutService.setContext("create");
```

2. **Edit panel opens**:
```typescript
shortcutService.setContext(["create", "edit-panel"]);
```

3. **Edit panel closes**:
```typescript
shortcutService.setContext("create");
```

4. **User switches away from CREATE**:
```typescript
shortcutService.setContext("explore"); // or other module
```

This is already set up in [KeyboardShortcutCoordinator.svelte:71-78](../src/lib/shared/keyboard/coordinators/KeyboardShortcutCoordinator.svelte#L71-L78):

```typescript
$effect(() => {
  if (shortcutService) {
    const module = getActiveModule();
    if (module) {
      shortcutService.setContext(module as any);
    }
  }
});
```

But you'll need to add additional context updates for sub-panels like edit panel.

---

## Testing the Shortcuts

### Manual Testing Checklist

1. **Switch to CREATE module** (press `1`)
2. **Test Space key** (should log "Play/Pause" for now)
3. **Test arrow keys** (should log navigation for now)
4. **Open edit panel** (manually)
5. **Test arrow keys again** (should prioritize edit panel navigation)
6. **Test Enter key** (should log "Accept changes")
7. **Test Ctrl+S** (should log "Save sequence")
8. **Test + key** (should log "Add beat")
9. **Test Backspace** (should log "Delete beat")

### Console Output to Watch For

When shortcuts are working, you'll see:
```
⌨️ Space pressed - Play/Pause (not yet implemented)
⌨️ Arrow Left - Previous beat (not yet implemented)
⌨️ Enter - Accept changes (not yet implemented)
```

---

## Priority Implementation Order

Based on user feedback and impact:

### Phase 1: Core Navigation (HIGH PRIORITY)
1. ✅ Register shortcuts (DONE)
2. ⏳ Space for play/pause
3. ⏳ Enter to accept changes in edit panel
4. ⏳ Arrow keys in edit panel (left/right for beat navigation)

### Phase 2: Sequence Management (HIGH PRIORITY)
5. ⏳ Ctrl+S to save sequence
6. ⏳ Add/delete beats

### Phase 3: Advanced Navigation (MEDIUM PRIORITY)
7. ⏳ Arrow keys for beat grid navigation
8. ⏳ [ and ] for value adjustments

---

## Notes

- All shortcuts respect the `enableSingleKeyShortcuts` setting (WCAG 2.1.4 compliance)
- Single-key shortcuts are automatically disabled when user is typing in an input field
- Modifier shortcuts (like Ctrl+S) work everywhere
- Higher priority shortcuts (edit panel arrow keys) override lower priority ones (grid arrow keys)

---

## Next Steps

1. Choose which shortcut to implement first (recommend: Space for play/pause)
2. Update the corresponding action handler in [register-create-shortcuts.ts](../src/lib/shared/keyboard/utils/register-create-shortcuts.ts)
3. Test the integration
4. Repeat for each shortcut

---

**Last Updated**: 2025
**Status**: Ready for integration
