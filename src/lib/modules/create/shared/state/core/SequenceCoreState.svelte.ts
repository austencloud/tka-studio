/**
 * Sequence Core State
 *
 * Manages the fundamental sequence state:
 * - Current sequence being edited
 * - List of all sequences
 * - Loading/error states
 * - Grid mode
 *
 * RESPONSIBILITY: Pure state management, no business logic or side effects
 */

import type { SequenceData } from "$shared";
import { GridMode } from "$shared";

export interface SequenceCoreStateData {
  currentSequence: SequenceData | null;
  sequences: SequenceData[];
  isLoading: boolean;
  error: string | null;
  gridMode: GridMode;
  selectedSequenceId: string | null;
}

export function createSequenceCoreState() {
  const state = $state<SequenceCoreStateData>({
    currentSequence: null,
    sequences: [],
    isLoading: false,
    error: null,
    gridMode: GridMode.DIAMOND,
    selectedSequenceId: null,
  });

  return {
    // Getters
    get currentSequence() {
      return state.currentSequence;
    },
    get sequences() {
      return state.sequences;
    },
    get isLoading() {
      return state.isLoading;
    },
    get error() {
      return state.error;
    },
    get gridMode() {
      return state.gridMode;
    },
    get selectedSequenceId() {
      return state.selectedSequenceId;
    },

    // Computed
    get hasSequence() {
      return state.currentSequence !== null;
    },
    get sequenceCount() {
      return state.sequences.length;
    },

    // Setters
    setCurrentSequence(sequence: SequenceData | null) {
      state.currentSequence = sequence;
      state.selectedSequenceId = sequence?.id ?? null;
    },

    setSequences(sequences: SequenceData[]) {
      state.sequences = sequences;
    },

    addSequence(sequence: SequenceData) {
      state.sequences.push(sequence);
    },

    updateSequence(updatedSequence: SequenceData) {
      const index = state.sequences.findIndex(
        (s) => s.id === updatedSequence.id
      );
      if (index >= 0) {
        state.sequences[index] = updatedSequence;
      }
      if (state.currentSequence?.id === updatedSequence.id) {
        state.currentSequence = updatedSequence;
      }
    },

    removeSequence(sequenceId: string) {
      state.sequences = state.sequences.filter((s) => s.id !== sequenceId);
      if (state.currentSequence?.id === sequenceId) {
        state.currentSequence = null;
        state.selectedSequenceId = null;
      }
    },

    setLoading(loading: boolean) {
      state.isLoading = loading;
    },

    setError(error: string | null) {
      state.error = error;
    },

    clearError() {
      state.error = null;
    },

    setGridMode(mode: GridMode) {
      state.gridMode = mode;
    },

    reset() {
      state.currentSequence = null;
      state.sequences = [];
      state.isLoading = false;
      state.error = null;
      state.gridMode = GridMode.DIAMOND;
      state.selectedSequenceId = null;
    },
  };
}

export type SequenceCoreState = ReturnType<typeof createSequenceCoreState>;
