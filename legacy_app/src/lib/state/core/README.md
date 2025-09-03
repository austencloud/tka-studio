# State Management Core

This directory contains the core utilities for state management in the Kinetic Constructor application. It provides a unified approach to state management that works with both Svelte 4 and Svelte 5, with special integration for XState 5.

## Key Components

### Container-based State Management

The container-based approach provides a more direct and ergonomic API for state management compared to the traditional store/registry pattern.

- `container.ts` - Core utilities for creating state containers
- `modernMachine.ts` - Utilities for working with XState 5 machines
- `adapters.ts` - Adapters between different state management approaches
- `svelte5-integration.svelte.ts` - Integration with Svelte 5 runes

## Usage Examples

### Creating a State Container

```typescript
// Create a state container
const counterContainer = createContainer(
  { count: 0 },
  (state, update) => ({
    increment: () => {
      update(state => {
        state.count += 1;
      });
    },
    decrement: () => {
      update(state => {
        state.count -= 1;
      });
    },
    reset: () => {
      update(state => {
        state.count = 0;
      });
    }
  })
);

// Use the container
counterContainer.increment();
console.log(counterContainer.state.count); // 1
```

### Creating a Machine Container

```typescript
// Create a state machine
const counterMachine = createModernMachine({
  id: 'counter',
  initial: 'active',
  context: { count: 0 },
  states: {
    active: {
      on: {
        INCREMENT: {
          actions: assign({
            count: ({ context }) => context.count + 1
          })
        },
        DECREMENT: {
          actions: assign({
            count: ({ context }) => context.count - 1
          })
        },
        RESET: {
          actions: assign({
            count: () => 0
          })
        }
      }
    }
  }
});

// Create a machine container
const counterContainer = createMachineContainer(counterMachine);

// Use the container
counterContainer.send({ type: 'INCREMENT' });
console.log(counterContainer.state.context.count); // 1
```

### Using with Svelte 5 Runes

In a Svelte 5 component (`.svelte` or `.svelte.ts` file):

```svelte
<script lang="ts">
  import { counterContainer } from './counterContainer';
  import { useContainer } from '$lib/state/core/svelte5-integration.svelte';

  // Use the container with Svelte 5 runes
  const counter = useContainer(counterContainer);

  // Create derived values
  const doubleCount = $derived(counter.count * 2);
</script>

<div>
  <h1>Counter: {counter.count}</h1>
  <p>Double: {doubleCount}</p>
  <button onclick={counterContainer.increment}>Increment</button>
  <button onclick={counterContainer.decrement}>Decrement</button>
  <button onclick={counterContainer.reset}>Reset</button>
</div>
```

### Using with XState 5 and Svelte 5 Runes

```svelte
<script lang="ts">
  import { counterMachineContainer } from './counterMachine';
  import { useMachine } from '$lib/state/core/svelte5-integration.svelte';

  // Use the machine with Svelte 5 runes
  const counter = useMachine(counterMachineContainer);
</script>

<div>
  <h1>Counter: {counter.state.context.count}</h1>
  <button onclick={() => counter.send({ type: 'INCREMENT' })}>Increment</button>
  <button onclick={() => counter.send({ type: 'DECREMENT' })}>Decrement</button>
  <button onclick={() => counter.send({ type: 'RESET' })}>Reset</button>
</div>
```

## Migration Guide

When migrating from the old store/registry pattern to the new container-based approach:

1. Create a new container using `createContainer` or `createMachineContainer`
2. Create an adapter using `containerToStore` if needed for backward compatibility
3. Update components to use the new container directly or via the adapter
4. For Svelte 5 components, use the `useContainer` or `useMachine` helpers

See the [State Management Migration Guide](../../../docs/state-management-migration-guide.md) for more details.
