/**
 * Persistence utilities for the state registry
 */
import { get, type Readable } from 'svelte/store';
import type { AnyActorRef } from 'xstate';
import { DataCorruptionError, StorageError } from './errors';
import { validateMachineSnapshot } from './validation';
import type { PersistedData, PersistedStateCache, StateContainer } from './types';

/**
 * Load persisted state from localStorage with enhanced validation and recovery
 */
export function loadPersistedState(persistenceKey: string): {
  persistedState: Record<string, any>;
  lastPersistedState: PersistedStateCache;
} {
  const persistedState: Record<string, any> = {};
  const lastPersistedState: PersistedStateCache = {};

  try {
    const persistedStateJson = localStorage.getItem(persistenceKey);
    if (!persistedStateJson) {
      return { persistedState, lastPersistedState };
    }

    // Parse the JSON data
    const parsedData = JSON.parse(persistedStateJson);

    // Validate the overall structure
    if (typeof parsedData !== 'object' || parsedData === null) {
      throw new DataCorruptionError('root');
    }

    // Process each entry with validation
    Object.entries(parsedData).forEach(([id, data]: [string, any]) => {
      try {
        // Basic structure validation
        if (!data || typeof data !== 'object' || !('type' in data)) {
          throw new DataCorruptionError(id);
        }

        // Type-specific validation
        if (
          data.type === 'machine' &&
          (!('snapshot' in data) || !validateMachineSnapshot(data.snapshot))
        ) {
          throw new DataCorruptionError(id);
        } else if (data.type === 'store' && !('value' in data)) {
          throw new DataCorruptionError(id);
        }

        // If it passed validation, add to persisted state
        persistedState[id] = data;

        // Also update last persisted state cache for selective persistence
        if (!lastPersistedState[id]) {
          lastPersistedState[id] = {};
        }

        if (data.type === 'machine') {
          lastPersistedState[id].value = data.snapshot;
        } else if (data.type === 'store') {
          lastPersistedState[id].value = data.value;
        }
      } catch (error) {
        console.warn(`Skipping corrupted state for "${id}":`, error);
        // Don't add corrupted entries to the persistedState object
      }
    });
  } catch (error) {
    console.error('Failed to load or parse persisted state from localStorage:', error);
    // Reset on critical errors and attempt recovery

    // Optionally backup and clear the corrupted data
    if (typeof localStorage !== 'undefined') {
      try {
        // Back up the corrupted data for potential recovery
        const corruptedData = localStorage.getItem(persistenceKey);
        if (corruptedData) {
          localStorage.setItem(`${persistenceKey}_corrupted_backup`, corruptedData);
          localStorage.removeItem(persistenceKey);
        }
      } catch {
        // If even this fails, just give up on persistence for now
      }
    }
  }

  return { persistedState, lastPersistedState };
}

/**
 * Perform the persistence operation
 */
export function performPersist(
  containers: Map<string, StateContainer>,
  lastPersistedState: PersistedStateCache,
  persistenceKey: string
): PersistedStateCache {
  const stateToPersist: PersistedData = {};
  let hasChanges = false;
  const updatedLastPersistedState = { ...lastPersistedState };

  Array.from(containers.values()).forEach((container) => {
    if (!container.persist) return;

    try {
      const instance = container.instance;
      let currentStateValue: any;
      let lastPersistedValue: any = lastPersistedState[container.id]?.value;

      // Extract current state value based on container type
      if (
        container.type === 'machine' &&
        instance &&
        typeof (instance as AnyActorRef).send === 'function'
      ) {
        const actorInstance = instance as AnyActorRef;
        if (actorInstance.getSnapshot().status !== 'stopped') {
          const persistedSnapshot = actorInstance.getPersistedSnapshot();
          if (persistedSnapshot !== undefined) {
            currentStateValue = persistedSnapshot;
            // For machines, we need to compare stringified snapshots since they're complex objects
            if (
              !lastPersistedValue ||
              JSON.stringify(lastPersistedValue) !== JSON.stringify(currentStateValue)
            ) {
              stateToPersist[container.id] = {
                type: 'machine',
                snapshot: currentStateValue
              };
              hasChanges = true;
            }
          }
        }
      } else if (container.type === 'store') {
        const store = instance as Readable<any>;
        currentStateValue = get(store);

        // Check if the current state is different from the last persisted state
        if (
          !lastPersistedValue ||
          JSON.stringify(lastPersistedValue) !== JSON.stringify(currentStateValue)
        ) {
          stateToPersist[container.id] = {
            type: 'store',
            value: currentStateValue
          };
          hasChanges = true;
        }
      }

      // Update the last persisted state cache if we're persisting this item
      if (stateToPersist[container.id]) {
        if (!updatedLastPersistedState[container.id]) {
          updatedLastPersistedState[container.id] = {};
        }
        updatedLastPersistedState[container.id].value = currentStateValue;
      }
    } catch (error) {
      console.error(`Failed to get state for persistence for ${container.id}:`, error);
    }
  });

  // Only save to localStorage if there are changes
  if (hasChanges) {
    try {
      localStorage.setItem(persistenceKey, JSON.stringify(stateToPersist));
    } catch (error) {
      const storageError = new StorageError('write', error instanceof Error ? error : undefined);
      console.error(storageError.message);

      // Attempt to handle quota exceeded errors by clearing less important data
      if (error instanceof DOMException && error.name === 'QuotaExceededError') {
        handleStorageQuotaError(persistenceKey);
      }
    }
  }

  return updatedLastPersistedState;
}

/**
 * Handle storage quota errors by trying to free up space
 */
export function handleStorageQuotaError(persistenceKey: string): void {
  try {
    // Strategy: Remove non-critical persisted states
    // This requires knowledge of which states are critical vs. non-critical
    // Here's a simplified example - in practice, you'd have a more sophisticated approach

    const allPersistedState = JSON.parse(localStorage.getItem(persistenceKey) || '{}');
    const criticalStateKeys = Object.keys(allPersistedState).filter(
      (key) =>
        // Define your criteria for critical states here
        key.includes('user') || key.includes('auth') || key.includes('app')
    );

    const reducedState: Record<string, any> = {};
    criticalStateKeys.forEach((key) => {
      reducedState[key] = allPersistedState[key];
    });

    // Try to save the reduced state
    localStorage.setItem(persistenceKey, JSON.stringify(reducedState));
    console.warn('Storage quota exceeded - reduced persisted state to critical data only');
  } catch (error) {
    console.error('Failed to handle storage quota error:', error);
  }
}
