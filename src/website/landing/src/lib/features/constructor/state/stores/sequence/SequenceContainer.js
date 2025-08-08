import { createContainer } from "../../../core/container.js";

export const sequenceContainer = createContainer(
  {
    beats: [],
    startPosition: null,
    metadata: { name: "", difficulty: 1 },
    selectedBeatIds: [],
  },
  (state, update) => ({
    addBeat: (beat) => {
      update((state) => {
        state.beats.push(beat);
      });
    },
    removeBeat: (index) => {
      update((state) => {
        state.beats.splice(index, 1);
      });
    },
    selectBeat: (beatId) => {
      update((state) => {
        if (!state.selectedBeatIds.includes(beatId)) {
          state.selectedBeatIds.push(beatId);
        }
      });
    },
    clearSelection: () => {
      update((state) => {
        state.selectedBeatIds = [];
      });
    },
  })
);
