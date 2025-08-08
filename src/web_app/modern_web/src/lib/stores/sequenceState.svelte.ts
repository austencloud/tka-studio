/**
 * Sequence State - Simplified for Svelte 5 Runes
 * 
 * Minimal working version to get the app running.
 * This provides basic sequence state management with proper Svelte 5 patterns.
 */

import type { SequenceData, BeatData } from '@tka/schemas';
import type { SequenceCreateRequest } from '$services/interfaces';
import type { ArrowPosition } from '$services/interfaces';

// ============================================================================
// CORE STATE
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
	gridMode: 'diamond' as 'diamond' | 'box',
	
	// Arrow positioning state
	arrowPositions: new Map<string, ArrowPosition>(),
	arrowPositioningInProgress: false,
	arrowPositioningError: null as string | null
});

// ============================================================================
// GETTERS
// ============================================================================

export function getCurrentSequence() { return state.currentSequence; }
export function getSequences() { return state.sequences; }
export function getIsLoading() { return state.isLoading; }
export function getError() { return state.error; }
export function getSelectedBeatIndex() { return state.selectedBeatIndex; }
export function getSelectedSequenceId() { return state.selectedSequenceId; }
export function getShowBeatNumbers() { return state.showBeatNumbers; }
export function getGridMode() { return state.gridMode; }
export function getArrowPositions() { return state.arrowPositions; }
export function getArrowPositioningInProgress() { return state.arrowPositioningInProgress; }
export function getArrowPositioningError() { return state.arrowPositioningError; }

// ============================================================================
// COMPUTED GETTERS
// ============================================================================

export function getCurrentBeats(): BeatData[] {
	return state.currentSequence?.beats ?? [];
}

export function getSelectedBeat(): BeatData | null {
	const beatIndex = state.selectedBeatIndex;
	const sequence = state.currentSequence;
	return beatIndex !== null && sequence 
		? sequence.beats[beatIndex] ?? null 
		: null;
}

export function getHasCurrentSequence(): boolean {
	return state.currentSequence !== null;
}

export function getSequenceCount(): number {
	return state.sequences.length;
}

export function getHasUnsavedChanges(): boolean {
	// TODO: Implement change tracking
	return false;
}

export function getHasArrowPositions(): boolean {
	return state.arrowPositions.size > 0;
}

export function getArrowPositioningComplete(): boolean {
	return !state.arrowPositioningInProgress && state.arrowPositions.size > 0;
}

// ============================================================================
// ACTIONS
// ============================================================================

/**
 * Set the current sequence
 */
export function setCurrentSequence(sequence: SequenceData | null): void {
	state.currentSequence = sequence;
	state.selectedSequenceId = sequence?.id ?? null;
	state.selectedBeatIndex = null; // Reset beat selection
}

/**
 * Add sequence to the list
 */
export function addSequence(sequence: SequenceData): void {
	state.sequences.push(sequence);
	setCurrentSequence(sequence);
}

/**
 * Update sequence in the list
 */
export function updateSequence(updatedSequence: SequenceData): void {
	const index = state.sequences.findIndex(s => s.id === updatedSequence.id);
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
export function removeSequence(sequenceId: string): void {
	state.sequences = state.sequences.filter(s => s.id !== sequenceId);
	
	// Clear current sequence if it was deleted
	if (state.currentSequence?.id === sequenceId) {
		setCurrentSequence(null);
	}
}

/**
 * Set sequences list
 */
export function setSequences(newSequences: SequenceData[]): void {
	state.sequences = newSequences;
}

/**
 * Set loading state
 */
export function setLoading(loading: boolean): void {
	state.isLoading = loading;
}

/**
 * Set error state
 */
export function setError(error: string | null): void {
	state.error = error;
}

/**
 * Clear error state
 */
export function clearError(): void {
	state.error = null;
}

/**
 * Update current beat in sequence
 */
export function updateCurrentBeat(beatIndex: number, beatData: BeatData): void {
	if (state.currentSequence && beatIndex >= 0 && beatIndex < state.currentSequence.beats.length) {
		state.currentSequence.beats[beatIndex] = beatData;
	}
}

/**
 * Select a beat
 */
export function selectBeat(beatIndex: number | null): void {
	state.selectedBeatIndex = beatIndex;
}

/**
 * Set grid mode
 */
export function setGridMode(mode: 'diamond' | 'box'): void {
	state.gridMode = mode;
}

/**
 * Set show beat numbers
 */
export function setShowBeatNumbers(show: boolean): void {
	state.showBeatNumbers = show;
}

/**
 * Set arrow positions
 */
export function setArrowPositions(positions: Map<string, ArrowPosition>): void {
	state.arrowPositions = positions;
}

/**
 * Set arrow positioning in progress
 */
export function setArrowPositioningInProgress(inProgress: boolean): void {
	state.arrowPositioningInProgress = inProgress;
}

/**
 * Set arrow positioning error
 */
export function setArrowPositioningError(error: string | null): void {
	state.arrowPositioningError = error;
}

/**
 * Get arrow position for color
 */
export function getArrowPosition(color: string): ArrowPosition | null {
	return state.arrowPositions.get(color) || null;
}

/**
 * Clear all arrow positions
 */
export function clearArrowPositions(): void {
	state.arrowPositions.clear();
}

/**
 * Reset all state
 */
export function resetSequenceState(): void {
	state.currentSequence = null;
	state.sequences = [];
	state.isLoading = false;
	state.error = null;
	state.selectedBeatIndex = null;
	state.selectedSequenceId = null;
	state.showBeatNumbers = true;
	state.gridMode = 'diamond';
	state.arrowPositions.clear();
	state.arrowPositioningInProgress = false;
	state.arrowPositioningError = null;
}
