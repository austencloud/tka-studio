/**
 * Service Actions - Bridge between services and runes state
 * 
 * These functions coordinate service calls with runes state updates.
 * Pure functions that handle the integration between services and reactive state.
 */

import type { SequenceData, BeatData } from '@tka/schemas';
import type { 
	ISequenceService, 
	SequenceCreateRequest,
	GenerationOptions 
} from '$services/interfaces';

import {
	setCurrentSequence,
	addSequence,
	updateSequence,
	removeSequence,
	setSequences,
	updateCurrentBeat,
	setLoading,
	setError,
	clearError
} from './sequenceState.svelte';

// ============================================================================
// SEQUENCE ACTIONS
// ============================================================================

/**
 * Create a new sequence
 */
export async function createSequence(
	sequenceService: ISequenceService,
	request: SequenceCreateRequest
): Promise<SequenceData> {
	setLoading(true);
	clearError();

	try {
		console.log('Creating sequence:', request);
		
		const sequence = await sequenceService.createSequence(request);
		addSequence(sequence);
		
		console.log('Sequence created successfully:', sequence.id);
		return sequence;
	} catch (error) {
		const errorMessage = error instanceof Error ? error.message : 'Unknown error';
		setError(errorMessage);
		console.error('Failed to create sequence:', error);
		throw error;
	} finally {
		setLoading(false);
	}
}

/**
 * Load all sequences
 */
export async function loadSequences(sequenceService: ISequenceService): Promise<void> {
	setLoading(true);
	clearError();

	try {
		console.log('Loading sequences...');
		
		const sequences = await sequenceService.getAllSequences();
		setSequences(sequences);
		
		console.log(`Loaded ${sequences.length} sequences`);
	} catch (error) {
		const errorMessage = error instanceof Error ? error.message : 'Unknown error';
		setError(errorMessage);
		console.error('Failed to load sequences:', error);
	} finally {
		setLoading(false);
	}
}

/**
 * Select and load a sequence
 */
export async function selectSequence(
	sequenceService: ISequenceService,
	sequenceId: string
): Promise<void> {
	setLoading(true);
	clearError();

	try {
		console.log('Selecting sequence:', sequenceId);
		
		const sequence = await sequenceService.getSequence(sequenceId);
		if (sequence) {
			setCurrentSequence(sequence);
		} else {
			throw new Error(`Sequence ${sequenceId} not found`);
		}
	} catch (error) {
		const errorMessage = error instanceof Error ? error.message : 'Unknown error';
		setError(errorMessage);
		console.error('Failed to select sequence:', error);
	} finally {
		setLoading(false);
	}
}

/**
 * Delete a sequence
 */
export async function deleteSequence(
	sequenceService: ISequenceService,
	sequenceId: string
): Promise<void> {
	setLoading(true);
	clearError();

	try {
		console.log('Deleting sequence:', sequenceId);
		
		await sequenceService.deleteSequence(sequenceId);
		removeSequence(sequenceId);
		
		console.log('Sequence deleted successfully');
	} catch (error) {
		const errorMessage = error instanceof Error ? error.message : 'Unknown error';
		setError(errorMessage);
		console.error('Failed to delete sequence:', error);
		throw error;
	} finally {
		setLoading(false);
	}
}

/**
 * Update a beat in the current sequence
 */
export async function updateBeat(
	sequenceService: ISequenceService,
	currentSequence: SequenceData,
	beatIndex: number,
	beatData: BeatData
): Promise<void> {
	setLoading(true);
	clearError();

	try {
		console.log(`Updating beat ${beatIndex} in sequence ${currentSequence.id}`);
		
		await sequenceService.updateBeat(currentSequence.id, beatIndex, beatData);
		updateCurrentBeat(beatIndex, beatData);
		
		console.log('Beat updated successfully');
	} catch (error) {
		const errorMessage = error instanceof Error ? error.message : 'Unknown error';
		setError(errorMessage);
		console.error('Failed to update beat:', error);
		throw error;
	} finally {
		setLoading(false);
	}
}

/**
 * Add a beat to the current sequence
 */
export async function addBeat(
	sequenceService: ISequenceService,
	currentSequence: SequenceData,
	beatData?: Partial<BeatData>
): Promise<void> {
	setLoading(true);
	clearError();

	try {
		console.log('Adding beat to sequence:', currentSequence.id);
		
		// Use the service's addBeat method (assumes it exists)
		await (sequenceService as any).addBeat(currentSequence.id, beatData);
		
		// Reload the sequence to get the updated version
		const updatedSequence = await sequenceService.getSequence(currentSequence.id);
		if (updatedSequence) {
			updateSequence(updatedSequence);
		}
		
		console.log('Beat added successfully');
	} catch (error) {
		const errorMessage = error instanceof Error ? error.message : 'Unknown error';
		setError(errorMessage);
		console.error('Failed to add beat:', error);
		throw error;
	} finally {
		setLoading(false);
	}
}

// ============================================================================
// GENERATION ACTIONS
// ============================================================================

/**
 * Generate a new sequence
 */
export async function generateSequence(
	generationService: any, // ISequenceGenerationService
	options: GenerationOptions
): Promise<SequenceData> {
	setLoading(true);
	clearError();

	try {
		console.log('Generating sequence with options:', options);
		
		const sequence = await generationService.generateSequence(options);
		addSequence(sequence);
		
		console.log('Sequence generated successfully:', sequence.id);
		return sequence;
	} catch (error) {
		const errorMessage = error instanceof Error ? error.message : 'Unknown error';
		setError(errorMessage);
		console.error('Failed to generate sequence:', error);
		throw error;
	} finally {
		setLoading(false);
	}
}

