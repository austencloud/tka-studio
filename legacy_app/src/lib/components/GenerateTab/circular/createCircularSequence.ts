import { settingsStore, type CAPType } from '../store/settings';
import { generatorStore } from '../store/generator';
import { capExecutors } from './capExecutors';
import { validateCircularSequence } from './validators';
import { determineRotationDirection } from '../utils/rotationDeterminer';

interface SequenceGenerationOptions {
	capType: CAPType;
	numBeats: number;
	turnIntensity: number;
	propContinuity: 'continuous' | 'random';
}

// Local implementations of the missing exported functions
function generateOrientations() {
	// Implementation of orientation generation
	const orientations = ['north', 'east', 'south', 'west'];
	return orientations[Math.floor(Math.random() * orientations.length)];
}

function mapPositions(beatIndex: number) {
	// Implementation of position mapping
	const positions = ['alpha1', 'beta3', 'gamma5', 'delta7'];
	return positions[beatIndex % positions.length];
}

export async function createCircularSequence(options: SequenceGenerationOptions) {
	try {
		generatorStore.startGeneration();
		generatorStore.updateProgress(10, 'Initializing sequence generation');

		// Step 1: Determine initial parameters
		const rotationDirection = determineRotationDirection(options.propContinuity);

		generatorStore.updateProgress(30, 'Generating base sequence');
		// Step 2: Generate base sequence
		const baseSequence = generateBaseSequence(options);

		generatorStore.updateProgress(50, 'Applying CAP transformation');
		// Step 3: Apply Circular Algorithmic Permutation (CAP)
		const transformedSequence = applyCAP(baseSequence, options.capType);

		generatorStore.updateProgress(70, 'Validating sequence');
		// Step 4: Validate sequence
		const validationResult = validateCircularSequence(transformedSequence, options.capType);
		if (!validationResult.isValid) {
			throw new Error(validationResult.errors.join('; '));
		}

		generatorStore.updateProgress(90, 'Finalizing sequence');
		// Step 5: Final processing
		const finalSequence = postProcessSequence(transformedSequence);

		generatorStore.completeGeneration();
		return finalSequence;
	} catch (error) {
		const errorMessage =
			error instanceof Error ? error.message : 'Failed to generate circular sequence';

		generatorStore.setError(errorMessage);
		throw error;
	}
}

function generateBaseSequence(options: SequenceGenerationOptions) {
	const sequence = [];

	// Logic mirroring your PyQt circular sequence generation
	for (let i = 0; i < options.numBeats; i++) {
		const beat = generateSingleBeat(options, i);
		sequence.push(beat);
	}

	return sequence;
}

function generateSingleBeat(options: SequenceGenerationOptions, beatIndex: number) {
	// Simplified beat generation logic
	return {
		beat: beatIndex,
		turnIntensity: calculateTurnIntensity(options.turnIntensity),
		orientation: generateOrientations(),
		position: mapPositions(beatIndex)
	};
}

function calculateTurnIntensity(baseTurnIntensity: number) {
	// Add some randomness to turn intensity
	const variation = Math.random() * 0.5 - 0.25;
	return Math.max(0, baseTurnIntensity + variation);
}

function applyCAP(sequence: any[], capType: string) {
	const executor = capExecutors[capType];
	if (!executor) {
		throw new Error(`Unknown CAP type: ${capType}`);
	}
	return executor(sequence);
}

function postProcessSequence(sequence: any[]) {
	// Final transformations, orientation normalization, etc.
	return sequence.map((beat) => ({
		...beat,
		finalOrientation: normalizeOrientation(beat.orientation)
	}));
}

function normalizeOrientation(orientation: any) {
	// Add any final orientation normalization logic
	return orientation;
}
