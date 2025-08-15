/**
 * Sequence State Factory - Component-Scoped State for Svelte 5 Runes
 *
 * Creates component-scoped sequence state instead of global singletons.
 * Each component gets its own isolated state through factory function.
 */

import type { BeatData, SequenceData } from "$lib/domain";
import { GridMode } from "$lib/domain/enums";
import type { ArrowPosition, ISequenceService } from "$services/interfaces";

// ============================================================================
// FACTORY FUNCTION
// ============================================================================

export function createSequenceState(sequenceService: ISequenceService) {
  // ============================================================================
  // COMPONENT-SCOPED STATE
  // ============================================================================

  const state = $state({
    // Sequence state
    currentSequence: null as SequenceData | null,
    sequences: [] as SequenceData[],
    isLoading: false,
    error: null as string | null,

    // Selection state
    selectedBeatIndex: null as number | null,
    selectedSequenceId: null as string | null,

    // UI state
    showBeatNumbers: true,
    gridMode: GridMode.DIAMOND as GridMode,

    // Arrow positioning state
    arrowPositions: new Map<string, ArrowPosition>(),
    arrowPositioningInProgress: false,
    arrowPositioningError: null as string | null,
  });

  // ============================================================================
  // GETTERS
  // ============================================================================

  function getCurrentSequence() {
    return state.currentSequence;
  }
  function getSequences() {
    return state.sequences;
  }
  function getIsLoading() {
    return state.isLoading;
  }
  function getError() {
    return state.error;
  }
  function getSelectedBeatIndex() {
    return state.selectedBeatIndex;
  }
  function getSelectedSequenceId() {
    return state.selectedSequenceId;
  }
  function getShowBeatNumbers() {
    return state.showBeatNumbers;
  }
  function getGridMode() {
    return state.gridMode;
  }
  function getArrowPositions() {
    return state.arrowPositions;
  }
  function getArrowPositioningInProgress() {
    return state.arrowPositioningInProgress;
  }
  function getArrowPositioningError() {
    return state.arrowPositioningError;
  }

  // ============================================================================
  // COMPUTED GETTERS
  // ============================================================================

  function getCurrentBeats(): BeatData[] {
    // Return a mutable copy to allow UI modifications without violating readonly domain model
    return state.currentSequence ? [...state.currentSequence.beats] : [];
  }

  function getSelectedBeatData(): BeatData | null {
    if (state.selectedBeatIndex === null || !state.currentSequence) {
      return null;
    }
    return state.currentSequence.beats[state.selectedBeatIndex] ?? null;
  }

  function getSelectedBeat(): BeatData | null {
    const beatIndex = state.selectedBeatIndex;
    const sequence = state.currentSequence;
    return beatIndex !== null && sequence
      ? (sequence.beats[beatIndex] ?? null)
      : null;
  }

  function getHasCurrentSequence(): boolean {
    return state.currentSequence !== null;
  }

  function getSequenceCount(): number {
    return state.sequences.length;
  }

  function getHasUnsavedChanges(): boolean {
    // TODO: Implement change tracking
    return false;
  }

  function getHasArrowPositions(): boolean {
    return state.arrowPositions.size > 0;
  }

  function getArrowPositioningComplete(): boolean {
    return !state.arrowPositioningInProgress && state.arrowPositions.size > 0;
  }

  // ============================================================================
  // ACTIONS
  // ============================================================================

  /**
   * Set the current sequence
   */
  function setCurrentSequence(sequence: SequenceData | null): void {
    state.currentSequence = sequence;
    state.selectedSequenceId = sequence?.id ?? null;
    state.selectedBeatIndex = null; // Reset beat selection
  }

  /**
   * Add sequence to the list
   */
  function addSequence(sequence: SequenceData): void {
    state.sequences.push(sequence);
    setCurrentSequence(sequence);
  }

  /**
   * Update sequence in the list
   */
  function updateSequence(updatedSequence: SequenceData): void {
    const index = state.sequences.findIndex((s) => s.id === updatedSequence.id);
    if (index >= 0) {
      state.sequences[index] = updatedSequence;
    }

    // Update current sequence if it's the same one
    if (state.currentSequence?.id === updatedSequence.id) {
      state.currentSequence = updatedSequence;
    }
  }

  /**
   * Remove sequence from the list
   */
  function removeSequence(sequenceId: string): void {
    state.sequences = state.sequences.filter((s) => s.id !== sequenceId);

    // Clear current sequence if it was deleted
    if (state.currentSequence?.id === sequenceId) {
      setCurrentSequence(null);
    }
  }

  /**
   * Set sequences list
   */
  function setSequences(newSequences: SequenceData[]): void {
    state.sequences = newSequences;
  }

  /**
   * Set loading state
   */
  function setLoading(loading: boolean): void {
    state.isLoading = loading;
  }

  /**
   * Set error state
   */
  function setError(error: string | null): void {
    state.error = error;
  }

  /**
   * Clear error state
   */
  function clearError(): void {
    state.error = null;
  }

  /**
   * Update current beat in sequence
   */
  function updateCurrentBeat(beatIndex: number, beatData: BeatData): void {
    if (
      state.currentSequence &&
      beatIndex >= 0 &&
      beatIndex < state.currentSequence.beats.length
    ) {
      // Create a new beats array (respecting immutability of domain model) and assign
      const newBeats = [...state.currentSequence.beats];
      newBeats[beatIndex] = beatData;
      state.currentSequence = {
        ...state.currentSequence,
        beats: newBeats,
      } as SequenceData;
    }
  }

  /**
   * Select a beat
   */
  function selectBeat(beatIndex: number | null): void {
    state.selectedBeatIndex = beatIndex;
  }

  /**
   * Set grid mode
   */
  function setGridMode(mode: GridMode): void {
    state.gridMode = mode;
  }

  /**
   * Set show beat numbers
   */
  function setShowBeatNumbers(show: boolean): void {
    state.showBeatNumbers = show;
  }

  /**
   * Set arrow positions
   */
  function setArrowPositions(positions: Map<string, ArrowPosition>): void {
    state.arrowPositions = positions;
  }

  /**
   * Set arrow positioning in progress
   */
  function setArrowPositioningInProgress(inProgress: boolean): void {
    state.arrowPositioningInProgress = inProgress;
  }

  /**
   * Set arrow positioning error
   */
  function setArrowPositioningError(error: string | null): void {
    state.arrowPositioningError = error;
  }

  /**
   * Get arrow position for color
   */
  function getArrowPosition(color: string): ArrowPosition | null {
    return state.arrowPositions.get(color) || null;
  }

  /**
   * Clear all arrow positions
   */
  function clearArrowPositions(): void {
    state.arrowPositions.clear();
  }

  /**
   * Reset all state
   */
  function resetSequenceState(): void {
    state.currentSequence = null;
    state.sequences = [];
    state.isLoading = false;
    state.error = null;
    state.selectedBeatIndex = null;
    state.selectedSequenceId = null;
    state.gridMode = GridMode.DIAMOND;
    state.arrowPositions.clear();
    state.arrowPositioningInProgress = false;
    state.arrowPositioningError = null;
  }

  // ============================================================================
  // SERVICE INTEGRATION ACTIONS
  // ============================================================================

  /**
   * Load sequences using the injected service
   */
  async function loadSequences(): Promise<void> {
    setLoading(true);
    setError(null);
    try {
      const sequences = await sequenceService.getAllSequences();
      setSequences(sequences);
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Unknown error loading sequences";
      setError(errorMessage);
      console.error("Failed to load sequences:", error);
    } finally {
      setLoading(false);
    }
  }

  /**
   * Create sequence using the injected service
   */
  async function createSequence(request: {
    name: string;
    length: number;
  }): Promise<SequenceData | null> {
    setLoading(true);
    setError(null);
    try {
      const sequence = await sequenceService.createSequence(request);
      addSequence(sequence);
      return sequence;
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Unknown error creating sequence";
      setError(errorMessage);
      console.error("Failed to create sequence:", error);
      return null;
    } finally {
      setLoading(false);
    }
  }

  /**
   * Update sequence using the injected service
   */
  async function updateSequenceBeats(
    sequenceId: string,
    beatIndex: number,
    beatData: BeatData
  ): Promise<void> {
    try {
      await sequenceService.updateBeat(sequenceId, beatIndex, beatData);
      updateCurrentBeat(beatIndex, beatData);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error updating beat";
      setError(errorMessage);
      console.error("Failed to update beat:", error);
    }
  }

  // ============================================================================
  // RETURN STATE OBJECT
  // ============================================================================

  return {
    // State access (reactive)
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
    get selectedBeatIndex() {
      return state.selectedBeatIndex;
    },
    get selectedSequenceId() {
      return state.selectedSequenceId;
    },
    get showBeatNumbers() {
      return state.showBeatNumbers;
    },
    get gridMode() {
      return state.gridMode;
    },
    get arrowPositions() {
      return state.arrowPositions;
    },
    get arrowPositioningInProgress() {
      return state.arrowPositioningInProgress;
    },
    get arrowPositioningError() {
      return state.arrowPositioningError;
    },

    // Getters
    getCurrentSequence,
    getSequences,
    getIsLoading,
    getError,
    getSelectedBeatIndex,
    getSelectedSequenceId,
    getShowBeatNumbers,
    getGridMode,
    getArrowPositions,
    getArrowPositioningInProgress,
    getArrowPositioningError,

    // Computed getters
    getCurrentBeats,
    getSelectedBeatData,
    getSelectedBeat,
    getHasCurrentSequence,
    getSequenceCount,
    getHasUnsavedChanges,
    getHasArrowPositions,
    getArrowPositioningComplete,

    // Actions
    setCurrentSequence,
    addSequence,
    updateSequence,
    removeSequence,
    setSequences,
    setLoading,
    setError,
    clearError,
    updateCurrentBeat,
    selectBeat,
    setGridMode,
    setShowBeatNumbers,
    setArrowPositions,
    setArrowPositioningInProgress,
    setArrowPositioningError,
    getArrowPosition,
    clearArrowPositions,
    resetSequenceState,

    // Service integration
    loadSequences,
    createSequence,
    updateSequenceBeats,
  };
}

