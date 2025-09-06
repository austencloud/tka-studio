/**
 * Type definitions for the state registry
 */
import type { AnyActorRef, AnyStateMachine, Actor, SnapshotFrom } from 'xstate';
import type { Readable, Writable } from 'svelte/store';

// Types for the registry
export type StateContainerType = 'machine' | 'store';

export interface StateContainer {
  id: string;
  type: StateContainerType;
  instance: AnyActorRef | Readable<any>;
  persist?: boolean;
  description?: string;
  subscriptions?: Set<() => void>; // Track subscriptions for cleanup
}

// Options for registering state containers
export interface RegisterOptions {
  type: StateContainerType;
  persist?: boolean;
  description?: string;
}

// Options for registering machines
export interface RegisterMachineOptions<T extends AnyStateMachine> {
  persist?: boolean;
  description?: string;
  snapshot?: SnapshotFrom<T>;
}

// Options for registering stores
export interface RegisterStoreOptions<T> {
  persist?: boolean;
  description?: string;
  persistFields?: string[]; // Add support for selective field persistence
}

// Persistence data structure
export interface PersistedData {
  [id: string]: {
    type: StateContainerType;
    snapshot?: any; // For machines
    value?: any; // For stores
  };
}

// Cache for tracking last persisted state
export interface PersistedStateCache {
  [id: string]: {
    value?: any;
  };
}
