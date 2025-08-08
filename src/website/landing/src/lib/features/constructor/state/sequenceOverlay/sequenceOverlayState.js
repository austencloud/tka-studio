import { createStore } from "../../core/index.js";

// Sequence overlay state management
export const sequenceOverlayState = createStore({
  isOpen: false,
  currentSequence: null,
  isLoading: false,
  error: null,
});

// Export as sequenceOverlayStore for compatibility
export const sequenceOverlayStore = sequenceOverlayState;

// Actions
export function openSequenceOverlay(sequence = null) {
  sequenceOverlayState.update((state) => ({
    ...state,
    isOpen: true,
    currentSequence: sequence,
    error: null,
  }));
}

export function closeSequenceOverlay() {
  sequenceOverlayState.update((state) => ({
    ...state,
    isOpen: false,
    currentSequence: null,
    error: null,
  }));
}

export function setSequenceOverlayLoading(loading) {
  sequenceOverlayState.update((state) => ({
    ...state,
    isLoading: loading,
  }));
}

export function setSequenceOverlayError(error) {
  sequenceOverlayState.update((state) => ({
    ...state,
    error: error,
    isLoading: false,
  }));
}

export function updateSequenceOverlaySequence(sequence) {
  sequenceOverlayState.update((state) => ({
    ...state,
    currentSequence: sequence,
  }));
}
