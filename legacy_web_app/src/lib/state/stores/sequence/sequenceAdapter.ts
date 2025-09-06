/**
 * Sequence Store Adapter
 *
 * This module provides an adapter between the modern sequence container
 * and the legacy store-based API. This allows for a gradual migration
 * to the new container-based approach.
 */

import { writable, derived, type Writable, type Readable } from 'svelte/store';
import {
	sequenceContainer,
	selectedBeats,
	currentBeat,
	beatCount,
	sequenceDifficulty
} from './SequenceContainer';
import type { SequenceState, BeatData } from './SequenceContainer';

/**
 * Create a store adapter for the sequence container
 */
function createSequenceStoreAdapter(): Writable<SequenceState> & {
	addBeat: (beat: BeatData) => void;
	addBeats: (beats: BeatData[]) => void;
	setSequence: (beats: BeatData[]) => void;
	removeBeat: (beatId: string) => void;
	updateBeat: (beatId: string, updates: Partial<BeatData>) => void;
	selectBeat: (beatId: string, multiSelect?: boolean) => void;
	deselectBeat: (beatId: string) => void;
	clearSelection: () => void;
	setCurrentBeatIndex: (index: number) => void;
	updateMetadata: (metadata: Partial<SequenceState['metadata']>) => void;
	markAsSaved: () => void;
} {
	// Create a writable store that reflects the container's state
	const { subscribe, set } = writable<SequenceState>(sequenceContainer.state);

	// Set up a subscription to update the store when the container changes
	// Try to use the subscribe method if available, otherwise fall back to polling
	let cleanup: (() => void) | null = null;

	// Check if the container has a subscribe method
	if (
		'subscribe' in sequenceContainer &&
		typeof (sequenceContainer as any).subscribe === 'function'
	) {
		// Use the subscribe method
		const unsubscribe = (sequenceContainer as any).subscribe((state: SequenceState) => {
			set(state);
		});

		cleanup = () => {
			if (typeof unsubscribe === 'function') {
				unsubscribe();
			}
		};
	} else {
		// Fall back to polling with a short interval
		// This approach works reliably for adding beats to the sequence
		const intervalId = setInterval(() => {
			set(sequenceContainer.state);
		}, 16); // Poll at approximately 60fps for smoother updates

		cleanup = () => {
			clearInterval(intervalId);
		};
	}

	// Clean up when the store is no longer used
	if (typeof window !== 'undefined') {
		window.addEventListener('beforeunload', () => {
			if (cleanup) cleanup();
		});
	}

	// Return a store with the same API as the original sequence store
	return {
		subscribe,
		set: (value: SequenceState) => {
			// Update the container when the store is set
			sequenceContainer.setSequence(value.beats);
			sequenceContainer.updateMetadata(value.metadata);
			if (value.selectedBeatIds.length > 0) {
				// Clear existing selection first
				sequenceContainer.clearSelection();
				// Then add each selected beat
				value.selectedBeatIds.forEach((id) => sequenceContainer.selectBeat(id, true));
			}
			sequenceContainer.setCurrentBeatIndex(value.currentBeatIndex);
			if (!value.isModified) {
				sequenceContainer.markAsSaved();
			}
			set(value);
		},
		update: (updater: (value: SequenceState) => SequenceState) => {
			const newValue = updater(sequenceContainer.state);
			// Update the container with the new value
			sequenceContainer.setSequence(newValue.beats);
			sequenceContainer.updateMetadata(newValue.metadata);
			if (newValue.selectedBeatIds.length > 0) {
				// Clear existing selection first
				sequenceContainer.clearSelection();
				// Then add each selected beat
				newValue.selectedBeatIds.forEach((id) => sequenceContainer.selectBeat(id, true));
			}
			sequenceContainer.setCurrentBeatIndex(newValue.currentBeatIndex);
			if (!newValue.isModified) {
				sequenceContainer.markAsSaved();
			}
			set(newValue);
		},
		// Forward action methods to the container
		addBeat: sequenceContainer.addBeat,
		addBeats: sequenceContainer.addBeats,
		setSequence: sequenceContainer.setSequence,
		removeBeat: sequenceContainer.removeBeat,
		updateBeat: sequenceContainer.updateBeat,
		selectBeat: sequenceContainer.selectBeat,
		deselectBeat: sequenceContainer.deselectBeat,
		clearSelection: sequenceContainer.clearSelection,
		setCurrentBeatIndex: sequenceContainer.setCurrentBeatIndex,
		updateMetadata: sequenceContainer.updateMetadata,
		markAsSaved: sequenceContainer.markAsSaved
	};
}

// Create the adapter
export const sequenceStore = createSequenceStoreAdapter();

// Create derived stores for backward compatibility
export const selectedBeatsStore: Readable<BeatData[]> = derived(sequenceStore, ($store) =>
	$store.beats.filter((beat) => $store.selectedBeatIds.includes(beat.id))
);

export const currentBeatStore: Readable<BeatData | null> = derived(
	sequenceStore,
	($store) => $store.beats[$store.currentBeatIndex] || null
);

export const beatCountStore: Readable<number> = derived(
	sequenceStore,
	($store) => $store.beats.length
);

export const sequenceDifficultyStore: Readable<number> = derived(
	sequenceStore,
	($store) => $store.metadata.difficulty
);

// Export the derived values from the container for modern usage
export { selectedBeats, currentBeat, beatCount, sequenceDifficulty };