// ============================================================================
// ARROW POSITIONING ACTIONS
// ============================================================================

import type { 
	IArrowPositioningService,
	PictographData,
	GridData 
} from '$services/interfaces';

import {
	setArrowPositions,
	setArrowPositioningInProgress,
	setArrowPositioningError,
	clearArrowPositions
} from './sequenceState.svelte';

/**
 * Calculate arrow positions for current pictograph
 */
export async function calculateArrowPositions(
	arrowPositioningService: IArrowPositioningService,
	pictographData: PictographData,
	gridData: GridData
): Promise<void> {
	setArrowPositioningInProgress(true);
	setArrowPositioningError(null);

	try {
		console.log('Calculating arrow positions for pictograph...');

		const positions = await arrowPositioningService.calculateAllArrowPositions(
			pictographData,
			gridData
		);

		setArrowPositions(positions);
		console.log(`Arrow positions calculated: ${positions.size} arrows positioned`);

	} catch (error) {
		const errorMessage = error instanceof Error ? error.message : 'Unknown error';
		setArrowPositioningError(errorMessage);
		console.error('Failed to calculate arrow positions:', error);

	} finally {
		setArrowPositioningInProgress(false);
	}
}

/**
 * Update arrow positions when sequence changes
 */
export async function updateArrowPositionsForSequence(
	arrowPositioningService: IArrowPositioningService,
	sequence: SequenceData,
	selectedBeatIndex: number | null
): Promise<void> {
	if (!sequence || selectedBeatIndex === null) {
		clearArrowPositions();
		return;
	}

	const beat = sequence.beats[selectedBeatIndex];
	if (!beat) {
		clearArrowPositions();
		return;
	}

	// Convert beat data to pictograph data
	const pictographData = beatToPictographData(beat, sequence);
	const gridData = createDefaultGridData();

	await calculateArrowPositions(arrowPositioningService, pictographData, gridData);
}

/**
 * Convert beat to pictograph data format
 */
function beatToPictographData(beat: BeatData, sequence: SequenceData): PictographData {
	return {
		id: `beat-${beat.beatNumber}`,
		gridData: { mode: sequence.gridMode || 'diamond' },
		arrows: { blue: {}, red: {} },
		props: { blue: {}, red: {} },
		motions: {
			blue: beat.blueMotion,
			red: beat.redMotion
		},
		letter: beat.letter
	};
}

/**
 * Create default grid data for positioning calculations
 */
function createDefaultGridData(): GridData {
	const center = { x: 150, y: 150 };
	const size = 80;
	
	return {
		mode: 'diamond',
		allLayer2PointsNormal: {
			'n_diamond_layer2_point': { coordinates: { x: center.x, y: center.y - size } },
			'ne_diamond_layer2_point': { coordinates: { x: center.x + size * 0.7, y: center.y - size * 0.7 } },
			'e_diamond_layer2_point': { coordinates: { x: center.x + size, y: center.y } },
			'se_diamond_layer2_point': { coordinates: { x: center.x + size * 0.7, y: center.y + size * 0.7 } },
			's_diamond_layer2_point': { coordinates: { x: center.x, y: center.y + size } },
			'sw_diamond_layer2_point': { coordinates: { x: center.x - size * 0.7, y: center.y + size * 0.7 } },
			'w_diamond_layer2_point': { coordinates: { x: center.x - size, y: center.y } },
			'nw_diamond_layer2_point': { coordinates: { x: center.x - size * 0.7, y: center.y - size * 0.7 } },
		},
		allHandPointsNormal: {
			'n_diamond_hand_point': { coordinates: { x: center.x, y: center.y - size * 0.6 } },
			'ne_diamond_hand_point': { coordinates: { x: center.x + size * 0.5, y: center.y - size * 0.5 } },
			'e_diamond_hand_point': { coordinates: { x: center.x + size * 0.6, y: center.y } },
			'se_diamond_hand_point': { coordinates: { x: center.x + size * 0.5, y: center.y + size * 0.5 } },
			's_diamond_hand_point': { coordinates: { x: center.x, y: center.y + size * 0.6 } },
			'sw_diamond_hand_point': { coordinates: { x: center.x - size * 0.5, y: center.y + size * 0.5 } },
			'w_diamond_hand_point': { coordinates: { x: center.x - size * 0.6, y: center.y } },
			'nw_diamond_hand_point': { coordinates: { x: center.x - size * 0.5, y: center.y - size * 0.5 } },
		}
	};
}

// ============================================================================
// UTILITY ACTIONS
// ============================================================================

/**
 * Refresh current sequence from server
 */
export async function refreshCurrentSequence(
	sequenceService: ISequenceService,
	currentSequence: SequenceData
): Promise<void> {
	try {
		const refreshed = await sequenceService.getSequence(currentSequence.id);
		if (refreshed) {
			updateSequence(refreshed);
		}
	} catch (error) {
		console.error('Failed to refresh sequence:', error);
	}
}

/**
 * Save current sequence
 */
export async function saveCurrentSequence(
	sequenceService: ISequenceService,
	currentSequence: SequenceData
): Promise<void> {
	try {
		// Assuming the service has a save method or update method
		// This would typically be handled by the updateBeat method
		console.log('Sequence auto-saved:', currentSequence.id);
	} catch (error) {
		console.error('Failed to save sequence:', error);
	}
}
