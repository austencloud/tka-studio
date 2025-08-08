import { createStore } from "../../core/index.js";

// Sequence machine state
export const sequenceMachineState = createStore({
  currentSequence: null,
  isLoading: false,
  error: null,
  history: [],
  historyIndex: -1,
});

// Sequence actions
export const sequenceActions = {
  // Clear the current sequence
  clearSequence() {
    sequenceMachineState.update((state) => ({
      ...state,
      currentSequence: null,
      history: [...state.history, { action: "clear", timestamp: Date.now() }],
      historyIndex: state.history.length,
    }));
  },

  // Set a new sequence
  setSequence(sequence) {
    sequenceMachineState.update((state) => ({
      ...state,
      currentSequence: sequence,
      history: [
        ...state.history,
        { action: "set", sequence, timestamp: Date.now() },
      ],
      historyIndex: state.history.length,
    }));
  },

  // Add a beat to the sequence
  addBeat(beat) {
    sequenceMachineState.update((state) => {
      const newSequence = state.currentSequence
        ? {
            ...state.currentSequence,
            beats: [...(state.currentSequence.beats || []), beat],
          }
        : { beats: [beat] };

      return {
        ...state,
        currentSequence: newSequence,
        history: [
          ...state.history,
          { action: "addBeat", beat, timestamp: Date.now() },
        ],
        historyIndex: state.history.length,
      };
    });
  },

  // Remove a beat from the sequence
  removeBeat(beatIndex) {
    sequenceMachineState.update((state) => {
      if (!state.currentSequence || !state.currentSequence.beats) return state;

      const newBeats = state.currentSequence.beats.filter(
        (_, index) => index !== beatIndex
      );
      const newSequence = { ...state.currentSequence, beats: newBeats };

      return {
        ...state,
        currentSequence: newSequence,
        history: [
          ...state.history,
          { action: "removeBeat", beatIndex, timestamp: Date.now() },
        ],
        historyIndex: state.history.length,
      };
    });
  },

  // Set loading state
  setLoading(loading) {
    sequenceMachineState.update((state) => ({
      ...state,
      isLoading: loading,
    }));
  },

  // Set error state
  setError(error) {
    sequenceMachineState.update((state) => ({
      ...state,
      error: error,
      isLoading: false,
    }));
  },
};

// Sequence selectors
export const sequenceSelectors = {
  // Get the current sequence
  getCurrentSequence() {
    return sequenceMachineState.get().currentSequence;
  },

  // Get the current sequence beats
  getCurrentBeats() {
    const sequence = sequenceMachineState.get().currentSequence;
    return sequence ? sequence.beats || [] : [];
  },

  // Get the sequence length
  getSequenceLength() {
    const beats = this.getCurrentBeats();
    return beats.length;
  },

  // Check if sequence is empty
  isEmpty() {
    return this.getSequenceLength() === 0;
  },

  // Get loading state
  isLoading() {
    return sequenceMachineState.get().isLoading;
  },

  // Get error state
  getError() {
    return sequenceMachineState.get().error;
  },

  // Get history
  getHistory() {
    return sequenceMachineState.get().history;
  },

  // Get history index
  getHistoryIndex() {
    return sequenceMachineState.get().historyIndex;
  },

  // Check if can undo
  canUndo() {
    const state = sequenceMachineState.get();
    return state.historyIndex > 0;
  },

  // Check if can redo
  canRedo() {
    const state = sequenceMachineState.get();
    return state.historyIndex < state.history.length - 1;
  },
};
