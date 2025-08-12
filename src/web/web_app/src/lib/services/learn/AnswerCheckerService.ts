/**
 * Answer Checker Service
 *
 * Validates user answers and provides feedback for quiz questions.
 * Handles different answer types and lesson-specific validation logic.
 */

import { AnswerFeedback, type AnswerOption, LessonType, type QuestionData } from '$lib/types/learn';

export interface AnswerResult {
	isCorrect: boolean;
	feedback: AnswerFeedback;
	message: string;
	correctAnswer?: unknown;
	explanation?: string;
}

export class AnswerCheckerService {
	/**
	 * Check if a user's answer is correct.
	 */
	static checkAnswer(
		questionData: QuestionData,
		userAnswer: unknown,
		selectedOption?: AnswerOption
	): AnswerResult {
		if (!questionData || userAnswer === null || userAnswer === undefined) {
			return {
				isCorrect: false,
				feedback: AnswerFeedback.NONE,
				message: 'No answer provided',
			};
		}

		switch (questionData.lessonType) {
			case LessonType.PICTOGRAPH_TO_LETTER:
				return this.checkPictographToLetterAnswer(questionData, userAnswer, selectedOption);
			case LessonType.LETTER_TO_PICTOGRAPH:
				return this.checkLetterToPictographAnswer(questionData, userAnswer, selectedOption);
			case LessonType.VALID_NEXT_PICTOGRAPH:
				return this.checkValidNextPictographAnswer(
					questionData,
					userAnswer,
					selectedOption
				);
			default:
				return {
					isCorrect: false,
					feedback: AnswerFeedback.NONE,
					message: 'Unknown lesson type',
				};
		}
	}

	/**
	 * Check pictograph-to-letter answer.
	 */
	private static checkPictographToLetterAnswer(
		questionData: QuestionData,
		userAnswer: unknown,
		_selectedOption?: AnswerOption
	): AnswerResult {
		const correctLetter = questionData.correctAnswer;
		const userLetter = typeof userAnswer === 'string' ? userAnswer : userAnswer?.toString();

		const isCorrect = userLetter?.toLowerCase() === (correctLetter as string)?.toLowerCase();

		const base = {
			isCorrect,
			feedback: isCorrect ? AnswerFeedback.CORRECT : AnswerFeedback.INCORRECT,
			message: isCorrect
				? `Correct! The letter is ${correctLetter}.`
				: `Incorrect. The correct letter is ${correctLetter}.`,
			correctAnswer: correctLetter,
		} as AnswerResult;
		if (!isCorrect) {
			(base as AnswerResult).explanation =
				`The pictograph represents the letter "${correctLetter}".`;
		}
		return base;
	}

	/**
	 * Check letter-to-pictograph answer.
	 */
	private static checkLetterToPictographAnswer(
		questionData: QuestionData,
		userAnswer: unknown,
		_selectedOption?: AnswerOption
	): AnswerResult {
		const correctPictograph = questionData.correctAnswer;
		const userPictograph = userAnswer;

		// Compare pictograph data
		const isCorrect = this.comparePictographs(
			userPictograph as Record<string, unknown>,
			correctPictograph as Record<string, unknown>
		);

		const base = {
			isCorrect,
			feedback: isCorrect ? AnswerFeedback.CORRECT : AnswerFeedback.INCORRECT,
			message: isCorrect
				? `Correct! You selected the right pictograph.`
				: `Incorrect. The correct pictograph is highlighted.`,
			correctAnswer: correctPictograph,
		} as AnswerResult;
		if (!isCorrect) {
			(base as AnswerResult).explanation =
				`The correct pictograph for "${questionData.questionContent}" has different start/end positions.`;
		}
		return base;
	}

	/**
	 * Check valid-next-pictograph answer.
	 */
	private static checkValidNextPictographAnswer(
		questionData: QuestionData,
		userAnswer: unknown,
		_selectedOption?: AnswerOption
	): AnswerResult {
		const initialPictograph = questionData.questionContent;
		const userPictograph = userAnswer;

		// Check if the user's pictograph can follow the initial one
		const isCorrect = this.canPictographFollow(
			initialPictograph as Record<string, unknown>,
			userPictograph as Record<string, unknown>
		);

		const base = {
			isCorrect,
			feedback: isCorrect ? AnswerFeedback.CORRECT : AnswerFeedback.INCORRECT,
			message: isCorrect
				? `Correct! This pictograph can follow the previous one.`
				: `Incorrect. The pictograph's start position must match the previous end position.`,
			correctAnswer: questionData.correctAnswer,
		} as AnswerResult;
		if (!isCorrect) {
			(base as AnswerResult).explanation =
				`The correct pictograph must start where the previous one ends (${(initialPictograph as Record<string, unknown>)?.end_pos}).`;
		}
		return base;
	}

	/**
	 * Compare two pictographs for equality.
	 */
	private static comparePictographs(
		pictograph1: Record<string, unknown>,
		pictograph2: Record<string, unknown>
	): boolean {
		if (!pictograph1 || !pictograph2) return false;

		return (
			pictograph1.letter === pictograph2.letter &&
			pictograph1.start_pos === pictograph2.start_pos &&
			pictograph1.end_pos === pictograph2.end_pos &&
			pictograph1.grid_mode === pictograph2.grid_mode
		);
	}

