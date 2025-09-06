/**
 * Actors for the sequence state machine
 */
import { fromCallback } from 'xstate';
import type { SequenceMachineEvent, GenerateSequenceInput } from './types';

/**
 * Sequence generation actor
 * Handles the asynchronous process of generating a sequence
 */
export const generateSequenceActor = fromCallback<SequenceMachineEvent, GenerateSequenceInput>(
	({ sendBack, input }) => {
		console.log(
			`Generating ${input.generationType} sequence with options:`,
			input.generationOptions
		);

		// Import the appropriate generator based on the type
		(async () => {
			try {
				// Start with initial progress update
				sendBack({
					type: 'UPDATE_PROGRESS',
					progress: 10,
					message: `Initializing ${input.generationType} sequence generation...`
				});

				// Small delay to ensure the progress update is processed
				await new Promise((resolve) => setTimeout(resolve, 10));

				// Dynamically import the appropriate generator
				let generatedSequence: any[] = [];

				if (input.generationType === 'circular') {
					// Import circular sequence generator
					const { createCircularSequence } = await import(
						'$lib/components/GenerateTab/circular/createCircularSequence'
					);

					sendBack({
						type: 'UPDATE_PROGRESS',
						progress: 30,
						message: 'Creating circular sequence pattern...'
					});

					// Generate the sequence - use type assertion to handle type mismatch
					const circularOptions = input.generationOptions as any;
					generatedSequence = await createCircularSequence(circularOptions);
				} else {
					// Import freeform sequence generator
					const { createFreeformSequence } = await import(
						'$lib/components/GenerateTab/Freeform/createFreeformSequence'
					);

					sendBack({
						type: 'UPDATE_PROGRESS',
						progress: 30,
						message: 'Creating freeform sequence pattern...'
					});

					// Generate the sequence - use type assertion to handle type mismatch
					const freeformOptions = input.generationOptions as any;
					generatedSequence = await createFreeformSequence(freeformOptions);
				}

				// Final progress update
				sendBack({
					type: 'UPDATE_PROGRESS',
					progress: 90,
					message: 'Finalizing sequence...'
				});

				// Send completion event with the generated sequence
				sendBack({
					type: 'GENERATION_COMPLETE',
					output: generatedSequence
				});
			} catch (error) {
				// Handle any errors during generation
				const errorMessage =
					error instanceof Error ? error.message : 'Unknown error during sequence generation';
				console.error('Sequence generation error:', error);

				// Send error event
				sendBack({
					type: 'GENERATION_ERROR',
					error: errorMessage
				});
			}
		})();

		// Return cleanup function
		return () => {
			// Any cleanup if needed
		};
	}
);
