export type QuestionFormat = 'text' | 'pictograph';
export type AnswerFormat = 'button' | 'pictograph';

export interface LessonConfig {
	id: string;
	title: string;
	description: string;
	questionFormat: QuestionFormat;
	answerFormat: AnswerFormat;
	prompt: string;
	options?: {
		numOptions?: number; // Number of answer options to show
		randomizeOptions?: boolean; // Whether to randomize the order of options
	};
}

export const lessonConfigs: LessonConfig[] = [
	{
		id: 'letter_to_pictograph',
		title: 'Letter to Pictograph',
		description: 'Learn to identify the pictograph that represents a given letter',
		questionFormat: 'text',
		answerFormat: 'pictograph',
		prompt: 'Choose the pictograph for:',
		options: {
			numOptions: 4,
			randomizeOptions: true
		}
	},
	{
		id: 'pictograph_to_letter',
		title: 'Pictograph to Letter',
		description: 'Learn to identify the letter represented by a pictograph',
		questionFormat: 'pictograph',
		answerFormat: 'button',
		prompt: 'Choose the letter for:',
		options: {
			numOptions: 5,
			randomizeOptions: true
		}
	},
	{
		id: 'turns',
		title: 'Turn Recognition',
		description: 'Learn to identify clockwise and counterclockwise turns in pictographs',
		questionFormat: 'pictograph',
		answerFormat: 'button',
		prompt: 'Identify the turn pattern:',
		options: {
			numOptions: 3,
			randomizeOptions: true
		}
	},
	{
		id: 'positions',
		title: 'Position Recognition',
		description: 'Learn to recognize the positions represented in pictographs',
		questionFormat: 'pictograph',
		answerFormat: 'button',
		prompt: 'Identify the position:',
		options: {
			numOptions: 4,
			randomizeOptions: true
		}
	}
];
