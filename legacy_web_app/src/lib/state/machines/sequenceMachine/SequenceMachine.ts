/**
 * Modern Sequence Machine
 *
 * This module provides a modern implementation of the sequence state machine
 * using XState v5 and the new container-based approach.
 */

import { createModernMachine, createMachineContainer } from '../../core/modernMachine';
import { sequenceContainer } from '../../stores/sequence/SequenceContainer';
import type { GeneratorType, SettingsState } from '../../stores/settingsStore';
import {
	updateSequence,
	selectBeat,
	deselectBeat,
	addBeat,
	removeBeat,
	removeBeatAndFollowing,
	updateBeat,
	clearSequence
} from './actions';
import { generateSequenceActor } from './actors';

/**
 * Interface for the sequence machine context
 */
export interface SequenceMachineContext {
	generationType: 'circular' | 'freeform' | 'template' | null;
	generationOptions: any;
	generationProgress: number;
	generationMessage: string;
	error: string | null;
}

/**
 * Type for sequence machine events
 */
export type SequenceMachineEvent =
	| { type: 'GENERATE'; generationType: string; options: any }
	| { type: 'GENERATION_PROGRESS'; progress: number; message: string }
	| { type: 'GENERATION_COMPLETE'; output: any[] }
	| { type: 'GENERATION_ERROR'; error: string }
	| { type: 'SELECT_BEAT'; beatId: string }
	| { type: 'DESELECT_BEAT'; beatId: string }
	| { type: 'ADD_BEAT'; beat: any }
	| { type: 'REMOVE_BEAT'; beatId: string }
	| { type: 'REMOVE_BEAT_AND_FOLLOWING'; beatId: string }
	| { type: 'UPDATE_BEAT'; beatId: string; updates: any }
	| { type: 'CLEAR_SEQUENCE' }
	| { type: 'RETRY' }
	| { type: 'RESET' };

/**
 * Create the modern sequence machine
 */
export const modernSequenceMachine = createModernMachine<
	SequenceMachineContext,
	SequenceMachineEvent
>({
	id: 'sequence',
	initial: 'idle',
	context: {
		generationType: null,
		generationOptions: null,
		generationProgress: 0,
		generationMessage: '',
		error: null
	},
	states: {
		idle: {
			on: {
				GENERATE: {
					target: 'generating',
					actions: (
						context: SequenceMachineContext,
						event: { type: 'GENERATE'; generationType: string; options: any }
					) => {
						context.generationType = event.generationType as any;
						context.generationOptions = event.options;
						context.generationProgress = 0;
						context.generationMessage = 'Initializing sequence generation...';
						context.error = null;
					}
				},
				SELECT_BEAT: {
					actions: 'selectBeat'
				},
				DESELECT_BEAT: {
					actions: 'deselectBeat'
				},
				ADD_BEAT: {
					actions: 'addBeat'
				},
				REMOVE_BEAT: {
					actions: 'removeBeat'
				},
				REMOVE_BEAT_AND_FOLLOWING: {
					actions: 'removeBeatAndFollowing'
				},
				UPDATE_BEAT: {
					actions: 'updateBeat'
				},
				CLEAR_SEQUENCE: {
					actions: 'clearSequence'
				}
			}
		},
		generating: {
			invoke: {
				src: 'generateSequenceActor',
				input: ({ context }: { context: SequenceMachineContext }) => ({
					type: context.generationType,
					options: context.generationOptions
				}),
				onDone: {
					target: 'idle',
					actions: 'updateSequence'
				},
				onError: {
					target: 'error',
					actions: (context: SequenceMachineContext, event: { error?: Error }) => {
						context.error = event.error?.message || 'Unknown error during sequence generation';
						context.generationProgress = 0;
					}
				}
			},
			on: {
				GENERATION_PROGRESS: {
					actions: (
						context: SequenceMachineContext,
						event: { progress: number; message: string }
					) => {
						context.generationProgress = event.progress;
						context.generationMessage = event.message;
					}
				}
			}
		},
		error: {
			on: {
				RETRY: { target: 'generating' },
				RESET: {
					target: 'idle',
					actions: (context: SequenceMachineContext) => {
						context.error = null;
						context.generationProgress = 0;
						context.generationMessage = '';
					}
				}
			}
		}
	},
	actions: {
		updateSequence,
		selectBeat,
		deselectBeat,
		addBeat,
		removeBeat,
		removeBeatAndFollowing,
		updateBeat,
		clearSequence
	},
	services: {
		generateSequenceActor
	}
});

