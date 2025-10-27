/**
 * Sequence Selection State
 *
 * Manages selection state for:
 * - Selected beat NUMBER (0 = start position, 1 = first beat, 2 = second beat, etc.)
 * - Selected start position
 * - Start position editing mode
 *
 * RESPONSIBILITY: Pure selection tracking, no business logic
 *
 * NOTE: Uses beatNumber instead of array index
 * - beatNumber 0 = start position
 * - beatNumber 1 = beats[0] (first beat in array)
 * - beatNumber 2 = beats[1] (second beat in array)
 */

import type { PictographData } from "$shared";

export interface SequenceSelectionStateData {
  selectedBeatNumber: number | null; // 0 = start, 1 = first beat, 2 = second beat, etc.
  selectedStartPosition: PictographData | null;
  hasStartPosition: boolean;
}

export function createSequenceSelectionState() {
  const state = $state<SequenceSelectionStateData>({
    selectedBeatNumber: null,
    selectedStartPosition: null,
    hasStartPosition: false,
  });

  return {
    // Getters
    get selectedBeatNumber() {
      return state.selectedBeatNumber;
    },

    // Legacy getter for backwards compatibility (can be removed after full refactor)
    get selectedBeatIndex() {
      // Convert beatNumber to array index: beatNumber 1 -> index 0, beatNumber 2 -> index 1, etc.
      if (state.selectedBeatNumber === null || state.selectedBeatNumber === 0) {
        return null;
      }
      return state.selectedBeatNumber - 1;
    },

    get selectedStartPosition() {
      return state.selectedStartPosition;
    },
    get hasStartPosition() {
      return state.hasStartPosition;
    },
    get isStartPositionSelected() {
      return state.selectedBeatNumber === 0;
    },

    // Computed
    get hasSelection() {
      return state.selectedBeatNumber !== null;
    },

    // Selection operations
    selectBeat(beatNumber: number | null) {
      state.selectedBeatNumber = beatNumber;
    },

    selectStartPosition() {
      state.selectedBeatNumber = 0;
    },

    clearSelection() {
      state.selectedBeatNumber = null;
    },

    isBeatSelected(beatNumber: number): boolean {
      return state.selectedBeatNumber === beatNumber;
    },

    // Start position management
    setStartPosition(startPosition: PictographData | null) {
      state.selectedStartPosition = startPosition;
      state.hasStartPosition = startPosition !== null;
    },

    // Helpers for beat removal adjustments
    adjustSelectionForRemovedBeat(removedBeatNumber: number) {
      if (state.selectedBeatNumber === removedBeatNumber) {
        state.selectedBeatNumber = null;
      } else if (state.selectedBeatNumber !== null && state.selectedBeatNumber > removedBeatNumber) {
        state.selectedBeatNumber = state.selectedBeatNumber - 1;
      }
    },

    adjustSelectionForInsertedBeat(insertedBeatNumber: number) {
      if (state.selectedBeatNumber !== null && state.selectedBeatNumber >= insertedBeatNumber) {
        state.selectedBeatNumber = state.selectedBeatNumber + 1;
      }
    },

    reset() {
      state.selectedBeatNumber = null;
      state.selectedStartPosition = null;
      state.hasStartPosition = false;
    },
  };
}

export type SequenceSelectionState = ReturnType<typeof createSequenceSelectionState>;
