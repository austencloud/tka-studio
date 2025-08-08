/**
 * State Registry
 *
 * A central registry for all state machines and stores in the application.
 * This helps with:
 * - Tracking all state containers
 * - Providing debugging capabilities
 * - Enabling persistence
 * - Facilitating testing
 */

import { browser } from '$app/environment';
import { writable, get, type Writable, type Readable } from 'svelte/store';
import {
  createActor,
  type AnyActorRef,
  type AnyStateMachine,
  type ActorOptions,
  type AnyEventObject,
  type Actor,
  type SnapshotFrom,
  type InspectionEvent
} from 'xstate';

// Import from our modules
import type {
  StateContainer,
  StateContainerType,
  RegisterOptions,
  RegisterMachineOptions,
  RegisterStoreOptions,
  PersistedStateCache
} from './types.js';
import { DataCorruptionError } from './errors.js';
import { validateMachineSnapshot, validateStoreData } from './validation.js';
import {
  addDependency as addDep,
  getDependencies as getDeps,
  getDependents as getDepends,
  topologicalSort
} from './dependencies.js';
import { loadPersistedState, performPersist } from './persistence.js';
import { debugRegistry } from './debug.js';

// Re-export types and errors for external use
export * from './types.js';
export * from './errors.js';

// The registry itself
class StateRegistry {
  private containers: Map<string, StateContainer> = new Map();
  private persistenceEnabled = browser && typeof localStorage !== 'undefined';
  private persistenceKey = 'app_state';
  private persistedState: Record<string, any> = {};
  private lastPersistedState: PersistedStateCache = {}; // Cache for selective persistence
  private persistenceDebounceTimer: ReturnType<typeof setTimeout> | null = null;
  private persistenceDebounceDelay = 300; // ms
  private dependencies: Map<string, Set<string>> = new Map(); // Track dependencies between state containers

  constructor() {
    if (this.persistenceEnabled) {
      const { persistedState, lastPersistedState } = loadPersistedState(this.persistenceKey);
      this.persistedState = persistedState;
      this.lastPersistedState = lastPersistedState;

      if (typeof window !== 'undefined') {
        window.addEventListener('beforeunload', () => {
          this.persistState();
        });
      }
    }
  }

  /**
   * Register a state container (machine or store)
   */
  register<T extends AnyActorRef | Readable<any>>(
    id: string,
    instance: T,
    options: RegisterOptions
  ): T {
    if (this.containers.has(id)) {
      console.warn(`State container with ID "${id}" is already registered. Overwriting.`);
      // Clean up existing subscriptions if any
      this.unregister(id);
    }

    this.containers.set(id, {
      id,
      instance,
      subscriptions: new Set(),
      ...options
    });

    return instance;
  }

  /**
   * Add a dependency relationship between state containers
   */
  addDependency(dependentId: string, dependencyId: string): boolean {
    return addDep(
      this.dependencies,
      (id) => this.containers.has(id),
      dependentId,
      dependencyId
    );
  }

  /**
   * Get all dependencies for a state container
   */
  getDependencies(id: string): string[] {
    return getDeps(this.dependencies, id);
  }

  /**
   * Get all dependents of a state container
   */
  getDependents(id: string): string[] {
    return getDepends(this.dependencies, id);
  }

  /**
   * Get initialization order based on dependency graph
   */
  getInitializationOrder(): string[] {
    return topologicalSort(this.dependencies, Array.from(this.containers.keys()));
  }

  /**
   * Register a state machine
   */
  registerMachine<T extends AnyStateMachine>(
    id: string,
    machine: T,
    options: RegisterMachineOptions<T> = {}
  ): Actor<T> {
    // Check for persisted state with validation
    let snapshotToRestore: SnapshotFrom<T> | undefined = undefined;
    const persistedData = this.persistedState[id];

    if (persistedData?.type === 'machine') {
      try {
        // Validate persisted snapshot
        if (validateMachineSnapshot(persistedData.snapshot)) {
          snapshotToRestore = persistedData.snapshot;
        } else {
          throw new DataCorruptionError(id);
        }
      } catch (error) {
        console.error(`Invalid persisted snapshot for machine "${id}". Using fallback.`, error);
        // Use the provided snapshot as fallback
        snapshotToRestore = options.snapshot;
      }
    } else {
      // No persisted data, use the provided snapshot
      snapshotToRestore = options.snapshot;
    }

    const actorOptions: ActorOptions<T> = {};

    if (snapshotToRestore) {
      actorOptions.snapshot = snapshotToRestore;
    }

    let actor: Actor<T>;

    if (import.meta.env.DEV) {
      import('../logger')
        .then(({ LogLevel, shouldLog, log }) => {
          actorOptions.inspect = (inspectionEvent: InspectionEvent) => {
            if (!actor) return;
            if (inspectionEvent.type === '@xstate.event' && inspectionEvent.actorRef === actor) {
              if (shouldLog(id, LogLevel.DEBUG)) {
                log(id, LogLevel.DEBUG, 'Event:', inspectionEvent.event);
              }
            } else if (
              inspectionEvent.type === '@xstate.snapshot' &&
              inspectionEvent.actorRef === actor
            ) {
              if (shouldLog(id, LogLevel.DEBUG)) {
                log(id, LogLevel.DEBUG, 'State:', inspectionEvent.snapshot);
              }
            }
          };
        })
        .catch((err) => {
          console.error('Failed to load logger:', err);
        });
    }

    actor = createActor(machine, actorOptions) as Actor<T>;
    actor.start();

    this.containers.set(id, {
      id,
      type: 'machine',
      instance: actor,
      persist: options.persist,
      description: options.description,
      subscriptions: new Set()
    });

    return actor;
  }

