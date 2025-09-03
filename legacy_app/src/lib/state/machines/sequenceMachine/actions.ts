/**
 * Modern actions for the sequence state machine
 *
 * This module provides actions that interact with the modern sequence container
 * instead of the legacy sequence store.
 */

import { sequenceContainer } from '../../stores/sequence/SequenceContainer';
import type { BeatData } from '../../stores/sequence/SequenceContainer';
import { convertToStoreBeatData } from './types';
import { isSequenceEmpty } from './persistence';
import { selectedStartPos } from '$lib/stores/sequence/selectionStore';
import { pictographContainer } from '$lib/state/stores/pictograph/pictographContainer';
import { defaultPictographData } from '$lib/components/Pictograph/utils/defaultPictographData';
import type { Readable } from 'svelte/store';

/**
 * Helper function to get the current value from a Svelte store
 * This is needed because we can't use the $ syntax in regular TypeScript files
 */
function getStoreValue<T>(store: Readable<T>): T {
	let value: T;
	const unsubscribe = store.subscribe((currentValue) => {
		value = currentValue;
	});
	unsubscribe();
	return value!;
}

/**
 * Update the word name in the sequence metadata based on the current beats
 */
function updateSequenceWord() {
	const state = sequenceContainer.state;
	const beats = state.beats;

	// Update difficulty based on whether beats exist
	const difficulty = beats.length > 0 ? 1 : 0;

	// Extract letters from beats and combine into a word
	const letters = beats
		.map((beat) => {
			// Look for letter data according to the BeatData interface
			return (
				beat.letter ||
				(beat.metadata && typeof beat.metadata.letter === 'string' ? beat.metadata.letter : null)
			);
		})
		.filter((letter): letter is string => letter !== null);

	// Build the word from letters
	const word = letters.join('');

	// Update metadata with word and difficulty
	sequenceContainer.updateMetadata({
		name: word,
		difficulty: difficulty
	});

}

/**
 * Update the sequence container with the generated sequence
 */
export function updateSequence({ event }: { event: any }) {
	// Type assertion for the custom event
	const doneEvent = event as { type: 'GENERATION_COMPLETE'; output?: any[] };

	// Update the sequence container with the generated beats
	if (doneEvent.output && Array.isArray(doneEvent.output)) {
		// Convert the output to the container's BeatData format
		const storeBeats = convertToStoreBeatData(doneEvent.output);
		sequenceContainer.setSequence(storeBeats);
		console.log('Sequence updated with new data:', storeBeats);

		// Update the sequence word
		updateSequenceWord();

		// Update dev tools with the new sequence state
	}
}

/**
 * Select a beat in the sequence
 */
export function selectBeat({ event }: { event: any }) {
	const selectEvent = event as { type: 'SELECT_BEAT'; beatId: string };
	sequenceContainer.selectBeat(selectEvent.beatId);

	// Dispatch a custom event for components that need to know about selection changes
	if (typeof document !== 'undefined') {
		const selectionEvent = new CustomEvent('beat-selected', {
			detail: { beatId: selectEvent.beatId },
			bubbles: true
		});
		document.dispatchEvent(selectionEvent);

		// Update dev tools
	}
}

/**
 * Deselect a beat in the sequence
 */
export function deselectBeat({ event }: { event: any }) {
	const deselectEvent = event as { type: 'DESELECT_BEAT'; beatId: string };
	sequenceContainer.deselectBeat(deselectEvent.beatId);

	// Dispatch a custom event
	if (typeof document !== 'undefined') {
		const selectionEvent = new CustomEvent('beat-deselected', {
			detail: { beatId: deselectEvent.beatId },
			bubbles: true
		});
		document.dispatchEvent(selectionEvent);

		// Update dev tools
	}
}

/**
 * Add a beat to the sequence
 */
export function addBeat({ event }: { event: any }) {
	const addEvent = event as { type: 'ADD_BEAT'; beat: Partial<BeatData> };

	// Generate a unique ID if not provided
	const beatId = addEvent.beat.id || crypto.randomUUID();

	// Create a complete beat object
	const newBeat: BeatData = {
		id: beatId,
		number: addEvent.beat.number || 0,
		...addEvent.beat
	};

	// Add the beat to the sequence container
	sequenceContainer.addBeat(newBeat);

	// Update the sequence word
	updateSequenceWord();

	// Dispatch a custom event
	if (typeof document !== 'undefined') {
		const beatEvent = new CustomEvent('beat-added', {
			detail: { beat: newBeat },
			bubbles: true
		});
		document.dispatchEvent(beatEvent);

		// Update dev tools
	}
}

