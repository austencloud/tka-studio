# State Persistence Integration Guide

This guide shows how to integrate the new auto-sync state management and master restoration service into your existing TKA architecture.

## Files Created

1. **`/lib/state/utils/auto-sync-state.svelte.ts`** - Auto-syncing state wrapper with debouncing
2. **`/lib/services/implementations/MasterStateRestorationService.ts`** - Orchestrated state restoration
3. **`/lib/state/examples/auto-sync-browse-state.svelte.ts`** - Integration example for browse state

## Quick Start

### 1. Auto-Sync Any Existing Factory

Transform any of your current state factories to auto-sync:

```typescript
// BEFORE: Manual persistence
export function createSequenceState(service) {
  let state = $state({ ... });

  function saveSequence() {
    // Manual save call ❌
    persistenceService.save(state);
  }

  return { state, saveSequence };
}

// AFTER: Auto-sync
import { createSequenceAutoSync } from '$lib/state/utils/auto-sync-state.svelte';

export function createSequenceState(service) {
  const autoSync = createSequenceAutoSync('my-sequence-id');

  let state = $state(autoSync.load({ ... }));

  // Setup auto-sync
  const cleanup = autoSync.sync(() => state);

  return {
    get state() { return state; },
    updateSequence(data) {
      state = { ...state, ...data };
      // ✅ Auto-saved with debouncing!
    },
    destroy: cleanup
  };
}
```

### 2. Master State Restoration on App Startup

Add this to your main app initialization (e.g., `+layout.svelte` or app startup):

```typescript
import { initializeStateRestoration } from "$lib/services/implementations/MasterStateRestorationService";
import { tabStateService } from "$lib/state/services/TabStateService.svelte";
import { BrowseStatePersistenceService } from "$lib/services/implementations/browse/BrowseStatePersistenceService";

// On app startup
onMount(async () => {
  const browseStatePersistence = new BrowseStatePersistenceService();

  const result = await initializeStateRestoration({
    tabStateService,
    browseStatePersistence,
  });

  if (result.success) {
    console.log("✅ Complete state restoration successful!");
    console.log(`Restored in ${result.totalDuration}ms`);
  } else {
    console.warn(
      "⚠️ Some restoration steps failed:",
      result.failedEssentialSteps
    );
  }
});
```

### 3. Automatic Scroll Position Restoration

For any scrollable containers, add the `data-browse-scroll-container` attribute:

```svelte
<script>
  function handleScroll(e) {
    // If using auto-sync browse state:
    browseState.setScrollPosition({
      top: e.target.scrollTop,
      left: e.target.scrollLeft,
    });
    // ✅ Auto-saved and will be restored on next app load!
  }
</script>

<div
  class="sequence-list"
  data-browse-scroll-container
  on:scroll={handleScroll}
>
  <!-- Your sequences -->
</div>
```

## Integration Steps

### Step 1: Upgrade Browse State (Example)

Replace your current browse state factory:

```bash
# Backup your current factory
cp src/lib/state/browse-state-factory.svelte.ts src/lib/state/browse-state-factory.svelte.ts.backup

# Use the new auto-sync version as a reference
# See: /lib/state/examples/auto-sync-browse-state.svelte.ts
```

### Step 2: Remove Manual Persistence Calls

Search for and remove these patterns across your components:

```typescript
// Remove these ❌
await saveState();
persistenceService.save(...);
stateManager.save(...);

// They're now automatic! ✅
```

### Step 3: Add Scroll Tracking

Update scrollable containers to track position:

```svelte
<!-- Add data attribute and scroll handler -->
<div
  data-browse-scroll-container
  on:scroll={(e) => browseState.setScrollPosition({
    top: e.target.scrollTop,
    left: e.target.scrollLeft
  })}
>
```

### Step 4: Initialize Master Restoration

Add to your app's main layout or startup:

```typescript
import { initializeStateRestoration } from "$lib/services/implementations/MasterStateRestorationService";

// Call during app initialization
onMount(() => {
  initializeStateRestoration({
    tabStateService,
    browseStatePersistence: new BrowseStatePersistenceService(),
  });
});
```

## What You Get

### Perfect State Restoration

- ✅ **Exact tab restored** - User returns to the same tab they were on
- ✅ **Exact scroll position** - Smoothly scrolls back to where they left off
- ✅ **Exact selection** - Same sequence/item selected
- ✅ **Exact filter state** - Same filters applied
- ✅ **Exact search query** - Search term restored
- ✅ **Exact view mode** - Grid/list mode preserved

### Zero Manual Persistence

- ✅ **Auto-save everything** - No more manual `saveState()` calls
- ✅ **Debounced saves** - Efficient, doesn't spam localStorage
- ✅ **Error handling** - Graceful fallbacks if storage fails
- ✅ **Validation** - Only saves valid state

### Performance Benefits

- ✅ **Faster startup** - Coordinated restoration order
- ✅ **Smaller bundle** - Less persistence code duplication
- ✅ **Better UX** - Smooth scroll restoration, no jarring jumps

## Migration Checklist

- [ ] Backup existing state factories
- [ ] Install auto-sync wrapper in one factory (start with browse)
- [ ] Test auto-sync behavior
- [ ] Remove manual persistence calls
- [ ] Add scroll position tracking
- [ ] Initialize master restoration service
- [ ] Test complete app restart restoration
- [ ] Migrate other factories
- [ ] Remove unused persistence code

## Troubleshooting

**State not saving?**

- Check browser developer tools → Application → Local Storage
- Look for keys starting with `tka-*-state-v3`
- Verify `validate` function isn't rejecting state

**Scroll not restoring?**

- Ensure container has `data-browse-scroll-container` attribute
- Check timing - scroll restoration happens after 100ms delay for DOM readiness

**Restoration failing?**

- Check console for restoration service logs
- Look for timeout errors in individual steps
- Verify services are properly injected

**Want to debug state changes?**

```typescript
// Add to any auto-sync factory
const autoSync = createBrowseAutoSync();
console.log("State exists:", autoSync.exists());
console.log("Initial state:", autoSync.load({}));
```
