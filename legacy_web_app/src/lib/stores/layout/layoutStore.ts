// src/lib/stores/layout/layoutStore.ts
import { writable } from 'svelte/store';

// Interface for layout information
export interface LayoutInfo {
  rows: number;
  cols: number;
  beatCount: number;
  lastChanged: number; // Timestamp of last change
}

// Create a writable store with initial values
const createLayoutStore = () => {
  const initialLayout: LayoutInfo = {
    rows: 1,
    cols: 1,
    beatCount: 0,
    lastChanged: Date.now()
  };

  const { subscribe, set, update } = writable<LayoutInfo>(initialLayout);

  return {
    subscribe,

    // Update the layout information
    updateLayout: (rows: number, cols: number, beatCount: number) => {
      update(layout => {
        // Only update lastChanged if the layout actually changed
        const layoutChanged = layout.rows !== rows || layout.cols !== cols;
        return {
          rows,
          cols,
          beatCount,
          lastChanged: layoutChanged ? Date.now() : layout.lastChanged
        };
      });
    },

    // Reset the layout to initial values
    reset: () => set(initialLayout)
  };
};

// Export the store
export const layoutStore = createLayoutStore();
