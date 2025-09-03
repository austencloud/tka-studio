import { settingsStore, type CAPType } from '../store/settings';
import { generatorStore } from '../store/generator';
import { determineRotationDirection } from '../utils/rotationDeterminer';
import { validateFreeformSequence } from './validators';

interface SequenceGenerationOptions {
	capType: CAPType;
	numBeats: number;
	turnIntensity: number;
	propContinuity: 'continuous' | 'random';
	letterTypes?: string[]; // Make letterTypes optional to match usage in FreeformSequencer.svelte
}

// Define structure for beat data to match what validation function expects
interface BeatData {
	beat: number;
	turnIntensity: number;
	orientation: {
		blue: string;
		red: string;
	};
	position: string;
	letterType: string;
	[key: string]: any;
}

// Local implementations of the missing exported functions
function generateOrientations(): { blue: string; red: string } {
	// Implementation of orientation generation
	const orientations = ['north', 'east', 'south', 'west'];
	const blueOrientation = orientations[Math.floor(Math.random() * orientations.length)];
	const redOrientation = orientations[Math.floor(Math.random() * orientations.length)];
	return { blue: blueOrientation, red: redOrientation };
}

function mapPositions(beatIndex: number): string {
	// Implementation of position mapping
	const positions = ['alpha1', 'beta3', 'gamma5'];
	return positions[beatIndex % positions.length];
}

export async function createFreeformSequence(options: SequenceGenerationOptions) {
	try {
		generatorStore.startGeneration();
		generatorStore.updateProgress(10, 'Initializing freeform sequence generation');

		// Step 1: Determine rotation parameters
		const rotationDirection = determineRotationDirection(options.propContinuity);

		generatorStore.updateProgress(30, 'Generating base sequence');
		// Step 2: Generate base sequence
		const baseSequence = generateBaseSequence(options);

		generatorStore.updateProgress(70, 'Validating sequence');
		// Step 3: Validate sequence
		const validationResult = validateFreeformSequence(
			baseSequence,
			options.letterTypes || [] // Pass letterTypes array instead of capType
		);
		if (!validationResult.isValid) {
			throw new Error(validationResult.errors.join('; '));
		}

		generatorStore.updateProgress(90, 'Finalizing sequence');
		// Step 4: Final processing
		const finalSequence = postProcessSequence(baseSequence);

		generatorStore.completeGeneration();
		return finalSequence;
	} catch (error) {
		const errorMessage =
			error instanceof Error ? error.message : 'Failed to generate freeform sequence';

		generatorStore.setError(errorMessage);
		throw error;
	}
}

function generateBaseSequence(options: SequenceGenerationOptions): BeatData[] {
	const sequence: BeatData[] = [];

	for (let i = 0; i < options.numBeats; i++) {
		const beat = generateSingleBeat(options, i);
		sequence.push(beat);
	}

	return sequence;
}

function generateSingleBeat(options: SequenceGenerationOptions, beatIndex: number): BeatData {
	return {
		beat: beatIndex,
		turnIntensity: calculateTurnIntensity(options.turnIntensity),
		orientation: generateOrientations(),
		position: mapPositions(beatIndex),
		letterType: selectLetterType(options.letterTypes || [])
	};
}

function calculateTurnIntensity(baseTurnIntensity: number): number {
	const variation = Math.random() * 0.5 - 0.25;
	return Math.max(0, baseTurnIntensity + variation);
}

function selectLetterType(letterTypes: string[]): string {
	// If no types specified, choose randomly
	if (letterTypes.length === 0) {
		const allTypes = ['type1', 'type2', 'type3', 'type4'];
		return allTypes[Math.floor(Math.random() * allTypes.length)];
	}

	// Choose randomly from provided types
	return letterTypes[Math.floor(Math.random() * letterTypes.length)];
}

function postProcessSequence(sequence: BeatData[]): BeatData[] {
	return sequence.map((beat) => ({
		...beat,
		finalOrientation: normalizeOrientation(beat.orientation)
	}));
}

function normalizeOrientation(orientation: any): any {
	return orientation;
}
