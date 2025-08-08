/**
 * Store for managing the loading state during transitions between components
 */
import { writable } from 'svelte/store';

// Create a store for the transition loading state that can be accessed globally
export const transitionLoadingStore = writable(false);

// Helper functions to manipulate the store
export const transitionLoading = {
  /**
   * Start the loading state
   */
  start: () => {
    transitionLoadingStore.set(true);
  },

  /**
   * End the loading state
   */
  end: () => {
    transitionLoadingStore.set(false);
  },

  /**
   * Toggle the loading state
   */
  toggle: () => {
    transitionLoadingStore.update(state => !state);
  }
};

export default transitionLoading;