/**
 * Create the modern sequence machine container
 */
export const modernSequenceContainer = createMachineContainer(modernSequenceMachine, {
	inspect: import.meta.env.DEV ? undefined : undefined
});

/**
 * Create selectors for the sequence machine
 */
export const sequenceSelectors = {
	// Machine state selectors
	isGenerating: () => modernSequenceContainer.state.value === 'generating',
	hasError: () => modernSequenceContainer.state.value === 'error',
	error: () => modernSequenceContainer.state.context.error,
	progress: () => modernSequenceContainer.state.context.generationProgress,
	message: () => modernSequenceContainer.state.context.generationMessage,
	generationType: () => modernSequenceContainer.state.context.generationType,
	generationOptions: () => modernSequenceContainer.state.context.generationOptions,

	// Sequence data selectors
	beats: () => {
		// Get the sequence data from the sequence container
		const state = sequenceContainer.state;
		return state.beats || [];
	},

	selectedBeatIds: () => {
		// Get the selected beat IDs from the sequence container
		const state = sequenceContainer.state;
		return state.selectedBeatIds || [];
	},

	selectedBeats: () => {
		// Get the selected beats from the sequence container
		const state = sequenceContainer.state;
		return state.beats.filter((beat) => state.selectedBeatIds.includes(beat.id)) || [];
	},

	currentBeatIndex: () => {
		// Get the current beat index from the sequence container
		const state = sequenceContainer.state;
		return state.currentBeatIndex || 0;
	},

	currentBeat: () => {
		// Get the current beat from the sequence container
		const state = sequenceContainer.state;
		return state.beats[state.currentBeatIndex] || null;
	},

	beatCount: () => {
		// Get the beat count from the sequence container
		const state = sequenceContainer.state;
		return state.beats.length || 0;
	}
};

/**
 * Create actions for the sequence machine
 */
export const sequenceActions = {
	generate: (generatorType: GeneratorType, options: Omit<SettingsState, 'generatorType' | 'theme' | 'animationsEnabled' | 'lastUsedGeneratorType' | 'favoriteCapTypes'>) => {
		modernSequenceContainer.send({
			type: 'GENERATE',
			generationType: generatorType,
			options
		});
	},
	retry: () => {
		modernSequenceContainer.send({ type: 'RETRY' });
	},
	reset: () => {
		modernSequenceContainer.send({ type: 'RESET' });
	},
	selectBeat: (beatId: string) => {
		modernSequenceContainer.send({ type: 'SELECT_BEAT', beatId });
	},
	deselectBeat: (beatId: string) => {
		modernSequenceContainer.send({ type: 'DESELECT_BEAT', beatId });
	},
	addBeat: (beat: any) => {
		modernSequenceContainer.send({ type: 'ADD_BEAT', beat });
	},
	removeBeat: (beatId: string) => {
		modernSequenceContainer.send({ type: 'REMOVE_BEAT', beatId });
	},
	removeBeatAndFollowing: (beatId: string) => {
		modernSequenceContainer.send({ type: 'REMOVE_BEAT_AND_FOLLOWING', beatId });
	},
	updateBeat: (beatId: string, updates: any) => {
		modernSequenceContainer.send({ type: 'UPDATE_BEAT', beatId, updates });
	},
	clearSequence: () => {
		modernSequenceContainer.send({ type: 'CLEAR_SEQUENCE' });
	}
};