  /**
   * Register a Svelte store
   */
  registerStore<T>(
    id: string,
    store: Readable<T>,
    options: RegisterStoreOptions<T> = {}
  ): Readable<T> {
    // Check for persisted state with validation
    const persistedData = this.persistedState[id];

    // If this is a writable store and we have persisted data, restore it
    if (persistedData?.type === 'store' && 'set' in store) {
      const writableStore = store as Writable<T>;
      try {
        // Validate and sanitize persisted data
        if (validateStoreData<T>(persistedData.value)) {
          writableStore.set(persistedData.value);
        } else {
          throw new DataCorruptionError(id);
        }
      } catch (error) {
        console.error(`Failed to restore persisted state for store "${id}":`, error);
        // No need to explicitly fall back to initial state, as it already has that value
      }
    }

    // Create container entry with subscription tracking
    const container: StateContainer = {
      id,
      type: 'store',
      instance: store,
      persist: options.persist,
      description: options.description,
      subscriptions: new Set()
    };

    this.containers.set(id, container);

    return store;
  }

  /**
   * Get a state container by ID
   */
  get<T extends AnyActorRef | Readable<any>>(id: string): T | undefined {
    const container = this.containers.get(id);
    return container ? (container.instance as T) : undefined;
  }

  /**
   * Remove a state container from the registry and clean up all subscriptions
   */
  unregister(id: string): boolean {
    const container = this.containers.get(id);
    if (!container) return false;

    // Clean up based on container type
    if (container.type === 'machine') {
      const actor = container.instance as AnyActorRef;
      if (actor && actor.getSnapshot().status !== 'stopped') {
        try {
          actor.stop();
        } catch (error) {
          console.error(`Error stopping actor ${id}:`, error);
        }
      }
    }

    // Clean up all subscriptions
    if (container.subscriptions) {
      container.subscriptions.forEach((unsubscribe) => {
        try {
          unsubscribe();
        } catch (error) {
          console.error(`Error unsubscribing from ${id}:`, error);
        }
      });
    }

    // Remove from dependencies
    this.dependencies.delete(id);
    // Remove as dependency from other containers
    for (const [depId, deps] of this.dependencies.entries()) {
      deps.delete(id);
    }

    return this.containers.delete(id);
  }

  /**
   * Track a subscription for automatic cleanup
   */
  trackSubscription(id: string, unsubscribe: () => void): void {
    const container = this.containers.get(id);
    if (container && container.subscriptions) {
      container.subscriptions.add(unsubscribe);
    }
  }

  /**
   * Get all registered state containers
   */
  getAll(): StateContainer[] {
    return Array.from(this.containers.values());
  }

  /**
   * Get all state containers of a specific type
   */
  getAllByType(type: StateContainerType): StateContainer[] {
    return this.getAll().filter((container) => container.type === type);
  }

  /**
   * Clear the registry (useful for testing)
   */
  clear(): void {
    // Stop all actors before clearing
    this.getAllByType('machine').forEach((container) => {
      const actor = container.instance as AnyActorRef;
      if (actor && actor.getSnapshot().status !== 'stopped') {
        try {
          actor.stop();
        } catch (error) {
          console.error(`Error stopping actor ${container.id}:`, error);
        }
      }
    });

    // Clean up all subscriptions
    this.containers.forEach((container) => {
      if (container.subscriptions) {
        container.subscriptions.forEach((unsubscribe) => {
          try {
            unsubscribe();
          } catch (error) {
            console.error(`Error during unsubscribe in clear():`, error);
          }
        });
      }
    });

    this.containers.clear();
    this.dependencies.clear();
    this.persistedState = {};
    this.lastPersistedState = {};
  }

  /**
   * Persist state to localStorage with debouncing and selective updating
   */
  persistState(): void {
    if (!this.persistenceEnabled) return;

    // Clear any existing debounce timer
    if (this.persistenceDebounceTimer) {
      clearTimeout(this.persistenceDebounceTimer);
    }

    // Set a new debounce timer
    this.persistenceDebounceTimer = setTimeout(() => {
      this.lastPersistedState = performPersist(
        this.containers,
        this.lastPersistedState,
        this.persistenceKey
      );
    }, this.persistenceDebounceDelay);
  }

  /**
   * Debug helper to log the current state of all containers
   */
  debug(): void {
    debugRegistry(
      this.getAll(),
      (id) => this.getDependencies(id),
      (id) => this.getDependents(id)
    );
  }

  /**
   * Get persisted state for a specific ID (loaded at startup)
   */
  getPersistedState(id: string): any {
    return this.persistedState[id];
  }
}

// Export a singleton instance
export const stateRegistry = new StateRegistry();
