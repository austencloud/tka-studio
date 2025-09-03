import { writable, derived } from 'svelte/store';
import { actStore } from './actStore';

// Define the selection state interface
interface SelectionState {
  selectedRow: number | null;
  selectedCol: number | null;
}

// Create the initial state
const initialState: SelectionState = {
  selectedRow: null,
  selectedCol: null
};

// Create the writable store
function createSelectionStore() {
  const { subscribe, set, update } = writable<SelectionState>(initialState);

  return {
    subscribe,

    /**
     * Select a beat at the specified row and column
     */
    selectBeat: (row: number, col: number) => {
      update(state => ({
        ...state,
        selectedRow: row,
        selectedCol: col
      }));
    },

    /**
     * Clear the current selection
     */
    clearSelection: () => {
      set(initialState);
    }
  };
}

// Create and export the store
export const selectionStore = createSelectionStore();

// Create derived store for the currently selected beat
export const selectedBeat = derived(
  [selectionStore, actStore],
  ([$selection, $actStore]) => {
    const { selectedRow, selectedCol } = $selection;

    if (selectedRow === null || selectedCol === null) {
      return null;
    }

    const sequences = $actStore.act.sequences;
    if (selectedRow < sequences.length) {
      const sequence = sequences[selectedRow];
      if (selectedCol < sequence.beats.length) {
        return {
          beat: sequence.beats[selectedCol],
          row: selectedRow,
          col: selectedCol
        };
      }
    }

    return null;
  }
);
