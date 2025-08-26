/**
 * Auto-Sync State Wrapper for TKA
 *
 * Automatically persists state changes without manual saveState() calls.
 * Works with your existing factory pattern and services.
 */

import { browser } from "$app/environment";
import {
  safeLocalStorageGet,
  safeLocalStorageSet,
} from "$lib/utils/safe-storage";

// ============================================================================
// AUTO-SYNC CONFIGURATION
// ============================================================================

interface AutoSyncConfig {
  /** Storage key for persistence */
  key: string;
  /** Debounce delay in milliseconds (default: 500ms) */
  debounceMs?: number;
  /** Whether to use localStorage (true) or sessionStorage (false) */
  persistent?: boolean;
  /** Validation function to check if state is valid before saving */
  validate?: (state: unknown) => boolean;
  /** Transform state before saving (for serialization) */
  beforeSave?: (state: unknown) => unknown;
  /** Transform state after loading (for deserialization) */
  afterLoad?: (state: unknown) => unknown;
}

// ============================================================================
// AUTO-SYNC STATE FACTORY
// ============================================================================

/**
 * Creates auto-syncing reactive state using Svelte 5 runes
 *
 * @example
 * ```typescript
 * // In your existing createBrowseState factory
 * export function createBrowseState(services) {
 *   const autoSyncState = createAutoSyncState({
 *     key: 'tka-browse-state-v3',
 *     debounceMs: 300,
 *     validate: (state) => state && typeof state === 'object'
 *   });
 *
 *   // Load initial state
 *   let browseState = $state(autoSyncState.load({
 *     currentFilter: null,
 *     selectedSequence: null,
 *     scrollPosition: { top: 0, left: 0 }
 *   }));
 *
 *   // Auto-sync any changes to browseState
 *   autoSyncState.sync(() => browseState);
 *
 *   return {
 *     get currentFilter() { return (browseState as any).currentFilter; },
 *     setFilter(type, value) {
 *       (browseState as any).currentFilter = { type, value };
 *       // ✅ Automatically persisted - no manual save needed!
 *     }
 *   };
 * }
 * ```
 */
export function createAutoSyncState<T>(config: AutoSyncConfig) {
  const {
    key,
    debounceMs = 500,
    persistent = true,
    validate = () => true,
    beforeSave = (state) => state,
    afterLoad = (state) => state,
  } = config;

  let saveTimeout: number | null = null;
  let isLoaded = false;

  // ============================================================================
  // STORAGE OPERATIONS
  // ============================================================================

  function saveToStorage(state: T): void {
    if (!browser) return;

    try {
      if (!validate(state)) {
        console.warn(`Invalid state for key "${key}", skipping save`);
        return;
      }

      const transformedState = beforeSave(state);
      const success = safeLocalStorageSet(key, transformedState);

      if (!success) {
        console.error(`Failed to save state for key "${key}"`);
      }
    } catch (error) {
      console.error(`Error saving state for key "${key}":`, error);
    }
  }

  function loadFromStorage<D>(defaultValue: D): T | D {
    if (!browser) return defaultValue;

    try {
      const stored = safeLocalStorageGet<unknown>(key, null);

      if (stored === null) {
        return defaultValue;
      }

      const transformedState = afterLoad(stored);
      isLoaded = true;
      return transformedState as T;
    } catch (error) {
      console.error(`Error loading state for key "${key}":`, error);
      return defaultValue;
    }
  }

  // ============================================================================
  // AUTO-SYNC EFFECT
  // ============================================================================

  /**
   * Creates automatic state synchronization effect
   *
   * @param getState - Function that returns current state to sync
   * @returns Cleanup function to stop syncing
   */
  function sync(getState: () => T): () => void {
    // Create effect that runs whenever getState() changes
    const cleanup = $effect.root(() => {
      $effect(() => {
        const currentState = getState();

        // Skip initial load to avoid saving default state immediately
        if (!isLoaded) {
          isLoaded = true;
          return;
        }

        // Debounced save
        if (saveTimeout) {
          clearTimeout(saveTimeout);
        }

        saveTimeout = window.setTimeout(() => {
          saveToStorage(currentState);
        }, debounceMs);
      });
    });

    // Return cleanup function
    return () => {
      if (saveTimeout) {
        clearTimeout(saveTimeout);
      }
      cleanup();
    };
  }

  // ============================================================================
  // MANUAL OPERATIONS
  // ============================================================================

  /**
   * Load initial state from storage
   */
  function load<D>(defaultValue: D): T | D {
    return loadFromStorage(defaultValue);
  }

  /**
   * Immediately save state (skip debouncing)
   */
  function saveNow(state: T): void {
    if (saveTimeout) {
      clearTimeout(saveTimeout);
      saveTimeout = null;
    }
    saveToStorage(state);
  }

  /**
   * Clear persisted state
   */
  function clear(): void {
    if (!browser) return;
    localStorage.removeItem(key);
  }

  /**
   * Check if state exists in storage
   */
  function exists(): boolean {
    if (!browser) return false;
    return localStorage.getItem(key) !== null;
  }

  return {
    sync,
    load,
    saveNow,
    clear,
    exists,
  };
}