// ============================================================================
// DIRECT EXPORTS FOR BACKWARD COMPATIBILITY
// ============================================================================

// Create a default instance for direct function exports
// This maintains compatibility with files that import functions directly
import { resolve } from "$services/bootstrap";
import { browser } from "$app/environment";

// Lazy initialization - only create when first accessed
let defaultSequenceState: ReturnType<typeof createSequenceState> | null = null;

function getDefaultSequenceState() {
  if (!browser) return null;

  if (!defaultSequenceState) {
    defaultSequenceState = createSequenceState(resolve("ISequenceService"));
  }

  return defaultSequenceState;
}

// Export individual functions for backward compatibility
// Provide fallback functions for SSR environment
const noOp = () => {};
const noOpReturn = () => null;

export const getSequences = () => getDefaultSequenceState()?.sequences || [];
export const addSequence = (...args: any[]) => {
  const state = getDefaultSequenceState();
  return state?.addSequence ? (state.addSequence as any)(...args) : undefined;
};
export const clearError = () => {
  const state = getDefaultSequenceState();
  return state?.clearError ? state.clearError() : undefined;
};
export const removeSequence = (...args: any[]) => {
  const state = getDefaultSequenceState();
  return state?.removeSequence
    ? (state.removeSequence as any)(...args)
    : undefined;
};
export const setCurrentSequence = (...args: any[]) => {
  const state = getDefaultSequenceState();
  return state?.setCurrentSequence
    ? (state.setCurrentSequence as any)(...args)
    : undefined;
};
export const setError = (...args: any[]) => {
  const state = getDefaultSequenceState();
  return state?.setError ? (state.setError as any)(...args) : undefined;
};
export const setLoading = (...args: any[]) => {
  const state = getDefaultSequenceState();
  return state?.setLoading ? (state.setLoading as any)(...args) : undefined;
};
export const setSequences = (...args: any[]) => {
  const state = getDefaultSequenceState();
  return state?.setSequences ? (state.setSequences as any)(...args) : undefined;
};
export const updateCurrentBeat = (...args: any[]) => {
  const state = getDefaultSequenceState();
  return state?.updateCurrentBeat
    ? (state.updateCurrentBeat as any)(...args)
    : undefined;
};
export const updateSequence = (...args: any[]) => {
  const state = getDefaultSequenceState();
  return state?.updateSequence
    ? (state.updateSequence as any)(...args)
    : undefined;
};
export const clearArrowPositions = () => {
  const state = getDefaultSequenceState();
  return state?.clearArrowPositions ? state.clearArrowPositions() : undefined;
};
export const setArrowPositioningError = (...args: any[]) => {
  const state = getDefaultSequenceState();
  return state?.setArrowPositioningError
    ? (state.setArrowPositioningError as any)(...args)
    : undefined;
};
export const setArrowPositioningInProgress = (...args: any[]) => {
  const state = getDefaultSequenceState();
  return state?.setArrowPositioningInProgress
    ? (state.setArrowPositioningInProgress as any)(...args)
    : undefined;
};
export const setArrowPositions = (...args: any[]) => {
  const state = getDefaultSequenceState();
  return state?.setArrowPositions
    ? (state.setArrowPositions as any)(...args)
    : undefined;
};
