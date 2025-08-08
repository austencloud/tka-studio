/**
 * Sequence Store Adapter
 *
 * This module provides an adapter between the modern sequence container
 * and the legacy store-based API. This allows for a gradual migration
 * to the new container-based approach.
 */

import { writable, derived, type Writable, type Readable } from 'svelte/store';
import {
	sequenceContainer
} from './SequenceContainer.js';

// Define types based on the container structure
export interface BeatData {
	id: string;
	number: number;
	[key: string]: any; // Allow additional properties for flexibility
}

export interface SequenceState {
	beats: BeatData[];
	startPosition: any;
	metadata: {
		name: string;
		difficulty: number;
		[key: string]: any;
	};
	selectedBeatIds: string[];
	currentBeatIndex: number;
	isModified: boolean;
}

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
	const { subscribe, set } = writable<SequenceState>({
		...sequenceContainer.state,
		currentBeatIndex: 0,
		isModified: false
	});

	// Set up a subscription to update the store when the container changes
	// Try to use the subscribe method if available, otherwise fall back to polling
	let cleanup: (() => void) | null = null;

	// Check if the container has a subscribe method
	if (
		'subscribe' in sequenceContainer &&
		typeof (sequenceContainer as any).subscribe === 'function'
	) {
		// Use the subscribe method
		const unsubscribe = (sequenceContainer as any).subscribe((state: any) => {
			set({
				...state,
				currentBeatIndex: 0,
				isModified: false
			});
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
			set({
				...sequenceContainer.state,
				currentBeatIndex: 0,
				isModified: false
			});
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
			// Update the container when the store is set (with safety checks)
			if (sequenceContainer.setSequence) sequenceContainer.setSequence(value.beats);
			if (sequenceContainer.updateMetadata) sequenceContainer.updateMetadata(value.metadata);
			if (value.selectedBeatIds.length > 0) {
				// Clear existing selection first
				if (sequenceContainer.clearSelection) sequenceContainer.clearSelection();
				// Then add each selected beat
				value.selectedBeatIds.forEach((id) => {
					if (sequenceContainer.selectBeat) sequenceContainer.selectBeat(id, true);
				});
			}
			if (sequenceContainer.setCurrentBeatIndex) sequenceContainer.setCurrentBeatIndex(value.currentBeatIndex);
			if (!value.isModified && sequenceContainer.markAsSaved) {
				sequenceContainer.markAsSaved();
			}
			set(value);
		},
		update: (updater: (value: SequenceState) => SequenceState) => {
			const currentState = {
				...sequenceContainer.state,
				currentBeatIndex: 0,
				isModified: false
			};
			const newValue = updater(currentState);
			// Update the container with the new value (with safety checks)
			if (sequenceContainer.setSequence) sequenceContainer.setSequence(newValue.beats);
			if (sequenceContainer.updateMetadata) sequenceContainer.updateMetadata(newValue.metadata);
			if (newValue.selectedBeatIds.length > 0) {
				// Clear existing selection first
				if (sequenceContainer.clearSelection) sequenceContainer.clearSelection();
				// Then add each selected beat
				newValue.selectedBeatIds.forEach((id) => {
					if (sequenceContainer.selectBeat) sequenceContainer.selectBeat(id, true);
				});
			}
			if (sequenceContainer.setCurrentBeatIndex) sequenceContainer.setCurrentBeatIndex(newValue.currentBeatIndex);
			if (!newValue.isModified && sequenceContainer.markAsSaved) {
				sequenceContainer.markAsSaved();
			}
			set(newValue);
		},
		// Forward action methods to the container (with fallbacks for missing methods)
		addBeat: sequenceContainer.addBeat || (() => {}),
		addBeats: sequenceContainer.addBeats || (() => {}),
		setSequence: sequenceContainer.setSequence || (() => {}),
		removeBeat: sequenceContainer.removeBeat || (() => {}),
		updateBeat: sequenceContainer.updateBeat || (() => {}),
		selectBeat: sequenceContainer.selectBeat || (() => {}),
		deselectBeat: sequenceContainer.deselectBeat || (() => {}),
		clearSelection: sequenceContainer.clearSelection || (() => {}),
		setCurrentBeatIndex: sequenceContainer.setCurrentBeatIndex || (() => {}),
		updateMetadata: sequenceContainer.updateMetadata || (() => {}),
		markAsSaved: sequenceContainer.markAsSaved || (() => {})
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

// Note: For modern usage, use the derived stores above or access sequenceContainer directly
