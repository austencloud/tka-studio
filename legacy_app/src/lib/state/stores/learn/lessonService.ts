import type { LessonConfig } from './lesson_configs';
import pictographDataStore from '$lib/stores/pictograph/pictographStore';
import { get } from 'svelte/store';
import { writable } from 'svelte/store';

// Import the PictographData type
import type { PictographData } from '$lib/types/PictographData';
import type { Letter } from '$lib/types/Letter';
import { DIAMOND } from '$lib/types/Constants';

// Track previous question letters to avoid repetition
const previousLetterStore = writable<Letter | null>(null);
const motionTypes = ['anti', 'pro', 'static', 'dash', 'float'];

// Helper to shuffle an array
function shuffleArray<T>(array: T[]): T[] {
	return [...array].sort(() => Math.random() - 0.5);
}

// Helper function to ensure pictograph data is complete
function ensurePictographComplete(pictograph: PictographData): PictographData {
	// Make a deep copy to avoid modifying the original
	const data = { ...pictograph };

	// Ensure grid is set if gridMode is present
	if (data.gridMode && !data.grid) {
		data.grid = data.gridMode;
	}

	// Pre-populate default values for required fields
	if (!data.motions) data.motions = [];
	if (!data.props) data.props = [];

	return data;
}

// Function to get all available pictograph data from the store
function getAllPictographs(): PictographData[] {
	return get(pictographDataStore) || [];
}

// Function to get pictographs for a specific letter
function getPictographsForLetter(letter: string): PictographData[] {
	const allPictographs = getAllPictographs();
	return allPictographs.filter((p) => p.letter === (letter as Letter));
}

// Function to randomly select a letter that isn't the previous one
function getRandomLetter(availableLetters: Letter[]): Letter {
	if (availableLetters.length === 0) return 'A' as Letter;
	if (availableLetters.length === 1) return availableLetters[0];

	const previousLetter = get(previousLetterStore);
	const filteredLetters = previousLetter
		? availableLetters.filter((l) => l !== previousLetter)
		: availableLetters;

	const randomLetter = filteredLetters[Math.floor(Math.random() * filteredLetters.length)];
	previousLetterStore.set(randomLetter);
	return randomLetter;
}

// Generate a new question based on lesson config and current index
export function generateQuestion(lessonConfig: LessonConfig, questionIndex: number) {
	switch (lessonConfig.id) {
		case 'letter_to_pictograph':
			return generateLetterToPictographQuestion(lessonConfig, questionIndex);
		case 'pictograph_to_letter':
			return generatePictographToLetterQuestion(lessonConfig, questionIndex);
		case 'turns':
			return generateMotionTypeQuestion(lessonConfig, questionIndex);
		case 'positions':
			return generatePositionRecognitionQuestion(lessonConfig, questionIndex);
		default:
			console.error(`Unknown lesson type: ${lessonConfig.id}`);
			return { question: null, options: [], correctAnswer: null };
	}
}

// Generate question for Letter to Pictograph lesson
function generateLetterToPictographQuestion(lessonConfig: LessonConfig, index: number) {
	// Get all available pictographs
	const allPictographs = getAllPictographs();

	if (allPictographs.length === 0) {
		console.warn('No pictograph data available');
		return { question: null, options: [], correctAnswer: null };
	}

	// Get all available letters
	const availableLetters = [...new Set(allPictographs.map((p) => p.letter))].filter(
		Boolean
	) as Letter[];

	// Select a random letter that's different from the previous one
	const letter = getRandomLetter(availableLetters);

	// Get pictographs for this letter
	const pictographsForLetter = getPictographsForLetter(letter as string);

	if (pictographsForLetter.length === 0) {
		console.warn(`No pictographs found for letter ${letter}`);
		return { question: null, options: [], correctAnswer: null };
	}

	// Select a random pictograph as the correct answer
	const randomIndex = Math.floor(Math.random() * pictographsForLetter.length);
	const correctPictograph = ensurePictographComplete(pictographsForLetter[randomIndex]);

	// Collect all pictographs with different letters
	const otherLetterPictographs = allPictographs.filter((p) => p.letter !== letter);

	// Group them by letter to ensure we pick one from each letter
	const pictographsByLetter = new Map<Letter, PictographData[]>();
	otherLetterPictographs.forEach((p) => {
		if (p.letter) {
			if (!pictographsByLetter.has(p.letter)) {
				pictographsByLetter.set(p.letter, []);
			}
			pictographsByLetter.get(p.letter)?.push(p);
		}
	});

	// Select one random pictograph from each letter group
	const wrongOptions: PictographData[] = [];
	const uniqueLetters = Array.from(pictographsByLetter.keys());
	const shuffledLetters = shuffleArray(uniqueLetters);

	// Take enough letters to fill our options (usually 3 wrong answers)
	const wrongLetters = shuffledLetters.slice(0, (lessonConfig.options?.numOptions || 4) - 1);

	// For each wrong letter, pick a random pictograph
	wrongLetters.forEach((letter) => {
		const pictographsForLetter = pictographsByLetter.get(letter) || [];
		if (pictographsForLetter.length > 0) {
			const randomIndex = Math.floor(Math.random() * pictographsForLetter.length);
			wrongOptions.push(ensurePictographComplete(pictographsForLetter[randomIndex]));
		}
	});

	// Combine and shuffle options
	const allOptions = shuffleArray([correctPictograph, ...wrongOptions]);

	return {
		question: letter,
		options: allOptions,
		correctAnswer: correctPictograph
	};
}

