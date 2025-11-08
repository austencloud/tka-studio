# Drawer Event Handling Fix - EditSlidePanel State Management Issue

## Date

January 2025

## Problem Description

### Symptoms

After opening and closing the EditSlidePanel:

1. Panel appears to close visually
2. Background remains black (as if panel is still open)
3. Subsequent attempts to open the panel fail
4. The `editing-mode` class remains applied to `.create-tab`

### Root Cause

The Drawer component was using Svelte 4's deprecated `createEventDispatcher` pattern, which doesn't properly integrate with Svelte 5's reactivity system. When the drawer closed via vaul-svelte's internal mechanisms:

1. Drawer's `handleOpenChange` set local `isOpen = false`
2. The `dispatch("close")` event was emitted
3. **BUT** the parent component's state (`panelState.isEditPanelOpen`) wasn't reliably updated
4. This left `panelState.isEditPanelOpen = true`, keeping the black background active
5. The stale state prevented subsequent open attempts from working

### Technical Details

```svelte
<!-- OLD PATTERN (Svelte 4 - BROKEN in Svelte 5) -->
<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function handleOpenChange(open: boolean) {
    isOpen = open;
    if (lastOpenState && !open) {
      dispatch("close", { reason: "programmatic" }); // ❌ Not reliable in Svelte 5
    }
  }
</script>

<Drawer on:close={handleClose}>  <!-- ❌ Svelte 4 event syntax -->
```

## Solution

### 1. Updated Drawer Component to Svelte 5 Event Callbacks

**File**: `src/lib/shared/foundation/ui/Drawer.svelte`

**Changes**:

- Removed `createEventDispatcher` import
- Added `onclose` prop for Svelte 5 event callback pattern
- Created `emitClose()` function to call the callback directly
- Updated all close handlers to use `emitClose()`

```svelte
<!-- NEW PATTERN (Svelte 5 - CORRECT) -->
<script lang="ts">
  type CloseReason = "backdrop" | "escape" | "programmatic";

  let {
    isOpen = $bindable(false),
    onclose, // ✅ Svelte 5 event callback
    // ... other props
  } = $props<{
    onclose?: (event: CustomEvent<{ reason: CloseReason }>) => void;
    // ... other prop types
  }>();

  function emitClose(reason: CloseReason) {
    // ✅ Call the callback directly
    if (onclose) {
      onclose(new CustomEvent("close", { detail: { reason } }));
    }
  }

  function handleOpenChange(open: boolean) {
    isOpen = open; // ✅ Updates bindable prop
    if (lastOpenState && !open) {
      emitClose("programmatic"); // ✅ Calls parent callback
    }
    lastOpenState = open;
  }
</script>
```

### 2. Updated EditSlidePanel to Use Two-Way Binding

**File**: `src/lib/modules/create/edit/components/EditSlidePanel.svelte`

**Changes**:

- Created local `localIsOpen` state variable
- Added `$effect` to sync prop changes to local state
- Added `$effect` to trigger `onClose()` when local state changes
- Used `bind:isOpen={localIsOpen}` for two-way binding with Drawer

```svelte
<script lang="ts">
  const {
    isOpen = false, // ✅ Prop from parent
    onClose,
    // ... other props
  } = $props();

  // ✅ Local state for two-way binding
  let localIsOpen = $state(isOpen);

  // ✅ Sync prop changes to local state
  $effect(() => {
    localIsOpen = isOpen;
  });

  // ✅ Trigger onClose when drawer closes
  $effect(() => {
    if (localIsOpen !== isOpen) {
      if (!localIsOpen && isOpen) {
        onClose(); // ✅ Calls parent's close handler
      }
    }
  });

  function handleClose() {
    hapticService?.trigger('selection');
    onClose(); // ✅ Explicit close
  }
</script>

<Drawer
  bind:isOpen={localIsOpen}  <!-- ✅ Two-way binding -->
  onclose={handleClose}       <!-- ✅ Svelte 5 callback -->
  <!-- ... other props -->
>
```

### 3. Updated All Drawer Usages

Updated all Drawer component usages throughout the codebase to use Svelte 5 event callback pattern:

**Create Module Drawers** (with `respectLayoutMode={true}`):

- ✅ `SharePanelSheet.svelte` - `on:close` → `onclose`
- ✅ `AnimationPanel.svelte` - `on:close` → `onclose`
- ✅ `SequenceActionsSheet.svelte` - `on:close` → `onclose`
- ✅ `CAPSelectionModal.svelte` - `on:close` → `onclose`
- ✅ `EditSlidePanel.svelte` - `on:close` → `onclose` + two-way binding

