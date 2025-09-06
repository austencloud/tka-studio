import { writable, derived } from 'svelte/store';

export interface SequenceSelection {
  selectedBeats: number[];
  selectionMode: 'single' | 'multi' | 'range';
  lastSelectedBeat?: number;
}

function createSelectionStore() {
  const { subscribe, set, update } = writable<SequenceSelection>({
    selectedBeats: [],
    selectionMode: 'single'
  });

  return {
    subscribe,

    selectBeat: (beatIndex: number) => update(state => {
      switch (state.selectionMode) {
        case 'single':
          return {
            ...state,
            selectedBeats: [beatIndex],
            lastSelectedBeat: beatIndex
          };

        case 'multi':
          const isAlreadySelected = state.selectedBeats.includes(beatIndex);
          return {
            ...state,
            selectedBeats: isAlreadySelected
              ? state.selectedBeats.filter(b => b !== beatIndex)
              : [...state.selectedBeats, beatIndex],
            lastSelectedBeat: beatIndex
          };

        case 'range':
          const { lastSelectedBeat } = state;
          if (lastSelectedBeat === undefined) {
            return {
              ...state,
              selectedBeats: [beatIndex],
              lastSelectedBeat: beatIndex
            };
          }

          const start = Math.min(lastSelectedBeat, beatIndex);
          const end = Math.max(lastSelectedBeat, beatIndex);
          const rangeBeats = Array.from(
            { length: end - start + 1 },
            (_, i) => start + i
          );

          return {
            ...state,
            selectedBeats: rangeBeats,
            lastSelectedBeat: beatIndex
          };
      }
    }),

    setSelectionMode: (mode: SequenceSelection['selectionMode']) =>
      update(state => ({ ...state, selectionMode: mode })),

    clearSelection: () =>
      update(state => ({ ...state, selectedBeats: [], lastSelectedBeat: undefined })),

    isSelected: (beatIndex: number) => {
      let isSelected = false;
      subscribe(state => {
        isSelected = state.selectedBeats.includes(beatIndex);
      })();
      return isSelected;
    }
  };
}

export const selectionStore = createSelectionStore();

// Derived stores for convenience
export const selectedBeats = derived(
  selectionStore,
  $selection => $selection.selectedBeats
);

export const selectionMode = derived(
  selectionStore,
  $selection => $selection.selectionMode
);
