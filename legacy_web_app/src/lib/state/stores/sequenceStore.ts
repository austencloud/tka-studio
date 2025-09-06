/**
 * Sequence Store
 *
 * This is the main entry point for the sequence state. It re-exports the
 * sequence store from the adapter, which provides backward compatibility
 * with the legacy store API while using the modern container implementation.
 *
 * MIGRATION NOTE: This file maintains the same API as the original sequence store
 * but uses the new container-based implementation under the hood. Components
 * should gradually migrate to using the container directly.
 */

// Re-export types from the modern implementation
export type { BeatData, SequenceState } from './sequence/SequenceContainer';

// Re-export the store and derived stores from the adapter
export {
	sequenceStore,
	selectedBeatsStore as selectedBeats,
	currentBeatStore as currentBeat,
	beatCountStore as beatCount,
	sequenceDifficultyStore as sequenceDifficulty
} from './sequence/sequenceAdapter';

// Export the container for modern usage
export { sequenceContainer } from './sequence/SequenceContainer';

// Note: The sequence machine is already connected to the store
// through the updateSequence action in the sequenceMachine.ts file.
// No additional subscription is needed here.
