/**
 * Element Reference Store
 *
 * A centralized store for managing DOM element references across components.
 * This solves the problem of sharing element references between components
 * in a way that's resilient to component lifecycle events and hot module reloads.
 */
import { browser } from '$app/environment';
import { writable, get } from 'svelte/store';

export type ElementReferenceMap = {
  [key: string]: HTMLElement | null;
};

// Create a writable store for element references
const createElementReferenceStore = () => {
  // Initialize with empty references
  const { subscribe, set, update } = writable<ElementReferenceMap>({});

  // Try to restore references from localStorage on initialization
  if (browser) {
    try {
      const storedKeys = localStorage.getItem('element-reference-keys');
      if (storedKeys) {
        const keys = JSON.parse(storedKeys) as string[];
        console.log('ElementReferenceStore: Found stored keys:', keys);
      }
    } catch (error) {
      console.error('ElementReferenceStore: Error restoring references:', error);
    }
  }

  return {
    subscribe,

    /**
     * Set an element reference by key
     */
    setElement: (key: string, element: HTMLElement | null) => {
      if (!element) {
        console.warn(`ElementReferenceStore: Attempted to set null element for key "${key}"`);
        return false;
      }

      console.log(`ElementReferenceStore: Setting element for key "${key}"`, element);

      update(refs => {
        // Create a new object to ensure reactivity
        const newRefs = { ...refs, [key]: element };

        // Store the key in localStorage for persistence
        if (browser) {
          try {
            const currentKeys = Object.keys(newRefs);
            localStorage.setItem('element-reference-keys', JSON.stringify(currentKeys));
          } catch (error) {
            console.error('ElementReferenceStore: Error storing reference keys:', error);
          }
        }

        return newRefs;
      });

      // Also store in global fallback for maximum compatibility
      if (browser) {
        (window as any)[`__element_ref_${key}`] = element;
      }

      return true;
    },

    /**
     * Get an element reference by key
     */
    getElement: (key: string): HTMLElement | null => {
      const refs = get({ subscribe });
      const element = refs[key];

      // If not found in store, try global fallback
      if (!element && browser) {
        const globalFallback = (window as any)[`__element_ref_${key}`] as HTMLElement | null;
        if (globalFallback) {
          console.log(`ElementReferenceStore: Using global fallback for key "${key}"`);
          // Update the store with the fallback
          update(refs => ({ ...refs, [key]: globalFallback }));
          return globalFallback;
        }
      }

      return element || null;
    },

    /**
     * Remove an element reference by key
     */
    removeElement: (key: string) => {
      update(refs => {
        const { [key]: _, ...rest } = refs;

        // Update localStorage
        if (browser) {
          try {
            const currentKeys = Object.keys(rest);
            localStorage.setItem('element-reference-keys', JSON.stringify(currentKeys));
          } catch (error) {
            console.error('ElementReferenceStore: Error updating reference keys:', error);
          }
        }

        // Also remove from global fallback
        if (browser) {
          delete (window as any)[`__element_ref_${key}`];
        }

        return rest;
      });
    },

    /**
     * Clear all element references
     */
    clearAll: () => {
      set({});

      // Clear localStorage
      if (browser) {
        try {
          localStorage.removeItem('element-reference-keys');
        } catch (error) {
          console.error('ElementReferenceStore: Error clearing reference keys:', error);
        }
      }
    }
  };
};

// Export a singleton instance
export const elementReferenceStore = createElementReferenceStore();

// Constants for common element keys
export const ELEMENT_KEYS = {
  BEAT_FRAME: 'beatFrame',
  SEQUENCE_WIDGET: 'sequenceWidget',
  CURRENT_WORD_LABEL: 'currentWordLabel'
};
