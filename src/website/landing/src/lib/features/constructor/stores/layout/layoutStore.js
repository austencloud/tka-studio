import { createStore } from "../../core/index.js";

export const layoutStore = createStore({
  beatFrameLayout: {
    rows: 2,
    cols: 4,
    cellSize: 100,
  },
  containerDimensions: {
    width: 800,
    height: 600,
  },
});

export function updateBeatFrameLayout(layout) {
  layoutStore.update((state) => ({
    ...state,
    beatFrameLayout: { ...state.beatFrameLayout, ...layout },
  }));
}

export function updateContainerDimensions(dimensions) {
  layoutStore.update((state) => ({
    ...state,
    containerDimensions: { ...state.containerDimensions, ...dimensions },
  }));
}

// Add updateLayout method to match TypeScript API
export function updateLayout(rows, cols, beatCount) {
  layoutStore.update((state) => ({
    ...state,
    beatFrameLayout: {
      ...state.beatFrameLayout,
      rows,
      cols,
    },
    beatCount,
  }));
}