// Generate question for Pictograph to Letter lesson
function generatePictographToLetterQuestion(lessonConfig: LessonConfig, index: number) {
	// Get all available pictographs
	const allPictographs = getAllPictographs();

	if (allPictographs.length === 0) {
		console.warn('No pictograph data available');
		return { question: null, options: [], correctAnswer: null };
	}

	// Get all available letters
	const availableLetters = [...new Set(allPictographs.map((p) => p.letter))].filter(
		Boolean
	) as Letter[];

	// Select a random letter that's different from the previous one
	const letter = getRandomLetter(availableLetters);

	// Get pictographs for this letter
	const pictographsForLetter = getPictographsForLetter(letter as string);

	if (pictographsForLetter.length === 0) {
		console.warn(`No pictographs found for letter ${letter}`);
		return { question: null, options: [], correctAnswer: null };
	}

	// Select a random pictograph as the question
	const randomIndex = Math.floor(Math.random() * pictographsForLetter.length);
	const pictograph = ensurePictographComplete(pictographsForLetter[randomIndex]);

	// Generate wrong options (other letters)
	// Make sure to select letters that are all different from each other
	const otherLetters = availableLetters.filter((l) => l !== letter);
	const shuffledLetters = shuffleArray(otherLetters);
	const wrongOptions = shuffledLetters.slice(0, (lessonConfig.options?.numOptions || 4) - 1);

	// Combine and shuffle options
	const allOptions = shuffleArray([letter, ...wrongOptions]);

	return {
		question: pictograph,
		options: allOptions,
		correctAnswer: letter
	};
}

// Generate question for motion type recognition
function generateMotionTypeQuestion(lessonConfig: LessonConfig, index: number) {
	// Get all available pictographs
	const allPictographs = getAllPictographs();

	if (allPictographs.length === 0) {
		console.warn('No pictograph data available');
		return { question: null, options: [], correctAnswer: null };
	}

	// Filter pictographs that have motion data
	const pictographsWithMotion = allPictographs.filter(
		(p) => p.redMotionData?.motionType || p.blueMotionData?.motionType
	);

	if (pictographsWithMotion.length === 0) {
		console.warn('No pictographs with motion data found');
		return { question: null, options: [], correctAnswer: null };
	}

	// Select a pictograph for the question
	const selectedPictograph = pictographsWithMotion[index % pictographsWithMotion.length];

	// Get the motion type (prefer red motion type if available)
	const motionType =
		selectedPictograph.redMotionData?.motionType ||
		selectedPictograph.blueMotionData?.motionType ||
		'static';

	// Generate wrong options (other motion types)
	const wrongOptions = motionTypes.filter((m) => m !== motionType);
	const selectedWrongOptions = wrongOptions.slice(0, (lessonConfig.options?.numOptions || 4) - 1);

	// Combine and shuffle options if needed
	const allOptions = lessonConfig.options?.randomizeOptions
		? shuffleArray([motionType, ...selectedWrongOptions])
		: [motionType, ...selectedWrongOptions];

	return {
		question: ensurePictographComplete(selectedPictograph),
		options: allOptions,
		correctAnswer: motionType
	};
}

// Generate question for Position Recognition lesson
function generatePositionRecognitionQuestion(lessonConfig: LessonConfig, index: number) {
	// Get all available pictographs
	const allPictographs = getAllPictographs();

	if (allPictographs.length === 0) {
		console.warn('No pictograph data available');
		return { question: null, options: [], correctAnswer: null };
	}

	// Find pictographs with start/end positions defined
	const pictographsWithPosition = allPictographs.filter(
		(p) => p.redMotionData?.startLoc || p.blueMotionData?.startLoc
	);

	if (pictographsWithPosition.length === 0) {
		console.warn('No pictographs with position data found');
		return { question: null, options: [], correctAnswer: null };
	}

	// Select a pictograph for the question
	const selectedPictograph = pictographsWithPosition[index % pictographsWithPosition.length];

	// Get the position (prefer red position if available)
	const position = (
		selectedPictograph.redMotionData?.startLoc ||
		selectedPictograph.blueMotionData?.startLoc ||
		'n'
	).toUpperCase();

	// Generate wrong options (other positions)
	const allPositions = [
		...new Set(
			allPictographs
				.flatMap((p) => {
					const redLoc = p.redMotionData?.startLoc;
					const blueLoc = p.blueMotionData?.startLoc;
					// Type guard that ensures only defined values of type string pass through
					return [redLoc, blueLoc].filter((loc): loc is NonNullable<typeof loc> => typeof loc === 'string');
				})
				.map((loc) => loc.toUpperCase())
		)
	];

	const wrongOptions = allPositions.filter((p) => p !== position);
	const selectedWrongOptions = wrongOptions.slice(0, (lessonConfig.options?.numOptions || 4) - 1);

	// Combine and shuffle options if needed
	const allOptions = lessonConfig.options?.randomizeOptions
		? shuffleArray([position, ...selectedWrongOptions])
		: [position, ...selectedWrongOptions];

	return {
		question: ensurePictographComplete(selectedPictograph),
		options: allOptions,
		correctAnswer: position
	};
}

// Check if user's answer is correct
export function checkAnswerLogic(
	userAnswer: any,
	correctAnswer: any,
	lessonConfig: LessonConfig
): boolean {
	switch (lessonConfig.id) {
		case 'letter_to_pictograph':
			// Compare letter property instead of ID since we're now using real data
			return userAnswer.letter === correctAnswer.letter;

		case 'pictograph_to_letter':
			return userAnswer === correctAnswer;

		case 'turns':
			return userAnswer === correctAnswer;

		case 'positions':
			return userAnswer === correctAnswer;

		default:
			console.error(`Unknown lesson type for answer checking: ${lessonConfig.id}`);
			return false;
	}
}
