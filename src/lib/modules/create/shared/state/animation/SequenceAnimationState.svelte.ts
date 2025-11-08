/**
 * Sequence Animation State
 *
 * Manages animation state for:
 * - Beat removal animations
 * - Sequence clearing animations
 * - Multi-beat removal tracking
 *
 * RESPONSIBILITY: Pure animation state tracking
 */

export interface SequenceAnimationStateData {
  removingBeatIndex: number | null;
  removingBeatIndices: Set<number>;
  isClearing: boolean;
}

export function createSequenceAnimationState() {
  const state = $state<SequenceAnimationStateData>({
    removingBeatIndex: null,
    removingBeatIndices: new Set<number>(),
    isClearing: false,
  });

  return {
    // Getters
    get removingBeatIndex() {
      return state.removingBeatIndex;
    },
    get removingBeatIndices() {
      return state.removingBeatIndices;
    },
    get isClearing() {
      return state.isClearing;
    },

    // Computed
    get isAnimating() {
      return (
        state.removingBeatIndex !== null ||
        state.removingBeatIndices.size > 0 ||
        state.isClearing
      );
    },

    // Single beat removal animation
    startRemovingBeat(index: number) {
      state.removingBeatIndex = index;
    },

    endRemovingBeat() {
      state.removingBeatIndex = null;
    },

    // Multi-beat removal animation
    startRemovingBeats(indices: number[]) {
      state.removingBeatIndices = new Set(indices);
    },

    addRemovingBeat(index: number) {
      // Create new Set to trigger Svelte reactivity
      state.removingBeatIndices = new Set([
        ...state.removingBeatIndices,
        index,
      ]);
    },

    endRemovingBeats() {
      state.removingBeatIndices = new Set();
    },

    isBeatRemoving(index: number): boolean {
      return (
        state.removingBeatIndex === index ||
        state.removingBeatIndices.has(index)
      );
    },

    // Sequence clearing animation
    startClearing() {
      state.isClearing = true;
    },

    endClearing() {
      state.isClearing = false;
    },

    reset() {
      state.removingBeatIndex = null;
      state.removingBeatIndices = new Set();
      state.isClearing = false;
    },
  };
}

export type SequenceAnimationState = ReturnType<
  typeof createSequenceAnimationState
>;
