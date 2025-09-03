/**
 * Type definitions for the sequence state machine
 */
import type { BeatData as StoreBeatData } from '../../stores/sequenceStore';

// Types for sequence generation options
export interface SequenceGenerationOptions {
	capType: CAPType;
	numBeats: number;
	turnIntensity: number;
	propContinuity: 'continuous' | 'random';
}

export interface FreeformSequenceOptions {
	numBeats: number;
	turnIntensity: number;
	propContinuity: 'continuous' | 'random';
	letterTypes: string[];
}

// Input type for the sequence generation actor
export interface GenerateSequenceInput {
	generationType: 'circular' | 'freeform';
	generationOptions: SequenceGenerationOptions | FreeformSequenceOptions;
}

// Context for the sequence state machine
export interface SequenceMachineContext {
	error: string | null;
	isGenerating: boolean;
	generationProgress: number;
	generationMessage: string;
	generationType: 'circular' | 'freeform';
	generationOptions: SequenceGenerationOptions | FreeformSequenceOptions;
}

// Events for the sequence state machine
export type SequenceMachineEvent =
	// Generation events
	| {
			type: 'GENERATE';
			options: SequenceGenerationOptions | FreeformSequenceOptions;
			generationType: 'circular' | 'freeform';
	  }
	| { type: 'UPDATE_PROGRESS'; progress: number; message: string } // Sent by actor
	| { type: 'GENERATION_COMPLETE'; output: any[] } // Sent by actor on success
	| { type: 'GENERATION_ERROR'; error: string } // Sent by actor on failure (optional)
	| { type: 'CANCEL' }
	| { type: 'RETRY' }
	| { type: 'RESET' }

	// Beat manipulation events
	| { type: 'SELECT_BEAT'; beatId: string }
	| { type: 'DESELECT_BEAT'; beatId?: string } // Optional beatId, if not provided, deselects all
	| { type: 'ADD_BEAT'; beat: Partial<StoreBeatData> }
	| { type: 'REMOVE_BEAT'; beatId: string }
	| { type: 'REMOVE_BEAT_AND_FOLLOWING'; beatId: string }
	| { type: 'UPDATE_BEAT'; beatId: string; updates: Partial<StoreBeatData> }
	| { type: 'CLEAR_SEQUENCE' };

// CAP Type for circular sequence generation
export type CAPType =
	| 'mirrored'
	| 'rotated'
	| 'mirrored_complementary'
	| 'rotated_complementary'
	| 'mirrored_swapped'
	| 'rotated_swapped'
	| 'strict_mirrored'
	| 'strict_rotated'
	| 'strict_complementary'
	| 'strict_swapped'
	| 'swapped_complementary';

/**
 * Convert generated sequence data to the store's BeatData format
 */
export function convertToStoreBeatData(componentBeats: any[]): StoreBeatData[] {
	return componentBeats.map((beat, index) => ({
		id: beat.id || `beat-${index}`,
		number: beat.number || index + 1,
		letter: beat.letterType || beat.letter || '',
		position: beat.position || '',
		orientation:
			typeof beat.orientation === 'object'
				? `${beat.orientation.blue || 'in'}_${beat.orientation.red || 'in'}`
				: beat.orientation || '',
		turnsTuple: beat.turnIntensity ? String(beat.turnIntensity) : '',
		redPropData: beat.redPropData || null,
		bluePropData: beat.bluePropData || null,
		redArrowData: beat.redArrowData || null,
		blueArrowData: beat.blueArrowData || null,
		pictographData: beat.pictographData || null,
		metadata: beat.metadata || {}
	}));
}
