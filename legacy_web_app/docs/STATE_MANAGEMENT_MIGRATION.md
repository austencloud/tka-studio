# State Management Migration Guide

This document outlines the plan for migrating our current state management approach to a more modern, efficient, and maintainable architecture. This guide is intended for both human developers and AI assistants helping with the migration.

## Current Architecture

Our application currently uses a hybrid state management approach:

1. **XState Machines**: For complex workflows and application-level state
2. **Svelte Stores**: For feature-specific state
3. **Component State**: For local UI state
4. **State Registry**: A central registry for tracking, debugging, and persisting state

While this approach has served us well, it has several challenges:

- Complex boilerplate for creating stores
- Inconsistent reactivity between components and external modules
- Overhead from the registry system
- Transition code that supports both old and new patterns

## Target Architecture

We're moving toward a more streamlined architecture that leverages modern reactive patterns:

1. **Svelte Runes**: For universal, fine-grained reactivity
2. **XState v5**: For complex state machines with improved ergonomics
3. **Layered State Management**: Clear separation of concerns
4. **Simplified State Containers**: Less boilerplate, more direct access

## Migration Strategy

We'll follow a gradual, incremental approach to minimize disruption:

1. **Create New Patterns**: Implement new state management patterns
2. **Build Adapters**: Create adapters between old and new systems
3. **Migrate Feature by Feature**: Start with isolated features
4. **Update Components**: Refactor components to use new patterns
5. **Remove Legacy Code**: Once migration is complete

## Implementation Steps

### Phase 1: Foundation

1. Create simplified state container utilities
2. Set up XState v5 integration
3. Create adapters for backward compatibility
4. Implement testing utilities for new patterns

### Phase 2: Core State Migration

1. Migrate application state machine
2. Migrate sequence state
3. Migrate pictograph state
4. Migrate UI state

### Phase 3: Feature Migration

1. Identify isolated features for initial migration
2. Migrate feature by feature, testing thoroughly
3. Update components to use new state management

### Phase 4: Cleanup

1. Remove legacy state management code
2. Remove adapters and compatibility layers
3. Update documentation

## New Patterns and Utilities

### Simplified State Container

```typescript
// src/lib/state/core/container.ts
export function createContainer<T, A extends Record<string, Function>>(
  initialState: T,
  actions: (state: T) => A,
) {
  // Create state with runes
  const state = $state(initialState);

  // Create actions with access to state
  const boundActions = actions(state);

  // Create a reset function
  const reset = () => {
    Object.assign(state, initialState);
  };

  return {
    // Getter for current state
    get state() {
      return state;
    },

    // Actions
    ...boundActions,

    // Reset function
    reset,
  };
}
```

### XState v5 Setup

```typescript
// src/lib/state/core/machine.ts
import { setup } from "xstate";

export function createMachine<
  TContext extends Record<string, any>,
  TEvent extends { type: string },
>(options: {
  id: string;
  initial: string;
  context: TContext;
  states: Record<string, any>;
  actions?: Record<string, any>;
  services?: Record<string, any>;
}) {
  return setup({
    types: {} as {
      context: TContext;
      events: TEvent;
    },
    actions: options.actions || {},
    actors: options.services || {},
  }).createMachine({
    id: options.id,
    initial: options.initial,
    context: options.context,
    states: options.states,
  });
}
```

### Adapter for Legacy Stores

```typescript
// src/lib/state/core/adapters.ts
import { writable } from "svelte/store";

export function containerToStore<T, A extends Record<string, Function>>(
  container: { state: T } & A,
) {
  const { subscribe, set } = writable(container.state);

  // Create proxy to update store when state changes
  $effect(() => {
    set(container.state);
  });

  return {
    subscribe,
    ...Object.fromEntries(
      Object.entries(container).filter(
        ([key]) => key !== "state" && typeof container[key] === "function",
      ),
    ),
  };
}
```

## Migration Examples

### Before: Svelte Store

```typescript
// Before
function createPictographStore() {
  const { subscribe, set, update } = writable<PictographStoreState>({
    status: "idle",
    data: null,
    error: null,
    // ...more initial state
  });

  function setData(data: PictographData) {
    update((state) => ({ ...state, data }));
  }

  // ...more actions

  return {
    subscribe,
    setData,
    // ...more actions
  };
}
```

### After: Container with Runes

```typescript
// After
function createPictographStore() {
  let state = $state({
    status: "idle",
    data: null,
    error: null,
    // ...more initial state
  });

  // Derived values
  const isLoading = $derived(
    state.status !== "idle" &&
      state.status !== "complete" &&
      state.status !== "error",
  );

  function setData(data: PictographData) {
    state.data = data;
  }

  // ...more actions

  return {
    get state() {
      return state;
    },
    get isLoading() {
      return isLoading;
    },
    setData,
    // ...more actions
  };
}
```

## Testing Strategy

1. **Unit Tests**: Test each new utility and pattern in isolation
2. **Integration Tests**: Test interaction between new state containers
3. **Component Tests**: Test components with new state management
4. **End-to-End Tests**: Verify application behavior remains consistent

## Rollback Plan

If issues arise during migration:

1. Identify the specific component or feature causing problems
2. Revert that component to use the legacy state management
3. Add to the list of "migration blockers" to address later
4. Continue with other parts of the migration

## Timeline and Milestones

1. **Foundation (2 weeks)**

   - Create utilities and patterns
   - Set up testing infrastructure

2. **Core State (3 weeks)**

   - Migrate application state
   - Migrate sequence state

3. **Feature Migration (6-8 weeks)**

   - Migrate features one by one
   - Update components

4. **Cleanup (2 weeks)**
   - Remove legacy code
   - Update documentation

## Resources and References

- [Svelte Runes Documentation](https://svelte.dev/blog/runes)
- [XState v5 Documentation](https://stately.ai/docs/xstate-v5)
- [Testing Reactive State](https://testing-library.com/docs/svelte-testing-library/intro/)
