/**
 * Helper functions for the sequence state machine
 */
import type { SequenceGenerationOptions, FreeformSequenceOptions } from './types.js';
import type { Actor } from 'xstate';
import type { SequenceMachineEvent } from './types.js';

/**
 * Helper functions to interact with the sequence machine
 */
export function createSequenceActions(sequenceActor: Actor<any>) {
  return {
    // Generation actions
    generate: (options: any, type: 'circular' | 'freeform' = 'circular') => {
      // Validate and convert options to the correct type
      let validOptions: SequenceGenerationOptions | FreeformSequenceOptions;

      if (type === 'circular') {
        validOptions = {
          capType: options.capType || 'mirrored',
          numBeats: options.numBeats || 8,
          turnIntensity: options.turnIntensity || 3,
          propContinuity: options.propContinuity || 'continuous'
        };
      } else {
        validOptions = {
          numBeats: options.numBeats || 8,
          turnIntensity: options.turnIntensity || 3,
          propContinuity: options.propContinuity || 'continuous',
          letterTypes: options.letterTypes || []
        };
      }

      sequenceActor.send({
        type: 'GENERATE',
        options: validOptions,
        generationType: type
      } as SequenceMachineEvent);
    },

    cancel: () => {
      sequenceActor.send({ type: 'CANCEL' } as SequenceMachineEvent);
    },

    retry: () => {
      sequenceActor.send({ type: 'RETRY' } as SequenceMachineEvent);
    },

    reset: () => {
      sequenceActor.send({ type: 'RESET' } as SequenceMachineEvent);
    },

    // Beat manipulation actions
    selectBeat: (beatId: string) => {
      sequenceActor.send({ type: 'SELECT_BEAT', beatId } as SequenceMachineEvent);
    },

    deselectBeat: (beatId?: string) => {
      sequenceActor.send({ type: 'DESELECT_BEAT', beatId } as SequenceMachineEvent);
    },

    addBeat: (beat: any) => {
      sequenceActor.send({ type: 'ADD_BEAT', beat } as SequenceMachineEvent);
    },

    removeBeat: (beatId: string) => {
      sequenceActor.send({ type: 'REMOVE_BEAT', beatId } as SequenceMachineEvent);
    },

    removeBeatAndFollowing: (beatId: string) => {
      sequenceActor.send({ type: 'REMOVE_BEAT_AND_FOLLOWING', beatId } as SequenceMachineEvent);
    },

    updateBeat: (beatId: string, updates: any) => {
      sequenceActor.send({ type: 'UPDATE_BEAT', beatId, updates } as SequenceMachineEvent);
    },

    clearSequence: () => {
      sequenceActor.send({ type: 'CLEAR_SEQUENCE' } as SequenceMachineEvent);
    }
  };
}