/**
 * Remove a beat from the sequence
 *
 * This function has been improved to:
 * 1. Preserve the start position when removing beats
 * 2. Ensure the OptionPicker refreshes with valid options
 * 3. Validate that the start position data is correct (static motion, matching start/end locations)
 */
export function removeBeat({ event }: { event: any }) {
	const removeEvent = event as { type: 'REMOVE_BEAT'; beatId: string };

	// Store the current start position before removing the beat
	// This ensures we can restore it if needed
	let currentStartPos = null;
	try {
		// Use our helper function to get the current value from the store
		currentStartPos = getStoreValue(selectedStartPos);

		// Validate and fix the start position data if needed
		if (currentStartPos) {
			// Mark this as a start position
			currentStartPos.isStartPosition = true;

			// Ensure start and end locations match for a start position
			if (currentStartPos.redMotionData) {
				currentStartPos.redMotionData.motionType = 'static';
				currentStartPos.redMotionData.endLoc = currentStartPos.redMotionData.startLoc;
				currentStartPos.redMotionData.endOri = currentStartPos.redMotionData.startOri;
				currentStartPos.redMotionData.turns = 0;
			}

			if (currentStartPos.blueMotionData) {
				currentStartPos.blueMotionData.motionType = 'static';
				currentStartPos.blueMotionData.endLoc = currentStartPos.blueMotionData.startLoc;
				currentStartPos.blueMotionData.endOri = currentStartPos.blueMotionData.startOri;
				currentStartPos.blueMotionData.turns = 0;
			}

			// Create a deep copy to avoid reference issues
			currentStartPos = JSON.parse(JSON.stringify(currentStartPos));
		}
	} catch (error) {
		console.error('Failed to get current start position:', error);
	}

	sequenceContainer.removeBeat(removeEvent.beatId);

	// Update the sequence word
	updateSequenceWord();

	// Dispatch a custom event
	if (typeof document !== 'undefined') {
		const beatEvent = new CustomEvent('beat-removed', {
			detail: { beatId: removeEvent.beatId },
			bubbles: true
		});
		document.dispatchEvent(beatEvent);

		// If we have a start position, ensure it's still active
		if (currentStartPos) {
			// Ensure the start position is preserved by dispatching the event again
			const startPosEvent = new CustomEvent('start-position-selected', {
				detail: { startPosition: currentStartPos },
				bubbles: true
			});
			document.dispatchEvent(startPosEvent);

			// Also dispatch an event to refresh the OptionPicker with valid options
			// based on the start position
			const refreshOptionsEvent = new CustomEvent('refresh-options', {
				detail: { startPosition: currentStartPos },
				bubbles: true
			});
			document.dispatchEvent(refreshOptionsEvent);

			// Save the start position to localStorage
			try {
				localStorage.setItem('start_position', JSON.stringify(currentStartPos));
				console.log('Saved start position to localStorage after beat removal');
			} catch (error) {
				console.error('Failed to save start position to localStorage:', error);
			}

			console.log('Preserved start position after beat removal');
		}

		// Update dev tools
	}
}

/**
 * Remove a beat and all following beats from the sequence
 *
 * This function has been improved to:
 * 1. Preserve the start position when removing beats
 * 2. Ensure the OptionPicker refreshes with valid options
 */
