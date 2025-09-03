/**
 * Debugging utilities for the state registry
 */
import { get, type Readable } from 'svelte/store';
import type { AnyActorRef } from 'xstate';
import type { StateContainer } from './types';

/**
 * Debug helper to log the current state of all containers
 */
export function debugRegistry(
  containers: StateContainer[],
  getDependencies: (id: string) => string[],
  getDependents: (id: string) => string[]
): void {
  console.group('State Registry');
  containers.forEach((container) => {
    console.group(`${container.id} (${container.type})`);
    if (container.description) {
      console.log(`Description: ${container.description}`);
    }

    try {
      const instance = container.instance;
      if (
        container.type === 'machine' &&
        instance &&
        typeof (instance as AnyActorRef).send === 'function'
      ) {
        const actor = instance as AnyActorRef;
        console.log('State:', actor.getSnapshot());
      } else if (container.type === 'store') {
        const store = instance as Readable<any>;
        console.log('Value:', get(store));
      }
    } catch (error) {
      console.error(`Error getting state for ${container.id}:`, error);
    }

    // Add dependency information if available
    const dependencies = getDependencies(container.id);
    if (dependencies.length > 0) {
      console.log('Dependencies:', dependencies);
    }

    const dependents = getDependents(container.id);
    if (dependents.length > 0) {
      console.log('Dependents:', dependents);
    }

    console.groupEnd();
  });
  console.groupEnd();
}
