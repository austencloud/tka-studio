/**
 * Modern Sequence Machine
 *
 * This module provides a modern implementation of the sequence state machine
 * using the new container-based approach with XState v5.
 */

import { assign } from 'xstate';
import { createModernMachine, createMachineContainer } from '$lib/state/core/modernMachine';

// Define the sequence machine context
export interface SequenceMachineContext {
	sequence: any[];
	selectedBeatIndex: number | null;
	isGenerating: boolean;
	generationProgress: number;
	generationMessage: string;
	error: string | null;
}

// Define the sequence machine events
export type SequenceMachineEvent =
	| { type: 'GENERATE'; options: any }
	| { type: 'GENERATION_PROGRESS'; progress: number; message: string }
	| { type: 'GENERATION_COMPLETE'; sequence: any[] }
	| { type: 'GENERATION_ERROR'; error: string }
	| { type: 'SELECT_BEAT'; index: number }
	| { type: 'DESELECT_BEAT' }
	| { type: 'ADD_BEAT'; beat: any }
	| { type: 'REMOVE_BEAT'; index: number }
	| { type: 'UPDATE_BEAT'; index: number; beat: any }
	| { type: 'CLEAR_SEQUENCE' }
	| { type: 'CANCEL_GENERATION' };

// Create the sequence machine
const sequenceMachine = createModernMachine<SequenceMachineContext, SequenceMachineEvent>({
	id: 'sequence',
	initial: 'idle',
	context: {
		sequence: [],
		selectedBeatIndex: null,
		isGenerating: false,
		generationProgress: 0,
		generationMessage: '',
		error: null
	},
	states: {
		idle: {
			on: {
				GENERATE: {
					target: 'generating',
					actions: assign({
						isGenerating: true,
						generationProgress: 0,
						generationMessage: 'Initializing sequence generation...',
						error: null
					})
				},
				SELECT_BEAT: {
					actions: assign({
						selectedBeatIndex: ({ event }) => event.index
					})
				},
				DESELECT_BEAT: {
					actions: assign({
						selectedBeatIndex: null
					})
				},
				ADD_BEAT: {
					actions: assign({
						sequence: ({ context, event }) => [...context.sequence, event.beat]
					})
				},
				REMOVE_BEAT: {
					actions: assign({
						sequence: ({ context, event }) =>
							context.sequence.filter((_: any, index: number) => index !== event.index)
					})
				},
				UPDATE_BEAT: {
					actions: assign({
						sequence: ({ context, event }) =>
							context.sequence.map((beat: any, index: number) => (index === event.index ? event.beat : beat))
					})
				},
				CLEAR_SEQUENCE: {
					actions: assign({
						sequence: [],
						selectedBeatIndex: null
					})
				}
			}
		},
		generating: {
			on: {
				GENERATION_PROGRESS: {
					actions: assign({
						generationProgress: ({ event }) => event.progress,
						generationMessage: ({ event }) => event.message
					})
				},
				GENERATION_COMPLETE: {
					target: 'idle',
					actions: assign({
						sequence: ({ event }) => event.sequence,
						isGenerating: false,
						generationProgress: 100,
						generationMessage: 'Generation complete'
					})
				},
				GENERATION_ERROR: {
					target: 'error',
					actions: assign({
						error: ({ event }) => event.error,
						isGenerating: false
					})
				},
				CANCEL_GENERATION: {
					target: 'idle',
					actions: assign({
						isGenerating: false,
						generationProgress: 0,
						generationMessage: 'Generation cancelled'
					})
				}
			}
		},
		error: {
			on: {
				GENERATE: {
					target: 'generating',
					actions: assign({
						isGenerating: true,
						generationProgress: 0,
						generationMessage: 'Initializing sequence generation...',
						error: null
					})
				}
			}
		}
	}
});

// Create the sequence machine container
export const sequenceContainer = createMachineContainer(sequenceMachine);

// Create sequence actions
export const sequenceActions = {
	generate: (options: any) => {
		sequenceContainer.send({ type: 'GENERATE', options });

		// Simulate generation progress (in a real app, this would come from a service)
		setTimeout(() => {
			sequenceContainer.send({
				type: 'GENERATION_PROGRESS',
				progress: 30,
				message: 'Generating sequence...'
			});

			setTimeout(() => {
				sequenceContainer.send({
					type: 'GENERATION_PROGRESS',
					progress: 70,
					message: 'Finalizing sequence...'
				});

				setTimeout(() => {
					// Generate a simple sequence
					const sequence = Array.from({ length: 8 }, (_, i) => ({
						id: `beat-${i}`,
						index: i,
						data: { value: Math.random() }
					}));

					sequenceContainer.send({
						type: 'GENERATION_COMPLETE',
						sequence
					});
				}, 500);
			}, 500);
		}, 500);
	},

	cancelGeneration: () => {
		sequenceContainer.send({ type: 'CANCEL_GENERATION' });
	},

	selectBeat: (index: number) => {
		sequenceContainer.send({ type: 'SELECT_BEAT', index });
	},

	deselectBeat: () => {
		sequenceContainer.send({ type: 'DESELECT_BEAT' });
	},

	addBeat: (beat: any) => {
		sequenceContainer.send({ type: 'ADD_BEAT', beat });
	},

	removeBeat: (index: number) => {
		sequenceContainer.send({ type: 'REMOVE_BEAT', index });
	},

	updateBeat: (index: number, beat: any) => {
		sequenceContainer.send({ type: 'UPDATE_BEAT', index, beat });
	},

	clearSequence: () => {
		sequenceContainer.send({ type: 'CLEAR_SEQUENCE' });
	}
};