	/**
	 * Check if one pictograph can follow another.
	 */
	private static canPictographFollow(
		firstPictograph: Record<string, unknown>,
		secondPictograph: Record<string, unknown>
	): boolean {
		if (!firstPictograph || !secondPictograph) return false;

		// The second pictograph's start position must match the first's end position
		return firstPictograph.end_pos === secondPictograph.start_pos;
	}

	/**
	 * Get feedback message based on answer result.
	 */
	static getFeedbackMessage(result: AnswerResult): string {
		return result.message;
	}

	/**
	 * Get detailed explanation for incorrect answers.
	 */
	static getExplanation(result: AnswerResult): string | undefined {
		return result.explanation;
	}

	/**
	 * Validate answer format for a lesson type.
	 */
	static validateAnswerFormat(lessonType: LessonType, answer: unknown): boolean {
		switch (lessonType) {
			case LessonType.PICTOGRAPH_TO_LETTER:
				return typeof answer === 'string' && answer.length === 1;
			case LessonType.LETTER_TO_PICTOGRAPH:
				return Boolean(answer && typeof answer === 'object' && 'letter' in answer);
			case LessonType.VALID_NEXT_PICTOGRAPH:
				return Boolean(
					answer &&
						typeof answer === 'object' &&
						'start_pos' in answer &&
						'end_pos' in answer
				);
			default:
				return false;
		}
	}

	/**
	 * Get hint for a question (without revealing the answer).
	 */
	static getHint(questionData: QuestionData): string {
		switch (questionData.lessonType) {
			case LessonType.PICTOGRAPH_TO_LETTER:
				return 'Look at the pictograph carefully. What letter does it represent?';
			case LessonType.LETTER_TO_PICTOGRAPH:
				return 'Find the pictograph that matches the given letter.';
			case LessonType.VALID_NEXT_PICTOGRAPH:
				return 'The next pictograph must start where the current one ends.';
			default:
				return 'Choose the correct answer.';
		}
	}

	/**
	 * Calculate answer confidence score (0-1).
	 */
	static calculateConfidence(
		questionData: QuestionData,
		userAnswer: unknown,
		timeToAnswer: number
	): number {
		const result = this.checkAnswer(questionData, userAnswer);

		if (!result.isCorrect) return 0;

		// Base confidence on correctness and response time
		let confidence = 1.0;

		// Reduce confidence for very quick answers (might be guessing)
		if (timeToAnswer < 2000) {
			// Less than 2 seconds
			confidence *= 0.7;
		}

		// Reduce confidence for very slow answers (might be uncertain)
		if (timeToAnswer > 30000) {
			// More than 30 seconds
			confidence *= 0.8;
		}

		return Math.max(0, Math.min(1, confidence));
	}

	/**
	 * Get performance feedback based on answer patterns.
	 */
	static getPerformanceFeedback(
		correctAnswers: number,
		totalAnswers: number,
		averageTime: number
	): string {
		const accuracy = totalAnswers > 0 ? correctAnswers / totalAnswers : 0;

		if (accuracy >= 0.9) {
			if (averageTime < 5000) {
				return "Excellent! You're both accurate and fast.";
			} else {
				return 'Great accuracy! Try to answer a bit faster.';
			}
		} else if (accuracy >= 0.7) {
			return 'Good work! Keep practicing to improve your accuracy.';
		} else if (accuracy >= 0.5) {
			return "You're making progress. Take your time to think through each answer.";
		} else {
			return 'Keep practicing! Review the lesson materials if needed.';
		}
	}

	/**
	 * Analyze answer patterns to identify learning gaps.
	 */
	static analyzeLearningGaps(
		answerHistory: Array<{ questionData: QuestionData; isCorrect: boolean }>
	): string[] {
		const gaps: string[] = [];
		const lessonTypeStats: Record<LessonType, { correct: number; total: number }> = {
			[LessonType.PICTOGRAPH_TO_LETTER]: { correct: 0, total: 0 },
			[LessonType.LETTER_TO_PICTOGRAPH]: { correct: 0, total: 0 },
			[LessonType.VALID_NEXT_PICTOGRAPH]: { correct: 0, total: 0 },
		};

		// Analyze performance by lesson type
		answerHistory.forEach(({ questionData, isCorrect }) => {
			const stats = lessonTypeStats[questionData.lessonType];
			stats.total++;
			if (isCorrect) stats.correct++;
		});

		// Identify gaps
		Object.entries(lessonTypeStats).forEach(([lessonType, stats]) => {
			if (stats.total > 0) {
				const accuracy = stats.correct / stats.total;
				if (accuracy < 0.6) {
					switch (lessonType as LessonType) {
						case LessonType.PICTOGRAPH_TO_LETTER:
							gaps.push('Difficulty recognizing letters from pictographs');
							break;
						case LessonType.LETTER_TO_PICTOGRAPH:
							gaps.push('Difficulty matching letters to pictographs');
							break;
						case LessonType.VALID_NEXT_PICTOGRAPH:
							gaps.push('Difficulty understanding pictograph flow and connections');
							break;
					}
				}
			}
		});

		return gaps;
	}
}
