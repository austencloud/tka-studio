/**
 * Animation Panel State Factory
 *
 * Manages all reactive state for the animation panel using Svelte 5 runes pattern.
 * Provides clean getters/setters following TKA state management conventions.
 */

import type { SequenceData } from "$shared";
import type { PropState } from "../domain";

// ============================================================================
// PERSISTENCE CONSTANTS
// ============================================================================

const ANIMATION_LOOP_STATE_KEY = "tka_animation_loop_state";

export type AnimationPanelState = {
  // Playback state
  readonly currentBeat: number;
  readonly isPlaying: boolean;
  readonly speed: number;
  readonly shouldLoop: boolean;

  // Sequence metadata
  readonly totalBeats: number;
  readonly sequenceWord: string;
  readonly sequenceAuthor: string;

  // Prop rendering states
  readonly bluePropState: PropState;
  readonly redPropState: PropState;

  // Loading state
  readonly loading: boolean;
  readonly error: string | null;
  readonly sequenceData: SequenceData | null;

  // State mutators
  setCurrentBeat: (beat: number) => void;
  setIsPlaying: (playing: boolean) => void;
  setSpeed: (speed: number) => void;
  setShouldLoop: (loop: boolean) => void;
  setTotalBeats: (beats: number) => void;
  setSequenceMetadata: (word: string, author: string) => void;
  setBluePropState: (state: PropState) => void;
  setRedPropState: (state: PropState) => void;
  setPropStates: (blue: PropState, red: PropState) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setSequenceData: (data: SequenceData | null) => void;
  reset: () => void;
};

const DEFAULT_PROP_STATE: PropState = {
  centerPathAngle: 0,
  staffRotationAngle: 0,
  // x and y are optional - only set for dash motions
};

export function createAnimationPanelState(): AnimationPanelState {
  // Load persisted loop state
  const loadLoopState = (): boolean => {
    try {
      const stored = localStorage.getItem(ANIMATION_LOOP_STATE_KEY);
      return stored ? JSON.parse(stored) : false;
    } catch (error) {
      console.error("❌ Failed to load loop state:", error);
      return false;
    }
  };

  // Save loop state to localStorage
  const saveLoopState = (loop: boolean): void => {
    try {
      localStorage.setItem(ANIMATION_LOOP_STATE_KEY, JSON.stringify(loop));
    } catch (error) {
      console.error("❌ Failed to save loop state:", error);
    }
  };

  // Playback state
  let currentBeat = $state(0);
  let isPlaying = $state(false);
  let speed = $state(1.0);
  let shouldLoop = $state(loadLoopState());

  // Sequence metadata
  let totalBeats = $state(0);
  let sequenceWord = $state("");
  let sequenceAuthor = $state("");

  // Prop states
  let bluePropState = $state<PropState>({ ...DEFAULT_PROP_STATE });
  let redPropState = $state<PropState>({ ...DEFAULT_PROP_STATE });

  // Loading state
  let loading = $state(false);
  let error = $state<string | null>(null);
  let sequenceData = $state<SequenceData | null>(null);

  return {
    // Getters
    get currentBeat() { return currentBeat; },
    get isPlaying() { return isPlaying; },
    get speed() { return speed; },
    get shouldLoop() { return shouldLoop; },
    get totalBeats() { return totalBeats; },
    get sequenceWord() { return sequenceWord; },
    get sequenceAuthor() { return sequenceAuthor; },
    get bluePropState() { return bluePropState; },
    get redPropState() { return redPropState; },
    get loading() { return loading; },
    get error() { return error; },
    get sequenceData() { return sequenceData; },

    // Setters
    setCurrentBeat: (beat: number) => {
      currentBeat = beat;
    },

    setIsPlaying: (playing: boolean) => {
      isPlaying = playing;
    },

    setSpeed: (newSpeed: number) => {
      speed = Math.max(0.1, Math.min(3.0, newSpeed));
    },

    setShouldLoop: (loop: boolean) => {
      shouldLoop = loop;
      saveLoopState(loop);
    },

    setTotalBeats: (beats: number) => {
      totalBeats = beats;
    },

    setSequenceMetadata: (word: string, author: string) => {
      sequenceWord = word;
      sequenceAuthor = author;
    },

    setBluePropState: (state: PropState) => {
      console.log("🔵 AnimationPanelState: Setting blue prop state:", state);
      bluePropState = { ...state };
    },

    setRedPropState: (state: PropState) => {
      console.log("🔴 AnimationPanelState: Setting red prop state:", state);
      redPropState = { ...state };
    },

    setPropStates: (blue: PropState, red: PropState) => {

      bluePropState = { ...blue };
      redPropState = { ...red };
    },

    setLoading: (isLoading: boolean) => {
      loading = isLoading;
    },

    setError: (err: string | null) => {
      error = err;
    },

    setSequenceData: (data: SequenceData | null) => {
      sequenceData = data;
    },

    reset: () => {
      currentBeat = 0;
      isPlaying = false;
      speed = 1.0;
      shouldLoop = false;
      totalBeats = 0;
      sequenceWord = "";
      sequenceAuthor = "";
      bluePropState = { ...DEFAULT_PROP_STATE };
      redPropState = { ...DEFAULT_PROP_STATE };
      loading = false;
      error = null;
      sequenceData = null;
    },
  };
}
