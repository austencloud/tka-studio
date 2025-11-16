# IExploreLoader Service Resolution Fix

## Problem
The `IExploreLoader` service couldn't be resolved when loading the Animate, WordCard, or other tabs that use explore services. This was causing the app to crash with:
```
No bindings found for service: "Symbol(IExploreLoader)"
```

## Root Causes
There were **TWO related issues**:

### Issue 1: Missing Module Dependencies
The Animate and WordCard modules use **SequenceBrowserPanel** and other components that depend on explore services (`IExploreLoader`), but the explore module wasn't being loaded as a dependency.

- **AnimateTab** uses `SequenceBrowserPanel` which needs `IExploreLoader` (line 33)
- **WordCardTab** directly uses `IExploreLoader` (line 11)
- But when loading the `animate` or `word_card` feature, the `exploreModule` wasn't being loaded

### Issue 2: HMR Not Restoring Feature Modules
When HMR triggered a container rebuild, the system was only reloading:
- **Tier 1 modules**: core, navigation, data, keyboard (critical infrastructure)
- **Tier 2 modules**: render, pictograph, animator, gamification (shared services)

But **Tier 3 feature modules** (explore, create, learn, etc.) were loaded on-demand and were NOT being restored after HMR, even if they were actively in use.

## Solution

### Fix 1: Added Missing Module Dependencies
Modified [container.ts:306-317](src/lib/shared/inversify/container.ts#L306-L317) to declare module dependencies:
```typescript
animate: [modules.exploreModule], // Animate depends on explore (SequenceBrowserPanel uses IExploreLoader)
word_card: [modules.wordCardModule, modules.exploreModule], // WordCard depends on explore
```

Now when loading the animate or word_card module, the explore module is automatically loaded first.

### Fix 2: HMR Feature Module Restoration
Modified [container.ts:28-77](src/lib/shared/inversify/container.ts#L28-L77) to:
1. Save the list of loaded feature modules before clearing the container during HMR
2. After rebuilding the container, restore all previously loaded feature modules
3. This ensures that if you're viewing any tab and make a code change, the module services remain available

### Fix 3: Better Error Messages
Improved [inversify/index.ts:112-169](src/lib/shared/inversify/index.ts#L112-L169) to provide helpful hints when service resolution fails, making it easier to diagnose similar issues in the future.

## How to Test

### Test 1: Animate Tab Loads Successfully
1. **Refresh the page** (hard refresh: Ctrl+Shift+R or Cmd+Shift+R)
2. **Navigate to the Animate tab**
3. **Verify** that:
   - No `IExploreLoader` binding errors appear
   - The Animate tab loads without errors
   - The SequenceBrowserPanel works correctly

### Test 2: WordCard Tab Loads Successfully
1. **Navigate to the WordCard tab**
2. **Verify** that:
   - No `IExploreLoader` binding errors appear
   - The WordCard tab loads without errors

### Test 3: HMR Preserves Module Services
1. **Navigate to the Explore tab**
2. **Make a trivial change** to any file (e.g., add a comment to ExploreModule.svelte)
3. **Save the file** to trigger HMR
4. **Verify** that:
   - The console shows: `🔄 HMR: Restoring feature modules: explore`
   - The console shows: `✅ HMR: Restored feature module "explore"`
   - The Explore tab continues to work without errors
   - No `IExploreLoader` binding errors appear

## Expected Console Output After HMR
```
🔄 HMR: Rebuilding InversifyJS container...
🔄 HMR: Restoring feature modules: explore
✅ HMR: Restored feature module "explore"
✅ HMR: Container successfully rebuilt
```

## Files Modified
- [src/lib/shared/inversify/container.ts](src/lib/shared/inversify/container.ts) - Added feature module restoration during HMR
- [src/lib/shared/inversify/index.ts](src/lib/shared/inversify/index.ts) - Improved error messages for missing service bindings