// ============================================================================
// SPECIALIZED AUTO-SYNC FACTORIES
// ============================================================================

/**
 * Auto-sync factory specifically for browse state
 */
export function createBrowseAutoSync() {
  return createAutoSyncState({
    key: "tka-browse-state-v3",
    debounceMs: 300, // Faster saves for browse interactions
    validate: (state: unknown) =>
      Boolean(state && typeof state === "object" && state !== null),
    beforeSave: (state: unknown) => {
      // Add timestamp for debugging
      return {
        ...(state as object),
        lastSaved: new Date().toISOString(),
      };
    },
    afterLoad: (state: unknown) => {
      // Remove timestamp after loading
      const { lastSaved, ...cleanState } = state as {
        lastSaved?: string;
        [key: string]: unknown;
      };
      return cleanState;
    },
  });
}

/**
 * Auto-sync factory for sequence state
 */
export function createSequenceAutoSync(sequenceId: string) {
  return createAutoSyncState({
    key: `tka-sequence-state-${sequenceId}`,
    debounceMs: 1000, // Slower saves for sequence editing
    validate: (state: unknown) =>
      Boolean(state && typeof state === "object" && state !== null),
  });
}

/**
 * Auto-sync factory for app-level state
 */
export function createAppAutoSync() {
  return createAutoSyncState({
    key: "tka-app-state-v3",
    debounceMs: 200, // Fast saves for UI state
    validate: (state: unknown) =>
      Boolean(state && typeof state === "object" && state !== null),
  });
}

// ============================================================================
// USAGE EXAMPLE IN EXISTING FACTORIES
// ============================================================================

/**
 * Example: Enhanced browse state factory with auto-sync
 * You can use this pattern in your existing createBrowseState factory
 */
export function createEnhancedBrowseStateExample(services: any) {
  const autoSync = createBrowseAutoSync();

  // Load initial state
  const initialState = autoSync.load({
    currentFilter: null,
    selectedSequence: null,
    displayMode: "grid",
    scrollPosition: { top: 0, left: 0 },
    searchQuery: "",
  });

  // Reactive state
  let browseState = $state(initialState);

  // Setup auto-sync
  const cleanup = autoSync.sync(() => browseState);

  return {
    // Reactive getters
    get currentFilter() {
      return (browseState as any).currentFilter;
    },
    get selectedSequence() {
      return (browseState as any).selectedSequence;
    },
    get displayMode() {
      return (browseState as any).displayMode;
    },
    get scrollPosition() {
      return (browseState as any).scrollPosition;
    },
    get searchQuery() {
      return (browseState as any).searchQuery;
    },

    // Actions (automatically persisted)
    setFilter(type: string, value: unknown) {
      (browseState as any).currentFilter = { type, value };
      // ✅ Auto-saved with debouncing!
    },

    selectSequence(sequence: any) {
      (browseState as any).selectedSequence = sequence;
      // ✅ Auto-saved with debouncing!
    },

    setScrollPosition(position: { top: number; left: number }) {
      (browseState as any).scrollPosition = position;
      // ✅ Auto-saved with debouncing!
    },

    updateSearch(query: string) {
      (browseState as any).searchQuery = query;
      // ✅ Auto-saved with debouncing!
    },

    // Manual operations
    saveStateNow() {
      autoSync.saveNow(browseState);
    },

    clearPersistedState() {
      autoSync.clear();
    },

    // Cleanup
    destroy() {
      cleanup();
    },
  };
}
