/**
 * Sequence Beat Operations
 *
 * Handles beat-level operations with animation support:
 * - Adding/removing beats
 * - Updating beat data
 * - Beat insertion
 * - Animated beat removal
 *
 * RESPONSIBILITY: Beat operations coordinator, orchestrates state + services
 */

import type { BeatData, SequenceData } from "$shared";
import type { SequenceAnimationState } from "../animation/SequenceAnimationState.svelte";
import type { SequenceCoreState } from "../core/SequenceCoreState.svelte";
import type { SequenceSelectionState } from "../selection/SequenceSelectionState.svelte";

export interface BeatOperationsConfig {
  coreState: SequenceCoreState;
  selectionState: SequenceSelectionState;
  animationState: SequenceAnimationState;
  onError?: (error: string) => void;
  onSave?: () => Promise<void>;
}

export function createSequenceBeatOperations(config: BeatOperationsConfig) {
  const { coreState, selectionState, animationState, onError, onSave } = config;

  // Helper functions for in-memory sequence manipulation
  function addBeatToSequence(
    sequence: SequenceData,
    beatData?: Partial<BeatData>
  ): SequenceData {
    const newBeat: BeatData = {
      id: beatData?.id ?? crypto.randomUUID(),
      beatNumber: sequence.beats.length + 1,
      isBlank: beatData?.isBlank ?? true,
      duration: beatData?.duration ?? 1,
      blueReversal: beatData?.blueReversal ?? false,
      redReversal: beatData?.redReversal ?? false,
      letter: beatData?.letter ?? null,
      startPosition: beatData?.startPosition ?? null,
      endPosition: beatData?.endPosition ?? null,
      motions: beatData?.motions ?? {},
      ...beatData,
    };
    return { ...sequence, beats: [...sequence.beats, newBeat] };
  }

  function removeBeatFromSequence(
    sequence: SequenceData,
    beatIndex: number
  ): SequenceData {
    if (beatIndex < 0 || beatIndex >= sequence.beats.length) {
      return sequence;
    }
    const newBeats = sequence.beats.filter((_, index) => index !== beatIndex);
    return { ...sequence, beats: newBeats };
  }

  function removeBeatAndSubsequentFromSequence(
    sequence: SequenceData,
    beatIndex: number
  ): SequenceData {
    if (beatIndex < 0 || beatIndex >= sequence.beats.length) {
      return sequence;
    }
    const newBeats = sequence.beats.slice(0, beatIndex);
    return { ...sequence, beats: newBeats };
  }

  function updateBeatInSequence(
    sequence: SequenceData,
    beatIndex: number,
    beatData: Partial<BeatData>
  ): SequenceData {
    if (beatIndex < 0 || beatIndex >= sequence.beats.length) {
      return sequence;
    }
    const newBeats = [...sequence.beats];
    newBeats[beatIndex] = { ...newBeats[beatIndex]!, ...beatData };
    return { ...sequence, beats: newBeats };
  }

  function insertBeatInSequence(
    sequence: SequenceData,
    beatIndex: number,
    beatData: Partial<BeatData>
  ): SequenceData {
    const newBeat: BeatData = {
      id: beatData?.id ?? crypto.randomUUID(),
      beatNumber: beatIndex + 1,
      isBlank: beatData?.isBlank ?? true,
      duration: beatData?.duration ?? 1,
      blueReversal: beatData?.blueReversal ?? false,
      redReversal: beatData?.redReversal ?? false,
      letter: beatData?.letter ?? null,
      startPosition: beatData?.startPosition ?? null,
      endPosition: beatData?.endPosition ?? null,
      motions: beatData?.motions ?? {},
      ...beatData,
    };
    const newBeats = [
      ...sequence.beats.slice(0, beatIndex),
      newBeat,
      ...sequence.beats.slice(beatIndex),
    ];
    return { ...sequence, beats: newBeats };
  }

  function clearSequenceBeats(sequence: SequenceData): SequenceData {
    return { ...sequence, beats: [] };
  }

  function getSelectedBeat(
    sequence: SequenceData,
    index: number
  ): BeatData | null {
    if (index < 0 || index >= sequence.beats.length) {
      return null;
    }
    return sequence.beats[index] ?? null;
  }

  function handleError(message: string, error?: unknown) {
    const errorMsg = error instanceof Error ? error.message : message;
    coreState.setError(errorMsg);
    onError?.(errorMsg);
    console.error(message, error);
  }

  return {
    addBeat(beatData?: Partial<BeatData>) {
      if (!coreState.currentSequence) return;

      try {
        const updatedSequence = addBeatToSequence(
          coreState.currentSequence,
          beatData
        );
        coreState.setCurrentSequence(updatedSequence);
        coreState.clearError();
      } catch (error) {
        handleError("Failed to add beat", error);
      }
    },

    removeBeat(beatIndex: number) {
      if (!coreState.currentSequence) return;

      try {
        const updatedSequence = removeBeatFromSequence(
          coreState.currentSequence,
          beatIndex
        );
        coreState.setCurrentSequence(updatedSequence);
        selectionState.adjustSelectionForRemovedBeat(beatIndex);
        coreState.clearError();
        onSave?.().catch((err) =>
          console.error("Failed to auto-save after beat removal:", err)
        );
      } catch (error) {
        handleError("Failed to remove beat", error);
      }
    },

    removeBeatWithAnimation(beatIndex: number, onComplete?: () => void) {
      if (!coreState.currentSequence) return;

      animationState.startRemovingBeat(beatIndex);

      // Wait for fade animation (updated to match new faster animation: 250ms)
      setTimeout(() => {
        try {
          const updatedSequence = removeBeatFromSequence(
            coreState.currentSequence!,
            beatIndex
          );
          coreState.setCurrentSequence(updatedSequence);
          selectionState.adjustSelectionForRemovedBeat(beatIndex);
          coreState.clearError();
          onSave?.().catch((err) =>
            console.error("Failed to auto-save after beat removal:", err)
          );

          // Wait for slide animation (updated to match new faster animation: 200ms)
          setTimeout(() => {
            animationState.endRemovingBeat();
            onComplete?.();
          }, 200);
        } catch (error) {
          handleError("Failed to remove beat", error);
          animationState.endRemovingBeat();
        }
      }, 250);
    },

    removeBeatAndSubsequent(beatIndex: number) {
      if (!coreState.currentSequence) return;

      try {
        const updatedSequence = removeBeatAndSubsequentFromSequence(
          coreState.currentSequence,
          beatIndex
        );
        coreState.setCurrentSequence(updatedSequence);
        selectionState.clearSelection();
        coreState.clearError();
        onSave?.().catch((err) =>
          console.error("Failed to auto-save after beat removal:", err)
        );
      } catch (error) {
        handleError("Failed to remove beat and subsequent beats", error);
      }
    },

    removeBeatAndSubsequentWithAnimation(
      beatIndex: number,
      onComplete?: () => void
    ) {
      if (!coreState.currentSequence) return;

      const beatsToRemove = coreState.currentSequence.beats.length - beatIndex;
      const removingIndices: number[] = [];
      for (let i = beatIndex; i < coreState.currentSequence.beats.length; i++) {
        removingIndices.push(i);
      }

      console.log(
        `🎬 Starting REVERSE staggered fade-out for ${beatsToRemove} beats starting from index ${beatIndex}`
      );

      const staggerDelay = 200;
      const fadeAnimationDuration = 250; // Updated to match new faster animation
      const reversedIndices = [...removingIndices].reverse();

      // Start animations
      animationState.startRemovingBeats([]);
      reversedIndices.forEach((index, arrayIndex) => {
        setTimeout(() => {
          animationState.addRemovingBeat(index);
          console.log(
            `🎭 Fading out beat ${index} (${arrayIndex + 1}/${beatsToRemove}) - REVERSE ORDER`
          );
        }, arrayIndex * staggerDelay);
      });

      // Remove beats after animations
      const totalAnimationTime =
        (beatsToRemove - 1) * staggerDelay + fadeAnimationDuration;
      setTimeout(() => {
        try {
          const updatedSequence = removeBeatAndSubsequentFromSequence(
            coreState.currentSequence!,
            beatIndex
          );
          coreState.setCurrentSequence(updatedSequence);
          selectionState.clearSelection();
          coreState.clearError();
          onSave?.().catch((err) =>
            console.error("Failed to auto-save after beat removal:", err)
          );

          setTimeout(() => {
            animationState.endRemovingBeats();
            console.log(
              `✅ Reverse staggered removal complete for ${beatsToRemove} beats`
            );
            onComplete?.();
          }, 200); // Updated to match new faster animation
        } catch (error) {
          handleError("Failed to remove beat and subsequent beats", error);
          animationState.endRemovingBeats();
        }
      }, totalAnimationTime);
    },

    updateBeat(beatIndex: number, beatData: Partial<BeatData>) {
      if (!coreState.currentSequence) return;

      try {
        const updatedSequence = updateBeatInSequence(
          coreState.currentSequence,
          beatIndex,
          beatData
        );
        coreState.setCurrentSequence(updatedSequence);
        coreState.clearError();
      } catch (error) {
        handleError("Failed to update beat", error);
      }
    },

    insertBeat(beatIndex: number, beatData?: Partial<BeatData>) {
      if (!coreState.currentSequence) return;

      try {
        const updatedSequence = insertBeatInSequence(
          coreState.currentSequence,
          beatIndex,
          beatData ?? {}
        );
        coreState.setCurrentSequence(updatedSequence);
        selectionState.adjustSelectionForInsertedBeat(beatIndex);
        coreState.clearError();
      } catch (error) {
        handleError("Failed to insert beat", error);
      }
    },

    clearSequence() {
      if (!coreState.currentSequence) return;

      try {
        const updatedSequence = clearSequenceBeats(coreState.currentSequence);
        coreState.setCurrentSequence(updatedSequence);
        selectionState.clearSelection();
        coreState.clearError();
      } catch (error) {
        handleError("Failed to clear sequence", error);
      }
    },

    getBeat(index: number): BeatData | null {
      if (!coreState.currentSequence) return null;
      return getSelectedBeat(coreState.currentSequence, index);
    },

    getBeatCount(): number {
      return coreState.currentSequence?.beats.length ?? 0;
    },

    hasContent(): boolean {
      return coreState.currentSequence?.beats.some((b) => !b.isBlank) ?? false;
    },
  };
}

export type SequenceBeatOperations = ReturnType<
  typeof createSequenceBeatOperations
>;