**Global Drawers** (centered, no responsive layout):

- ✅ `SettingsSheet.svelte` - `on:close` → `onclose`
- ✅ `ProfileSettingsSheet.svelte` - `on:close` → `onclose`
- ✅ `PrivacySheet.svelte` - `on:close` → `onclose`
- ✅ `TermsSheet.svelte` - `on:close` → `onclose`
- ✅ `AchievementsBrowser.svelte` - `on:close` → `onclose`

## How It Works Now

### Event Flow (Correct)

1. User closes drawer (swipe, backdrop click, or escape key)
2. Drawer's `handleOpenChange()` is called by vaul-svelte
3. `isOpen = false` updates the bindable prop
4. `emitClose()` calls the `onclose` callback
5. Parent's `handleClose()` is executed
6. Parent updates `panelState.closeEditPanel()`
7. `panelState.isEditPanelOpen` becomes `false`
8. `.editing-mode` class is removed from `.create-tab`
9. Black background is removed
10. Panel can be opened again successfully

### State Synchronization (EditSlidePanel)

1. Parent passes `isOpen={panelState.isEditPanelOpen}`
2. EditSlidePanel creates `localIsOpen = $state(isOpen)`
3. `$effect` syncs prop changes: `localIsOpen = isOpen`
4. Drawer binds to `localIsOpen` via `bind:isOpen={localIsOpen}`
5. When Drawer closes, `localIsOpen` becomes `false`
6. `$effect` detects change and calls `onClose()`
7. Parent's `panelState.closeEditPanel()` is executed
8. State is fully synchronized

## Benefits

### ✅ Reliable Event Handling

- Events are guaranteed to reach parent components
- No more stale state issues
- Proper integration with Svelte 5 reactivity

### ✅ Two-Way Binding

- Drawer state stays in sync with parent state
- Changes propagate correctly in both directions
- No more "stuck open" or "stuck closed" states

### ✅ Future-Proof

- Uses Svelte 5's recommended patterns
- No deprecated APIs
- Consistent with modern Svelte best practices

## Testing Checklist

### EditSlidePanel Specific

- [x] Open edit panel by clicking a beat
- [x] Close panel via swipe down gesture
- [x] Verify black background is removed
- [x] Open panel again - should work
- [x] Close panel via backdrop click
- [x] Verify black background is removed
- [x] Open panel again - should work
- [x] Close panel via escape key
- [x] Verify black background is removed
- [x] Open panel again - should work

### All Drawers

- [ ] SharePanelSheet - open/close cycle works
- [ ] AnimationPanel - open/close cycle works
- [ ] SequenceActionsSheet - open/close cycle works
- [ ] CAPSelectionModal - open/close cycle works
- [ ] SettingsSheet - open/close cycle works
- [ ] ProfileSettingsSheet - open/close cycle works
- [ ] PrivacySheet - open/close cycle works
- [ ] TermsSheet - open/close cycle works
- [ ] AchievementsBrowser - open/close cycle works

## Related Files

### Core Changes

- `src/lib/shared/foundation/ui/Drawer.svelte` - Event handling fix
- `src/lib/modules/create/edit/components/EditSlidePanel.svelte` - Two-way binding

### Updated Usages

- `src/lib/modules/create/share/components/SharePanelSheet.svelte`
- `src/lib/modules/create/animate/components/AnimationPanel.svelte`
- `src/lib/modules/create/workspace-panel/shared/components/SequenceActionsSheet.svelte`
- `src/lib/modules/create/generate/components/modals/CAPSelectionModal.svelte`
- `src/lib/shared/settings/components/SettingsSheet.svelte`
- `src/lib/shared/navigation/components/ProfileSettingsSheet.svelte`
- `src/lib/shared/navigation/components/PrivacySheet.svelte`
- `src/lib/shared/navigation/components/TermsSheet.svelte`
- `src/lib/shared/gamification/components/AchievementsBrowser.svelte`

## Migration Pattern

For any future Drawer usages:

```svelte
<!-- OLD (Svelte 4) -->
<Drawer
  isOpen={show}
  on:close={handleClose}
>

<!-- NEW (Svelte 5) -->
<Drawer
  isOpen={show}
  onclose={handleClose}
>
```

If you need two-way binding (like EditSlidePanel):

```svelte
<script>
  let localIsOpen = $state(isOpen);

  $effect(() => {
    localIsOpen = isOpen;
  });

  $effect(() => {
    if (localIsOpen !== isOpen && !localIsOpen && isOpen) {
      onClose();
    }
  });
</script>

<Drawer
  bind:isOpen={localIsOpen}
  onclose={handleClose}
>
```
