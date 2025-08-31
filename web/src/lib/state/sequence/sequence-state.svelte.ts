/**
 * Sequence State Factory
 *
 * Reactive state wrapper around the pure SequenceStateService.
 * Follows the established TKA state factory pattern.
 */

import type { BeatData, SequenceData, ValidationResult } from "$domain";
import type { ISequenceStateService } from "$lib/services/contracts/sequence/ISequenceStateService";
/**
 * Creates component-scoped sequence state
 *
 * @param sequenceStateService - Injected via DI container
 * @returns Reactive state object with getters and actions
 */
export function createSequenceState(
  sequenceStateService: ISequenceStateService
) {
  // ============================================================================
  // REACTIVE STATE (Component-scoped)
  // ============================================================================

  let currentSequence = $state<SequenceData | null>(null);
  let selectedBeatIndex = $state<number>(-1);
  let isLoading = $state<boolean>(false);
  let error = $state<string | null>(null);

  // ============================================================================
  // DERIVED STATE (Reactive computations)
  // ============================================================================

  const selectedBeat = $derived(() => {
    if (!currentSequence || selectedBeatIndex < 0) {
      return null;
    }
    return sequenceStateService.getSelectedBeat(
      currentSequence,
      selectedBeatIndex
    );
  });

  const hasSequence = $derived(() => currentSequence !== null);
  const beatCount = $derived(() => currentSequence?.beats.length ?? 0);

  const sequenceStatistics = $derived(() => {
    if (!currentSequence) {
      return null;
    }
    return sequenceStateService.getSequenceStatistics(currentSequence);
  });

  const sequenceWord = $derived(() => {
    if (!currentSequence) {
      return "";
    }
    return sequenceStateService.generateSequenceWord(currentSequence);
  });

  const sequenceDuration = $derived(() => {
    if (!currentSequence) {
      return 0;
    }
    return sequenceStateService.calculateSequenceDuration(currentSequence);
  });

  // ============================================================================
  // GETTERS (Reactive access to state)
  // ============================================================================

  return {
    // Core state getters
    get currentSequence() {
      return currentSequence;
    },

    get selectedBeatIndex() {
      return selectedBeatIndex;
    },

    get isLoading() {
      return isLoading;
    },

    get error() {
      return error;
    },

    // Derived state getters
    get selectedBeat() {
      return selectedBeat;
    },

    get hasSequence() {
      return hasSequence;
    },

    get beatCount() {
      return beatCount;
    },

    get sequenceStatistics() {
      return sequenceStatistics;
    },

    get sequenceWord() {
      return sequenceWord;
    },

    get sequenceDuration() {
      return sequenceDuration;
    },

    // ============================================================================
    // ACTIONS (State mutations and service calls)
    // ============================================================================

    // Sequence management actions
    setCurrentSequence(sequence: SequenceData | null) {
      currentSequence = sequence;
      selectedBeatIndex = -1; // Reset selection
      error = null;
    },

    createNewSequence(name: string, length?: number) {
      try {
        isLoading = true;
        error = null;

        const newSequence = sequenceStateService.createNewSequence(
          name,
          length
        );
        currentSequence = newSequence;
        selectedBeatIndex = -1;
      } catch (err) {
        error =
          err instanceof Error ? err.message : "Failed to create sequence";
      } finally {
        isLoading = false;
      }
    },

    // Beat selection actions
    selectBeat(index: number) {
      if (sequenceStateService.isValidBeatIndex(currentSequence, index)) {
        selectedBeatIndex = index;
      } else {
        selectedBeatIndex = -1;
      }
    },

    clearSelection() {
      selectedBeatIndex = -1;
    },

    // Beat operation actions
    addBeat(beatData?: Partial<BeatData>) {
      if (!currentSequence) return;

      try {
        currentSequence = sequenceStateService.addBeat(
          currentSequence,
          beatData
        );
        error = null;
      } catch (err) {
        error = err instanceof Error ? err.message : "Failed to add beat";
      }
    },

    removeBeat(beatIndex: number) {
      if (!currentSequence) return;

      try {
        currentSequence = sequenceStateService.removeBeat(
          currentSequence,
          beatIndex
        );

        // Adjust selection if necessary
        if (selectedBeatIndex === beatIndex) {
          selectedBeatIndex = -1;
        } else if (selectedBeatIndex > beatIndex) {
          selectedBeatIndex = selectedBeatIndex - 1;
        }

        error = null;
      } catch (err) {
        error = err instanceof Error ? err.message : "Failed to remove beat";
      }
    },

    updateBeat(beatIndex: number, beatData: Partial<BeatData>) {
      if (!currentSequence) return;

      try {
        currentSequence = sequenceStateService.updateBeat(
          currentSequence,
          beatIndex,
          beatData
        );
        error = null;
      } catch (err) {
        error = err instanceof Error ? err.message : "Failed to update beat";
      }
    },

    insertBeat(beatIndex: number, beatData?: Partial<BeatData>) {
      if (!currentSequence) return;

      try {
        currentSequence = sequenceStateService.insertBeat(
          currentSequence,
          beatIndex,
          beatData
        );

        // Adjust selection if necessary
        if (selectedBeatIndex >= beatIndex) {
          selectedBeatIndex = selectedBeatIndex + 1;
        }

        error = null;
      } catch (err) {
        error = err instanceof Error ? err.message : "Failed to insert beat";
      }
    },

    // Sequence transformation actions
    clearSequence() {
      if (!currentSequence) return;

      try {
        currentSequence = sequenceStateService.clearSequence(currentSequence);
        selectedBeatIndex = -1;
        error = null;
      } catch (err) {
        error = err instanceof Error ? err.message : "Failed to clear sequence";
      }
    },

    duplicateSequence(newName?: string) {
      if (!currentSequence) return null;

      try {
        const duplicated = sequenceStateService.duplicateSequence(
          currentSequence,
          newName
        );
        error = null;
        return duplicated;
      } catch (err) {
        error =
          err instanceof Error ? err.message : "Failed to duplicate sequence";
        return null;
      }
    },

    setStartPosition(startPosition: BeatData) {
      if (!currentSequence) return;

      try {
        currentSequence = sequenceStateService.setStartPosition(
          currentSequence,
          startPosition
        );
        error = null;
      } catch (err) {
        error =
          err instanceof Error ? err.message : "Failed to set start position";
      }
    },

    // Sequence operations
    mirrorSequence() {
      if (!currentSequence) return;

      try {
        currentSequence = sequenceStateService.mirrorSequence(currentSequence);
        error = null;
      } catch (err) {
        error =
          err instanceof Error ? err.message : "Failed to mirror sequence";
      }
    },

    swapColors() {
      if (!currentSequence) return;

      try {
        currentSequence = sequenceStateService.swapColors(currentSequence);
        error = null;
      } catch (err) {
        error = err instanceof Error ? err.message : "Failed to swap colors";
      }
    },

    rotateSequence(direction: "clockwise" | "counterclockwise") {
      if (!currentSequence) return;

      try {
        currentSequence = sequenceStateService.rotateSequence(
          currentSequence,
          direction
        );
        error = null;
      } catch (err) {
        error =
          err instanceof Error ? err.message : "Failed to rotate sequence";
      }
    },

    // Validation
    validateCurrentSequence(): ValidationResult | null {
      if (!currentSequence) return null;

      return sequenceStateService.validateSequence(currentSequence);
    },

    // ============================================================================
    // CONVENIENCE METHODS
    // ============================================================================

    // Check if beat index is selected
    isBeatSelected(index: number): boolean {
      return selectedBeatIndex === index;
    },

    // Get beat by index safely
    getBeat(index: number): BeatData | null {
      return sequenceStateService.getSelectedBeat(currentSequence, index);
    },

    // Check if sequence has any content
    hasContent(): boolean {
      return currentSequence?.beats.some((beat) => !beat.isBlank) ?? false;
    },
  };
}

/**
 * Type definition for the sequence state
 */
export type SequenceState = ReturnType<typeof createSequenceState>;
