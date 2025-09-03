import { writable, derived, get } from 'svelte/store';
import { lessonConfigs } from './lesson_configs';
import { checkAnswerLogic, generateQuestion } from './lessonService';
import { progressStore } from './progressStore';

export type LessonMode = 'fixed_question' | 'countdown';
export type ViewType = 'selector' | 'lesson' | 'results';

interface LearnState {
	currentView: ViewType;
	selectedLessonType: string | null;
	selectedMode: LessonMode;
	lessonConfig: any | null;
	quizActive: boolean;
	currentQuestionIndex: number;
	totalQuestions: number;
	remainingTime: number;
	currentQuestionData: any;
	currentAnswerOptions: any[];
	correctAnswer: any;
	userAnswer: any | null;
	isAnswerCorrect: boolean | null;
	incorrectGuesses: number;
	score: number;
	lessonHistory: Array<{
		question: any;
		correctAnswer: any;
		userAnswer: any;
		isCorrect: boolean;
	}>;
}

const initialState: LearnState = {
	currentView: 'selector',
	selectedLessonType: null,
	selectedMode: 'fixed_question',
	lessonConfig: null,
	quizActive: false,
	currentQuestionIndex: 0,
	totalQuestions: 30, // Default for fixed_question mode
	remainingTime: 60, // Default for countdown mode (seconds)
	currentQuestionData: null,
	currentAnswerOptions: [],
	correctAnswer: null,
	userAnswer: null,
	isAnswerCorrect: null,
	incorrectGuesses: 0,
	score: 0,
	lessonHistory: []
};

const createLearnStore = () => {
	const { subscribe, set, update } = writable<LearnState>(initialState);

	// Timer interval reference
	let timerInterval: ReturnType<typeof setInterval> | null = null;

	return {
		subscribe,

		selectLesson: (lessonType: string) =>
			update((state) => {
				const config = lessonConfigs.find((c) => c.id === lessonType);

				if (!config) {
					console.error(`Lesson config not found for: ${lessonType}`);
					return state;
				}

				return {
					...state,
					selectedLessonType: lessonType,
					lessonConfig: config,
					currentView: 'lesson'
				};
			}),

		setMode: (mode: LessonMode) =>
			update((state) => ({
				...state,
				selectedMode: mode
			})),

		startLesson: () => {
			update((state) => {
				// Stop any existing timer
				if (timerInterval) {
					clearInterval(timerInterval);
					timerInterval = null;
				}

				return {
					...state,
					quizActive: true,
					currentQuestionIndex: 0,
					score: 0,
					incorrectGuesses: 0,
					userAnswer: null,
					isAnswerCorrect: null,
					lessonHistory: [],
					remainingTime: state.selectedMode === 'countdown' ? 60 : 0
				};
			});

			// Start timer if in countdown mode
			const store = get(learnStore);
			if (store.selectedMode === 'countdown' && store.quizActive) {
				timerInterval = setInterval(() => {
					learnStore.updateTimer();
				}, 1000);
			}

			// Generate the first question
			learnStore.generateNextQuestion();
		},

		generateNextQuestion: () =>
			update((state) => {
				if (!state.lessonConfig) return state;

				const { question, options, correctAnswer } = generateQuestion(
					state.lessonConfig,
					state.currentQuestionIndex
				);

				return {
					...state,
					currentQuestionData: question,
					currentAnswerOptions: options,
					correctAnswer,
					userAnswer: null,
					isAnswerCorrect: null
				};
			}),

		submitAnswer: (answer: any) =>
			update((state) => {
				const isCorrect = checkAnswerLogic(answer, state.correctAnswer, state.lessonConfig);

				// Update lesson history
				const historyEntry = {
					question: state.currentQuestionData,
					correctAnswer: state.correctAnswer,
					userAnswer: answer,
					isCorrect
				};

				const updatedHistory = [...state.lessonHistory, historyEntry];

				// Update score
				const newScore = isCorrect ? state.score + 1 : state.score;
				const newIncorrectGuesses = isCorrect ? state.incorrectGuesses : state.incorrectGuesses + 1;

				return {
					...state,
					userAnswer: answer,
					isAnswerCorrect: isCorrect,
					score: newScore,
					incorrectGuesses: newIncorrectGuesses,
					lessonHistory: updatedHistory
				};
			}),

		nextQuestionOrEnd: () =>
			update((state) => {
				const nextIndex = state.currentQuestionIndex + 1;

				// Check if we've reached the end of the quiz
				if (state.selectedMode === 'fixed_question' && nextIndex >= state.totalQuestions) {
					if (timerInterval) {
						clearInterval(timerInterval);
						timerInterval = null;
					}

					// Update progress store with the lesson results
					if (state.selectedLessonType) {
						const score = Math.round((state.score / state.totalQuestions) * 100);

						progressStore.updateLessonProgress(
							state.selectedLessonType,
							score,
							state.lessonHistory.length,
							state.totalQuestions
						);
					}

					return {
						...state,
						currentView: 'results',
						quizActive: false
					};
				}

				return {
					...state,
					currentQuestionIndex: nextIndex
				};
			}),

		updateTimer: () =>
			update((state) => {
				if (!state.quizActive || state.selectedMode !== 'countdown') {
					return state;
				}

				const newTime = Math.max(0, state.remainingTime - 1);

				if (newTime === 0) {
					if (timerInterval) {
						clearInterval(timerInterval);
						timerInterval = null;
					}

					// Update progress store with the lesson results
					if (state.selectedLessonType) {
						const totalQuestions = state.lessonHistory.length;
						const score = totalQuestions > 0 ? Math.round((state.score / totalQuestions) * 100) : 0;

						progressStore.updateLessonProgress(
							state.selectedLessonType,
							score,
							totalQuestions,
							totalQuestions
						);
					}

					return {
						...state,
						remainingTime: 0,
						currentView: 'results',
						quizActive: false
					};
				}

				return {
					...state,
					remainingTime: newTime
				};
			}),

		showResults: () =>
			update((state) => {
				if (timerInterval) {
					clearInterval(timerInterval);
					timerInterval = null;
				}

				// Update progress store with the lesson results
				if (state.selectedLessonType) {
					const totalQuestions =
						state.selectedMode === 'fixed_question'
							? state.totalQuestions
							: state.lessonHistory.length;

					const score = Math.round((state.score / totalQuestions) * 100);

					progressStore.updateLessonProgress(
						state.selectedLessonType,
						score,
						state.lessonHistory.length,
						totalQuestions
					);
				}

				return {
					...state,
					currentView: 'results',
					quizActive: false
				};
			}),

		goBackToSelector: () => {
			if (timerInterval) {
				clearInterval(timerInterval);
				timerInterval = null;
			}

			set({
				...initialState
			});
		},

		startOver: () => {
			update((state) => ({
				...state,
				currentView: 'lesson'
			}));

			learnStore.startLesson();
		}
	};
};

export const learnStore = createLearnStore();

// Derived stores for convenience
export const currentQuestion = derived(learnStore, ($store) => $store.currentQuestionData);

export const currentAnswers = derived(learnStore, ($store) => $store.currentAnswerOptions);

export const quizProgress = derived(learnStore, ($store) => ({
	current: $store.currentQuestionIndex + 1,
	total: $store.totalQuestions,
	remainingTime: $store.remainingTime
}));

export const quizResults = derived(learnStore, ($store) => ({
	score: $store.score,
	total:
		$store.selectedMode === 'fixed_question' ? $store.totalQuestions : $store.lessonHistory.length,
	incorrectGuesses: $store.incorrectGuesses,
	history: $store.lessonHistory
}));
