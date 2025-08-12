<!--
	Question Generator Component

	Generates and displays quiz questions for different lesson types.
	Handles question content, answer options, and user interactions.
-->

<script lang="ts">
	import type { PictographData } from '$domain/PictographData';
	import { QuestionGeneratorService } from '$lib/services/learn/QuestionGeneratorService';
	import type { AnswerOption, LessonType, QuestionData } from '$lib/types/learn';
	import { AnswerFormat } from '$lib/types/learn';
	// Events are now handled via callbacks in props
	import AnswerButton from './AnswerButton.svelte';
	import AnswerPictograph from './AnswerPictograph.svelte';
	import PictographRenderer from './PictographRenderer.svelte';

	// Props
	interface Props {
		lessonType: LessonType;
		questionData?: QuestionData | null;
		showFeedback?: boolean;
		selectedAnswerId?: string | null;
		isAnswered?: boolean;
		onAnswerSelected?: (data: {
			answerId: string;
			answerContent: PictographData;
			isCorrect: boolean;
		}) => void;
		onNextQuestion?: () => void;
	}

	let {
		lessonType,
		questionData = null,
		showFeedback = false,
		selectedAnswerId = null,
		isAnswered = false,
		onAnswerSelected,
		onNextQuestion,
	}: Props = $props();

	// Reactive effect to generate question when needed
	$effect(() => {
		if (lessonType && !questionData) {
			generateNewQuestion();
		}
	});

	// Methods
	function generateNewQuestion() {
		try {
			questionData = QuestionGeneratorService.generateQuestion(lessonType);
		} catch (error) {
			console.error('Failed to generate question:', error);
		}
	}

	function handleAnswerClick(option: AnswerOption) {
		if (isAnswered) return;

		selectedAnswerId = option.id;
		onAnswerSelected?.({
			answerId: option.id,
			answerContent: option.content as PictographData,
			isCorrect: option.isCorrect,
		});
	}

	function handleNextQuestion() {
		// Reset state
		selectedAnswerId = null;
		showFeedback = false;
		isAnswered = false;

		// Generate new question
		generateNewQuestion();

		onNextQuestion?.();
	}

	function getAnswerClass(option: AnswerOption): string {
		if (!showFeedback) {
			return selectedAnswerId === option.id ? 'selected' : '';
		}

		if (option.isCorrect) {
			return 'correct';
		} else if (selectedAnswerId === option.id && !option.isCorrect) {
			return 'incorrect';
		}

		return 'disabled';
	}
</script>

<div class="question-generator">
	{#if questionData}
		<!-- Question Section -->
		<div class="question-section">
			<div class="question-prompt">
				<h3>{(questionData as any).questionPrompt || 'Choose the correct answer:'}</h3>
			</div>

			<div class="question-content">
				{#if (questionData as any).questionType === 'pictograph'}
					<PictographRenderer
						pictographData={(questionData as any).questionContent as PictographData}
					/>
				{:else if (questionData as any).questionType === 'letter'}
					<div class="letter-display">
						<span class="letter">{(questionData as any).questionContent}</span>
					</div>
				{:else}
					<div class="text-display">
						<p>{questionData.questionContent}</p>
					</div>
				{/if}
			</div>
		</div>

		<!-- Answer Section -->
		<div class="answer-section">
			<div
				class="answer-grid"
				class:button-grid={questionData.answerType === AnswerFormat.BUTTON}
			>
				{#each questionData.answerOptions as option (option.id)}
					<div class="answer-option {getAnswerClass(option)}">
						{#if (questionData as any).answerType === AnswerFormat.BUTTON}
							<AnswerButton
								content={option.content as string}
								isSelected={selectedAnswerId === option.id}
								isCorrect={option.isCorrect}
								{showFeedback}
								disabled={isAnswered}
								on:click={() => handleAnswerClick(option)}
							/>
						{:else if (questionData as any).answerType === AnswerFormat.PICTOGRAPH}
							<AnswerPictograph
								pictographData={option.content as PictographData}
								isSelected={selectedAnswerId === option.id}
								isCorrect={option.isCorrect}
								{showFeedback}
								disabled={isAnswered}
								on:click={() => handleAnswerClick(option)}
							/>
						{/if}
					</div>
				{/each}
			</div>
		</div>

		<!-- Feedback Section -->
		{#if showFeedback && isAnswered}
			<div class="feedback-section">
				{#if questionData.answerOptions.find((opt) => opt.id === selectedAnswerId)?.isCorrect}
					<div class="feedback correct">
						<span class="icon">✓</span>
						<span class="message">Correct!</span>
					</div>
				{:else}
					<div class="feedback incorrect">
						<span class="icon">✗</span>
						<span class="message">Incorrect. The correct answer is highlighted.</span>
					</div>
				{/if}

				<button class="next-button" onclick={handleNextQuestion}> Next Question </button>
			</div>
		{/if}
	{:else}
		<div class="loading">
			<p>Generating question...</p>
		</div>
	{/if}
</div>

<style>
	.question-generator {
		display: flex;
		flex-direction: column;
		gap: 2rem;
		padding: 1.5rem;
		height: 100%;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 12px;
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.question-section {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		text-align: center;
	}

	.question-prompt h3 {
		margin: 0;
		color: #ffffff;
		font-size: 1.25rem;
		font-weight: 500;
	}

	.question-content {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 120px;
		padding: 1rem;
		background: rgba(255, 255, 255, 0.03);
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.letter-display {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.letter {
		font-size: 4rem;
		font-weight: bold;
		color: #ffffff;
		text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
	}

	.text-display p {
		margin: 0;
		font-size: 1.125rem;
		color: #ffffff;
		line-height: 1.5;
	}

	.answer-section {
		flex: 1;
		display: flex;
		flex-direction: column;
	}

	.answer-grid {
		display: grid;
		gap: 1rem;
		grid-template-columns: repeat(2, 1fr);
		height: 100%;
	}

	.answer-grid.button-grid {
		grid-template-columns: repeat(2, 1fr);
	}

	.answer-option {
		transition: all 0.2s ease;
	}

	.answer-option.selected {
		transform: scale(1.02);
	}

	.answer-option.correct {
		animation: correctPulse 0.6s ease-in-out;
	}

	.answer-option.incorrect {
		animation: incorrectShake 0.6s ease-in-out;
	}

	.answer-option.disabled {
		opacity: 0.6;
		pointer-events: none;
	}

	.feedback-section {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		padding: 1rem;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.feedback {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 1.125rem;
		font-weight: 500;
	}

	.feedback.correct {
		color: #4ade80;
	}

	.feedback.incorrect {
		color: #f87171;
	}

	.feedback .icon {
		font-size: 1.5rem;
	}

	.next-button {
		padding: 0.75rem 2rem;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
		border: none;
		border-radius: 8px;
		font-size: 1rem;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.next-button:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
	}

	.loading {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 200px;
		color: #ffffff;
		font-size: 1.125rem;
	}

	@keyframes correctPulse {
		0%,
		100% {
			transform: scale(1);
		}
		50% {
			transform: scale(1.05);
		}
	}

	@keyframes incorrectShake {
		0%,
		100% {
			transform: translateX(0);
		}
		25% {
			transform: translateX(-5px);
		}
		75% {
			transform: translateX(5px);
		}
	}

	/* Responsive Design */
	@media (max-width: 768px) {
		.question-generator {
			padding: 1rem;
			gap: 1.5rem;
		}

		.answer-grid {
			grid-template-columns: 1fr;
		}

		.letter {
			font-size: 3rem;
		}

		.question-prompt h3 {
			font-size: 1.125rem;
		}
	}
</style>
