# Pictograph State Refactoring Summary

**Date:** 2025-10-17
**Status:** ✅ Complete

## Overview

Refactored the 469-line `pictograph-state.svelte.ts` god object into focused, independent sub-states with clean separation of concerns. **NO orchestrator needed** - just simple composition.

## Problem

The original `pictograph-state.svelte.ts` was a god object doing too much:

- ❌ **Too many responsibilities**: Data transformation, arrow lifecycle, prop lifecycle, loading tracking, settings watching
- ❌ **Tight coupling**: Directly resolving 5+ services inside state factory
- ❌ **Mixed concerns**: UI reactivity + business logic + service coordination
- ❌ **Hard to test**: Async initialization, auto-triggering effects
- ❌ **Complex prop type logic**: 35 lines of mapping logic embedded in state (lines 268-302)
- ❌ **High impact**: Pictographs used everywhere (Build, Animator, Gallery, Quiz)

## Solution Architecture

### 1. Extract Service: `PropTypeConfigurationService`

**Location:** [src/lib/shared/pictograph/prop/services/implementations/PropTypeConfigurationService.ts](../src/lib/shared/pictograph/prop/services/implementations/PropTypeConfigurationService.ts)

Extracted complex prop type mapping logic into a testable service:

```typescript
// Before: 35 lines of mapping logic in state
const propTypeMapping: Record<string, string> = {
  /* ... */
};
const userPropType =
  propTypeMapping[selectedPropType] || selectedPropType.toLowerCase();
const updatedPictographData = {
  /* manual transformation */
};

// After: Clean service interface
propTypeConfigService.mapPropTypeToFilename(uiPropType);
propTypeConfigService.applyPropTypeToPictographData(
  pictographData,
  userPropType
);
```

### 2. Create Independent Sub-States

**Domain-Aligned Organization:**

- ✅ Arrow state in `arrow/state/` (arrow domain)
- ✅ Prop state in `prop/state/` (prop domain)
- ✅ Shared states in `shared/state/` (cross-cutting concerns)

#### PictographDataState (75 lines)

**Location:** [src/lib/shared/pictograph/shared/state/PictographDataState.svelte.ts](../src/lib/shared/pictograph/shared/state/PictographDataState.svelte.ts)

- Data transformation
- Component requirements
- Display letter derivation
- **Independent** - no dependencies on other states

#### PictographLoadingState (95 lines)

**Location:** [src/lib/shared/pictograph/shared/state/PictographLoadingState.svelte.ts](../src/lib/shared/pictograph/shared/state/PictographLoadingState.svelte.ts)

- Component loading tracking
- Error management
- Loading status derivation
- **Independent** - takes required components & validation as parameters

#### PictographArrowState (92 lines)

**Location:** [src/lib/shared/pictograph/arrow/state/PictographArrowState.svelte.ts](../src/lib/shared/pictograph/arrow/state/PictographArrowState.svelte.ts)

- Arrow positioning
- Arrow assets management
- Lifecycle coordination
- **Independent** - no dependency on prop state
- **Lives in arrow domain** for domain-aligned organization

#### PictographPropState (153 lines)

**Location:** [src/lib/shared/pictograph/prop/state/PictographPropState.svelte.ts](../src/lib/shared/pictograph/prop/state/PictographPropState.svelte.ts)

- Prop positioning
- Prop assets management
- User prop type integration
- **Independent** - no dependency on arrow state
- **Lives in prop domain** for domain-aligned organization

### 3. Simple Composition (No Orchestrator!)

**Location:** [src/lib/shared/pictograph/shared/state/pictograph-state.svelte.ts](../src/lib/shared/pictograph/shared/state/pictograph-state.svelte.ts)

```typescript
// Clean composition - just delegation, no orchestration!
const dataState = createPictographDataState(
  data,
  dataService,
  componentService
);
const loadingState = createPictographLoadingState(
  () => dataState.requiredComponents,
  () => dataState.hasValidData
);
const arrowState = createPictographArrowState(arrowLifecycleManager);
const propState = createPictographPropState(
  propSvgLoader,
  propPlacementService,
  propTypeConfigService
);

// Return composed state - simple getters
return {
  get effectivePictographData() {
    return dataState?.effectivePictographData ?? null;
  },
  get arrowPositions() {
    return arrowState?.arrowPositions ?? {};
  },
  get propPositions() {
    return propState?.propPositions ?? {};
  },
  // ... etc
};
```

**Why no orchestrator?** The sub-states are **completely independent**:

- Arrow positioning doesn't depend on prop positioning
- Prop positioning doesn't depend on arrow positioning
- Loading state just tracks both
- No coordination logic needed!

## Files Created

### New Services

- ✅ `PropTypeConfigurationService.ts` - Prop type mapping logic
- ✅ `IPropTypeConfigurationService.ts` - Service contract

### New Sub-States (Domain-Aligned)

- ✅ `shared/state/PictographDataState.svelte.ts` - Data transformation (shared concern)
- ✅ `shared/state/PictographLoadingState.svelte.ts` - Loading tracking (shared concern)
- ✅ `arrow/state/PictographArrowState.svelte.ts` - Arrow positioning (**arrow domain**)
- ✅ `prop/state/PictographPropState.svelte.ts` - Prop positioning (**prop domain**)
- ✅ `arrow/state/index.ts` & `prop/state/index.ts` - Module exports

### Updated Files