export function removeBeatAndFollowing({ event }: { event: any }) {
	const removeEvent = event as { type: 'REMOVE_BEAT_AND_FOLLOWING'; beatId: string };

	// Find the beat index
	const beatIndex = sequenceContainer.state.beats.findIndex(
		(beat) => beat.id === removeEvent.beatId
	);

	if (beatIndex >= 0) {
		// Get all beats that should be removed (the selected beat and all following beats)
		const beatsToRemove = sequenceContainer.state.beats.slice(beatIndex).map((beat) => beat.id);

		// Store the current start position before removing beats
		// This ensures we can restore it if needed
		let currentStartPos = null;
		try {
			// Use our helper function to get the current value from the store
			currentStartPos = getStoreValue(selectedStartPos);

			// Validate and fix the start position data if needed
			if (currentStartPos) {
				// Mark this as a start position
				currentStartPos.isStartPosition = true;



			}
		} catch (error) {
			console.error('Failed to get current start position:', error);
		}

		// Remove each beat
		beatsToRemove.forEach((id) => {
			sequenceContainer.removeBeat(id);
		});

		// Update the sequence word
		updateSequenceWord();

		// Dispatch a custom event
		if (typeof document !== 'undefined') {
			// First, dispatch the sequence-updated event
			const sequenceUpdatedEvent = new CustomEvent('sequence-updated', {
				detail: { type: 'beats-removed', fromIndex: beatIndex },
				bubbles: true
			});
			document.dispatchEvent(sequenceUpdatedEvent);

			// If we have a start position, ensure it's still active
			// This is especially important when removing the first beat
			if (currentStartPos) {
				// Ensure the start position is preserved by dispatching the event again
				const startPosEvent = new CustomEvent('start-position-selected', {
					detail: { startPosition: currentStartPos },
					bubbles: true
				});
				document.dispatchEvent(startPosEvent);

				// Also dispatch an event to refresh the OptionPicker with valid options
				// based on the start position
				const refreshOptionsEvent = new CustomEvent('refresh-options', {
					detail: { startPosition: currentStartPos },
					bubbles: true
				});
				document.dispatchEvent(refreshOptionsEvent);

				// Save the start position to localStorage
				try {
					localStorage.setItem('start_position', JSON.stringify(currentStartPos));
					console.log('Saved start position to localStorage after beat removal');
				} catch (error) {
					console.error('Failed to save start position to localStorage:', error);
				}

				console.log('Preserved start position after beat removal');
			}

			// Update dev tools
		}
	}
}

/**
 * Update a beat in the sequence
 */
export function updateBeat({ event }: { event: any }) {
	const updateEvent = event as {
		type: 'UPDATE_BEAT';
		beatId: string;
		updates: Partial<BeatData>;
	};
	sequenceContainer.updateBeat(updateEvent.beatId, updateEvent.updates);

	// Update the sequence word
	updateSequenceWord();

	// Dispatch a custom event
	if (typeof document !== 'undefined') {
		const beatEvent = new CustomEvent('beat-updated', {
			detail: { beatId: updateEvent.beatId, updates: updateEvent.updates },
			bubbles: true
		});
		document.dispatchEvent(beatEvent);

		// Update dev tools
	}
}

/**
 * Clear the entire sequence
 *
 * This function has been improved to:
 * 1. Ensure both sequence and start position are properly cleared
 * 2. Properly reset state to allow creating new sequences
 * 3. Notify all components of the change
 */
export function clearSequence() {
	console.log('Clearing sequence and start position');

	// Set an empty sequence
	sequenceContainer.setSequence([]);

	// Update the sequence word
	updateSequenceWord();

	// Reset metadata to initial state instead of just clearing the name
	sequenceContainer.updateMetadata({
		name: '',
		difficulty: 0,
		tags: []
	});

	// Ensure isSequenceEmpty is set to true
	// This is a backup in case the subscription in persistence.ts doesn't trigger
	isSequenceEmpty.set(true);

	// Reset the start position to null
	selectedStartPos.set(null);

	// Reset the pictograph container to default data
	pictographContainer.setData(defaultPictographData);

	// Instead of removing localStorage items, save the empty state
	// This ensures we have a valid empty state rather than missing data
	if (typeof window !== 'undefined') {
		try {
			// Save the empty sequence state to localStorage
			sequenceContainer.saveToLocalStorage();

			// Save empty start position
			localStorage.setItem('start_position', JSON.stringify(null));

			// Save empty backup
			localStorage.setItem(
				'sequence_backup',
				JSON.stringify({
					beats: [],
					options: null,
					word: ''
				})
			);

			console.log('Saved empty sequence state to localStorage');
		} catch (error) {
			console.error('Error saving empty sequence state:', error);
		}
	}

	// Mark the sequence as not modified after clearing
	// This prevents unnecessary saves
	sequenceContainer.markAsSaved();

	// Dispatch custom events to notify components
	if (typeof document !== 'undefined') {
		// Notify about sequence clearing
		const sequenceUpdatedEvent = new CustomEvent('sequence-updated', {
			detail: { type: 'sequence-cleared' },
			bubbles: true
		});
		document.dispatchEvent(sequenceUpdatedEvent);

		// Notify about start position clearing
		const startPosEvent = new CustomEvent('start-position-selected', {
			detail: { startPosition: null },
			bubbles: true
		});
		document.dispatchEvent(startPosEvent);

		// Dispatch an additional event to reset the Option Picker state
		const resetOptionPickerEvent = new CustomEvent('reset-option-picker', {
			bubbles: true
		});
		document.dispatchEvent(resetOptionPickerEvent);


	}
}
