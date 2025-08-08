/**
 * Right Panel Store
 *
 * Manages the state of the right panel in the sequence interface,
 * including which tab is active and which picker to show.
 */

import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';
import { isSequenceEmpty } from '../state/machines/sequenceMachine/persistence.js';

// Define the tab types
export type RightPanelTab = 'construct' | 'generate';

// Define the picker types for the construct tab
export type ConstructPickerType = 'startPosition' | 'options';

// Interface for the store state
interface RightPanelState {
  activeTab: RightPanelTab;
  constructPicker: ConstructPickerType;
}

// Create the store with default values
function createRightPanelStore() {
  // Initialize with default values
  const initialState: RightPanelState = {
    activeTab: 'construct',
    constructPicker: 'startPosition'
  };

  // Create the writable store
  const { subscribe, set, update } = writable<RightPanelState>(initialState);

  // Return the store with custom methods
  return {
    subscribe,

    // Set the active tab
    setActiveTab: (tab: RightPanelTab) => {
      update(state => ({ ...state, activeTab: tab }));
    },

    // Set the construct picker type
    setConstructPicker: (picker: ConstructPickerType) => {
      update(state => ({ ...state, constructPicker: picker }));
    },

    // Reset to default state
    reset: () => {
      set(initialState);
    }
  };
}

// Create the store instance
export const rightPanelStore = createRightPanelStore();

// Derived store to determine which picker to show in the construct tab
export const activePicker = derived(
  [rightPanelStore, isSequenceEmpty],
  ([$rightPanelStore, $isEmpty]) => {
    // If we're in the generate tab, return null (no picker)
    if ($rightPanelStore.activeTab === 'generate') {
      return null;
    }

    // If the sequence is empty, show the start position picker
    if ($isEmpty) {
      return 'startPosition';
    }

    // Otherwise, use the stored picker type
    return $rightPanelStore.constructPicker;
  }
);

// Derived store for the active tab
export const activeTab = derived(
  rightPanelStore,
  ($rightPanelStore) => $rightPanelStore.activeTab
);