- ✅ `pictograph-state.svelte.ts` - Simplified to 280 lines (was 469)
- ✅ `pictograph.module.ts` - Registered PropTypeConfigurationService
- ✅ `types.ts` - Added IPropTypeConfigurationService symbol
- ✅ `prop/services/contracts/index.ts` - Export new contract
- ✅ `prop/services/implementations/index.ts` - Export new implementation

### Archived

- 📦 `pictograph-state.old.svelte.ts` - Original 469-line god object (backup)

## Results

### Before

```
pictograph-state.svelte.ts: 469 lines
├─ Service resolution (inside state factory)
├─ Data transformation (mixed concerns)
├─ Arrow lifecycle (197-241)
├─ Prop lifecycle (243-376)
├─ Loading state (378-392)
├─ Complex prop type mapping (268-302)
└─ Settings watching
```

### After

```
pictograph-state.svelte.ts: 280 lines (clean composition)
├─ PictographDataState: 75 lines
├─ PictographLoadingState: 95 lines
├─ PictographArrowState: 92 lines
├─ PictographPropState: 153 lines
└─ PropTypeConfigurationService: 67 lines

Total: 762 lines across focused modules (vs 469 monolithic lines)
```

## Benefits

### ✅ Separation of Concerns

- Each state has **one responsibility**
- Business logic extracted to services
- UI reactivity cleanly separated

### ✅ Independent & Testable

- Sub-states can be tested in isolation
- No complex async initialization in tests
- Services injected via parameters (not resolved internally)

### ✅ Maintainable

- Small, focused files (75-153 lines each)
- Clear boundaries
- Easy to understand and modify

### ✅ Reusable

- Sub-states can be composed differently if needed
- Services can be used elsewhere
- No tight coupling

### ✅ No Unnecessary Abstraction

- **No orchestrator** - just simple composition
- Arrow and prop states are independent
- Clean, direct delegation

## Comparison to BuildTab Refactoring

### BuildTab (Needed Orchestrator)

```
SequenceStateOrchestrator: 479 lines
├─ Coordination logic (beat operations across states)
├─ Complex lifecycle (persistence, reversal detection)
├─ Shared operations (multiple states must collaborate)
└─ Multiple consumers (5+ sub-tabs)
```

### Pictograph (No Orchestrator Needed)

```
pictograph-state: 280 lines
├─ Simple composition (no coordination)
├─ Independent sub-states (no collaboration)
├─ Parallel workflows (arrow and prop don't interact)
└─ Single consumer pattern
```

## Testing Strategy

### Unit Tests (Recommended)

```typescript
// Test each sub-state independently
describe("PictographArrowState", () => {
  it("should calculate arrow positions", async () => {
    const mockLifecycleManager = createMock<IArrowLifecycleManager>();
    const state = createPictographArrowState(mockLifecycleManager);
    await state.calculateArrowPositions(mockPictographData);
    expect(state.arrowPositions).toBeDefined();
  });
});

// Test service in isolation
describe("PropTypeConfigurationService", () => {
  it("should map UI prop types to filenames", () => {
    const service = new PropTypeConfigurationService();
    expect(service.mapPropTypeToFilename("Staff")).toBe("staff");
    expect(service.mapPropTypeToFilename("Simplestaff")).toBe("simple_staff");
  });
});
```

### Integration Test

```typescript
describe("PictographState Integration", () => {
  it("should compose all sub-states correctly", async () => {
    const state = createPictographState(mockPictographData);
    await state.calculateArrowPositions();
    await state.calculatePropPositions();

    expect(state.effectivePictographData).toBeDefined();
    expect(state.arrowPositions).toBeDefined();
    expect(state.propPositions).toBeDefined();
  });
});
```

## Migration Notes

### For Developers

- **No API changes** - Public interface unchanged
- **Backward compatible** - Drop-in replacement
- **Same imports** - `createPictographState()` works exactly the same

### For Future Refactoring

- If you need to add new positioning logic, create a new sub-state **in the appropriate domain folder**
- If you need to modify arrow logic, edit `arrow/state/PictographArrowState` only
- If you need to modify prop logic, edit `prop/state/PictographPropState` only
- If you need to change mapping, edit `PropTypeConfigurationService` only
- **Keep domain boundaries clear** - arrow concerns in `arrow/`, prop concerns in `prop/`

## Key Learnings

1. **Not everything needs an orchestrator** - Use orchestration only when sub-states must coordinate
2. **Extract complex logic to services** - Don't embed business logic in state
3. **Compose, don't orchestrate** - When sub-states are independent, simple composition works best
4. **Service injection > service resolution** - Pass services as parameters for better testing
5. **One responsibility per file** - Split large files by concern, not arbitrarily
6. **Align state with domain boundaries** - Put state in the domain it belongs to (arrow state in `arrow/`, prop state in `prop/`)

## Related Documentation

- [BuildTab Refactoring Battle Plan](./BuildTab-Refactoring-Battle-Plan.md)
- [BuildTab Architecture Visual](./BuildTab-Architecture-Visual.md)
- [ToolPanel Refactoring Summary](./ToolPanel-Refactoring-Summary.md)

## Next Steps (Optional Future Improvements)

1. Add unit tests for sub-states
2. Add integration tests for composition
3. Extract additional prop logic if needed
4. Consider creating similar sub-states for AnimatorState (if it has similar complexity)

---

**Refactored by:** Claude
**Approved by:** Austen
**Pattern:** Decomposition without orchestration
