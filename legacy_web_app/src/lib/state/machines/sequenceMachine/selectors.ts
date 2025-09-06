/**
 * Selectors for the sequence state machine
 */
import type { BeatData as StoreBeatData } from '../../stores/sequenceStore';
import { sequenceStore } from '../../stores/sequenceStore';
import type { Actor } from 'xstate';

/**
 * Helper functions to get current state from the sequence machine
 */
export function createSequenceSelectors(sequenceActor: Actor<any>) {
  return {
    // Generation selectors
    isGenerating: () => {
      return sequenceActor.getSnapshot().matches('generating');
    },

    hasError: () => {
      return sequenceActor.getSnapshot().matches('error');
    },

    error: () => {
      return sequenceActor.getSnapshot().context.error;
    },

    progress: () => {
      return sequenceActor.getSnapshot().context.generationProgress;
    },

    message: () => {
      return sequenceActor.getSnapshot().context.generationMessage;
    },

    generationMessage: () => {
      return sequenceActor.getSnapshot().context.generationMessage;
    },

    generationType: () => {
      return sequenceActor.getSnapshot().context.generationType;
    },

    generationOptions: () => {
      return sequenceActor.getSnapshot().context.generationOptions;
    },

    // Beat selectors (using sequenceStore)
    selectedBeatIds: () => {
      let selectedIds: string[] = [];
      sequenceStore.subscribe((state) => {
        selectedIds = state.selectedBeatIds;
      })();
      return selectedIds;
    },

    selectedBeats: () => {
      let selected: StoreBeatData[] = [];
      sequenceStore.subscribe((state) => {
        selected = state.beats.filter((beat) => state.selectedBeatIds.includes(beat.id));
      })();
      return selected;
    },

    currentBeatIndex: () => {
      let index = 0;
      sequenceStore.subscribe((state) => {
        index = state.currentBeatIndex;
      })();
      return index;
    },

    beats: () => {
      let beats: StoreBeatData[] = [];
      sequenceStore.subscribe((state) => {
        beats = state.beats;
      })();
      return beats;
    },

    beatCount: () => {
      let count = 0;
      sequenceStore.subscribe((state) => {
        count = state.beats.length;
      })();
      return count;
    }
  };
}
