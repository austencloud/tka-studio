// stores/animation.ts - Proper Svelte store implementation
import { writable, derived } from "svelte/store";
import type { AnimationState, SequenceData, PropState } from "../types.js";

// Default states
const DEFAULT_PROP_STATE: PropState = {
  centerPathAngle: 0,
  staffRotationAngle: 0,
  x: 0,
  y: 0,
};

const DEFAULT_ANIMATION_STATE: AnimationState = {
  isPlaying: false,
  currentBeat: 0,
  totalBeats: 0,
  speed: 1.0,
  loop: false,
  blueProp: { ...DEFAULT_PROP_STATE },
  redProp: { ...DEFAULT_PROP_STATE },
};

// Core animation state
export const animationState = writable<AnimationState>(DEFAULT_ANIMATION_STATE);

// Sequence data
export const sequenceData = writable<SequenceData[]>([]);

// Derived state for UI binding
export const isPlaying = derived(animationState, ($state) => $state.isPlaying);
export const currentBeat = derived(
  animationState,
  ($state) => $state.currentBeat
);
export const totalBeats = derived(
  animationState,
  ($state) => $state.totalBeats
);
export const speed = derived(animationState, ($state) => $state.speed);
export const blueProp = derived(animationState, ($state) => $state.blueProp);
export const redProp = derived(animationState, ($state) => $state.redProp);

// Actions
export const animationActions = {
  play: () => animationState.update((state) => ({ ...state, isPlaying: true })),
  pause: () =>
    animationState.update((state) => ({ ...state, isPlaying: false })),
  reset: () =>
    animationState.update((state) => ({
      ...state,
      currentBeat: 0,
      isPlaying: false,
    })),
  setSpeed: (speed: number) =>
    animationState.update((state) => ({ ...state, speed })),
  setBeat: (beat: number) =>
    animationState.update((state) => ({ ...state, currentBeat: beat })),
  setLoop: (loop: boolean) =>
    animationState.update((state) => ({ ...state, loop })),
  updateProps: (blueProp: PropState, redProp: PropState) =>
    animationState.update((state) => ({ ...state, blueProp, redProp })),
  loadSequence: (sequence: SequenceData[]) => {
    sequenceData.set(sequence);
    animationState.update((state) => ({
      ...state,
      totalBeats: sequence.length - 2, // Exclude metadata and start state
      currentBeat: 0,
      isPlaying: false,
    }));
  },
};
